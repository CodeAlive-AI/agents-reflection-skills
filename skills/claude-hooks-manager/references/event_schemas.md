# Event Input Schemas

Complete JSON schemas for each hook event type. Hooks receive this data via stdin.

## Common Fields (All Events)

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions",
  "hook_event_name": "string"
}
```

## PreToolUse

Runs before tool execution. Exit 2 to block.

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash|Edit|Write|Read|...",
  "tool_input": { /* tool-specific */ },
  "tool_use_id": "string"
}
```

### Tool Input by Tool

**Bash**:
```json
{
  "command": "string",
  "description": "string",
  "timeout": 120000,
  "run_in_background": false
}
```

**Write**:
```json
{
  "file_path": "string",
  "content": "string"
}
```

**Edit**:
```json
{
  "file_path": "string",
  "old_string": "string",
  "new_string": "string",
  "replace_all": false
}
```

**Read**:
```json
{
  "file_path": "string",
  "offset": 0,
  "limit": 0
}
```

## PostToolUse

Runs after tool execution completes.

```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "string",
  "tool_input": { /* tool-specific */ },
  "tool_response": { /* response data */ },
  "tool_use_id": "string"
}
```

## PermissionRequest

Runs when permission dialog shown. Return JSON to allow/deny.

```json
{
  "hook_event_name": "PermissionRequest",
  "tool_name": "string",
  "tool_input": { /* tool-specific */ }
}
```

**Output to allow**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow"
    }
  }
}
```

**Output to deny**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "Reason for denial"
    }
  }
}
```

## UserPromptSubmit

Runs when user submits a prompt.

```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "string"
}
```

## Notification

Runs when Claude sends notifications.

```json
{
  "hook_event_name": "Notification",
  "message": "string",
  "notification_type": "permission_prompt|idle_prompt|auth_success|elicitation_dialog"
}
```

## Stop / SubagentStop

Runs when Claude finishes responding.

```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": boolean
}
```

## PreCompact

Runs before compaction. Matcher: `"manual"` or `"auto"`.

```json
{
  "hook_event_name": "PreCompact",
  "trigger": "manual|auto",
  "custom_instructions": "string"
}
```

## SessionStart

Runs on session start/resume. Matcher: `"startup"|"resume"|"clear"|"compact"`.

Special: Has access to `CLAUDE_ENV_FILE` env var for persisting variables.

```json
{
  "hook_event_name": "SessionStart",
  "source": "startup|resume|clear|compact"
}
```

## SessionEnd

Runs when session ends.

```json
{
  "hook_event_name": "SessionEnd",
  "reason": "clear|logout|prompt_input_exit|other"
}
```

## Output Schema

### Standard Output

```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": true,
  "systemMessage": "string",
  "hookSpecificOutput": { /* event-specific */ }
}
```

### PreToolUse Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "string",
    "updatedInput": { /* modified tool input */ }
  }
}
```

### PostToolUse Output

```json
{
  "decision": "block",
  "reason": "string",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "string"
  }
}
```

## Environment Variables

Available in all hooks:
- `CLAUDE_PROJECT_DIR`: Project root path
- `CLAUDE_CODE_REMOTE`: `"true"` if remote session

SessionStart only:
- `CLAUDE_ENV_FILE`: File path for persisting env vars
