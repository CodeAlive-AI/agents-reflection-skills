# MCP Transport Types

## Contents

- [HTTP Transport (Recommended)](#http-transport-recommended)
- [SSE Transport (Deprecated)](#sse-transport-deprecated)
- [Stdio Transport](#stdio-transport)
- [Popular Servers](#popular-servers)

## HTTP Transport (Recommended)

Remote servers accessible via HTTP/HTTPS URLs.

```bash
claude mcp add --transport http <name> <url>

# With custom headers
claude mcp add --transport http <name> <url> --header "Authorization: Bearer TOKEN"
```

**Config format:**
```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://api.example.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

**Best for:** Cloud services, SaaS integrations, OAuth-protected APIs.

## SSE Transport (Deprecated)

Server-Sent Events transport. Use HTTP instead when possible.

```bash
claude mcp add --transport sse <name> <url>
```

**Config format:**
```json
{
  "mcpServers": {
    "server-name": {
      "type": "sse",
      "url": "https://example.com/sse"
    }
  }
}
```

## Stdio Transport

Local servers via subprocess execution. Required for npm packages.

```bash
claude mcp add --transport stdio <name> -- <command> [args...]
```

**Config format:**
```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "/path/to/server",
      "args": ["--config", "/path/to/config.json"],
      "env": {
        "API_KEY": "${MY_API_KEY}",
        "DEBUG": "true"
      }
    }
  }
}
```

**Best for:** Local databases, npm packages, custom scripts.

## Popular Servers

### Stdio Servers

| Server | Command |
|--------|---------|
| Filesystem | `npx -y @modelcontextprotocol/server-filesystem /path` |
| PostgreSQL | `npx -y @bytebase/dbhub --dsn "postgresql://..."` |
| SQLite | `npx -y @modelcontextprotocol/server-sqlite path/to/db.sqlite` |
| Brave Search | `npx -y @anthropics/mcp-server-brave-search` |
| Puppeteer | `npx -y @anthropics/mcp-server-puppeteer` |

### HTTP Servers

| Service | URL |
|---------|-----|
| GitHub | `https://api.githubcopilot.com/mcp/` |
| Sentry | `https://mcp.sentry.dev/mcp` |
| Notion | `https://mcp.notion.com/mcp` |
| Asana | `https://mcp.asana.com/sse` (SSE) |
| Linear | `https://mcp.linear.app/sse` (SSE) |

Browse more: https://github.com/modelcontextprotocol/servers
