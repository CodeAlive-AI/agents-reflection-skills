# MCP Transport Types

## HTTP Transport (Recommended)

Remote servers accessible via HTTP/HTTPS URLs.

```bash
claude mcp add --transport http <name> <url>

# With custom headers
claude mcp add --transport http <name> <url> --header "Authorization: Bearer TOKEN"
```

**Configuration format (.mcp.json):**
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

**Configuration format:**
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

# With environment variables
claude mcp add --transport stdio --env VAR1=value1 --env VAR2=value2 <name> -- <command>
```

**Configuration format:**
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

## Popular Stdio Servers

| Server | Command |
|--------|---------|
| Filesystem | `npx -y @modelcontextprotocol/server-filesystem /path` |
| PostgreSQL | `npx -y @bytebase/dbhub --dsn "postgresql://..."` |
| SQLite | `npx -y @modelcontextprotocol/server-sqlite path/to/db.sqlite` |
| Brave Search | `npx -y @anthropics/mcp-server-brave-search` |
| Puppeteer | `npx -y @anthropics/mcp-server-puppeteer` |

## Popular HTTP Servers

| Service | URL |
|---------|-----|
| GitHub | `https://api.githubcopilot.com/mcp/` |
| Sentry | `https://mcp.sentry.dev/mcp` |
| Notion | `https://mcp.notion.com/mcp` |
| Asana | `https://mcp.asana.com/sse` (SSE) |
| Linear | `https://mcp.linear.app/sse` (SSE) |

Browse more servers: https://github.com/modelcontextprotocol/servers
