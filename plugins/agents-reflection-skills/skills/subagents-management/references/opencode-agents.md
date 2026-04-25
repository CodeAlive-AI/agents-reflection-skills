# OpenCode Agents & AGENTS.md Reference

Agent and instruction configuration for [sst/opencode](https://github.com/sst/opencode) (v1.14.x).

## Contents

- [Agent Modes](#agent-modes)
- [Defining Agents](#defining-agents)
- [Agent Frontmatter / JSON Fields](#agent-frontmatter--json-fields)
- [Permission Overrides](#permission-overrides)
- [Built-in Agents](#built-in-agents)
- [AGENTS.md (Instructions)](#agentsmd-instructions)
- [Invoking Agents](#invoking-agents)
- [CLI](#cli)
- [Comparison with Claude Code](#comparison-with-claude-code)

## Agent Modes

OpenCode supports two operational modes:

| Mode | Purpose |
|------|---------|
| `primary` | Top-level agents you interact with directly (e.g., `build`, `plan`) |
| `subagent` | Specialized helpers spawned by primary agents or via `@mention` |
| `all` | Available in both contexts |

The `default_agent` top-level config key picks which primary agent loads first. Press **Tab** to cycle primary agents in the TUI.

## Defining Agents

Agents can be declared two ways. Both are merged (JSON wins on conflict).

### 1. JSON in `opencode.json`

```json
{
  "agent": {
    "reviewer": {
      "mode": "subagent",
      "description": "Reviews PRs for security issues and code smells",
      "model": "anthropic/claude-opus-4-5",
      "temperature": 0.1,
      "prompt": "{file:./prompts/reviewer.md}",
      "permission": {
        "edit": "deny",
        "bash": { "*": "deny", "rg *": "allow", "fd *": "allow" }
      },
      "color": "#3B82F6"
    }
  }
}
```

### 2. Markdown files

- **Global**: `~/.config/opencode/agents/<name>.md`
- **Project**: `<project>/.opencode/agents/<name>.md`

The filename (minus `.md`) becomes the agent ID.

```markdown
---
mode: subagent
description: Reviews PRs for security issues and code smells
model: anthropic/claude-opus-4-5
temperature: 0.1
permission:
  edit: deny
  bash:
    "*": deny
    "rg *": allow
---

You are a senior security reviewer. When invoked, ...
```

## Agent Frontmatter / JSON Fields

| Field | Required | Type | Purpose |
|-------|----------|------|---------|
| `mode` | No | `primary` / `subagent` / `all` | Where the agent appears (default `subagent` for files in `agents/`) |
| `description` | Yes | string | Shown in pickers and used by router for auto-invocation |
| `model` | No | `provider/model-id` | Override the global default model |
| `temperature` | No | 0.0 – 1.0 | Sampling temperature |
| `prompt` | No | string or `{file:...}` | System prompt body (for JSON form) |
| `steps` | No | integer | Max iterations for this agent |
| `tools` | No | object | Per-tool enable/disable map (shorthand for permissions) |
| `permission` | No | object | Per-tool `allow`/`ask`/`deny` rules (overrides global) |
| `color` | No | hex string | UI accent color |
| `reasoningEffort` | No | `none` / `minimal` / `low` / `medium` / `high` / `xhigh` | For reasoning models (GPT-5, etc.) |

## Permission Overrides

Per-agent permissions override global `permission` rules. They use the same `allow`/`ask`/`deny` vocabulary with glob patterns.

```json
{
  "agent": {
    "build": {
      "mode": "primary",
      "description": "Default builder agent",
      "permission": {
        "bash": {
          "*": "allow",
          "git push *": "deny",
          "rm -rf *": "deny"
        }
      }
    },
    "plan": {
      "mode": "primary",
      "description": "Read-only analysis",
      "permission": {
        "edit": "deny",
        "bash": "deny",
        "webfetch": "ask"
      }
    }
  }
}
```

## Built-in Agents

| Agent | Mode | Purpose |
|-------|------|---------|
| `build` | primary | Full development access (default) |
| `plan` | primary | Restricted analysis-only mode |
| `general` | subagent | Multi-step research / generic delegation |
| `explore` | subagent | Fast read-only codebase exploration |

## AGENTS.md (Instructions)

`AGENTS.md` is OpenCode's primary rules/memory file — equivalent to Claude Code's `CLAUDE.md`.

### Discovery Order

1. **Project**: `<project>/AGENTS.md` (loaded for the working tree, walking up to git root)
2. **Global**: `~/.config/opencode/AGENTS.md`
3. **Claude Code fallback**: `CLAUDE.md` and `~/.claude/CLAUDE.md` are loaded if their OpenCode counterparts are missing (unless disabled)

The first matching file wins per category — if both `AGENTS.md` and `CLAUDE.md` exist in a directory, only `AGENTS.md` is used. All accepted files are concatenated into the LLM context.

### Loading additional files via config

```json
{
  "instructions": [
    "AGENTS.md",
    "CONTRIBUTING.md",
    ".cursor/rules/*.md",
    "packages/*/AGENTS.md",
    "https://raw.githubusercontent.com/my-org/shared/main/style.md"
  ]
}
```

- **Globs** are expanded (great for monorepos).
- **Remote URLs** are fetched with a 5-second timeout.
- This array is concatenated, not replaced, when configs merge.

### AGENTS.md Example

```markdown
# Project Instructions

## Stack
- TypeScript (strict mode)
- React 19, Next.js 16
- Bun for package mgmt and tests

## Commands
- `bun test` — run all tests
- `bun run typecheck` — strict TS check
- `bun run lint` — biome lint + format

## Conventions
- Functional components only
- No `any` — use `unknown` and narrow
- All domain types live in `src/domain/`
```

## Invoking Agents

| Path | How |
|------|-----|
| Switch primary agent (TUI) | `Tab` or the `agent_cycle` keybind |
| Mention a subagent | `@reviewer please look at this PR` |
| From a slash command | `/test` may set `"agent": "build"` in its config |
| Auto-invocation | Primary agent picks subagents based on `description` |
| Programmatically | `opencode run --agent reviewer "..."` |

## CLI

```bash
# Interactive scaffolder — prompts for description, picks tools, generates prompt
opencode agent create

# List configured agents (built-ins + user-defined)
opencode agent list
```

## Comparison with Claude Code

| Feature | Claude Code | OpenCode |
|---------|------------|----------|
| Instruction file | `CLAUDE.md` | `AGENTS.md` (fallback to `CLAUDE.md`) |
| Override file | `CLAUDE.local.md` (deprecated) | `~/.config/opencode/AGENTS.md` for personal-global |
| Subagent definitions | `.claude/agents/*.md` (markdown only) | `.opencode/agents/*.md` AND `agent` JSON block |
| Frontmatter fields | `name`, `description`, `tools`, `model`, `permissionMode` | `mode`, `description`, `model`, `temperature`, `permission`, `prompt`, `tools`, `steps`, `reasoningEffort`, `color` |
| Model values | `sonnet`/`opus`/`haiku`/`inherit` | Full `provider/model-id` |
| Tool restriction | `tools: Read, Grep` (allowlist) | `permission: { edit: deny, bash: {...} }` (granular) |
| Global instructions | `~/.claude/CLAUDE.md` | `~/.config/opencode/AGENTS.md` |
| Auto-invocation | Yes (Task tool) | Yes (`@mention` and router) |
| Multi-agent orchestration | Subagents via Task tool | Subagents + plugins + MCP server mode |

## Sources

- https://opencode.ai/docs/agents/
- https://opencode.ai/docs/rules/
- https://opencode.ai/docs/permissions/
- https://opencode.ai/docs/cli/
- https://github.com/sst/opencode
