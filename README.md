<p align="center">
  <img src="https://img.shields.io/badge/Agent_Skills-Marketplace-blueviolet?style=for-the-badge" alt="Agent Skills Marketplace">
  <img src="https://img.shields.io/badge/Skills-7-blue?style=for-the-badge" alt="7 Skills">
  <img src="https://img.shields.io/badge/Agents-10+-orange?style=for-the-badge" alt="10+ Agents">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">Agents Reflection Skills</h1>

<p align="center">
  <strong>Meta-skills that let AI coding agents configure themselves</strong>
</p>

<p align="center">
  No more editing config files. Just tell your agent what you need.
</p>

<p align="center">
  <a href="README.ru.md">Русский</a> •
  <a href="README.zh.md">中文</a> •
  <a href="README.pt-BR.md">Português</a>
</p>

---

## Installation

**Via Skills CLI (recommended):**

```bash
claude install-skill CodeAlive-AI/agents-reflection-skills
```

**Via plugin marketplace:**

```bash
/plugin marketplace add https://github.com/CodeAlive-AI/agents-reflection-skills.git
/plugin install claude-code-reflection-skills@claude-code-reflection-skills
# Restart Claude Code for changes to take effect
```

---

## What's Included

This plugin provides 7 skills that work across **Claude Code, Codex CLI, Cursor, VS Code, Gemini CLI**, and more:

| Skill | What It Does |
|-------|--------------|
| **mcp-management** | Install and manage MCP servers across 10+ coding agents |
| **hooks-management** | Manage hooks and automation for Claude Code and Codex CLI |
| **settings-management** | Configure settings for Claude Code (JSON) and Codex CLI (TOML) |
| **subagents-management** | Create and manage subagents across Claude Code and Codex CLI |
| **skills-management** | Organize, discover, and share skills for coding agents |
| **plugins-management** | Package and publish your own plugins |
| **optimizing-claude-code** | Audit repos and optimize CLAUDE.md for agent work |

> **Lightweight:** All 7 skill descriptions combined use less than 500 tokens in your context window.

---

## Use Cases (skills)

### mcp-management

> Install and manage MCP servers across 10+ coding agents

**Install to All Your Agents at Once**
> *"Install the Postgres MCP server to Claude Code, Cursor, and VS Code"*

Uses [add-mcp](https://github.com/neondatabase/add-mcp) to install MCP servers to 10+ coding agents (Claude Code, Cursor, VS Code, Claude Desktop, Gemini CLI, Codex, Goose, GitHub Copilot CLI, OpenCode, Zed) with a single command. Handles config format differences (JSON, YAML, TOML) automatically.

**Connect to Your Database**
> *"Connect Claude to my PostgreSQL database"*

Installs the [database MCP server](https://github.com/modelcontextprotocol/servers), configures your connection string. Now you can query your data conversationally.

**Install GitHub Integration**
> *"Connect Claude to GitHub so it can create PRs and manage issues"*

Installs the [official GitHub MCP server](https://github.com/github/github-mcp-server). Claude can now create branches, PRs, and work with issues directly.

**Multi-Agent Sync**
> *"Make sure all my coding agents have the same MCP servers"*

Configures MCP servers consistently across Claude Code, Cursor, VS Code, Gemini CLI, and other agents, handling each agent's config format and paths.

---

### hooks-management

> Manage hooks and automation for Claude Code and Codex CLI

**Auto-Format Code**
> *"Run Prettier on TypeScript files after every edit"*

Adds a PostToolUse hook. Every file Claude touches gets formatted automatically — no more style inconsistencies.

**Auto-Run Tests**
> *"Run pytest whenever Claude edits Python files"*

Adds a PostToolUse hook for `*.py` files. Instant feedback on whether changes broke anything.

**Log All Commands**
> *"Log every command Claude runs to an audit file"*

Adds a PreToolUse hook that appends commands to `~/.claude/command-log.txt`. Full audit trail.

**Block Dangerous Commands**
> *"Add hook that blocks global rm -rf commands"*

Adds a PreToolUse hook that rejects destructive commands before they run. Protects against accidental data loss.

**Require Confirmation**
> *"Add hook that asks user permission for commands containing 'db reset'"*

Adds a PreToolUse hook that pauses and requests confirmation for database resets or other sensitive operations.

---

### settings-management

> Configure settings for Claude Code (JSON) and Codex CLI (TOML)

**Enable Sandbox Mode**
> *"Turn on sandbox mode so Claude can work without asking permission for every command"*

Enables [native sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) — reduces permission prompts by 84% while keeping your system safe.

**Block Access to Secrets**
> *"Block Claude from reading .env files and anything in /secrets"*

Adds deny rules to permissions. Sensitive files stay protected even if Claude tries to access them.

**Switch Models**
> *"Use Opus model for this project"*

Updates settings to use `claude-opus-4-5` — better reasoning for complex architectural decisions.

**Share Team Configuration**
> *"Set up project settings so everyone gets the same Claude config"*

Creates `.claude/settings.json` in project scope. Commit once, entire team gets identical setup.

---

### subagents-management

> Create and manage subagents across Claude Code and Codex CLI

**Create a Code Reviewer**
> *"Create a reviewer subagent that can only read files, uses Opus for quality"*

Creates a [custom subagent](https://code.claude.com/docs/en/sub-agents) with `tools: Read, Grep, Glob` and `model: opus`. Thorough, insightful code reviews.

**Create a Test Runner**
> *"Create a subagent that runs tests and reports failures"*

Creates a specialized agent for running test suites with limited tool access for safety.

---

### skills-management

> Organize, discover, and share skills for coding agents

**List Available Skills**
> *"Show me all my installed skills"*

Lists skills from user and project scopes with their triggers and descriptions.

**Move Skills Between Scopes**
> *"Move this skill to my user scope so I can use it everywhere"*

Moves skills between project and user scopes for broader or narrower availability.

---

### plugins-management

> Package and publish your own plugins

**Create a Plugin**
> *"Create a new plugin with my custom skills"*

Scaffolds a new plugin structure with manifest, README, and skill directories.

**Publish to GitHub**
> *"Publish my plugin to GitHub"*

Packages your plugin and creates a GitHub release for others to install.

---

### optimizing-claude-code

> Audit repos and optimize CLAUDE.md for agent work

**Audit Project Readiness**
> *"Check if this repo is set up well for Claude Code"*

Runs a comprehensive audit analyzing CLAUDE.md files, settings, MCP configs, and project structure. Returns prioritized recommendations (P0/P1/P2) with specific suggestions for improvement.

**Optimize CLAUDE.md**
> *"Review my CLAUDE.md and suggest improvements"*

Evaluates memory file quality: structure, conciseness, @import validation, essential sections (commands, architecture, conventions). Provides concrete edits to make your project more agent-friendly.

---

## Requirements

- Claude Code CLI or Codex CLI
- Python 3.x (for skill scripts)
- `gh` CLI (optional, for plugin publishing features)

---

## Structure

```
agents-reflection-skills/
├── .claude-plugin/
│   └── marketplace.json         (marketplace catalog)
├── plugins/
│   └── claude-code-reflection-skills/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── mcp-management/
│       │   ├── hooks-management/
│       │   ├── settings-management/
│       │   ├── subagents-management/
│       │   ├── skills-management/
│       │   ├── plugins-management/
│       │   └── optimizing-claude-code/
│       ├── LICENSE
│       └── README.md
├── CLAUDE.md
├── LICENSE
└── README.md
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
