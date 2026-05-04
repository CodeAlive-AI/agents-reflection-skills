#!/bin/bash
#
# Consensus Query — opinions from every enabled agent in config.json, in parallel.
#
# Usage:
#   consensus-query.sh "question"
#   consensus-query.sh --xml "question"
#   cat file.ts | consensus-query.sh "review this code"   # prompt + stdin context
#   consensus-query.sh < prompt.txt                       # stdin = prompt itself
#   consensus-query.sh --prompt-file prompt.txt           # same, raw mode
#   consensus-query.sh -a codex -a opencode-go-kimi "question"
#   consensus-query.sh -a 'opencode-go-*' "question"
#   consensus-query.sh -x codex "question"
#   consensus-query.sh --list-agents        # dump plan as XML, no queries
#   consensus-query.sh --help
#
# The prompt is normally a POSITIONAL argument. If you don't pass one,
# stdin (if present) is used as the prompt instead. When both are given,
# stdin is treated as context appended to the prompt.
#
# Options:
#   --xml            Emit responses as <consilium-report> XML (stable for agent consumers).
#                    Default is a human-readable markdown report.
#   --list-agents    Print the current plan (all configured agents, enabled/disabled,
#                    with model/role/backend-available) as XML and exit 0.
#   --prompt-file <path>
#                    Send the file's contents to every agent VERBATIM. No principles,
#                    no role injection, no output template — exactly the prompt you wrote.
#                    Use this for benchmark / eval runs where wrapper-level differences
#                    between agents would confound results.
#   -a, --agents <ID|GLOB>
#                    Override the active agent set with this id or glob (e.g. 'opencode-go-*').
#                    Repeatable; comma-separated values also accepted (-a codex,opencode).
#                    When given, the per-agent "enabled" flag in config.json is ignored —
#                    only matched agents run.
#   -x, --exclude <ID|GLOB>
#                    Subtract matching agents from the active set. Repeatable.
#                    Combine with --agents for include-then-exclude composition.
#   -h, --help       Show this help.
#
# Environment overrides:
#   CONSILIUM_AGENTS    Comma-separated --agents fallback when no -a is passed.
#   CONSILIUM_EXCLUDE   Comma-separated --exclude fallback when no -x is passed.
#
# Exit codes:
#   0 — all queried agents succeeded (or --list-agents completed)
#   2 — partial failure (at least one agent succeeded, at least one failed)
#   3 — every queried agent failed
#   4 — config error (missing config, no enabled agents, unknown backend)
#   5 — usage error (missing prompt, unknown flag)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/config.sh"

OUTPUT_FORMAT="markdown"  # markdown | xml
LIST_ONLY=false
PROMPT=""
PROMPT_FILE=""
INCLUDE_PATTERNS=()
EXCLUDE_PATTERNS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --xml)          OUTPUT_FORMAT="xml"; shift ;;
        --list-agents)  LIST_ONLY=true; shift ;;
        --prompt-file)  shift; PROMPT_FILE="${1:-}"; shift ;;
        -a|--agents|--agent)
                        shift
                        IFS=',' read -ra _parts <<< "${1:-}"
                        INCLUDE_PATTERNS+=("${_parts[@]}")
                        shift
                        ;;
        -x|--exclude)   shift
                        IFS=',' read -ra _parts <<< "${1:-}"
                        EXCLUDE_PATTERNS+=("${_parts[@]}")
                        shift
                        ;;
        -h|--help)      sed -n '2,50p' "$0"; exit $EXIT_OK ;;
        --)             shift; PROMPT="${1:-}"; break ;;
        -*)             echo -e "${RED}Error: unknown flag: $1${NC}" >&2; exit $EXIT_USAGE ;;
        *)              PROMPT="$1"; shift; break ;;
    esac
done

