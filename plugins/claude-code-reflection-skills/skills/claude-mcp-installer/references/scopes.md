# MCP Installation Scopes

## Scope Types

### Local Scope (Default)

- **Storage**: `~/.claude.json` under project's path key
- **Visibility**: Only you, only current project
- **Use when**: Personal development servers, sensitive credentials, experimental configs

```bash
claude mcp add --transport http stripe https://mcp.stripe.com
# or explicitly:
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### Project Scope

- **Storage**: `.mcp.json` at project root
- **Visibility**: Everyone via version control
- **Use when**: Team-shared servers, project-specific integrations

```bash
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

**Example .mcp.json:**
```json
{
  "mcpServers": {
    "project-db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${DATABASE_URL}"]
    },
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

### User Scope

- **Storage**: `~/.claude.json` (global section)
- **Visibility**: Only you, all projects on your machine
- **Use when**: Personal utilities, cross-project tools

```bash
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

## Scope Precedence

When servers with the same name exist at multiple scopes:

1. **Local** (highest priority)
2. **Project**
3. **User** (lowest priority)

This allows overriding team configs with personal preferences.

## Managed MCP (Enterprise)

System administrators can control MCP via managed configuration files:

| Platform | Location |
|----------|----------|
| macOS | `/Library/Application Support/ClaudeCode/managed-mcp.json` |
| Linux/WSL | `/etc/claude-code/managed-mcp.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-mcp.json` |

### Exclusive Control

Takes complete control; users cannot modify:

```json
{
  "mcpServers": {
    "company-api": {
      "type": "http",
      "url": "https://internal.company.com/mcp"
    }
  }
}
```

### Allowlist/Denylist Control

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverUrl": "https://mcp.company.com/*" }
  ],
  "deniedMcpServers": [
    { "serverName": "dangerous-server" },
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```
