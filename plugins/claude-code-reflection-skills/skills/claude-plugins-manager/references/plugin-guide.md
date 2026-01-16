# Claude Code Plugins Complete Reference

## Table of Contents
1. [Plugin Structure](#plugin-structure)
2. [Plugin Manifest](#plugin-manifest)
3. [Plugin Components](#plugin-components)
4. [Marketplace Structure](#marketplace-structure)
5. [Marketplace Configuration](#marketplace-configuration)
6. [Source Types](#source-types)
7. [CLI Commands](#cli-commands)
8. [Official Submission](#official-submission)

---

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin metadata
├── commands/                 # Optional: Custom slash commands
│   └── *.md
├── agents/                   # Optional: Specialized AI agents
│   └── *.md
├── skills/                   # Optional: Agent Skills
│   └── */SKILL.md
├── hooks/                    # Optional: Event handlers
│   └── hooks.json
├── .mcp.json                # Optional: MCP server config
├── README.md                # Required: Documentation
└── LICENSE                  # Recommended: License file
```

---

## Plugin Manifest

File: `.claude-plugin/plugin.json`

### Required Fields

```json
{
  "name": "plugin-name",
  "description": "Clear explanation of what the plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Author Name"
  }
}
```

### Optional Fields

```json
{
  "author": {
    "email": "email@example.com"
  },
  "homepage": "https://github.com/user/plugin",
  "repository": "https://github.com/user/plugin",
  "license": "MIT",
  "keywords": ["tag1", "tag2"]
}
```

### Version Format
Semantic versioning: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

---

## Plugin Components

### Commands (commands/*.md)

Markdown files with YAML frontmatter become slash commands.

```markdown
---
description: Short description of command
---

# Command Title

Instructions for Claude when command is invoked.
```

### Agents (agents/*.md)

Specialized agent definitions.

```markdown
---
description: Agent purpose and specialty
---

# Agent Name

Detailed instructions and expertise for this agent.
```

### Skills (skills/*/SKILL.md)

Agent skills with frontmatter.

```markdown
---
skill_name: Skill Display Name
description: What the skill does
when_to_use: Trigger conditions
---

# Skill Documentation
```

### Hooks (hooks/hooks.json)

Event handlers for Claude actions.

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "./scripts/validate.sh",
          "description": "Validate after edits"
        }
      ]
    }
  ],
  "PrePrompt": [
    {
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Security reminder text",
          "description": "Description"
        }
      ]
    }
  ]
}
```

**Hook Events:** PrePrompt, PostToolUse

### MCP Servers (.mcp.json)

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["./servers/server.js"],
      "env": {
        "VAR": "${ENV_VAR}"
      }
    }
  }
}
```

---

## Marketplace Structure

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace catalog
├── plugins/                  # Optional: hosted plugins
│   └── plugin-name/
└── README.md
```

---

## Marketplace Configuration

File: `.claude-plugin/marketplace.json`

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name",
    "email": "email@example.com"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0",
    "homepage": "https://github.com/user/marketplace",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "author": { "name": "Author" },
      "category": "productivity",
      "keywords": ["tag1", "tag2"]
    }
  ]
}
```

### Advanced Plugin Entry

Override component locations:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin",
  "commands": ["./commands/core/", "./commands/extra/"],
  "agents": ["./agents/agent1.md"],
  "hooks": { "PostToolUse": [...] },
  "mcpServers": { "server": {...} },
  "strict": false
}
```

---

## Source Types

### Relative Path
```json
{ "source": "./plugins/local-plugin" }
```

### GitHub
```json
{
  "source": {
    "source": "github",
    "repo": "owner/repo",
    "ref": "main"
  }
}
```

### Git URL
```json
{
  "source": {
    "source": "git",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "v1.0.0"
  }
}
```

### Direct URL
```json
{
  "source": {
    "source": "url",
    "url": "https://example.com/marketplace.json"
  }
}
```

---

## CLI Commands

### Plugin Management
```bash
/plugin                              # Browse plugins
/plugin install <name>@<marketplace>
/plugin uninstall <name>@<marketplace>
/plugin enable <name>@<marketplace>
/plugin disable <name>@<marketplace>
```

### Marketplace Management
```bash
/plugin marketplace add <source>
/plugin marketplace list
/plugin marketplace update <name>
/plugin marketplace remove <name>
```

### Validation
```bash
claude plugin validate <path>
```

---

## Official Submission

### Anthropic Plugin Submission Form

The official submission form requires the following fields:

| Field | Required | Description | Auto-gathered |
|-------|----------|-------------|---------------|
| Link to Plugin | Yes | GitHub repository URL | `gh repo view --json url` |
| Full SHA | Yes | Commit SHA to be reviewed | `git rev-parse HEAD` |
| Plugin Homepage | Yes | Documentation/landing page | plugin.json homepage |
| Company/Organization URL | Yes | Your company website | `--company-url` flag |
| Primary Contact Email | Yes | Email for communication | `--email` flag |
| Plugin Name | Yes | Name for Plugin Directory | plugin.json name |
| Plugin Description | Yes | 50-100 words | plugin.json description |

### Prepare Submission Command

```bash
python scripts/prepare_submission.py ./my-plugin \
  --email your@email.com \
  --company-url https://yourcompany.com \
  --copy-sha
```

### Prerequisites
- Plugin pushed to GitHub
- `gh` CLI installed and authenticated (`gh auth login`)
- Working directory clean (commit all changes)
- Description is 50-100 words

### Requirements
- Clear, comprehensive documentation
- Well-tested functionality
- Security best practices followed
- Professional code quality
- Responsive maintainer

### Quality Checklist
- [ ] plugin.json has all required fields
- [ ] README.md is comprehensive
- [ ] All commands work correctly
- [ ] Agents behave as expected
- [ ] Hooks trigger appropriately
- [ ] No API keys or secrets in code
- [ ] LICENSE file included
- [ ] Version follows semver
- [ ] Description is 50-100 words
- [ ] Plugin pushed to GitHub
- [ ] Working directory is clean
