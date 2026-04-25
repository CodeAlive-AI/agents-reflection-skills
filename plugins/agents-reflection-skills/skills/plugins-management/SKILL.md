---
name: plugins-management
description: Create, publish, delete, and submit Claude Code plugins. Use when user wants to (1) create a new plugin with proper structure, (2) create or configure a plugin marketplace, (3) publish plugins to GitHub/GitLab, (4) delete/uninstall plugins, (5) validate plugin structure, or (6) prepare and submit plugins to the official Anthropic directory.
---

# Claude Plugins Manager

Manage Claude Code plugins: create, validate, publish, delete, and submit to official directory.

**CRITICAL**: Before performing any deletion, uninstall, or removal operation, you MUST use the `AskUserQuestion` tool to confirm with the user. Never delete/uninstall plugins or remove marketplaces without explicit user confirmation.

## Quick Reference

| Task | Command/Script |
|------|----------------|
| Create plugin | `python scripts/init_plugin.py <name>` |
| Create marketplace | `python scripts/init_marketplace.py <name>` |
| Validate plugin | `python scripts/validate_plugin.py <path>` |
| Validate marketplace | `claude plugin validate <path>` |
| Prepare submission | `python scripts/prepare_submission.py <path> --email X --company-url Y` |
| Install plugin | `/plugin install <name>@<marketplace>` |
| Delete plugin | `/plugin uninstall <name>@<marketplace>` |
| Test plugin (dev) | `claude --plugin-dir ./my-plugin` |
| Reload after edits | `/reload-plugins` |
| Cut release tag | `claude plugin tag --push` |
| List installed | `claude plugin list [--json] [--available]` |
| Update plugin | `claude plugin update <name>@<marketplace>` |

## Workflows

### 1. Create a New Plugin

```bash
# Basic plugin with commands
python scripts/init_plugin.py my-plugin --path ./

# Full plugin with all components
python scripts/init_plugin.py my-plugin --path ./ --all

# Specific components
python scripts/init_plugin.py my-plugin --with-agents --with-skills
```

**Flags:**
- `--with-commands` (default): Include commands directory
- `--with-agents`: Include agents directory
- `--with-skills`: Include skills directory
- `--with-hooks`: Include hooks configuration
- `--with-mcp`: Include MCP server configuration
- `--all`: Include all components
- `--author "Name"`: Set author name

**After creation:**
1. Edit `.claude-plugin/plugin.json` with plugin details
2. Add commands to `commands/*.md` with YAML frontmatter
3. Add agents to `agents/*.md` if needed
4. Update `README.md` with documentation

### 2. Create a Marketplace

```bash
# Empty marketplace
python scripts/init_marketplace.py my-marketplace --path ./

# With initial plugin
python scripts/init_marketplace.py my-marketplace --with-plugin my-plugin
```

**After creation:**
1. Edit `.claude-plugin/marketplace.json`
2. Add plugins to `plugins/` directory
3. Push to GitHub: `git push origin main`

**Users install with:**
```bash
/plugin marketplace add username/my-marketplace
```

**Marketplace references:**
- Required file: `.claude-plugin/marketplace.json`
- Plugin entries must have `name` that matches each plugin's `plugin.json` name
- Use relative paths in `source` (e.g., `./plugins/my-plugin`), not absolute paths
- Use `${CLAUDE_PLUGIN_ROOT}` inside hooks and MCP configs referenced by marketplace plugins

### 3. Validate a Plugin

```bash
python scripts/validate_plugin.py ./my-plugin
```

**Validates:**
- plugin.json required fields (name, description, version, author)
- Semantic versioning format
- Command/agent frontmatter
- Hooks and MCP configuration
- README.md and LICENSE presence

**Also consider:**
- `claude plugin validate <path>` for marketplace JSON validation

### 4. Publish a Plugin

**To GitHub:**
```bash
cd my-marketplace
git init
git add .
git commit -m "Initial release"
git remote add origin https://github.com/user/my-marketplace.git
git push -u origin main

# Tag release
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

**Distribution methods:**
- GitHub: `/plugin marketplace add user/repo`
- GitLab: `/plugin marketplace add https://gitlab.com/user/repo.git`
- URL: `/plugin marketplace add https://example.com/marketplace.json`

### 5. Delete/Uninstall Plugins

**⚠️ ALWAYS confirm with user before deleting/uninstalling.** Use `AskUserQuestion` to ask: "Are you sure you want to uninstall '[plugin-name]'? This action cannot be undone."

