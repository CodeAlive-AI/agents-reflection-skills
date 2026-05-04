# Prompt Audit Checklist

Structured checklist for reviewing any prompt. Each dimension maps to reference files for deeper guidance.

## How to Use

1. Read the prompt fully before scoring
2. Walk through each dimension — mark issues found
3. For each issue, note severity (Critical / Warning / Suggestion) and cite the fix
4. Produce a report: issues table + rewritten prompt (or targeted fix suggestions)

Severity guide:
- **Critical** — will cause failures, security holes, or systematic errors in production
- **Warning** — degraded quality, brittleness, or maintenance burden
- **Suggestion** — would improve clarity or robustness but not blocking

---

## 1. Clarity & Specificity

Check for ambiguity, missing constraints, and vague objectives.

| Check | What to Look For | Severity | Fix Reference |
|-------|-----------------|----------|---------------|
| Task definition | Is the task explicitly stated? Could someone misinterpret what's being asked? | Critical | [failure-taxonomy.md](failure-taxonomy.md) #1 Ambiguous prompts |
| Success criteria | Does the prompt define what a correct output looks like? | Critical | [mistakes-hallucinations.md](mistakes-hallucinations.md) — "Ambiguous Objectives" |
| Audience & purpose | Is it clear who the output is for and why? | Warning | [failure-taxonomy.md](failure-taxonomy.md) #2 Under-specification |
| Output format | Is the expected format (JSON, bullets, prose, length) specified? | Warning | SKILL.md "Control Output Shape" |
| Conflicting constraints | Are there contradictory requirements (e.g., "be concise" + "be exhaustive")? | Critical | [failure-taxonomy.md](failure-taxonomy.md) #3 Over-specification, #11 Instruction conflicts |
| Constraint priority | If multiple constraints exist, is precedence clear? | Warning | [mistakes-structure.md](mistakes-structure.md) — "Mixed Instruction Layers" |

## 2. Structure & Formatting

Check for structural anti-patterns and prompt smells.

| Check | What to Look For | Severity | Fix Reference |
|-------|-----------------|----------|---------------|
| Section separation | Are instructions, context, data, and examples clearly separated (e.g., XML tags)? | Warning | SKILL.md "Structure with XML Tags" |
| Monolithic prompt | Is a single prompt doing multiple complex tasks that should be chained? | Warning | [mistakes-structure.md](mistakes-structure.md) — "Monolithic Prompting" smell |
| Mixed instruction layers | Are role, tone, format, and reasoning requirements tangled in the same sentence? | Warning | [mistakes-structure.md](mistakes-structure.md) — "Mixed Instruction Layers" smell |
| Negative instruction bias | Does the prompt rely heavily on "don't do X" instead of "do Y"? | Suggestion | [mistakes-structure.md](mistakes-structure.md) — "Negative Instruction Bias" smell |
| Overloaded context | Is there excessive backstory, edge-case lists, or irrelevant detail? | Warning | [mistakes-structure.md](mistakes-structure.md) — "Overloaded Context" smell |
| Format brittleness | Has the prompt been tested with alternative formatting (spacing, casing, ordering)? | Warning | [mistakes-structure.md](mistakes-structure.md) — "Formatting Fragility" |

## 3. Safety & Security

Check for injection vectors, leakage risks, and privilege issues.

| Check | What to Look For | Severity | Fix Reference |
|-------|-----------------|----------|---------------|
| Control/data separation | Is untrusted input (user text, retrieved docs, tool outputs) clearly delimited from instructions? | Critical | [failure-taxonomy.md](failure-taxonomy.md) — Control-plane vs Data-plane |
| Secrets in prompt | Does the system prompt contain API keys, credentials, internal limits, or architecture details? | Critical | [mistakes-security.md](mistakes-security.md) — "System Prompt Leakage" |
| Injection resilience | Could a user embed "ignore previous instructions" in their input and affect behavior? | Critical | [mistakes-security.md](mistakes-security.md) — "Direct Prompt Injection" |
| External data trust | Are retrieved documents, web pages, or tool outputs treated as potentially adversarial? | Critical | [mistakes-security.md](mistakes-security.md) — "Indirect Prompt Injection" |
| Tool permissions | If tools are available, does the prompt enforce least-privilege access? | Critical | [failure-taxonomy.md](failure-taxonomy.md) — Prioritized Action Items |
| Output validation | Are LLM outputs validated before executing actions (DB queries, API calls, file ops)? | Critical | [mistakes-security.md](mistakes-security.md) — "Output Validation" |
| System prompt leak guard | Does the prompt include instructions to not reveal its own contents? | Warning | [mistakes-security.md](mistakes-security.md) — "System Prompt Hardening" |

## 4. Hallucination & Factuality

Check for patterns that trigger confabulation or ungrounded claims.

