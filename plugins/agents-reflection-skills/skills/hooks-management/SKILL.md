---
name: hooks-management
description: Manage hooks and automation for coding agents (Claude Code, Codex CLI, OpenCode). Use when users want to add, list, remove, update, or validate hooks. Triggers on requests like "add a hook", "create a hook that...", "list my hooks", "remove the hook", "validate hooks", or any mention of automating agent behavior with shell commands or plugins.
---

# Hooks Management

Manage hooks and automation through natural language commands.

**IMPORTANT**: After adding, modifying, or removing hooks, always inform the user that they need to **restart the agent** for changes to take effect. Hooks are loaded at startup.

## Quick Reference

**Hook Events** (Claude Code, as of 2026-04 — 28 events):

- *Session lifecycle*: SessionStart, SessionEnd, InstructionsLoaded
- *User input*: UserPromptSubmit, UserPromptExpansion
- *Tool execution*: PreToolUse, PostToolUse, PostToolUseFailure, PostToolBatch
- *Permissions*: PermissionRequest, PermissionDenied
- *Model output*: Stop, StopFailure
- *Subagents/tasks*: SubagentStart, SubagentStop, TaskCreated, TaskCompleted, TeammateIdle
- *Config/state*: ConfigChange, FileChanged, CwdChanged
- *Compaction*: PreCompact, PostCompact
- *Worktree*: WorktreeCreate, WorktreeRemove
- *MCP*: Elicitation, ElicitationResult
- *Notifications*: Notification

**Handler types**: `command`, `http`, `mcp_tool`, `prompt`, `agent`. Some events are command-only (PostCompact, PermissionDenied, Elicitation/ElicitationResult, FileChanged, CwdChanged, ConfigChange, InstructionsLoaded, WorktreeCreate/Remove, SubagentStart, StopFailure, TeammateIdle, Setup, SessionStart, SessionEnd, Notification).

**Settings Files**:
- User-wide: `~/.claude/settings.json`
- Project: `.claude/settings.json`
- Local (not committed): `.claude/settings.local.json`
- Drop-in policy fragments: `~/.claude/managed-settings.d/` (managed-settings only)

