---
name: mcp-management
description: Search, install, configure, update, and remove MCP servers across coding agents (Claude Code, Cursor, VS Code, Claude Desktop, Gemini CLI, Codex, Goose, Zed, and more). Supports multi-agent installation via npx add-mcp, the official MCP registry, and direct config editing.
---

# MCP Server Management

**IMPORTANT**: After adding, removing, or updating MCP servers, inform the user to **restart the affected agent** for changes to take effect.

**CRITICAL**: Before removing any server, use `AskUserQuestion` to confirm with the user.

## Quick Reference (Claude Code)

```bash
# Install
claude mcp add --transport http <name> <url>
claude mcp add --transport stdio <name> -- <command> [args...]

# List/inspect
claude mcp list
claude mcp get <name>

# Remove (confirm with user first!)
claude mcp remove <name>
```

Options must come BEFORE the server name.

## Multi-Agent Installation (npx add-mcp)

Install MCP servers to multiple coding agents at once using [add-mcp](https://github.com/neondatabase/add-mcp):

```bash
# Remote server (HTTP)
npx add-mcp https://mcp.example.com/mcp

# npm package (stdio)
npx add-mcp @modelcontextprotocol/server-postgres

# Local command
npx add-mcp "npx -y @org/mcp-server --flag value"

# SSE transport
npx add-mcp https://mcp.example.com/sse --transport sse
```

### Options

| Flag | Description |
|------|-------------|
| `-g, --global` | Install globally instead of project-level |
| `-a, --agent <agent>` | Target specific agent(s), repeatable |
| `-n, --name <name>` | Custom server name |
| `-t, --transport <type>` | HTTP (default) or SSE |
| `--header <header>` | Custom HTTP headers, repeatable |
| `-y, --yes` | Skip confirmation prompts |
| `--all` | Install to all detected agents |

### Supported Agents

| Agent | CLI Argument | Supports Project-Level |
|-------|-------------|----------------------|
| Claude Code | `claude-code` | Yes (`.mcp.json`) |
| Claude Desktop | `claude-desktop` | No (global only) |
| Cursor | `cursor` | Yes (`.cursor/mcp.json`) |
| VS Code | `vscode` | Yes (`.vscode/mcp.json`) |
| Gemini CLI | `gemini-cli` | Yes (`.gemini/settings.json`) |
| Codex | `codex` | Yes (`.codex/config.toml`) |
| Goose | `goose` | No (global only) |
| GitHub Copilot CLI | `github-copilot-cli` | Yes (`.vscode/mcp.json`) |
| OpenCode | `opencode` | Yes (`opencode.json`) |
| Zed | `zed` | Yes (`.zed/settings.json`) |

### Examples

```bash
# Install to Claude Code and Cursor only
npx add-mcp -a claude-code -a cursor https://mcp.stripe.com

# Install npm package to all agents, globally
npx add-mcp -g --all @modelcontextprotocol/server-postgres

# Install with custom name and headers
npx add-mcp -n my-api --header "Authorization: Bearer TOKEN" https://api.example.com/mcp

# List available agents
npx add-mcp list-agents
```

See [references/multi-agent.md](references/multi-agent.md) for agent-specific config paths, formats, and transformations.

## Searching for MCP Servers

When users ask to find or install an MCP server, see [references/search.md](references/search.md) for:
- Official vendor server lookup (always try first)
- MCP Registry API queries (fallback)
- Known official servers table
- User choice template format

**Trust hierarchy**: Official vendor > MCP reference servers > Verified partners > Community

## Adding Servers (Claude Code)

### With Environment Variables

The `--env` CLI flag is unreliable with special characters. Instead:

1. Add server without env vars:
   ```bash
   claude mcp add --transport stdio <name> -- npx -y @package/mcp-server
   ```

2. Edit config file to add env vars. See [references/scopes.md](references/scopes.md) for file locations.

### Collect Configuration First

Before installing, check if the server needs API keys or tokens. Use `AskUserQuestion` to collect required values before running install commands.

## Updating Servers

No direct update command exists. Options:

1. **Edit config directly** (preferred for credential changes)
2. **Remove and re-add** (confirm removal with user first)
3. **Use environment variables** for credentials that change often

For OAuth servers (GitHub, Sentry): Run `/mcp` in Claude Code to re-authenticate.

## Removing Servers

Always confirm with user via `AskUserQuestion` before removing.

```bash
claude mcp remove <server-name>
```

For project-scoped servers in `.mcp.json`, delete the entry from the file after user confirmation.

## Reference

- **Search and known servers**: [references/search.md](references/search.md)
- **Multi-agent installation**: [references/multi-agent.md](references/multi-agent.md)
- **Transport types**: [references/transports.md](references/transports.md)
- **Scopes and config files**: [references/scopes.md](references/scopes.md)
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md)

## Scopes Summary (Claude Code)

| Scope | Flag | Config Location | Use Case |
|-------|------|-----------------|----------|
| Local | `--scope local` (default) | `~/.claude.json` | Personal dev servers |
| Project | `--scope project` | `.mcp.json` | Team-shared servers |
| User | `--scope user` | `~/.claude.json` | Cross-project tools |

## Environment Variable Syntax

In config files: `${VAR}` or `${VAR:-default}`

## Windows Note

Use `cmd /c` wrapper for npx:
```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```
