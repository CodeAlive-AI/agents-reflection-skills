# GitHub CLI (`gh`) reference

Use this when `scripts/history_context.py` fails, when manual inspection is needed, or when you need to verify a candidate PR. All GitHub access in this skill is performed via the `gh` CLI — never via direct HTTP calls to `api.github.com`. `gh` handles auth, pagination, caching, and rate-limit retries.

## Contents

- [Prerequisites](#prerequisites)
- [Commit → PR association](#commit--pr-association)
- [PR metadata](#pr-metadata)
- [PR files](#pr-files)
- [PR commits](#pr-commits)
- [PR reviews](#pr-reviews)
- [Inline review comments](#inline-review-comments)
- [General PR conversation comments](#general-pr-conversation-comments)
- [Search for candidate PRs](#search-for-candidate-prs)
- [Helpful `gh` patterns](#helpful-gh-patterns)
- [Failure handling](#failure-handling)

## Prerequisites

```bash
gh auth status
gh repo view --json nameWithOwner --jq .nameWithOwner
git rev-parse --show-toplevel
```

## Commit → PR association

```bash
gh api \
  -H "Accept: application/vnd.github+json" \
  repos/OWNER/REPO/commits/SHA/pulls \
  --paginate --slurp
```

Use this first, but remember that squashed merges, direct pushes, and reused commits may need fuzzy provenance.

## PR metadata

```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER
```

Useful fields:

```text
number, title, body, state, merged_at, merge_commit_sha,
base.ref, base.sha, head.ref, head.sha, user.login, html_url
```

## PR files

```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER/files --paginate --slurp
```

Useful fields:

```text
filename, previous_filename, status, patch, additions, deletions, changes
```

If `patch` is absent or the file count is huge, mark diff evidence incomplete and compute local diffs if possible.

## PR commits

```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER/commits --paginate --slurp
```

## PR reviews

```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER/reviews --paginate --slurp
```

Reviews carry state such as `APPROVED`, `CHANGES_REQUESTED`, `COMMENTED`, plus review body and author.

## Inline review comments

```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments --paginate --slurp
```

Useful fields:

```text
path, diff_hunk, body, line, original_line,
start_line, original_start_line, side, start_side,
commit_id, original_commit_id, user.login, html_url
```

Treat these comments as hunk/symbol evidence, not merely old-path evidence.

## General PR conversation comments

Every PR is also an issue, so fetch conversation comments via issue comments:

```bash
gh api repos/OWNER/REPO/issues/PR_NUMBER/comments --paginate --slurp
```

## Search for candidate PRs

```bash
gh api -X GET search/issues \
  -f q='repo:OWNER/REPO is:pr is:merged "SomeSymbol" compatibility' \
  -F per_page=20
```

Search is background evidence only. Do not make high-confidence claims from search results alone.

## Helpful `gh` patterns

```bash
# Compact PR view
gh pr view PR_NUMBER --json number,title,body,author,mergedAt,mergeCommit,files,commits,reviews,url

# Use cache for repeated reads
gh api repos/OWNER/REPO/pulls/PR_NUMBER --cache 1h
```

## Failure handling

- Auth failure: run `gh auth status`; do not attempt interactive login unless the user explicitly asks.
- 404: verify repo slug and token permissions.
- Empty commit→PR: try anomaly handling; do not conclude “no PR” until checking squash/search/path evidence.
- Very large output: write JSON to a file and read only relevant slices.
