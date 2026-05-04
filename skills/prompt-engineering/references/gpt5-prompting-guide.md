# GPT-5.2 Prompting Guide (OpenAI)

Source: [openai-cookbook/examples/gpt-5/gpt-5-2_prompting_guide.ipynb](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5-2_prompting_guide.ipynb)

## Key Behavioral Traits of Advanced Models

- **More deliberate scaffolding**: Builds clearer plans and intermediate structure by default; benefits from explicit scope and verbosity constraints
- **Generally lower verbosity**: More concise and task-focused, though still prompt-sensitive
- **Stronger instruction adherence**: Less drift from user intent; improved formatting
- **Tool efficiency trade-offs**: May take additional tool actions; can be optimized via prompting
- **Conservative grounding bias**: Favors correctness and explicit reasoning; ambiguity handling improves with clarification prompts

## Verbosity Control — Full Specification

```xml
<output_verbosity_spec>
- Default: 3–6 sentences or ≤5 bullets for typical answers.
- For simple "yes/no + short explanation" questions: ≤2 sentences.
- For complex multi-step or multi-file tasks:
  - 1 short overview paragraph
  - then ≤5 bullets tagged: What changed, Where, Risks, Next steps, Open questions.
- Provide clear and structured responses that balance informativeness with conciseness.
- Break down information into digestible chunks and use formatting like lists, paragraphs and tables.
- Avoid long narrative paragraphs; prefer compact bullets and short sections.
- Do not rephrase the user's request unless it changes semantics.
</output_verbosity_spec>
```

## Scope Drift Prevention — Full Specification

```xml
<design_and_scope_constraints>
- Explore any existing design systems and understand it deeply.
- Implement EXACTLY and ONLY what the user requests.
- No extra features, no added components, no UX embellishments.
- Style aligned to the design system at hand.
- Do NOT invent colors, shadows, tokens, animations, or new UI elements, unless requested or necessary.
- If any instruction is ambiguous, choose the simplest valid interpretation.
</design_and_scope_constraints>
```

## Ambiguity & Hallucination Mitigation — Full Specification

```xml
<uncertainty_and_ambiguity>
- If the question is ambiguous or underspecified, explicitly call this out and:
  - Ask up to 1–3 precise clarifying questions, OR
  - Present 2–3 plausible interpretations with clearly labeled assumptions.
- When external facts may have changed recently and no tools are available:
  - Answer in general terms and state that details may have changed.
- Never fabricate exact figures, line numbers, or external references when uncertain.
- Prefer language like "Based on the provided context…" instead of absolute claims.
</uncertainty_and_ambiguity>
```

## High-Risk Self-Check

```xml
<high_risk_self_check>
Before finalizing an answer in legal, financial, compliance, or safety-sensitive contexts:
- Briefly re-scan your own answer for:
  - Unstated assumptions,
  - Specific numbers or claims not grounded in context,
  - Overly strong language ("always," "guaranteed," etc.).
- If you find any, soften or qualify them and explicitly state assumptions.
</high_risk_self_check>
```

## Long-Context Handling — Full Specification

```xml
<long_context_handling>
- For inputs longer than ~10k tokens (multi-chapter docs, long threads, multiple PDFs):
  - First, produce a short internal outline of the key sections relevant to the user's request.
  - Re-state the user's constraints explicitly (e.g., jurisdiction, date range, product, team).
  - In your answer, anchor claims to sections ("In the 'Data Retention' section…").
- If the answer depends on fine details (dates, thresholds, clauses), quote or paraphrase them.
</long_context_handling>
```

## Agentic User Updates — Full Specification

```xml
<user_updates_spec>
- Send brief updates (1–2 sentences) only when:
  - You start a new major phase of work, or
  - You discover something that changes the plan.
- Avoid narrating routine tool calls ("reading file…", "running tests…").
- Each update must include at least one concrete outcome ("Found X", "Confirmed Y", "Updated Z").
- Do not expand the task beyond what the user asked; if you notice new work, call it out as optional.
</user_updates_spec>
```

## Tool-Calling Rules — Full Specification

```xml
<tool_usage_rules>
- Prefer tools over internal knowledge whenever:
  - You need fresh or user-specific data (tickets, orders, configs, logs).
  - You reference specific IDs, URLs, or document titles.
- Parallelize independent reads (read_file, fetch_record, search_docs) when possible.
- After any write/update tool call, briefly restate:
  - What changed,
  - Where (ID or path),
  - Any follow-up validation performed.
</tool_usage_rules>
```

## Structured Extraction — Full Specification

