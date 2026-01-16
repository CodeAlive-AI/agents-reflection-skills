<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-blueviolet?style=for-the-badge" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Skills-6-blue?style=for-the-badge" alt="6 Skills">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">Claude Code Reflection Skills</h1>

<p align="center">
  <strong>Meta-skills that let Claude Code configure itself through conversation</strong>
</p>

<p align="center">
  No more editing JSON files. Just ask Claude to set things up.
</p>

---

## What's Included

| Skill | What It Does |
|-------|--------------|
| **claude-mcp-installer** | Connect to databases, GitHub, APIs via MCP servers |
| **claude-hooks-manager** | Auto-format, auto-test, log commands after edits |
| **claude-settings-manager** | Configure permissions, sandbox, model selection |
| **claude-subagents-manager** | Create specialized agents for specific tasks |
| **claude-skills-manager** | Organize and share skills across projects |
| **claude-plugins-manager** | Package and publish your own plugins |

---

## Top 10 Use Cases

### 1. Connect to Your Database

> *"Connect Claude to my PostgreSQL database"*

Installs the [database MCP server](https://github.com/modelcontextprotocol/servers), configures your connection string. Now you can query your data conversationally.

---

### 2. Auto-Format Code After Every Edit

> *"Run Prettier on TypeScript files after every edit"*

Adds a PostToolUse hook. Every file Claude touches gets formatted automatically — no more style inconsistencies.

---

### 3. Auto-Run Tests After Changes

> *"Run pytest whenever Claude edits Python files"*

Adds a PostToolUse hook for `*.py` files. Instant feedback on whether changes broke anything.

---

### 4. Enable Sandbox Mode

> *"Turn on sandbox mode so Claude can work without asking permission for every command"*

Enables [native sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) — reduces permission prompts by 84% while keeping your system safe.

---

### 5. Block Access to Secrets

> *"Block Claude from reading .env files and anything in /secrets"*

Adds deny rules to permissions. Sensitive files stay protected even if Claude tries to access them.

---

### 6. Create a Read-Only Code Reviewer

> *"Create a reviewer subagent that can only read files, uses Haiku for speed"*

Creates a [custom subagent](https://code.claude.com/docs/en/sub-agents) with `tools: Read, Grep, Glob` and `model: haiku`. Fast, safe code reviews.

---

### 7. Switch to Opus for Complex Tasks

> *"Use Opus model for this project"*

Updates settings to use `claude-opus-4-5` — better reasoning for complex architectural decisions.

---

### 8. Share Team Configuration

> *"Set up project settings so everyone gets the same Claude config"*

Creates `.claude/settings.json` in project scope. Commit once, entire team gets identical setup.

---

### 9. Log All Bash Commands

> *"Log every command Claude runs to an audit file"*

Adds a PreToolUse hook that appends commands to `~/.claude/command-log.txt`. Full audit trail.

---

### 10. Install GitHub Integration

> *"Connect Claude to GitHub so it can create PRs and manage issues"*

Installs the [official GitHub MCP server](https://github.com/github/github-mcp-server). Claude can now create branches, PRs, and work with issues directly.

---

## Installation

```bash
/plugin marketplace add CodeAlive-AI/claude-code-reflection-skills
/plugin install claude-code-reflection-skills
```

Or directly:

```bash
/plugin install github:CodeAlive-AI/claude-code-reflection-skills
```

---

## Requirements

- Claude Code CLI
- Python 3.x (for skill scripts)
- `gh` CLI (optional, for plugin publishing)

---

## Structure

```
claude-code-reflection-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── claude-mcp-installer/
│   ├── claude-hooks-manager/
│   ├── claude-settings-manager/
│   ├── claude-subagents-manager/
│   ├── claude-skills-manager/
│   └── claude-plugins-manager/
├── README.md
└── LICENSE
```

---

## Learn More

- [MCP Servers Guide](https://code.claude.com/docs/en/mcp)
- [Hooks Documentation](https://code.claude.com/docs/en/hooks-guide)
- [Custom Subagents](https://code.claude.com/docs/en/sub-agents)
- [Sandboxing](https://code.claude.com/docs/en/sandboxing)

---

## License

MIT — see [LICENSE](LICENSE)

---

<p align="center">
  <sub>Built with Claude Code</sub>
</p>
