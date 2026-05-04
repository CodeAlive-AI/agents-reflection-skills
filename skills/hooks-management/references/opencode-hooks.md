# OpenCode Hooks Reference

Hook/lifecycle event support in [anomalyco/opencode](https://github.com/anomalyco/opencode) (v1.14.x).

OpenCode does **not** have a config-based shell hooks system like Claude Code. Instead, hooks are TypeScript/JavaScript **plugins** that subscribe to lifecycle events and can intercept/block tool calls.

## Contents

- [Architecture](#architecture)
- [Plugin Locations](#plugin-locations)
- [Plugin Structure](#plugin-structure)
- [Hook Events](#hook-events)
- [Tool Interception (`tool.execute.before` / `after`)](#tool-interception-toolexecutebefore--after)
- [Common Patterns](#common-patterns)
- [npm Plugins](#npm-plugins)
- [Limitations](#limitations)
- [Comparison with Claude Code](#comparison-with-claude-code)

## Architecture

| Aspect | Detail |
|--------|--------|
| Language | TypeScript or JavaScript |
| Runtime | Bun (bundled with OpenCode) |
| SDK package | `@opencode-ai/plugin` (npm) |
| Loading | Auto-discovery from plugin directories + npm packages listed in `opencode.json` |
| Persistence | Plugins run inside the OpenCode process — full SDK access |

Install the SDK locally for type completion:

```bash
npm i -D @opencode-ai/plugin
# or
bun add -d @opencode-ai/plugin
```

## Plugin Locations

| Scope | Path |
|-------|------|
| Project | `<project>/.opencode/plugins/` (or `.opencode/plugin/`) |
| Global | `~/.config/opencode/plugins/` |
| npm | Listed in `opencode.json` under `plugin` |

Files: `.ts`, `.js`, `.mjs`. Each file's default export is loaded; named exports starting with `default` are also picked up.

For project-local plugins that need npm packages, add a `package.json` in `.opencode/`. OpenCode runs `bun install` at startup. Cached node_modules live in `~/.cache/opencode/node_modules/`.

## Plugin Structure

```typescript
// .opencode/plugins/my-plugin.ts
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree, app }) => {
  return {
    // Tool lifecycle hooks (cannot block MCP calls in v1.14.x)
    tool: {
      execute: {
        before: async (input, output) => {
          if (input.tool === "read" && output.args.filePath?.includes(".env")) {
            throw new Error("Reading .env files is forbidden")
          }
        },
        after: async (input, output) => {
          if (input.tool === "edit" || input.tool === "write") {
            await $`prettier --write ${output.args.filePath}`.quiet()
          }
        },
      },
    },

    // Generic event subscription
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        client.app.log({ level: "info", message: "Session idle" })
      }
    },
  }
}

export default MyPlugin
```

### Plugin context (`PluginInput`)

| Field | Description |
|-------|-------------|
| `project` | Project metadata (root, name) |
| `client` | OpenCode SDK client (`createOpencodeClient` instance) |
| `$` | Bun shell helper (`@bun/shell`-style) |
| `directory` | CWD where OpenCode was invoked |
| `worktree` | Git worktree root |
| `app` | App-level helpers (logging, etc.) |

## Hook Events

OpenCode's plugin hooks cover **25+ lifecycle events** grouped by domain:

### Tool

- `tool.execute.before` — fires before any tool call (except MCP, see Limitations)
- `tool.execute.after` — fires after tool completes

### Session

- `session.created`
- `session.updated`
- `session.idle` — turn complete
- `session.compacted`
- `session.deleted`
- `session.diff`
- `session.error`
- `session.status`

### Message

- `message.part.updated`
- `message.part.removed`
- `message.updated`
- `message.removed`

### File

- `file.edited`
- `file.watcher.updated`

### Permission

- `permission.asked`
- `permission.replied`

### Command / Todo / LSP / TUI / Server

- `command.executed`
- `todo.updated`
- `lsp.client.diagnostics`
- `lsp.updated`
- `tui.prompt.append`
- `tui.command.execute`
- `tui.toast.show`
- `server.connected`
- `installation.updated`
- `shell.env`

### Experimental

- `experimental.session.compacting` — inject context or rewrite prompt during compaction

## Tool Interception (`tool.execute.before` / `after`)

The closest analogue to Claude Code's `PreToolUse` is `tool.execute.before`. **Throwing inside `before` blocks the tool call.**

```typescript
tool: {
  execute: {
    before: async (input, output) => {
      // input.tool — tool name string
      // output.args — tool arguments (may be mutated to modify input)

      // Block .env reads
      if (input.tool === "read" && output.args.filePath?.includes(".env")) {
        throw new Error("Reading .env is forbidden")
      }

      // Block destructive bash
      if (input.tool === "bash" && /rm\s+-rf|git\s+push.*--force/.test(output.args.command || "")) {
        throw new Error("Destructive command blocked by hook")
      }

      // Modify args before execution
      if (input.tool === "bash") {
        output.args.command = output.args.command.replace(/cd /, "cd ./")
      }
    },
  },
}
```

### `apply_patch` quirks

For `apply_patch`, the file path lives inside `output.args.patchText` as a marker line, not in `output.args.filePath`. Markers include:

- `*** Add File: <path>`
- `*** Update File: <path>`
- `*** Move to: <path>`
- `*** Delete File: <path>`

Paths are relative to the project root.

## Common Patterns

### Block .env access (file protection)

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export default (async () => ({
  tool: {
    execute: {
      before: async (input, output) => {
        const path = output.args.filePath ?? ""
        if (/\.env(\.|$)|secrets|credentials|\.pem$|\.key$/i.test(path)) {
          throw new Error(`Protected file: ${path}`)
        }
      },
    },
  },
})) satisfies Plugin
```

Save as `.opencode/plugins/env-protection.ts`. Loaded automatically.

### Auto-format on edit

```typescript
export default (async ({ $ }) => ({
  tool: {
    execute: {
      after: async (input, output) => {
        if (input.tool !== "edit" && input.tool !== "write") return
        const file = output.args.filePath
        if (!file) return
        if (/\.(ts|tsx|js|jsx)$/.test(file)) await $`prettier --write ${file}`.quiet()
        else if (file.endsWith(".py")) await $`black --quiet ${file}`.quiet()
        else if (file.endsWith(".go")) await $`gofmt -w ${file}`.quiet()
      },
    },
  },
})) satisfies Plugin
```

### Session-end notification

```typescript
export default (async ({ $ }) => ({
  event: async ({ event }) => {
    if (event.type === "session.idle") {
      // macOS
      await $`osascript -e 'display notification "Session idle" with title "OpenCode"'`.quiet()
    }
  },
})) satisfies Plugin
```

### Log all bash commands

```typescript
export default (async () => ({
  tool: {
    execute: {
      before: async (input, output) => {
        if (input.tool !== "bash") return
        const fs = await import("node:fs/promises")
        await fs.appendFile(
          `${process.env.HOME}/.config/opencode/command-log.txt`,
          `[${new Date().toISOString()}] ${output.args.command}\n`,
        )
      },
    },
  },
})) satisfies Plugin
```

## npm Plugins

Distribute via npm with the `opencode-plugin` keyword. Register in `opencode.json`:

```json
{
  "plugin": [
    "opencode-helicone-session",
    "opencode-wakatime",
    "@my-org/custom-plugin"
  ]
}
```

OpenCode runs `bun install` at startup, caches under `~/.cache/opencode/node_modules/`.

`package.json` for an authored plugin:

```json
{
  "name": "opencode-my-plugin",
  "version": "1.0.0",
  "main": "dist/index.js",
  "keywords": ["opencode-plugin"],
  "peerDependencies": { "@opencode-ai/plugin": "^1.0.0" }
}
```

## Limitations

| Limitation | Impact |
|------------|--------|
| **MCP tool calls do NOT trigger `tool.execute.before/after`** in v1.14.x | Plugin-based interception of MCP tools is impossible — use the `permission` block instead |
| No "agent-as-hook" pattern | Cannot spawn an analyzer subagent before tool use the way Claude Code's `"type": "agent"` hooks can |
| No `Notification` equivalent for OS-level notifications without manual shelling | Use `$` from the plugin context to call `osascript` / `notify-send` yourself |
| No session-start hook that blocks startup | `session.created` fires after init |
| Plugin failures fail loudly | Throwing in `before` blocks the tool; throwing elsewhere may surface as a session error |

## Comparison with Claude Code

| Capability | Claude Code | OpenCode |
|-----------|-------------|----------|
| Pre-tool blocking | `PreToolUse` hook with exit 2 / JSON `permissionDecision: "deny"` | `tool.execute.before` plugin throws |
| Pre-tool ask user | `PreToolUse` JSON `permissionDecision: "ask"` | Set `permission` rule to `"ask"`; plugin can mutate args before |
| Post-tool side effects | `PostToolUse` shell command | `tool.execute.after` plugin |
| Notifications | `Notification` event + shell hook | Subscribe to `session.idle` etc. in plugin, shell out via `$` |
| Session lifecycle | `SessionStart`, `Stop`, `SubagentStop` | `session.created`, `session.idle`, `session.deleted` |
| Block on MCP tool | `mcp__server__.*` matcher | **Not supported** in v1.14.x — use `permission` |
| Modify tool input | `updatedInput` in JSON output | Mutate `output.args` in `tool.execute.before` |
| Execution model | Shell command (stdin/stdout JSON) | Async TypeScript function with full SDK |
| Distribution | Hooks live in `settings.json` or plugins | npm packages or local TS files |

### Migration map

| Claude Code hook | OpenCode equivalent |
|------------------|---------------------|
| `PreToolUse` Bash exit 2 | `tool.execute.before` throws |
| `PreToolUse` permissionDecision `"ask"` | `permission` rule `"ask"` |
| `PreToolUse` permissionDecision `"deny"` | `permission` rule `"deny"` (or throw) |
| `PostToolUse` formatter | `tool.execute.after` runs `$`prettier ...`` |
| `Notification` osascript | `event` listener for `session.idle` |
| `SessionStart` env loader | `session.created` event |
| `Stop` cleanup | `session.idle` (turn end) or `session.deleted` |
| File protection on `.env` | `tool.execute.before` rejects on path match |

## Sources

- https://opencode.ai/docs/plugins/
- https://opencode.ai/docs/tools/
- https://www.npmjs.com/package/@opencode-ai/plugin
- https://github.com/anomalyco/opencode/issues/2319 (MCP-hook caveat)
- https://dev.to/einarcesar/does-opencode-support-hooks-a-complete-guide-to-extensibility-k3p
- https://lushbinary.com/blog/opencode-plugin-development-custom-tools-hooks-guide/