# --prompt-file: load file content as the prompt and switch backends to RAW mode
# (no principles / role / template wrapping).
if [[ -n "$PROMPT_FILE" ]]; then
    if [[ ! -f "$PROMPT_FILE" ]]; then
        echo -e "${RED}Error: prompt file not found: $PROMPT_FILE${NC}" >&2
        exit $EXIT_USAGE
    fi
    if [[ -n "$PROMPT" ]]; then
        echo -e "${RED}Error: cannot combine --prompt-file with a positional prompt${NC}" >&2
        exit $EXIT_USAGE
    fi
    PROMPT="$(cat "$PROMPT_FILE")"
    export CONSILIUM_RAW_PROMPT=1
fi

# Env-var fallbacks (only when no CLI flag of the same kind was given).
if [[ ${#INCLUDE_PATTERNS[@]} -eq 0 && -n "${CONSILIUM_AGENTS:-}" ]]; then
    IFS=',' read -ra INCLUDE_PATTERNS <<< "$CONSILIUM_AGENTS"
fi
if [[ ${#EXCLUDE_PATTERNS[@]} -eq 0 && -n "${CONSILIUM_EXCLUDE:-}" ]]; then
    IFS=',' read -ra EXCLUDE_PATTERNS <<< "$CONSILIUM_EXCLUDE"
fi

config_validate || exit $EXIT_CONFIG_ERROR

# --list-agents: emit plan and exit.
if $LIST_ONLY; then
    config_xml_plan
    exit $EXIT_OK
fi

# Capture piped input once. We read stdin BEFORE the PROMPT check so that
# `consensus-query.sh < prompt.txt` and `cat prompt.txt | consensus-query.sh`
# work as expected — without a positional, stdin is the prompt itself.
# When BOTH a positional prompt and stdin are present, stdin keeps its
# original meaning (context to the prompt) — that's the existing pattern
# `cat code.py | consensus-query.sh "review this"`.
STDIN_CONTENT=""
if [[ ! -t 0 ]]; then
    STDIN_CONTENT=$(cat)
fi

if [[ -z "$PROMPT" && -n "$STDIN_CONTENT" ]]; then
    PROMPT="$STDIN_CONTENT"
    STDIN_CONTENT=""
    echo -e "${YELLOW}[note] no positional prompt; using stdin as the prompt${NC}" >&2
fi

if [[ -z "$PROMPT" ]]; then
    echo -e "${RED}Error: No prompt provided${NC}" >&2
    echo "Usage: $0 [--xml] \"question\"" >&2
    echo "       $0 [--xml] < prompt.txt" >&2
    echo "       $0 [--xml] --prompt-file path.txt" >&2
    exit $EXIT_USAGE
fi

# Resolve the query script path for a given agent backend.
backend_script() {
    case "$1" in
        codex-cli)   echo "$SCRIPT_DIR/codex-query.sh" ;;
        gemini-cli)  echo "$SCRIPT_DIR/gemini-query.sh" ;;
        opencode)    echo "$SCRIPT_DIR/opencode-query.sh" ;;
        claude-code) echo "$SCRIPT_DIR/claude-query.sh" ;;
        *)           echo "" ;;
    esac
}

ALL_AGENTS=()
while IFS= read -r a; do
    [[ -n "$a" ]] && ALL_AGENTS+=("$a")
done < <(config_all_agents)

# Build candidate set: --agents overrides config's "enabled" field.
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

# Apply --exclude.
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

echo -e "${CYAN}  CONSENSUS QUERY — ${#ENABLED_AGENTS[@]} agent(s) in parallel: ${ENABLED_AGENTS[*]}${NC}" >&2
echo -e "${YELLOW}[Launching parallel queries...]${NC}" >&2

declare -a AGENT_IDS PIDS OUT_FILES ERR_FILES LABELS MODELS ROLES BACKENDS STATUSES EXITS

for agent in "${ENABLED_AGENTS[@]}"; do
    backend="$(config_get_field "$agent" backend)"
    script="$(backend_script "$backend")"
    label="$(config_get_field "$agent" label)"; label="${label:-$agent}"
    model="$(config_get_field "$agent" model)"
    role="$(config_get_field "$agent" role)"

    AGENT_IDS+=("$agent")
    LABELS+=("$label")
    MODELS+=("$model")
    ROLES+=("$role")
    BACKENDS+=("$backend")

    # Loud override notice: an agent with enabled=false reaches this loop
    # only when --agents/--exclude pulled it in. Print it so the override
    # is visible (AX: no silent override).
    if ! config_is_enabled "$agent"; then
        echo -e "${YELLOW}[${label}] forced via --agents (enabled=false in config)${NC}" >&2
    fi

    if [[ -z "$script" || ! -x "$script" ]]; then
        echo -e "${RED}Skipping '$agent': unknown/unavailable backend '$backend'${NC}" >&2
        STATUSES+=("skipped")
        EXITS+=("$EXIT_CONFIG_ERROR")
        OUT_FILES+=("")
        ERR_FILES+=("")
        PIDS+=("")
        continue
    fi

    out=$(mktemp)
    err=$(mktemp)
    if [[ -n "$STDIN_CONTENT" ]]; then
        echo "$STDIN_CONTENT" | CONSILIUM_AGENT_ID="$agent" "$script" "$PROMPT" > "$out" 2>"$err" &
    else
        CONSILIUM_AGENT_ID="$agent" "$script" "$PROMPT" > "$out" 2>"$err" &
    fi

    STATUSES+=("pending")
    EXITS+=("0")
    OUT_FILES+=("$out")
    ERR_FILES+=("$err")
    PIDS+=("$!")
done

cleanup() {
    for f in "${OUT_FILES[@]:-}" "${ERR_FILES[@]:-}"; do
        [[ -n "$f" ]] && rm -f "$f"
    done
}
trap cleanup EXIT

# Wait for all dispatched agents and record exit codes.
for i in "${!AGENT_IDS[@]}"; do
    [[ "${STATUSES[$i]}" == "skipped" ]] && continue
    pid="${PIDS[$i]}"
    [[ -z "$pid" ]] && continue
    code=0
    wait "$pid" || code=$?
    EXITS[$i]="$code"
    # Empty stdout with exit 0 is never a real answer. We compare bytes, not
    # `-s`, because run_with_timeout always emits two newlines as a header
    # before the actual response body — so the file is never strictly zero.
    out_bytes=$(wc -c < "${OUT_FILES[$i]}" | tr -d ' ')
    if [[ $code -eq 0 && $out_bytes -gt 10 ]]; then
        STATUSES[$i]="ok"
    elif [[ $code -eq 0 ]]; then
        EXITS[$i]=66  # EX_NOINPUT
        STATUSES[$i]="failed"
        echo -e "${RED}[${LABELS[$i]}] empty response (${out_bytes} bytes), marking failed${NC}" >&2
    else
        STATUSES[$i]="failed"
    fi
done

# Count outcomes (queried agents only).
queried=0
succeeded=0
failed=0
for i in "${!AGENT_IDS[@]}"; do
    case "${STATUSES[$i]}" in
        ok)      queried=$((queried+1)); succeeded=$((succeeded+1)) ;;
        failed)  queried=$((queried+1)); failed=$((failed+1)) ;;
        skipped) queried=$((queried+1)); failed=$((failed+1)) ;;
    esac
