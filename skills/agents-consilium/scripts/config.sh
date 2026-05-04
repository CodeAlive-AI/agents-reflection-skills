#!/bin/bash
#
# Config loader for consilium multi-agent scripts.
# Reads config.json (in the skill root) and exposes helper functions.
#
# Agent config schema (per agent id):
#   enabled  : bool   — is agent active for consensus runs
#   backend  : string — codex-cli | gemini-cli | opencode
#   model    : string — model id passed to the backend
#   role     : string — analyst (deep/precise) | lateral (broad/creative)
#   label    : string — display name in reports (optional)
#
# Overrides: CONSILIUM_CONFIG env var can point to a custom JSON file.

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONSILIUM_CONFIG="${CONSILIUM_CONFIG:-$SKILL_ROOT/config.json}"

# Internal: read JSON via python3.
# Usage: _cfg_python "script body that reads CONSILIUM_CONFIG"
_cfg_python() {
    CONSILIUM_CONFIG_PATH="$CONSILIUM_CONFIG" python3 -c "$1"
}

# Validate config file exists and parses as JSON.
# Exits 1 with a clear message if missing/invalid.
config_validate() {
    if [[ ! -f "$CONSILIUM_CONFIG" ]]; then
        echo "Error: consilium config not found: $CONSILIUM_CONFIG" >&2
        return 1
    fi
    _cfg_python '
import json, os, sys
path = os.environ["CONSILIUM_CONFIG_PATH"]
try:
    with open(path) as f:
        json.load(f)
except Exception as e:
    print(f"Error: invalid JSON in {path}: {e}", file=sys.stderr)
    sys.exit(1)
' || return 1
}

# Print IDs of agents where enabled=true, one per line (config order preserved).
config_enabled_agents() {
    _cfg_python '
import json, os
with open(os.environ["CONSILIUM_CONFIG_PATH"]) as f:
    cfg = json.load(f)
for name, agent in cfg.get("agents", {}).items():
    if agent.get("enabled"):
        print(name)
'
}

# Print IDs of every agent defined in config (enabled or not).
config_all_agents() {
    _cfg_python '
import json, os
with open(os.environ["CONSILIUM_CONFIG_PATH"]) as f:
    cfg = json.load(f)
for name in cfg.get("agents", {}):
    print(name)
'
}

# Return a single field for a given agent id.
# Usage: config_get_field <agent_id> <field>
# Prints the value on stdout (empty if missing). Exits non-zero if agent id unknown.
config_get_field() {
    local agent_id="$1"
    local field="$2"
    AGENT_ID="$agent_id" FIELD="$field" _cfg_python '
import json, os, sys
with open(os.environ["CONSILIUM_CONFIG_PATH"]) as f:
    cfg = json.load(f)
agents = cfg.get("agents", {})
name = os.environ["AGENT_ID"]
if name not in agents:
    print(f"Error: unknown agent id: {name}", file=sys.stderr)
    sys.exit(2)
value = agents[name].get(os.environ["FIELD"], "")
print(value if value is not None else "")
'
}

# Check whether a specific agent is enabled. Exits 0 if enabled, 1 otherwise.
config_is_enabled() {
    local agent_id="$1"
    AGENT_ID="$agent_id" _cfg_python '
import json, os, sys
with open(os.environ["CONSILIUM_CONFIG_PATH"]) as f:
    cfg = json.load(f)
agents = cfg.get("agents", {})
name = os.environ["AGENT_ID"]
sys.exit(0 if agents.get(name, {}).get("enabled") else 1)
'
}

# Resolve a role identifier to the corresponding role prompt variable name in common.sh.
# Kept for backward compatibility; prefer `get_role_prompt` from common.sh.
config_role_prompt_var() {
    case "$1" in
        analyst) echo "ANALYST_ROLE_PROMPT" ;;
        lateral) echo "LATERAL_ROLE_PROMPT" ;;
        *) echo "" ;;
    esac
}

# Emit XML-escaped agent plan for every configured agent.
# Fields: id, label, backend, model, role, enabled, backend-available.
# Used by `consensus-query.sh --list-agents`.
config_xml_plan() {
    _cfg_python '
import json, os, shutil

def esc(v):
    return (str(v)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\"", "&quot;"))

BACKEND_CMDS = {
    "codex-cli": "codex",
    "gemini-cli": "gemini",
    "opencode": "opencode",
    "claude-code": "claude",
}

with open(os.environ["CONSILIUM_CONFIG_PATH"]) as f:
    cfg = json.load(f)

print("<consilium-plan>")
for name, agent in cfg.get("agents", {}).items():
    backend = agent.get("backend", "")
    model = agent.get("model", "")
    role = agent.get("role", "")
    label = agent.get("label") or name
    enabled = "true" if agent.get("enabled") else "false"
    cmd = BACKEND_CMDS.get(backend)
    available = "true" if (cmd and shutil.which(cmd)) else "false"
    attrs = (
        "id=\"" + esc(name) + "\""
        " label=\"" + esc(label) + "\""
        " backend=\"" + esc(backend) + "\""
        " model=\"" + esc(model) + "\""
        " role=\"" + esc(role) + "\""
        " enabled=\"" + enabled + "\""
        " backend-available=\"" + available + "\""
    )
    print("  <agent " + attrs + "/>")
print("</consilium-plan>")
'
}

# Match a value against any glob/literal pattern in the remaining args.
# Returns 0 (match) on first hit, 1 otherwise.
# Usage: config_match_any "agent-id" "pat1" "pat2" ...
config_match_any() {
    local val="$1"; shift
    local pat
    for pat in "$@"; do
        # shellcheck disable=SC2053
        [[ "$val" == $pat ]] && return 0
    done
    return 1
}
