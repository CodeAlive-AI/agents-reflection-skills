<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Marketplace-blueviolet?style=for-the-badge" alt="Claude Code Marketplace">
  <img src="https://img.shields.io/badge/Plugins-1-blue?style=for-the-badge" alt="1 Plugin">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">Claude Code Reflection Skills</h1>

<p align="center">
  <strong>A marketplace for meta-skills that let Claude Code configure itself</strong>
</p>

<p align="center">
  No more editing JSON files. Just ask Claude to set things up.
</p>

<p align="center">
  <a href="README.ru.md">Русский</a> •
  <a href="README.zh.md">中文</a> •
  <a href="README.pt-BR.md">Português</a>
</p>

---

## Installation

```bash
# Step 1: Add the marketplace
/plugin marketplace add https://github.com/CodeAlive-AI/claude-code-reflection-skills.git

# Step 2: Install the plugin
/plugin install claude-code-reflection-skills@claude-code-reflection-skills
```

---

## What's Included

The **claude-code-reflection-skills** plugin provides 7 skills:

| Skill | What It Does |
|-------|--------------|
| **claude-mcp-manager** | Connect to databases, GitHub, APIs via MCP servers |
| **claude-hooks-manager** | Auto-format, auto-test, log commands after edits |
| **claude-settings-manager** | Configure permissions, sandbox, model selection |
| **claude-subagents-manager** | Create specialized agents for specific tasks |
| **claude-skills-manager** | Organize and share skills across projects |
| **claude-plugins-manager** | Package and publish your own plugins |
| **optimizing-claude-code** | Audit repos and optimize CLAUDE.md for agent work |

> **Lightweight:** All 7 skill descriptions combined use less than 500 tokens in your context window.

---

## Use Cases (skills)

### claude-mcp-manager

> Connect to databases, GitHub, APIs via MCP servers

**Connect to Your Database**
> *"Connect Claude to my PostgreSQL database"*

Installs the [database MCP server](https://github.com/modelcontextprotocol/servers), configures your connection string. Now you can query your data conversationally.

**Install GitHub Integration**
> *"Connect Claude to GitHub so it can create PRs and manage issues"*

Installs the [official GitHub MCP server](https://github.com/github/github-mcp-server). Claude can now create branches, PRs, and work with issues directly.

**Update API Keys**
> *"Update my CodeAlive API key in the MCP config"*

Edits your `~/.claude.json` or `.mcp.json` to update API keys. Perfect for rotating credentials without reinstalling.

**Bulk Update Server Config**
> *"Change the timeout for all my MCP servers to 120 seconds"*

Bulk updates MCP server configuration. Adjust timeouts, environment variables, or command args across all servers at once.

---

### claude-hooks-manager

> Auto-format, auto-test, log commands after edits

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

### claude-settings-manager

> Configure permissions, sandbox, model selection

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

### claude-subagents-manager

> Create specialized agents for specific tasks

**Create a Code Reviewer**
> *"Create a reviewer subagent that can only read files, uses Opus for quality"*

Creates a [custom subagent](https://code.claude.com/docs/en/sub-agents) with `tools: Read, Grep, Glob` and `model: opus`. Thorough, insightful code reviews.

**Create a Test Runner**
> *"Create a subagent that runs tests and reports failures"*

Creates a specialized agent for running test suites with limited tool access for safety.

---

### claude-skills-manager

> Organize and share skills across projects

**List Available Skills**
> *"Show me all my installed skills"*

Lists skills from user and project scopes with their triggers and descriptions.

**Move Skills Between Scopes**
> *"Move this skill to my user scope so I can use it everywhere"*

Moves skills between project and user scopes for broader or narrower availability.

---

### claude-plugins-manager

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

- Claude Code CLI version 1.0.33 or later
- Python 3.x (for skill scripts)
- `gh` CLI (optional, for plugin publishing features)

---

## Structure

```
claude-code-reflection-skills/
├── .claude-plugin/
│   └── marketplace.json         (marketplace catalog)
├── plugins/
│   └── claude-code-reflection-skills/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── claude-mcp-manager/
│       │   ├── claude-hooks-manager/
│       │   ├── claude-settings-manager/
│       │   ├── claude-subagents-manager/
│       │   ├── claude-skills-manager/
│       │   ├── claude-plugins-manager/
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
