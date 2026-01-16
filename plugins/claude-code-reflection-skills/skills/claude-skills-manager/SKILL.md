---
name: claude-skills-manager
description: List, inspect, delete, modify, and move Claude Code skills between user and project scopes.
---

# Claude Skill Manager

Manage Claude Code skills: list, inspect, delete, modify, and move between scopes.

**IMPORTANT**: After adding, removing, or moving skills, inform the user that they may need to **restart Claude Code** (exit and relaunch) for the skill list to refresh. Edits to existing skill content may take effect without restart.

**CRITICAL**: Before performing any deletion operation, you MUST use the `AskUserQuestion` tool to confirm with the user. Never delete a skill without explicit user confirmation, even if using `--force` flag.

## Skill Scopes

| Scope | Path | Visibility |
|-------|------|------------|
| User | `~/.claude/skills/` | All projects for this user |
| Project | `.claude/skills/` | Anyone in this repository |

**Precedence**: User skills override project skills with the same name.

## Operations

### List Skills

Show all available skills:
```bash
python3 scripts/list_skills.py
```

Filter by scope:
```bash
python3 scripts/list_skills.py --scope user
python3 scripts/list_skills.py --scope project
```

Output formats: `--format text` (default), `--format json`, `--format table`

### Show Skill Info

Display detailed information about a skill:
```bash
python3 scripts/show_skill.py <skill-name>
```

Include file listing:
```bash
python3 scripts/show_skill.py <skill-name> --files
```

JSON output:
```bash
python3 scripts/show_skill.py <skill-name> --format json
```

### Delete Skill

**⚠️ ALWAYS confirm with user before deleting.** Use `AskUserQuestion` to ask: "Are you sure you want to delete the skill '[skill-name]'? This action cannot be undone."

Remove a skill:
```bash
python3 scripts/delete_skill.py <skill-name>
```

Skip script confirmation (still requires user confirmation via AskUserQuestion):
```bash
python3 scripts/delete_skill.py <skill-name> --force
```

Target specific scope:
```bash
python3 scripts/delete_skill.py <skill-name> --scope project
```

### Move Skill Between Scopes

Move skill from project to user (make personal):
```bash
python3 scripts/move_skill.py <skill-name> user
```

Move skill from user to project (share with team):
```bash
python3 scripts/move_skill.py <skill-name> project
```

Overwrite if exists in target:
```bash
python3 scripts/move_skill.py <skill-name> user --force
```

### Modify Skill

To modify a skill's content:
1. Use `show_skill.py` to locate and inspect it
2. Edit SKILL.md directly at the skill's path
3. Content changes take effect on next skill invocation; restart Claude Code if skill doesn't appear updated

For significant modifications, read the skill's SKILL.md first to understand its structure.

### Create New Skill

For creating new skills, use the **skill-creator** skill:
```
/skill-creator <description of new skill>
```

The skill-creator provides structured guidance for building effective skills with proper frontmatter, progressive disclosure, and bundled resources.

## Quick Reference

| Task | Command |
|------|---------|
| List all skills | `python3 scripts/list_skills.py` |
| List user skills | `python3 scripts/list_skills.py -s user` |
| Show skill details | `python3 scripts/show_skill.py <name>` |
| Delete skill | `python3 scripts/delete_skill.py <name>` |
| Move to user scope | `python3 scripts/move_skill.py <name> user` |
| Move to project scope | `python3 scripts/move_skill.py <name> project` |
| Create new skill | Use `/skill-creator` |
