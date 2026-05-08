#!/bin/bash
#
# ultrareview.sh — multi-stage code review based on the ultrareview-bench h3
# preset (Codex gpt-5.5 broad-grid + probe; best severity-weighted recall on
# snippet1.cs at ~$1.47-2.96).
#
# Pipeline (21 LLM calls total):
#
#   Stage 1: broad (parallel) — 4 frontier analysts
#     • codex (gpt-5.5 high)         analyst       (uncapped)
#     • claude-code (Opus 4.7 max)   analyst       (uncapped)
#     • opencode (gemini-3.1-pro)    lateral       (uncapped)
#     • opencode-go-deepseek (Pro)   analyst       (uncapped)
#
#   Stage 2: specialists (parallel) — 5×3 matrix, uniform cap=10
#     3 small models × 5 roles (security, correctness, performance,
#     architecture, consistency). Models: deepseek-flash, qwen36-plus,
#     gemini-3-flash.
#
#   Stage 3: probe (sequential) — 1 generic gap probe
#     • opencode-go-deepseek-flash auditor (cap=10) on the generic prompt
#       (model picks the highest-risk defect class for THIS input)
#
#   Stage 4: dedup (deterministic) — union all findings
#
#   Stage 5: judge — claude-code (Opus) by default; on failure falls back to
#     opencode-gpt5.5-xhigh (which was the rescue judge in the bench).
#
# Output: filtered findings (VALID + DOWNGRADE) as markdown or XML.
#
# Usage:
#   ultrareview.sh <file>                  # review a file on disk
#   ultrareview.sh --diff < git-diff       # unified diff from stdin
#   ultrareview.sh --xml <file>            # XML output
#   ultrareview.sh --dry-run <file>        # plan + check config; no LLM calls
#   ultrareview.sh --judge <agent-id> ..   # override judge (default claude-code)
#   ultrareview.sh --no-fallback ..        # disable judge fallback
#   ultrareview.sh --keep-tmp <file>       # retain $RESP_DIR
#   ultrareview.sh --help
#
# Cost expectation: ~$1.50-3.00 on a 12KB file. The Opus judge is the
# expensive component (~$0.50-1.00); fallback to opencode-gpt5.5-xhigh is
# slightly cheaper (~$0.40-0.50) and proved more reliable in the bench.
#
# Exit codes:
#   0 — success
#   2 — partial: some discovery passes failed; judge ran
#   3 — every discovery pass failed
#   4 — config error
#   5 — usage error
#   6 — judge failed (and fallback also failed, if enabled)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LIB_DIR="$SCRIPT_DIR/lib"
PROMPTS_DIR="$SKILL_DIR/prompts"

source "$SCRIPT_DIR/common.sh" 2>/dev/null || true
: "${RED:=$'\033[0;31m'}" "${GREEN:=$'\033[0;32m'}" "${YELLOW:=$'\033[1;33m'}" "${CYAN:=$'\033[0;36m'}" "${NC:=$'\033[0m'}"

OUTPUT_FORMAT="markdown"
INPUT_KIND="file"
INPUT_PATH=""
DRY_RUN=""
KEEP_TMP=""
JUDGE_AGENT="claude-code"
JUDGE_FALLBACK="opencode-gpt5.5-xhigh"
NO_FALLBACK=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --xml)         OUTPUT_FORMAT="xml"; shift ;;
        --diff)        INPUT_KIND="diff"; shift ;;
        --dry-run)     DRY_RUN=1; shift ;;
        --keep-tmp)    KEEP_TMP=1; shift ;;
        --judge)       JUDGE_AGENT="$2"; shift 2 ;;
        --no-fallback) NO_FALLBACK=1; shift ;;
        -h|--help)     sed -n '2,45p' "$0"; exit 0 ;;
        --)            shift; INPUT_PATH="${1:-}"; break ;;
        -*)            echo -e "${RED}Error: unknown flag: $1${NC}" >&2; exit 5 ;;
        *)             INPUT_PATH="$1"; shift; break ;;
    esac
done

# ------ Discovery plan -----------------------------------------------------
BROAD_PASSES=(
    "codex|analyst|uncapped|broad-analyst.txt"
    "claude-code|analyst|uncapped|broad-analyst.txt"
    "opencode|lateral|uncapped|broad-lateral.txt"
    "opencode-go-deepseek|analyst|uncapped|broad-analyst.txt"
)