| Check | What to Look For | Severity | Fix Reference |
|-------|-----------------|----------|---------------|
| Role framing | Is there a persona/role with explicit operational boundaries? | Warning | [mistakes-hallucinations.md](mistakes-hallucinations.md) — "No role framing" |
| Grounding instructions | Does the prompt anchor the model to provided context ("Based on the provided data...")? | Warning | [mistakes-hallucinations.md](mistakes-hallucinations.md) — Prevention #6 |
| Citation demand without sources | Does the prompt ask for citations/references without providing source material? | Critical | [failure-taxonomy.md](failure-taxonomy.md) #10 Hallucination triggers |
| Uncertainty handling | Does the prompt instruct what to do when uncertain (ask, abstain, flag)? | Warning | SKILL.md "Handle Ambiguity Explicitly" |
| Verification separation | If the prompt asks to both verify AND explain, are these separated into steps? | Warning | [mistakes-hallucinations.md](mistakes-hallucinations.md) — "Logical Failures in Verification Tasks" |
| Overloaded reasoning | Does a single instruction combine tone + format + multi-step reasoning? | Warning | [mistakes-hallucinations.md](mistakes-hallucinations.md) — "Overloaded prompts" |

## 5. Context Management

Check for context window issues, especially in long prompts or RAG systems.

| Check | What to Look For | Severity | Fix Reference |
|-------|-----------------|----------|---------------|
| Critical info placement | Are key instructions at the beginning or end, not buried in the middle? | Warning | [mistakes-context.md](mistakes-context.md) — "Strategic Information Placement" |
| Context size | Is the total context (system + retrieved + user) appropriate for the task? | Warning | [mistakes-context.md](mistakes-context.md) — "Quick Decision Guide" |
| RAG document count | If using RAG, are retrieved documents limited to high-signal items (not dumping 50+)? | Warning | [mistakes-context.md](mistakes-context.md) — "RAG Over-Retrieval" |
| Re-grounding | For inputs >10K tokens, does the prompt include re-grounding instructions? | Warning | SKILL.md "Long-Context Grounding" |
| Middle-buried directives | Are any safety rules, format constraints, or key requirements in the middle of a long prompt? | Critical | [mistakes-context.md](mistakes-context.md) — "Lost in the Middle" |
| Memory strategy | For long-horizon agentic tasks, is there a memory/compaction strategy? | Suggestion | [mistakes-context.md](mistakes-context.md) — "Memory Tools & Context Compaction" |

## 6. Maintainability & Debt

Check for patterns that create technical debt or operational risk.

| Check | What to Look For | Severity | Fix Reference |
|-------|-----------------|----------|---------------|
| Hardcoded values | Are business rules, thresholds, or config values hardcoded instead of templated? | Warning | [mistakes-debt.md](mistakes-debt.md) — "Prompt Debt" |
| Regenerated logic | Is the LLM regenerating logic that a deterministic function could handle? | Warning | [mistakes-debt.md](mistakes-debt.md) — "The Token Tax" |
| Model version pinning | Is the prompt designed for a specific model version, or will it break on updates? | Suggestion | [mistakes-debt.md](mistakes-debt.md) — Prevention #3 |
| Framework coupling | Is the prompt tightly coupled to a specific orchestration framework? | Suggestion | [mistakes-debt.md](mistakes-debt.md) — "Framework Debt" |
| Testability | Can the prompt's behavior be evaluated with automated tests? | Warning | [evaluation-redteaming.md](evaluation-redteaming.md) — "CI Workflow" |
| Reproducibility | Is everything documented (model, temperature, prompt text, library versions)? | Suggestion | [mistakes-structure.md](mistakes-structure.md) — "The Reproducibility Crisis" |

## 7. Model-Specific Fit

Check if the prompt uses patterns appropriate for the target model.

| Check | What to Look For | Fix Reference |
|-------|-----------------|---------------|
| Claude-specific | Using deprecated prefill? Missing `effort` param? Tool overtriggering? | [claude-family-prompting.md](claude-family-prompting.md) |
| GPT-5-specific | Using correct `reasoning_effort` defaults? Aware of instruction conflict sensitivity? | [gpt5-family-prompting.md](gpt5-family-prompting.md) |
| Gemini-specific | Temperature set to 1.0? Constraints placed at end of prompt? Using `thinking_budget`? | [gemini3-family-prompting.md](gemini3-family-prompting.md) |
| Cross-model portability | If used across models, has migration checklist been followed? | SKILL.md "Prompt Migration Checklist" |

## 8. Evaluation Readiness

Check if the prompt is set up for testing and monitoring.

| Check | What to Look For | Severity | Fix Reference |
|-------|-----------------|----------|---------------|
| Eval criteria defined | Are pass/fail criteria clear enough to write automated tests? | Warning | [evaluation-redteaming.md](evaluation-redteaming.md) — "CI Workflow" |
| Adversarial test cases | Have edge cases and adversarial inputs been considered? | Warning | [failure-taxonomy.md](failure-taxonomy.md) — "Prioritized Action Items" |
| Schema enforcement | If structured output is expected, is there a schema for validation? | Suggestion | SKILL.md "Structured Extraction" |
| Monitoring hooks | In production, are there signals for drift, safety violations, or cost spikes? | Suggestion | [evaluation-redteaming.md](evaluation-redteaming.md) — "Observability" |

---

## Audit Report Template

```markdown
# Prompt Audit Report

**Prompt:** [name/description]
**Target model:** [model name + version]
**Use case:** [brief description]

## Issues Found

| # | Dimension | Check | Severity | Issue | Suggested Fix |
|---|-----------|-------|----------|-------|---------------|
| 1 | ...       | ...   | Critical | ...   | ...           |

## Summary

- Critical: N
- Warning: N
- Suggestion: N

## Recommended Changes

[Rewritten prompt or targeted fix list]
```
