---
name: bug-fix-protocol
description: 8-step disciplined bug-fix protocol that treats every production bug as two failures — the code defect itself and the testing system that allowed it through. Use when fixing a production bug, investigating a regression, writing a post-mortem, or auditing a missed defect. Triggers on "fix this bug", "production bug", "regression test", "post-mortem", "test gap", "why did the tests miss this".
---

# Bug Fix Protocol

A bug fix is **two fixes in one**: fix the code, **and** fix the testing system that let the bug through. Skipping the second step means the same class of bug ships again.

The full protocol (philosophy, eight steps with examples, audit checklist, anti-patterns) lives in [`PROTOCOL.md`](PROTOCOL.md). Read it before applying.

## When to apply

Use this protocol whenever a defect reaches production, staging, or a customer environment. Do **not** use it for bugs caught locally during normal development — those are part of the writing process, not testing-system failures.

## The eight steps (summary)

1. **Analyze and reproduce requirements.** Understand exact actual vs expected behaviour; identify minimal repro path; ask the user before guessing on ambiguities.
2. **Write a failing test (red).** Encode the bug as a test that fails for the right reason. No code change yet.
3. **Trace root cause.** Walk the failing test back through the system. Stop at the smallest place that, if changed, makes the test pass.
4. **Apply the minimal fix.** Smallest possible change. No drive-by refactors.
5. **Verify green locally.** Failing test now passes; no other tests regressed.
6. **Run the full suite + lints + types.** Catch indirect regressions.
7. **Document the fix.** Commit message and PR description name the symptom, the root cause, and the fix in one sentence each.
8. **Audit the testing system (the most important step).** Ask: *which layer should have caught this, and why didn't it?* Then change that layer so it would catch the next instance — new test type, new fixture, new lint rule, new property test, new contract assertion. **A fix without step 8 is incomplete.**

## Output expectations

When applying the protocol, return:

- The repro test (red, then green).
- The minimal code fix.
- A one-paragraph step-8 audit naming the missed coverage layer and the change made to close the gap.

If step 8 produces "we couldn't have caught this," investigate further — that answer is almost always wrong, and accepting it is how the testing system stagnates.

## Reference

Full text: [`PROTOCOL.md`](PROTOCOL.md).
