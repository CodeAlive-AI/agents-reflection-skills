# OpenCode Skills Reference

Skills system for [sst/opencode](https://github.com/sst/opencode) (v1.14.x).

OpenCode supports the standard Anthropic skill format (`SKILL.md` with YAML frontmatter) plus Claude-Code-compatible fallback paths. Skills are discovered automatically — no installation step needed beyond placing the directory.

## Contents

- [Discovery Paths](#discovery-paths)
- [SKILL.md Format](#skillmd-format)
- [Invocation](#invocation)
- [Skill Permissions](#skill-permissions)
- [AGENTS.md Integration](#agentsmd-integration)
- [Multi-Agent Compatibility](#multi-agent-compatibility)
- [Comparison with Claude Code](#comparison-with-claude-code)

## Discovery Paths

OpenCode walks up from the current working directory to the git worktree root, collecting matching skills, then layers in global definitions:

| Priority | Scope | Path |
|----------|-------|------|
| 1 | Project (OpenCode-native) | `<dir>/.opencode/skills/<name>/SKILL.md` |
| 2 | Project (Claude-compatible) | `<dir>/.claude/skills/<name>/SKILL.md` |
| 3 | Project (agents-compatible) | `<dir>/.agents/skills/<name>/SKILL.md` |
| 4 | Global (OpenCode-native) | `~/.config/opencode/skills/<name>/SKILL.md` |
| 5 | Global (Claude-compatible) | `~/.claude/skills/<name>/SKILL.md` |
| 6 | Global (agents-compatible) | `~/.agents/skills/<name>/SKILL.md` |

The first match for a given skill name wins. Walking up directories means a skill defined in a sub-package's `.opencode/skills/` is visible only inside that package, while a root-level definition is visible everywhere in the repo.

## SKILL.md Format

OpenCode's frontmatter is a strict subset of the standard Anthropic skills schema:

```markdown
---
name: code-reviewer
description: Reviews code for security issues and code smells. Use when the user asks to review a PR, audit for bugs, or check coding standards.
license: MIT
compatibility: opencode,claude-code,codex
metadata:
  audience: senior
  workflow: review
---

## Instructions

When invoked:
1. Read the diff
2. Flag security issues
3. Suggest improvements
4. Reference style guide in CONTRIBUTING.md
```

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | 1–64 chars, lowercase alphanumeric + hyphens (`^[a-z0-9]+(-[a-z0-9]+)*$`). Must equal the directory name |
| `description` | Yes | 1–1024 chars |
| `license` | No | SPDX identifier or freeform |
| `compatibility` | No | Comma-separated agent IDs the skill targets |
| `metadata` | No | Object of string-to-string pairs (custom keys) |

Body content (after the frontmatter): regular markdown — instructions, examples, references.

### Skill directory layout

```
<scope>/skills/code-reviewer/
├── SKILL.md           # Required
├── scripts/           # Optional helper scripts
├── references/        # Optional deep references
└── assets/            # Optional templates, icons
```

## Invocation

| Path | How |
|------|-----|
| Programmatic | The agent calls the built-in `skill` tool: `skill({ name: "code-reviewer" })` |
| Listed in tool catalog | Each available skill appears with its `description` so the model can pick one |
| Manual reference | Mention the skill name in conversation; the model loads it |

The `skill` tool's catalog comes from the union of all discovered skill directories, deduplicated by `name`.

## Skill Permissions

Control which skills can be invoked through the `permission` block in `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "destructive-*": "ask"
    }
  }
}
```

Glob patterns (`*`, `?`, `~`) match against skill names. Defaults to `"allow"`.

## AGENTS.md Integration

Skills coexist with `AGENTS.md` instructions:

- **AGENTS.md** carries always-on rules and project context (build commands, conventions, gotchas)
- **Skills** are opt-in capability packages the agent invokes when relevant

A skill can reference AGENTS.md content:

```markdown
---
name: pr-reviewer
description: Reviews PRs against the project's CONTRIBUTING.md style guide.
---

Read AGENTS.md and CONTRIBUTING.md to understand the project's conventions
before reviewing the diff.
```

You can register skill instructions globally by adding the skill's body to `instructions` in `opencode.json` (rare; usually overkill):

```json
{
  "instructions": ["~/.config/opencode/skills/code-reviewer/SKILL.md"]
}
```

## Multi-Agent Compatibility

A single skill directory can serve multiple agents because OpenCode reads `.claude/skills/`, `.agents/skills/`, and `.opencode/skills/` automatically. Recommended primary location for cross-tool skills:

- **`.agents/skills/`** for project-shared (works for OpenCode, Codex, Gemini CLI, Replit, Amp)
- **`~/.config/opencode/skills/`** for OpenCode-only personal skills
- **`.claude/skills/`** if Claude Code is the primary tool

Add `compatibility: opencode,claude-code` to the frontmatter to signal multi-agent support.

## Comparison with Claude Code

| Feature | Claude Code | OpenCode |
|---------|-------------|----------|
| Project skill path | `.claude/skills/` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` (all read) |
| Global skill path | `~/.claude/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` (all read) |
| Frontmatter required | `name`, `description` | `name`, `description` (same) |
| Frontmatter optional | `license` | `license`, `compatibility`, `metadata` |
| Discovery | Auto-discovery + restart | Auto-discovery on startup |
| Invocation | Auto-trigger via description | Auto-trigger via `skill` tool catalog; explicit `skill({ name })` calls |
| Permission control | n/a (skills always callable) | `permission.skill` glob rules |
| Walk-up behavior | n/a (single project root) | Walks from CWD up to git worktree root |

### Migrating skills

Most Anthropic-format skills work in OpenCode unchanged. Optional polish:

1. Add `compatibility: opencode,claude-code,codex` to the frontmatter
2. Verify the skill body doesn't assume Claude-specific tools (`Task`, `WebFetch` casing). OpenCode tool names are lowercase: `bash`, `edit`, `read`, etc.
3. Reference scripts via relative paths only — no `${CLAUDE_PLUGIN_ROOT}` equivalent

## Sources

- https://opencode.ai/docs/skills/
- https://opencode.ai/docs/permissions/
- https://opencode.ai/docs/rules/
- https://opencode.ai/docs/config/
