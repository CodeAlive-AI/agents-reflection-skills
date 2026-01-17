# Claude Code Reflection Skills

Meta-skills that let Claude Code configure itself through conversation.

## Skills

| Skill | Description |
|-------|-------------|
| **claude-mcp-manager** | Connect to databases, GitHub, APIs via MCP servers |
| **claude-hooks-manager** | Auto-format, auto-test, log commands after edits |
| **claude-settings-manager** | Configure permissions, sandbox, model selection |
| **claude-subagents-manager** | Create specialized agents for specific tasks |
| **claude-skills-manager** | Organize and share skills across projects |
| **claude-plugins-manager** | Package and publish your own plugins |
| **optimizing-claude-code** | Audit repos and optimize CLAUDE.md for agent work |

> All 7 skill descriptions use less than 500 tokens total.

## Installation

```bash
/plugin marketplace add CodeAlive-AI/claude-code-reflection-skills
/plugin install claude-code-reflection-skills@claude-code-reflection-skills
```

## Examples

- "Connect Claude to my PostgreSQL database"
- "Run Prettier after every edit"
- "Turn on sandbox mode"
- "Create a reviewer subagent"
- "Audit this repo for Claude Code readiness"

## License

MIT
