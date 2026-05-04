# Prompt Engineering Skill

Universal prompt engineering skill for AI coding agents. Works with **any agent that supports the skills concept** -- Claude Code, Cursor, Gemini CLI, Codex, Goose, Windsurf, Roo Code, Cline, and [40+ other agents](https://skills.sh).

## What It Does

Provides structured techniques, audit workflows, and reference materials for crafting, reviewing, and optimizing prompts for any LLM.

### Capabilities

- **Craft prompts** -- XML-tagged structure, output control, scope constraints, uncertainty handling, long-context grounding
- **Audit/review prompts** -- 8-dimension checklist (clarity, structure, safety, hallucination, context, maintainability, model fit, eval readiness) with severity ratings and fix references
- **Agentic prompts** -- tool usage rules, user update patterns, self-check for high-risk outputs
- **Structured extraction** -- schema-based data extraction with validation
- **Prompt migration** -- cross-model migration checklist

### Reference Library (15 files, 5000+ lines)

| Category | Files |
|----------|-------|
| **Fundamentals** | Prompting introduction, techniques catalog (17 techniques), risks & misuses |
| **Model-specific** | Claude 4.6, GPT-5/5.1/5.2, Gemini 2.5/3/3.1 |
| **Mistakes & anti-patterns** | Hallucinations, structural fragility, context rot, prompt debt, security vulnerabilities |
| **Failure analysis** | 18-category taxonomy with minimal reproducible prompts, risk scoring, case studies |
| **Evaluation** | Metrics, CI gating, red-teaming workflows, tooling ecosystem |
| **Audit** | 43-check prompt audit checklist across 8 dimensions |

## Installation

### Via Skills CLI (recommended)

```bash
npx skills add CodeAlive-AI/ai-driven-development@prompt-engineering -g -y
```

### Manual

Copy the `prompt-engineering` directory (containing `SKILL.md` and `references/`) into your agent's skills folder:

| Agent | Path |
|-------|------|
| Claude Code | `~/.claude/skills/prompt-engineering/` |
| Cursor | `~/.cursor/skills/prompt-engineering/` |
| Gemini CLI | `~/.gemini/skills/prompt-engineering/` |
| Codex | `~/.codex/skills/prompt-engineering/` |
| Windsurf | `~/.codeium/windsurf/skills/prompt-engineering/` |
| Goose | `~/.config/goose/skills/prompt-engineering/` |
| Roo Code | `~/.roo/skills/prompt-engineering/` |

For the full list of 42 supported agents and their paths, see [skills.sh](https://skills.sh).

## Usage

Once installed, the skill activates automatically when you ask your agent to:

- "improve this prompt"
- "write a system prompt"
- "audit this prompt"
- "review my prompt"
- "optimize my instructions"
- "help me prompt engineer"

Or invoke directly: `/prompt-engineering`

## License

MIT
