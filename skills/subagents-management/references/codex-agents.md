# Codex CLI Agents & Skills Reference

Subagent and skill configuration for [OpenAI Codex CLI](https://github.com/openai/codex). Reflects CLI v0.124.0 (April 2026).

## Contents

- [AGENTS.md (Instructions)](#agentsmd-instructions)
- [Subagents (GA March 2026)](#subagents-ga-march-2026)
- [Skills System](#skills-system)
- [Skill Structure](#skill-structure)
- [Skill Scan Locations](#skill-scan-locations)
- [Skill Configuration](#skill-configuration)
- [Codex as MCP Server](#codex-as-mcp-server)
- [Comparison with Claude Code](#comparison-with-claude-code)

## AGENTS.md (Instructions)

Codex uses `AGENTS.md` files as its primary instruction system — equivalent to Claude Code's `CLAUDE.md`.

### Discovery Order

Built once per run, concatenated root-to-leaf. Codex stops adding files once the combined size hits `project_doc_max_bytes` (default 32 KiB; raise it or split across nested directories if you hit the cap).

1. **Global scope** (`~/.codex/` or `$CODEX_HOME`):
   - `AGENTS.override.md` (checked first)
   - `AGENTS.md` (fallback)
   - Only the first non-empty file at this level

2. **Project scope** (project root → CWD, walking down):
   - At each directory: `AGENTS.override.md` → `AGENTS.md` → fallback names
   - Files concatenate; closer directories can override earlier guidance
   - Codex stops searching once it reaches the current directory

### Recommended hierarchy for monorepos with subagents

```
~/.codex/AGENTS.md            # Global: personal conventions
project/AGENTS.md             # Always loaded: project-wide facts
project/agents/AGENTS.md      # Shared subagent rules
project/agents/<name>/AGENTS.md  # Scoped: job, scope, done criteria
project/.agents/skills/       # Reusable skills (keyword-triggered)
```

### Example AGENTS.md

```markdown
# Project Instructions

## Code Conventions
- Use TypeScript strict mode
- Prefer functional patterns
- All functions must have JSDoc comments

## Testing
- Run `npm test` before committing
- Minimum 80% code coverage

## Architecture
- src/components/ — React components
- src/lib/ — Shared utilities
- src/api/ — API route handlers
```

### Configuration

```toml
# In ~/.codex/config.toml

# Fallback filenames when AGENTS.md is missing
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]

# Max bytes from AGENTS.md files (default: 32768)
project_doc_max_bytes = 65536

# Additional inline instructions (injected before AGENTS.md)
developer_instructions = "Always use TypeScript. Prefer functional patterns."

# Replace built-in base instructions entirely
model_instructions_file = "/path/to/instructions.md"
# (renamed from experimental_instructions_file; old key is deprecated)

# Project root detection markers (default: [".git"])
project_root_markers = [".git", ".hg", ".sl"]
# Set [] to skip parent search (treat CWD as the root)
```

### Override Files

`AGENTS.override.md` at any level **replaces** the `AGENTS.md` at that level (not additive). Useful for:
- Temporary instruction changes
- Per-developer overrides (gitignore the override file)
- Testing different instruction sets

## Subagents (GA March 2026)

Codex CLI gained generally available subagents in March 2026 after several weeks behind a feature flag. Subagents let Codex spawn specialised child agents in parallel and aggregate their results.

### Built-in subagents

Codex ships three by default:
- `default` — generic helper
- `explorer` — codebase exploration / read-mostly tasks
- `worker` — high-throughput small parallel tasks (used by `spawn_agents_on_csv`)

### Configuring orchestration

```toml
# ~/.codex/config.toml or .codex/config.toml

[features]
multi_agent = true                # On by default in modern versions; pin if you need it explicit

[agents]
max_threads = 6                   # Concurrent agent threads (default 6)
max_depth = 1                     # Max nesting; root = 0 (default 1) — raise carefully
job_max_runtime_seconds = 1800    # Per-worker timeout for spawn_agents_on_csv jobs
interrupt_message = true          # Allow interrupting child agents
```

### Custom subagent definitions

Define custom agents as TOML files in `~/.codex/agents/`:

```toml
# ~/.codex/agents/security-reviewer.toml
description = "Reads diffs and flags security issues. Read-only."
model = "gpt-5.5"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
approval_policy = "never"

# Optional: scope MCP servers / skills for this agent
[mcp_servers.semgrep]
command = "semgrep-mcp"
args = ["--config", "p/owasp-top-ten"]

[[skills.config]]
path = "~/.codex/skills/security-checklist/SKILL.md"
enabled = true
```

Register the agent in the main config:

```toml
[agents.security-reviewer]
config_file = "~/.codex/agents/security-reviewer.toml"
description = "Read-only security reviewer."
nickname_candidates = ["secrev", "sec"]
```

If a custom agent name matches a built-in (`explorer`, `worker`, `default`), the custom file overrides the built-in. Subagents inherit the parent's interactive runtime overrides (e.g., `/approvals` changes, `--yolo`).

### Subagent approvals UX

When several agents run, approval prompts surface from inactive threads. The TUI shows the source thread label; press `o` to open that thread before approving / rejecting / answering. Codex re-applies the parent turn's runtime sandbox/approval choices to children.

### Community pattern: file-based definitions

Issue [openai/codex#11701](https://github.com/openai/codex/issues/11701) tracks community demand for `.agents/subagents/<name>.md` files (mirroring Claude's `.claude/agents/<name>.md`). Until that lands, prefer `~/.codex/agents/*.toml` plus per-directory `AGENTS.md` files.

## Skills System

Skills are reusable, task-specific capability packages. Each skill is a directory with a `SKILL.md`. The Agent Skills standard is shared with Claude Code, Cursor, Antigravity, and others — a SKILL.md authored for one platform usually runs unchanged in another.

### Skill Structure

```
my-skill/
├── SKILL.md                  # Required: name, description, instructions
├── scripts/                  # Optional: helper scripts
├── references/               # Optional: long-form docs (loaded on demand)
├── assets/                   # Optional: icons, templates
└── agents/
    └── openai.yaml           # Optional: UI appearance, policy, tool deps
```

### SKILL.md Format

```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and best practices. Use when asked to review code, audit for bugs, or check coding standards.
---

## Instructions

When reviewing code:
1. Check for security vulnerabilities
2. Verify error handling
3. Assess code clarity and maintainability
4. Look for performance issues
5. Validate test coverage
```

Required frontmatter: `name`, `description`. Codex front-loads skills via progressive disclosure — at startup it reads only `name` + `description`; the body and `references/` load on demand.

### Optional Metadata (`agents/openai.yaml`)

```yaml
interface:
  display_name: "Code Reviewer"
  short_description: "Reviews code for quality and security"
  icon_small: "./assets/icon-small.svg"
  icon_large: "./assets/icon-large.png"
  brand_color: "#3B82F6"

policy:
  allow_implicit_invocation: false    # Must be explicitly invoked

dependencies:
  tools:
    - type: "mcp"
      value: "toolName"               # Required MCP tools
```

If the skill declares MCP dependencies, Codex can offer to install them automatically when `[features].skill_mcp_dependency_install = true`.

## Skill Scan Locations

Codex discovers skills from these locations (highest priority first):

| Priority | Scope | Path | Use Case |
|----------|-------|------|----------|
| 1 | Repo (CWD) | `$CWD/.agents/skills/` | Folder-specific skills |
| 2 | Repo (parent) | `$CWD/../.agents/skills/` | Nested repo areas |
| 3 | Repo (root) | `$REPO_ROOT/.agents/skills/` | Org-wide repo skills |
| 4 | User | `$HOME/.codex/skills/` | Personal cross-repo skills (the practical default) |
| 4b | User (alias) | `$HOME/.agents/skills/` | Cross-tool sharing path; Codex also scans here |
| 5 | Admin | `/etc/codex/skills/` | System-level skills |
| 6 | System | Bundled (e.g., `~/.codex/skills/.system/`) | Built-in skills like `$plan`, `$skill-creator` |

> **Path note:** `$CODEX_HOME/skills` (defaulting to `~/.codex/skills`) is the canonical user-level path used by `codex` skill installers and the built-in catalogue. The `~/.agents/skills/` path exists primarily for cross-tool portability and is treated as an alias.

When duplicate skill names appear at multiple locations they coexist in the skill picker rather than merging — the user picks which one to invoke.

### Invoking Skills

- **Explicitly**: via `/skills` command or `$skill-name` mention
- **Implicitly**: Codex auto-selects matching skills based on the task (when `allow_implicit_invocation` is not false)

### Built-in System Skills

Codex ships built-ins under `~/.codex/skills/.system/`:
- `$plan` — plan lifecycle management; plans live in `$CODEX_HOME/plans` (default `~/.codex/plans`)
- `$skill-creator` — interactive skill scaffolding
- `$skill-installer` — install curated or experimental skills from inside an active session

Curated skills can be installed by name: `$skill-installer install <name>` (defaults to `skills/.curated`).

## Skill Configuration

### Disabling Skills

```toml
# In config.toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

Restart Codex after editing `~/.codex/config.toml`.

### Feature flag history

Older Codex versions gated skills behind `codex --enable skills`. The flag is still accepted for backward compatibility but skills are on by default in v0.124.

### Skill Directory Convention

```
~/.codex/skills/
├── code-reviewer/
│   └── SKILL.md
├── test-runner/
│   └── SKILL.md
└── deploy-helper/
    ├── SKILL.md
    ├── scripts/
    │   └── deploy.sh
    └── references/
        └── environments.md
```

## Codex as MCP Server

Codex can run as an MCP server for multi-agent orchestration:

```bash
codex mcp-server | your_mcp_client
```

This enables building agent pipelines with the OpenAI Agents SDK, where multiple Codex instances can be orchestrated with roles like project manager, frontend developer, backend developer, and tester.

### MCP Methods Exposed

| Method | Description |
|--------|-------------|
| `newConversation` | Start new session with model/profile/approval overrides |
| `sendUserMessage` | Send input to the agent |
| `interruptConversation` | Stop current turn |
| `listConversations` | List active conversations |
| `resumeConversation` | Resume a paused conversation |
| `archiveConversation` | Archive a conversation |

## Comparison with Claude Code

| Feature | Claude Code | Codex CLI |
|---------|------------|-----------|
| **Instruction file** | `CLAUDE.md` | `AGENTS.md` |
| **Override file** | `CLAUDE.local.md` | `AGENTS.override.md` |
| **Global instructions** | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| **Subagents — built-in** | Task tool | `default`, `explorer`, `worker` |
| **Subagents — custom (file-based)** | `.claude/agents/*.md`, `~/.claude/agents/*.md` | `~/.codex/agents/*.toml` (project-scoped files tracked in [#11701](https://github.com/openai/codex/issues/11701)) |
| **Subagent format** | Markdown + YAML frontmatter | TOML (full config) |
| **Subagent orchestration knobs** | Implicit | `[agents]` block: `max_threads`, `max_depth`, `job_max_runtime_seconds` |
| **Skills** | `~/.claude/skills/`, `.claude/skills/` | `~/.codex/skills/` (user), `.agents/skills/` (project) |
| **Skill format** | SKILL.md with YAML frontmatter | Same (cross-platform compatible) |
| **Skill metadata** | YAML frontmatter only | + optional `agents/openai.yaml` |
| **Model selection** | `model:` in frontmatter | Via profiles, `[agents.NAME].config_file`, or top-level `model` |
| **Tool restrictions** | `tools:` in frontmatter | Per-agent `[mcp_servers.*]` and `[[skills.config]]` |
| **Invoke skills** | Slash commands, auto-trigger | `/skills`, `$name`, auto-trigger |
| **Multi-agent** | Task tool (subagents) | Native subagents + MCP server mode + Agents SDK |

### Key differences

1. **Codex subagents are TOML, not Markdown.** A custom Codex subagent is a TOML config file (model, sandbox, MCP, skills) registered under `[agents.NAME]`. Claude's are Markdown files with frontmatter and the system prompt as the body.
2. **Skills are compatible.** Both use SKILL.md with YAML frontmatter. Skills written for one system usually work in the other.
3. **Different instruction file names.** `CLAUDE.md` vs `AGENTS.md`. Teams running both can use Codex's `project_doc_fallback_filenames = ["CLAUDE.md"]`.
4. **Codex subagents inherit runtime overrides.** A `--yolo` invocation propagates to all children — important security consideration.
5. **Skill paths differ slightly per platform.** Codex prefers `.agents/skills/` for project scope (cross-tool friendly) and `~/.codex/skills/` for user scope (Codex-native).

## Sources

- [Codex configuration reference](https://developers.openai.com/codex/config-reference)
- [Codex skills docs](https://developers.openai.com/codex/skills)
- [Codex subagents docs](https://developers.openai.com/codex/subagents)
- [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- [Codex changelog](https://developers.openai.com/codex/changelog)
- [openai/skills catalogue](https://github.com/openai/skills)
- [Subagent file-based config request — openai/codex#11701](https://github.com/openai/codex/issues/11701)
