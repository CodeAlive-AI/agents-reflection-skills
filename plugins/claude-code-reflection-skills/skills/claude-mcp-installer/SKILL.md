---
name: claude-mcp-installer
description: Search, install, configure, update, and remove MCP servers in Claude Code. Can search the official MCP registry to find servers, preferring official/trusted sources and requiring user permission before installing.
---

# MCP Server Management

MCP (Model Context Protocol) enables Claude Code to connect to external tools, databases, and APIs.

**IMPORTANT**: After adding, removing, or updating MCP servers, always inform the user that they need to **restart Claude Code** (exit and relaunch) for changes to take effect. MCP servers are loaded at startup.

**CRITICAL**: Before performing any removal operation, you MUST use the `AskUserQuestion` tool to confirm with the user. Never remove an MCP server without explicit user confirmation.

## Quick Reference

```bash
# Install - HTTP server (recommended for remote)
claude mcp add --transport http <name> <url>

# Install - Stdio server (for local/npm packages)
claude mcp add --transport stdio <name> -- <command> [args...]

# List/inspect servers
claude mcp list
claude mcp get <name>

# Remove server
claude mcp remove <name>
```

## Searching for MCP Servers

When users ask to find, search for, or check if an MCP exists for a service, follow this workflow.

### Search Workflow

**Step 1: Find the Official Vendor Source (MANDATORY FIRST STEP)**

Use WebSearch to find the official MCP server from the vendor:
```
"[service-name] MCP server official" OR "[service-name] Model Context Protocol"
```

Look for:
- Official vendor GitHub repo (e.g., `github.com/github/github-mcp-server` for GitHub)
- Official documentation page about MCP integration
- Vendor's announcement/blog post about MCP support

**Step 2: Fetch installation instructions from official source**

Use WebFetch on the official repo README or documentation to get:
- All available deployment options (Remote, Local/npm, Docker)
- Required environment variables and authentication
- The vendor's recommended approach

**Step 3: If no official source found, query MCP Registry**

Use WebFetch to query:
```
https://registry.modelcontextprotocol.io/v0.1/servers?search=<query>&limit=20
```

**Step 4: Present ALL deployment options to user**

Always show available options and let user choose. Use `AskUserQuestion` with format:

```
## MCP Server for [Service]: Installation Options

### Option 1: Remote (Recommended) ⭐
- Type: HTTP/SSE
- URL: https://mcp.service.com/mcp
- Pros: No local setup, always up-to-date, managed by vendor
- Install: `claude mcp add --transport http [name] [url]`

### Option 2: Local (npm)
- Type: Stdio
- Package: @vendor/mcp-server
- Pros: Works offline, full control
- Requires: Node.js, API key
- Install: `claude mcp add --transport stdio [name] -- npx -y @vendor/mcp-server`

### Option 3: Docker
- Image: vendor/mcp-server
- Pros: Isolated environment, consistent setup
- Requires: Docker installed
- Install: `claude mcp add --transport stdio [name] -- docker run -i vendor/mcp-server`

Which option would you like to install?
```

**Step 5: Collect required configuration from user**

Before installing, check if the MCP server requires any configuration (API keys, URLs, tokens, etc.). If so, use `AskUserQuestion` to collect this information BEFORE running the install command.

Example:
```
This MCP server requires configuration:

1. **API Key** (required): Your service API key
2. **Workspace ID** (optional): Your workspace identifier

Please provide the required values:
```

**Step 6: CRITICAL - Get explicit user permission** before installing.

### Deployment Types

| Type | Transport | Best For | Pros | Cons |
|------|-----------|----------|------|------|
| **Remote** | HTTP/SSE | Most users | No setup, always updated, vendor-managed | Requires internet, vendor dependency |
| **Local** | Stdio | Offline use, customization | Works offline, full control | Requires Node.js, manual updates |
| **Docker** | Stdio | Isolation, CI/CD | Clean environment, reproducible | Requires Docker, more resources |

### Trust Hierarchy

When multiple servers exist for the same service, prefer:

1. **Official Vendor Server** (Highest Trust)
   - From the service vendor's own GitHub org or domain
   - Example: `github.com/github/github-mcp-server`, `mcp.notion.com`

2. **Official MCP Reference Server**
   - From `modelcontextprotocol` or `anthropic`
   - Example: Filesystem, Git, Memory servers

3. **Verified Partner Server**
   - Listed in MCP registry with verified publisher

4. **Community Server** (Verify before use)
   - Check GitHub stars, activity, security issues

See [references/search.md](references/search.md) for the list of known official vendor MCP servers and detailed API documentation.

## Adding MCP Servers with Environment Variables

**IMPORTANT**: The `--env` / `-e` CLI flag is unreliable, especially with URLs containing special characters or multiple environment variables. The recommended approach is to:

1. **Add the server without env vars first**:
   ```bash
   claude mcp add <name> -- npx -y @package/mcp-server
   ```

