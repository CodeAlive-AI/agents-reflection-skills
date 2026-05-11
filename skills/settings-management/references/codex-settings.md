# Codex CLI Settings Reference

Configuration for [OpenAI Codex CLI](https://github.com/openai/codex) using TOML format. Reflects CLI v0.124.0 (April 2026) and the configuration schema published at [developers.openai.com/codex/config-reference](https://developers.openai.com/codex/config-reference).

## Contents

- [Config File Locations](#config-file-locations)
- [Core Settings](#core-settings)
- [Approval Policies](#approval-policies)
- [Sandbox Modes](#sandbox-modes)
- [Profiles](#profiles)
- [Feature Flags](#feature-flags)
- [Agents (Subagents) Block](#agents-subagents-block)
- [Skills Block](#skills-block)
- [Hooks Block](#hooks-block)
- [Rules](#rules)
- [Custom Model Providers](#custom-model-providers)
- [Admin Enforcement](#admin-enforcement)
- [CLI Override Examples](#cli-override-examples)

## Config File Locations

Precedence (highest to lowest):

| Priority | Location | Description |
|----------|----------|-------------|
| 1 | CLI flags / `-c` overrides | Per-invocation |
| 2 | Profile values (`--profile`) | Named presets |
| 3 | `.codex/config.toml` (CWD → project root) | Project config; trusted projects only; closest wins |
| 4 | `~/.codex/config.toml` | User config |
| 5 | `/etc/codex/config.toml` | System config |
| 6 | Built-in defaults | Codex defaults |

Override `CODEX_HOME` env var to change the home directory (default: `~/.codex`).

**Schema support** for editor autocompletion:
```toml
#:schema https://developers.openai.com/codex/config-schema.json
```

The generated JSON Schema lives at [`codex-rs/core/config.schema.json`](https://github.com/openai/codex/blob/main/codex-rs/core/config.schema.json).

## Core Settings

```toml
# Model — defaults to a recommended model when unset.
# As of April 2026, gpt-5.5 is recommended for complex coding/agentic work.
# gpt-5.4 remains a valid fallback during rollout. gpt-5.3-codex-spark is a
# fast text-only research preview for ChatGPT Pro users.
model = "gpt-5.5"
model_provider = "openai"
model_reasoning_effort = "medium"       # minimal | low | medium | high | xhigh
model_reasoning_summary = "auto"        # auto | concise | detailed | none
model_verbosity = "medium"              # low | medium | high
model_context_window = 128000           # Manual override
model_auto_compact_token_limit = 0      # Auto-compact trigger (0 = default)

# Approval and sandbox
approval_policy = "on-request"          # untrusted | on-request | never | { granular = { ... } }
                                         # NOTE: "on-failure" is DEPRECATED in 2026 — use
                                         # "on-request" for interactive or "never" for non-interactive.
sandbox_mode = "workspace-write"        # read-only | workspace-write | danger-full-access

# Instructions
developer_instructions = "Always use TypeScript."
model_instructions_file = "/path/to/instructions.md"
# (renamed from experimental_instructions_file; old key is deprecated)

# Project docs
project_doc_max_bytes = 32768
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
project_root_markers = [".git"]         # Set [] to skip parent search

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
| `on-request` | Model decides when to ask (default; recommended for interactive use) |
| `never` | Never prompt (recommended for non-interactive runs and CI) |
| `on-failure` | **DEPRECATED.** Auto-run in sandbox; prompt on failure. Migrate to `on-request` or `never`. |

### Granular approval (advanced)

```toml
[approval_policy.granular]
mcp_elicitations   = true
request_permissions = false
rules               = true
sandbox_approval    = true
skill_approval      = false
```

Each flag toggles whether Codex prompts for that class of action independently. CLI flag: `codex --ask-for-approval on-request` (or `-a on-request`).

## Sandbox Modes

```toml
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
writable_roots = ["~/.pyenv/shims"]
network_access = false                 # On macOS this is silently ignored (Seatbelt limitation)
exclude_tmpdir_env_var = false
exclude_slash_tmp = false
```

| Mode | Read | Write | Network | Use Case |
|------|------|-------|---------|----------|
| `read-only` | All files | None | Controlled | Safe exploration |
| `workspace-write` | All files | CWD + writable_roots + `/tmp` | Controlled | Normal development (default) |
| `danger-full-access` | All | All | All | No sandbox (risky; use only inside an externally hardened VM/container) |

**Platform implementations:**
- macOS: Seatbelt (`sandbox-exec`)
- Linux: Landlock + seccomp (default), or **bwrap** (vendored and compiled in since v0.100.0; `use_linux_sandbox_bwrap = true` to force it)
- WSL: Linux sandbox via WSL2 only. **WSL1 is unsupported since v0.115** (sandbox moved to bwrap).
- Windows native: Windows-specific sandbox implementation (gated by `enable_experimental_windows_sandbox` / `experimental_windows_sandbox`)

> **macOS gotcha:** `network_access = true` in `[sandbox_workspace_write]` is silently ignored by Seatbelt ([openai/codex#10390](https://github.com/openai/codex/issues/10390)). Linux respects it.

> **v0.116.0 regression:** Some container environments hit repeated approval prompts under workspace-write. Workaround: `codex --enable use_legacy_landlock --sandbox workspace-write`.

Helper commands: `codex sandbox seatbelt`, `codex sandbox landlock`, `codex debug ...`.

## Profiles

Define named presets for different workflows:

```toml
profile = "default"

[profiles.deep-review]
model = "gpt-5.5"
model_reasoning_effort = "high"
approval_policy = "never"

[profiles.lightweight]
model = "gpt-5.4"
approval_policy = "untrusted"

[profiles.offline]
model = "qwen2.5-coder"
model_provider = "ollama"
```

Usage: `codex --profile deep-review`. When `--profile X` is set, `codex features enable/disable` writes to that profile rather than the root.

## Feature Flags

```toml
[features]
# Stable, on by default in 2026
codex_hooks = true                # Lifecycle hooks (PreToolUse/PostToolUse/...). STABLE in v0.124
shell_tool = true                 # Shell command execution
multi_agent = true                # Subagent spawning
collaboration_modes = true        # Plan mode etc.
request_rule = true               # Smart approvals — Codex suggests rules from approvals
search_tool = true                # Web search tool
image_generation = true           # On by default since v0.122
tool_search = true                # Tool discovery (on by default since v0.122)

# Experimental / opt-in
shell_snapshot = false            # Speed up repeated commands (Beta)
unified_exec = false              # PTY-backed exec tool (Beta)
apply_patch_freeform = false      # Freeform patch tool
js_repl = false                   # JavaScript REPL (added v0.121)
in_app_browser = false            # Computer-use browser (Beta on macOS)
memories = false                  # Persistent memory tool
remote_models = false             # Remote model support
runtime_metrics = false           # Runtime summaries
skill_mcp_dependency_install = false   # Auto-install MCP deps declared by skills
fast_mode = false                 # Fast service tier (default for eligible plans)
plugins = false                   # Plugin system
remote_plugin = false             # Remote plugin marketplaces

# Sandbox-related
use_legacy_landlock = false       # Force pre-bwrap Landlock path
use_linux_sandbox_bwrap = false   # Force bwrap on Linux
enable_experimental_windows_sandbox = false
elevated_windows_sandbox = false

# Deprecated — do NOT set
# web_search          (use `search_tool` instead)
# web_search_cached
# web_search_request
# child_agents_md     (folded into multi_agent)
```

CLI management:
```bash
codex features list
codex features enable <feature>
codex features disable <feature>
codex --enable <feature>          # Per-invocation
codex --disable <feature>
```

When `--profile X` is active, `enable`/`disable` write to that profile.

For the canonical, exhaustive list of feature keys see the JSON schema linked above — the `[features]` table grows quickly.

## Agents (Subagents) Block

Codex went generally available with subagents in **March 2026**. Configure orchestration in `[agents]`:

```toml
[agents]
max_threads = 6                   # Concurrently open agent threads (default 6)
max_depth = 1                     # Maximum nesting depth; root = 0 (default 1)
job_max_runtime_seconds = 1800    # Per-worker timeout for spawn_agents_on_csv (default 1800)
interrupt_message = true          # Allow interrupting child agents (default true)

# Define / override custom agents
[agents.frontend]
config_file = "~/.codex/agents/frontend.toml"
description = "Frontend specialist for React/Next.js work."
nickname_candidates = ["fe", "ui"]
```

Custom agent files in `~/.codex/agents/*.toml` may include any standard config keys: `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`, etc. If the name matches a built-in agent (`explorer`, `worker`, `default`), the custom file overrides the built-in.

Subagents inherit the parent's interactive runtime overrides (e.g., `/approvals` changes, `--yolo`).

## Skills Block

Skills are stable in 2026. Codex auto-discovers skills from these locations (highest priority first):

| Scope | Path |
|-------|------|
| Project (CWD) | `$CWD/.agents/skills/` |
| Project (intermediate dirs) | `$CWD/../.agents/skills/` |
| Project (repo root) | `$REPO_ROOT/.agents/skills/` |
| User | `$HOME/.codex/skills/` (alias: `$HOME/.agents/skills/`) |
| Admin | `/etc/codex/skills/` |
| System | Bundled with Codex (e.g., `~/.codex/skills/.system/`) |

Per-skill overrides:

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

Skills are always-on as of CLI v0.124. (Earlier versions required `codex --enable skills`; the flag is still accepted for back-compat.)

## Hooks Block

Inline lifecycle hooks. Fully documented in the hooks-management skill — see `references/codex-hooks.md`.

```toml
[features]
codex_hooks = true

[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 ~/.codex/hooks/policy.py'
timeout = 30
statusMessage = "Checking Bash command"
```

Events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `Stop`. Block via exit code `2` or `permissionDecision: "deny"` JSON.

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

Decisions: `allow`, `prompt`, `forbidden`. Most restrictive wins when multiple match. Compound commands (`a && b`) are split and evaluated per-segment.

Test rules:
```bash
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888
```

## Custom Model Providers

Built-in providers in 2026: `openai`, `ollama`, `lmstudio`, plus `amazon-bedrock` (added v0.123).

```toml
[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
wire_api = "responses"                  # responses | chat
query_params = { api-version = "2025-04-01-preview" }
http_headers = { X-Org = "MyOrg" }
request_max_retries = 3
stream_max_retries = 3
stream_idle_timeout_ms = 30000

[model_providers.ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"
wire_api = "chat"

# Bedrock (built-in v0.123+, configurable)
[model_providers.amazon-bedrock]
aws_profile = "my-profile"
# uses AWS SigV4 signing automatically
```

Usage: `codex --model-provider ollama --model qwen2.5-coder`
Or: `codex --oss` (uses `oss_provider` from config).

## Admin Enforcement

Non-overridable constraints in `requirements.toml`:

```toml
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached"]

[features]
codex_hooks = true                       # Pin feature flags

[rules]
prefix_rules = [
  { pattern = [{ token = "rm" }], decision = "forbidden", justification = "Use git clean." },
]

# Inline managed hooks
[[hooks.PreToolUse]]
matcher = "^Bash$"
[[hooks.PreToolUse.hooks]]
type = "command"
command = "/enterprise/hooks/policy.py"

[hooks]
managed_dir = "/enterprise/hooks"
windows_managed_dir = 'C:\enterprise\hooks'

# Filesystem deny-read globs (added v0.122)
deny_read_globs = ["**/.env", "**/secrets/**"]

[mcp_servers.docs]
identity = { command = "codex-mcp" }
```

Precedence: macOS MDM > Cloud (Enterprise) > `/etc/codex/requirements.toml` > `managed_config.toml` > user `config.toml`.

## CLI Override Examples

```bash
codex --model gpt-5.5
codex -m gpt-5.4                         # short form for --model
codex --config model='"gpt-5.5"'
codex --config sandbox_workspace_write.network_access=true
codex -c mcp_servers.context7.enabled=false
codex -c approval_policy='"never"'
codex --profile deep-review
codex --enable codex_hooks --enable multi_agent
codex --add-dir /extra/path             # extend writable roots without leaving sandbox
codex exec --isolated ...               # ignore user config & rules (added v0.122)
```

## Sources

- [Codex configuration reference](https://developers.openai.com/codex/config-reference)
- [Codex config sample](https://developers.openai.com/codex/config-sample)
- [Advanced configuration](https://developers.openai.com/codex/config-advanced)
- [Codex changelog](https://developers.openai.com/codex/changelog)
- [GPT-5.5 announcement](https://openai.com/index/introducing-gpt-5-5/)
- [JSON schema source](https://github.com/openai/codex/blob/main/codex-rs/core/config.schema.json)
