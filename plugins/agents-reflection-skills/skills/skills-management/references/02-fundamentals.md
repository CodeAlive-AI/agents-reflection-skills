# Chapter 1: Fundamentals

## What is a skill?

A **skill** is a folder containing:

- **SKILL.md** (required): Instructions in Markdown with YAML frontmatter
- **scripts/** (optional): Executable code (Python, Bash, etc.)
- **references/** (optional): Documentation loaded as needed
- **assets/** (optional): Templates, fonts, icons used in output

## Core design principles

### Progressive Disclosure

Skills use a three-level system:

- **First level (YAML frontmatter):** Always loaded in Claude's system prompt. Provides just enough information for Claude to know when each skill should be used without loading all of it into context.
- **Second level (SKILL.md body):** Loaded when Claude thinks the skill is relevant to the current task. Contains the full instructions and guidance.
- **Third level (Linked files):** Additional files bundled within the skill directory that Claude can choose to navigate and discover only as needed.

This progressive disclosure minimizes token usage while maintaining specialized expertise.

### Composability

Claude can load multiple skills simultaneously. Your skill should work well alongside others, not assume it's the only capability available.

### Portability

Skills work identically across Claude.ai, Claude Code, and API. Create a skill once and it works across all surfaces without modification, provided the environment supports any dependencies the skill requires.

## For MCP Builders: Skills + Connectors

> Building standalone skills without MCP? Skip to Planning and Design - you can always return here later.

If you already have a working MCP server, you've done the hard part. Skills are the knowledge layer on top - capturing the workflows and best practices you already know, so Claude can apply them consistently.

**The kitchen analogy**

MCP provides the professional kitchen: access to tools, ingredients, and equipment.
Skills provide the recipes: step-by-step instructions on how to create something valuable.

Together, they enable users to accomplish complex tasks without needing to figure out every step themselves.

**How they work together:**

| MCP (Connectivity) | Skills (Knowledge) |
|---|---|
| Connects Claude to your service (Notion, Asana, Linear, etc.) | Teaches Claude how to use your service effectively |
| Provides real-time data access and tool invocation | Captures workflows and best practices |
| What Claude *can* do | How Claude *should* do it |

**Why this matters for your MCP users**

Without skills:
- Users connect your MCP but don't know what to do next
- Support tickets asking "how do I do X with your integration"
- Each conversation starts from scratch
- Inconsistent results because users prompt differently each time
- Users blame your connector when the real issue is workflow guidance

With skills:
- Pre-built workflows activate automatically when needed
- Consistent, reliable tool usage
- Best practices embedded in every interaction
- Lower learning curve for your integration
