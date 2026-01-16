<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-blueviolet?style=for-the-badge" alt="Claude Code Plugin">
  <img src="https://img.shields.io/badge/Skills-6-blue?style=for-the-badge" alt="6 Skills">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">Claude Code Reflection Skills</h1>

<p align="center">
  <strong>Meta-skills that let Claude Code introspect and configure itself</strong>
</p>

<p align="center">
  Manage skills, subagents, plugins, settings, MCP servers, and hooks — all through natural conversation.
</p>

---

## Why Reflection Skills?

Claude Code is powerful, but configuring it requires editing JSON files, running CLI commands, and understanding multiple configuration systems. **Reflection skills change that.**

With this plugin, you can say things like:
- *"Connect to my Postgres database"* → MCP server installed and configured
- *"Create a read-only reviewer subagent"* → Custom agent with restricted permissions
- *"Lock down Claude for our security audit"* → Sandbox enabled, permissions restricted, logging added

**Claude configures itself through conversation.**

---

## Included Skills

| Skill | Purpose |
|-------|---------|
| **claude-skills-manager** | List, inspect, delete, move skills between user/project scopes |
| **claude-subagents-manager** | Create specialized agents with custom tools, models, and restrictions |
| **claude-plugins-manager** | Full plugin lifecycle: create, validate, publish, submit to Anthropic |
| **claude-settings-manager** | Configure model, permissions, sandbox, thinking mode, and more |
| **claude-mcp-installer** | Search MCP registry, install servers for databases, APIs, and services |
| **claude-hooks-manager** | Add automation triggers for logging, validation, and custom workflows |

---

## Use Cases

### 1. Instant Database Integration

> *"Connect Claude to my Postgres database so I can query it directly"*

MCP Installer searches the registry, finds the right server, installs it with your connection string. Claude can now execute SQL queries conversationally — no manual configuration needed.

---

### 2. Security-Hardened Compliance Mode

> *"Lock down Claude for our security audit: sandbox all commands, block .env access, and log every file operation"*

**Settings Manager** enables sandbox mode and deny rules. **Hooks Manager** adds PreToolUse logging to an audit trail. Result: a restricted, auditable assistant that meets compliance requirements.

---

### 3. One-Command Team Environment

> *"Set up this project so my whole team gets: opus model, our internal API server, and auto-format on save"*

All configured in project scope. Commit once to git, and every team member gets identical Claude configuration when they open the project.

---

### 4. Specialized Code Review Pipeline

> *"Create a reviewer subagent that only has read access, uses haiku for speed, and runs eslint before approving"*

**Subagents Manager** creates a restricted agent with `tools: Read, Grep, Glob` and `model: haiku`. **Hooks Manager** adds eslint validation. Fast, safe, automated code reviews.

---

### 5. Package and Distribute Team Tools

> *"Turn our custom skills into a plugin, publish to GitHub, and prepare for Anthropic's directory"*

**Plugins Manager** handles the full lifecycle:
```
init_plugin.py → validate_plugin.py → gh repo create → prepare_submission.py
```
From internal tools to official distribution in one conversation.

---

### 6. Capability Audit and Cleanup

> *"Show me everything installed. Find duplicates, move my api-helper to project scope for the team, delete unused subagents"*

All managers work together to audit your setup across scopes, reorganize capabilities, and clean up what you no longer need.

---

### 7. Context-Aware Project Switching

> *"For my payments project: connect Stripe MCP, enable extended thinking, add a hook that blocks commits without tests"*

Project-scoped configuration activates automatically when you enter the directory. Different projects get different Claude configurations — zero manual switching.

---

## Installation

### From GitHub

```bash
/plugin marketplace add CodeAlive-AI/claude-code-reflection-skills
/plugin install claude-code-reflection-skills
```

### Direct Install

```bash
/plugin install github:CodeAlive-AI/claude-code-reflection-skills
```

---

## Requirements

- Claude Code CLI
- `gh` CLI (for plugin publishing features)
- Python 3.x (for skill scripts)

---

## Structure

```
claude-code-reflection-skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── claude-skills-manager/
│   ├── claude-subagents-manager/
│   ├── claude-plugins-manager/
│   ├── claude-settings-manager/
│   ├── claude-mcp-installer/
│   └── claude-hooks-manager/
├── README.md
└── LICENSE
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with Claude Code</sub>
</p>
