# Output schema

Use this when producing machine-readable output or when the user asks for a formal report.

## JSON report

```json
{
  "scope": {
    "repo": "OWNER/REPO",
    "paths": ["src/foo.ts"],
    "line_ranges": [{"path": "src/foo.ts", "start": 10, "end": 30}],
    "symbols": ["Foo.bar"],
    "question": "Can I remove this check?"
  },
  "evidence_completeness": {
    "local_git": "complete|partial|not_run",
    "github_prs": "complete|partial|not_run",
    "review_comments": "complete|partial|not_run",
    "api_truncation_possible": false,
    "notes": []
  },
  "relevant_prs": [
    {
      "number": 123,
      "title": "Preserve legacy behavior",
      "url": "https://github.com/OWNER/REPO/pull/123",
      "relation": "exact_commit_association|probable_squash_origin|symbol_lineage|search_candidate|backport|revert|unknown",
      "score": 0.91,
      "confidence": "high|medium|low",
      "why_relevant": ["introduced blamed line", "review comment mentions compatibility"],
      "warnings": []
    }
  ],
  "decision_atoms": [
    {
      "claim": "The check is a compatibility guard.",
      "type": "compatibility_constraint",
      "scope": "src/foo.ts:Foo.bar",
      "confidence": 0.84,
      "superseded": false,
      "evidence": [{"kind": "review_comment", "pr": 123, "url": "..."}]
    }
  ],
  "risk": {
    "level": "low|medium|high|unknown",
    "confidence": 0.0,
    "recommended_action": "proceed|modify_plan|ask_human|do_not_change"
  },
  "unknowns": [],
  "plan_impact": []
}
```

## Markdown history note

```markdown
## History note

Scope inspected: [repo, path, lines, symbol]

Relevant evidence:
- PR #[number] — [title] — relation: [relation], confidence: [level]
  - Why: [short reasons]
  - Evidence: [comment/review/commit references]

Decision atoms:
- [type] [claim] — evidence: [reference]

Risk: [level]
Confidence: [0.00-1.00]
Unknowns: [list]
Plan impact: [proceed/modify/ask human/do not change]
```
