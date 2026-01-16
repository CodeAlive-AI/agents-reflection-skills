# Claude Code Reflection Skills - Development Guide

## When to Create Tags and Releases

**Only create git tags and GitHub releases when skill or plugin files change.**

### Requires New Tag/Release

Changes to these files/directories require a new version tag and release:

- `skills/*/` - Any skill file changes (SKILL.md, scripts, references, assets)
- `.claude-plugin/plugin.json` - Plugin manifest changes
- `LICENSE` - License changes

Examples:
- Adding a new skill
- Updating skill instructions in SKILL.md
- Modifying skill scripts
- Changing plugin metadata or version

### Does NOT Require New Tag/Release

Documentation-only changes do not require tagging:

- `README.md` - Documentation and use case updates
- `CLAUDE.md` - This file
- Commit messages
- GitHub-specific files (.github/*)

**Rationale:** Users install specific commits via SHA. Documentation updates don't affect functionality, so they don't need version bumps. This keeps the release history clean and meaningful.

## Versioning

Follow semantic versioning (semver):

- **MAJOR** (x.0.0) - Breaking changes to skill interfaces
- **MINOR** (1.x.0) - New skills or backward-compatible features
- **PATCH** (1.0.x) - Bug fixes and minor improvements

## Release Process

When skill/plugin files change:

1. Update version in `.claude-plugin/plugin.json`
2. Commit changes
3. Create and push tag: `git tag -a vX.Y.Z -m "Version X.Y.Z" && git push origin vX.Y.Z`
4. Create GitHub release: `gh release create vX.Y.Z --title "vX.Y.Z - Title" --notes "Release notes"`

## Current Structure

```
claude-code-reflection-skills/
├── .claude-plugin/
│   └── plugin.json          # Version metadata - changes require release
├── skills/                  # All changes require release
│   ├── claude-mcp-installer/
│   ├── claude-hooks-manager/
│   ├── claude-settings-manager/
│   ├── claude-subagents-manager/
│   ├── claude-skills-manager/
│   └── claude-plugins-manager/
├── README.md                # Documentation - no release needed
├── CLAUDE.md                # This file - no release needed
└── LICENSE                  # Changes require release
```
