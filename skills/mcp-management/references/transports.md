# MCP Transport Types

## Contents

- [HTTP Transport (Recommended)](#http-transport-recommended)
- [SSE Transport (Deprecated)](#sse-transport-deprecated)
- [Stdio Transport](#stdio-transport)
- [Popular Servers](#popular-servers)

## HTTP Transport (Recommended) — Streamable HTTP

Remote servers accessible via HTTP/HTTPS URLs. As of 2026-04 this is **the only supported remote transport** (SSE has reached end-of-life — see below).

```bash
claude mcp add --transport http <name> <url>

# With custom headers
claude mcp add --transport http <name> <url> --header "Authorization: Bearer TOKEN"

# Add via JSON
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer YOUR_PAT"}}'
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

**OAuth (2026):** HTTP transport supports OAuth 2.1 with RFC 9728 Protected Resource Metadata discovery, Client ID Metadata Document (CIMD / SEP-991), `oauth.authServerMetadataUrl` override, and step-up authorization via `insufficient_scope` 403 responses.

**Large tool results:** annotate MCP responses with `_meta["anthropic/maxResultSizeChars"]` (up to 500K) to avoid truncation of bulky payloads (e.g. DB schemas).

**Helper script env vars** (for `headersHelper`-style auth scripts): `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`.

## SSE Transport (Deprecated)

Server-Sent Events transport. **Deprecated by the MCP spec (2025-03-26 revision). Connections stop being accepted on April 1, 2026** — already past as of today (2026-04-26). Migrate any `"transport": "sse"` configs to `--transport http` (Streamable HTTP). Most servers that supported SSE accept Streamable HTTP on the same URL.

```bash
claude mcp add --transport sse <name> <url>   # legacy only
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
