# Subagent Schema Reference

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

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase letters, numbers, hyphens) |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Allowlist of tools (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny |
| `model` | No | Model: `sonnet`, `opus`, `haiku`, `inherit` (default: sonnet) |
| `permissionMode` | No | Permission override mode |
| `skills` | No | Skills to load at startup |
| `hooks` | No | Lifecycle hooks |

## Available Tools

Core tools:
- `Read` - Read files
- `Write` - Create/overwrite files
- `Edit` - Edit files
- `Glob` - File pattern matching
- `Grep` - Content search
- `Bash` - Execute commands

Additional tools:
- `Task` - Launch subagents
- `WebFetch` - Fetch web content
- `WebSearch` - Search the web
- `NotebookEdit` - Edit Jupyter notebooks
- `TodoWrite` - Manage task lists
- `AskUserQuestion` - Ask user questions

Plus any MCP tools configured in the environment.

## Models

| Model | Use Case |
|-------|----------|
| `sonnet` | Default, balanced capability and speed |
| `opus` | Complex reasoning tasks |
| `haiku` | Fast, low-latency tasks |
| `inherit` | Use parent conversation's model |

## Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Standard permission prompts |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Auto-deny prompts (allowed tools still work) |
| `bypassPermissions` | Skip all permission checks |
| `plan` | Read-only exploration mode |

## Scopes

| Location | Scope | Priority |
|----------|-------|----------|
| `.claude/agents/` | Project | Higher |
| `~/.claude/agents/` | User (all projects) | Lower |

When both exist with same name, project scope wins.

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

Hook exit codes:
- `0` - Allow operation
- `2` - Block operation (stderr returned to Claude)
