# Claude Code Reflection Skills Plugin

Meta-skills that let Claude Code configure itself through conversation.

## Included Skills

- **claude-mcp-installer** - Connect to databases, GitHub, APIs via MCP servers
- **claude-hooks-manager** - Auto-format, auto-test, log commands after edits
- **claude-settings-manager** - Configure permissions, sandbox, model selection
- **claude-subagents-manager** - Create specialized agents for specific tasks
- **claude-skills-manager** - Organize and share skills across projects
- **claude-plugins-manager** - Package and publish your own plugins

## Installation

This plugin is distributed through the CodeAlive-AI marketplace:

```bash
/plugin marketplace add CodeAlive-AI/claude-code-reflection-skills
/plugin install claude-code-reflection-skills@claude-code-reflection-skills
```

## Usage Examples

- "Connect Claude to my PostgreSQL database"
- "Run Prettier on TypeScript files after every edit"
- "Turn on sandbox mode"
- "Block Claude from reading .env files"
- "Create a reviewer subagent that can only read files"

## License

MIT - see LICENSE file for details
