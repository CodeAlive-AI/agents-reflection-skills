#!/bin/bash
#
# discovery-pass.sh — run ONE discovery pass (broad-analyst | broad-lateral |
# specialist | probe). Used by superreview.sh and ultrareview.sh.
#
# Usage:
#   discovery-pass.sh \
#     --agent <agent-id> --role <role> --cap <N|uncapped> \
#     --prompt <prompt-template.txt> \
#     --input-kind <file|diff> --input-label <label> \
#     --input-body-file <path-to-line-numbered-or-raw-body> \
#     --out <output.xml>
#
# Behaviour:
#   - Renders {{INPUT_KIND}}, {{INPUT_LABEL}}, {{INPUT_BODY}}, {{ROLE}},
#     {{CAP_DIRECTIVE}} into the chosen prompt.
#   - Resolves backend via $CONSILIUM_CONFIG (default: skill's config.json).
#   - Tmp-isolates: creates a fresh /tmp dir, cd's into it before invoking
#     the backend, cleans up unless --keep-tmp.
#   - Writes the agent's raw stdout (which should contain <finding> XML
#     elements per the prompt schema) directly to --out.
#
# Exit codes:
#   0 — backend ok, output written
#   1 — backend produced empty output
#   3 — backend invocation failed
#   4 — config error
#   5 — usage error
#
set -euo pipefail

LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$(dirname "$LIB_DIR")"
SKILL_DIR="$(dirname "$SCRIPTS_DIR")"

if [[ -f "$SCRIPTS_DIR/common.sh" ]]; then source "$SCRIPTS_DIR/common.sh"; fi
: "${RED:=$'\033[0;31m'}" "${GREEN:=$'\033[0;32m'}" "${YELLOW:=$'\033[1;33m'}" "${CYAN:=$'\033[0;36m'}" "${NC:=$'\033[0m'}"

AGENT=""; ROLE=""; CAP="uncapped"; PROMPT=""
INPUT_KIND="file"; INPUT_LABEL=""; INPUT_BODY_FILE=""; OUT=""; KEEP_TMP=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent)             AGENT="$2"; shift 2 ;;
        --role)              ROLE="$2"; shift 2 ;;
        --cap)               CAP="$2"; shift 2 ;;
        --prompt)            PROMPT="$2"; shift 2 ;;
        --input-kind)        INPUT_KIND="$2"; shift 2 ;;
        --input-label)       INPUT_LABEL="$2"; shift 2 ;;
        --input-body-file)   INPUT_BODY_FILE="$2"; shift 2 ;;
        --out)               OUT="$2"; shift 2 ;;
        --keep-tmp)          KEEP_TMP=1; shift ;;
        -h|--help)           sed -n '2,30p' "$0"; exit 0 ;;
        *)                   echo -e "${RED}Error: unknown flag: $1${NC}" >&2; exit 5 ;;
    esac
done

for var in AGENT ROLE PROMPT INPUT_LABEL INPUT_BODY_FILE OUT; do
    [[ -n "${!var}" ]] || { echo -e "${RED}Error: --${var,,} required${NC}" >&2; exit 5; }
done
[[ -f "$PROMPT" ]]          || { echo -e "${RED}Error: prompt not found: $PROMPT${NC}" >&2; exit 4; }
[[ -f "$INPUT_BODY_FILE" ]] || { echo -e "${RED}Error: body file not found: $INPUT_BODY_FILE${NC}" >&2; exit 4; }

CONSILIUM_CONFIG="${CONSILIUM_CONFIG:-$SKILL_DIR/config.json}"
[[ -f "$CONSILIUM_CONFIG" ]] || { echo -e "${RED}Error: config not found: $CONSILIUM_CONFIG${NC}" >&2; exit 4; }

BACKEND="$(python3 -c "
import json, sys
d = json.load(open('$CONSILIUM_CONFIG'))['agents']
if '$AGENT' not in d:
    sys.stderr.write('agent not in config: $AGENT\n'); sys.exit(1)
