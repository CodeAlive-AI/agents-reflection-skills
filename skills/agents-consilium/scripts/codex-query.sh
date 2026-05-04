#!/bin/bash
#
# Codex CLI Wrapper for Consilium
# Role and model are read from config.json (agent id "codex").
#
# Usage: ./codex-query.sh "prompt" [context_file]
#        cat file.ts | ./codex-query.sh "analyze this"
#        ./codex-query.sh --help
#
# Exit codes:
#   0 — success
#   4 — config error (missing config, unknown role, CLI not installed)
#   5 — usage error (missing prompt or unknown flag)
#   other — propagated from codex CLI (e.g. 124 on timeout)
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
    sed -n '2,18p' "$0"
    exit $EXIT_OK
fi

config_validate || exit $EXIT_CONFIG_ERROR

AGENT_ID="${CONSILIUM_AGENT_ID:-codex}"

MODEL="${CODEX_MODEL:-$(config_get_field "$AGENT_ID" model)}"
ROLE_ID="${CONSILIUM_ROLE_OVERRIDE:-$(config_get_field "$AGENT_ID" role)}"
LABEL="$(config_get_field "$AGENT_ID" label)"
LABEL="${LABEL:-Codex}"
EFFORT="${CODEX_EFFORT:-$(config_get_field "$AGENT_ID" effort)}"
EFFORT="${EFFORT:-high}"

if ! ROLE_PROMPT="$(get_role_prompt "$ROLE_ID")"; then
    echo -e "${RED}Error: unknown role '$ROLE_ID' for codex in config${NC}" >&2
    exit $EXIT_CONFIG_ERROR
fi

if ! command -v codex &> /dev/null; then
    echo -e "${RED}Error: Codex CLI is not installed${NC}" >&2
    echo "Install from: https://github.com/openai/codex" >&2
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

echo -e "${YELLOW}[${LABEL}] Querying ${MODEL} (role=${ROLE_ID}, effort=${EFFORT})...${NC}" >&2

export MODEL
export CODEX_EFFORT_RESOLVED="$EFFORT"
export CODEX_TMPOUT=$(mktemp)
trap "rm -f $CODEX_TMPOUT" EXIT

run_codex() {
    # Runs in the caller's CWD so the agent can freely read the real project
    # (codebase search, git log, CLAUDE.md, etc.). Sandbox is pinned to
    # read-only so it cannot modify files; -a never keeps it non-interactive.
    local codex_stderr
    codex_stderr=$(mktemp)
    local effort_args=()
    if [[ -n "$CODEX_EFFORT_RESOLVED" ]]; then
        effort_args=(-c "model_reasoning_effort=\"$CODEX_EFFORT_RESOLVED\"")
    fi
    local nomcp_args=()
    # CONSILIUM_CODEX_NO_MCP=1 → bypass ~/.codex/config.toml entirely. Use this
    # for benchmark / eval runs where global MCP servers (e.g. oh-my-codex) can
    # deadlock at init. See codex-hang-postmortem in docs.
    if [[ -n "${CONSILIUM_CODEX_NO_MCP:-}" ]]; then
        nomcp_args=(--ignore-user-config)
    fi
    codex -a never "${effort_args[@]}" exec \
        "${nomcp_args[@]}" \
        --model "$MODEL" \
        --sandbox read-only \
        --skip-git-repo-check \
        --ephemeral \
        -o "$CODEX_TMPOUT" \
        "$FULL_PROMPT" >/dev/null 2>"$codex_stderr" &
    local codex_pid=$!
    # Liveness watchdog: was 0-byte $CODEX_TMPOUT, but `-o` file is written only at the very
    # end (codex doesn't stream the final message). On xhigh/long-reasoning runs the file
    # legitimately stays empty for minutes, and the watchdog killed productive work.
    # Switch to monitoring $codex_stderr instead — codex emits progress logs there from the
    # start (model spinner, MCP init, sandbox setup). Pre-first-byte hangs (MCP deadlock,
    # missing auth) keep stderr empty too, which is the actual signal we want.
    (
        local elapsed=0
        while kill -0 "$codex_pid" 2>/dev/null; do
            sleep 10; elapsed=$((elapsed+10))
            if [[ $elapsed -ge $CODEX_FIRST_BYTE_DEADLINE ]] && [[ ! -s "$codex_stderr" ]]; then
                echo "[Codex] watchdog: 0-byte stderr after ${elapsed}s (pre-first-byte hang), killing pid $codex_pid" >&2
                kill -TERM "$codex_pid" 2>/dev/null
                sleep 5
                kill -KILL "$codex_pid" 2>/dev/null
                exit 0
            fi
        done
    ) &
    local watchdog_pid=$!
    wait "$codex_pid"; local exit_code=$?
    kill "$watchdog_pid" 2>/dev/null; wait "$watchdog_pid" 2>/dev/null
    if [[ $exit_code -ne 0 ]]; then
        echo "[Codex] Error (exit $exit_code):" >&2
        cat "$codex_stderr" >&2
    fi
    rm -f "$codex_stderr"
    cat "$CODEX_TMPOUT"
    return $exit_code
}

run_with_timeout "$LABEL" run_codex
