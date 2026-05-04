# Claude Code Plugins Complete Reference (2026-04)

## Table of Contents
1. [Plugin Structure](#plugin-structure)
2. [Plugin Manifest](#plugin-manifest)
3. [Plugin Components](#plugin-components)
4. [Background Monitors](#background-monitors)
5. [Themes](#themes)
6. [User Configuration](#user-configuration)
7. [Channels](#channels)
8. [Dependencies and Versioning](#dependencies-and-versioning)
9. [Marketplace Structure](#marketplace-structure)
10. [Marketplace Configuration](#marketplace-configuration)
11. [Source Types](#source-types)
12. [CLI Commands](#cli-commands)
13. [Plugin Cache and Path Traversal](#plugin-cache-and-path-traversal)
14. [Official Submission](#official-submission)

---

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Optional: Plugin manifest. If absent, components are auto-discovered and the directory name becomes the plugin name.
├── skills/                   # Optional: Agent Skills (preferred over commands/)
│   └── */SKILL.md
├── commands/                 # Optional: Skills as flat .md files (legacy / simple commands)
│   └── *.md
├── agents/                   # Optional: Specialized subagents
│   └── *.md
├── output-styles/            # Optional: Output style definitions (2026)
│   └── *.md
├── themes/                   # Optional: Color themes (2026)
│   └── *.json
├── monitors/                 # Optional: Background monitors (2026, requires v2.1.105+)
│   └── monitors.json
├── hooks/                    # Optional: Event handlers
│   └── hooks.json
├── bin/                      # Optional: Executables added to PATH while plugin is enabled (2026)
├── settings.json             # Optional: Default agent / subagentStatusLine config (2026)
├── .mcp.json                 # Optional: MCP server config
├── .lsp.json                 # Optional: LSP server config (2026, official LSP support since v2.0.74)
├── scripts/                  # Optional: Hook helpers and utilities
├── package.json              # Optional: Auto-installed deps when plugin enables (2026)
├── README.md                 # Recommended
├── CHANGELOG.md              # Recommended
└── LICENSE                   # Recommended
```

> Components live at the plugin **root**, not inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

---

## Plugin Manifest

File: `.claude-plugin/plugin.json`

### Required Fields (Schema)

```json
{
  "name": "plugin-name"
}
```

### Strongly Recommended Metadata

```json
{
  "name": "plugin-name",
  "description": "Clear explanation of what the plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Author Name"
  }
}
```

### Optional Fields

```json
{
  "author": {
    "email": "email@example.com"
  },
  "homepage": "https://github.com/user/plugin",
  "repository": "https://github.com/user/plugin",
  "license": "MIT",
  "keywords": ["tag1", "tag2"]
}
```

### Component Path Fields (Optional)

Use these only for non-standard locations. Paths must be relative to the plugin root and start with `./`. **2026 additions: `outputStyles`, `themes`, `lspServers`, `monitors`, `userConfig`, `channels`, `dependencies`.**

```json
{
  "commands": ["./custom/commands/extra.md"],
  "agents": "./custom/agents/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./mcp.json",
  "outputStyles": "./styles/",
  "themes": "./themes/",
  "lspServers": "./.lsp.json",
  "monitors": "./monitors.json",
  "skills": ["./skills/", "./extras/"]
}
```

| Field | Type | Notes |
|-------|------|-------|
| `skills` | string\|array | Custom directories with `<name>/SKILL.md`. Replaces default `skills/`. To keep default and add more, include both: `"skills": ["./skills/", "./extras/"]`. If a skill path points to the plugin root (e.g. `["./"]`), the frontmatter `name` is used as invocation name. |
| `commands` | string\|array | Flat-`.md` skill files |
| `agents` | string\|array | Replaces default `agents/` |
| `hooks` | string\|array\|object | Path(s) or inline config |
| `mcpServers` | string\|array\|object | Path(s) or inline config |
| `outputStyles` | string\|array | 2026 |
| `themes` | string\|array | 2026 — color theme JSON files |
| `lspServers` | string\|array\|object | 2026 — LSP configs |
| `monitors` | string\|array | 2026 — background monitors (v2.1.105+) |
| `userConfig` | object | 2026 — values prompted at enable time |
| `channels` | array | 2026 — Telegram/Slack/Discord-style channel declarations |
| `dependencies` | array | 2026 — other plugins required (with optional semver constraints) |

### Version Format

Semantic versioning: MAJOR.MINOR.PATCH. Setting `version` in `plugin.json` pins the cache key — bump it on every release. **If you omit `version`, Claude Code falls back to the git commit SHA**, so every commit is treated as a new version (good for internal/team plugins under active development).

Resolution order: `plugin.json#version` → marketplace entry `version` → git SHA → `unknown`.

---

## Plugin Components

### Commands (commands/*.md)

Markdown files with YAML frontmatter become slash commands.

```markdown
---
description: Short description of command
---

# Command Title

Instructions for Claude when command is invoked.
```

### Agents (agents/*.md)

Specialized agent definitions.

```markdown
---
description: Agent purpose and specialty
---

# Agent Name

Detailed instructions and expertise for this agent.
```

### Skills (skills/*/SKILL.md)

Agent skills with frontmatter.

```markdown
---
name: skill-name
description: What the skill does and when to use it
---

# Skill Documentation
```

### Hooks (hooks/hooks.json)

Event handlers for Claude actions.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
            "description": "Validate after edits"
          }
        ]
      }
    ]
  }
}
```

**Hook Events (2026, 28 events):** SessionStart, SessionEnd, InstructionsLoaded, UserPromptSubmit, UserPromptExpansion, PreToolUse, PostToolUse, PostToolUseFailure, PostToolBatch, PermissionRequest, PermissionDenied, Stop, StopFailure, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, TeammateIdle, ConfigChange, FileChanged, CwdChanged, PreCompact, PostCompact, WorktreeCreate, WorktreeRemove, Elicitation, ElicitationResult, Notification.

**Hook handler types:** `command`, `http`, `mcp_tool`, `prompt`, `agent`.

### MCP Servers (.mcp.json)

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["./servers/server.js"],
      "env": {
        "VAR": "${ENV_VAR}"
      }
    }
  }
}
```

### LSP Servers (.lsp.json)

Official since Claude Code v2.0.74. Provides instant diagnostics, go-to-definition, find references, and hover info.

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" },
    "transport": "stdio",
    "env": { "GOFLAGS": "-mod=vendor" },
    "initializationOptions": {},
    "settings": {},
    "workspaceFolder": ".",
    "startupTimeout": 30000,
    "shutdownTimeout": 5000,
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

**Note:** Users must install the language server binary locally. If `Executable not found in $PATH` appears in `/plugin` Errors tab, install the binary (e.g. `npm install -g typescript-language-server typescript`).

---

## Background Monitors

**(2026, requires v2.1.105+)** Monitors run a shell command for the lifetime of the session and deliver every stdout line to Claude as a notification.

`monitors/monitors.json`:

```json
[
  {
    "name": "deploy-status",
    "command": "${CLAUDE_PLUGIN_ROOT}/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

Required fields: `name`, `command`, `description`. Optional: `when` (`"always"` default, or `"on-skill-invoke:<skill-name>"`).

Variable substitutions in `command`: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${user_config.*}`, any `${ENV_VAR}`. Disabling a plugin mid-session does NOT stop running monitors — they stop at session end. Plugin monitors run unsandboxed at the same trust level as hooks.

---

## Themes

**(2026)** Plugins can ship color themes that appear in `/theme` alongside built-in presets.

`themes/dracula.json`:

```json
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Plugin themes are read-only; `Ctrl+E` on a plugin theme in `/theme` copies it to `~/.claude/themes/` for editing.

---

## User Configuration

**(2026)** Plugins can prompt for values at enable time instead of requiring users to hand-edit `settings.json`.

```json
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

Field types: `string`, `number`, `boolean`, `directory`, `file`. Sensitive values go to the system keychain (or `~/.claude/.credentials.json`); non-sensitive values persist in `settings.json` under `pluginConfigs[<plugin-id>].options`. **Keychain has ~2KB shared limit with OAuth tokens — keep sensitive values small.**

Available as `${user_config.KEY}` substitution in MCP/LSP/hook/monitor configs (and skill/agent content for non-sensitive). Also exported as `CLAUDE_PLUGIN_OPTION_<KEY>` env vars to subprocesses.

---

## Channels

**(2026)** Declare message channels that inject content into the conversation (Telegram, Slack, Discord style). Each channel binds to an MCP server provided by the plugin.

```json
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": { "type": "string", "title": "Bot token", "sensitive": true },
        "owner_id": { "type": "string", "title": "Owner ID" }
      }
    }
  ]
}
```

`server` must match a key in the plugin's `mcpServers`.

---

## Dependencies and Versioning

**(2026)** Plugins can require other plugins:

```json
{
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

Plugins pinned by another plugin's version constraint auto-update to the highest satisfying git tag. Use `claude plugin tag` to cut release tags from the plugin directory.

`${CLAUDE_PLUGIN_DATA}` is a persistent directory (`~/.claude/plugins/data/{id}/`) that survives plugin updates. Use it for `node_modules`, Python venvs, caches, and generated files. Pattern: compare bundled `package.json` against a copy in `${CLAUDE_PLUGIN_DATA}` and reinstall when they differ.

---

## Marketplace Structure

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace catalog
├── plugins/                  # Optional: hosted plugins
│   └── plugin-name/
└── README.md
```

---

## Marketplace Configuration

File: `.claude-plugin/marketplace.json`

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name",
    "email": "email@example.com"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0",
    "homepage": "https://github.com/user/marketplace",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "author": { "name": "Author" },
      "category": "productivity",
      "keywords": ["tag1", "tag2"],
      "tags": ["tag1", "tag2"],
      "strict": true
    }
  ]
}
```

**Note:** Plugin entries accept all `plugin.json` fields as optional metadata, plus marketplace-only fields: `source`, `category`, `tags`, and `strict`. When `strict` is `false`, the marketplace entry can serve as the full manifest if the plugin lacks `plugin.json`.

### Advanced Plugin Entry

Override component locations:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin",
  "commands": ["./commands/core/", "./commands/extra/"],
  "agents": ["./agents/agent1.md"],
  "hooks": { "hooks": { "PostToolUse": [...] } },
  "mcpServers": { "server": {...} },
  "strict": false
}
```

---

## Source Types

### Relative Path
```json
{ "source": "./plugins/local-plugin" }
```

### GitHub
```json
{
  "source": {
    "source": "github",
    "repo": "owner/repo",
    "ref": "main"
  }
}
```

### Git URL
```json
{
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "v1.0.0"
  }
}
```

---

## CLI Commands

### Plugin Management
```bash
/plugin                              # Browse plugins
/plugin install <name>@<marketplace>
/plugin uninstall <name>@<marketplace>
/plugin enable <name>@<marketplace>
/plugin disable <name>@<marketplace>
/reload-plugins                      # Reload after editing a plugin

claude plugin install <name>@<marketplace> --scope user|project|local
claude plugin uninstall <name>@<marketplace> --scope project [--keep-data]
claude plugin enable <name>@<marketplace> --scope user
claude plugin disable <name>@<marketplace> --scope user
claude plugin update <name>@<marketplace> --scope user|project|local|managed
claude plugin list [--json] [--available]
claude plugin tag [--push] [--dry-run] [--force]      # 2026 — cut release git tag
claude --plugin-dir ./my-plugin                       # Test a plugin without installing
```

### Marketplace Management
```bash
/plugin marketplace add <source>
/plugin marketplace list
/plugin marketplace update <name>
/plugin marketplace remove <name>
```

### Validation
```bash
claude plugin validate <path>
```

---

## Plugin Cache and Path Traversal

**(2026)** Marketplace plugins are copied to `~/.claude/plugins/cache/<id>/<version>/` rather than used in place. Each installed version is a separate directory; orphaned versions are auto-removed after **7 days** to allow concurrent sessions to keep running with the older version.

**Path traversal limit:** Installed plugins cannot reference files outside their directory. Paths like `../shared-utils` won't work after install. Workaround: create symlinks **inside** your plugin directory pointing at external files; symlinks are preserved in the cache and resolved at runtime.

`${CLAUDE_PLUGIN_ROOT}` resolves to the cache install path (changes with every version). `${CLAUDE_PLUGIN_DATA}` resolves to `~/.claude/plugins/data/{id}/` — persistent across updates.

`/plugin` interface shows the data directory size and prompts before deletion on uninstall. CLI deletes by default; pass `--keep-data` to preserve.

---

## Official Submission

### Anthropic Plugin Submission Form

The official submission form requires the following fields:

| Field | Required | Description | Auto-gathered |
|-------|----------|-------------|---------------|
| Link to Plugin | Yes | GitHub repository URL | `gh repo view --json url` |
| Full SHA | Yes | Commit SHA to be reviewed | `git rev-parse HEAD` |
| Plugin Homepage | Yes | Documentation/landing page | plugin.json homepage |
| Company/Organization URL | Yes | Your company website | `--company-url` flag |
| Primary Contact Email | Yes | Email for communication | `--email` flag |
| Plugin Name | Yes | Name for Plugin Directory | plugin.json name |
| Plugin Description | Yes | 50-100 words | plugin.json description |

### Prepare Submission Command

```bash
python scripts/prepare_submission.py ./my-plugin \
  --email your@email.com \
  --company-url https://yourcompany.com \
  --copy-sha
```

### Prerequisites
- Plugin pushed to GitHub
- `gh` CLI installed and authenticated (`gh auth login`)
- Working directory clean (commit all changes)
- Description is 50-100 words

### Requirements
- Clear, comprehensive documentation
- Well-tested functionality
- Security best practices followed
- Professional code quality
- Responsive maintainer

### Quality Checklist
- [ ] plugin.json has all required fields
- [ ] README.md is comprehensive
- [ ] All commands work correctly
- [ ] Agents behave as expected
- [ ] Hooks trigger appropriately
- [ ] No API keys or secrets in code
- [ ] LICENSE file included
- [ ] Version follows semver
- [ ] Description is 50-100 words
- [ ] Plugin pushed to GitHub
- [ ] Working directory is clean

---

## Environment Variables

**`${CLAUDE_PLUGIN_ROOT}`** resolves to the plugin's installation directory. Use it in hooks, MCP configs, and scripts to avoid path errors after install.
