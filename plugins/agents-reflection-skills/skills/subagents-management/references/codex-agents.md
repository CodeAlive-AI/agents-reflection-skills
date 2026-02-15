# Codex CLI Agents & Skills Reference

Agent and skill configuration for [OpenAI Codex CLI](https://github.com/openai/codex).

## Contents

- [AGENTS.md (Instructions)](#agentsmd-instructions)
- [Skills System](#skills-system)
- [Skill Structure](#skill-structure)
- [Skill Scan Locations](#skill-scan-locations)
- [Skill Configuration](#skill-configuration)
- [Codex as MCP Server](#codex-as-mcp-server)
- [Comparison with Claude Code](#comparison-with-claude-code)

## AGENTS.md (Instructions)

Codex uses `AGENTS.md` files as its primary instruction system -- equivalent to Claude Code's `CLAUDE.md`.

### Discovery Order

Built once per run, concatenated root-to-leaf:

1. **Global scope** (`~/.codex/` or `$CODEX_HOME`):
   - `AGENTS.override.md` (checked first)
   - `AGENTS.md` (fallback)
   - Only the first non-empty file at this level

2. **Project scope** (git root → CWD, walking down):
   - At each directory: `AGENTS.override.md` → `AGENTS.md` → fallback names
   - Files concatenate; closer directories can override earlier guidance

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
- src/components/ - React components
- src/lib/ - Shared utilities
- src/api/ - API route handlers
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

# Project root detection markers (default: [".git"])
project_root_markers = [".git", ".hg", ".sl"]
```

### Override Files

`AGENTS.override.md` at any level **replaces** the `AGENTS.md` at that level (not additive). Useful for:
- Temporary instruction changes
- Per-developer overrides (gitignore the override file)
- Testing different instruction sets

## Skills System

Skills are reusable, task-specific capability packages. Each skill is a directory with a `SKILL.md` file.

### Skill Structure

```
my-skill/
├── SKILL.md                  # Required: name, description, instructions
├── scripts/                  # Optional: helper scripts
├── references/               # Optional: reference documentation
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

### Optional Metadata (agents/openai.yaml)

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

## Skill Scan Locations

Skills are discovered from these locations (in order):

| Priority | Scope | Path | Use Case |
|----------|-------|------|----------|
| 1 | Repo (CWD) | `$CWD/.agents/skills/` | Folder-specific skills |
| 2 | Repo (parent) | `$CWD/../.agents/skills/` | Nested repo areas |
| 3 | Repo (root) | `$REPO_ROOT/.agents/skills/` | Org-wide repo skills |
| 4 | User | `$HOME/.agents/skills/` | Personal cross-repo skills |
| 5 | Admin | `/etc/codex/skills/` | System-level skills |
| 6 | System | Bundled with Codex | Built-in skills |

### Invoking Skills

- **Explicitly**: Via `/skills` command or `$skill-name` mention
- **Implicitly**: Codex auto-selects matching skills based on the task (if `allow_implicit_invocation` is not false)

## Skill Configuration

### Disabling Skills

```toml
# In config.toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

### Skill Directory Convention

```
~/.agents/skills/
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
| **Subagents** | `.claude/agents/*.md` | Not yet (in design) |
| **Skills** | `~/.claude/skills/` | `~/.agents/skills/` |
| **Skill format** | SKILL.md with YAML frontmatter | Same (SKILL.md with YAML) |
| **Skill metadata** | YAML frontmatter only | + optional `agents/openai.yaml` |
| **Model selection** | `model:` in frontmatter | Via profiles or config |
| **Tool restrictions** | `tools:` in frontmatter | Via `dependencies.tools` in yaml |
| **Invoke skills** | Slash commands, auto-trigger | `/skills`, `$name`, auto-trigger |
| **Multi-agent** | Task tool (subagents) | MCP server mode + Agents SDK |

### Key Differences

1. **No subagent definitions yet**: Codex doesn't have Claude Code's `.claude/agents/*.md` system for defining custom subagents with model/tool restrictions. This feature is under development.

2. **Skills are compatible**: Both use `SKILL.md` with YAML frontmatter. Skills written for one system can often work in the other with minor adjustments.

3. **Different instruction file names**: `CLAUDE.md` vs `AGENTS.md`. Teams using both tools need to maintain both files (or use Codex's `project_doc_fallback_filenames` to also read `CLAUDE.md`).

4. **Codex multi-agent via MCP**: Instead of built-in subagents, Codex supports running as an MCP server for orchestration via the Agents SDK.
