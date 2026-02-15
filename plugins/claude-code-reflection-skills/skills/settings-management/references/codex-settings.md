# Codex CLI Settings Reference

Configuration for [OpenAI Codex CLI](https://github.com/openai/codex) using TOML format.

## Contents

- [Config File Locations](#config-file-locations)
- [Core Settings](#core-settings)
- [Approval Policies](#approval-policies)
- [Sandbox Modes](#sandbox-modes)
- [Profiles](#profiles)
- [Feature Flags](#feature-flags)
- [Rules](#rules)
- [Custom Model Providers](#custom-model-providers)
- [Admin Enforcement](#admin-enforcement)

## Config File Locations

Precedence (highest to lowest):

| Priority | Location | Description |
|----------|----------|-------------|
| 1 | CLI flags / `-c` overrides | Per-invocation |
| 2 | Profile values (`--profile`) | Named presets |
| 3 | `.codex/config.toml` | Project config (trusted projects only) |
| 4 | `~/.codex/config.toml` | User config |
| 5 | `/etc/codex/config.toml` | System config |
| 6 | Built-in defaults | Codex defaults |

Override `CODEX_HOME` env var to change the home directory (default: `~/.codex`).

**Schema support** for editor autocompletion:
```toml
#:schema https://developers.openai.com/codex/config-schema.json
```

## Core Settings

```toml
# Model
model = "gpt-5.2-codex"
model_provider = "openai"
model_reasoning_effort = "medium"       # minimal | low | medium | high | xhigh
model_reasoning_summary = "auto"        # auto | concise | detailed | none
model_verbosity = "medium"              # low | medium | high
model_context_window = 128000           # Manual override
model_auto_compact_token_limit = 0      # Auto-compact trigger (0 = default)

# Approval and sandbox
approval_policy = "on-request"          # untrusted | on-failure | on-request | never
sandbox_mode = "read-only"              # read-only | workspace-write | danger-full-access

# Instructions
developer_instructions = "Always use TypeScript."
model_instructions_file = "/path/to/instructions.md"

# Project docs
project_doc_max_bytes = 32768
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
project_root_markers = [".git"]

# Credentials
cli_auth_credentials_store = "auto"     # file | keyring | auto

# Notification
notify = ["notify-send", "Codex"]

# Default profile
profile = "default"
```

## Approval Policies

```toml
approval_policy = "on-request"
```

| Policy | Behavior |
|--------|----------|
| `untrusted` | Only known-safe read-only commands auto-run; all others prompt |
| `on-failure` | Auto-run in sandbox; prompt only on failure |
| `on-request` | Model decides when to ask (default) |
| `never` | Never prompt (risky) |

CLI flags: `codex --ask-for-approval untrusted` or `codex -a on-request`

## Sandbox Modes

```toml
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
writable_roots = ["/Users/YOU/.pyenv/shims"]
network_access = false
exclude_tmpdir_env_var = false
exclude_slash_tmp = false
```

| Mode | Read | Write | Network | Use Case |
|------|------|-------|---------|----------|
| `read-only` | All files | None | Controlled | Safe exploration |
| `workspace-write` | All files | CWD + writable_roots | Controlled | Normal development |
| `danger-full-access` | All | All | All | No sandbox (risky) |

**Platform implementations:**
- macOS: Seatbelt (`sandbox-exec`)
- Linux: Landlock + seccomp (default), or bwrap (`use_linux_sandbox_bwrap = true`)

## Profiles

Define named presets for different workflows:

```toml
profile = "default"

[profiles.deep-review]
model = "gpt-5-pro"
model_reasoning_effort = "high"
approval_policy = "never"

[profiles.lightweight]
model = "gpt-4.1"
approval_policy = "untrusted"

[profiles.offline]
model = "local-model"
model_provider = "ollama"
```

Usage: `codex --profile deep-review`

## Feature Flags

```toml
[features]
shell_tool = true                # Shell command execution (stable)
unified_exec = false             # PTY-backed exec tool (beta)
shell_snapshot = false           # Environment snapshot (beta)
apply_patch_freeform = false     # Freeform patch tool (experimental)
request_rule = true              # Smart approvals (stable, default on)
collaboration_modes = true       # Plan mode etc. (stable, default on)
runtime_metrics = false          # Runtime summaries (experimental)
remote_models = false            # Remote model support
child_agents_md = false          # Child agents MD support
memory_tool = false              # Memory persistence tool
```

CLI management:
```bash
codex features list
codex features enable <feature>
codex features disable <feature>
codex --enable <feature>         # Per-invocation
codex --disable <feature>
```

## Rules

Starlark-based command execution policies in `.codex/rules/` or `~/.codex/rules/`:

```starlark
# Allow viewing PRs
prefix_rule(
    pattern = ["gh", "pr", "view"],
    decision = "allow",
    justification = "Viewing PRs is safe",
)

# Block destructive rm
prefix_rule(
    pattern = ["rm", ["-rf", "-r"]],
    decision = "forbidden",
    justification = "Use git clean -fd instead.",
)

# Prompt before docker operations
prefix_rule(
    pattern = ["docker"],
    decision = "prompt",
    justification = "Docker commands need review.",
)
```

Decisions: `allow`, `prompt`, `forbidden`. Most restrictive wins when multiple match.

Test rules:
```bash
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888
```

## Custom Model Providers

```toml
[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
wire_api = "responses"                  # responses | chat
query_params = { api-version = "2025-04-01-preview" }

[model_providers.ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"
wire_api = "chat"
```

Usage: `codex --model-provider ollama --model codestral`
Or: `codex --oss` (uses `oss_provider` from config)

## Admin Enforcement

Non-overridable constraints in `requirements.toml`:

```toml
allowed_approval_policies = ["untrusted", "on-request", "on-failure"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached"]

[rules]
prefix_rules = [
  { pattern = [{ token = "rm" }], decision = "forbidden", justification = "Use git clean." },
]

[mcp_servers.docs]
identity = { command = "codex-mcp" }
```

Precedence: macOS MDM > Cloud (Enterprise) > `/etc/codex/requirements.toml` > `managed_config.toml` > user `config.toml`

## CLI Override Examples

```bash
codex --model gpt-5.2
codex --config model='"gpt-5.2"'
codex --config sandbox_workspace_write.network_access=true
codex -c mcp_servers.context7.enabled=false
codex -c approval_policy='"never"'
```
