#!/bin/bash
#
# judge-runner.sh — production judge pass for ultrareview/superreview modes.
#
# Reads a unioned <code-review-report> XML, the original source under review,
# and runs ONE LLM call that emits a JSON verdicts object (VALID / DUPLICATE /
# FALSE_POSITIVE / DOWNGRADE per finding). No ground-truth comparison — this
# is for production code review, not benchmark scoring.
#
# Usage:
#   judge-runner.sh \
#     --agent <agent-id-from-config.json> \
#     --findings <unioned.xml> \
#     --source <file-or-diff-source> \
#     --input-kind <file|diff> \
#     --out <verdicts.json> \
#     [--prompt <judge.txt>] [--keep-tmp]
#
# Exit codes:
#   0 — success, valid JSON written
#   1 — backend produced empty output
#   2 — JSON failed schema validation (no `verdicts` array)
#   3 — backend invocation failed
#   4 — config error (agent or prompt missing)
#   5 — usage error
#
set -euo pipefail

LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$(dirname "$LIB_DIR")"
SKILL_DIR="$(dirname "$SCRIPTS_DIR")"

# Pick up colour helpers if the calling skill defines them.
if [[ -f "$SCRIPTS_DIR/common.sh" ]]; then source "$SCRIPTS_DIR/common.sh"; fi
: "${RED:=$'\033[0;31m'}" "${GREEN:=$'\033[0;32m'}" "${YELLOW:=$'\033[1;33m'}" "${CYAN:=$'\033[0;36m'}" "${NC:=$'\033[0m'}"

AGENT=""
FINDINGS=""
SOURCE=""
INPUT_KIND="file"
OUT=""
PROMPT="$SKILL_DIR/prompts/judge.txt"
KEEP_TMP=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent)       AGENT="$2"; shift 2 ;;
        --findings)    FINDINGS="$2"; shift 2 ;;
        --source)      SOURCE="$2"; shift 2 ;;
        --input-kind)  INPUT_KIND="$2"; shift 2 ;;
        --out)         OUT="$2"; shift 2 ;;
        --prompt)      PROMPT="$2"; shift 2 ;;
        --keep-tmp)    KEEP_TMP=1; shift ;;
        -h|--help)     sed -n '2,30p' "$0"; exit 0 ;;
        *)             echo -e "${RED}Error: unknown flag: $1${NC}" >&2; exit 5 ;;
    esac
done

for var in AGENT FINDINGS SOURCE OUT; do
    [[ -n "${!var}" ]] || { echo -e "${RED}Error: --${var,,} required${NC}" >&2; exit 5; }
done
[[ -f "$FINDINGS" ]] || { echo -e "${RED}Error: findings xml not found: $FINDINGS${NC}" >&2; exit 4; }
[[ -f "$PROMPT"   ]] || { echo -e "${RED}Error: judge prompt not found: $PROMPT${NC}" >&2; exit 4; }

# Resolve backend script via skill's config.json — same pattern as code-review.sh
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

# --- Tmp-isolated execution ------------------------------------------------
TMP_DIR="$(mktemp -d -t "agents-consilium-judge-XXXXXX")"
cleanup() { [[ -z "$KEEP_TMP" ]] && rm -rf "$TMP_DIR" || echo -e "${YELLOW}[debug] keeping tmp: $TMP_DIR${NC}" >&2; }
trap cleanup EXIT

# Render judge prompt with placeholders. SOURCE may be a path (file mode) or
# the literal diff text already on disk (we accept either — "--source" points
# to whatever was reviewed, line-numbered for verification).
INPUT_LABEL="$SOURCE"
if [[ -f "$SOURCE" ]]; then
    if [[ "$INPUT_KIND" == "file" ]]; then
        INPUT_BODY="$(awk '{printf "%4d  %s\n", NR, $0}' "$SOURCE")"
    else
        INPUT_BODY="$(cat "$SOURCE")"
    fi
else
    # SOURCE is a raw label (e.g. "(stdin diff)") — input body must be
    # piped via $JUDGE_INPUT_BODY env var to keep this script stdin-free.
    INPUT_BODY="${JUDGE_INPUT_BODY:-}"
fi

FINDINGS_BODY="$(cat "$FINDINGS")"

# Substitute placeholders via python — bash parameter expansion would choke on
# the XML/CDATA/braces inside the bodies. We hand the values to python through
# env vars (single quoted heredoc, no shell interpolation needed).
export JR_INPUT_KIND="$INPUT_KIND"
export JR_INPUT_LABEL="$INPUT_LABEL"
export JR_INPUT_BODY="$INPUT_BODY"
export JR_FINDINGS_BODY="$FINDINGS_BODY"
RENDERED_PROMPT="$(python3 - "$PROMPT" <<'PYEOF'
import os, sys
tpl = open(sys.argv[1]).read()
out = (tpl
       .replace('{{INPUT_KIND}}',    os.environ.get('JR_INPUT_KIND', ''))
       .replace('{{INPUT_LABEL}}',   os.environ.get('JR_INPUT_LABEL', ''))
       .replace('{{INPUT_BODY}}',    os.environ.get('JR_INPUT_BODY', ''))
       .replace('{{FINDINGS_BODY}}', os.environ.get('JR_FINDINGS_BODY', '')))
sys.stdout.write(out)
PYEOF
)"

RAW_OUT="$TMP_DIR/raw-out.txt"
RAW_ERR="$TMP_DIR/raw-err.txt"

(
    cd "$TMP_DIR"
    export CONSILIUM_AGENT_ID="$AGENT"
    export CONSILIUM_ROLE_OVERRIDE="analyst"
    export CONSILIUM_SKIP_OUTPUT_TEMPLATE=1
    export CODEX_FIRST_BYTE_DEADLINE="${ULTRAREVIEW_FIRST_BYTE:-900}"
    "$BACKEND_SCRIPT" "$RENDERED_PROMPT" > "$RAW_OUT" 2> "$RAW_ERR"
) || {
    rc=$?
    echo -e "${RED}[judge/$AGENT] backend failed (exit $rc)${NC}" >&2
    [[ -s "$RAW_ERR" ]] && head -30 "$RAW_ERR" >&2
    exit 3
}

[[ -s "$RAW_OUT" ]] || { echo -e "${RED}[judge/$AGENT] empty output${NC}" >&2; exit 1; }

# Extract JSON object (strip ```json fences or grab first balanced {...}).
mkdir -p "$(dirname "$OUT")"
python3 - "$RAW_OUT" > "$OUT" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1]).read()
fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
candidate = fence.group(1) if fence else raw
if not fence:
    start = candidate.find("{")
    if start < 0:
        sys.stderr.write("no JSON object found in judge output\n"); sys.exit(2)
    depth = 0
    for i, c in enumerate(candidate[start:], start=start):
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                candidate = candidate[start:i+1]; break
    else:
        sys.stderr.write("unbalanced braces in judge output\n"); sys.exit(2)
try:
    obj = json.loads(candidate)
except Exception as e:
    sys.stderr.write(f"json parse failed: {e}\n"); sys.exit(2)
if "verdicts" not in obj or not isinstance(obj["verdicts"], list):
    sys.stderr.write("judge output missing 'verdicts' array\n"); sys.exit(2)
print(json.dumps(obj, indent=2))
PYEOF

[[ -s "$OUT" ]] || { echo -e "${RED}[judge/$AGENT] JSON extraction failed${NC}" >&2; exit 2; }
echo -e "${GREEN}[judge/$AGENT] ok → $OUT${NC}" >&2
exit 0
