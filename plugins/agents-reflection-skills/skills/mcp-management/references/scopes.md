# MCP Installation Scopes

## Contents

- [Scope Types](#scope-types)
- [Config File Locations](#config-file-locations)
- [Scope Precedence](#scope-precedence)
- [Config File Examples](#config-file-examples)
- [Managed MCP (Enterprise)](#managed-mcp-enterprise)

## Scope Types

### Local Scope (Default)

```bash
claude mcp add --transport http stripe https://mcp.stripe.com
# or explicitly:
claude mcp add --scope local --transport http stripe https://mcp.stripe.com
```

- **Storage**: `~/.claude.json` under project's path key
- **Visibility**: Only you, only current project
- **Use when**: Personal dev servers, sensitive credentials, experimental configs

### Project Scope

```bash
claude mcp add --scope project --transport http paypal https://mcp.paypal.com/mcp
```

- **Storage**: `.mcp.json` at project root
- **Visibility**: Everyone via version control
- **Use when**: Team-shared servers, project-specific integrations

### User Scope

```bash
claude mcp add --scope user --transport http hubspot https://mcp.hubspot.com/anthropic
```

- **Storage**: `~/.claude.json` (global section)
- **Visibility**: Only you, all projects
- **Use when**: Personal utilities, cross-project tools

## Config File Locations

| Scope | File | Section |
|-------|------|---------|
| Local | `~/.claude.json` | `projects.<project-path>.mcpServers` |
| Project | `.mcp.json` (project root) | `mcpServers` |
| User | `~/.claude.json` | `mcpServers` |

## Scope Precedence

When servers with the same name exist at multiple scopes:

1. **Local** (highest priority)
2. **Project**
3. **User** (lowest priority)

This allows overriding team configs with personal preferences.

## Config File Examples

### Local/User scope (~/.claude.json)

```json
{
  "mcpServers": {
    "my-global-server": {
      "type": "http",
      "url": "https://api.example.com/mcp"
    }
  },
  "projects": {
    "/path/to/project": {
      "mcpServers": {
        "project-db": {
          "type": "stdio",
          "command": "npx",
          "args": ["-y", "@bytebase/dbhub", "--dsn", "${DATABASE_URL}"],
          "env": {
            "API_KEY": "${MY_API_KEY}"
          }
        }
      }
    }
  }
}
```

### Project scope (.mcp.json)

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

### Environment Variables in Config

Syntax: `${VAR}` or `${VAR:-default}`

```json
{
  "mcpServers": {
    "api": {
      "type": "http",
      "url": "${API_URL:-https://default.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

## Managed MCP (Enterprise)

System administrators can control MCP via managed configuration files.

### File Locations

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
