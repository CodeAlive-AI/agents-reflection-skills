# Decision atoms

A decision atom is a compact, evidence-backed claim extracted from history. Use these to turn raw PR discussion into actionable context.

## Atom schema

```json
{
  "claim": "This null check preserves compatibility with legacy payloads.",
  "type": "compatibility_constraint",
  "scope": "src/user/deserializer.ts:readUser",
  "confidence": 0.84,
  "superseded": false,
  "evidence": [
    {
      "kind": "review_comment",
      "pr": 123,
      "url": "...",
      "why_relevant": "Comment is attached to the same hunk and discusses legacy payloads."
    }
  ]
}
```

## Types

- `constraint`
- `compatibility_constraint`
- `public_api_contract`
- `security_invariant`
- `performance_constraint`
- `concurrency_invariant`
- `migration_rule`
- `rejected_approach`
- `accepted_tradeoff`
- `test_requirement`
- `known_bug_or_workaround`
- `ownership_or_style_convention`
- `related_context`

## Extraction rules

1. Prefer explicit language: `must`, `should not`, `by design`, `compatibility`, `breaking`, `security`, `race`, `allocation`, `rejected`, `revert`, `flaky`, `migration`.
2. Distinguish facts from inferences.
3. Do not promote “related context” to “decision” unless the source supports it.
4. Mark stale evidence when a later revert, fix-forward, or superseding PR exists.
5. Include evidence links or exact PR/comment identifiers whenever possible.

## Confidence guide

High:
- direct review comment on the exact hunk/symbol;
- PR body states the design goal;
- linked issue describes the requirement;
- exact commit→PR plus matching discussion.

Medium:
- same symbol/path and relevant discussion, but no direct hunk comment.

Low:
- semantic match only;
- title-only match;
- old path with no lineage confirmation;
- generated file or mass-refactor origin.
