# OpenCode MCP Reference

Detailed MCP server configuration for [anomalyco/opencode](https://github.com/anomalyco/opencode) (v1.14.x).

## Contents

- [Config Locations](#config-locations)
- [Server Types](#server-types)
- [Local (stdio) Server](#local-stdio-server)
- [Remote (http) Server](#remote-http-server)
- [OAuth and Auth](#oauth-and-auth)
- [Tool Permissions for MCP](#tool-permissions-for-mcp)
- [CLI Commands](#cli-commands)
- [Field Differences vs Other Agents](#field-differences-vs-other-agents)

## Config Locations

| Scope | Path |
|-------|------|
| Global | `~/.config/opencode/opencode.json` |
| Project | `<project>/opencode.json` (or `.opencode/opencode.json`) |

The MCP config lives under the top-level `mcp` key. Multiple files merge (later wins; project overrides global).

## Server Types

```json
{
  "mcp": {
    "<server-name>": {
      "type": "local",   // or "remote"
      ...
    }
  }
}
```

OpenCode requires the `type` field — there is no implicit default.

## Local (stdio) Server

```json
{
  "mcp": {
    "postgres": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-postgres"],
      "environment": {
        "DATABASE_URL": "{env:DATABASE_URL}"
      },
      "enabled": true,
      "timeout": 5000
    }
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `type` | string | Must be `"local"` for stdio |
| `command` | string[] | First element is the binary; rest are args. **Note: array, not split into `command`/`args`** |
| `environment` | object | Env vars passed to the child process. **Key name is `environment`, NOT `env`** |
| `enabled` | boolean | Default `true`. Set `false` to disable without deleting |
| `timeout` | number (ms) | Tool-fetching timeout (default `5000`) |

## Remote (http) Server

```json
{
  "mcp": {
    "stripe": {
      "type": "remote",
      "url": "https://mcp.stripe.com",
      "headers": {
        "Authorization": "Bearer {env:STRIPE_API_KEY}"
      },
      "enabled": true,
      "timeout": 30000
    }
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `type` | string | Must be `"remote"` for HTTP/SSE |
| `url` | string | Endpoint |
| `headers` | object | Static HTTP headers; supports `{env:VAR}` substitution |
| `oauth` | boolean / object | OAuth configuration (see below) |
| `enabled` | boolean | Default `true` |
| `timeout` | number (ms) | Per-call timeout |

## OAuth and Auth

For servers that require OAuth (GitHub, Sentry, Linear, etc.):

```json
{
  "mcp": {
    "github": {
      "type": "remote",
      "url": "https://api.githubcopilot.com/mcp/",
      "oauth": true
    }
  }
}
```

```bash
# Authenticate or re-authenticate
opencode mcp auth github

# Remove stored credentials
opencode mcp logout github

# Diagnose OAuth failures
opencode mcp debug github
```

Tokens are stored alongside other auth in `~/.local/share/opencode/auth.json`.

## Tool Permissions for MCP

Use the `permission` block to control whether MCP tool calls run silently, prompt, or are blocked. Wildcards match tool names:

```json
{
  "permission": {
    "github_*": "allow",
    "stripe_*": "ask",
    "internal_*": "deny"
  }
}
```

**Caveat (as of v1.14.x):** plugin `tool.execute.before` / `tool.execute.after` hooks **do not** fire on MCP tool calls. Plan around this if you rely on plugin-based interception.

## CLI Commands

```bash
# Add a server interactively
opencode mcp add

# List configured servers + connection status
opencode mcp list           # alias: opencode mcp ls

# Authenticate / sign out
opencode mcp auth <name>
opencode mcp logout <name>

# Debug OAuth issues
opencode mcp debug <name>
```

## Field Differences vs Other Agents

| Concept | Claude Code (`mcpServers`) | Codex (`mcp_servers`) | OpenCode (`mcp`) |
|---------|----------------------------|------------------------|------------------|
| Top-level key | `mcpServers` | `mcp_servers` | `mcp` |
| Format | JSON | TOML | JSON / JSONC |
| Local command | `command` (string) + `args` (array) | `command` (string) + `args` (array) | `command` (single array, command + args together) |
| Env vars | `env` | `env` | `environment` |
| Enable/disable | (omit to remove) | `enabled = true/false` | `enabled: true/false` |
| Remote type | `type: "http"` or `"sse"` | `url` (auto-detected) | `type: "remote"` |
| Local type | `type: "stdio"` | (default for command) | `type: "local"` |
| Bearer token env | `headers.Authorization` | `bearer_token_env_var` | `headers.Authorization` |
| OAuth flag | (handled by `/mcp`) | `mcp_oauth_callback_port` | `oauth: true` per server |

## Variable Substitution

Inside any string value, OpenCode supports:
- `{env:VAR_NAME}` — read env var
- `{file:./path}` — inline file contents

## Full Multi-Server Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "postgres": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-postgres"],
      "environment": {
        "DATABASE_URL": "{env:DATABASE_URL}"
      },
      "enabled": true,
      "timeout": 10000
    },
    "github": {
      "type": "remote",
      "url": "https://api.githubcopilot.com/mcp/",
      "oauth": true,
      "enabled": true
    },
    "stripe": {
      "type": "remote",
      "url": "https://mcp.stripe.com",
      "headers": {
        "Authorization": "Bearer {env:STRIPE_API_KEY}"
      },
      "enabled": false
    }
  },
  "permission": {
    "github_*": "allow",
    "stripe_*": "ask"
  }
}
```

## Sources

- https://opencode.ai/docs/mcp-servers/
- https://opencode.ai/docs/cli/
- https://opencode.ai/docs/config/
- https://opencode.ai/docs/permissions/
