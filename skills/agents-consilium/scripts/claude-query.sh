#!/bin/bash
#
# Claude Code CLI Wrapper for Consilium
# Role and model are read from config.json (agent id "claude-code").
# Runs `claude -p` in plan permission mode so it is read-only.
#
# Usage: ./claude-query.sh "prompt" [context_file]
#        cat file.ts | ./claude-query.sh "analyze this"
#        ./claude-query.sh --help
#
# Overrides:
#   CLAUDE_MODEL           — override model from config (alias like "opus" or full id)
#   CLAUDE_PERMISSION_MODE — override permission mode (default: plan)
#   CLAUDE_EFFORT          — reasoning effort level (low, medium, high, xhigh, max).
#                            Defaults to the "effort" field in config.json, or
#                            "max" if both env and config are empty (claude is the
#                            most capable backend; max effort is the sane default).
#
# Exit codes:
#   0 — success
#   4 — config error (claude CLI missing, unknown role, missing config)
#   5 — usage error (missing prompt or unknown flag)
#   other — propagated from claude CLI
#
# Note: this script always executes when invoked. The `enabled` field in
# config.json is consulted only by `consensus-query.sh` to build the default
# agent set; direct invocation ignores it.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/config.sh"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    sed -n '2,27p' "$0"
    exit $EXIT_OK
fi

config_validate || exit $EXIT_CONFIG_ERROR

AGENT_ID="${CONSILIUM_AGENT_ID:-claude-code}"

MODEL="${CLAUDE_MODEL:-$(config_get_field "$AGENT_ID" model)}"
ROLE_ID="${CONSILIUM_ROLE_OVERRIDE:-$(config_get_field "$AGENT_ID" role)}"
LABEL="$(config_get_field "$AGENT_ID" label)"
LABEL="${LABEL:-ClaudeCode}"
PERMISSION_MODE="${CLAUDE_PERMISSION_MODE:-plan}"
EFFORT="${CLAUDE_EFFORT:-$(config_get_field "$AGENT_ID" effort)}"
EFFORT="${EFFORT:-max}"

if ! ROLE_PROMPT="$(get_role_prompt "$ROLE_ID")"; then
    echo -e "${RED}Error: unknown role '$ROLE_ID' for claude-code in config${NC}" >&2
    exit $EXIT_CONFIG_ERROR
fi

if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: Claude Code CLI is not installed${NC}" >&2
    echo "Install from: https://docs.claude.com/claude-code" >&2
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

echo -e "${YELLOW}[${LABEL}] Querying ${MODEL} via claude -p (permission-mode=${PERMISSION_MODE}, effort=${EFFORT}, role=${ROLE_ID})...${NC}" >&2

# Runs in the caller's CWD so Claude can freely read the real project
# (Read/Grep/Glob/Bash read-only). Writes are blocked by --permission-mode plan.
export CLAUDE_MODEL_RESOLVED="$MODEL"
export CLAUDE_PERMISSION_MODE_RESOLVED="$PERMISSION_MODE"
export CLAUDE_EFFORT_RESOLVED="$EFFORT"

run_claude() {
    local effort_arg=()
    # Only pass --effort if explicitly set; empty = CLI default.
    if [[ -n "$CLAUDE_EFFORT_RESOLVED" ]]; then
        effort_arg=(--effort "$CLAUDE_EFFORT_RESOLVED")
    fi
    claude -p "$FULL_PROMPT" \
        --model "$CLAUDE_MODEL_RESOLVED" \
        --permission-mode "$CLAUDE_PERMISSION_MODE_RESOLVED" \
        "${effort_arg[@]}" \
        --output-format text 2>/dev/null
}

run_with_timeout "$LABEL" run_claude