SPECIALIST_ROLES=(security correctness performance architecture consistency)
SPECIALIST_MODELS=(opencode-go-deepseek-flash opencode-go-qwen36-plus opencode-gemini-3-flash)

PROBE_PASS="opencode-go-deepseek-flash|auditor|10|probe-generic.txt"

ALL_AGENTS_NEEDED=(
    "codex" "claude-code" "opencode" "opencode-go-deepseek"
    "opencode-go-deepseek-flash" "opencode-go-qwen36-plus" "opencode-gemini-3-flash"
    "$JUDGE_AGENT"
)
[[ -z "$NO_FALLBACK" ]] && ALL_AGENTS_NEEDED+=("$JUDGE_FALLBACK")

# ------ Config validation --------------------------------------------------
CONSILIUM_CONFIG="${CONSILIUM_CONFIG:-$SKILL_DIR/config.json}"
[[ -f "$CONSILIUM_CONFIG" ]] || { echo -e "${RED}Error: config not found: $CONSILIUM_CONFIG${NC}" >&2; exit 4; }

missing="$(python3 - <<PYEOF
import json, sys
needed = "${ALL_AGENTS_NEEDED[*]}".split()
agents = json.load(open("$CONSILIUM_CONFIG"))["agents"]
print(",".join([n for n in needed if n not in agents]))
PYEOF
)"
if [[ -n "$missing" ]]; then
    echo -e "${RED}Error: agents not in config.json: $missing${NC}" >&2
    exit 4
fi

# ------ Input loading ------------------------------------------------------
INPUT_LABEL=""
TMP_ROOT="$(mktemp -d -t "agents-consilium-ultrareview-XXXXXX")"
cleanup_root() { [[ -z "$KEEP_TMP" ]] && rm -rf "$TMP_ROOT" || echo -e "${YELLOW}[debug] keeping ultrareview tmp: $TMP_ROOT${NC}" >&2; }
trap cleanup_root EXIT

INPUT_BODY_FILE="$TMP_ROOT/input-body.txt"
SOURCE_FILE="$TMP_ROOT/source-original"

if [[ "$INPUT_KIND" == "diff" ]]; then
    if [[ -t 0 ]]; then
        echo -e "${RED}Error: --diff requires a unified diff on stdin${NC}" >&2; exit 5
    fi
    cat > "$SOURCE_FILE"
    cp "$SOURCE_FILE" "$INPUT_BODY_FILE"
    INPUT_LABEL="${INPUT_PATH:-(stdin diff)}"
elif [[ -n "$INPUT_PATH" ]]; then
    [[ -f "$INPUT_PATH" ]] || { echo -e "${RED}Error: file not found: $INPUT_PATH${NC}" >&2; exit 5; }
    cp "$INPUT_PATH" "$SOURCE_FILE"
    awk '{printf "%4d  %s\n", NR, $0}' "$INPUT_PATH" > "$INPUT_BODY_FILE"
    INPUT_LABEL="$INPUT_PATH"
else
    echo -e "${RED}Error: no input${NC}" >&2; exit 5
fi

# Build full specialist plan
SPECIALIST_PASSES=()
for model in "${SPECIALIST_MODELS[@]}"; do
    for role in "${SPECIALIST_ROLES[@]}"; do
        SPECIALIST_PASSES+=("${model}|${role}|10|specialist.txt")
    done
done