done

# -------- Render report --------
if [[ "$OUTPUT_FORMAT" == "xml" ]]; then
    echo "<consilium-report prompt-length=\"${#PROMPT}\">"
    # Queried agents (enabled).
    for i in "${!AGENT_IDS[@]}"; do
        agent="${AGENT_IDS[$i]}"
        label="${LABELS[$i]}"
        model="${MODELS[$i]}"
        role="${ROLES[$i]}"
        backend="${BACKENDS[$i]}"
        status="${STATUSES[$i]}"
        code="${EXITS[$i]}"
        printf '  <agent id="%s" label="%s" backend="%s" model="%s" role="%s" status="%s" exit-code="%s">\n' \
            "$(printf '%s' "$agent"   | xml_escape)" \
            "$(printf '%s' "$label"   | xml_escape)" \
            "$(printf '%s' "$backend" | xml_escape)" \
            "$(printf '%s' "$model"   | xml_escape)" \
            "$(printf '%s' "$role"    | xml_escape)" \
            "$status" "$code"
        case "$status" in
            ok)
                printf '    <response>'
                cat "${OUT_FILES[$i]}" | cdata_wrap
                printf '</response>\n'
                ;;
            failed)
                printf '    <error>'
                cat "${ERR_FILES[$i]}" | cdata_wrap
                printf '</error>\n'
                ;;
            skipped)
                printf '    <error>Backend %s unavailable</error>\n' \
                    "$(printf '%s' "$backend" | xml_escape)"
                ;;
        esac
        echo "  </agent>"
    done
    # Disabled agents, for agent-consumer introspection.
    for agent in "${ALL_AGENTS[@]}"; do
        in_enabled=false
        for a in "${ENABLED_AGENTS[@]}"; do
            [[ "$a" == "$agent" ]] && in_enabled=true && break
        done
        $in_enabled && continue
        label="$(config_get_field "$agent" label)"; label="${label:-$agent}"
        model="$(config_get_field "$agent" model)"
        role="$(config_get_field "$agent" role)"
        backend="$(config_get_field "$agent" backend)"
        if config_is_enabled "$agent"; then
            status_attr="filtered"  # enabled in config but excluded at runtime
        else
            status_attr="disabled"
        fi
        printf '  <agent id="%s" label="%s" backend="%s" model="%s" role="%s" status="%s"/>\n' \
            "$(printf '%s' "$agent"   | xml_escape)" \
            "$(printf '%s' "$label"   | xml_escape)" \
            "$(printf '%s' "$backend" | xml_escape)" \
            "$(printf '%s' "$model"   | xml_escape)" \
            "$(printf '%s' "$role"    | xml_escape)" \
            "$status_attr"
    done
    echo "</consilium-report>"
