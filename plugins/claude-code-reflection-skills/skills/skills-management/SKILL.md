---
name: skills-management
description: Manages skills for AI coding agents: list, install, remove, update, review, move, and discover. Use when the user asks to find, install, remove, or update skills, review skill quality, move skills between scopes, check for updates, or asks "how do I do X" where X might have an existing skill.
---

# Skills Manager

## Quick Reference

| Task | Command |
|------|---------|
| List all | `python3 scripts/list_skills.py` |
| List by scope | `python3 scripts/list_skills.py -s user` or `-s project` |
| Show details | `python3 scripts/show_skill.py <name>` |
| Review skill | `python3 scripts/review_skill.py <name>` |
| Delete | `python3 scripts/delete_skill.py <name>` |
| Move to user | `python3 scripts/move_skill.py <name> user` |
| Move to project | `python3 scripts/move_skill.py <name> project` |
| Create new | Use `/skill-creator` |
| **Discovery & Install** | |
| Find skills | `npx skills find [query]` |
| Review remote skills | Fetch skills.sh pages, assess using [assessment framework](references/remote-skill-assessment.md) |
| List ecosystem skills | `npx skills list` or `npx skills ls` |
| Install from GitHub | `npx skills add <owner/repo@skill> -g -y` |
| Remove ecosystem skill | `npx skills remove <name> -g -y` or `npx skills rm` |
| Check for updates | `npx skills check` |
| Update all | `npx skills update` |
| Browse online | [skills.sh](https://skills.sh) |
| **Multi-Agent** | |
| Detect agents | `python3 scripts/detect_agents.py` |
| List agent skills | `python3 scripts/list_agent_skills.py --agent cursor` |
| Install to agent | `python3 scripts/install_skill.py /path --agent cursor` |
| Copy between agents | `python3 scripts/copy_skill.py <name> --from claude-code --to cursor` |
| Move between agents | `python3 scripts/move_skill_agent.py <name> --from claude-code --to cursor` |

## Scopes

| Scope | Path | Visibility |
|-------|------|------------|
| User | `~/.claude/skills/` | All projects for this user |
| Project | `.claude/skills/` | This repository only |

User scope takes precedence over project scope for skills with the same name.

## Operations

### List Skills

```bash
python3 scripts/list_skills.py              # All skills
python3 scripts/list_skills.py -s user      # User scope only
python3 scripts/list_skills.py -f json      # JSON output
```

### Show Skill Details

```bash
python3 scripts/show_skill.py <name>           # Basic info
python3 scripts/show_skill.py <name> --files   # Include file listing
python3 scripts/show_skill.py <name> -f json   # JSON output
```

### Review Skill

Audits a skill against best practices and suggests improvements:

```bash
python3 scripts/review_skill.py <name>         # Review with text output
python3 scripts/review_skill.py <name> -f json # JSON output for programmatic use
```

**Checks performed:**
- Name format (lowercase, hyphens, max 64 chars, gerund form)
- Description quality (triggers, third person, specificity)
- Body length (warns if >500 lines)
- Time-sensitive content
- Path format (no Windows backslashes)
- Reference depth (should be one level)
- Table of contents for long files

**After reviewing:** Read the skill's SKILL.md and apply the suggested fixes directly.

### Delete Skill

**CRITICAL**: Always use `AskUserQuestion` to confirm before deleting: "Are you sure you want to delete the skill '[name]'? This cannot be undone."

```bash
python3 scripts/delete_skill.py <name>              # With script confirmation
python3 scripts/delete_skill.py <name> --force      # Skip script prompt
python3 scripts/delete_skill.py <name> -s project   # Target specific scope
```

### Move Skill

```bash
python3 scripts/move_skill.py <name> user      # Project → User (personal)
python3 scripts/move_skill.py <name> project   # User → Project (share with team)
python3 scripts/move_skill.py <name> user -f   # Overwrite if exists
```

### Modify Skill

1. Run `python3 scripts/show_skill.py <name>` to locate it
2. Edit SKILL.md directly at the returned path

### Create New Skill

Use the `/skill-creator` skill for guided creation with proper structure.

## Discover & Install Skills

Search and install skills from the open agent skills ecosystem via the [Skills CLI](https://github.com/vercel-labs/add-skill) (`npx skills`). Browse at [skills.sh](https://skills.sh).

### Find Skills

```bash
npx skills find [query]              # Interactive search
npx skills find react performance    # Keyword search
npx skills find pr review            # Search by task
```

### Install from Ecosystem

```bash
npx skills add <owner/repo@skill> -g -y    # Install globally, skip prompts
npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -y
```

### List Ecosystem Skills

```bash
npx skills list                      # List all installed ecosystem skills
npx skills ls                        # Alias
npx skills list -g                   # Global skills only
npx skills list -a cursor            # Skills for a specific agent
```

### Remove Ecosystem Skills

Uninstalls skills installed via `npx skills add`. For locally-created skills, use `python3 scripts/delete_skill.py` instead.

**CRITICAL**: Always confirm with the user before removing.

```bash
npx skills remove <name> -g -y       # Remove a global skill, skip prompt
npx skills rm <name>                 # Alias, with confirmation prompt
npx skills remove <name> -a cursor   # Remove from specific agent
npx skills remove --all -g -y        # Remove all global ecosystem skills
```

### Check & Update

```bash
npx skills check                     # Check for available updates
npx skills update                    # Update all installed skills
```

When the user asks to "update skills", "update all skills", "are my skills up to date?", or "check for updates":

1. Run `npx skills check` first to show what has updates available
2. If updates exist, confirm with user before running `npx skills update`
3. After updating, remind user to restart the agent for changes to take effect

### When to Search

Use `npx skills find` when the user:
- Asks "how do I do X" where X is a common task
- Says "find a skill for X" or "is there a skill for X"
- Wants specialized capabilities (design, testing, deployment, etc.)

### Common Search Categories

| Category | Example queries |
|----------|----------------|
| Web Dev | react, nextjs, typescript, tailwind |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Docs | docs, readme, changelog, api-docs |
| Quality | review, lint, refactor, best-practices |
| Design | ui, ux, design-system, accessibility |
| Productivity | workflow, automation, git |

### Review & Compare Results

When search results are ambiguous (3+ results, similar names, or user asks to compare), assess candidates before recommending. This is agent-driven — use WebFetch on `https://skills.sh/<owner>/<repo>/<skill>` pages and apply judgment.

**Trigger conditions:**
- 3+ results returned for a query
- Multiple results with similar names or overlapping descriptions
- User asks to compare, review, evaluate, or pick the best
- A result has suspicious metrics (niche topic with very high installs)

**Process:**
1. Fetch skills.sh pages for top 3-6 candidates
2. Evaluate quality signals: install count, agent distribution, age, description, relevance, overlap with installed skills
3. Assign verdict: Recommended / Consider / Skip
4. Present ranked summary with 1-2 sentence assessments

See [references/remote-skill-assessment.md](references/remote-skill-assessment.md) for the full assessment framework including red flags and scoring signals.

### No Results

If no skills found: offer to help directly, then suggest `npx skills init <name>` to create a custom skill.

## Multi-Agent Operations

Manage skills across 42 supported AI coding agents. Full registry at [skills.sh](https://skills.sh).

### Supported Agents

| Agent ID | Display Name | Project Skills Dir | Global Skills Dir |
|----------|--------------|-------------------|-------------------|
| `adal` | AdaL | `.adal/skills` | `~/.adal/skills` |
| `amp` | Amp | `.agents/skills` | `~/.config/agents/skills` |
| `antigravity` | Antigravity | `.agent/skills` | `~/.gemini/antigravity/skills` |
| `augment` | Augment | `.augment/skills` | `~/.augment/skills` |
| `claude-code` | Claude Code | `.claude/skills` | `~/.claude/skills` |
| `cline` | Cline | `.cline/skills` | `~/.cline/skills` |
| `codebuddy` | CodeBuddy | `.codebuddy/skills` | `~/.codebuddy/skills` |
| `codex` | Codex | `.agents/skills` | `~/.codex/skills` |
| `command-code` | Command Code | `.commandcode/skills` | `~/.commandcode/skills` |
| `continue` | Continue | `.continue/skills` | `~/.continue/skills` |
| `crush` | Crush | `.crush/skills` | `~/.config/crush/skills` |
| `cursor` | Cursor | `.cursor/skills` | `~/.cursor/skills` |
| `droid` | Droid | `.factory/skills` | `~/.factory/skills` |
| `gemini-cli` | Gemini CLI | `.agents/skills` | `~/.gemini/skills` |
| `github-copilot` | GitHub Copilot | `.agents/skills` | `~/.copilot/skills` |
| `goose` | Goose | `.goose/skills` | `~/.config/goose/skills` |
| `iflow-cli` | iFlow CLI | `.iflow/skills` | `~/.iflow/skills` |
| `junie` | Junie | `.junie/skills` | `~/.junie/skills` |
| `kilo` | Kilo Code | `.kilocode/skills` | `~/.kilocode/skills` |
| `kimi-cli` | Kimi Code CLI | `.agents/skills` | `~/.config/agents/skills` |
| `kiro-cli` | Kiro CLI | `.kiro/skills` | `~/.kiro/skills` |
| `kode` | Kode | `.kode/skills` | `~/.kode/skills` |
| `mcpjam` | MCPJam | `.mcpjam/skills` | `~/.mcpjam/skills` |
| `mistral-vibe` | Mistral Vibe | `.vibe/skills` | `~/.vibe/skills` |
| `mux` | Mux | `.mux/skills` | `~/.mux/skills` |
| `neovate` | Neovate | `.neovate/skills` | `~/.neovate/skills` |
| `openclaw` | OpenClaw | `skills` | `~/.openclaw/skills` |
| `opencode` | OpenCode | `.agents/skills` | `~/.config/opencode/skills` |
| `openhands` | OpenHands | `.openhands/skills` | `~/.openhands/skills` |
| `pi` | Pi | `.pi/skills` | `~/.pi/agent/skills` |
| `pochi` | Pochi | `.pochi/skills` | `~/.pochi/skills` |
| `qoder` | Qoder | `.qoder/skills` | `~/.qoder/skills` |
| `qwen-code` | Qwen Code | `.qwen/skills` | `~/.qwen/skills` |
| `replit` | Replit | `.agents/skills` | `~/.config/agents/skills` |
| `roo` | Roo Code | `.roo/skills` | `~/.roo/skills` |
| `trae` | Trae | `.trae/skills` | `~/.trae/skills` |
| `trae-cn` | Trae CN | `.trae/skills` | `~/.trae-cn/skills` |
| `windsurf` | Windsurf | `.windsurf/skills` | `~/.codeium/windsurf/skills` |
| `zencoder` | Zencoder | `.zencoder/skills` | `~/.zencoder/skills` |

### Detect Installed Agents

```bash
python3 scripts/detect_agents.py              # List detected agents
python3 scripts/detect_agents.py --all        # Show all supported agents
python3 scripts/detect_agents.py -f json      # JSON output
```

### List Skills for Any Agent

```bash
python3 scripts/list_agent_skills.py --agent cursor           # Single agent
python3 scripts/list_agent_skills.py --agent goose -s global  # Specific scope
python3 scripts/list_agent_skills.py --all                    # All detected agents
python3 scripts/list_agent_skills.py --agent amp -f json      # JSON output
```

### Install Skill to Agents

```bash
python3 scripts/install_skill.py /path/to/skill --agent cursor              # Single agent
python3 scripts/install_skill.py /path/to/skill --agent cursor --agent amp  # Multiple agents
python3 scripts/install_skill.py /path/to/skill --all                       # All detected
python3 scripts/install_skill.py /path/to/skill --agent goose -s global     # Global scope
python3 scripts/install_skill.py /path/to/skill --agent cursor --force      # Overwrite
```

### Copy Skill Between Agents

```bash
python3 scripts/copy_skill.py my-skill --from claude-code --to cursor
python3 scripts/copy_skill.py my-skill --from claude-code --to cursor --to-scope global
python3 scripts/copy_skill.py my-skill --from claude-code --from-scope project --to amp
python3 scripts/copy_skill.py my-skill --from claude-code --to cursor --force
```

### Move Skill Between Agents

```bash
python3 scripts/move_skill_agent.py my-skill --from claude-code --to cursor
python3 scripts/move_skill_agent.py my-skill --from claude-code --to goose --force
```

## Important Notes

- **Restart required**: After adding, removing, or moving skills, restart the AI agent for changes to take effect
- **Edits are immediate**: Changes to existing skill content work without restart
- **Agent detection**: Uses config directory presence to detect installed agents

## References — The Complete Guide to Building Skills for Claude

Consult these when reviewing skills or advising on skill structure and best practices.

| File | Description |
|------|-------------|
| `references/01-introduction.md` | What skills are, who this guide is for, two learning paths |
| `references/02-fundamentals.md` | Skill structure, progressive disclosure, composability, MCP integration |
| `references/03-planning-and-design.md` | Use cases, categories, success criteria, YAML frontmatter, writing instructions |
| `references/04-testing-and-iteration.md` | Trigger tests, functional tests, performance comparison, skill-creator usage |
| `references/05-distribution-and-sharing.md` | Distribution model, API usage, GitHub hosting, positioning |
| `references/06-patterns-and-troubleshooting.md` | 5 workflow patterns, common errors and fixes |
| `references/07-resources-and-references.md` | Official docs, example skills, tools, support channels |
| `references/ref-a-quick-checklist.md` | Pre-build, development, upload, and post-upload checklists |
| `references/ref-b-yaml-frontmatter.md` | Required/optional fields, security restrictions |
| `references/ref-c-complete-skill-examples.md` | Links to production-ready skill examples |
| `references/remote-skill-assessment.md` | Framework for evaluating ecosystem skills before installation |

## Acknowledgments

Multi-agent support is based on the [Skills CLI](https://github.com/vercel-labs/add-skill) (`npx skills`) by Vercel Labs. Browse the open agent skills ecosystem at [skills.sh](https://skills.sh).
