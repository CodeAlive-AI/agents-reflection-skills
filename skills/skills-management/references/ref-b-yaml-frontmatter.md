# Reference B: YAML Frontmatter (2026-04)

## Required & Recommended fields (Claude Code)

```yaml
---
name: skill-name-in-kebab-case          # Optional in CC; if omitted, directory name is used
description: What it does and when to use it. Include specific trigger phrases.
---
```

Constraints:
- `name` — lowercase letters/numbers/hyphens, max 64 chars, no XML angle brackets, no `claude`/`anthropic` prefix
- `description` — non-empty, no XML angle brackets. **`description + when_to_use` is truncated at 1,536 characters in the skill listing** (counts toward Claude's startup-prompt budget). Front-load the key use case.

## All optional fields (Claude Code, 2026-04)

| Field | Description |
|-------|-------------|
| `name` | Display name. Defaults to directory name. |
| `description` | What the skill does and when to use it. Falls back to first markdown paragraph if omitted. |
| `when_to_use` | Additional invocation context (trigger phrases, examples). Appended to `description`. |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` or `[filename] [format]`. |
| `arguments` | Named positional argument list (space-separated string or YAML list) for `$name` substitution. |
| `disable-model-invocation` | `true` = only the user can invoke (`/name`); Claude will not load it automatically. Also blocks subagent preload. Default: `false`. |
| `user-invocable` | `false` = hide from `/` menu (background knowledge skills). Default: `true`. |
| `allowed-tools` | Tools Claude can use without permission prompt while skill is active. Space-separated string or YAML list. Does NOT restrict tools — use permission settings to deny. |
| `model` | Model alias (`sonnet`, `opus`, `haiku`, `inherit`) or full ID (`claude-opus-4-7`). Override applies for the rest of the turn only — does not save to settings. |
| `effort` | Effort level: `low`, `medium`, `high`, `xhigh` (Opus 4.7 only), `max`. Inherits session level if absent. |
| `context` | `fork` to run in a forked subagent with isolated context. |
| `agent` | Subagent type when `context: fork` (`Explore`, `Plan`, `general-purpose`, or any custom `.claude/agents/*`). |
| `hooks` | Hooks scoped to this skill's lifecycle. |
| `paths` | Glob patterns that limit auto-activation. Comma-separated string or YAML list (same syntax as `CLAUDE.md` path-specific rules). |
| `shell` | `bash` (default) or `powershell` for `` !`command` `` and ` ```! ` blocks. PowerShell requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. |
| `license` | License identifier (open-source). |
| `metadata` | Custom dict (`author`, `version`, `mcp-server`, `category`, `tags`, etc.). |

## String substitutions (Claude Code skills)

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill (appended as `ARGUMENTS: <value>` if `$ARGUMENTS` is absent from content). |
| `$ARGUMENTS[N]` | 0-based positional argument. |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g. `$0`, `$1`). |
| `$name` | Named argument (per `arguments` frontmatter). |
| `${CLAUDE_SESSION_ID}` | Current session ID. |
| `${CLAUDE_SKILL_DIR}` | Directory containing the skill's `SKILL.md`. |

## Dynamic context injection (Claude Code, 2026)

`` !`command` `` runs a shell command **before** the skill content is sent to Claude; the output replaces the placeholder. Multi-line: open a fenced block with ` ```! `.

This is **preprocessing** — Claude only sees the rendered result, not the command.

Disable via `"disableSkillShellExecution": true` in settings (most useful in managed settings).

## Skill content lifecycle (Claude Code, 2026)

- Invoked SKILL.md content enters the conversation as a single message and stays for the rest of the session.
- Auto-compaction re-attaches each invoked skill's most-recent invocation, keeping the **first 5,000 tokens** per skill.
- Combined budget for re-attached skills: **25,000 tokens**, filled most-recent-first. Older skills can be dropped.

## Security notes

**Allowed:**
- Any standard YAML types (strings, numbers, booleans, lists, objects)
- Custom metadata fields under `metadata`
- Long descriptions (up to 1024 characters per the cross-platform spec; CC truncates the listing entry at 1,536 incl. `when_to_use`)

**Forbidden:**
- XML angle brackets (`< >`) in `name` or `description` — security restriction
- Code execution in YAML (uses safe YAML parsing)
- Skills named with `claude` or `anthropic` prefix (reserved)

## Permissioning skill access (Claude Code, 2026)

Claude's access to skills is governed by permission rules:
- `Skill(name)` — exact match
- `Skill(name *)` — prefix match with any arguments
- `Skill` (in `deny`) — block all skills

Bundled built-ins exposed via the Skill tool: `/init`, `/review`, `/security-review`. Other built-ins like `/compact` are not.

## Where Claude Code skills live (priority order)

| Location | Path | Scope |
|----------|------|-------|
| Enterprise | (managed-settings) | All users in org |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled (namespaced as `plugin-name:skill-name`) |

Higher-priority levels win on name conflicts. **Live change detection (2026):** edits to existing skill directories take effect within the current session. Creating a top-level `skills/` directory that didn't exist at session start still requires a restart. Subdirectory `.claude/skills/` is auto-discovered when working in those subdirs (monorepo support).

`--add-dir` grants file access AND auto-loads `.claude/skills/` from the added dir.
