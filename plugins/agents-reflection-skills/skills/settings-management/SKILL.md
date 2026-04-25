---
name: settings-management
description: View and configure settings for coding agents (Claude Code, Codex CLI, OpenCode, and others). Covers JSON settings for Claude Code, TOML for Codex CLI, and JSON/JSONC for OpenCode, including permissions, sandbox, model selection, providers, and profiles.
---

# Settings Management

Manage configuration for coding agents.

**IMPORTANT**: After modifying settings, always inform the user that they need to **restart the agent** for changes to take effect. Most settings are only loaded at startup.

## Settings File Locations

| Scope | Location | Shared with team? |
|-------|----------|-------------------|
| **User** | `~/.claude/settings.json` | No |
| **Project** | `.claude/settings.json` | Yes (committed) |
| **Local** | `.claude/settings.local.json` | No (gitignored) |
| **Managed** | System-level `managed-settings.json` | IT-deployed |

**Precedence** (highest to lowest): Managed → Command line → Local → Project → User

## Quick Actions

### View Current Settings

```bash
cat ~/.claude/settings.json 2>/dev/null || echo "No user settings"
cat .claude/settings.json 2>/dev/null || echo "No project settings"
cat .claude/settings.local.json 2>/dev/null || echo "No local settings"
```

### Create/Edit Settings

Use the Edit or Write tool to modify settings files. Always read existing content first to merge changes.

## Common Configuration Tasks

### Set Default Model

```json
{
  "model": "claude-sonnet-4-5-20250929"
}
```

### Configure Permissions

```json
{
  "permissions": {
    "allow": ["Bash(npm run:*)", "Bash(git:*)"],
    "deny": ["Read(.env)", "Read(.env.*)", "WebFetch"],
    "defaultMode": "allowEdits"
  }
}
```

### Add Environment Variables

```json
{
  "env": {
    "MY_VAR": "value",
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
  }
}
```

### Enable Extended Thinking

```json
{
  "alwaysThinkingEnabled": true
}
```

### Configure Attribution

```json
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

### Configure Sandbox

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker", "git"]
  }
}
```

### Configure Hooks

```json
{
  "hooks": {
    "PreToolUse": {
      "Bash": "echo 'Running command...'"
    }
  }
}
```

## Scope Selection Guide

- **User settings** (`~/.claude/settings.json`): Personal preferences across all projects
- **Project settings** (`.claude/settings.json`): Team-shared settings, commit to git
- **Local settings** (`.claude/settings.local.json`): Personal project overrides, not committed

## Workflow

1. **Determine scope**: Ask user which scope (user/project/local) if not specified
2. **Read existing settings**: Always read current file before modifying
3. **Merge changes**: Preserve existing settings, only modify requested keys
4. **Validate JSON**: Ensure valid JSON before writing
5. **Confirm changes**: Show user the final settings
6. **Remind to restart**: Tell user to restart Claude Code for changes to take effect

## Codex CLI Settings

Codex uses TOML format in `~/.codex/config.toml` (user) and `.codex/config.toml` (project).

```toml
model = "gpt-5.2-codex"
approval_policy = "on-request"    # untrusted | on-failure | on-request | never
sandbox_mode = "workspace-write"  # read-only | workspace-write | danger-full-access
```

Key differences from Claude Code:
- TOML format instead of JSON
- Starlark rules for command policies (`.codex/rules/`)
- Named profiles for different workflows
- Feature flags system (`codex features list`)

See [references/codex-settings.md](references/codex-settings.md) for full Codex config reference.

## OpenCode Settings

OpenCode (sst/opencode v1.14.x) uses JSON/JSONC in `~/.config/opencode/opencode.json` (user) and `opencode.json` (project root, or under `.opencode/`).

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "permission": {
    "edit": "ask",
    "bash": { "*": "ask", "git status *": "allow" }
  },
  "instructions": ["AGENTS.md", "docs/style.md"]
}
```

Key differences from Claude Code:
- Schema-validated JSON/JSONC, not plain JSON
- Configs are **deep-merged** (later wins; arrays like `instructions` are concatenated, not replaced)
- Permissions are an object of `allow`/`ask`/`deny` per tool with glob patterns, not separate `allow`/`deny`/`ask` arrays
- Theme/keybinds live in a separate `tui.json` file
- Multi-provider via `model: "<provider>/<model-id>"` and a top-level `provider` block
- Variable substitution: `{env:VAR}` and `{file:path}`

See [references/opencode-settings.md](references/opencode-settings.md) for full OpenCode config reference.

## Reference

- **Claude Code settings**: [references/claude-settings.md](references/claude-settings.md)
- **Codex CLI settings**: [references/codex-settings.md](references/codex-settings.md)
- **OpenCode settings**: [references/opencode-settings.md](references/opencode-settings.md)
