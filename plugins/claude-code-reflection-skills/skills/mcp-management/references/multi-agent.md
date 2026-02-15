# Multi-Agent MCP Installation

## Contents

- [Overview](#overview)
- [Source Types](#source-types)
- [Agent Configuration Reference](#agent-configuration-reference)
- [Config Format Examples](#config-format-examples)
- [Agent-Specific Transformations](#agent-specific-transformations)
- [Manual Multi-Agent Setup](#manual-multi-agent-setup)

## Overview

[add-mcp](https://github.com/neondatabase/add-mcp) is a CLI tool that installs MCP servers into multiple coding agents with a single command. It handles agent detection, config format differences, and agent-specific transformations automatically.

```bash
npx add-mcp <source> [options]
```

**Source types detected automatically:**
- URLs (`https://...`) → Remote HTTP/SSE server
- npm packages (`@org/package` or `package-name`) → Stdio via `npx -y`
- Commands with spaces (`npx -y @org/server --flag`) → Stdio with custom args

**Name inference:** Server names are auto-inferred from the source:
- `https://mcp.neon.tech/mcp` → `neon`
- `@modelcontextprotocol/server-postgres` → `postgres`
- `mcp-server-github` → `github`

Use `-n <name>` to override.

## Source Types

### Remote (HTTP/SSE)

```bash
# HTTP (default)
npx add-mcp https://mcp.stripe.com

# SSE (deprecated, use HTTP when possible)
npx add-mcp https://mcp.example.com/sse --transport sse

# With auth headers
npx add-mcp --header "Authorization: Bearer TOKEN" https://api.example.com/mcp
```

### npm Packages

```bash
# Scoped package
npx add-mcp @modelcontextprotocol/server-postgres

# Simple package
npx add-mcp mcp-server-github
```

Installed via `npx -y <package>` as stdio transport.

### Local Commands

```bash
# Custom npx command with args
npx add-mcp "npx -y @org/mcp-server --config /path/to/config"

# Node script
npx add-mcp "node /path/to/server.js --port 3000"

# Python server
npx add-mcp "python -m mcp_server --host localhost"
```

## Agent Configuration Reference

### Claude Code

| Property | Value |
|----------|-------|
| Global config | `~/.claude.json` |
| Project config | `.mcp.json` |
| Config key | `mcpServers` |
| Format | JSON |
| Transports | stdio, http, sse |

### Claude Desktop

| Property | Value |
|----------|-------|
| Global config (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Global config (Windows) | `%APPDATA%/Claude/claude_desktop_config.json` |
| Global config (Linux) | `~/.config/Claude/claude_desktop_config.json` |
| Project config | Not supported (global only) |
| Config key | `mcpServers` |
| Format | JSON |
| Transports | stdio, http, sse |

### Cursor

| Property | Value |
|----------|-------|
| Global config | `~/.cursor/mcp.json` |
| Project config | `.cursor/mcp.json` |
| Config key | `mcpServers` |
| Format | JSON |
| Transports | stdio, http, sse |

**Note:** Remote servers use simplified config (just `url` and optional `headers`, no `type` field).

### VS Code

| Property | Value |
|----------|-------|
| Global config (macOS) | `~/Library/Application Support/Code/User/mcp.json` |
| Global config (Windows) | `%APPDATA%/Code/User/mcp.json` |
| Global config (Linux) | `~/.config/Code/User/mcp.json` |
| Project config | `.vscode/mcp.json` |
| Config key | `servers` |
| Format | JSON |
| Transports | stdio, http, sse |

### Gemini CLI

| Property | Value |
|----------|-------|
| Global config | `~/.gemini/settings.json` |
| Project config | `.gemini/settings.json` |
| Config key | `mcpServers` |
| Format | JSON |
| Transports | stdio, http, sse |

### Codex

| Property | Value |
|----------|-------|
| Global config | `~/.codex/config.toml` |
| Project config | `.codex/config.toml` |
| Config key | `mcp_servers` |
| Format | TOML |
| Transports | stdio, http, sse |

### Goose

| Property | Value |
|----------|-------|
| Global config (macOS/Linux) | `~/.config/goose/config.yaml` |
| Global config (Windows) | `%APPDATA%/Block/goose/config/config.yaml` |
| Project config | Not supported (global only) |
| Config key | `extensions` |
| Format | YAML |
| Transports | stdio, http, sse |

**Transformation:** Uses `uri` instead of `url`, `streamable_http` instead of `http`, `cmd` instead of `command`, `envs` instead of `env`.

### GitHub Copilot CLI

| Property | Value |
|----------|-------|
| Global config | `~/.copilot/mcp-config.json` |
| Project config | `.vscode/mcp.json` (shared with VS Code) |
| Config key (global) | `mcpServers` |
| Config key (project) | `servers` |
| Format | JSON |
| Transports | stdio, http, sse |

**Transformation:** Global config adds `tools: ["*"]` to each server entry.

### OpenCode

| Property | Value |
|----------|-------|
| Global config | `~/.config/opencode/opencode.json` |
| Project config | `opencode.json` |
| Config key | `mcp` |
| Format | JSON |
| Transports | stdio, http, sse |

**Transformation:** Uses `type: "remote"` / `type: "local"`, `command` as array, `environment` instead of `env`.

### Zed

| Property | Value |
|----------|-------|
| Global config (macOS/Windows) | `~/Library/Application Support/Zed/settings.json` |
| Global config (Linux) | `~/.config/zed/settings.json` |
| Project config | `.zed/settings.json` |
| Config key | `context_servers` |
| Format | JSON |
| Transports | stdio, http, sse |

**Transformation:** Adds `source: "custom"` to each entry.

## Config Format Examples

### JSON (most agents)

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"]
    },
    "stripe": {
      "type": "http",
      "url": "https://mcp.stripe.com",
      "headers": {
        "Authorization": "Bearer ${STRIPE_API_KEY}"
      }
    }
  }
}
```

### YAML (Goose)

```yaml
extensions:
  neon:
    name: neon
    type: streamable_http
    uri: https://mcp.neon.tech/mcp
    headers: {}
    enabled: true
    timeout: 300
  postgres:
    name: postgres
    cmd: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-postgres"
    type: stdio
    envs: {}
    enabled: true
    timeout: 300
```

### TOML (Codex)

```toml
[mcp_servers.postgres]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-postgres"]

[mcp_servers.stripe]
type = "http"
url = "https://mcp.stripe.com"

[mcp_servers.stripe.headers]
Authorization = "Bearer ${STRIPE_API_KEY}"
```

## Agent-Specific Transformations

When installing manually (without add-mcp), be aware of these config variations:

| Agent | Config Key | URL Field | Command Field | Env Field | Extra Fields |
|-------|-----------|-----------|--------------|-----------|--------------|
| Claude Code | `mcpServers` | `url` | `command` | `env` | - |
| Claude Desktop | `mcpServers` | `url` | `command` | `env` | - |
| Cursor | `mcpServers` | `url` | `command` | `env` | No `type` for remote |
| VS Code | `servers` | `url` | `command` | `env` | - |
| Gemini CLI | `mcpServers` | `url` | `command` | `env` | - |
| Codex | `mcp_servers` | `url` | `command` | `env` | - |
| Goose | `extensions` | `uri` | `cmd` | `envs` | `name`, `enabled`, `timeout` |
| GitHub Copilot CLI | `mcpServers` | `url` | `command` | `env` | `tools: ["*"]` (global) |
| OpenCode | `mcp` | `url` | `command` (array) | `environment` | `type: "remote"/"local"` |
| Zed | `context_servers` | `url` | `command` | `env` | `source: "custom"` |

## Manual Multi-Agent Setup

If you need to install to agents without using `npx add-mcp`, edit each agent's config file directly. The key differences to handle:

1. **Find the config file** from the agent reference table above
2. **Use the correct config key** (`mcpServers`, `servers`, `extensions`, etc.)
3. **Apply transformations** for agents that use different field names
4. **Use the correct format** (JSON for most, YAML for Goose, TOML for Codex)

For team projects, prefer project-level configs (`.mcp.json`, `.cursor/mcp.json`, `.vscode/mcp.json`) so all team members get the same MCP servers. Commit these files to version control.