print(d['$AGENT']['backend'])
")" || exit 4

case "$BACKEND" in
    codex-cli)   BACKEND_SCRIPT="$SCRIPTS_DIR/codex-query.sh" ;;
    gemini-cli)  BACKEND_SCRIPT="$SCRIPTS_DIR/gemini-query.sh" ;;
    opencode)    BACKEND_SCRIPT="$SCRIPTS_DIR/opencode-query.sh" ;;
    claude-code) BACKEND_SCRIPT="$SCRIPTS_DIR/claude-query.sh" ;;
    *)           echo -e "${RED}Error: unknown backend '$BACKEND'${NC}" >&2; exit 4 ;;
esac
[[ -x "$BACKEND_SCRIPT" ]] || { echo -e "${RED}Error: backend script not executable: $BACKEND_SCRIPT${NC}" >&2; exit 4; }

# Cap directive — same wording as the harness.
if [[ "$CAP" == "uncapped" || "$CAP" == "0" ]]; then
    CAP_DIRECTIVE="OUTPUT: no upper bound on the number of findings. Emit every distinct, defensible finding that survives the gates above."
else
    CAP_DIRECTIVE="OUTPUT CAP: emit at most $CAP findings. If more candidates survive the gates, keep the top $CAP by (severity, confidence)."
fi

TMP_DIR="$(mktemp -d -t "agents-consilium-pass-XXXXXX")"
cleanup() { [[ -z "$KEEP_TMP" ]] && rm -rf "$TMP_DIR" || echo -e "${YELLOW}[debug] keeping tmp: $TMP_DIR${NC}" >&2; }
trap cleanup EXIT

export DP_INPUT_KIND="$INPUT_KIND"
export DP_INPUT_LABEL="$INPUT_LABEL"
export DP_INPUT_BODY_FILE="$INPUT_BODY_FILE"
export DP_ROLE="$ROLE"
export DP_CAP_DIRECTIVE="$CAP_DIRECTIVE"
RENDERED_PROMPT="$(python3 - "$PROMPT" <<'PYEOF'
import os, sys
tpl = open(sys.argv[1]).read()
body = open(os.environ['DP_INPUT_BODY_FILE']).read()
out = (tpl
       .replace('{{INPUT_KIND}}',    os.environ.get('DP_INPUT_KIND', ''))
       .replace('{{INPUT_LABEL}}',   os.environ.get('DP_INPUT_LABEL', ''))
       .replace('{{INPUT_BODY}}',    body)
       .replace('{{ROLE}}',          os.environ.get('DP_ROLE', ''))
       .replace('{{CAP_DIRECTIVE}}', os.environ.get('DP_CAP_DIRECTIVE', '')))
sys.stdout.write(out)
PYEOF
)"

mkdir -p "$(dirname "$OUT")"
RAW_ERR="$TMP_DIR/raw-err.txt"

(
    cd "$TMP_DIR"
    export CONSILIUM_AGENT_ID="$AGENT"
    export CONSILIUM_ROLE_OVERRIDE="$ROLE"
    export CONSILIUM_SKIP_OUTPUT_TEMPLATE=1
    export CODEX_FIRST_BYTE_DEADLINE="${ULTRAREVIEW_FIRST_BYTE:-900}"
    "$BACKEND_SCRIPT" "$RENDERED_PROMPT" > "$OUT" 2> "$RAW_ERR"
) || {
    rc=$?
    echo -e "${RED}[$AGENT/$ROLE] backend failed (exit $rc)${NC}" >&2
    [[ -s "$RAW_ERR" ]] && head -20 "$RAW_ERR" >&2
    exit 3
}

if [[ ! -s "$OUT" ]]; then
    echo -e "${RED}[$AGENT/$ROLE] empty output${NC}" >&2
    exit 1
fi

n="$(grep -c "<finding\b" "$OUT" 2>/dev/null || echo 0)"
echo -e "${GREEN}[$AGENT/$ROLE] ok → $n finding(s)${NC}" >&2
exit 0
