#!/bin/bash
#
# superreview.sh — multi-stage code review based on the ultrareview-bench h9
# preset (GPT-5.5 Pro r4, Pareto sweet-spot at 67.7% recall / 82.7% sev-w on
# snippet1.cs at ~$1.21 mid).
#
# Pipeline (10 LLM calls total):
#
#   Stage 1: discovery-small (parallel) — 7 small/cheap passes
#     • opencode-go-deepseek-flash analyst       (uncapped)
#     • opencode-go-qwen36-plus    analyst       (uncapped)
#     • opencode-go-qwen36-plus    lateral       (uncapped)
#     • opencode-go-deepseek-flash architecture  (uncapped, specialist)
#     • opencode-go-deepseek-flash correctness   (cap=10,    specialist)
#     • opencode-go-qwen36-plus    architecture  (cap=3,     specialist)
#     • opencode-go-qwen36-plus    security      (uncapped,  specialist)
#
#   Stage 2: discovery-frontier (parallel) — 2 hand-picked frontier add-ons
#     • opencode-gpt5.5-xhigh      analyst       (uncapped)  → adds GT-41/63
#     • claude-code (Opus 4.7 max) lateral       (uncapped)  → adds GT-43
#
#   Stage 3: dedup (deterministic) — union all findings into one XML
#
#   Stage 4: judge — claude-sonnet over the unioned XML, emits verdicts JSON
#
# Output: filtered findings (VALID + DOWNGRADE) as markdown or XML.
#
# Usage:
#   superreview.sh <file>                  # review a file on disk
#   superreview.sh --diff < git-diff       # review a unified diff from stdin
#   superreview.sh --xml <file>            # XML output
#   superreview.sh --dry-run <file>        # plan + check config; no LLM calls
#   superreview.sh --judge <agent-id> ..   # override judge (default claude-sonnet)
#   superreview.sh --keep-tmp <file>       # retain $RESP_DIR for inspection
#   superreview.sh --help
#
# Cost expectation: ~$0.90-1.50 on a 12KB file. Larger inputs scale roughly
# linearly with the discovery-pass count (10 calls, mostly small models).
#
# Exit codes:
#   0 — success
#   2 — partial: some discovery passes failed but >=1 succeeded; judge ran
#   3 — every discovery pass failed
#   4 — config error
#   5 — usage error
#   6 — judge failed
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
JUDGE_AGENT="claude-sonnet"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --xml)        OUTPUT_FORMAT="xml"; shift ;;
        --diff)       INPUT_KIND="diff"; shift ;;
        --dry-run)    DRY_RUN=1; shift ;;
        --keep-tmp)   KEEP_TMP=1; shift ;;
        --judge)      JUDGE_AGENT="$2"; shift 2 ;;
        -h|--help)    sed -n '2,40p' "$0"; exit 0 ;;
        --)           shift; INPUT_PATH="${1:-}"; break ;;
        -*)           echo -e "${RED}Error: unknown flag: $1${NC}" >&2; exit 5 ;;
        *)            INPUT_PATH="$1"; shift; break ;;
    esac
done

# ------ Discovery plan -----------------------------------------------------
# Format: agent|role|cap|prompt-template
SMALL_PASSES=(
    "opencode-go-deepseek-flash|analyst|uncapped|broad-analyst.txt"
    "opencode-go-qwen36-plus|analyst|uncapped|broad-analyst.txt"
    "opencode-go-qwen36-plus|lateral|uncapped|broad-lateral.txt"
    "opencode-go-deepseek-flash|architecture|uncapped|specialist.txt"
    "opencode-go-deepseek-flash|correctness|10|specialist.txt"
    "opencode-go-qwen36-plus|architecture|3|specialist.txt"
    "opencode-go-qwen36-plus|security|uncapped|specialist.txt"
)
FRONTIER_PASSES=(
    "opencode-gpt5.5-xhigh|analyst|uncapped|broad-analyst.txt"
    "claude-code|lateral|uncapped|broad-lateral.txt"
)

ALL_AGENTS_NEEDED=(
    "opencode-go-deepseek-flash"
    "opencode-go-qwen36-plus"
    "opencode-gpt5.5-xhigh"
    "claude-code"
    "$JUDGE_AGENT"
)

# ------ Config validation --------------------------------------------------
CONSILIUM_CONFIG="${CONSILIUM_CONFIG:-$SKILL_DIR/config.json}"
[[ -f "$CONSILIUM_CONFIG" ]] || { echo -e "${RED}Error: config not found: $CONSILIUM_CONFIG${NC}" >&2; exit 4; }

missing="$(python3 - <<PYEOF
import json, sys
needed = "${ALL_AGENTS_NEEDED[*]}".split()
agents = json.load(open("$CONSILIUM_CONFIG"))["agents"]
missing = [n for n in needed if n not in agents]
print(",".join(missing))
PYEOF
)"
if [[ -n "$missing" ]]; then
    echo -e "${RED}Error: agents not in config.json: $missing${NC}" >&2
    echo "Add these entries (see config.example.json) before running superreview." >&2
    exit 4
fi

# ------ Input loading ------------------------------------------------------
INPUT_LABEL=""
TMP_ROOT="$(mktemp -d -t "agents-consilium-superreview-XXXXXX")"
cleanup_root() { [[ -z "$KEEP_TMP" ]] && rm -rf "$TMP_ROOT" || echo -e "${YELLOW}[debug] keeping superreview tmp: $TMP_ROOT${NC}" >&2; }
trap cleanup_root EXIT

INPUT_BODY_FILE="$TMP_ROOT/input-body.txt"
SOURCE_FILE="$TMP_ROOT/source-original"

