# FPF Skill Index Update Guide

Methodology for maintaining SKILL.md when the FPF specification changes.
Discovered by applying FPF to its own skill file — dog-fooding the framework.

## When to update

- New sections or sub-sections added to FPF
- Sections renamed, merged, or reorganized
- New FPF patterns introduced that serve a distinct thinking need
- Existing router entries found to misroute (validated against real usage)
- Description trigger phrases no longer match how users actually invoke FPF

Per B.3.4 (Evidence Decay), the SKILL.md carries epistemic debt whenever the spec
evolves and the skill file doesn't. The Section INDEX provides a structural fallback,
but a stale thinking-verb router silently degrades navigation quality.

## What to update (checklist)

### 1. Description field (YAML frontmatter)

The description decides WHETHER the skill triggers at all. It must include:
- What FPF does (capability)
- When to use it (trigger phrases the user might say)
- When NOT to use it (negative triggers to prevent false activation)

When adding new FPF capabilities, add corresponding trigger phrases.
Keep under 1024 characters. No XML angle brackets.

### 2. Use cases section

These are broad cognitive situations — "thinking accelerator" framing, not section lookups.
Each use case should be a problem a human recognizes, not an FPF-internal concept.

Ask: "Would a user who has never heard of FPF describe their problem this way?"
If yes, it's a good use case. If it requires FPF vocabulary to understand, it's too internal.

### 3. Thinking-verb router (Step 1 table)

This is the core navigation improvement. Each row maps a **thinking verb** to a starting point.

To add a new row:
1. Identify the thinking need the new FPF content serves (what does it help the user DO?)
2. Name it with a bold verb: **Decompose**, **Evaluate**, **Unify**, etc.
3. Point to the specific section AND sub-section (e.g., "08 Part C -> C.18 NQD")
4. Check for overlap with existing rows — merge if the thinking need is the same

To validate a row:
- Simulate a user query that should trigger this row
- Follow the path: does the `_index.md` of the target section lead to a useful sub-section?
- If the path dead-ends or leads somewhere unexpected, the row is wrong

Principles (from the FPF audit):
- **Strict Distinction (A.7)**: Each row should serve a distinct thinking need. If two rows feel interchangeable, they're probably a category error — find the real distinction or merge them.
- **Cognitive Elegance (P-1)**: Resist growing the router beyond ~20 entries. If it gets longer, some entries probably overlap. An agent pattern-matches against the table — more rows means slower matching and more ambiguity.
- **WLNK (B.3)**: One wrong row degrades trust in the whole router. Validate carefully.

### 4. Section INDEX table

Structural reference. Must stay in sync with actual `sections/` folders.

Each "When to use" cell should lead with a **bold thinking verb** so even the structural
table doubles as intent-based navigation. Pattern: `**Verb**: what's inside`.

When sections are added/removed:
1. Add/remove the row
2. Write a thinking-verb description
3. Check if the new section should also appear in the thinking-verb router (Step 1)

### 5. Composition guidance (Step 4)

Update if:
- New patterns create novel cross-section composition needs
- Users consistently struggle to synthesize findings from certain section combinations
- New category-error patterns are discovered (add to the A.7 check)

The natural synthesis order (decompose -> evaluate -> resolve) should remain stable
unless FPF's reasoning architecture fundamentally changes.

## How to validate (FPF self-audit)

After updating, run these checks against the FPF patterns that matter most for a navigation artifact:

| FPF Pattern | Check |
|---|---|
| **Bounded Context (A.1.1)** | Does the SKILL.md have clear entry/exit semantics? Does the router bridge user-intent context to FPF-spec context without collapsing them? |
| **Strict Distinction (A.7)** | Are use cases (admission) and router (navigation) still clearly separated? Does any row conflate two different thinking needs? |
| **Trust & Assurance (B.3)** | Can each router row be grounded in actual spec content? Would following the path produce a useful result? |
| **Multi-View (E.17)** | Does the router serve different user roles (engineer, manager, researcher) without being locked to one view? |
| **Epistemic Debt (B.3.4)** | Are there sections in the INDEX that aren't reachable from the router? If so, is that intentional (not every section needs a router entry) or an omission? |
| **Composition (B.1)** | If new sections are added, does Step 4 still give adequate synthesis guidance? Are there new cross-section patterns to document? |
| **Cognitive Elegance (P-1)** | Is the file still compact? Growth should be justified by navigation value, not completeness for its own sake. |

### 6. README files

After updating SKILL.md, sync both README.md and README-RU.md:
- Update the Sections table if sections were added, removed, or renamed
- Update the "How it works" / "Как это работает" description if the navigation approach changed
- Keep both language versions consistent with each other

README files are for humans on GitHub — they must reflect the current state of the skill.

## Process summary

```
1. Identify what changed in the FPF spec
2. For each change, ask: "What thinking need does this serve?"
3. Update the relevant SKILL.md component (description / use cases / router / INDEX)
4. Run the FPF self-audit (table above)
5. Test with simulated user queries
6. Update README.md and README-RU.md to match
```