**Default control mechanism for PreToolUse**: emit JSON on stdout with `hookSpecificOutput.permissionDecision` set to `"allow"`, `"deny"`, **`"ask"`** (triggers the built-in user confirmation prompt), or **`"defer"`** (pause headless tool calls; resume with `-p --resume`). See [Decision Control](#decision-control-pretooluse). Do NOT roll your own confirmation schemes (env-var flags, interactive `osascript` prompts, bypass tokens) — those break the built-in UX and silently fail under existing `permissions.allow` entries.

**Disable all hooks**: set `disableAllHooks: true` in settings.json.

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
| "ask before dangerous commands" | PreToolUse | Bash | Emit JSON `permissionDecision: "ask"` (built-in confirm UI) |
| "require manual approval for X" | PreToolUse | Bash/Edit/Write | Same — emit JSON `permissionDecision: "ask"`, NOT exit 2 |
| "block unless confirmed" | PreToolUse | Bash | Same — JSON `"ask"` lets the user approve per call |

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

**Script template for PreToolUse** (`~/.claude/hooks/my-hook.sh`) — use JSON decision control as the primary mechanism; exit codes are a fallback for simple blocking only:

```bash
#!/bin/bash
set -euo pipefail

# Read JSON input from stdin
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command')

# Your logic here
if echo "$cmd" | grep -q 'pattern-requiring-confirmation'; then
    # PRIMARY PATTERN for "require user confirmation": emit JSON on stdout.
    # Claude Code will show its built-in confirm prompt to the user.
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "ask",
        permissionDecisionReason: "Explain why this call is risky"
      }
    }'
    exit 0
fi

if echo "$cmd" | grep -q 'pattern-to-hard-block'; then
    # Hard block (no user override possible): JSON deny, NOT exit 2.
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "Reason shown to Claude"
      }
    }'
    exit 0
fi

exit 0  # Allow (silent)
```

**Why JSON decisions, not exit 2 or home-grown prompts:**
- `permissionDecision: "ask"` triggers the built-in Claude Code confirm UI — the user sees a clean prompt and can allow/deny per-call.
- `exit 2` is a blunt block; the user cannot override it from the UI, and Claude often re-tries with workarounds.
- Home-grown schemes (env-var flags like `CONFIRMED=1`, `osascript` dialogs, bypass tokens) break the native UX, leak into command history, and are silently bypassed if the tool already has a matching `permissions.allow` rule.

**Hook config using script**:
```json
{
  "type": "command",
  "command": "~/.claude/hooks/my-hook.sh"
}
```

**Other handler types (2026)**: `http` (POSTs event JSON to a URL), `mcp_tool` (calls a tool on a configured MCP server), `prompt` (evaluates a prompt with an LLM, supports `$ARGUMENTS`), `agent` (runs an agentic verifier with tools). Some events are command-only (PostCompact, PermissionDenied, Elicitation/ElicitationResult, FileChanged, CwdChanged, ConfigChange, InstructionsLoaded, WorktreeCreate/Remove, SubagentStart, StopFailure, TeammateIdle, SessionStart/End, Notification).

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

## Decision Control (PreToolUse)

PreToolUse hooks control tool execution by emitting JSON on stdout. This is the **default mechanism** — use it instead of exit codes whenever the intent is richer than "silently allow / hard block", especially when the user should be asked to confirm.

| `permissionDecision` | Behavior | Use for |
|----------------------|----------|---------|
| `"allow"` | Bypass permissions, proceed silently | Pre-approving a safe call |
| `"deny"` | Block, reason shown to Claude | Hard block (no user override) |
| `"ask"` | **Built-in Claude Code confirm UI** shown to user | "Require manual approval for X" — the canonical pattern |
| `"defer"` | Pause headless tool call, resume via `-p --resume` | External-system integrations in headless (`-p`) sessions |

Additional JSON fields:
- `permissionDecisionReason` — shown to the user for `"allow"`/`"ask"`, shown to Claude for `"deny"`
- `updatedInput` — modify tool input before execution
- `additionalContext` — inject context for Claude before the tool executes

### Ask user before dangerous command (the canonical pattern)

When the user says anything like **"require manual confirmation"**, **"ask before doing X"**, **"don't run Y without my approval"** — this is the pattern. Do not invent bypass env vars, `osascript` dialogs, or confirmation tokens. The built-in prompt already handles per-call allow/deny and is the only path that integrates with existing `permissions.allow` rules correctly.

```bash
#!/bin/bash
set -euo pipefail
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // empty')

if echo "$cmd" | grep -qE 'supabase\s+db\s+reset'; then
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "ask",
        permissionDecisionReason: "This will destroy and recreate the local database."
      }
    }'
else
    exit 0
fi
```

### Deny with reason (hard block)

```bash
jq -n '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason: "Destructive command blocked by hook"
  }
}'
```

### Gotcha: `"ask"` vs existing `permissions.allow` rules

If the tool call already matches an entry in `.claude/settings.local.json` → `permissions.allow` (for example, `"Bash"` is blanket-allowed for this session), the hook's `"ask"` is **bypassed** and the call proceeds silently. Symptom: the hook appears to do nothing. Diagnose by reading `.claude/settings.local.json` and narrowing the allow rule, or remove the blanket allow for the matcher while the hook is in effect.

See [references/claude-event-schemas.md](references/claude-event-schemas.md) for the full output schema.

## Codex CLI Hooks

As of CLI v0.124.0 (April 2026) Codex hooks are **stable** and support six lifecycle events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `Stop`. Hooks live inline in `config.toml` (preferred) or in `hooks.json`.

Enable the feature flag:
```toml
# ~/.codex/config.toml
[features]
codex_hooks = true
```

Minimal PreToolUse blocking hook:
```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 ~/.codex/hooks/policy.py'
timeout = 30
statusMessage = "Checking Bash command"
```

Blocking semantics: exit code `2` blocks (stderr is reason), or emit JSON `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "..."}}`. Starlark rules in `.codex/rules/` are still useful for static command policy and complement hooks.

See [references/codex-hooks.md](references/codex-hooks.md) for full Codex hooks reference, all event input/output schemas, common patterns, and migration from the legacy `AfterAgent` / `AfterToolUse` events.

## OpenCode Hooks (Plugin-based)

OpenCode (anomalyco/opencode v1.14.x) does NOT use config-based shell hooks. Hooks are TypeScript/JavaScript **plugins** that subscribe to lifecycle events. The closest analogue to `PreToolUse` is `tool.execute.before` — throwing inside it blocks the tool call.

```typescript
// .opencode/plugins/env-protection.ts
import type { Plugin } from "@opencode-ai/plugin"

export default (async () => ({
  tool: {
    execute: {
      before: async (input, output) => {
        if (output.args.filePath?.includes(".env")) {
          throw new Error("Reading .env is forbidden")
        }
      },
    },
  },
})) satisfies Plugin
```

**Plugin locations**:
- Project: `.opencode/plugins/*.ts`
- Global: `~/.config/opencode/plugins/*.ts`
- npm packages: listed in `opencode.json` under `plugin: []`

**Common events**: `tool.execute.before`, `tool.execute.after`, `session.idle`, `session.created`, `file.edited`, `permission.asked`, `command.executed` (~25 total).

**Critical caveat (v1.14.x)**: `tool.execute.*` hooks **do NOT** fire for MCP tool calls — use the `permission` block in `opencode.json` to control MCP tool access instead.

For "ask before" semantics, prefer `permission` rules over plugin throws — they integrate with the built-in confirm UI:
```json
{ "permission": { "bash": { "rm -rf *": "ask" } } }
```

See [references/opencode-hooks.md](references/opencode-hooks.md) for the full event catalog, migration patterns from Claude Code hooks, and npm plugin distribution.

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
| 2 | Block | Simple blocking (prefer JSON decision control for PreToolUse) |
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
