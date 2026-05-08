<p align="center">
  <img src="https://img.shields.io/badge/Agent_Skills-Collection-blueviolet?style=for-the-badge" alt="Agent Skills Collection">
  <img src="https://img.shields.io/badge/Skills-19-blue?style=for-the-badge" alt="19 Skills">
  <img src="https://img.shields.io/badge/Hooks-1-yellow?style=for-the-badge" alt="1 Hook">
  <img src="https://img.shields.io/badge/Agents-12+-orange?style=for-the-badge" alt="12+ Agents">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">AI-Driven Development</h1>

<p align="center">
  <strong>Practices, protocols, and skills for AI-driven software development</strong>
</p>

<p align="center">
  An umbrella collection of 19 skills + 1 hook that work across <strong>Claude Code, Codex CLI, OpenCode, Cursor, Gemini CLI, Antigravity</strong>, and any other agent that supports the <a href="https://agentskills.io">Agent Skills</a> standard.
</p>

---

## Installation

**Via Skills CLI** (recommended — works in 12+ agents):

```bash
# Install all 19 skills
npx skills add CodeAlive-AI/ai-driven-development

# Or pick a single skill
npx skills add CodeAlive-AI/ai-driven-development --skill prompt-engineering
```

**Via Claude Code plugin marketplace:**

```bash
/plugin marketplace add CodeAlive-AI/ai-driven-development
/plugin install ai-driven-development@ai-driven-development
# Restart Claude Code for changes to take effect
```

The Bash safety hook (`bash-guard`) ships separately — see [hooks/balanced-safety-hooks/](hooks/balanced-safety-hooks/) for its install one-liner.

---

## What's Included

### Agent reflection & meta (7)

Meta-skills that let AI coding agents configure themselves. No more editing config files — just tell your agent what you need.

