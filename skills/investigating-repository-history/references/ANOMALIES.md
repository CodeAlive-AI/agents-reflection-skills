# History anomalies reference

Use this when exact blame commit → PR mapping is missing, weak, or suspicious.

## Contents

- [Provenance Mesh](#provenance-mesh)
- [Squash merge](#squash-merge)
- [Rebase merge and reused commits](#rebase-merge-and-reused-commits)
- [Cherry-pick and backport](#cherry-pick-and-backport)
- [Reverts and re-applies](#reverts-and-re-applies)
- [Lost renames and moved code](#lost-renames-and-moved-code)
- [Mass refactor / formatting commits](#mass-refactor--formatting-commits)
- [Generated, vendor, lock, and snapshot files](#generated-vendor-lock-and-snapshot-files)
- [PR-less direct commits](#pr-less-direct-commits)

## Provenance Mesh

Do not model history as a line. Model it as a graph:

```text
LineSpan ──owned_by── Commit
LineSpan ──inside── Symbol
File ──renamed_from── File
Symbol ──moved_from── Symbol
Commit ──associated_with── PullRequest
Commit ──patch_equivalent_to── PullRequest
Hunk ──discussed_in── ReviewComment
DecisionAtom ──supported_by── Evidence[]
DecisionAtom ──superseded_by── DecisionAtom
```

Use three independent indexes:

1. **Commit Association Index** — exact GitHub commit→PR links, merge commits, PR commits.
2. **Patch Equivalence Index** — stable patch IDs, normalized hunk fingerprints, inverse patches.
3. **Content Lineage Index** — file rename graph, directory moves, symbol fingerprints, moved/copied-line anchors.

Accept a high-confidence inference only when:

- exact GitHub association exists; or
- two independent non-exact indexes agree; or
- one non-exact signal is extremely strong and no contradictory candidate exists.

## Squash merge

Problem: the commit on the base branch may not be any commit from the PR.

Signals:

- final commit message contains `#123`, `PR #123`, or `Merge pull request #123`;
- commit net patch matches PR net diff;
- hunk bag Jaccard similarity is high;
- same paths, directories, public symbols, and tests;
- merge time close to commit time;
- same author or committer;
- PR review comments discuss the exact hunk/symbol.

Guardrail: use reciprocal nearest-neighbor validation. The commit’s best PR should be PR X, and PR X’s best commit in the time/path window should be that commit. If not, output a candidate cluster, not one “true” PR.

Phrase as inference:

```text
Probable squash origin: PR #123, confidence 0.86, because net patch similarity is 0.94, paths match, and it merged 12 minutes before the squash commit.
```

Never phrase inferred squash matches as exact facts.

## Rebase merge and reused commits

Exact commit→PR may return multiple PRs. Prefer the PR that first introduced the commit into the queried branch and matches the target path/symbol. If multiple PRs reuse the same commit, return a cluster and label origin vs propagation.

## Cherry-pick and backport

Signals:

- same stable patch ID;
- similar commit message;
- message contains `cherry picked from commit`;
- different target branch;
- same issue or PR reference.

Output:

```text
Design rationale appears to originate in PR #123 on main; PR #456 is a backport to release/2.1.
```

## Reverts and re-applies

Signals:

- title/message starts with `Revert`;
- body references prior PR;
- inverse patch similarity;
- later PR touches same symbol and says `fix forward` or `reapply`.

Rule: a reverted PR cannot support a current constraint unless a later PR reintroduced it.

## Lost renames and moved code

Treat path as a feature, not identity.

Signals:

- `git diff-tree -M20% -C20%` / `-M50%` / `-M80%`;
- same blob SHA across paths;
- normalized content shingle similarity;
- same symbol fingerprint;
- same call graph neighborhood;
- directory majority move: many files moved from old_dir to new_dir in the same PR;
- review comment hunk remaps to current code by context.

## Mass refactor / formatting commits

Downweight commits with:

- huge file count;
- low semantic token delta;
- high whitespace-only ratio;
- titles like `format`, `prettier`, `rename`, `move`, `mechanical`, `cleanup`.

Prefer `.git-blame-ignore-revs` when available.

## Generated, vendor, lock, and snapshot files

Exclude or downweight unless the user explicitly asks or the generated file is the actual API surface.

Common indicators:

```text
node_modules/ vendor/ third_party/ dist/ build/ generated/ snapshots/
*.lock package-lock.json yarn.lock pnpm-lock.yaml Cargo.lock go.sum
```

## PR-less direct commits

If no PR exists, say so:

```text
No PR evidence found. The line appears to originate from direct commit abc123. Confidence in design intent is low.
```
