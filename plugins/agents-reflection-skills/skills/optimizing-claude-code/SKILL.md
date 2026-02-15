---
name: optimizing-claude-code
description: Audits repositories for Claude Code readiness and suggests improvements. Use when asked to check CLAUDE.md quality, review settings, audit project organization, or optimize for agentic work.
---

# Optimizing Claude Code

**Default**: Audit-only. Present findings and await approval before modifying files.

## Workflow

### 1. Run Audit

Execute from repo root:

```bash
python scripts/audit_repo.py --root . --include-user-scope
```

Analyzes:
- Repository scale and directory hotspots
- CLAUDE.md files (discovery, quality, @imports)
- Settings (user/project/local scopes)
- MCP configurations
- Skills and subagents

### 2. Generate Report

Structure output as:

**Executive Summary** (5 bullets max)
- Readiness assessment
- Key strengths
- Critical gaps
- Priority actions

**Repository Profile**
- File count and scale (Small/Medium/Large)
- Primary language/framework

**Memory Files Assessment**
- Per-file metrics
- @import validation
- Content quality
- Staleness indicators

**Settings & Configuration**
- Permissions analysis
- MCP server inventory
- Skills/subagents discovered

**Issues by Priority**
- P0: Blocks agentic work
- P1: High impact
- P2: Nice-to-have

**Recommendations**
- Specific suggested edits
- Reference best practices
- Do NOT apply without approval

### 3. Apply Changes (If Requested)

When asked to implement:
1. Confirm which changes
2. Edit incrementally
3. Show diffs
4. Re-audit to verify

## Large Repository Guidance

When file count exceeds 3000, include scaling recommendations:
- Vanilla context becomes unreliable at scale
- Consider context engines or retrieval layers
- Strategic CLAUDE.md placement becomes critical
- Focus on navigation aids over exhaustive documentation

## Reference Files

- **[best-practices.md](references/best-practices.md)**: Environment setup, CLAUDE.md structure, prompting patterns, workflows, safety
- **[rubric.md](references/rubric.md)**: CLAUDE.md scoring criteria (0-16 scale), anti-patterns, templates
- **[checklist.md](references/checklist.md)**: Step-by-step audit workflow, prioritization guide
