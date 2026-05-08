# Evaluation guide

Use this when validating whether the skill works on a repository.

## Benchmark cases

Create or find cases for:

- normal merge commit;
- squash merge;
- rebase merge;
- cherry-pick;
- backport;
- revert and reapply;
- file rename;
- directory rename;
- file split or merge;
- symbol rename;
- mass formatting commit;
- generated file;
- huge PR above API limits;
- PR-less direct commit;
- reused commit across PRs;
- closed-unmerged PR with useful review discussion.

## Test protocol

1. Select a known merged PR.
2. Hide its PR number from the agent.
3. Ask the agent why a specific line/symbol exists or whether a change is safe.
4. Check whether the skill returns the origin PR, related discussion, and correct risk.

## Metrics

- PR Recall@5
- main-origin PR MRR
- false association rate
- decision atom precision
- citation correctness
- risk classification accuracy
- unknown calibration
- API truncation detection accuracy
- latency p50/p95
- token cost per successful retrieval

Most important: minimize false high-confidence provenance. A conservative `UNKNOWN` is better than a confident but wrong story.
