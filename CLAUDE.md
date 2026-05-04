# AI-Driven Development — Development Guide

This repo is a single-plugin marketplace and a cross-agent skill collection in one. The same `skills/` directory at the repo root is read by both `npx skills add` (the cross-agent CLI) and Claude Code's plugin install (`/plugin marketplace add` + `/plugin install …@ai-driven-development`). The plugin sees the repo root as itself via `source: "./"` in `marketplace.json` — no nesting, no symlinks, no duplication.

## When to create tags and releases

**Only create git tags and GitHub releases when skill, hook, or plugin files change.**

### Requires a new tag/release

- `skills/*/` — any skill file changes (SKILL.md, scripts, references, assets)
- `hooks/*/` — any hook source changes (Go code, install scripts, hook configs)
- `.claude-plugin/plugin.json` — plugin manifest changes
- `.claude-plugin/marketplace.json` — marketplace catalogue changes
- `LICENSE` — licence changes

Examples:

- Adding a new skill or hook
- Updating skill instructions in SKILL.md
- Modifying skill scripts
- Changing plugin metadata or version

### Does NOT require a new tag/release

Documentation-only changes don't need tagging:

- `README.md` — documentation and use-case updates
- `CLAUDE.md` — this file
- Commit messages
- GitHub-specific files (`.github/*`)

**Rationale:** users install specific commits via SHA. Documentation updates don't affect functionality, so they don't need version bumps. This keeps the release history clean.

## README maintenance

The repo ships **English-only**. When you add or remove a skill, or change a skill description:

- Update the relevant section table in `README.md`
- Update the skill's own `SKILL.md` (agent-facing) and `README.md` (human-facing, optional)
- Update `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` versions

## Versioning

Follow semver:

- **MAJOR** (x.0.0) — breaking changes to skill interfaces, removals, layout overhauls
- **MINOR** (X.x.0) — new skills, new hooks, backward-compatible features
- **PATCH** (X.X.x) — bug fixes, prompt tweaks, doc fixes that ship in skills

## Release process

When skill/hook/plugin files change:

1. Bump version in `.claude-plugin/plugin.json` AND `.claude-plugin/marketplace.json` (keep them in sync).
2. Commit changes.
3. Create and push tag: `git tag -a vX.Y.Z -m "Version X.Y.Z" && git push origin vX.Y.Z`
4. Create GitHub release: `gh release create vX.Y.Z --title "vX.Y.Z — Title" --notes "Release notes"`

The bash-guard hook ships its own pre-built binary release with a separate tag (`bash-guard-vX.Y.Z`) — see [hooks/balanced-safety-hooks/](hooks/balanced-safety-hooks/) for that release flow.

## Repository structure

```
ai-driven-development/
├── .claude-plugin/
│   ├── marketplace.json    ← single-plugin marketplace, source: "./"
│   └── plugin.json
├── skills/                  ← canonical Agent Skills layout (npx skills add)
│   └── <skill-name>/SKILL.md (+ optional README.md, references/, scripts/, assets/)
├── hooks/
│   └── <hook-name>/         ← Claude Code hooks (Go binary + install scripts)
├── README.md
├── CLAUDE.md
└── LICENSE
```

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`).
2. Add optional `README.md`, `references/`, `scripts/`, `assets/` as needed.
3. Update the relevant section table in the root `README.md`.
4. Bump `version` in both `.claude-plugin/*.json` files (minor bump for new skill).
5. Commit, tag, release.

## Adding a new hook

1. Create `hooks/<hook-name>/` with the hook implementation, `install.sh`, and `README.md`.
2. If the hook ships pre-built binaries, add a release flow (see `hooks/balanced-safety-hooks/` as the canonical example: cross-platform Go build via `make build-all`, GitHub release with `SHA256SUMS`, `install-prebuilt.sh` that pins by tag).
3. Update the Hooks section in the root `README.md`.
4. Bump `version` in both `.claude-plugin/*.json` files.
5. Commit, tag, release.
