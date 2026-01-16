---
name: claude-settings-manager
description: View and configure Claude Code settings.json files across user, project, local, and managed scopes.
---

# Claude Code Settings Manager

Manage Claude Code configuration through settings.json files.

**IMPORTANT**: After modifying settings, always inform the user that they need to **restart Claude Code** (exit and relaunch) for changes to take effect. Most settings are only loaded at startup.

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

## Reference

For complete settings reference including all available options, environment variables, and advanced configuration, see [references/settings-reference.md](references/settings-reference.md).
