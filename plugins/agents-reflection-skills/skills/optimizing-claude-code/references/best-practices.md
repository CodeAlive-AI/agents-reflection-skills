# Claude Code Best Practices

## Contents
1. Environment Setup
2. CLAUDE.md Structure
3. Prompting Patterns
4. Workflows
5. Context Management
6. Safety

---

## Environment Setup

### Permissions

```json
{
  "permissions": {
    "allow": ["Edit", "Write", "Bash(git:*)", "Bash(npm:test)", "Bash(npm:build)"]
  }
}
```

- Auto-allow benign operations (editing, git on feature branches)
- Gate dangerous operations (database deletions, system configs)
- Install `gh` CLI for issue/PR workflows

### Custom Commands

Create in `.claude/commands/`:

```markdown
# .claude/commands/fix-issue.md
Fix GitHub issue $ARGUMENTS:
1. Fetch with `gh issue view $ARGUMENTS`
2. Find relevant code
3. Implement fix
4. Run tests
5. Create PR
```

---

## CLAUDE.md Structure

### Template

```markdown
# Project Name

## Overview
Brief description (2-5 bullets)

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Architecture
- `src/` - Main source
- `lib/` - Utilities
- `tests/` - Tests

## Conventions
- TypeScript strict mode
- Functional components
- User-friendly errors

## Gotchas
- API rate limits: 100 req/min
- Cache invalidation requires restart
```

### Guidelines

- **Concise**: Map, not wiki - use @imports for details
- **No duplication**: One authoritative place per rule
- **Include commands**: Build/test/lint for productivity
- **Update regularly**: Living document

### Monorepos

- Top-level CLAUDE.md with global rules + navigation
- Nested CLAUDE.md only for package-specific rules
- Prefer @imports over monolithic files

---

## Prompting Patterns

### Plan-Then-Execute

1. **Explore**: "Read these files but do NOT write code yet"
2. **Plan**: "Draft step-by-step plan, consider edge cases"
3. **Review**: Approve/refine the plan
4. **Execute**: "Implement and self-verify each part"
5. **Commit**: "Commit with descriptive message"

### Extended Thinking

- `think` - Standard reasoning
- `think harder` - More computation
- `ultrathink` - Maximum depth

### Be Specific

**Bad**: "Add tests for login"
**Good**: "Write unit test in `login.test.js` for expired session tokens. Use standard library. No mocks."

### Provide Context

- **Images**: Design mocks for UI
- **URLs**: External docs directly
- **Files**: Exact paths
- **Examples**: Input/output samples

---

## Workflows

### Test-Driven Development

1. Claude writes failing tests first
2. Run tests (should fail)
3. Claude implements minimal passing code
4. Tell Claude NOT to alter tests
5. Iterate until green

### Visual Implementation

1. Provide reference image/mock
2. Claude implements UI
3. Screenshot and compare
4. Iterate 2-3 times

### Git Operations

- Compare releases: "Changes in v2.3.0 affecting auth?"
- History: `git blame`, `git log` for archaeology
- `/commit` for auto commit messages

---

## Context Management

### Reset Often

Use `/clear` between tasks to remove irrelevant history.

### Sub-Agents

- **Explore**: Read-only, may be lossy - follow up directly
- **General-Purpose**: Full context, complex sub-tasks
- **Plan**: Architecture focus

### Large Tasks

For 50+ items:
1. "Write errors to `FIXES.md` as checklist"
2. Address one by one

### Monitor

- `/context` - Check usage
- `/compact` - Reduce context
- Keep under 50-60% for complex tasks

---

## Safety

### Version Control

- **Separate branches** for Claude's work
- Never commit directly to main
- Review AI contributions like any PR

### Sandboxed Autonomy

For `--dangerously-skip-permissions`:
- Only in Docker/VMs
- No credentials or external access
- Review output, discard sandbox

### Multi-Agent Validation

1. Agent 1 writes code
2. Agent 2 (fresh) reviews
3. Agent 1 fixes issues

### Human-in-the-Loop

- **Escape**: Pause generation
- **Double Escape**: Rewind prompt
- Sessions are pair programming
- Interrupt early if noticing mistakes