else
    for i in "${!AGENT_IDS[@]}"; do
        label="${LABELS[$i]}"
        model="${MODELS[$i]}"
        status="${STATUSES[$i]}"
        code="${EXITS[$i]}"
        echo ""
        echo "## ${label} Response (${model})"
        echo ""
        case "$status" in
            ok)      cat "${OUT_FILES[$i]}" ;;
            failed)  echo "[${label} query failed with exit code $code]"; cat "${ERR_FILES[$i]}" ;;
            skipped) echo "[${label} skipped: backend unavailable]" ;;
        esac
    done
    # Inactive block (config-disabled or runtime-filtered).
    inactive_any=false
    for agent in "${ALL_AGENTS[@]}"; do
        in_enabled=false
        for a in "${ENABLED_AGENTS[@]}"; do
            [[ "$a" == "$agent" ]] && in_enabled=true && break
        done
        $in_enabled && continue
        $inactive_any || { echo ""; echo "## Inactive agents (not queried)"; echo ""; inactive_any=true; }
        label="$(config_get_field "$agent" label)"; label="${label:-$agent}"
        model="$(config_get_field "$agent" model)"
        if config_is_enabled "$agent"; then
            reason="filtered by --agents/--exclude"
        else
            reason="disabled in config"
        fi
        echo "- ${label} (${model}) — ${reason}"
    done
    echo ""
    echo "---"
    echo "END OF CONSENSUS REPORT"
fi

# -------- Exit code --------
if [[ $succeeded -eq $queried ]]; then
    exit $EXIT_OK
elif [[ $succeeded -eq 0 ]]; then
    exit $EXIT_ALL_FAILED
else
    exit $EXIT_PARTIAL
fi