| Skill | What It Does |
|-------|--------------|
| [mcp-management](skills/mcp-management/) | Install and manage MCP servers across 10+ coding agents (Claude Code, Cursor, VS Code, Gemini CLI, Codex, Goose, Copilot CLI, OpenCode, Zed) — single command, handles JSON/YAML/TOML config differences |
| [hooks-management](skills/hooks-management/) | Manage hooks and automation for Claude Code, Codex CLI, and OpenCode |
| [settings-management](skills/settings-management/) | Configure settings for Claude Code (JSON), Codex CLI (TOML), and OpenCode (JSON/JSONC) |
| [subagents-management](skills/subagents-management/) | Create and manage subagents across Claude Code, Codex CLI, and OpenCode |
| [skills-management](skills/skills-management/) | Organise, discover, and share skills for coding agents |
| [plugins-management](skills/plugins-management/) | Package and publish plugins for Claude Code and OpenCode (validate, scaffold, submit to Anthropic's directory) |
| [optimizing-claude-code](skills/optimizing-claude-code/) | Audit repos and optimise CLAUDE.md for agent work |

### Engineering practices (4)

Disciplined approaches that improve how agents and humans collaborate on code.

| Skill | What It Does |
|-------|--------------|
| [prompt-engineering](skills/prompt-engineering/) | Universal prompt-engineering toolkit. 14 reference docs covering Claude / GPT / Gemini family-specific guidance, prompting techniques, evaluation & red-teaming, common failure modes (hallucinations, security, structure, debt) |
| [fpf-problem-solving](skills/fpf-problem-solving/) | First Principles Framework — a transdisciplinary "operating system for thought". Decompose cross-domain problems, audit conclusions, and reason rigorously about complex systems. Based on Anatoly Levenchuk's [FPF](https://github.com/ailev/FPF) |
| [bug-fix-protocol](skills/bug-fix-protocol/) | 8-step bug-fix protocol. Treats every production bug as **two** failures (the code defect + the testing system that allowed it through) and enforces a step-8 audit that closes the gap |
| [investigating-repository-history](skills/investigating-repository-history/) | Reconstruct historical intent before risky edits. Local `git blame`/`log` + GitHub PR/review evidence (via `gh`, never direct API), with squash/rebase/cherry-pick/rename/revert anomaly handling, decision-atom extraction, and confidence-scored output — produces a cited history note instead of guessing |

### Research & docs (3)

| Skill | What It Does |
|-------|--------------|
| [semantic-scholar-deep](skills/semantic-scholar-deep/) | Deep research over the Semantic Scholar Graph API — backward references, recommendations, batch lookup (up to 500 IDs), multi-hop citation-graph BFS, snippet search. Ships with an optional paired subagent for token-isolated literature reviews |
| [fetch-url-as-markdown](skills/fetch-url-as-markdown/) | URL → clean Markdown via local trafilatura (real-browser UA, anti-stub guards, structured exit codes), with Exa MCP as a fallback for JS-rendered or anti-bot pages. Drop-in replacement for built-in WebFetch |
| [ubiquitous-language](skills/ubiquitous-language/) | Domain thesaurus manager — DDD naming consistency, thesaurus generation, naming audit |

### Multi-agent orchestration (1)

| Skill | What It Does |
|-------|--------------|
| [agents-consilium](skills/agents-consilium/) | Query Codex CLI and Gemini CLI in parallel for independent expert opinions on architecture, code reviews, and investigations. Different models bring different angles: more original ideas in brainstorming, broader coverage in code review |

### macOS & system health (1)

| Skill | What It Does |
|-------|--------------|
| [maintaining-macos-health](skills/maintaining-macos-health/) | Disk cleanup + dev-machine optimisation + proactive health alerting. Triage flow for kernel panic / watchdog timeout / `vm-compressor-space-shortage` / Jetsam events. Tiered cleanup playbook (zero-risk → discuss-first), Mole-style safety guards, and a noise-resistant LaunchAgent alerter (3 CRITICAL-only triggers, hysteresis, calibration window). Apple Silicon focus |

### Niche utilities (3)

| Skill | What It Does |
|-------|--------------|
| [clipboard](skills/clipboard/) | Copy text to macOS clipboard with optional rich formatting (HTML + plain text). Slack/LinkedIn-aware — uses HTML rich text instead of mrkdwn, and warns about `<table>` not rendering in chat targets |
| [repo-explorer](skills/repo-explorer/) | Explores repositories by delegating to Claude Code CLI. Saves context for the calling agent and speeds up codebase understanding |
| [windows-qa-engineer](skills/windows-qa-engineer/) | Manual QA copilot for Windows 11 desktop apps (WinForms / WPF / UWP). Uses Microsoft UFO (UIA / Win32) + FastMCP `mount()` composition + MCP protocol |

### Hooks (1)

Standalone agent-safety tooling that doesn't fit the skill format — typically because it has to live inside an agent's hook protocol or run as a compiled binary.

| Hook | What It Does | Install |
|------|--------------|---------|
| [balanced-safety-hooks](hooks/balanced-safety-hooks/) | `bash-guard` — Claude Code `PreToolUse:Bash` safety hook in Go. Real Bash AST parsing via [`mvdan.cc/sh`](https://github.com/mvdan/sh) (heredocs, single-quoted prose, `sudo`/`env`/`xargs`/`bash -c`/`eval`/`ssh`/pipe-to-shell). Catastrophic-path matrix with safe-path carve-outs. **Default rule set uses `ask`, not `deny`** — agents trivially bypass `deny` by rephrasing. Covers `rm`/`unlink`/`shred`, ORM migrations, infra (kubectl/gcloud/helm/docker/terraform/`git push -f`), PaaS CLIs (railway/fly/heroku), DB clients (psql/redis-cli), and cloud control-plane API mutations | `curl -fsSL https://raw.githubusercontent.com/CodeAlive-AI/ai-driven-development/main/hooks/balanced-safety-hooks/install-prebuilt.sh \| sh` |

---

## Working principles

This collection is built on four principles that show up across all skills:

1. **Cross-agent first.** Skills follow the [Agent Skills](https://agentskills.io) open standard so they work in Claude Code, Cursor, Codex, Gemini, OpenCode, Antigravity, Copilot CLI — anywhere `npx skills add` reaches.
2. **Low false-positive friction.** Tools that interrupt your workflow (the bash-guard hook, agent prompts) are tuned for high signal: only ask when the action is genuinely destructive, not when there's a fuzzy keyword match.
3. **Disciplined defaults.** Skills like `bug-fix-protocol` and `fpf-problem-solving` codify practices that pay off when the agent goes off the happy path — multi-step protocols rather than one-shot prompts.
4. **Token-cheap.** Skill descriptions are kept tight so they don't dominate context. The [`semantic-scholar-deep`](skills/semantic-scholar-deep/) skill goes further with an optional paired subagent for token-isolated research.

---

## Repository structure

```
ai-driven-development/
├── .claude-plugin/
│   ├── marketplace.json         ← lists this repo as a single plugin (source: "./")
│   └── plugin.json               ← umbrella plugin manifest
├── skills/                       ← canonical agent-skills layout
│   ├── agents-consilium/
│   ├── bug-fix-protocol/
│   ├── clipboard/
│   ├── fetch-url-as-markdown/
│   ├── fpf-problem-solving/
│   ├── hooks-management/
│   ├── investigating-repository-history/
│   ├── maintaining-macos-health/
│   ├── mcp-management/
│   ├── optimizing-claude-code/
│   ├── plugins-management/
│   ├── prompt-engineering/
│   ├── repo-explorer/
│   ├── semantic-scholar-deep/
│   ├── settings-management/
│   ├── skills-management/
│   ├── subagents-management/
│   ├── ubiquitous-language/
│   └── windows-qa-engineer/
├── hooks/
│   └── balanced-safety-hooks/    ← bash-guard (Go, pre-built binaries via release)
├── README.md (+ ru/zh/pt-BR translations)
├── CLAUDE.md
└── LICENSE
```

The same `skills/` directory is read by both `npx skills add` (the cross-agent CLI) and Claude Code's plugin install — no symlinks, no duplication. The `.claude-plugin/marketplace.json` declares this repo itself as a single plugin via `source: "./"`.

---

## Contributing

Each skill lives in `skills/<skill-name>/` with a `SKILL.md` (agent-facing contract) and an optional `README.md` (human-facing entry). Most skills also have `references/`, `scripts/`, or `assets/` directories for supporting material.

When adding a skill or materially changing one, refresh:

- The skill's own `SKILL.md` and `README.md`
- The relevant section table above
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` version (semver — minor bump for new skills, major for breaking interface changes)

See [CLAUDE.md](CLAUDE.md) for the full development guide.

---

## Heritage

This collection is the consolidation of nine previously-separate CodeAlive-AI repositories:

- `agents-reflection-skills` (the 7 meta-skills, the marketplace base)
- `prompt-engineering-skill`
- `fpf-problem-solving-skill`
- `clipboard-skill`
- `claude-repo-explorer-skill`
- `windows-qa-engineer-skill`
- `ai-driven-development` (the original — bug-fix protocol)
- `awesome-agent-skills` (5 skills + the bash-guard hook)

The 7 meta-skills' commit history lives on in this repo (consolidated via `git mv`). The other source repos retain their own histories at their original URLs and will be archived with pointer READMEs shortly.

---

## License

MIT
