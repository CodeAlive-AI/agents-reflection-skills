# MCP Server Search & Verification

## Contents

- [Search Workflow](#search-workflow)
- [Deployment Options](#deployment-options)
- [Known Official Vendor Servers](#known-official-vendor-servers)
- [MCP Reference Servers](#mcp-reference-servers)
- [User Choice Template](#user-choice-template)
- [Collecting Configuration](#collecting-configuration)

## Search Workflow

**ALWAYS search for official vendor source FIRST, then fallback to MCP Registry.**

### Step 1: Find Official Vendor Source

Use WebSearch:
```
"[service-name] MCP server official"
"[service-name] Model Context Protocol GitHub"
site:github.com [vendor-name] mcp-server
```

**Verify it's official:**
- GitHub org matches vendor name (e.g., `github/github-mcp-server`)
- Links from vendor's official website
- Mentioned in vendor's official docs

### Step 2: Fetch Installation Details

Use WebFetch on the official repo README to get:
- Available deployment options (Remote, Local, Docker)
- Vendor's recommended approach
- Required environment variables
- Authentication requirements

### Step 3: Fallback to MCP Registry

Only if no official source found:
```
https://registry.modelcontextprotocol.io/v0.1/servers?search=<query>&limit=20
```

**Response fields:**
- `server.name` - Server identifier
- `server.description` - What it does
- `server.repository.url` - Source code
- `server.remotes[].url` - Remote endpoint
- `server.packages[].identifier` - npm package name
- `server.packages[].environmentVariables` - Required config

## Deployment Options

### Remote (HTTP/SSE)
```bash
claude mcp add --transport http <name> <url>
```
**Pros:** No local setup, always updated, vendor-managed
**Cons:** Requires internet
**Best for:** Most users, production

### Local (npm/Stdio)
```bash
claude mcp add --transport stdio <name> -- npx -y @vendor/mcp-server
```
**Pros:** Works offline, full control
**Cons:** Requires Node.js, manual updates
**Best for:** Offline use, development

### Docker
```bash
claude mcp add --transport stdio <name> -- docker run -i --rm vendor/mcp-server
```
**Pros:** Isolated, reproducible
**Cons:** Requires Docker
**Best for:** CI/CD, isolation requirements

## Known Official Vendor Servers

### Developer Tools & Platforms

| Service | Official Repo | Remote URL | Local Package |
|---------|---------------|------------|---------------|
| GitHub | `github/github-mcp-server` | `https://api.githubcopilot.com/mcp/` | `@github/mcp-server` |
| GitLab | `gitlab.com` (docs) | `https://gitlab.com/-/mcp` | - |
| Atlassian | `atlassian/atlassian-mcp-server` | `https://mcp.atlassian.com/v1/mcp` | - |
| Linear | `linear.app` (docs) | `https://mcp.linear.app/sse` | - |
| JetBrains | JetBrains official | Via IDE integration | - |
| Vercel | `vercel` (in MCP registry) | - | `@vercel/mcp` |
| Heroku | `heroku/heroku-mcp-server` | - | `@heroku/mcp` |

### Cloud & Infrastructure

| Service | Official Repo | Remote URL | Local Package |
|---------|---------------|------------|---------------|
| Cloudflare | `cloudflare/mcp-server-cloudflare` | Multiple remote servers | `@cloudflare/mcp-server` |
| AWS | `awslabs/mcp` | - | AWS MCP servers |
| Google Cloud Run | `GoogleCloudPlatform/cloud-run-mcp` | - | - |
| Microsoft Azure | `microsoft/mcp` | - | Azure MCP Server |

### Databases

| Service | Official Repo | Remote URL | Local Package |
|---------|---------------|------------|---------------|
| MongoDB | `mongodb-js/mongodb-mcp-server` | - | `@mongodb-js/mongodb-mcp-server` |
| Redis | `redis/mcp-redis` | - | `@redis/mcp` |
| Supabase | `supabase-community/supabase-mcp` | - | `@supabase/mcp` |
| Neon | `neondatabase/mcp-server-neon` | - | `@neondatabase/mcp-server-neon` |

### Productivity & Communication

| Service | Official Repo | Remote URL | Local Package |
|---------|---------------|------------|---------------|
| Notion | `makenotion/notion-mcp-server` | `https://mcp.notion.com/mcp` | - |
| Slack | `zencoderai/slack-mcp-server` | - | `@modelcontextprotocol/server-slack` |
| HubSpot | `developer.hubspot.com` | `https://mcp.hubspot.com/anthropic` | - |
| Monday.com | `mondaycom/mcp` | - | `@mondaycom/mcp` |
| Asana | Asana official | `https://mcp.asana.com/sse` | - |

### Observability & Monitoring

| Service | Official Repo | Remote URL | Local Package |
|---------|---------------|------------|---------------|
| Sentry | Sentry official | `https://mcp.sentry.dev/mcp` | - |
| Datadog | `Datadog-Official/Datadog-MCP` | - | Datadog MCP |
| Grafana | `grafana/mcp-grafana` | - | `@grafana/mcp-grafana` |

### Code Intelligence

| Service | Official Repo | Remote URL | Local Package |
|---------|---------------|------------|---------------|
| CodeAlive | `CodeAlive-AI/codealive-mcp` | `https://mcp.codealive.ai/api` | `codealive-mcp` (Python) |

### Other Services

| Service | Official Repo | Remote URL | Local Package |
|---------|---------------|------------|---------------|
| Twilio | `twilio-labs/mcp` | - | Twilio MCP |
| Firebase | `firebase/firebase-tools` | - | Firebase MCP |
| Auth0 | `auth0/auth0-mcp-server` | - | `@auth0/mcp` |

## MCP Reference Servers

From Anthropic/MCP team:

| Server | Package | Description |
|--------|---------|-------------|
| Filesystem | `@modelcontextprotocol/server-filesystem` | File operations |
| Git | `@modelcontextprotocol/server-git` | Git repository access |
| Memory | `@modelcontextprotocol/server-memory` | Knowledge graph storage |
| SQLite | `@modelcontextprotocol/server-sqlite` | SQLite database access |
| Fetch | `@modelcontextprotocol/server-fetch` | Web content fetching |
| Time | `@modelcontextprotocol/server-time` | Time and timezone conversion |
| Sequential Thinking | `@modelcontextprotocol/server-sequentialthinking` | Problem-solving workflows |

## User Choice Template

When presenting options, use `AskUserQuestion` with this format:

```
Found [Service] MCP Server (Official ✓)

Available deployment options:

1. **Remote (Recommended)** ⭐
   No setup required, always up-to-date
   → claude mcp add --transport http [name] [url]

2. **Local (npm)**
   Works offline, requires Node.js
   → claude mcp add --transport stdio [name] -- npx -y @package

3. **Docker**
   Isolated environment, requires Docker
   → claude mcp add --transport stdio [name] -- docker run -i image

Which would you like to install?
```

Mark vendor's recommended option (or Remote if not specified) with ⭐.

## Collecting Configuration

**IMPORTANT:** Check if server requires configuration before installing. Use `AskUserQuestion`:

```
This MCP server requires configuration:

**Required:**
- API_KEY: Your [Service] API key (get it from [url])
- WORKSPACE_ID: Your workspace identifier

**Optional:**
- CUSTOM_URL: Custom API endpoint (default: https://api.service.com)

Please provide the required values.
```

Common patterns:
- **API Keys**: Most services require authentication
- **OAuth**: GitHub, Atlassian - will prompt in browser
- **Database URLs**: Connection strings like `postgresql://user:pass@host:5432/db`
- **Workspace IDs**: Slack, Notion, Atlassian often need workspace identifiers

Never install with placeholder values.
