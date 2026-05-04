# Claude Code Settings Reference

Complete reference for all Claude Code settings options. Updated for Claude Code 2.1.x (April 2026).

## Table of Contents

1. [Available Settings](#available-settings)
2. [Permission Settings](#permission-settings)
3. [Sandbox Settings](#sandbox-settings)
4. [Attribution Settings](#attribution-settings)
5. [Plugin Settings](#plugin-settings)
6. [Worktree Settings](#worktree-settings)
7. [Environment Variables](#environment-variables)

---

## Available Settings

| Key | Description | Example |
|-----|-------------|---------|
| `apiKeyHelper` | Script to generate auth value (executed in /bin/sh) | `/bin/generate_temp_api_key.sh` |
| `cleanupPeriodDays` | Days before inactive sessions/tasks/shell-snapshots/backups deleted (default: 30, 0 = immediate). 2026: now also covers `~/.claude/tasks/`, `~/.claude/shell-snapshots/`, `~/.claude/backups/`. | `20` |
| `companyAnnouncements` | Announcements displayed at startup (cycled randomly) | `["Welcome to Acme Corp!"]` |
| `env` | Environment variables for every session | `{"FOO": "bar"}` |
| `attribution` | Customize git commit/PR attribution | `{"commit": "...", "pr": ""}` |
| `permissions` | Permission rules (see Permission Settings) | |
| `hooks` | Custom commands before/after tool executions | `{"PreToolUse": {...}}` |
| `disableAllHooks` | Disable all hooks | `true` |
| `model` | Override default model | `"claude-opus-4-7"` |
| `effort` | Default effort level (low/medium/high/xhigh/max). API/Bedrock/Vertex/Foundry/Team/Enterprise default to `high` since 2026. | `"high"` |
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
| `disableSkillShellExecution` | **(2026)** Disable inline `` !`shell` `` execution in skills, custom slash commands, and plugin commands. Useful in managed settings. | `true` |
| `prUrlTemplate` | **(2026)** Custom code-review URL template for footer PR badge instead of github.com | `"https://gitlab.example.com/{repo}/-/merge_requests/{number}"` |
| `disableDeepLinkRegistration` | **(2026)** Prevent `claude-cli://` protocol handler registration | `true` |
| `autoScrollEnabled` | **(2026)** Disable conversation auto-scroll in fullscreen | `false` |
| `showClearContextOnPlanAccept` | **(2026)** Control plan-mode behavior on accept | `true` |
| `wslInheritsWindowsSettings` | **(2026)** WSL on Windows inherits Windows-side managed settings via this policy key | `true` |
| `enableAwaySummary` | **(2026)** Session recap when returning (also `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0` env to opt out) | `true` |
| `tui` | UI rendering mode (alt-screen flicker-free vs scrollback). Run `/tui fullscreen` to switch live. | `"fullscreen"` |
| `worktree` | Worktree behavior config object (see [Worktree Settings](#worktree-settings)) | `{"sparsePaths": ["src/"]}` |
| `pluginConfigs` | Per-plugin user-config values (`pluginConfigs[<plugin-id>].options`) | |
| `enabledPlugins` | List of plugins enabled in this scope | |
| `extraKnownMarketplaces` | Marketplaces required by the project; auto-installed on trust | |
| `blockedMarketplaces` | **(2026)** Managed-only. Blocks marketplaces by `hostPattern`/`pathPattern` | |
| `strictKnownMarketplaces` | **(2026)** Managed-only. Enforce only `extraKnownMarketplaces` | `true` |
| `allowedChannelPlugins` | **(2026)** Managed-only. Channel plugin allowlist (Slack/Telegram/Discord) | |
| `forceRemoteSettingsRefresh` | **(2026)** Managed-only. Fail-closed if remote settings can't be refreshed | `true` |

---

## Permission Settings

| Key | Description | Example |
|-----|-------------|---------|
| `allow` | Rules to allow tool use (Bash uses prefix matching) | `["Bash(git diff:*)"]` |
| `ask` | Rules requiring confirmation | `["Bash(git push:*)"]` |
| `deny` | Rules to deny tool use | `["WebFetch", "Read(./.env)"]` |
| `additionalDirectories` | Extra working directories Claude can access. **(2026)** Now applies mid-session. | `["../docs/"]` |
| `defaultMode` | Default permission mode (`default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`) | `"acceptEdits"` |
| `disableBypassPermissionsMode` | Disable `--dangerously-skip-permissions` | `"disable"` |
| `autoMode.allow` | **(2026)** Custom rules added to Auto-mode classifier allowlist (use `$defaults` to extend built-ins) | |
| `autoMode.soft_deny` | **(2026)** Custom rules for Auto-mode soft-deny | |
| `autoMode.environment` | **(2026)** Environment context flags for the classifier | |

### Permission Modes (2026)

| Mode | Behavior |
|------|----------|
| `default` | Standard prompts; reads always allowed |
| `acceptEdits` | Auto-approves file edits + benign filesystem Bash (`mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`) |
| `plan` | Read-only exploration |
| `auto` | **NEW (March 2026)** — Sonnet/Opus classifier auto-approves safe ops, denies dangerous (mass deletion, exfiltration, malware). Triggers `PermissionDenied` hook. Requires Team/Enterprise/Max plan + Sonnet 4.6 / Opus 4.6+. |
| `dontAsk` | Auto-deny anything not explicitly allowed (CI/CD lockdown) |
| `bypassPermissions` | All checks off. **`.git/`, `.claude/`, `.claude/skills/` remain protected (since v2.1.78–v2.1.81).** |

Cycle live with **Shift+Tab** (default → acceptEdits → plan).

### Protected Paths (2026)

Even with `bypassPermissions`, writes to `.git/`, `.claude/`, `.claude/skills/`, and `.husky/` (in `acceptEdits` mode) trigger an approval prompt.

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
| `network.deniedDomains` | **(2026)** Block specific domains even when broader `allowedDomains` permits them | `["analytics.example.com"]` |
| `network.allowMachLookup` | **(2026)** macOS-specific Mach socket lookup | `true` |
| `enableWeakerNestedSandbox` | Enable weaker sandbox for Docker (Linux, reduces security) | `true` |
| `failIfUnavailable` | **(2026)** Exit with error when sandbox cannot start (CI safety) | `true` |

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

   Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

**PR:**
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Plugin Settings

Plugin-related fields in `settings.json`:

| Key | Description |
|-----|-------------|
| `enabledPlugins` | Plugins enabled in this scope |
| `pluginConfigs` | Per-plugin user-config values; non-sensitive values stored here, sensitive ones in keychain |
| `extraKnownMarketplaces` | Marketplaces required by the project; auto-installed when the user trusts the repo folder |
| `blockedMarketplaces` | (managed) Block marketplaces by `hostPattern`/`pathPattern` |
| `strictKnownMarketplaces` | (managed) Restrict to declared marketplaces only |
| `allowedChannelPlugins` | (managed) Channel-plugin allowlist |

Plugins now ship `package.json` and lockfile dependencies that auto-install at enable time. `claude plugin tag` cuts release tags. `/plugin install` on an already-installed plugin resolves missing dependencies.

---

## Worktree Settings

```json
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"],
    "sparsePaths": ["src/", "packages/my-service/"]
  }
}
```

| Field | Description |
|-------|-------------|
| `symlinkDirectories` | Dirs to symlink (not copy) into each worktree |
| `sparsePaths` | **(2026)** `git sparse-checkout` paths for `claude --worktree` in large monorepos |

Subagents declare worktree isolation via frontmatter `isolation: "worktree"`. The `WorktreeCreate`/`WorktreeRemove` hooks fire around lifecycle events and can override the path or block creation.

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
| `DISABLE_UPDATES` | **(2026)** Block ALL update paths including manual `claude update` (stricter than `DISABLE_AUTOUPDATER`) |
| `DISABLE_TELEMETRY` | Opt out of Statsig telemetry |
| `DISABLE_ERROR_REPORTING` | Opt out of Sentry error reporting |
| `DISABLE_COST_WARNINGS` | Disable cost warning messages |
| `DISABLE_PROMPT_CACHING` | Disable prompt caching for all models |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Disable autoupdater, bug command, error reporting, and telemetry |
| `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` | Set to `0` to opt out of session-recap summaries |

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
| `CLAUDE_CODE_HIDE_CWD` | **(2026)** Hide working directory in startup logo |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Load `CLAUDE.md` from `--add-dir` directories |

### New 2026 Environment Variables

| Variable | Purpose |
|----------|---------|
| `CLAUDE_CODE_FORK_SUBAGENT` | Enable forked subagents on external builds |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL` | Enable PowerShell tool (Windows opt-in; manual on macOS/Linux) |
| `CLAUDE_CODE_PERFORCE_MODE` | Hint for Perforce `p4 edit` workflow |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | Strip credentials from subprocess environments; enables PID-namespace isolation on Linux |
| `CLAUDE_CODE_SCRIPT_CAPS` | Limit per-session script invocations |
| `CLAUDE_CODE_NO_FLICKER` | Flicker-free alt-screen rendering |
| `CLAUDE_CODE_CERT_STORE` | `bundled` (use only bundled CAs) — default uses OS store |
| `CLAUDE_CODE_OAUTH_TOKEN` | Pre-set OAuth token (cleared on `/login`) |
| `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` | Keep marketplace cache when `git pull` fails (offline support) |
| `CLAUDE_CODE_USE_MANTLE` | Use Amazon Bedrock powered by Mantle |
| `CLAUDE_CODE_USE_BEDROCK` / `CLAUDE_CODE_USE_VERTEX` / `CLAUDE_CODE_USE_FOUNDRY` | Provider routing |
| `ENABLE_PROMPT_CACHING_1H` | 1-hour prompt cache TTL (API/Bedrock/Vertex/Foundry) |
| `FORCE_PROMPT_CACHING_5M` | Force 5-minute TTL |
| `CLAUDE_STREAM_IDLE_TIMEOUT_MS` | Streaming idle watchdog (default 90_000) |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Raise the skill-listing description character budget (default ≈1% of context, fallback 8000) |
| `OTEL_LOG_RAW_API_BODIES` / `OTEL_LOG_USER_PROMPTS` / `OTEL_LOG_TOOL_DETAILS` / `OTEL_LOG_TOOL_CONTENT` | Telemetry granularity |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME` / `_DESCRIPTION` (etc) | Customize displayed model labels |

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
