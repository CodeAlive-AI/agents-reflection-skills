# Event Input Schemas

Complete JSON schemas for each hook event type. Hooks receive this data via stdin.

**As of 2026-04** Claude Code supports 28 lifecycle events (was 14 in 2025). New events added in the last 12 months: `PostCompact`, `PostToolUseFailure`, `PostToolBatch`, `PermissionDenied`, `StopFailure`, `SubagentStart`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`, `ConfigChange`, `FileChanged`, `CwdChanged`, `WorktreeCreate`, `WorktreeRemove`, `Elicitation`, `ElicitationResult`, `InstructionsLoaded`, `UserPromptExpansion`. Handler types expanded from `command` to `command | http | mcp_tool | prompt | agent`.

## Common Fields (All Events)

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "default|plan|acceptEdits|auto|dontAsk|bypassPermissions",
  "hook_event_name": "string"
}
```

`auto` is the Sonnet/Opus-based classifier permission mode (Team/Enterprise/Max plans). When auto denies a tool call, the `PermissionDenied` hook fires.

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

Runs after tool execution completes successfully.

```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "string",
  "tool_input": { /* tool-specific */ },
  "tool_response": { /* response data */ },
  "tool_use_id": "string",
  "duration_ms": 12
}
```

`duration_ms` (added in 2026) — tool execution time, excluding permission prompts and PreToolUse hooks.

PostToolUse output may include `updatedMCPToolOutput` to replace MCP tool results before Claude sees them.

## PostToolUseFailure

Runs when a tool fails. Has `error` and `is_interrupt`.

```json
{
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "string",
  "tool_input": {},
  "tool_use_id": "string",
  "error": "string",
  "is_interrupt": false,
  "duration_ms": 0
}
```

## PostToolBatch

Runs after a full batch of parallel tool calls resolves, before the next model call. No matcher.

```json
{
  "hook_event_name": "PostToolBatch",
  "tool_calls": [ /* array of executed tool info */ ]
}
```

## PermissionRequest

Runs when permission dialog shown. Return JSON to allow/deny.

```json
{
  "hook_event_name": "PermissionRequest",
  "tool_name": "string",
  "tool_input": { /* tool-specific */ },
  "permission_suggestions": []
}
```

