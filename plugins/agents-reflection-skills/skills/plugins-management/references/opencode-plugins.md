# OpenCode Plugins Reference

Plugin system for [anomalyco/opencode](https://github.com/anomalyco/opencode) (v1.14.x).

OpenCode plugins are TypeScript/JavaScript modules that extend the agent with custom tools and lifecycle hooks. They are fundamentally different from Claude Code plugins (`.claude-plugin/`):

- **Distribution**: npm packages (or local files), not Anthropic marketplaces
- **Format**: TypeScript modules with default-exported async functions, not `plugin.json` manifests
- **Components**: custom tools, lifecycle hooks, custom slash commands — defined inline in code
- **Loading**: auto-discovered from `.opencode/plugins/` and `~/.config/opencode/plugins/`, plus npm packages listed in `opencode.json`

## Contents

- [Plugin Locations](#plugin-locations)
- [Authoring a Plugin](#authoring-a-plugin)
- [Plugin Manifest (package.json)](#plugin-manifest-packagejson)
- [Plugin Capabilities](#plugin-capabilities)
- [Custom Tools](#custom-tools)
- [Lifecycle Hooks](#lifecycle-hooks)
- [Distribution](#distribution)
- [Installing Plugins](#installing-plugins)
- [Removing Plugins](#removing-plugins)
- [Validating Plugins](#validating-plugins)
- [Comparison with Claude Code Plugins](#comparison-with-claude-code-plugins)

## Plugin Locations

| Scope | Path |
|-------|------|
| Project | `<project>/.opencode/plugins/*.{ts,js}` |
| Global | `~/.config/opencode/plugins/*.{ts,js}` |
| npm | `opencode.json` → `"plugin": ["<package-name>", ...]` |

OpenCode runs `bun install` at startup for npm plugins listed in `opencode.json`. node_modules cache: `~/.cache/opencode/node_modules/`.

For project-local plugins that pull npm dependencies, place a `package.json` in `.opencode/`. OpenCode will install its dependencies via Bun automatically.

## Authoring a Plugin

```typescript
// .opencode/plugins/my-plugin.ts
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({
  project,
  client,
  $,
  directory,
  worktree,
  app,
}) => {
  return {
    tool: {
      execute: {
        before: async (input, output) => {
          // Block, modify, or log tool calls
        },
        after: async (input, output) => {
          // Run side effects after tool completes
        },
      },
    },
    event: async ({ event }) => {
      // Generic event subscription
    },
  }
}

export default MyPlugin
```

### Plugin context

| Field | Type | Description |
|-------|------|-------------|
| `project` | object | Project metadata (root path, name) |
| `client` | OpenCodeClient | SDK client (created via `createOpencodeClient()`) |
| `$` | shell helper | Bun-style shell — `await $`prettier --write ${file}`` |
| `directory` | string | CWD where OpenCode was launched |
| `worktree` | string | Git worktree root |
| `app` | object | App-level helpers (e.g., logging) |

## Plugin Manifest (package.json)

For npm-distributed plugins:

```json
{
  "name": "opencode-my-plugin",
  "version": "1.0.0",
  "description": "Adds X to OpenCode",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "keywords": ["opencode-plugin"],
  "license": "MIT",
  "repository": "https://github.com/me/opencode-my-plugin",
  "peerDependencies": {
    "@opencode-ai/plugin": "^1.0.0"
  },
  "devDependencies": {
    "@opencode-ai/plugin": "^1.14.0",
    "typescript": "^5.5.0"
  }
}
```

**Conventions:**
- Prefix the package name with `opencode-` or scope it under your org
- Always include the `opencode-plugin` keyword for discoverability
- Use `peerDependencies` for `@opencode-ai/plugin` so the host's version is used

## Plugin Capabilities

A single plugin file can expose:

1. **Custom tools** — add new tools the AI can call (with Zod schemas)
2. **Tool interceptors** — `tool.execute.before` / `after`
3. **Event subscribers** — react to ~25 lifecycle events
4. **Custom auth** — wire up new providers
5. **Compaction transforms** — rewrite messages or system prompts during context compaction (`experimental.session.compacting`)

## Custom Tools

Custom tools live in `.opencode/tools/` (project) or `~/.config/opencode/tools/` (global), or are returned from a plugin. The filename becomes the tool name.

```typescript
// .opencode/tools/database.ts
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Query the project database",
  args: {
    query: tool.schema.string().describe("SQL query to execute"),
  },
  async execute(args, ctx) {
    // ctx exposes: agent name, session id, message id, directory, worktree
    return `Executed: ${args.query}`
  },
})
```

Multiple tools per file: export named tools — they get the tool name `<filename>_<exportname>`:

```typescript
export const add = tool({ ... })
export const multiply = tool({ ... })
// → tools "math_add" and "math_multiply" if file is math.ts
```

A custom tool with the same name as a built-in (`bash`, `edit`, etc.) **overrides** the built-in.

## Lifecycle Hooks

See the dedicated reference at `../../hooks-management/references/opencode-hooks.md` for the full event catalog. Quick summary:

- **Tool**: `tool.execute.before`, `tool.execute.after`
- **Session**: `session.created`, `session.idle`, `session.compacted`, `session.deleted`, etc.
- **Message**: `message.updated`, `message.part.updated`, etc.
- **File**: `file.edited`, `file.watcher.updated`
- **Permission**: `permission.asked`, `permission.replied`
- **Other**: `command.executed`, `todo.updated`, `lsp.client.diagnostics`, `tui.toast.show`, `server.connected`

## Distribution

There is **no centralized OpenCode plugin marketplace**. Plugins are distributed via:

- **npm** with the `opencode-plugin` keyword
- **GitHub repositories** users clone or reference
- **Community aggregators** like [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) and [opencode.cafe](https://opencode.cafe)

Notable community plugins (npm):
- `@opencode-ai/plugin` — official SDK (the dependency, not a plugin itself)
- `opencode-helicone-session` — usage tracking
- `opencode-wakatime` — coding-time analytics
- `opencode-antigravity-auth` — Google Antigravity OAuth bridge
- `oh-my-opencode` — comprehensive bundle (agents, hooks, MCPs, skills)

## Installing Plugins

### From npm

Add the package name to `opencode.json` and restart:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "opencode-helicone-session",
    "opencode-wakatime",
    "@my-org/custom-plugin"
  ]
}
```

OpenCode runs `bun install` automatically at next startup. Cached at `~/.cache/opencode/node_modules/`.

### From a local file

Drop the `.ts` or `.js` file into `.opencode/plugins/` (project) or `~/.config/opencode/plugins/` (global). It will be loaded on next startup.

### Pin versions

For npm plugins, pin in `opencode.json`:

```json
{ "plugin": ["opencode-helicone-session@1.2.3"] }
```

## Removing Plugins

**Always confirm with the user via `AskUserQuestion` before removing.**

- **npm**: remove the entry from `opencode.json` `plugin` array. Restart OpenCode. (The package stays in `~/.cache/opencode/node_modules/` until cache clear.)
- **Local file**: delete the file from `.opencode/plugins/` or `~/.config/opencode/plugins/`.

## Validating Plugins

OpenCode does not ship a plugin validator CLI. Manual checks before publishing:

- [ ] Default export is an async function returning a hooks object (or a `Plugin` value)
- [ ] `package.json` includes `keywords: ["opencode-plugin"]`
- [ ] `peerDependencies` lists `@opencode-ai/plugin`
- [ ] `main` (and `types` if TypeScript) point at the bundled output
- [ ] No top-level side effects (network, fs writes) on import
- [ ] Throws in `tool.execute.before` are intentional (they block tool calls)
- [ ] No hardcoded credentials — use env vars and `{env:VAR}` substitution
- [ ] README documents required env vars and any opt-in `permission` rules

## Comparison with Claude Code Plugins

| Aspect | Claude Code | OpenCode |
|--------|-------------|----------|
| Manifest | `.claude-plugin/plugin.json` | npm `package.json` (no separate manifest) |
| Distribution | Marketplace JSON (`marketplace.json`), `/plugin marketplace add` | npm + GitHub direct linking |
| Components | Commands, agents, skills, hooks, MCP — declared as files in dirs | Custom tools, lifecycle hooks — defined in TypeScript code |
| Hook config | `hooks/hooks.json` (shell commands) | `tool.execute.before/after` plugin functions |
| Install scope | Project (`.claude/`), user, marketplace | Project (`.opencode/plugins/`), user (`~/.config/opencode/plugins/`), npm |
| `${CLAUDE_PLUGIN_ROOT}` | Yes | No equivalent — plugins use `directory` / `worktree` from context |
| Runtime | Shell commands | Bun (TypeScript) |
| Submission | Anthropic Plugin Directory | None — register on awesome-opencode / npm |
| Type safety | None (markdown + JSON) | Full TS types via `@opencode-ai/plugin` |

### Equivalences

| Claude Code plugin component | OpenCode equivalent |
|------------------------------|---------------------|
| `commands/*.md` | `command` block in `opencode.json` or `.opencode/commands/*.md` |
| `agents/*.md` | `agent` block in `opencode.json` or `.opencode/agents/*.md` |
| `skills/*/SKILL.md` | `.opencode/skills/*/SKILL.md` (compatible format) |
| `hooks/hooks.json` | `tool.execute.*` and `event` handlers in plugin |
| `.mcp.json` | `mcp` block in `opencode.json` |

## Sources

- https://opencode.ai/docs/plugins/
- https://opencode.ai/docs/custom-tools/
- https://opencode.ai/docs/ecosystem/
- https://www.npmjs.com/package/@opencode-ai/plugin
- https://lushbinary.com/blog/opencode-plugin-development-custom-tools-hooks-guide/