2. **Then edit the config file** to add environment variables:

   For **local/project scope**, edit `~/.claude.json` and find your project's `mcpServers` section:
   ```json
   {
     "projects": {
       "/path/to/your/project": {
         "mcpServers": {
           "your-server": {
             "type": "stdio",
             "command": "npx",
             "args": ["-y", "@package/mcp-server"],
             "env": {
               "API_URL": "https://your-api.com/api",
               "API_KEY": "your-api-key"
             }
           }
         }
       }
     }
   }
   ```

   For **project scope** (shared with team), create/edit `.mcp.json` in project root:
   ```json
   {
     "mcpServers": {
       "your-server": {
         "type": "stdio",
         "command": "npx",
         "args": ["-y", "@package/mcp-server"],
         "env": {
           "API_URL": "https://your-api.com/api",
           "API_KEY": "${MY_API_KEY}"
         }
       }
     }
   }
   ```

3. **Restart Claude Code** for changes to take effect.

### Why Not Use `--env` Flag?

The CLI parser can misinterpret arguments when:
- URLs contain special characters (`:`, `/`, `?`)
- Multiple `-e` flags are used consecutively
- Values contain spaces or special characters

See [GitHub Issue #1254](https://github.com/anthropics/claude-code/issues/1254) for known environment variable handling bugs.

## Removing MCP Servers

**⚠️ ALWAYS confirm with user before removing.** Use `AskUserQuestion` to ask: "Are you sure you want to remove the MCP server '[server-name]'? This action cannot be undone."

```bash
# Remove by name
claude mcp remove <server-name>

# Examples
claude mcp remove github
claude mcp remove db
claude mcp remove notion
```

**For project-scoped servers** (in `.mcp.json`), first confirm with user via `AskUserQuestion`, then delete the entry from the file or remove the file if empty.

## Updating MCP Servers

There is no direct `claude mcp update` command. Use one of these approaches:

### Option 1: Remove and Re-add (Recommended)

**Note:** When using this option, confirm the removal with the user first via `AskUserQuestion`.

```bash
# Remove existing (confirm with user first!)
claude mcp remove api-server

# Re-add with new credentials
claude mcp add --transport http api-server https://api.example.com/mcp \
  --header "Authorization: Bearer NEW_TOKEN"
```

### Option 2: Edit Configuration Files Directly

**For local/user scope** - Edit `~/.claude.json`:
```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer NEW_API_KEY"
      }
    }
  }
}
```

**For project scope** - Edit `.mcp.json` in project root:
```json
{
  "mcpServers": {
    "db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "postgresql://user:NEWPASS@host:5432/db"],
      "env": {
        "API_KEY": "new-key-value"
      }
    }
  }
}
```

### Option 3: Use Environment Variables (Best Practice)

Store credentials in environment variables so updates don't require config changes:

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${MY_API_KEY}"
      }
    }
  }
}
```

Then update the environment variable in your shell profile (`~/.zshrc`, `~/.bashrc`):
```bash
export MY_API_KEY="new-key-value"
```

### Re-authenticate OAuth Servers

For OAuth-protected servers (GitHub, Sentry, etc.):
```bash
# In Claude Code, run:
/mcp
# Follow browser prompts to re-authenticate
```

## Installation Workflow

1. **Determine transport type**:
   - **HTTP**: Remote servers with URL endpoints (most common)
   - **SSE**: Server-Sent Events (deprecated, use HTTP)
   - **Stdio**: Local servers via npm/command execution

2. **Choose scope**:
   - `--scope local` (default): Private, current project only
   - `--scope project`: Shared via `.mcp.json` in version control
   - `--scope user`: Available across all projects

3. **Run installation command** (options must come BEFORE server name)

4. **Authenticate if needed**: `/mcp` command in Claude Code

## Common Installations

### GitHub (example)
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

### With Auth Header
```bash
claude mcp add --transport http api-server https://api.example.com/mcp \
  --header "Authorization: Bearer YOUR_TOKEN"
```

## Detailed Reference

- **Search and verification**: See [references/search.md](references/search.md)
- **Transport types and configuration**: See [references/transports.md](references/transports.md)
- **Scopes and precedence**: See [references/scopes.md](references/scopes.md)
- **Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md)

## Configuration Files

| Scope | Location | Use Case |
|-------|----------|----------|
| Local | `~/.claude.json` (project path) | Personal dev servers |
| Project | `.mcp.json` (project root) | Team-shared servers |
| User | `~/.claude.json` | Cross-project tools |

## Environment Variables

```json
{
  "mcpServers": {
    "api": {
      "type": "http",
      "url": "${API_URL:-https://default.com}/mcp",
      "headers": { "Authorization": "Bearer ${API_KEY}" }
    }
  }
}
```

Syntax: `${VAR}` or `${VAR:-default}`

## Windows Note

Use `cmd /c` wrapper for npx commands:
```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```
