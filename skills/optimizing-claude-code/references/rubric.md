# Optimization Rubric

## Scoring Guide

Use this rubric to evaluate CLAUDE.md files and overall Claude Code readiness.

---

## CLAUDE.md Quality Criteria

### Structure (0-3 points)

| Score | Criteria |
|-------|----------|
| 0 | No CLAUDE.md or empty file |
| 1 | Exists but unstructured (no headings, wall of text) |
| 2 | Has some headings but disorganized or incomplete |
| 3 | Clear sections: Overview, Commands, Architecture, Conventions, Gotchas |

### Conciseness (0-3 points)

| Score | Criteria |
|-------|----------|
| 0 | >500 lines without @imports (bloated) |
| 1 | 300-500 lines, could be split |
| 2 | 100-300 lines, reasonable size |
| 3 | <100 lines using @imports for details, or appropriately sized for simple project |

### Commands Section (0-2 points)

| Score | Criteria |
|-------|----------|
| 0 | No commands documented |
| 1 | Some commands but missing key ones (build/test/lint/dev) |
| 2 | Complete commands with clear descriptions |

### Architecture Overview (0-2 points)

| Score | Criteria |
|-------|----------|
| 0 | No architecture information |
| 1 | Basic directory listing |
| 2 | Clear module boundaries, entry points, key files identified |

### Conventions (0-2 points)

| Score | Criteria |
|-------|----------|
| 0 | No coding conventions |
| 1 | Some conventions but incomplete |
| 2 | Clear style, naming, error handling, and testing conventions |

### Import Hygiene (0-2 points)

| Score | Criteria |
|-------|----------|
| 0 | Broken @imports or deeply nested chains |
| 1 | Some @imports but organization unclear |
| 2 | All @imports resolve, shallow nesting, clear purpose |

### Freshness (0-2 points)

| Score | Criteria |
|-------|----------|
| 0 | Stale (commands don't match tooling, architecture outdated) |
| 1 | Partially current |
| 2 | Up-to-date with current project state |

---

## Overall CLAUDE.md Score

| Total | Rating |
|-------|--------|
| 0-4 | Poor - Needs significant work |
| 5-8 | Fair - Basic functionality, room for improvement |
| 9-12 | Good - Solid foundation |
| 13-16 | Excellent - Well-optimized |

---

## Settings Quality Criteria

### Permission Configuration (0-2 points)

| Score | Criteria |
|-------|----------|
| 0 | No configuration or overly permissive (`Bash(*)`) |
| 1 | Some restrictions but could be tighter |
| 2 | Appropriate balance of capability and safety |

### MCP Integration (0-2 points)

| Score | Criteria |
|-------|----------|
| 0 | No MCP servers configured when beneficial |
| 1 | Some servers but not optimally configured |
| 2 | Relevant tools integrated with clear descriptions |

---

## Project Scale Considerations

### Small Projects (<500 files)

- Single CLAUDE.md usually sufficient
- Minimal @imports needed
- Focus on commands and conventions

### Medium Projects (500-3000 files)

- Consider nested CLAUDE.md for distinct modules
- Use @imports for detailed documentation
- Document key entry points clearly

### Large Projects (>3000 files)

- Context engine or retrieval layer recommended
- Strategic CLAUDE.md placement
- Focus on navigation aids

---

## Anti-Patterns to Flag

### Memory File Issues

- **Duplication**: Same information in multiple CLAUDE.md files
- **Conflicts**: Contradictory instructions across files
- **Staleness**: Commands reference removed scripts/tools
- **Bloat**: Copy-pasted documentation instead of @imports
- **Missing**: No CLAUDE.md at all

### Settings Issues

- **Overly permissive**: `Bash(*)` allows all shell commands
- **No customization**: Default settings for complex projects
- **Conflicting scopes**: Project and user settings at odds

### Structural Issues

- **Wall of text**: No markdown formatting
- **Deep nesting**: @imports chain >2 levels deep
- **Hidden files**: Important context buried in unusual locations

---

## Recommended CLAUDE.md Template

```markdown
# Project Name

Brief description in 1-2 sentences.

## Commands

| Command | Description |
|---------|-------------|
| `npm run build` | Build production bundle |
| `npm test` | Run test suite |
| `npm run lint` | Check code style |
| `npm run dev` | Start dev server |

## Architecture

- `src/components/` - React components
- `src/api/` - API client and types
- `src/hooks/` - Custom React hooks
- `src/utils/` - Shared utilities

Key entry point: `src/App.tsx`

## Conventions

- TypeScript strict mode enabled
- Functional components with hooks
- Error boundaries at route level
- Tests co-located with source files

## Gotchas

- API requires auth token in `Authorization` header
- WebSocket reconnects automatically after 30s
- Cache invalidation needs manual refresh in dev

## References

For detailed API documentation, see @docs/api.md
For database schema, see @docs/schema.md
```

---

## Quick Assessment Checklist

Use during audit to quickly evaluate CLAUDE.md:

- [ ] File exists in expected location
- [ ] Has clear section headings
- [ ] Commands section present and accurate
- [ ] Architecture/structure documented
- [ ] Conventions specified
- [ ] No broken @imports
- [ ] Size appropriate (<300 lines or uses @imports)
- [ ] Content matches current project state
