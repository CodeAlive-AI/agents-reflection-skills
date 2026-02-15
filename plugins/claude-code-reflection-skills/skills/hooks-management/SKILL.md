---
name: hooks-management
description: Manage hooks and automation for coding agents (Claude Code, Codex CLI). Use when users want to add, list, remove, update, or validate hooks. Triggers on requests like "add a hook", "create a hook that...", "list my hooks", "remove the hook", "validate hooks", or any mention of automating agent behavior with shell commands.
---

# Hooks Management

Manage hooks and automation through natural language commands.

**IMPORTANT**: After adding, modifying, or removing hooks, always inform the user that they need to **restart the agent** for changes to take effect. Hooks are loaded at startup.

## Quick Reference

**Hook Events**: PreToolUse, PostToolUse, PermissionRequest, UserPromptSubmit, Notification, Stop, SubagentStop, PreCompact, SessionStart, SessionEnd

**Settings Files**:
- User-wide: `~/.claude/settings.json`
- Project: `.claude/settings.json`
- Local (not committed): `.claude/settings.local.json`

## Workflow

### 1. Understand the Request

Parse what the user wants:
- **Add/Create**: New hook for specific event and tool
- **List/Show**: Display current hooks configuration
- **Remove/Delete**: Remove specific hook(s)
- **Update/Modify**: Change existing hook
- **Validate**: Check hooks for errors

### 2. Validate Before Writing

Always run validation before saving:
```bash
python3 "$SKILL_PATH/scripts/validate_hooks.py" ~/.claude/settings.json
```

### 3. Read Current Configuration

```bash
cat ~/.claude/settings.json 2>/dev/null || echo '{}'
```

### 4. Apply Changes

Use Edit tool for modifications, Write tool for new files.

## Adding Hooks

### Translate Natural Language to Hook Config

| User Says | Event | Matcher | Notes |
|-----------|-------|---------|-------|
| "log all bash commands" | PreToolUse | Bash | Logging to file |
| "format files after edit" | PostToolUse | Edit\|Write | Run formatter |
| "block .env file changes" | PreToolUse | Edit\|Write | Exit code 2 blocks |
| "notify me when done" | Notification | "" | Desktop notification |
| "run tests after code changes" | PostToolUse | Edit\|Write | Filter by extension |
| "ask before dangerous commands" | PermissionRequest | Bash | Return allow/deny |

### Hook Configuration Template

```json
{
  "hooks": {
    "EVENT_NAME": [
      {
        "matcher": "TOOL_PATTERN",
        "hooks": [
          {
            "type": "command",
            "command": "SHELL_COMMAND",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Simple vs Complex Hooks

**PREFER SCRIPT FILES** for complex hooks. Inline commands with nested quotes, `osascript`, or multi-step logic often break due to JSON escaping issues.

| Complexity | Approach | Example |
|------------|----------|---------|
| Simple | Inline | `jq -r '.tool_input.command' >> log.txt` |
| Medium | Inline | Single grep/jq pipe with basic conditionals |
| Complex | **Script file** | Dialogs, multiple conditions, osascript, error handling |

**Script location**: `~/.claude/hooks/` (create if needed)

**Script template** (`~/.claude/hooks/my-hook.sh`):
```bash
#!/bin/bash
set -euo pipefail

# Read JSON input from stdin
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command')

# Your logic here
if echo "$cmd" | grep -q 'pattern'; then
    # Show dialog, log, or block
    exit 2  # Block the operation
fi

exit 0  # Allow
```

**Hook config using script**:
```json
{
  "type": "command",
  "command": "~/.claude/hooks/my-hook.sh"
}
```

**Always**:
1. Create script in `~/.claude/hooks/`
2. Make executable: `chmod +x ~/.claude/hooks/my-hook.sh`
3. Test with sample input: `echo '{"tool_input":{"command":"test"}}' | ~/.claude/hooks/my-hook.sh`

### Common Patterns

**Logging (PreToolUse)**:
```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
  }]
}
```

**File Protection (PreToolUse, exit 2 to block)**:
```json
{
  "matcher": "Edit|Write",
  "hooks": [{
    "type": "command",
    "command": "jq -r '.tool_input.file_path' | grep -qE '(\\.env|secrets)' && exit 2 || exit 0"
  }]
}
```

**Auto-format (PostToolUse)**:
```json
{
  "matcher": "Edit|Write",
  "hooks": [{
    "type": "command",
    "command": "file=$(jq -r '.tool_input.file_path'); [[ $file == *.ts ]] && npx prettier --write \"$file\" || true"
  }]
}
```

**Desktop Notification (Notification)**:
```json
{
  "matcher": "",
  "hooks": [{
    "type": "command",
    "command": "osascript -e 'display notification \"Claude needs attention\" with title \"Claude Code\"'"
  }]
}
```

## Codex CLI Hooks

Codex CLI has a limited hook system. For blocking/allowing commands, use Starlark rules instead of hooks:

```starlark
# In .codex/rules/safety.rules
prefix_rule(
    pattern = ["rm", ["-rf", "-r"]],
    decision = "forbidden",
    justification = "Use git clean -fd instead.",
)
```

For notifications: `notify = ["notify-send", "Codex"]` in `config.toml`.

See [references/codex-hooks.md](references/codex-hooks.md) for full Codex hooks reference and migration patterns.

## Event Input Schemas

See [references/claude-event-schemas.md](references/claude-event-schemas.md) for complete JSON input schemas for each event type (Claude Code).

## Validation

Run validation script to check hooks:

```bash
python3 "$SKILL_PATH/scripts/validate_hooks.py" <settings-file>
```

Validates:
- JSON syntax
- Required fields (type, command/prompt)
- Valid event names
- Matcher patterns (regex validity)
- Command syntax basics

## Removing Hooks

1. Read current config
2. Identify hook by event + matcher + command pattern
3. Remove from hooks array
4. If array empty, remove the matcher entry
5. If event empty, remove event key
6. Validate and save

## Exit Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 0 | Success/Allow | Continue execution |
| 2 | Block | PreToolUse: deny tool, PermissionRequest: deny permission |
| Other | Error | Log to stderr, shown in verbose mode |

## Security Checklist

Before adding hooks, verify:
- [ ] No credential logging
- [ ] No sensitive data exposure
- [ ] Specific matchers (avoid `*` when possible)
- [ ] Validated input parsing
- [ ] Appropriate timeout for long operations

## Troubleshooting

**Hook not triggering**: Check matcher case-sensitivity, ensure event name is exact.

**Command failing**: Test command standalone with sample JSON input.

**Permission denied**: Ensure script is executable (`chmod +x`).

**Timeout**: Increase timeout field or optimize command.
