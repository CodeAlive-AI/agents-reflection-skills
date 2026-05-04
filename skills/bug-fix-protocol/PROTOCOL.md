# Bug Fix Protocol

## Philosophy: the testing system is the primary quality guarantor

The testing system is the **safety net and quality guarantor** of our application. Our goal is to build a testing system that catches **100% of defects before they reach production**. Every layer — unit tests, integration tests, E2E tests, property-based tests, contract tests, visual-AI tests, symbolic verification — exists to make it impossible for a broken build to ship.

**If a bug reaches production, the root problem is the testing system, not the code.** Code bugs are inevitable — developers make mistakes, requirements shift, edge cases hide. A mature testing system anticipates this and catches defects before users see them. When it fails to do so, the testing system itself has a defect that must be diagnosed and fixed with the same rigor as any production bug.

This means every bug fix is **two fixes in one**:
1. Fix the code defect (steps 1–7 below).
2. Fix the testing system defect that allowed it through (step 8 — the most important step).

Over time, this discipline systematically eliminates blind spots and drives the testing system toward its ideal state: a complete, self-improving safety net where no class of bug can slip through twice.

---

Every bug fix follows these eight steps in order.

---

## 1. Analyze and reproduce requirements

Before touching code, think deeply about the bug:

- Understand the **exact** user-reported behavior vs expected behavior.
- Identify the **minimal reproduction path** (inputs, state, sequence of actions).
- If any detail is unclear or ambiguous, **ask the user** before proceeding. Do not guess.

## 2. Write a failing test (red)

Choose the test type using the feedback loop priority:

1. **Unit test** (preferred) — if the bug is in logic, hooks, services, or domain rules.
2. **Integration test** — if the bug spans multiple modules or requires real services.
3. **E2E test** (rare) — only when the bug is fundamentally cross-service, UI-interaction-based, or a core business process.

Write the test that **reproduces the bug** and confirm it **fails** (red). This test is the proof that the bug exists and will later prove the fix works.

## 3. Identify the real root cause

Do not stop at the surface symptom. Trace the failure to the **actual** root cause:

- Read the code path end-to-end.
- Check whether the symptom is caused by a deeper issue (wrong assumption, missing validation, stale state, race condition, incorrect data flow).
- The root cause is the thing that, once fixed, makes the class of bug impossible — not just the specific instance.

## 4. Design the proper fix

Think deeply about the **correct** fix, not just the quickest patch:

- Does the fix address the root cause or only the symptom?
- Does it introduce any regressions, side effects, or architectural debt?
- Is it consistent with existing patterns in the codebase?

**If the proper fix requires significant effort** (large refactor, architectural change, cross-cutting concern), **stop and tell the user**. Present:
- What the proper fix involves and why.
- A lighter alternative (if one exists) with its trade-offs.
- Let the user decide which path to take.

## 5. Apply the fix

Implement the chosen fix. Keep changes minimal and focused on the bug — do not mix in unrelated refactors or improvements.

## 6. Verify the fix (green)

Run the reproduction test from step 2 and confirm it **passes** (green). Also run the broader test suite for affected areas to ensure no regressions.

## 7. Analyze consequences and related issues

Go deeper than the immediate fix:

- **Related bugs**: Could the same root cause manifest elsewhere? Check for similar patterns, shared code paths, or analogous logic.
- **Data impact**: Could existing data be corrupted or inconsistent due to this bug? If so, flag it.
- **Downstream effects**: Are there other features, components, or services that depend on the buggy behavior (possibly relying on the wrong output)?

If you find related issues, suggest fixing them (as separate, tracked work if non-trivial).

## 8. Audit the testing system

**This is the most important step in the entire protocol.** The code fix (steps 1–7) resolves the symptom; this step fixes the underlying failure — the gap in the safety net that let the bug through. Without this step, the testing system remains broken and the same class of defect will reach users again.

The bug reached the user, which means the testing system has a blind spot. Treat this as a **testing system bug** with the same severity as the original defect.

### 8a. Why did our tests miss this?

Analyze specifically:

- Was there **no test** covering this code path? Why not?
- Was there a test, but it **didn't assert the right thing**? (e.g., checked status code but not response body)
- Was the test **using mocks that hid the real behavior**? (mock fidelity gap)
- Was the scenario **outside the parameter space** our tests explore? (missing edge case, missing pairwise combination, missing property)
- Was it a **cross-layer issue** that unit tests can't catch by design? (integration/E2E gap)
- Was it a **state-dependent bug** not covered by our state machine coverage?
- Is the affected code in a **coverage exclusion** that should be reconsidered?
- Does the **criticality classification** underrate this file?

### 8b. Suggest testing system improvements

Based on the analysis, propose concrete improvements:

- New tests (unit, integration, E2E, property-based, pairwise) that would have caught this.
- Criticality classification updates if the file risk was underrated.
- Traceability updates if the requirement was missing or under-covered.
- New runtime contracts if the function should have had postconditions.
- API contract updates if the bug was a shape mismatch between consumer and provider.
- Mock fidelity updates if mocks diverged from reality.
- Coverage exclusion changes if an excluded category should be covered.
- New pairwise models if the bug was a parameter interaction.

### 8c. Scan for similar undetected bugs

Proactively search the codebase for the **same pattern** that caused this bug:

- Grep for similar code constructs, assumptions, or anti-patterns.
- Check if sibling modules/functions have the same flaw.
- Report findings so they can be fixed before users hit them.

---

## Rationale

A bug that reaches a user represents two failures: the code defect itself, and the testing system's failure to catch it. **The testing system failure is the more important one to fix.** Code defects are one-off; a gap in the testing system is a systemic weakness that will let other defects through.

Fixing only the code defect leaves the safety net broken. By auditing and improving the testing system with every bug fix, we systematically eliminate blind spots, strengthen coverage where it matters, and drive toward our goal: a testing system that catches 100% of issues before they reach production. Each bug fix makes the safety net tighter, and the same class of bug becomes impossible to miss in the future.
