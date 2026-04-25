---
name: subagents-management
description: Create, edit, list, move, and delete subagents and skills for coding agents (Claude Code, Codex CLI, OpenCode). Manage AGENTS.md instructions, custom subagent definitions, and skill packages across user and project scopes.
---

# Subagents & Skills Management

Manage subagents, skills, and instruction files for coding agents.

- **Claude Code**: Subagents in `~/.claude/agents/` and `.claude/agents/`
- **Codex CLI**: AGENTS.md instructions + skills in `~/.agents/skills/` and `.agents/skills/`
- **OpenCode**: `agent` blocks in `opencode.json` AND markdown agents in `~/.config/opencode/agents/` / `.opencode/agents/`; AGENTS.md for instructions

**IMPORTANT**: After creating, modifying, or deleting subagents/skills, inform the user that they need to **restart the agent** for changes to take effect.

**CRITICAL**: Before performing any deletion operation, you MUST use the `AskUserQuestion` tool to confirm with the user. Never delete a subagent without explicit user confirmation, even if using `--force` flag or direct `rm` commands.

## Operations

### List Subagents

```bash
python3 {SKILL_PATH}/scripts/list_subagents.py [--scope user|project|all] [--json]
```

### Create Subagent

Write a markdown file directly to the appropriate scope directory:

**User scope:** `~/.claude/agents/{name}.md`
**Project scope:** `.claude/agents/{name}.md`

Template:
```markdown
---
name: {name}
description: {when Claude should use this subagent}
tools: {comma-separated tools, or omit to inherit all}
model: {sonnet|opus|haiku|inherit}
---

{System prompt - instructions for the subagent}
```

Or use the helper script:
```bash
python3 {SKILL_PATH}/scripts/create_subagent.py {name} \
  --description "..." \
  --prompt "..." \
  --scope {user|project} \
  --tools "Read,Grep,Glob" \
  --model sonnet
```

### Edit Subagent

1. Find the file: `~/.claude/agents/{name}.md` or `.claude/agents/{name}.md`
2. Edit the frontmatter and/or system prompt using Edit tool

### Move Subagent

```bash
python3 {SKILL_PATH}/scripts/move_subagent.py {name} --to {user|project} [--overwrite]
```

Or manually:
1. Read the source file
2. Write to target directory
3. Delete source file

### Delete Subagent

**⚠️ ALWAYS confirm with user before deleting.** Use `AskUserQuestion` to ask: "Are you sure you want to delete the subagent '[name]'? This action cannot be undone."

```bash
python3 {SKILL_PATH}/scripts/delete_subagent.py {name} [--scope user|project] [--force]
```

Or delete directly (still requires user confirmation via AskUserQuestion first): `rm ~/.claude/agents/{name}.md` or `rm .claude/agents/{name}.md`

## Codex CLI: AGENTS.md & Skills

Codex uses `AGENTS.md` (equivalent to `CLAUDE.md`) for project instructions and a skills system for reusable capabilities.

### AGENTS.md

```
~/.codex/AGENTS.md            # Global instructions
<project-root>/AGENTS.md      # Project instructions
<project-root>/sub/AGENTS.md  # Subdirectory instructions (additive)
```

### Skills

```
~/.agents/skills/my-skill/SKILL.md           # User skills
<project-root>/.agents/skills/my-skill/SKILL.md  # Project skills
```

See [references/codex-agents.md](references/codex-agents.md) for Codex agents/skills reference.

## OpenCode: agent blocks & AGENTS.md

OpenCode (sst/opencode v1.14.x) supports both JSON `agent` blocks in `opencode.json` and markdown files in `agents/`.

### AGENTS.md (instructions)

```
~/.config/opencode/AGENTS.md           # Global personal instructions
<project>/AGENTS.md                    # Project instructions (commit to git)
```

Falls back to `CLAUDE.md` and `~/.claude/CLAUDE.md` automatically when the OpenCode equivalents are missing.

### Subagents

Two equivalent forms:

**JSON in `opencode.json`:**
```json
{
  "agent": {
    "reviewer": {
      "mode": "subagent",
      "description": "Reviews PRs for security issues",
      "model": "anthropic/claude-opus-4-5",
      "temperature": 0.1,
      "prompt": "{file:./prompts/reviewer.md}",
      "permission": {
        "edit": "deny",
        "bash": { "*": "deny", "rg *": "allow" }
      }
    }
  }
}
```

**Markdown file** at `~/.config/opencode/agents/reviewer.md` or `<project>/.opencode/agents/reviewer.md`:
```markdown
---
mode: subagent
description: Reviews PRs for security issues
model: anthropic/claude-opus-4-5
temperature: 0.1
permission:
  edit: deny
  bash:
    "*": deny
    "rg *": allow
---

You are a senior security reviewer...
```

OpenCode-specific fields not present in Claude Code subagents: `mode` (`primary`/`subagent`/`all`), `temperature`, `reasoningEffort`, `color`, granular `permission` glob rules, and full `provider/model-id` model strings.

**CLI helpers:**
```bash
opencode agent create   # Interactive scaffolder
opencode agent list     # List agents
```

See [references/opencode-agents.md](references/opencode-agents.md) for the complete OpenCode agents/AGENTS.md reference.

## Key Concepts (Claude Code)

- **User scope** (`~/.claude/agents/`): Available in all projects
- **Project scope** (`.claude/agents/`): Specific to current project, higher priority
- Subagents reload on session restart or via `/agents` command
- See [references/claude-subagents.md](references/claude-subagents.md) for Claude Code subagent schema

## Common Patterns

**Read-only reviewer:**
```yaml
tools: Read, Grep, Glob
model: haiku
```

**Full-access helper:**
```yaml
# omit tools field to inherit all
model: inherit
```

**Restricted with hooks:**
```yaml
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
```
