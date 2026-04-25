# Subagent Schema Reference (Claude Code, 2026-04)

## File Structure

Subagent files are Markdown with YAML frontmatter:

```markdown
---
name: subagent-name
description: When Claude should use this subagent
tools: Read, Grep, Glob
model: sonnet
---

System prompt content goes here...
```

## Frontmatter Fields

Only `name` and `description` are required. The full set as of 2026-04:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase letters, numbers, hyphens) |
| `description` | Yes | When Claude should delegate to this subagent (third-person) |
| `prompt` | No | Inline system prompt (alternative to body) — only valid in `--agents` JSON |
| `tools` | No | Allowlist of tools (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny. **If both `tools` and `disallowedTools` are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool — empty result = no tools.** |
| `model` | No | Alias (`sonnet`, `opus`, `haiku`, `inherit`) or full model ID (e.g. `claude-opus-4-7`, `claude-sonnet-4-6`) |
| `effort` | No | `low`, `medium`, `high`, `xhigh` (Opus 4.7 only), `max`. Overrides session effort. |
| `maxTurns` | No | Cap subagent turns (prevents runaway sessions) |
| `permissionMode` | No | `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. **Not supported for plugin subagents.** |
| `mcpServers` | No | Per-agent MCP server config. **Not supported for plugin subagents.** Loaded for main-thread sessions when launched via `--agent` (2026). |
| `hooks` | No | Lifecycle hooks. **Not supported for plugin subagents.** |
| `skills` | No | Skills to preload at startup (full content injected, not just description) |
| `initialPrompt` | No | First user-turn prompt (only valid in `--agents` JSON) |
| `memory` | No | Memory scope (`project`, `user`, etc.) — accumulates state in `.claude/agent-memory/<name>/` |
| `background` | No | `true` to run concurrently in the background; results arrive as messages when done |
| `isolation` | No | **`worktree`** — creates a fresh git worktree for the agent (auto-cleaned if no changes; persists if changes are made). Plugin agents only support `"worktree"`. Other isolation modes mentioned in 2026 docs: `remote`, `in-process`. |
| `color` | No | Display color in `/agents` UI (e.g. `blue`, `red`) |

## Available Tools

Core tools:
- `Read` - Read files
- `Write` - Create/overwrite files
- `Edit` - Edit files
- `Glob` - File pattern matching
- `Grep` - Content search
- `Bash` - Execute commands
- `PowerShell` - Windows / opt-in (`CLAUDE_CODE_USE_POWERSHELL_TOOL=1`)

Additional tools:
- `Task` / `Agent` - Launch subagents
- `WebFetch` - Fetch web content
- `WebSearch` - Search the web
- `NotebookEdit` - Edit Jupyter notebooks
- `TodoWrite` - Manage task lists
- `AskUserQuestion` - Ask user questions
- `Skill` - Invoke a skill (governed by permission rules: `Skill(name)`, `Skill(name *)`)
- `Monitor` - Stream events from background scripts
- `ExitPlanMode` - End plan mode

Plus any MCP tools configured in the environment.

## Models

| Model | Use Case |
|-------|----------|
| `opus` (Opus 4.7) | Complex reasoning, agentic coding (xhigh effort available) |
| `sonnet` (Sonnet 4.6) | Balanced default |
| `haiku` | Fast, low-latency, exploration |
| `inherit` | Use parent conversation's model |

Full IDs (2026): `claude-opus-4-7`, `claude-sonnet-4-6`, etc.

Set `CLAUDE_CODE_SUBAGENT_MODEL` to override the default for `inherit` agents (e.g. let Opus drive the main session while subagents fall back to Sonnet).

## Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Standard permission prompts |
| `acceptEdits` | Auto-accept file edits + benign filesystem Bash |
| `plan` | Read-only exploration mode |
| `auto` | **NEW (March 2026)** — Sonnet/Opus classifier auto-approves safe ops |
| `dontAsk` | Auto-deny prompts (allowed tools still work) |
| `bypassPermissions` | Skip all permission checks (`.git/`, `.claude/`, `.claude/skills/` still protected) |

When the parent uses `bypassPermissions`, **all subagents inherit it and cannot override**.

## Scopes

| Location | Scope | Priority |
|----------|-------|----------|
| `.claude/agents/` | Project | Higher |
| `~/.claude/agents/` | User (all projects) | Lower |

When both exist with the same name, project scope wins.

## Hooks Configuration

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
```

Handler types: `command`, `http`, `mcp_tool`, `prompt`, `agent`. See hooks-management for the full list of 28 events.

Hook exit codes:
- `0` - Allow operation
- `2` - Block operation (stderr returned to Claude)

## Worktree Isolation

```yaml
---
name: parallel-fixer
description: Fix issues in isolation
isolation: worktree
background: true
---
```

`isolation: worktree` creates a separate git checkout for the agent. Multiple subagents can edit files in parallel without conflict. Combine with `background: true` for fire-and-forget runs. Cleanup is automatic when no changes are made; otherwise the worktree path + branch are returned for review.

## Plugin Subagent Restrictions

For security, plugin-shipped subagents do **not** support: `hooks`, `mcpServers`, `permissionMode`. The only valid `isolation` value is `worktree`. They DO support: `tools`, `disallowedTools`, `model`, `effort`, `maxTurns`, `skills`, `memory`, `background`, `color`, `name`, `description`.

## Forked Subagents (2026)

Forks share the parent's prompt cache (cheaper than fresh subagents). Available in interactive mode only — disabled in non-interactive (`-p`) and the Agent SDK. A fork cannot spawn further forks. Pass `isolation: "worktree"` to write fork edits to a separate worktree.

External builds need `CLAUDE_CODE_FORK_SUBAGENT=1`.