```xml
<extraction_spec>
You will extract structured data from tables/PDFs/emails into JSON.

- Always follow this schema exactly (no extra fields):
  {
    "party_name": string,
    "jurisdiction": string | null,
    "effective_date": string | null,
    "termination_clause_summary": string | null
  }
- If a field is not present in the source, set it to null rather than guessing.
- Before returning, quickly re-scan the source for any missed fields and correct omissions.
</extraction_spec>
```

For multi-file extractions: serialize per-document results separately and include stable IDs (filename, contract title, page range).

## Compaction (Extending Effective Context)

Compaction performs a loss-aware compression pass over prior conversation state, returning encrypted, opaque items that preserve task-relevant information while dramatically reducing token footprint.

**When to use:**
- Multi-step agent flows with many tool calls
- Long conversations where earlier turns must be retained
- Iterative reasoning beyond the maximum context window

**Best practices:**
- Monitor context usage and plan ahead
- Compact after major milestones (tool-heavy phases), not every turn
- Keep prompts functionally identical when resuming to avoid behavior drift
- Treat compacted items as opaque; don't parse or depend on internals

**OpenAI API endpoint:**
```
POST https://api.openai.com/v1/responses/compact
```

**Code example:**
```python
from openai import OpenAI
import json

client = OpenAI()

response = client.responses.create(
    model="gpt-5.2",
    input=[{"role": "user", "content": "write a very long poem about a dog."}]
)

output_json = [msg.model_dump() for msg in response.output]

compacted_response = client.responses.compact(
    model="gpt-5.2",
    input=[
        {"role": "user", "content": "write a very long poem about a dog."},
        output_json[0]
    ]
)

print(json.dumps(compacted_response.model_dump(), indent=2))
```

## Reasoning Effort Tuning

GPT-5-class models support a `reasoning_effort` parameter: `none | minimal | low | medium | high | xhigh`.

**Migration mapping:**

| Source Model | Target reasoning_effort | Notes |
|---|---|---|
| GPT-4o / GPT-4.1 | `none` | Fast/low-deliberation by default; increase only if evals regress |
| GPT-5 | Same except `minimal` → `none` | Default for GPT-5 is `medium` |
| GPT-5.1 / GPT-5.2 | Same value | Default is `none`; adjust after evals |

## Prompt Migration Methodology

1. **Switch models, don't change prompts yet** — test the model change alone
2. **Pin reasoning_effort** — match the prior model's latency/depth profile
3. **Run evals for a baseline** — if results look good, ship
4. **If regressions, tune the prompt** — use targeted constraints (verbosity/format/schema, scope discipline)
5. **Re-run evals after each small change** — bump reasoning_effort one notch or make incremental prompt tweaks, then re-measure

## Web Research — Full Agent Prompt

### Core Mission
Answer the user's question fully with enough evidence that a skeptical reader can trust it. Never invent facts. If you can't verify something, say so clearly.

### Search Methodology
- Start with multiple targeted searches
- Use parallel searches when helpful
- Don't rely on a single query
- Begin broad enough to capture main answer and likely interpretations
- Add targeted follow-up searches to fill gaps and resolve disagreements
- Keep iterating until additional searching won't materially change the answer
- Stop only when: you answered every subpart / found concrete examples / found sufficient sources

### Citation Rules
- Include citations after each paragraph with non-obvious web-derived claims
- Prioritize more recent events for news queries
- Compare publish dates of sources and event dates

### Writing Guidelines
- Be direct: start answering immediately
- Be comprehensive: answer every part of the query
- Use simple language: full sentences, short words, concrete verbs, active voice
- Use readable formatting: Markdown, bullets, tables for comparisons
- Do NOT add follow-up questions unless explicitly asked

### Ambiguity Handling (Without Asking Questions)
Never ask clarifying questions unless the user explicitly asks. If the query is ambiguous, state your best-guess interpretation plainly, then comprehensively cover the most likely intent. If multiple intents, cover each one fully.

### Completeness Pass
Before finalizing: Did I answer every subpart? / Did each section include explanation + at least one concrete detail? / Did I include tradeoffs/decision criteria where relevant?

```xml
<web_search_rules>
- Act as an expert research assistant; default to comprehensive, well-structured answers.
- Prefer web research over assumptions whenever facts may be uncertain or incomplete.
- Research all parts of the query, resolve contradictions, and follow important implications.
- Do not ask clarifying questions; instead cover all plausible user intents.
- Write clearly using Markdown (headers, bullets, tables); define acronyms and use concrete examples.
</web_search_rules>
```