```bash
# Uninstall from Claude Code
/plugin uninstall plugin-name@marketplace-name

# Remove marketplace (confirm with user first!)
/plugin marketplace remove marketplace-name
```

**To delete source files:** First confirm with user via `AskUserQuestion`, then remove the plugin directory from the marketplace's `plugins/` folder and update `marketplace.json`.

### 6. Submit to Anthropic's Official Directory

The submission script automatically gathers all required form fields using `gh` CLI and git.

**Prerequisites:**
1. Plugin pushed to GitHub
2. `gh` CLI installed and authenticated
3. All validation checks pass

**Prepare submission:**
```bash
# Basic - gathers repo URL and SHA automatically
python scripts/prepare_submission.py ./my-plugin

# With required contact info
python scripts/prepare_submission.py ./my-plugin \
  --email your@email.com \
  --company-url https://yourcompany.com

# Copy SHA to clipboard
python scripts/prepare_submission.py ./my-plugin --copy-sha

# Save to JSON file
python scripts/prepare_submission.py ./my-plugin --output submission.json

# Open form in browser
python scripts/prepare_submission.py ./my-plugin --open-form
```

**Form fields gathered automatically:**
| Field | Source |
|-------|--------|
| Link to Plugin | `gh repo view --json url` |
| Full SHA | `git rev-parse HEAD` |
| Plugin Homepage | plugin.json homepage or repo URL |
| Plugin Name | plugin.json name |
| Plugin Description | plugin.json description (50-100 words) |

**Fields you must provide:**
- `--email`: Primary contact email
- `--company-url`: Company/Organization URL

**Submission requirements:**
- Plugin must be pushed to GitHub
- Working directory should be clean (no uncommitted changes)
- Description should be 50-100 words
- README.md and LICENSE files present
- No secrets/API keys in code

## Plugin Structure Reference

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json       # Optional manifest (auto-discovered if absent)
├── skills/               # Agent skills (preferred over commands/)
│   └── */SKILL.md
├── commands/             # Skills as flat .md files
│   └── *.md
├── agents/               # AI subagents
│   └── *.md
├── output-styles/        # Output style definitions (2026)
├── themes/               # Color themes (2026)
├── monitors/             # Background monitors (2026, v2.1.105+)
│   └── monitors.json
├── hooks/
│   └── hooks.json        # Event handlers
├── bin/                  # Executables added to PATH (2026)
├── settings.json         # Default agent / subagentStatusLine (2026)
├── .mcp.json             # MCP servers
├── .lsp.json             # LSP server config (since v2.0.74)
├── package.json          # Auto-installed dependencies (2026)
├── README.md             # Documentation
├── CHANGELOG.md
└── LICENSE
```

**For detailed reference:** See [references/plugin-guide.md](references/plugin-guide.md)

## Critical Rules (Avoid Silent Failures)

- Keep `skills/`, `commands/`, `agents/`, `hooks/`, `monitors/`, `themes/`, `output-styles/`, `bin/` at the plugin root (never inside `.claude-plugin/`).
- Do not add standard component paths to `plugin.json`. Only specify non-standard paths starting with `./`.
- Use `${CLAUDE_PLUGIN_ROOT}` (cache path, changes per version) and `${CLAUDE_PLUGIN_DATA}` (persistent across updates) in hooks and MCP/LSP/monitor config paths. Relative paths break after install.
- Ensure hook scripts are executable (`chmod +x scripts/*`).
- Marketplace `plugins[].name` must match the plugin's `plugin.json` `name`.
- **Path traversal limit (2026)**: plugins cannot reference files outside their directory; use symlinks inside the plugin if needed.
- **Versioning (2026)**: omit `version` to use git SHA (every commit is a new version). Set `version` and bump for stable releases. Use `claude plugin tag` to cut release tags.

## Common Patterns

### Command File Format

```markdown
---
description: What this command does
---

# Command Name

Instructions for Claude when command is invoked.
```

### Agent File Format

```markdown
---
description: Agent specialty and purpose
---

# Agent Name

Detailed instructions and expertise.
```

### Hooks Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

### MCP Server Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["./servers/server.js"]
    }
  }
}
```

### Skill File Format

```markdown
---
name: my-skill
description: What this skill does and when to use it
---

# Skill Title

Instructions for Claude when this skill is invoked.
```

### Marketplace Entry Example

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "description": "Short description",
  "version": "1.0.0",
  "author": { "name": "Author Name" },
  "category": "productivity",
  "keywords": ["tag1", "tag2"],
  "strict": true
}
```
