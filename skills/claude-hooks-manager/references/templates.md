# Hook Templates

Ready-to-use hook configurations. Copy and adapt as needed.

## Logging & Auditing

### Log All Commands

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "jq -r '\"[\" + (now | strftime(\"%Y-%m-%d %H:%M:%S\")) + \"] \" + .tool_input.command' >> ~/.claude/command-log.txt"
      }]
    }]
  }
}
```

### Log File Changes

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' >> ~/.claude/modified-files.txt"
      }]
    }]
  }
}
```

## File Protection

### Block Sensitive Files

Blocks edits to .env, secrets, credentials files.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | grep -qE '(\\.env|secrets|credentials|\\.pem|\\.key)' && { echo 'Protected file' >&2; exit 2; } || exit 0"
      }]
    }]
  }
}
```

### Block Git Directory

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | grep -q '\\.git/' && { echo 'Cannot modify .git directory' >&2; exit 2; } || exit 0"
      }]
    }]
  }
}
```

### Block package-lock.json

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | grep -q 'package-lock.json$' && { echo 'Let npm manage package-lock.json' >&2; exit 2; } || exit 0"
      }]
    }]
  }
}
```

## Code Formatting

### Auto-format TypeScript/JavaScript

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "file=$(jq -r '.tool_input.file_path'); [[ $file =~ \\.(ts|tsx|js|jsx)$ ]] && npx prettier --write \"$file\" 2>/dev/null || true"
      }]
    }]
  }
}
```

### Auto-format Python

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "file=$(jq -r '.tool_input.file_path'); [[ $file == *.py ]] && black --quiet \"$file\" 2>/dev/null || true"
      }]
    }]
  }
}
```

### Auto-format Go

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "file=$(jq -r '.tool_input.file_path'); [[ $file == *.go ]] && gofmt -w \"$file\" 2>/dev/null || true"
      }]
    }]
  }
}
```

## Notifications

### macOS Notification

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "msg=$(jq -r '.message'); osascript -e \"display notification \\\"$msg\\\" with title \\\"Claude Code\\\"\""
      }]
    }]
  }
}
```

### Linux Notification (notify-send)

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.message' | xargs -I {} notify-send 'Claude Code' '{}'"
      }]
    }]
  }
}
```

### Play Sound on Complete

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "afplay /System/Library/Sounds/Glass.aiff 2>/dev/null || true"
      }]
    }]
  }
}
```

## Command Safety

### Confirm Dangerous Commands

Blocks rm -rf, git push --force, etc. without confirmation.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "cmd=$(jq -r '.tool_input.command'); echo \"$cmd\" | grep -qE '(rm -rf|git push.*--force|DROP TABLE|DELETE FROM.*WHERE 1)' && { echo 'Dangerous command blocked' >&2; exit 2; } || exit 0"
      }]
    }]
  }
}
```

### Block sudo Commands

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.command' | grep -q '^sudo ' && { echo 'sudo not allowed' >&2; exit 2; } || exit 0"
      }]
    }]
  }
}
```

## Testing & Quality

### Run Tests After Code Change

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "file=$(jq -r '.tool_input.file_path'); [[ $file == *.test.* || $file == *_test.* ]] && npm test -- --findRelatedTests \"$file\" 2>/dev/null || true",
        "timeout": 120
      }]
    }]
  }
}
```

### Lint on Save

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "file=$(jq -r '.tool_input.file_path'); [[ $file =~ \\.(ts|tsx|js|jsx)$ ]] && npx eslint --fix \"$file\" 2>/dev/null || true"
      }]
    }]
  }
}
```

## Session Management

### Load Project Environment

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "[ -f \"$CLAUDE_PROJECT_DIR/.claude-env\" ] && cat \"$CLAUDE_PROJECT_DIR/.claude-env\" >> \"$CLAUDE_ENV_FILE\" || true"
      }]
    }]
  }
}
```

### Session Start Message

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup|resume",
      "hooks": [{
        "type": "command",
        "command": "echo '{\"systemMessage\": \"Project: '\"$CLAUDE_PROJECT_DIR\"'\"}'"
      }]
    }]
  }
}
```

## MCP Tools

### Log MCP Tool Usage

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "mcp__.*",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_name' >> ~/.claude/mcp-usage.txt"
      }]
    }]
  }
}
```

### Block Specific MCP Server

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "mcp__dangerous_server__.*",
      "hooks": [{
        "type": "command",
        "command": "echo 'MCP server blocked' >&2; exit 2"
      }]
    }]
  }
}
```
