# Claude Code Reflection Skills

Meta-skills that let Claude Code configure itself through conversation.

## Skills

| Skill | Description |
|-------|-------------|
| **mcp-management** | Install and manage MCP servers across coding agents |
| **hooks-management** | Auto-format, auto-test, log commands after edits |
| **settings-management** | Configure permissions, sandbox, model selection |
| **subagents-management** | Create specialized agents for specific tasks |
| **skills-management** | Organize and share skills across projects |
| **plugins-management** | Package and publish your own plugins |
| **optimizing-claude-code** | Audit repos and optimize CLAUDE.md for agent work |

> All 7 skill descriptions use less than 500 tokens total.

## Installation

```bash
/plugin marketplace add CodeAlive-AI/claude-code-reflection-skills
/plugin install claude-code-reflection-skills@claude-code-reflection-skills
# Restart Claude Code for changes to take effect
```

## Examples

- "Connect Claude to my PostgreSQL database"
- "Run Prettier after every edit"
- "Turn on sandbox mode"
- "Create a reviewer subagent"
- "Audit this repo for Claude Code readiness"

## License

MIT