**Output to allow** (with optional `updatedPermissions` to persist a rule):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": { "behavior": "allow" },
    "updatedInput": { /* optional, modified tool input */ },
    "updatedPermissions": [
      {
        "type": "addRules",
        "rules": [{ "toolName": "Bash", "ruleContent": "npm *" }],
        "behavior": "allow",
        "destination": "localSettings"
      }
    ]
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
      "message": "Reason for denial",
      "interrupt": false
    }
  }
}
```

## PermissionDenied

Fires after the auto-mode classifier (`permission_mode: "auto"`) denies a tool call. Return `retry: true` to tell the model it may retry.

```json
{
  "hook_event_name": "PermissionDenied",
  "tool_name": "string",
  "tool_input": {},
  "denial_reason": "string"
}
```

**Output**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

## UserPromptSubmit

Runs when user submits a prompt, before Claude processes it.

```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "string"
}
```

**Output** can include `decision: "block"` with `reason`, `additionalContext`, and `sessionTitle` to set/update the session title.

## UserPromptExpansion

Runs when a slash command (or MCP prompt) expands into a prompt before reaching Claude. Matcher: `command_name`.

```json
{
  "hook_event_name": "UserPromptExpansion",
  "expansion_type": "slash_command|mcp_prompt",
  "command_name": "string",
  "command_args": "string",
  "command_source": "user|project|plugin",
  "prompt": "string"
}
```

Can block expansion or inject `additionalContext`.

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

Runs when Claude (or a subagent) finishes responding.

```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": boolean
}
```

**SubagentStop** also includes `agent_type`, `agent_id`, and `stop_reason`.

## StopFailure

Fires when the turn ends due to API error. Output and exit code are ignored.

```json
{
  "hook_event_name": "StopFailure",
  "error_type": "rate_limit|authentication_failed|billing_error|invalid_request|server_error|max_output_tokens|unknown",
  "error_message": "string",
  "retry_after": 0
}
```

## SubagentStart

Fires when a subagent is spawned. Matcher: agent type (`Bash`, `Explore`, `Plan`, custom). Observability only.

```json
{
  "hook_event_name": "SubagentStart",
  "agent_type": "string",
  "agent_prompt": "string",
  "agent_model": "string"
}
```

## TaskCreated / TaskCompleted

Fires when a task is created (`TaskCreate` tool) or marked complete. Both can block via `decision: "block"`.

```json
{ "hook_event_name": "TaskCreated", "task_name": "string", "task_description": "string" }
{ "hook_event_name": "TaskCompleted", "task_id": "string", "task_name": "string" }
```

## TeammateIdle

Fires when an agent-team teammate is about to go idle. Exit 2 or `continue: false` prevents idle.

## PreCompact

Runs before compaction. Matcher: `"manual"` or `"auto"`. Can block via exit 2 or `{"decision":"block"}`.

```json
{
  "hook_event_name": "PreCompact",
  "trigger": "manual|auto",
  "custom_instructions": "string"
}
```

## PostCompact

Fires after compaction completes. Matcher: `"manual"` or `"auto"`. Observability only.

```json
{
  "hook_event_name": "PostCompact",
  "trigger_reason": "manual|auto",
  "tokens_removed": 0,
  "compact_summary": "string"
}
```

## SessionStart

Runs on session start/resume. Matcher: `"startup"|"resume"|"clear"|"compact"`.

Special: Has access to `CLAUDE_ENV_FILE` env var for persisting variables. Handler types: `command`, `mcp_tool` only.

```json
{
  "hook_event_name": "SessionStart",
  "source": "startup|resume|clear|compact",
  "model": "claude-sonnet-4-6"
}
```

Output may include `additionalContext`.

## SessionEnd

Runs when session ends. Matcher: `"clear"|"resume"|"logout"|"prompt_input_exit"|"bypass_permissions_disabled"|"other"`.

```json
{
  "hook_event_name": "SessionEnd",
  "reason": "clear|logout|prompt_input_exit|bypass_permissions_disabled|other"
}
```

## InstructionsLoaded

Fires when a `CLAUDE.md` or `.claude/rules/*.md` file loads into context. Matcher: `"session_start"|"nested_traversal"|"path_glob_match"|"include"|"compact"`. Observability only.

```json
{
  "hook_event_name": "InstructionsLoaded",
  "file_path": "string",
  "memory_type": "string",
  "load_reason": "string",
  "globs": [],
  "trigger_file_path": "string",
  "parent_file_path": "string"
}
```

## ConfigChange

Fires when a configuration source changes mid-session. Matcher: `"user_settings"|"project_settings"|"local_settings"|"policy_settings"|"skills"`. Can block (except `policy_settings`).

```json
{
  "hook_event_name": "ConfigChange",
  "config_source": "string",
  "changes": {}
}
```

## FileChanged

Fires when a watched file changes on disk. Matcher: literal filenames, alternation supported (`.envrc|.env`). Has `CLAUDE_ENV_FILE` access.

```json
{
  "hook_event_name": "FileChanged",
  "file_path": "string",
  "change_type": "created|modified|deleted"
}
```

## CwdChanged

Fires when the working directory changes. No matcher. Has `CLAUDE_ENV_FILE` access (useful with direnv).

```json
{
  "hook_event_name": "CwdChanged",
  "old_cwd": "string",
  "new_cwd": "string"
}
```

## WorktreeCreate

Fires when a worktree is being created via `--worktree` or subagent `isolation: "worktree"`. Handler types: `command`, `http`, `mcp_tool`. Non-zero exit aborts creation.

```json
{
  "hook_event_name": "WorktreeCreate",
  "worktree_path": "string",
  "parent_path": "string",
  "isolation_reason": "string"
}
```

`command` hook prints the chosen path on stdout; `http` hook returns `hookSpecificOutput.worktreePath`.

## WorktreeRemove

Fires when a worktree is removed (session exit or subagent finish). Observability only.

```json
{
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "string",
  "removal_reason": "string"
}
```

## Elicitation / ElicitationResult

`Elicitation` fires when an MCP server requests user input mid-tool-call. `ElicitationResult` fires after the user responds, before the response is sent back. Matcher: MCP server name.

```json
{
  "hook_event_name": "Elicitation",
  "server_name": "string",
  "tool_name": "string",
  "elicitation_form": {}
}
```

```json
{
  "hook_event_name": "ElicitationResult",
  "server_name": "string",
  "tool_name": "string",
  "user_response": {},
  "form_fields": {}
}
```

Both can override via `hookSpecificOutput.action: "accept"|"decline"|"cancel"` and `hookSpecificOutput.content`.

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
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "string",
    "updatedInput": { /* modified tool input */ },
    "additionalContext": "string"
  }
}
```

`"defer"` (added 2026): pauses headless tool calls; resume with `claude -p --resume` to re-evaluate the hook. Returns `stop_reason: "tool_deferred"` with `deferred_tool_use` payload.

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
