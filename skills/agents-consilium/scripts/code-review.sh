#!/bin/bash
#
# Code Review Mode for Consilium
#
# Runs N specialist passes across the enabled agents and returns findings with
# line anchors and a quoted-code check. There is no coordinator pass: the caller
# (you, or whatever agent invoked this) is expected to judge, dedup, and
# prioritize the findings.
#
# Two modes are supported:
#   basic        (default) — 2 specialists: security, correctness.
#   specialists  (opt-in)  — 5 specialists: security, correctness, performance,
#                            architecture, consistency. Modeled on CodeAlive's
#                            code_review crew (5 parallel specialists, no
#                            synthesizer). Higher quality, ~2.5× cost.
#
# Usage:
#   code-review.sh <file>                  # review a single file on disk (basic mode: 2 specialists)
#   code-review.sh --diff                  # read a unified diff from stdin
#   git diff HEAD | code-review.sh --diff  # same, piped
#   code-review.sh --xml <file>            # XML output (stable for agent consumers)
#   code-review.sh -a opencode-go-kimi <file>     # ad-hoc agent override
#   code-review.sh -a 'opencode-go-*' <file>      # glob: all OpenCode-Go agents
#   code-review.sh -x codex <file>                # subtract from defaults
#   code-review.sh --mode specialists <file>      # 5-specialist deep review
#   code-review.sh --help
#
# Options:
#   --diff               Treat input as a unified diff from stdin. Line anchors
#                        then refer to lines in the diff, not a specific file,
#                        and quoted-code validation is skipped.
#   --xml                Emit findings as <code-review-report> XML.
#                        Default is a markdown report grouped by severity.
#   --mode <basic|specialists>
#                        Specialization set. Default = "basic" (research-backed
#                        2 passes: security + correctness, fixed cost). Set to
#                        "specialists" to opt in to a 5-pass review modeled on
#                        CodeAlive's review crew (security + correctness +
#                        performance + architecture + consistency). Specialists
#                        mode is ~2.5× the LLM cost — use it for high-stakes
#                        reviews, not every diff. Default is unchanged so
#                        existing callers are not affected.
#   -a, --agents <ID|GLOB>
#                        Override the active agent set with this id or glob.
#                        Repeatable; comma-separated values also accepted.
#                        When given, the per-agent "enabled" flag in config.json
#                        is ignored — only matched agents run.
#   -x, --exclude <ID|GLOB>
#                        Subtract matching agents from the active set. Repeatable.
#   -h, --help           Show this help.
#
# Environment overrides:
#   CONSILIUM_AGENTS         Comma-separated --agents fallback when no -a is passed.
#   CONSILIUM_EXCLUDE        Comma-separated --exclude fallback when no -x is passed.
#   CONSILIUM_REVIEW_MODE    Default review mode (basic|specialists) when no --mode is passed.
#
# Behaviour:
#   - Mode "basic" (default): 2 specializations — security, correctness (the
#     research-backed pair; perf/architecture/consistency intentionally out of
#     scope to keep the fixed cost predictable).
#   - Mode "specialists" (opt-in): 5 specializations — security, correctness,
#     performance, architecture, consistency. Modeled on CodeAlive's
#     code_review crew (codealive.agents.server/src/crews/code_review). 5×
#     parallel passes; cost scales accordingly.
#   - Enabled agents are round-robin assigned (modulo) to specializations. With
#     fewer agents than specializations, agents are reused (one agent runs
#     multiple specializations sequentially).
#   - All findings are returned; no severity filtering (the caller filters).
#   - When input is a file on disk, every finding's <quoted-code> is cross-
#     checked against the real source; mismatches are flagged as
#     quote-valid="false" so you can drop likely hallucinations.
#
# Exit codes:
#   0 — run completed (even if zero findings). Check quote-valid per finding.
#   3 — every dispatched agent failed
#   4 — config error (missing config, no enabled agents, role unknown)
#   5 — usage error (missing input, unknown flag, file not found)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/config.sh"

OUTPUT_FORMAT="markdown"
INPUT_KIND="file"        # file | diff
INPUT_PATH=""
INCLUDE_PATTERNS=()
EXCLUDE_PATTERNS=()
REVIEW_MODE="${CONSILIUM_REVIEW_MODE:-basic}"   # basic | specialists

