# Claude Code Settings Reference

Complete reference for all Claude Code settings options.

## Table of Contents

1. [Available Settings](#available-settings)
2. [Permission Settings](#permission-settings)
3. [Sandbox Settings](#sandbox-settings)
4. [Attribution Settings](#attribution-settings)
5. [Environment Variables](#environment-variables)

---

## Available Settings

| Key | Description | Example |
|-----|-------------|---------|
| `apiKeyHelper` | Script to generate auth value (executed in /bin/sh) | `/bin/generate_temp_api_key.sh` |
| `cleanupPeriodDays` | Days before inactive sessions are deleted (default: 30, 0 = immediate) | `20` |
| `companyAnnouncements` | Announcements displayed at startup (cycled randomly) | `["Welcome to Acme Corp!"]` |
| `env` | Environment variables for every session | `{"FOO": "bar"}` |
| `attribution` | Customize git commit/PR attribution | `{"commit": "...", "pr": ""}` |
| `permissions` | Permission rules (see Permission Settings) | |
| `hooks` | Custom commands before/after tool executions | `{"PreToolUse": {...}}` |
| `disableAllHooks` | Disable all hooks | `true` |
| `model` | Override default model | `"claude-sonnet-4-5-20250929"` |
| `statusLine` | Custom status line configuration | `{"type": "command", "command": "..."}` |
| `fileSuggestion` | Custom @ file autocomplete script | `{"type": "command", "command": "..."}` |
| `respectGitignore` | Whether @ picker respects .gitignore (default: true) | `false` |
| `outputStyle` | Adjust system prompt style | `"Explanatory"` |
| `forceLoginMethod` | Restrict login to `claudeai` or `console` | `"claudeai"` |
| `forceLoginOrgUUID` | Auto-select organization UUID during login | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` |
| `enableAllProjectMcpServers` | Auto-approve all project MCP servers | `true` |
| `enabledMcpjsonServers` | Specific MCP servers to approve | `["memory", "github"]` |
| `disabledMcpjsonServers` | Specific MCP servers to reject | `["filesystem"]` |
| `alwaysThinkingEnabled` | Enable extended thinking by default | `true` |
| `plansDirectory` | Where plan files are stored (default: `~/.claude/plans`) | `"./plans"` |
| `showTurnDuration` | Show turn duration messages | `true` |
| `language` | Claude's preferred response language | `"japanese"` |
| `autoUpdatesChannel` | Update channel: `"stable"` or `"latest"` (default) | `"stable"` |

---

## Permission Settings

| Key | Description | Example |
|-----|-------------|---------|
| `allow` | Rules to allow tool use (Bash uses prefix matching) | `["Bash(git diff:*)"]` |
| `ask` | Rules requiring confirmation | `["Bash(git push:*)"]` |
| `deny` | Rules to deny tool use | `["WebFetch", "Read(./.env)"]` |
| `additionalDirectories` | Extra working directories Claude can access | `["../docs/"]` |
| `defaultMode` | Default permission mode | `"acceptEdits"` |
| `disableBypassPermissionsMode` | Disable `--dangerously-skip-permissions` | `"disable"` |

### Permission Rule Syntax

```
Tool(pattern)
```

Examples:
- `Bash(npm run:*)` - Allow any npm run command
- `Bash(git:*)` - Allow any git command
- `Read(./.env)` - Match .env file
- `Read(./.env.*)` - Match .env.local, .env.production, etc.
- `Read(./secrets/**)` - Match all files under secrets/

---

## Sandbox Settings

| Key | Description | Example |
|-----|-------------|---------|
| `enabled` | Enable bash sandboxing (macOS/Linux only) | `true` |
| `autoAllowBashIfSandboxed` | Auto-approve bash when sandboxed (default: true) | `true` |
| `excludedCommands` | Commands to run outside sandbox | `["git", "docker"]` |
| `allowUnsandboxedCommands` | Allow `dangerouslyDisableSandbox` parameter (default: true) | `false` |
| `network.allowUnixSockets` | Unix socket paths accessible in sandbox | `["~/.ssh/agent-socket"]` |
| `network.allowLocalBinding` | Allow binding to localhost (macOS only) | `true` |
| `network.httpProxyPort` | HTTP proxy port for custom proxy | `8080` |
| `network.socksProxyPort` | SOCKS5 proxy port for custom proxy | `8081` |
| `enableWeakerNestedSandbox` | Enable weaker sandbox for Docker (Linux, reduces security) | `true` |

### Sandbox Example

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "network": {
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    }
  }
}
```

---

## Attribution Settings

| Key | Description |
|-----|-------------|
| `commit` | Attribution for git commits (including trailers). Empty string hides it |
| `pr` | Attribution for PR descriptions. Empty string hides it |

### Default Attribution

**Commit:**
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**PR:**
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Environment Variables

### Core Configuration

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API key for Claude SDK |
| `ANTHROPIC_AUTH_TOKEN` | Custom Authorization header value |
| `ANTHROPIC_MODEL` | Model setting to use |
| `ANTHROPIC_CUSTOM_HEADERS` | Custom headers (Name: Value format) |

### Model Overrides

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Override Haiku model |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Override Opus model |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Override Sonnet model |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents |

### Behavior Settings

| Variable | Purpose |
|----------|---------|
| `BASH_DEFAULT_TIMEOUT_MS` | Default timeout for bash commands |
| `BASH_MAX_TIMEOUT_MS` | Maximum timeout for bash commands |
| `BASH_MAX_OUTPUT_LENGTH` | Max characters before truncation |
| `MAX_THINKING_TOKENS` | Extended thinking budget (0 to disable) |
| `MAX_MCP_OUTPUT_TOKENS` | Max tokens in MCP responses (default: 25000) |

### Disable Features

| Variable | Purpose |
|----------|---------|
| `DISABLE_AUTOUPDATER` | Disable automatic updates |
| `DISABLE_TELEMETRY` | Opt out of Statsig telemetry |
| `DISABLE_ERROR_REPORTING` | Opt out of Sentry error reporting |
| `DISABLE_COST_WARNINGS` | Disable cost warning messages |
| `DISABLE_PROMPT_CACHING` | Disable prompt caching for all models |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Disable autoupdater, bug command, error reporting, and telemetry |

### Provider-Specific

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CODE_USE_BEDROCK` | Use Amazon Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI |
| `CLAUDE_CODE_USE_FOUNDRY` | Use Microsoft Foundry |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH` | Skip AWS auth (for LLM gateways) |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH` | Skip Google auth (for LLM gateways) |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH` | Skip Azure auth (for LLM gateways) |

### Directories and Paths

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CONFIG_DIR` | Custom config/data directory |
| `CLAUDE_CODE_TMPDIR` | Override temp directory |
| `CLAUDE_CODE_SHELL` | Override shell detection |

### Proxy Settings

| Variable | Purpose |
|----------|---------|
| `HTTP_PROXY` | HTTP proxy server |
| `HTTPS_PROXY` | HTTPS proxy server |
| `NO_PROXY` | Domains/IPs to bypass proxy |

---

## Other Configuration Files

| Feature | User Location | Project Location |
|---------|---------------|------------------|
| **MCP servers** | `~/.claude.json` | `.mcp.json` |
| **Subagents** | `~/.claude/agents/` | `.claude/agents/` |
| **CLAUDE.md** | `~/.claude/CLAUDE.md` | `CLAUDE.md` or `.claude/CLAUDE.md` |
| **Local CLAUDE.md** | — | `CLAUDE.local.md` |