if [[ "$INPUT_KIND" == "diff" ]]; then
    if [[ -t 0 ]]; then
        echo -e "${RED}Error: --diff requires a unified diff on stdin${NC}" >&2
        exit 5
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
    echo -e "${RED}Error: no input (provide a file path or --diff with stdin)${NC}" >&2
    exit 5
fi

# ------ Plan ---------------------------------------------------------------
total_passes=$(( ${#SMALL_PASSES[@]} + ${#FRONTIER_PASSES[@]} ))
echo -e "${CYAN}superreview (h9): $total_passes discovery + 1 judge ($JUDGE_AGENT) on '$INPUT_LABEL'${NC}" >&2

if [[ -n "$DRY_RUN" ]]; then
    echo "" >&2
    echo "  Stage 1 — discovery-small (parallel):" >&2
    for p in "${SMALL_PASSES[@]}"; do echo "    $p" >&2; done
    echo "" >&2
    echo "  Stage 2 — discovery-frontier (parallel):" >&2
    for p in "${FRONTIER_PASSES[@]}"; do echo "    $p" >&2; done
    echo "" >&2
    echo "  Stage 3 — dedup (deterministic union)" >&2
    echo "  Stage 4 — judge: $JUDGE_AGENT" >&2
    echo "" >&2
    echo -e "${GREEN}DRY RUN: config + plan validated, no LLM calls made.${NC}" >&2
    exit 0
fi

# ------ Stage 1+2: dispatch all discovery passes in parallel ---------------
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

echo -e "${YELLOW}[Launching $total_passes discovery passes in parallel...]${NC}" >&2
for p in "${SMALL_PASSES[@]}";    do launch_pass "$p" "discovery-small"; done
for p in "${FRONTIER_PASSES[@]}"; do launch_pass "$p" "discovery-frontier"; done

succeeded=0; failed=0
for i in "${!PIDS[@]}"; do
    code=0
    wait "${PIDS[$i]}" || code=$?
    if [[ $code -eq 0 ]]; then succeeded=$((succeeded+1)); else failed=$((failed+1)); fi
done

if [[ $succeeded -eq 0 ]]; then
    echo -e "${RED}All $total_passes discovery passes failed.${NC}" >&2
    exit 3
fi

# ------ Stage 3: dedup -----------------------------------------------------
UNION_XML="$TMP_ROOT/findings-union.xml"
non_empty_outputs=()
for f in "${OUT_FILES[@]}"; do [[ -s "$f" ]] && non_empty_outputs+=("$f"); done

if [[ ${#non_empty_outputs[@]} -eq 0 ]]; then
    echo -e "${RED}All discovery outputs empty — nothing to judge.${NC}" >&2
    exit 3
fi

python3 "$LIB_DIR/dedup-findings.py" "$UNION_XML" "${non_empty_outputs[@]}" || {
    echo -e "${RED}dedup failed${NC}" >&2; exit 3;
}

# ------ Stage 4: judge -----------------------------------------------------
VERDICTS_JSON="$TMP_ROOT/verdicts.json"
echo -e "${YELLOW}[Running judge: $JUDGE_AGENT]${NC}" >&2
"$LIB_DIR/judge-runner.sh" \
    --agent "$JUDGE_AGENT" \
    --findings "$UNION_XML" \
    --source "$SOURCE_FILE" \
    --input-kind "$INPUT_KIND" \
    --out "$VERDICTS_JSON" || {
    echo -e "${RED}judge failed; emitting unfiltered union for triage.${NC}" >&2
    cat "$UNION_XML"
    exit 6
}

# ------ Render filtered output --------------------------------------------
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
    if not v:
        continue
    if v["verdict"] in ("VALID", "DOWNGRADE"):
        # Apply DOWNGRADE severity if present
        if v["verdict"] == "DOWNGRADE" and v.get("new_severity"):
            raw = re.sub(r'severity="[^"]*"', f'severity="{v["new_severity"]}"', raw, count=1)
        kept.append((idx, attrs, body, raw, v))

summary = verdicts.get("summary", {})
if fmt == "xml":
    print(f'<code-review-report total="{len(kept)}" source="{label}">')
    for idx, attrs, body, raw, v in kept:
        print(raw)
    print(f'<judge-summary valid="{summary.get("valid", 0)}" duplicate="{summary.get("duplicate", 0)}" false_positive="{summary.get("false_positive", 0)}" downgrade="{summary.get("downgrade", 0)}"/>')
    print('</code-review-report>')
else:
    print(f"# Code review (`{label}`)\n")
    print(f"**Judge:** {summary.get('valid', 0)} valid · {summary.get('duplicate', 0)} dup · {summary.get('false_positive', 0)} FP · {summary.get('downgrade', 0)} downgraded\n")
    if not kept:
        print("_No findings survived judge filtering._")
    severities = {"critical": [], "high": [], "medium": [], "low": []}
    for idx, attrs, body, raw, v in kept:
        sev = attrs.get("severity", "low")
        severities.setdefault(sev, []).append((idx, attrs, body, v))
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
            agent = attrs.get("source-agent", "?")
            role = attrs.get("source-role", "?")
            print(f"### [{line}] {title}")
            print(f"_{agent}/{role} · confidence {attrs.get('confidence','?')}_\n")
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
    echo -e "${YELLOW}superreview: $succeeded ok, $failed failed (judge ran on partial input)${NC}" >&2
    exit 2
fi
echo -e "${GREEN}superreview: $total_passes/$total_passes discovery passes ok${NC}" >&2
exit 0