while [[ $# -gt 0 ]]; do
    case "$1" in
        --xml)       OUTPUT_FORMAT="xml"; shift ;;
        --diff)      INPUT_KIND="diff"; shift ;;
        --mode)      shift; REVIEW_MODE="${1:-}"; shift ;;
        --mode=*)    REVIEW_MODE="${1#--mode=}"; shift ;;
        -a|--agents|--agent)
                     shift
                     IFS=',' read -ra _parts <<< "${1:-}"
                     INCLUDE_PATTERNS+=("${_parts[@]}")
                     shift
                     ;;
        -x|--exclude)
                     shift
                     IFS=',' read -ra _parts <<< "${1:-}"
                     EXCLUDE_PATTERNS+=("${_parts[@]}")
                     shift
                     ;;
        -h|--help)   sed -n '2,78p' "$0"; exit $EXIT_OK ;;
        --)          shift; INPUT_PATH="${1:-}"; break ;;
        -*)          echo -e "${RED}Error: unknown flag: $1${NC}" >&2; exit $EXIT_USAGE ;;
        *)           INPUT_PATH="$1"; shift; break ;;
    esac
done

case "$REVIEW_MODE" in
    basic|specialists) ;;
    *)
        echo -e "${RED}Error: --mode must be 'basic' or 'specialists' (got: '$REVIEW_MODE')${NC}" >&2
        exit $EXIT_USAGE
        ;;
esac

