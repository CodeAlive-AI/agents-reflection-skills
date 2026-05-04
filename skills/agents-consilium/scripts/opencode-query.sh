#!/bin/bash
#
# OpenCode CLI Wrapper for Consilium
# Role and model are read from config.json (agent id "opencode").
# Runs opencode in read-only plan agent mode so it cannot modify files.
#
# Usage: ./opencode-query.sh "prompt" [context_file]
#        cat file.ts | ./opencode-query.sh "analyze this"
#        ./opencode-query.sh --help
#
# Overrides:
#   OPENCODE_MODEL   — override model from config
#   OPENCODE_AGENT   — override built-in opencode agent (default: plan)
#   OPENCODE_EFFORT  — provider-specific reasoning effort (e.g. high, max, minimal).
#                      Defaults to the "effort" field in config.json. If neither is
#                      set, or the value is "none"/empty, no --variant is passed
#                      and the provider's default is used. Models with no variants
#                      (e.g. qwen3.6-plus) MUST run without --variant; passing one
#                      causes opencode to reject the call (silent hang).
#
# Exit codes:
#   0 — success
#   4 — config error (opencode CLI missing, unknown role, missing config)
#   5 — usage error (missing prompt or unknown flag)
#   other — propagated from opencode
#
# Note: this script always executes when invoked. The `enabled` field in
# config.json is consulted only by `consensus-query.sh` to build the default
# agent set; direct invocation ignores it. To skip an agent in the default
# consensus, set `enabled: false` in config.json — that does NOT prevent
# direct invocation here, by design (single source of truth).
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/config.sh"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    sed -n '2,28p' "$0"
    exit $EXIT_OK
fi

config_validate || exit $EXIT_CONFIG_ERROR

AGENT_ID="${CONSILIUM_AGENT_ID:-opencode}"

MODEL="${OPENCODE_MODEL:-$(config_get_field "$AGENT_ID" model)}"
ROLE_ID="${CONSILIUM_ROLE_OVERRIDE:-$(config_get_field "$AGENT_ID" role)}"
LABEL="$(config_get_field "$AGENT_ID" label)"
LABEL="${LABEL:-OpenCode}"
BUILTIN_AGENT="${OPENCODE_AGENT:-plan}"
EFFORT="${OPENCODE_EFFORT:-$(config_get_field "$AGENT_ID" effort)}"
# "none" or empty → omit --variant entirely (provider default). Required for
# models whose variants list is empty (e.g. opencode-go/qwen3.6-plus); passing
# any --variant to such a model causes opencode to silently reject the call.
if [[ "$EFFORT" == "none" ]]; then
    EFFORT=""
fi

if ! ROLE_PROMPT="$(get_role_prompt "$ROLE_ID")"; then
    echo -e "${RED}Error: unknown role '$ROLE_ID' for opencode in config${NC}" >&2
    exit $EXIT_CONFIG_ERROR
fi

if ! command -v opencode &> /dev/null; then
    echo -e "${RED}Error: opencode CLI is not installed${NC}" >&2
    echo "Install from: https://opencode.ai" >&2
    exit $EXIT_CONFIG_ERROR
fi

PROMPT="${1:-}"
CONTEXT_FILE="${2:-}"

# If no positional prompt was given but stdin has content, treat stdin as
# the prompt itself (so `script.sh < prompt.txt` works). Reading it here
# also stops build_prompt from later re-adding the same content as a
# `--- Input ---` context block — that would duplicate the prompt.
# Dual case (PROMPT set + stdin) is unchanged: build_prompt still reads
# stdin and appends it as context.
if [[ -z "$PROMPT" && ! -t 0 ]]; then
    PROMPT=$(cat)
    [[ -n "$PROMPT" ]] && echo -e "${YELLOW}[note] no positional prompt; using stdin as the prompt${NC}" >&2
fi

if [[ -z "$PROMPT" ]]; then
    echo -e "${RED}Error: No prompt provided${NC}" >&2
    echo "Usage: $0 \"prompt\" [context_file]" >&2
    echo "       $0 < prompt.txt" >&2
    exit $EXIT_USAGE
fi

export FULL_PROMPT
FULL_PROMPT=$(build_prompt "$ROLE_PROMPT" "$PROMPT" "$CONTEXT_FILE")

echo -e "${YELLOW}[${LABEL}] Querying ${MODEL} via opencode (agent=${BUILTIN_AGENT}, effort=${EFFORT:-default}, role=${ROLE_ID})...${NC}" >&2

# Runs in the caller's CWD so opencode can freely inspect the real project.
# Writes are blocked by `--agent plan` (opencode's built-in read-only agent).
export OPENCODE_MODEL_RESOLVED="$MODEL"
export OPENCODE_BUILTIN_AGENT="$BUILTIN_AGENT"
export OPENCODE_EFFORT_RESOLVED="$EFFORT"

run_opencode() {
    local variant_arg=()
    # Only pass --variant if effort is explicitly set; empty = provider default.
    if [[ -n "$OPENCODE_EFFORT_RESOLVED" ]]; then
        variant_arg=(--variant "$OPENCODE_EFFORT_RESOLVED")
    fi
    opencode run \
        --agent "$OPENCODE_BUILTIN_AGENT" \
        -m "$OPENCODE_MODEL_RESOLVED" \
        "${variant_arg[@]}" \
        --format default \
        --dangerously-skip-permissions \
        "$FULL_PROMPT" 2>/dev/null
}

run_with_timeout "$LABEL" run_opencode
