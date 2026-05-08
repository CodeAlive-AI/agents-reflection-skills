---
name: investigating-repository-history
description: Investigate GitHub repository history before risky code changes using git blame/log, GitHub PRs, review comments, squash/rebase/cherry-pick/rename heuristics, and cited evidence. Use when asking why code exists, whether a change is safe, what PR introduced behavior, or before editing API, compatibility, security, concurrency, persistence, migration, or performance-sensitive code.
license: MIT
compatibility: Designed for Claude Code, Codex, and similar coding agents. Requires a local git clone; bundled scripts require Python 3.9+, git, and authenticated GitHub CLI `gh` for GitHub PR evidence.
allowed-tools: Bash(git:*) Bash(gh:*) Bash(python3:*) Read Grep
metadata:
  version: "1.0.0"
  methodology: "Provenance Mesh"
---

# Repository History Investigator

Use this skill to reconstruct the historical intent behind code before changing it. The goal is not merely “find the blame commit”; the goal is to return a compact, cited history note explaining relevant PRs, review comments, constraints, rejected approaches, and anomalies.

## Contents

- [Trigger conditions](#trigger-conditions)
- [Core rule](#core-rule)
- [Fast path](#fast-path)
- [Progressive disclosure](#progressive-disclosure)
- [Investigation workflow](#investigation-workflow)
- [Evidence confidence rules](#evidence-confidence-rules)
- [Output template](#output-template)
- [Gotchas](#gotchas)
- [Available scripts](#available-scripts)

## Trigger conditions

Use this skill when the user asks any of these:

- “Why is this code written this way?”
- “Can I remove/simplify/change this check, constraint, branch, migration, public API, or feature flag?”
- “Which PR introduced this behavior or regression?”
- “Find the relevant PR/review discussion/history for this code.”
- Before editing code that touches API compatibility, security, concurrency, persistence, migrations, performance, generated interfaces, feature flags, or unclear legacy/workaround logic.

Do not use this skill for trivial new code with no dependency on existing behavior.

## Core rule

Before making a risky edit, produce a **history note** answering:

1. What code scope was inspected?
2. Which commits and PRs are relevant?
3. Which review comments or PR discussions explain intent?
4. What constraints, risks, rejected approaches, or tests were found?
5. Is the evidence strong, weak, contradictory, stale, truncated, or unknown?
6. How should the implementation plan change?

If the evidence is weak, say `UNKNOWN` and lower confidence. Never invent intent from a semantic match alone.

## Fast path

From the repository working tree, run the collector first. If the skill directory is not the current directory, prefix the script path with the installed skill path and pass `--repo-dir /path/to/repo`.

```bash
python3 scripts/history_context.py inspect \
  --repo-dir /path/to/repo \
  --path path/to/file.ext \
  --start 120 --end 160 \
  --question "Can I remove this constraint?" \
  --format markdown
```

For symbol-level questions without exact lines:

```bash
python3 scripts/history_context.py inspect \
  --repo-dir /path/to/repo \
  --path path/to/file.ext \
  --symbol SymbolOrFunctionName \
  --question "Why does this behavior exist?" \
  --format markdown
```

For JSON suitable for deeper agent reasoning:

```bash
python3 scripts/history_context.py inspect \
  --repo-dir /path/to/repo \
  --path path/to/file.ext \
  --start 120 --end 160 \
  --symbol SymbolOrFunctionName \
  --question "What PR introduced this behavior?" \
  --format json \
  --output history-context.json
```

Then read only the relevant sections of the output. Do not paste huge raw PR/comment dumps into the final answer.

## Progressive disclosure

Load these files only when needed:

- `references/ANOMALIES.md` — use when exact commit→PR mapping fails, or when squash, rebase, cherry-pick, backport, revert, rename, split, generated files, or mass refactors are possible.
- `references/GH_CLI.md` — use when the script fails or manual `gh api` calls are needed.
- `references/DECISION_ATOMS.md` — use when converting PR/comment evidence into constraints, risks, rejected approaches, or test requirements.
- `references/OUTPUT_SCHEMA.md` — use when producing a formal machine-readable report.
- `references/EVALUATION.md` — use when testing or improving the skill.

## Investigation workflow

1. **Define scope.** Identify paths, line ranges, symbols, tests, error strings, feature flags, and any proposed diff.
2. **Collect local history.** Use the script or manual `git blame -w -M -C -C -C`, `git log --follow`, `git log -S`, and `git log -G`.
3. **Map commits to PRs.** Prefer exact GitHub commit→PR association. Treat it as one signal, not the entire answer.
4. **Fetch PR evidence.** For candidate PRs, inspect PR body, files, commits, reviews, inline review comments, and issue comments.
5. **Resolve anomalies.** If mapping is weak, apply the Provenance Mesh: commit association + patch equivalence + content/symbol lineage.
6. **Extract decision atoms.** Convert evidence into explicit claims: constraints, compatibility requirements, security invariants, performance constraints, rejected approaches, test requirements.
7. **Assess risk.** Downgrade confidence for semantic-only matches, path-only matches, reverted PRs, API truncation, large PRs, generated files, or missing PRs.
8. **Produce a history note** before editing code.

## Evidence confidence rules

High confidence:
- exact GitHub commit→PR association; or
- patch/hunk equivalence plus path/symbol agreement; or
- review comment remaps to the current hunk/symbol and matches the proposed change.

Medium confidence:
- same symbol/path plus relevant PR discussion, but no patch-level match.

Low confidence:
- semantic search only, title/body match only, path-only match, or stale/reverted evidence.

Never claim “this was decided” unless a commit, PR body, review, review comment, issue comment, or linked issue supports it.

## Output template

Use this concise template in the final answer or implementation plan:

```markdown
## History note

Scope inspected: [paths, lines, symbols]

Relevant evidence:
- PR #[n] — [relation: exact/squash-like/rename-lineage/search], [why relevant], [confidence]
- Commit [sha] — [what it changed], [relation]
- Review/comment — [constraint or concern]

Decision atoms:
- [constraint/risk/rejected approach/test requirement] — [claim] — evidence: [PR/comment/commit]

Risk: [low|medium|high|unknown]
Confidence: [0.00-1.00]
Unknowns/truncation: [none or list]
Plan impact: [proceed|modify plan|ask human|do not change]
```

## Gotchas

- `git blame` is a seed generator, not truth. Formatting commits, moves, squashes, and refactors can hide origin.
- A PR can be relevant even if it did not introduce the current line; review comments may explain why an alternative was rejected.
- Squash merges often require patch/hunk matching because the final commit SHA differs from PR commits.
- File paths are not identity. Track file lineage, directory moves, symbol fingerprints, and hunk context.
- Reverted PRs are stale evidence unless a later PR reintroduced the same decision.
- Large `gh api` responses may be truncated by the underlying GitHub endpoints. If truncation is possible, mark evidence incomplete.
- General PR conversation comments come from issue comments; inline review comments come from PR review comments.

## Available scripts

- `scripts/history_context.py` — main collector for local Git + GitHub PR evidence. Run `python3 scripts/history_context.py --help`.
- `scripts/compact_pr.py` — fetch one or more PRs and print compact evidence. Run `python3 scripts/compact_pr.py --help`.
- `scripts/validate_skill.py` — validate this skill’s frontmatter and basic structure.
