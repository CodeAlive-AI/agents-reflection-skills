#!/bin/bash
#
# Gemini Wrapper for Consilium
# Role and model are read from config.json (agent id "gemini-cli").
# Strategy: Gemini CLI with API key auth → direct v1beta API fallback.
#
# Usage: ./gemini-query.sh "prompt" [context_file]
#        cat file.ts | ./gemini-query.sh "analyze this"
#        ./gemini-query.sh --help
#
# Exit codes:
#   0 — success
#   4 — config error (missing GEMINI_API_KEY, unknown role, missing config)
#   5 — usage error (missing prompt or unknown flag)
#   other — propagated from Gemini CLI/API
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
    sed -n '2,20p' "$0"
    exit $EXIT_OK
fi

config_validate || exit $EXIT_CONFIG_ERROR

AGENT_ID="${CONSILIUM_AGENT_ID:-gemini-cli}"

MODEL="${GEMINI_MODEL:-$(config_get_field "$AGENT_ID" model)}"
ROLE_ID="${CONSILIUM_ROLE_OVERRIDE:-$(config_get_field "$AGENT_ID" role)}"
LABEL="$(config_get_field "$AGENT_ID" label)"
LABEL="${LABEL:-Gemini}"

if ! ROLE_PROMPT="$(get_role_prompt "$ROLE_ID")"; then
    echo -e "${RED}Error: unknown role '$ROLE_ID' for gemini-cli in config${NC}" >&2
    exit $EXIT_CONFIG_ERROR
fi

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
    echo -e "${RED}Error: GEMINI_API_KEY environment variable is not set${NC}" >&2
    echo "Get a key at: https://ai.google.dev/gemini-api/docs/api-key" >&2
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

export GEMINI_MODEL_RESOLVED="$MODEL"

# --- Strategy 1: Gemini CLI in the caller's CWD ---
# approval-mode=plan makes the agent read-only (no Edit/Write/Run tools).
# For v1beta models like gemini-3.1-pro-preview you must have
# "security.auth.selectedType"="gemini-api-key" in $HOME/.gemini/settings.json
# (or in a project-local .gemini/settings.json). GEMINI_API_KEY env is still required.
run_gemini_cli() {
    gemini \
        -p "$FULL_PROMPT" \
        --model "$GEMINI_MODEL_RESOLVED" \
        --approval-mode plan \
        -o text \
        -e "" \
        --allowed-mcp-server-names "" \
        2>/dev/null
}

# --- Strategy 2: Direct v1beta REST API (fallback) ---
run_gemini_api() {
    python3 -c '
import json, sys, os, urllib.request, urllib.error

api_key = os.environ["GEMINI_API_KEY"]
model = os.environ.get("GEMINI_MODEL_RESOLVED", "gemini-3.1-pro-preview")
prompt = os.environ["FULL_PROMPT"]
timeout = int(os.environ.get("AGENT_TIMEOUT", "1200"))

url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
body = json.dumps({
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"maxOutputTokens": 65536}
}).encode()

req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read())
        candidates = result.get("candidates", [])
        if not candidates:
            print("Error: No candidates in response", file=sys.stderr)
            print(json.dumps(result, indent=2), file=sys.stderr)
            sys.exit(1)
        text = candidates[0]["content"]["parts"][0]["text"]
        print(text)
except urllib.error.HTTPError as e:
    err_body = e.read().decode()
    print(f"Gemini API Error {e.code}: {err_body}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Gemini Error: {e}", file=sys.stderr)
    sys.exit(1)
'
}

# --- Dispatch ---
if command -v gemini &> /dev/null; then
    echo -e "${YELLOW}[${LABEL}] Querying ${MODEL} via CLI (role=${ROLE_ID})...${NC}" >&2
    run_with_timeout "$LABEL" run_gemini_cli
else
    echo -e "${YELLOW}[${LABEL}] CLI not found, using API directly for ${MODEL} (role=${ROLE_ID})...${NC}" >&2
    run_with_timeout "$LABEL" run_gemini_api
fi
