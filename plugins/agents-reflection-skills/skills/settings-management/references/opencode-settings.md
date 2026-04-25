# OpenCode Settings Reference

Configuration for [sst/opencode](https://github.com/sst/opencode) (v1.14.x, Go-based, npm/Bun runtime).

## Contents

- [Config File Locations](#config-file-locations)
- [File Format and Schema](#file-format-and-schema)
- [Top-Level Keys](#top-level-keys)
- [Core Settings Examples](#core-settings-examples)
- [Permissions](#permissions)
- [Provider Configuration](#provider-configuration)
- [TUI Settings (tui.json)](#tui-settings-tuijson)
- [Variable Substitution](#variable-substitution)
- [Environment Variables](#environment-variables)

## Config File Locations

OpenCode loads configuration files in this order (later overrides earlier; objects are deep-merged, arrays like `instructions` are concatenated):

| Priority | Location | Purpose |
|----------|----------|---------|
| 1 (lowest) | Remote `.well-known/opencode` | Organizational defaults |
| 2 | `~/.config/opencode/opencode.json` | User-global config |
| 3 | `$OPENCODE_CONFIG` (env var) | Custom override path |
| 4 | `<project>/opencode.json` (or `.json5`/`.jsonc`) | Project config |
| 5 | `<project>/.opencode/` directory | Project sub-config |
| 6 | `$OPENCODE_CONFIG_CONTENT` (env var) | Inline JSON content |
| 7 | Managed config (system dirs) | IT-deployed |
| 8 (highest) | macOS managed preferences | MDM |

**System managed paths:**
- macOS: `/Library/Application Support/opencode/`
- Linux: `/etc/opencode/`
- Windows: `%ProgramData%\opencode`

**Subdirectory conventions** (plural names; singulars also accepted for backwards compatibility): `agents/`, `commands/`, `tools/`, `themes/`, `plugins/`, `skills/`, `modes/`.

## File Format and Schema

OpenCode accepts both **JSON** and **JSONC** (JSON with comments). Reference the schema for editor autocompletion:

```json
{
  "$schema": "https://opencode.ai/config.json"
}
```

TUI-specific settings (theme, keybinds) live in a separate `tui.json` file with its own schema: `https://opencode.ai/tui.json`.

The schema is enforced via Zod in `packages/opencode/src/config/config.ts`. Legacy keys (e.g., `theme`, `tui` keys placed inside `opencode.json`) are stripped with a warning.

## Top-Level Keys

| Key | Type | Purpose |
|-----|------|---------|
| `$schema` | string | Schema URL (recommended for IDE autocomplete) |
| `model` | string | Default LLM in `provider/model-id` format |
| `small_model` | string | Lightweight model (titles, summaries) |
| `provider` | object | Provider credentials/options/custom registrations |
| `agent` | object | Custom agents and subagents |
| `default_agent` | string | Which agent loads by default |
| `command` | object | Custom slash commands |
| `mcp` | object | MCP servers |
| `plugin` | array of string | npm plugin packages |
| `tools` | object | Disable specific built-in tools |
| `permission` | object | Per-tool allow/ask/deny rules |
| `instructions` | array of string | Extra instruction file paths/globs/URLs |
| `formatter` | object | Code formatters per language |
| `share` | string | Conversation sharing: `manual` / `auto` / `disabled` |
| `server` | object | Headless server: port, hostname, mDNS, CORS |
| `snapshot` | boolean | Track file changes for undo (default: true) |
| `autoupdate` | boolean / string | `true` / `false` / `"notify"` |
| `compaction` | object | Context compaction tuning |
| `watcher` | object | File watcher ignore patterns |
| `disabled_providers` | array of string | Providers to exclude |
| `enabled_providers` | array of string | Allowlist of providers |
| `experimental` | object | Development/preview features |

## Core Settings Examples

### Basic config (`~/.config/opencode/opencode.json`)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4",
  "share": "manual",
  "autoupdate": "notify",
  "instructions": [
    "AGENTS.md",
    "CONTRIBUTING.md",
    "docs/style-guide.md"
  ]
}
```

### Disable specific tools

```json
{
  "tools": {
    "write": false,
    "bash": false,
    "websearch": false
  }
}
```

The 13 built-in tools: `bash`, `edit`, `write`, `read`, `grep`, `glob`, `lsp`, `apply_patch`, `skill`, `todowrite`, `webfetch`, `websearch`, `question`.

### Server / headless mode

```json
{
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "mdns": false,
    "cors": ["http://localhost:3000"]
  }
}
```

## Permissions

OpenCode uses a `permission` key with three outcomes per rule: `"allow"`, `"ask"`, `"deny"`.

```json
{
  "permission": {
    "edit": "ask",
    "bash": {
      "*": "ask",
      "git status *": "allow",
      "git log *": "allow",
      "rm -rf *": "deny"
    },
    "webfetch": "allow",
    "external_directory": "ask"
  }
}
```

**Permission keys:** `read`, `edit`, `bash`, `webfetch`, `external_directory`, `task`, `skill`, `lsp`, `question`, `websearch`, `codesearch`, `glob`, `grep`, `doom_loop`.

**Pattern matching:** `*` matches any chars, `?` matches one char, `~`/`$HOME` expands.

**Defaults:** Most permissions default to `"allow"`. `doom_loop` and `external_directory` default to `"ask"`. `.env` files are denied by default.

**Per-agent overrides:** see [opencode-agents.md in subagents-management](../../subagents-management/references/opencode-agents.md).

## Provider Configuration

```json
{
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 600000
      }
    },
    "azure-openai": {
      "npm": "@ai-sdk/azure",
      "name": "Azure OpenAI",
      "options": {
        "baseURL": "https://YOUR.openai.azure.com/openai",
        "apiVersion": "2024-10-21"
      },
      "models": {
        "gpt-4o": { "name": "GPT-4o (Azure)" }
      }
    },
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "llama3.3": { "name": "Llama 3.3", "limit": { "context": 128000 } }
      }
    }
  }
}
```

**Authenticate via CLI:** `opencode auth login` → stored in `~/.local/share/opencode/auth.json`.
**List providers:** `opencode auth list` (alias `ls`).

OpenCode supports 75+ providers including OpenAI, Anthropic, Vertex AI, Bedrock, Groq, OpenRouter, DeepSeek, Moonshot, xAI, Ollama, LM Studio, llama.cpp, Hugging Face.

## TUI Settings (tui.json)

Theme and keybinds live in a separate file:

**Locations** (in priority order):
- User: `~/.config/opencode/tui.json` (or `$XDG_CONFIG_HOME/opencode/tui.json`)
- Project: `<project>/.opencode/tui.json`
- Working dir: `./.opencode/tui.json`

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight",
  "keybinds": {
    "leader": "ctrl+x",
    "session_new": "<leader>n",
    "session_compact": "none",
    "agent_cycle": "tab"
  }
}
```

Built-in themes include: `tokyonight`, `everforest`, `catppuccin`, `gruvbox`, `nord`, `matrix`, and more. Custom themes go in `~/.config/opencode/themes/*.json` (truecolor required).

Set any keybind value to `"none"` to disable. The default leader key is `ctrl+x`.

## Variable Substitution

In any string value:

| Pattern | Resolves to |
|---------|-------------|
| `{env:VAR_NAME}` | Environment variable |
| `{file:path/to/file}` | File contents (relative, absolute, or `~` paths) |

```json
{
  "provider": {
    "openai": {
      "options": {
        "apiKey": "{env:OPENAI_API_KEY}"
      }
    }
  },
  "agent": {
    "reviewer": {
      "prompt": "{file:./prompts/reviewer.md}"
    }
  }
}
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENCODE_CONFIG` | Path to a custom config file (added to load order) |
| `OPENCODE_CONFIG_CONTENT` | Inline JSON config (highest user priority) |
| `OPENCODE_ENABLE_EXA` | Enable `websearch` tool (`=1`) |
| `XDG_CONFIG_HOME` | Override config directory base |

Auth credentials live in `~/.local/share/opencode/auth.json`.

## Comparison with Claude Code

| Feature | Claude Code | OpenCode |
|---------|------------|----------|
| Config format | JSON (`settings.json`) | JSON / JSONC (`opencode.json`) |
| Global path | `~/.claude/settings.json` | `~/.config/opencode/opencode.json` |
| Project path | `.claude/settings.json` | `opencode.json` (or `.opencode/`) |
| Schema | implicit | `https://opencode.ai/config.json` |
| Permissions | `permissions.allow/ask/deny` arrays | `permission` object with allow/ask/deny |
| Theme | n/a | Separate `tui.json` |
| Provider routing | Anthropic-only by default | 75+ providers, switch via `model` string |
| Instructions file | `CLAUDE.md` | `AGENTS.md` (with `CLAUDE.md` fallback) |
| Custom commands | `.claude/commands/*.md` | `.opencode/commands/*.md` or `command` key |
| Plugin packages | `.claude-plugin/` (Anthropic plugins) | `plugin: []` array (npm packages) |

## Sources

- https://opencode.ai/docs/config/
- https://opencode.ai/docs/permissions/
- https://opencode.ai/docs/providers/
- https://opencode.ai/docs/themes/
- https://opencode.ai/docs/keybinds/
- https://opencode.ai/docs/tools/
- https://github.com/sst/opencode
