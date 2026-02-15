# Codex CLI Hooks Reference

Hook support in [OpenAI Codex CLI](https://github.com/openai/codex).

## Contents

- [Current State](#current-state)
- [Notify Setting](#notify-setting)
- [Hook Events](#hook-events)
- [Hook Payload Format](#hook-payload-format)
- [Rules as Hook Alternative](#rules-as-hook-alternative)
- [Comparison with Claude Code Hooks](#comparison-with-claude-code-hooks)

## Current State

Codex CLI has a **limited hook system** compared to Claude Code. The full lifecycle hook system (PreToolUse/PostToolUse with blocking) is under active design by OpenAI but not yet fully released.

What exists today:
- **`notify`** setting for external program notifications
- **`AfterAgent`** and **`AfterToolUse`** hook events (fire-and-forget)
- **Rules** (Starlark-based) for command approval/blocking (closest equivalent to PreToolUse blocking)

## Notify Setting

Trigger an external program on specific events:

```toml
# In ~/.codex/config.toml

# Linux desktop notification
notify = ["notify-send", "Codex"]

# macOS sound
notify = ["bash", "-lc", "afplay /System/Library/Sounds/Blow.aiff"]

# Custom script
notify = ["/path/to/notify-script.sh"]
```

### TUI Notification Filtering

```toml
[tui]
# All notifications
notifications = true

# Filter by event type
notifications = ["agent-turn-complete", "approval-requested"]
```

## Hook Events

### AfterAgent

Fires after the agent completes a turn.

```json
{
  "hook_event": "AfterAgent",
  "thread_id": "string",
  "turn_id": "string",
  "triggered_at": "2025-01-15T10:30:00Z",
  "cwd": "/path/to/project",
  "input_messages": ["user message"],
  "last_assistant_message": "agent response"
}
```

### AfterToolUse

Fires after a tool execution completes.

```json
{
  "hook_event": "AfterToolUse",
  "thread_id": "string",
  "turn_id": "string",
  "triggered_at": "2025-01-15T10:30:00Z",
  "cwd": "/path/to/project",
  "call_id": "string",
  "tool_name": "shell",
  "tool_kind": "LocalShell",
  "command": ["git", "status"],
  "workdir": "/path/to/project",
  "output_preview": "On branch main...",
  "sandbox": "seatbelt",
  "sandbox_policy": "workspace-write"
}
```

### Execution Model

- Hooks are **fire-and-forget** (cannot block operations)
- JSON payload is passed as the final command-line argument
- Hooks execute asynchronously after the event

## Hook Payload Format

All hook payloads include common fields:

| Field | Type | Description |
|-------|------|-------------|
| `hook_event` | string | Event name (`AfterAgent`, `AfterToolUse`) |
| `thread_id` | string | Conversation thread ID |
| `turn_id` | string | Current turn ID |
| `triggered_at` | string | ISO 8601 timestamp |
| `cwd` | string | Working directory |

### AfterToolUse-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `call_id` | string | Tool call identifier |
| `tool_name` | string | Tool that was executed |
| `tool_kind` | string | Tool type (LocalShell, ApplyPatch, etc.) |
| `command` | string[] | Command and arguments |
| `workdir` | string | Tool working directory |
| `output_preview` | string | Truncated output |
| `sandbox` | string | Sandbox type (none, seatbelt, bwrap) |
| `sandbox_policy` | string | Sandbox mode used |

## Rules as Hook Alternative

For **blocking/allowing commands** (the primary use case of Claude Code's PreToolUse hooks), Codex uses Starlark rules instead:

```starlark
# In .codex/rules/safety.rules or ~/.codex/rules/default.rules

# Block dangerous commands (like PreToolUse exit 2)
prefix_rule(
    pattern = ["rm", ["-rf", "-r"]],
    decision = "forbidden",
    justification = "Use git clean -fd instead.",
)

# Auto-allow safe commands (like PreToolUse exit 0)
prefix_rule(
    pattern = ["git", "status"],
    decision = "allow",
    justification = "Read-only operation.",
)

# Require confirmation (like PreToolUse with dialog)
prefix_rule(
    pattern = ["docker", "rm"],
    decision = "prompt",
    justification = "Container removal needs review.",
)
```

Rules support compound command splitting -- `git add . && rm -rf /` is evaluated per-segment.

### Smart Approvals

```toml
[features]
request_rule = true  # Default: true
```

When enabled, Codex suggests creating rules when you approve commands, learning your preferences over time.

## Comparison with Claude Code Hooks

| Feature | Claude Code | Codex CLI |
|---------|------------|-----------|
| **PreToolUse blocking** | Full support (exit 2 blocks) | Use Starlark rules instead |
| **PostToolUse** | Full support | AfterToolUse (fire-and-forget) |
| **PreToolUse modification** | Can modify tool input | Not supported |
| **Notifications** | Notification event + hooks | `notify` config setting |
| **Session lifecycle** | SessionStart, SessionEnd, Stop | AfterAgent event |
| **File protection** | PreToolUse matcher on Edit/Write | Sandbox + rules |
| **Auto-formatting** | PostToolUse on Edit/Write | AfterToolUse (no blocking) |
| **Command logging** | PreToolUse on Bash | AfterToolUse |
| **Permission control** | PermissionRequest event | approval_policy + rules |
| **Config format** | JSON (settings.json) | TOML (config.toml) |
| **Config location** | `~/.claude/settings.json` | `~/.codex/config.toml` |

### Migration Patterns

| Claude Code Hook | Codex Equivalent |
|-----------------|------------------|
| Block dangerous commands | Starlark rule with `decision = "forbidden"` |
| Auto-allow safe commands | Starlark rule with `decision = "allow"` |
| Require confirmation | Starlark rule with `decision = "prompt"` |
| Log commands | AfterToolUse hook script |
| Desktop notifications | `notify` config |
| Auto-format after edit | AfterToolUse hook (non-blocking) |
| File protection | Sandbox writable_roots + rules |
