# Repository History Investigator skill

A production-oriented Agent Skill for Claude Code, Codex, and compatible agents. It helps a coding agent inspect GitHub repository history before risky edits using local git history, GitHub PRs, review comments, and anomaly-aware provenance matching.

## Contents

```text
investigating-repository-history/
├── SKILL.md
├── scripts/
│   ├── history_context.py
│   ├── compact_pr.py
│   └── validate_skill.py
├── references/
│   ├── ANOMALIES.md
│   ├── GH_CLI.md
│   ├── DECISION_ATOMS.md
│   ├── OUTPUT_SCHEMA.md
│   └── EVALUATION.md
├── tests/
│   └── test_skill.py
├── agents/
│   └── openai.yaml
└── assets/
    └── history-note-template.md
```

## Install

For repository-scoped Codex use, copy this folder to:

```text
$REPO_ROOT/.agents/skills/investigating-repository-history
```

For personal Codex use:

```text
$HOME/.agents/skills/investigating-repository-history
```

For Claude Code, copy it to your Claude skills directory, for example:

```text
$HOME/.claude/skills/investigating-repository-history
```

## Validate

```bash
python3 scripts/validate_skill.py .
```

## Tests

Run the full self-contained test suite (stdlib `unittest`, no external deps):

```bash
python3 -m unittest tests.test_skill -v
```

Tests cover: package structure, YAML frontmatter, gh-only access policy (no
direct `api.github.com` calls), `--help` / `--version` for every script, the
`validate_skill.py` validator, and a local-only smoke test of `history_context.py`
that builds a tiny throw-away git repo and runs `inspect` with `--no-gh`.

## Quick run

From a git repository with `gh` authenticated:

```bash
python3 scripts/history_context.py inspect \
  --repo-dir /path/to/repo \
  --path src/foo.ts \
  --start 10 --end 30 \
  --question "Can I remove this check?" \
  --format markdown
```
