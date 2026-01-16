---
name: claude-subagents-manager
description: Create, edit, list, move, and delete Claude Code subagents across user and project scopes.
---

# Claude Subagents Manager

Manage Claude Code subagents stored in `~/.claude/agents/` (user) and `.claude/agents/` (project).

**IMPORTANT**: After creating, modifying, or deleting subagents, inform the user that they need to **restart Claude Code** (exit and relaunch) or run `/agents` command to reload the subagent list.

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

## Key Concepts

- **User scope** (`~/.claude/agents/`): Available in all projects
- **Project scope** (`.claude/agents/`): Specific to current project, higher priority
- Subagents reload on session restart or via `/agents` command
- See [references/subagent-schema.md](references/subagent-schema.md) for complete field reference

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
