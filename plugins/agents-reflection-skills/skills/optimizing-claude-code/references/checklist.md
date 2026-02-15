# Audit Checklist

Quick-reference checklist for auditing Claude Code readiness.

---

## Pre-Audit

- [ ] Identify repository root
- [ ] Determine if monorepo or single project
- [ ] Note primary language/framework

---

## Memory Files Audit

### Discovery

- [ ] Check for `CLAUDE.md` at root
- [ ] Check for `.claude/CLAUDE.md`
- [ ] Check for `CLAUDE.local.md` (deprecated)
- [ ] Search for nested CLAUDE.md files in subdirectories

### Per-File Analysis

- [ ] Count lines (flag if >300)
- [ ] Verify all @imports resolve
- [ ] Check for markdown headings
- [ ] Verify commands match actual tooling
- [ ] Check last git commit date for staleness

### Content Quality

- [ ] Overview section present?
- [ ] Commands documented (build/test/lint/dev)?
- [ ] Architecture/structure described?
- [ ] Coding conventions specified?
- [ ] Common gotchas listed?

---

## Settings Audit

### Discovery

- [ ] Check `~/.claude/settings.json` (user scope)
- [ ] Check `.claude/settings.json` (project scope)
- [ ] Check `.claude/settings.local.json` (local scope)
- [ ] Check for managed settings (enterprise)

### Analysis

- [ ] Review allowed tools list
- [ ] Flag overly permissive Bash permissions
- [ ] Check for MCP server configurations
- [ ] Verify no conflicting settings across scopes

---

## MCP Configuration Audit

### Discovery

- [ ] Check `~/.claude/mcp.json` (user scope)
- [ ] Check `.mcp.json` (project scope)
- [ ] Check `.claude/mcp.json` (project scope)

### Analysis

- [ ] Count total servers
- [ ] Flag if >10 servers (context overhead)
- [ ] Verify server descriptions are clear
- [ ] Check for unused/stale server configs

---

## Skills Audit

### Discovery

- [ ] Check `~/.claude/skills/` (user scope)
- [ ] Check `.claude/skills/` (project scope)

### Per-Skill Analysis

- [ ] SKILL.md has description in frontmatter?
- [ ] SKILL.md under 500 lines?
- [ ] Scripts tested and working?
- [ ] References organized appropriately?

---

## Subagents Audit

### Discovery

- [ ] Check `~/.claude/agents/` (user scope)
- [ ] Check `.claude/agents/` (project scope)

### Per-Agent Analysis

- [ ] Clear description/purpose?
- [ ] Appropriate tool restrictions?
- [ ] Well-defined scope?

---

## Repository Scale Assessment

### Metrics

- [ ] Count tracked files
- [ ] Identify largest directories
- [ ] Check for build artifacts in tracking

### Thresholds

- [ ] Small (<500 files): Standard setup sufficient
- [ ] Medium (500-3000 files): Consider modular CLAUDE.md
- [ ] Large (>3000 files): Recommend context engine

---

## Issue Prioritization

### P0 - Critical (Blocks Agentic Work)

- No CLAUDE.md exists
- Broken @imports preventing context loading
- Invalid settings.json syntax

### P1 - High Priority

- CLAUDE.md very large (>500 lines) without @imports
- Missing essential sections (commands, architecture)
- Stale information (commands don't work)
- Security issues (overly permissive permissions)
- Large repo without context scaling strategy

### P2 - Medium Priority

- Using deprecated CLAUDE.local.md
- Suboptimal structure (no headings)
- Minor staleness (documentation drift)
- Many MCP servers without lazy loading awareness

### P3 - Low Priority / Nice-to-Have

- Could add more conventions
- Could improve organization
- Minor formatting improvements

---

## Report Template

```markdown
# Claude Code Optimization Report

## Executive Summary
- [1-3 key findings]
- Overall readiness score: X/16

## Repository Profile
- Files: X
- Primary language: Y
- Framework: Z
- Scale category: Small/Medium/Large

## Memory Files
| File | Lines | Issues | Score |
|------|-------|--------|-------|
| CLAUDE.md | X | Y | Z/16 |

## Key Issues

### P0 - Critical
- [List or "None"]

### P1 - High Priority
- [List]

### P2 - Medium Priority
- [List]

## Recommendations
1. [Prioritized action items]
2. ...

## Suggested Edits
[Specific changes if requested]
```

---

## Post-Audit Actions

- [ ] Present findings to user
- [ ] Prioritize by P0 > P1 > P2
- [ ] Offer to implement changes if requested
- [ ] Do NOT modify files without explicit approval