total_discovery=$(( ${#BROAD_PASSES[@]} + ${#SPECIALIST_PASSES[@]} + 1 ))
echo -e "${CYAN}ultrareview (h3): $total_discovery discovery + 1 judge ($JUDGE_AGENT) on '$INPUT_LABEL'${NC}" >&2

if [[ -n "$DRY_RUN" ]]; then
    echo "" >&2
    echo "  Stage 1 — broad (parallel):" >&2
    for p in "${BROAD_PASSES[@]}"; do echo "    $p" >&2; done
    echo "" >&2
    echo "  Stage 2 — specialists (parallel, 5×3 matrix, uniform cap=10):" >&2
    for p in "${SPECIALIST_PASSES[@]}"; do echo "    $p" >&2; done
    echo "" >&2
    echo "  Stage 3 — probe (sequential):" >&2
    echo "    $PROBE_PASS" >&2
    echo "" >&2
    echo "  Stage 4 — dedup (deterministic union)" >&2
    if [[ -z "$NO_FALLBACK" ]]; then
        echo "  Stage 5 — judge: $JUDGE_AGENT (fallback: $JUDGE_FALLBACK)" >&2
    else
        echo "  Stage 5 — judge: $JUDGE_AGENT (no fallback)" >&2
    fi
    echo "" >&2
    echo -e "${GREEN}DRY RUN: config + plan validated, no LLM calls made.${NC}" >&2
    exit 0
fi

# ------ Stage 1+2: parallel discovery --------------------------------------
RESP_DIR="$TMP_ROOT/responses"
mkdir -p "$RESP_DIR"

declare -a PIDS LABELS OUT_FILES
launch_pass() {
    local triple="$1" stage="$2"
    local agent role cap prompt_name
    IFS='|' read -r agent role cap prompt_name <<< "$triple"
    local out_file="$RESP_DIR/${stage}__${agent}__${role}.xml"
    "$LIB_DIR/discovery-pass.sh" \
        --agent "$agent" --role "$role" --cap "$cap" \
        --prompt "$PROMPTS_DIR/$prompt_name" \
        --input-kind "$INPUT_KIND" \
        --input-label "$INPUT_LABEL" \
        --input-body-file "$INPUT_BODY_FILE" \
        --out "$out_file" &
    PIDS+=("$!")
    LABELS+=("$stage:$agent/$role")
    OUT_FILES+=("$out_file")
}

echo -e "${YELLOW}[Launching broad + specialists in parallel ($((${#BROAD_PASSES[@]} + ${#SPECIALIST_PASSES[@]})) passes)...]${NC}" >&2
for p in "${BROAD_PASSES[@]}";      do launch_pass "$p" "broad"; done
for p in "${SPECIALIST_PASSES[@]}"; do launch_pass "$p" "specialists"; done

succeeded=0; failed=0
for i in "${!PIDS[@]}"; do
    code=0; wait "${PIDS[$i]}" || code=$?
    if [[ $code -eq 0 ]]; then succeeded=$((succeeded+1)); else failed=$((failed+1)); fi
done

# ------ Stage 3: probe (sequential after parallel completes) ---------------
echo -e "${YELLOW}[Running generic probe...]${NC}" >&2
probe_out="$RESP_DIR/probe__opencode-go-deepseek-flash__auditor.xml"
probe_code=0
"$LIB_DIR/discovery-pass.sh" \
    --agent "opencode-go-deepseek-flash" --role "auditor" --cap "10" \
    --prompt "$PROMPTS_DIR/probe-generic.txt" \
    --input-kind "$INPUT_KIND" \
    --input-label "$INPUT_LABEL" \
    --input-body-file "$INPUT_BODY_FILE" \
    --out "$probe_out" || probe_code=$?
if [[ $probe_code -eq 0 ]]; then succeeded=$((succeeded+1)); else failed=$((failed+1)); fi
OUT_FILES+=("$probe_out")

if [[ $succeeded -eq 0 ]]; then
    echo -e "${RED}All $total_discovery discovery passes failed.${NC}" >&2
    exit 3
fi

# ------ Stage 4: dedup -----------------------------------------------------
UNION_XML="$TMP_ROOT/findings-union.xml"
non_empty_outputs=()
for f in "${OUT_FILES[@]}"; do [[ -s "$f" ]] && non_empty_outputs+=("$f"); done

if [[ ${#non_empty_outputs[@]} -eq 0 ]]; then
    echo -e "${RED}All discovery outputs empty — nothing to judge.${NC}" >&2; exit 3
fi

python3 "$LIB_DIR/dedup-findings.py" "$UNION_XML" "${non_empty_outputs[@]}" || {
    echo -e "${RED}dedup failed${NC}" >&2; exit 3;
}

# ------ Stage 5: judge with fallback ---------------------------------------
VERDICTS_JSON="$TMP_ROOT/verdicts.json"
judge_ok=""
echo -e "${YELLOW}[Running primary judge: $JUDGE_AGENT]${NC}" >&2
if "$LIB_DIR/judge-runner.sh" \
        --agent "$JUDGE_AGENT" \
        --findings "$UNION_XML" \
        --source "$SOURCE_FILE" \
        --input-kind "$INPUT_KIND" \
        --out "$VERDICTS_JSON"; then
    judge_ok=1
else
    echo -e "${RED}Primary judge ($JUDGE_AGENT) failed.${NC}" >&2
    if [[ -z "$NO_FALLBACK" ]]; then
        echo -e "${YELLOW}[Falling back to: $JUDGE_FALLBACK]${NC}" >&2
        if "$LIB_DIR/judge-runner.sh" \
                --agent "$JUDGE_FALLBACK" \
                --findings "$UNION_XML" \
                --source "$SOURCE_FILE" \
                --input-kind "$INPUT_KIND" \
                --out "$VERDICTS_JSON"; then
            judge_ok=1
        fi
    fi
fi

if [[ -z "$judge_ok" ]]; then
    echo -e "${RED}Both primary and fallback judge failed; emitting unfiltered union.${NC}" >&2
    cat "$UNION_XML"
    exit 6
fi

# ------ Render filtered output (same as superreview) ----------------------
python3 - "$UNION_XML" "$VERDICTS_JSON" "$OUTPUT_FORMAT" "$INPUT_LABEL" <<'PYEOF'
import json, re, sys
union_path, verdicts_path, fmt, label = sys.argv[1:5]
union_text = open(union_path).read()
verdicts = json.load(open(verdicts_path))

FINDING_RE = re.compile(r'<finding\b([^>]*)>(.*?)</finding>', re.DOTALL)
ATTR_RE = re.compile(r'(\w+(?:-\w+)*)="([^"]*)"')

findings = []
for m in FINDING_RE.finditer(union_text):
    attrs = dict(ATTR_RE.findall(m.group(1)))
    body = m.group(2)
    findings.append((int(attrs.get("index", "0")), attrs, body, m.group(0)))

verdict_by_idx = {v["finding_idx"]: v for v in verdicts.get("verdicts", [])}
kept = []
for idx, attrs, body, raw in findings:
    v = verdict_by_idx.get(idx)
    if not v: continue
    if v["verdict"] in ("VALID", "DOWNGRADE"):
        if v["verdict"] == "DOWNGRADE" and v.get("new_severity"):
            raw = re.sub(r'severity="[^"]*"', f'severity="{v["new_severity"]}"', raw, count=1)
        kept.append((idx, attrs, body, raw, v))

summary = verdicts.get("summary", {})
if fmt == "xml":
    print(f'<code-review-report total="{len(kept)}" source="{label}">')
    for _, _, _, raw, _ in kept: print(raw)
    print(f'<judge-summary valid="{summary.get("valid", 0)}" duplicate="{summary.get("duplicate", 0)}" false_positive="{summary.get("false_positive", 0)}" downgrade="{summary.get("downgrade", 0)}"/>')
    print('</code-review-report>')
else:
    print(f"# Code review (`{label}`)\n")
    print(f"**Judge:** {summary.get('valid', 0)} valid · {summary.get('duplicate', 0)} dup · {summary.get('false_positive', 0)} FP · {summary.get('downgrade', 0)} downgraded\n")
    if not kept:
        print("_No findings survived judge filtering._")
    severities = {"critical": [], "high": [], "medium": [], "low": []}
    for idx, attrs, body, raw, v in kept:
        severities.setdefault(attrs.get("severity", "low"), []).append((idx, attrs, body, v))
    for sev in ("critical", "high", "medium", "low"):
        items = severities.get(sev, [])
        if not items: continue
        print(f"\n## {sev.title()} ({len(items)})\n")
        for idx, attrs, body, v in items:
            title_m = re.search(r"<title>(.*?)</title>", body, re.DOTALL)
            title = title_m.group(1).strip() if title_m else "(no title)"
            line = f"L{attrs.get('line-start','?')}"
            line_end = attrs.get('line-end', '')
            if line_end and line_end != attrs.get('line-start',''):
                line += f"-{line_end}"
            print(f"### [{line}] {title}")
            print(f"_{attrs.get('source-agent','?')}/{attrs.get('source-role','?')} · confidence {attrs.get('confidence','?')}_\n")
            for tag, hdr in (("rationale", "**Why:**"), ("suggested-fix", "**Fix:**"), ("quoted-code", "**Code:**")):
                m = re.search(rf"<{tag}>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{tag}>", body, re.DOTALL)
                if m:
                    txt = m.group(1).strip()
                    if tag == "quoted-code":
                        print(f"{hdr}\n```\n{txt}\n```\n")
                    else:
                        print(f"{hdr} {txt}\n")
            print()
PYEOF

if [[ $failed -gt 0 ]]; then
    echo -e "${YELLOW}ultrareview: $succeeded ok, $failed failed (judge ran on partial input)${NC}" >&2
    exit 2
fi
echo -e "${GREEN}ultrareview: $total_discovery/$total_discovery discovery passes ok${NC}" >&2
exit 0