if [[ ${#INCLUDE_PATTERNS[@]} -eq 0 && -n "${CONSILIUM_AGENTS:-}" ]]; then
    IFS=',' read -ra INCLUDE_PATTERNS <<< "$CONSILIUM_AGENTS"
fi
if [[ ${#EXCLUDE_PATTERNS[@]} -eq 0 && -n "${CONSILIUM_EXCLUDE:-}" ]]; then
    IFS=',' read -ra EXCLUDE_PATTERNS <<< "$CONSILIUM_EXCLUDE"
fi

config_validate || exit $EXIT_CONFIG_ERROR

# --- Load input ---
CODE_CONTENT=""
INPUT_SOURCE_LABEL=""
if [[ "$INPUT_KIND" == "diff" ]]; then
    if [[ -t 0 ]]; then
        echo -e "${RED}Error: --diff requires a unified diff on stdin${NC}" >&2
        exit $EXIT_USAGE
    fi
    CODE_CONTENT=$(cat)
    INPUT_SOURCE_LABEL="${INPUT_PATH:-(stdin diff)}"
elif [[ -n "$INPUT_PATH" ]]; then
    if [[ ! -f "$INPUT_PATH" ]]; then
        echo -e "${RED}Error: file not found: $INPUT_PATH${NC}" >&2
        exit $EXIT_USAGE
    fi
    CODE_CONTENT=$(cat "$INPUT_PATH")
    INPUT_SOURCE_LABEL="$INPUT_PATH"
else
    echo -e "${RED}Error: no input (provide a file path or --diff with stdin)${NC}" >&2
    exit $EXIT_USAGE
fi

# --- Determine agents (config "enabled" by default; --agents/--exclude override) ---
ALL_AGENTS=()
while IFS= read -r a; do
    [[ -n "$a" ]] && ALL_AGENTS+=("$a")
done < <(config_all_agents)

CANDIDATES=()
if [[ ${#INCLUDE_PATTERNS[@]} -gt 0 ]]; then
    for a in "${ALL_AGENTS[@]}"; do
        config_match_any "$a" "${INCLUDE_PATTERNS[@]}" && CANDIDATES+=("$a")
    done
    if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
        echo -e "${RED}Error: no agents matched --agents patterns: ${INCLUDE_PATTERNS[*]}${NC}" >&2
        echo "Configured agents: ${ALL_AGENTS[*]}" >&2
        exit $EXIT_CONFIG_ERROR
    fi
else
    while IFS= read -r a; do
        [[ -n "$a" ]] && CANDIDATES+=("$a")
    done < <(config_enabled_agents)
fi

ENABLED_AGENTS=()
if [[ ${#EXCLUDE_PATTERNS[@]} -gt 0 ]]; then
    for a in "${CANDIDATES[@]}"; do
        config_match_any "$a" "${EXCLUDE_PATTERNS[@]}" || ENABLED_AGENTS+=("$a")
    done
else
    ENABLED_AGENTS=("${CANDIDATES[@]}")
fi

if [[ ${#ENABLED_AGENTS[@]} -eq 0 ]]; then
    if [[ ${#INCLUDE_PATTERNS[@]} -gt 0 || ${#EXCLUDE_PATTERNS[@]} -gt 0 ]]; then
        echo -e "${RED}Error: no agents remain after include/exclude filters${NC}" >&2
    else
        echo -e "${RED}Error: no agents enabled in $CONSILIUM_CONFIG${NC}" >&2
    fi
    exit $EXIT_CONFIG_ERROR
fi

case "$REVIEW_MODE" in
    basic)        SPECIALIZATIONS=(security correctness) ;;
    specialists)  SPECIALIZATIONS=(security correctness performance architecture consistency) ;;
esac

# Fixed cost per mode: always exactly len(SPECIALIZATIONS) passes — regardless
# of how many agents are enabled in the config. Extra agents are intentionally
# ignored so adding a 3rd/4th agent does not inflate review cost.
# Agents are assigned to specializations via modulo round-robin: with fewer
# agents than roles, each agent runs multiple roles sequentially. With 2 roles
# this reduces to the original "first available, else first" behaviour, so
# basic mode is bit-identical to the pre-modulo implementation.
declare -a ASSIGN_AGENTS ASSIGN_ROLES
for i in "${!SPECIALIZATIONS[@]}"; do
    role="${SPECIALIZATIONS[$i]}"
    idx=$(( i % ${#ENABLED_AGENTS[@]} ))
    ASSIGN_AGENTS+=("${ENABLED_AGENTS[$idx]}")
    ASSIGN_ROLES+=("$role")
done

# --- Resolve backend script for each assigned agent ---
backend_script() {
    case "$1" in
        codex-cli)   echo "$SCRIPT_DIR/codex-query.sh" ;;
        gemini-cli)  echo "$SCRIPT_DIR/gemini-query.sh" ;;
        opencode)    echo "$SCRIPT_DIR/opencode-query.sh" ;;
        claude-code) echo "$SCRIPT_DIR/claude-query.sh" ;;
        *)           echo "" ;;
    esac
}

# --- Build the per-request user prompt ---
# Code content is wrapped in CDATA so quotes, angle brackets, and xml-like
# sequences in user code can't break the outer prompt framing.
make_prompt() {
    local kind="$1"
    local label="$2"
    local content="$3"

    # Line-numbered rendering for file input makes it easier for the agent to
    # pick correct line-start/line-end and quote the matching text.
    local body
    if [[ "$kind" == "file" ]]; then
        body=$(awk '{printf "%4d  %s\n", NR, $0}' <<< "$content")
    else
        body="$content"
    fi

    local escaped_body
    escaped_body="${body//]]>/]]]]><![CDATA[>}"

    cat <<PROMPT
<input kind="${kind}" source="${label}">
<![CDATA[
${escaped_body}
]]>
</input>

<task>
Perform a focused code review on the input above, restricted to your specialization.
Respond with ONE OR MORE <finding> elements in the exact schema below.
If you have no findings in your specialization, respond with a single self-closing <findings/> element and nothing else.
Do NOT add prose, headings, markdown, or XML outside the <finding> elements.
</task>

<schema>
<finding severity="critical|high|medium|low" category="security|correctness|performance|architecture|consistency" file="${label}" line-start="N" line-end="N" confidence="0.0..1.0">
  <title>one-sentence summary</title>
  <rationale><![CDATA[why this is an issue; include ONE reason this might be a false positive]]></rationale>
  <suggested-fix><![CDATA[concrete code or steps]]></suggested-fix>
  <quoted-code><![CDATA[the exact source text spanning lines line-start..line-end, taken verbatim from the input]]></quoted-code>
</finding>
</schema>

The category attribute MUST equal your specialization id exactly. Do not emit findings outside your specialization.

<severity_rubric>
Score each finding on TWO axes — worst-case impact, and likelihood/reachability — then map:

- **critical** — RCE, auth/trust-boundary bypass, data loss, or guaranteed production outage, AND exploitation is likely in the as-written code path. Merge blocker. Emit ONLY with a concrete exploit/dataflow trace.
- **high** — critical-tier impact gated by a non-trivial precondition (auth required, specific config, user interaction), OR moderate impact with high reachability (e.g. unhandled exception on a documented error path, resource leak that exhausts pools in prod). Fix before release.
- **medium** — limited impact (verbose error leakage, localized incorrectness, degraded-but-recoverable behavior), OR critical impact gated by implausible preconditions. Schedule; not a merge blocker.
- **low** — cosmetic, stylistic, defense-in-depth, or theoretical issues with minimal real-world impact. Optional / backlog. Suppress unless unambiguous.

Adjustments: downgrade one level on mitigating factors (auth required, non-default config, unusual interaction). Do NOT upgrade speculative findings — require a concrete PoC or trace to claim the higher tier.
</severity_rubric>

<rules>
- Cite real line numbers. quoted-code MUST match the input text at those lines exactly; the caller validates this.
- HALLUCINATION GATE: the finding MUST reference a symbol, expression, or construct that is actually present in <input>. Do not invent APIs, flags, parameters, or patterns that aren't there.
- ACTIONABILITY GATE: every finding MUST cite a concrete line range AND include a concrete <suggested-fix> (real code or a precise instruction). Vague advice ("be careful with user input", "consider refactoring") = suppress.
- FIX-CONSISTENCY GATE: for severity=critical|warning, re-read your rationale and suggested-fix as a pair. If the fix would not clearly eliminate the hypothesized defect, drop the finding (or downgrade to nit). An inability to write a coherent fix is a strong signal the defect is imaginary.
- Confidence MUST reflect genuine uncertainty. A finding you are not sure about belongs at confidence <= 0.6.
- Stay inside your specialization. Do not emit findings from other categories.
- No nits unless they are on the critical path of the specialization.
- OUTPUT CAP: emit at most 3 findings. If more candidates survive the gates, keep the top 3 by (severity, confidence). The caller prefers a short, high-signal list over exhaustive coverage.
- Tone: educational, not accusatory. Describe the issue and the fix; don't editorialize about the author.
- Keep rationale under 6 sentences.
- You have read-only access to the surrounding project directory. Use it: Read/Grep/Glob neighboring files, check call sites, look at tests, consult CLAUDE.md / README / config, and verify data flow before asserting a finding. Do not modify anything.
</rules>
PROMPT
}

# --- Dispatch in parallel ---
RESP_DIR=$(mktemp -d)
# Debug knob: set CONSILIUM_KEEP_TEMP=1 to retain raw per-agent responses
# under $RESP_DIR. Useful when debugging why a review returned zero findings.
if [[ -z "${CONSILIUM_KEEP_TEMP:-}" ]]; then
    trap "rm -rf '$RESP_DIR'" EXIT
else
    echo -e "${YELLOW}[debug] keeping temp dir: $RESP_DIR${NC}" >&2
fi

declare -a PIDS OUT_FILES ERR_FILES KEYS
total=${#ASSIGN_AGENTS[@]}
echo -e "${CYAN}  CODE REVIEW (mode=$REVIEW_MODE) — $total pass(es): ${ASSIGN_AGENTS[*]} / roles=${ASSIGN_ROLES[*]}${NC}" >&2
echo -e "${YELLOW}[Launching parallel specialist queries...]${NC}" >&2

for i in "${!ASSIGN_AGENTS[@]}"; do
    agent="${ASSIGN_AGENTS[$i]}"
    role="${ASSIGN_ROLES[$i]}"
    backend="$(config_get_field "$agent" backend)"
    script="$(backend_script "$backend")"
    key="${agent}.${role}"
    out="$RESP_DIR/${key}.out"
    err="$RESP_DIR/${key}.err"

    if [[ -z "$script" || ! -x "$script" ]]; then
        echo -e "${RED}Skipping '$agent/$role': backend '$backend' unavailable${NC}" >&2
        : > "$out"
        echo "backend unavailable: $backend" > "$err"
        PIDS+=("")
        OUT_FILES+=("$out"); ERR_FILES+=("$err"); KEYS+=("$key")
        continue
    fi

    prompt="$(make_prompt "$INPUT_KIND" "$INPUT_SOURCE_LABEL" "$CODE_CONTENT")"
    (
        CONSILIUM_AGENT_ID="$agent" \
        CONSILIUM_ROLE_OVERRIDE="$role" \
        CONSILIUM_SKIP_OUTPUT_TEMPLATE=1 \
        "$script" "$prompt" > "$out" 2>"$err"
    ) &
    PIDS+=("$!")
    OUT_FILES+=("$out"); ERR_FILES+=("$err"); KEYS+=("$key")
done

# --- Await ---
declare -a EXITS
failed=0
succeeded=0
for i in "${!PIDS[@]}"; do
    pid="${PIDS[$i]}"
    if [[ -z "$pid" ]]; then
        EXITS+=("$EXIT_CONFIG_ERROR")
        failed=$((failed+1))
        continue
    fi
    code=0
    wait "$pid" || code=$?
    EXITS+=("$code")
    if [[ $code -eq 0 ]]; then
        succeeded=$((succeeded+1))
    else
        failed=$((failed+1))
    fi
done

# --- Summary line to stderr ---
for i in "${!KEYS[@]}"; do
    key="${KEYS[$i]}"
    code="${EXITS[$i]}"
    if [[ $code -eq 0 ]]; then
        echo -e "${GREEN}[${key}] ok${NC}" >&2
    else
        echo -e "${RED}[${key}] failed (exit $code) — see ${ERR_FILES[$i]}${NC}" >&2
    fi
done

# If every pass failed, bail out before the validator chokes on empty input.
if [[ $succeeded -eq 0 ]]; then
    exit $EXIT_ALL_FAILED
fi

# --- Parse + validate + render ---
python3 "$SCRIPT_DIR/code_review_validate.py" \
    --input-kind "$INPUT_KIND" \
    --input-path "$INPUT_SOURCE_LABEL" \
    --output-format "$OUTPUT_FORMAT" \
    "$RESP_DIR"
