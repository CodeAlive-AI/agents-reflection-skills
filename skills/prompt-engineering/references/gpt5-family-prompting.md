# GPT-5 Family Prompting Guide

Covers GPT-5, GPT-5.1, GPT-5.2, GPT-5.4, and GPT-5.5. Based on official OpenAI Cookbook and developer-docs prompting guides.

Sources:
- [GPT-5 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide)
- [GPT-5.1 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide)
- [GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide)
- [GPT-5.4 / GPT-5.5 Prompt Guidance (developers.openai.com)](https://developers.openai.com/api/docs/guides/prompt-guidance)
- [Prompt Personalities Cookbook](https://developers.openai.com/cookbook/examples/gpt-5/prompt_personalities)

## Model Comparison

| Aspect | GPT-5 | GPT-5.1 | GPT-5.2 | GPT-5.4 | GPT-5.5 |
|--------|-------|---------|---------|---------|---------|
| Default reasoning_effort | `medium` | `medium` | `none` | `none` (action) / `medium` (research) | Task-driven; treat as last-mile knob |
| Reasoning levels | low/medium/high + `minimal` | low/medium/high + `none` | none/minimal/low/medium/high/`xhigh` | none/low/medium/high/`xhigh` | none/low/medium/high/`xhigh` |
| Key strength | Agentic eagerness control | Calibrated token consumption | Enterprise accuracy & instruction following | Long-running autonomy, evidence-rich synthesis, batched tool calls | Outcome-first prompts, default-direct personality, steerable formatting |
| Verbosity | Steerable | Can be excessively concise | Concise by default, prompt-sensitive | More structured by default; may overuse bullets | `text.verbosity` API control (default `medium`); steerable via prompt |
| Tool calling | Improved vs GPT-4 | Named tools (apply_patch, shell) | Best structured reasoning & grounding | Dependency-aware, parallel; weak early tool routing | Inherits 5.4 tooling; `phase` field for commentary vs final answer |
| Compaction / `phase` | — | — | Compaction API | Compaction + `phase` field | Compaction + `phase` field |
| API | Responses API + Chat Completions | Responses API (preferred) | Responses API (preferred) | Responses API (`previous_response_id`, `phase`) | Responses API (`previous_response_id`, `phase`, `text.verbosity`) |

## Reasoning Effort Parameter

Controls thinking depth before the final answer.

```python
response = client.responses.create(
    model="gpt-5.2",
    input="Your prompt here",
    reasoning={"effort": "medium"}
)
```

| Level | Use Case | Notes |
|-------|----------|-------|
| `none` | Formatting, classification, simple Q&A | No reasoning tokens; similar to GPT-4.1/4o. Supports hosted tools (web search, file search) |
| `minimal` | Latency-sensitive; GPT-4.1 migration | Fastest reasoning mode. Performance varies more with prompt quality |
| `low` | Simple straightforward tasks | Speed-oriented |
| `medium` | General purpose (default for GPT-5) | Balanced |
| `high` | Complex multi-step reasoning | Accuracy over speed |
| `xhigh` | Hardest problems (GPT-5.2 only) | Maximum depth |

### Tips for `minimal` / `none` reasoning

When reasoning is minimal, compensate with explicit prompt structure:
- Add brief explanation summarizing thought process at answer start
- Write thorough, descriptive tool-calling preambles
- Maximize disambiguation of tool instructions
- Add explicit agentic persistence reminders
- Prompt planning at task beginning

```
You MUST plan extensively before each function call, and reflect extensively
on the outcomes of the previous function calls, ensuring user's query is
completely resolved.
```

### Migration Mapping

| Source Model | Target → GPT-5.2 | Notes |
|---|---|---|
| GPT-4o / GPT-4.1 | `none` | Fast/low-deliberation; increase only if evals regress |
| GPT-5 | Same, except `minimal` → `none` | GPT-5 default is `medium` |
| GPT-5.1 / GPT-5.2 | Same value | GPT-5.2 default is `none` |

### GPT-5.4 / 5.5 — Reasoning as a Last-Mile Knob

For 5.4 and 5.5, OpenAI explicitly recommends treating reasoning effort as a *last-mile* tuning knob, not the primary lever for quality. Before raising reasoning effort, first add:

- `<completeness_contract>` (see below)
- `<verification_loop>`
- `<tool_persistence_rules>`

Recommended starting points for migrations to GPT-5.4 / 5.5:

| Current setup | Suggested start | Notes |
|---|---|---|
| `gpt-5.2` | Match current effort | Preserve latency/quality first, then tune. |
| `gpt-5.3-codex` | Match current effort | Coding workflows: keep effort the same. |
| `gpt-4.1` / `gpt-4o` | `none` | Keep snappy; raise only if evals regress. |
| Research-heavy assistants | `medium` or `high` | Pair with explicit research multi-pass and citation gating. |
| Long-horizon agents | `medium` or `high` | Pair with tool persistence and completeness accounting. |
| Execution-heavy (extraction, triage) | `none` | Often sufficient on 5.4/5.5 with a strong output contract. |

## Agentic Eagerness Control

GPT-5 is trained to operate along the full control spectrum. Steer via prompts.

### Less Eager (Precise, Fast)

```xml
<context_gathering>
Goal: Get enough context fast. Parallelize discovery and stop as soon as you can act.

Method:
- Start broad, then fan out to focused subqueries.
- In parallel, launch varied queries; read top hits per query.
- Avoid over-searching. If needed, run targeted searches in one parallel batch.

Early stop criteria:
- You can name exact content to change.
- Top hits converge (~70%) on one area/path.

Loop:
- Batch search → minimal plan → complete task.
- Search again only if validation fails or new unknowns appear.
</context_gathering>
```

### More Eager (Autonomous, Thorough)

```xml
<persistence>
- You are an agent — keep going until the user's query is completely resolved.
- Only terminate your turn when the problem is solved.
- Never stop when you encounter uncertainty — research or deduce the most
  reasonable approach and continue.
- Do not ask the human to confirm assumptions — decide what is most reasonable,
  proceed, and document for the user's reference after finishing.
</persistence>
```

### Fixed Tool Call Budget

```xml
<context_gathering>
- Search depth: very low
- Bias strongly towards providing a correct answer as quickly as possible.
- Usually, an absolute maximum of 2 tool calls.
- If you need more time, update the user with findings and open questions.
</context_gathering>
```

## Verbosity Control

### API Parameter

GPT-5+ supports a `verbosity` API parameter controlling final answer length (not thinking length). Supports natural-language overrides in prompts for context-specific deviations.

### Prompt-Level Control

```xml
<output_verbosity_spec>
- Default: 3–6 sentences or ≤5 bullets for typical answers.
- Simple "yes/no + short explanation" questions: ≤2 sentences.
- Complex multi-step or multi-file tasks:
  - 1 short overview paragraph
  - then ≤5 bullets: What changed, Where, Risks, Next steps, Open questions.
- Avoid long narrative paragraphs; prefer compact bullets and short sections.
- Do not rephrase the user's request unless it changes semantics.
</output_verbosity_spec>
```

### Coding Agent Verbosity (GPT-5.1 Pattern)

```xml
<final_answer_formatting>
- Tiny/small change (≤~10 lines): 2–5 sentences or ≤3 bullets. No headings.
- Medium change (single area / few files): ≤6 bullets or 6–10 sentences.
  At most 1–2 short snippets (≤8 lines each).
- Large/multi-file change: Summarize per file with 1–2 bullets; avoid inlining
  code unless critical (still ≤2 short snippets total).
- Never include before/after pairs, full method bodies, or scrolling code blocks.
- No build/lint/test logs unless requested or blocking.
</final_answer_formatting>
```

## Tool Calling Patterns

### Tool Preambles (GPT-5+)

GPT-5 is trained to provide upfront plans and progress updates. Steer their frequency and style:

```xml
<tool_preambles>
- Begin by rephrasing the user's goal clearly before calling any tools.
- Outline a structured plan detailing each logical step.
- As you execute, narrate each step succinctly and sequentially.
- Finish by summarizing completed work distinctly from upfront plan.
</tool_preambles>
```

### Tool Usage Rules

```xml
<tool_usage_rules>
- Prefer tools over internal knowledge for fresh or user-specific data.
- Parallelize independent reads (read_file, fetch_record, search_docs).
- After write/update calls, restate: what changed, where (ID/path), validation performed.
</tool_usage_rules>
```

### Named Tools (GPT-5.1+)

GPT-5.1 introduced named tool types: `apply_patch` and `shell`. Using named tools decreased apply_patch failure rates by 35%.

```python
response = client.responses.create(
    model="gpt-5.1",
    input=RESPONSE_INPUT,
    tools=[{"type": "apply_patch"}]
)
```

### Parallel Tool Calling

Issue multiple tool calls simultaneously for speed. Encourage explicitly:

```
Parallelize tool calls whenever possible. Batch reads (read_file) and
edits (apply_patch) to speed up the process.
```

### Context Preservation (Responses API)

Use `previous_response_id` to pass reasoning between turns. Preserves CoT tokens and eliminates plan reconstruction after tool calls.

Measured improvement: Tau-Bench Retail 73.9% → 78.2%.

## User Updates / Preambles

### GPT-5.2 (Concise)

```xml
<user_updates_spec>
- Send brief updates (1–2 sentences) only when:
  - Starting a new major phase of work, or
  - Discovering something that changes the plan.
- Avoid narrating routine tool calls.
- Each update must include at least one concrete outcome.
- Do not expand scope beyond what was asked.
</user_updates_spec>
```

### GPT-5.1 (Detailed)

```xml
<user_updates_spec>
- Send short updates (1–2 sentences) every few tool calls.
- Post an update at least every 6 execution steps or 8 tool calls.
- If expecting longer heads-down stretch, post a brief note with why and when.
- Before the first tool call, give a quick plan with goal, constraints, next steps.
- Always state at least one concrete outcome since prior update.
- End with a brief recap and follow-up steps.
- Include a brief checklist of planned items with status: Done or Closed (with reason).
</user_updates_spec>
```

## Scope Drift Prevention

```xml
<design_and_scope_constraints>
- Implement EXACTLY and ONLY what the user requests.
- No extra features, no added components, no UX embellishments.
- Style aligned to the design system at hand.
- Do NOT invent colors, shadows, tokens, animations, or new UI elements.
- If any instruction is ambiguous, choose the simplest valid interpretation.
</design_and_scope_constraints>
```

## Ambiguity & Hallucination Mitigation

```xml
<uncertainty_and_ambiguity>
- If the question is ambiguous or underspecified:
  - Ask up to 1–3 precise clarifying questions, OR
  - Present 2–3 plausible interpretations with clearly labeled assumptions.
- When external facts may have changed recently:
  - Answer in general terms and state that details may have changed.
- Never fabricate exact figures, line numbers, or external references.
- Prefer "Based on the provided context…" over absolute claims.
</uncertainty_and_ambiguity>
```

### High-Risk Self-Check

```xml
<high_risk_self_check>
Before finalizing answers in legal, financial, compliance, or safety contexts:
- Re-scan for unstated assumptions.
- Check for specific numbers or claims not grounded in context.
- Soften overly strong language ("always," "guaranteed").
- Explicitly state assumptions.
</high_risk_self_check>
```

## Long-Context Handling

```xml
<long_context_handling>
- For inputs >~10k tokens (multi-chapter docs, long threads, multiple PDFs):
  - First, produce a short internal outline of key sections relevant to the request.
  - Re-state user constraints explicitly.
  - Anchor claims to sections ("In the 'Data Retention' section…").
- Quote or paraphrase fine details (dates, thresholds, clauses).
</long_context_handling>
```

## Structured Extraction

```xml
<extraction_spec>
Extract structured data into this exact schema (no extra fields):
{
  "field_name": "string",
  "optional_field": "string | null"
}
- If a field is not present in source, set to null rather than guessing.
- Before returning, re-scan source for missed fields and correct omissions.
</extraction_spec>
```

For multi-file extractions: serialize per-document results separately, include stable IDs (filename, page range).

## Compaction (GPT-5.2)

Loss-aware compression of prior conversation state for long agentic sessions.

```
POST https://api.openai.com/v1/responses/compact
```

Best practices:
- Compact after major milestones, not every turn
- Keep prompts functionally identical when resuming
- Treat compacted items as opaque
- Monitor context usage and plan ahead

## Personality Shaping (GPT-5.1)

```xml
<final_answer_formatting>
You value clarity, momentum, and respect measured by usefulness.
- Adaptive politeness:
  - Warm user → single succinct acknowledgment, then back to work.
  - High stakes → drop acknowledgment, move straight to solving.
- Core: speak with grounded directness. Efficiency is respect.
- Never repeat acknowledgments. Pivot fully to the task.
- Match user's tempo: fast when they're fast, spacious when verbose.
</final_answer_formatting>
```

## Solution Persistence (GPT-5.1)

```xml
<solution_persistence>
- Treat yourself as autonomous senior pair-programmer: gather context, plan,
  implement, test, and refine without waiting for prompts at each step.
- Persist until task is fully handled end-to-end within current turn.
- Be extremely biased for action. If user asks "should we do x?" and your
  answer is "yes" — go ahead and perform the action.
</solution_persistence>
```

## Metaprompting: Debugging System Prompts

### Step 1: Diagnostic

```
Given the system prompt and failure traces, identify:
1) Distinct failure modes (tool_usage_inconsistency, verbosity_vs_concision, etc.)
2) Specific lines causing or reinforcing each failure
3) How those lines steer toward observed behavior
```

### Step 2: Surgical Revision

```
Propose minimal edits to reduce observed issues while preserving good behaviors.
- Clarify conflicting rules
- Remove redundant/contradictory lines
- Make tradeoffs explicit
- Keep structure and length roughly similar
Output: patch_notes + revised_system_prompt
```

## GPT-5.5 Patterns (Outcome-First Prompting)

GPT-5.5 works best when the prompt defines the **outcome** and leaves room for the model to choose an efficient path. Legacy prompts often over-specify the process — that adds noise on 5.5, narrows the search space, and produces mechanical answers. Strip prompt blocks the older models needed for hand-holding before adding 5.5-specific scaffolding.

### Outcome-First Prompts and Stopping Conditions

Describe the destination, not every step:

```
Resolve the customer's issue end to end.
Success means:
- the eligibility decision is made from the available policy and account data
- any allowed action is completed before responding
- the final answer includes completed_actions, customer_message, and blockers
- if evidence is missing, ask for the smallest missing field
```

Reserve `ALWAYS`, `NEVER`, `must`, `only` for true invariants (safety, required output fields, prohibited actions). For judgment calls (when to search, when to ask, when to keep iterating), use **decision rules** instead of absolutes.

Add explicit stopping conditions:

```
Resolve the user query in the fewest useful tool loops, but do not let loop
minimization outrank correctness, accessible fallback evidence, calculations,
or required citation tags for factual claims.
After each result, ask: "Can I answer the user's core request now with useful
evidence and citations for the factual claims?" If yes, answer.
```

Define missing-evidence behavior:

```
Use the minimum evidence sufficient to answer correctly, cite it precisely,
then stop.
```

### Personality vs Collaboration Style

Keep these two concerns **separate** and short:

- **Personality** — sound: tone, warmth, directness, formality, humor, empathy, polish.
- **Collaboration style** — work: when to ask, when to assume, proactivity, depth of context, when to check work, how to handle uncertainty/risk.

Neither replaces clear goals, success criteria, tool rules, or stopping conditions.

Steady, task-focused assistant:

```
# Personality
You are a capable collaborator: approachable, steady, and direct. Assume the user
is competent and acting in good faith, and respond with patience, respect, and
practical helpfulness.
Prefer making progress over stopping for clarification when the request is already
clear enough to attempt. Use context and reasonable assumptions to move forward.
Ask for clarification only when the missing information would materially change
the answer or create meaningful risk, and keep any question narrow.
Stay concise without becoming curt. Match the user's tone within professional
bounds. Avoid emojis and profanity by default.
```

Expressive, collaborative assistant:

```
# Personality
Adopt a vivid conversational presence: intelligent, curious, playful when
appropriate, attentive to the user's thinking. Ask good questions when the
problem is blurry, then become decisive once there is enough context.
Be warm, collaborative, and polished. Offer a real point of view rather than
mirroring the user, while staying responsive to their goals.
State a clear recommendation when you have enough context, explain important
tradeoffs, and name uncertainty without becoming evasive.
```

### Time-to-First-Visible-Token Preamble

In streaming UIs, GPT-5.5 may spend time reasoning or preparing tool calls before any visible text. For longer / tool-heavy tasks, prompt for a short preamble:

```
Before any tool calls for a multi-step task, send a short user-visible update
that acknowledges the request and states the first step. Keep it to one or two
sentences.
```

For coding agents with separate message phases:

```
You must always start with an intermediary update before any content in the
analysis channel if the task will require calling tools. The user update should
acknowledge the request and explain your first step.
```

### Formatting (5.5)

5.5 is highly steerable on output format. Set `text.verbosity` (API default `medium`; use `low` for shorter answers) and describe shape only when it improves comprehension:

```
Let formatting serve comprehension. Use plain paragraphs as the default for normal
conversation, explanations, reports, documentation, and technical writeups.
Use headers, bold text, bullets, and numbered lists sparingly — reach for them
when the user requests them, when the answer needs clear comparison or ranking,
or when the information would be harder to scan as prose.
Respect formatting preferences from the user. If they ask for a terse answer,
no bullets, no headers, or a specific structure, follow that preference.
```

For editing/rewriting/customer-facing summaries:

```
Preserve the requested artifact, length, structure, and genre first. Quietly
improve clarity, flow, and correctness. Do not add new claims, extra sections,
or a more promotional tone unless explicitly requested.
```

### Retrieval Budgets

Retrieval budgets are stopping rules for search — they tell the model when enough evidence is enough:

```
For ordinary Q&A, start with one broad search using short, discriminative keywords.
If the top results contain enough citable support for the core request, answer
from those results instead of searching again.
Make another retrieval call only when:
- The top results do not answer the core question.
- A required fact, parameter, owner, date, ID, or source is missing.
- The user asked for exhaustive coverage, a comparison, or a comprehensive list.
- A specific document, URL, email, meeting, record, or code artifact must be read.
- The answer would otherwise contain an important unsupported factual claim.
Do not search again to improve phrasing, add examples, cite nonessential details,
or support wording that can safely be made more generic.
```

### Creative Drafting Guardrails

For slides, launch copy, customer summaries, talk tracks, leadership blurbs, and narrative framing — separate source-backed facts from creative wording:

```
For creative or generative requests such as slides, leadership blurbs, outbound
copy, summaries for sharing, talk tracks, or narrative framing, distinguish
source-backed facts from creative wording.
- Use retrieved or provided facts for concrete product, customer, metric, roadmap,
  date, capability, and competitive claims, and cite those claims.
- Do not invent specific names, first-party data claims, metrics, roadmap status,
  customer outcomes, or product capabilities to make the draft sound stronger.
- If there is little or no citable support, write a useful generic draft with
  placeholders or clearly labeled assumptions rather than unsupported specifics.
```

### Suggested 5.5 Prompt Structure

Use as a starting skeleton — keep each section short, add detail only where it changes behavior:

```
Role: [1-2 sentences defining the model's function, context, and job]
# Personality
[tone, demeanor, and collaboration style]
# Goal
[user-visible outcome]
# Success criteria
[what must be true before the final answer]
# Constraints
[policy, safety, business, evidence, and side-effect limits]
# Output
[sections, length, and tone]
# Stop rules
[when to retry, fallback, abstain, ask, or stop]
```

## GPT-5.4 Patterns (Long-Running Agents)

GPT-5.4 is tuned for long-running multi-step agents, evidence-rich synthesis, and batched tool calls. It is most reliable when the prompt defines an explicit output contract, dependency-aware tool rules, and completion criteria.

### Output Contract & Verbosity Controls

```xml
<output_contract>
- Return exactly the sections requested, in the requested order.
- If the prompt defines a preamble, analysis block, or working section, do not
  treat it as extra output.
- Apply length limits only to the section they are intended for.
- If a format is required (JSON, Markdown, SQL, XML), output only that format.
</output_contract>
<verbosity_controls>
- Prefer concise, information-dense writing.
- Avoid repeating the user's request.
- Keep progress updates brief.
- Do not shorten the answer so aggressively that required evidence, reasoning,
  or completion checks are omitted.
</verbosity_controls>
```

### Default Follow-Through Policy

```xml
<default_follow_through_policy>
- If the user's intent is clear and the next step is reversible and low-risk,
  proceed without asking.
- Ask permission only if the next step is:
  (a) irreversible,
  (b) has external side effects (sending, purchasing, deleting, writing to prod), or
  (c) requires missing sensitive information or a choice that would materially
      change the outcome.
- If proceeding, briefly state what you did and what remains optional.
</default_follow_through_policy>
```

### Instruction Priority

```xml
<instruction_priority>
- User instructions override default style, tone, formatting, and initiative.
- Safety, honesty, privacy, and permission constraints do not yield.
- If a newer user instruction conflicts with an earlier one, follow the newer.
- Preserve earlier instructions that do not conflict.
</instruction_priority>
```

Higher-priority developer or system instructions remain binding.

### Mid-Conversation Task Updates

Use scoped steering messages that explicitly state Scope, Override, Carry forward:

```
<task_update>
For the next response only:
- Do not complete the task.
- Only produce a plan.
- Keep it to 5 bullets.
All earlier instructions still apply unless they conflict with this update.
</task_update>
```

If the task itself changes:

```
<task_update>
The task has changed.
Previous task: complete the workflow.
Current task: review the workflow and identify risks only.
Rules for this turn:
- Do not execute actions.
- Do not call destructive tools.
- Return exactly:
  1. Main risks
  2. Missing information
  3. Recommended next step
</task_update>
```

### Tool Persistence, Dependencies, Parallelism

GPT-5.4 can be **less reliable at tool routing early in a session** when context is thin. Prompt for prerequisites and exact tool intent:

```xml
<tool_persistence_rules>
- Use tools whenever they materially improve correctness, completeness, or
  grounding.
- Do not stop early when another tool call is likely to materially improve
  correctness or completeness.
- Keep calling tools until:
  (1) the task is complete, and
  (2) verification passes (see <verification_loop>).
- If a tool returns empty or partial results, retry with a different strategy.
</tool_persistence_rules>

<dependency_checks>
- Before taking an action, check whether prerequisite discovery, lookup, or
  memory retrieval steps are required.
- Do not skip prerequisite steps just because the intended final action seems
  obvious.
- If the task depends on the output of a prior step, resolve that dependency first.
</dependency_checks>

<parallel_tool_calling>
- When multiple retrieval or lookup steps are independent, prefer parallel tool
  calls to reduce wall-clock time.
- Do not parallelize steps that have prerequisite dependencies or where one
  result determines the next action.
- After parallel retrieval, pause to synthesize results before more calls.
- Prefer selective parallelism: parallelize independent evidence gathering,
  not speculative or redundant tool use.
</parallel_tool_calling>
```

### Completeness Contract & Empty-Result Recovery

```xml
<completeness_contract>
- Treat the task as incomplete until all requested items are covered or
  explicitly marked [blocked].
- Keep an internal checklist of required deliverables.
- For lists, batches, or paginated results:
  - determine expected scope when possible,
  - track processed items or pages,
  - confirm coverage before finalizing.
- If any item is blocked by missing data, mark it [blocked] and state exactly
  what is missing.
</completeness_contract>

<empty_result_recovery>
If a lookup returns empty, partial, or suspiciously narrow results:
- do not immediately conclude that no results exist,
- try at least one or two fallback strategies, such as:
  - alternate query wording,
  - broader filters,
  - a prerequisite lookup,
  - or an alternate source or tool,
- only then report that no results were found, along with what you tried.
</empty_result_recovery>
```

### Verification Loop & Action Safety

```xml
<verification_loop>
Before finalizing:
- Check correctness: does the output satisfy every requirement?
- Check grounding: are factual claims backed by the provided context or tool outputs?
- Check formatting: does the output match the requested schema or style?
- Check safety and irreversibility: if the next step has external side effects,
  ask permission first.
</verification_loop>

<missing_context_gating>
- If required context is missing, do NOT guess.
- Prefer the appropriate lookup tool when the missing context is retrievable;
  ask a minimal clarifying question only when it is not.
- If you must proceed, label assumptions explicitly and choose a reversible action.
</missing_context_gating>

<action_safety>
- Pre-flight: summarize the intended action and parameters in 1-2 lines.
- Execute via tool.
- Post-flight: confirm the outcome and any validation that was performed.
</action_safety>
```

### Citation & Grounding Rules (5.4)

```xml
<citation_rules>
- Only cite sources retrieved in the current workflow.
- Never fabricate citations, URLs, IDs, or quote spans.
- Use exactly the citation format required by the host application.
- Attach citations to the specific claims they support, not only at the end.
</citation_rules>

<grounding_rules>
- Base claims only on provided context or tool outputs.
- If sources conflict, state the conflict explicitly and attribute each side.
- If the context is insufficient or irrelevant, narrow the answer or say you
  cannot support the claim.
- If a statement is an inference rather than a directly supported fact, label
  it as an inference.
</grounding_rules>
```

### Research Mode (Three-Pass)

Use for research/review/synthesis tasks. Do not force onto short execution tasks:

```xml
<research_mode>
- Do research in 3 passes:
  1) Plan: list 3-6 sub-questions to answer.
  2) Retrieve: search each sub-question and follow 1-2 second-order leads.
  3) Synthesize: resolve contradictions and write the final answer with citations.
- Stop only when more searching is unlikely to change the conclusion.
</research_mode>
```

### Strict Output Formats & BBox Extraction

```xml
<structured_output_contract>
- Output only the requested format.
- Do not add prose or markdown fences unless they were requested.
- Validate that parentheses and brackets are balanced.
- Do not invent tables or fields.
- If required schema information is missing, ask for it or return an explicit
  error object.
</structured_output_contract>

<bbox_extraction_spec>
- Use the specified coordinate format exactly, e.g. [x1,y1,x2,y2] normalized 0..1.
- For each box, include page, label, text snippet, confidence.
- Add a vertical-drift sanity check so boxes stay aligned with the correct line.
- For dense layouts, process page by page and do a second pass for missed items.
</bbox_extraction_spec>
```

### Image Detail (Vision / Computer Use)

If the workflow depends on visual precision, set image `detail` explicitly rather than `auto`:

- `high` — standard high-fidelity image understanding.
- `original` — large, dense, or spatially sensitive images (computer use, OCR, click accuracy).
- `low` — only when speed/cost matter more than fine detail.

### Coding-Agent Guardrails

```xml
<terminal_tool_hygiene>
- Only run shell commands via the terminal tool.
- Never "run" tool names as shell commands.
- If a patch or edit tool exists, use it directly; do not attempt it in bash.
- After changes, run a lightweight verification step (ls, tests, or build) before
  declaring the task done.
</terminal_tool_hygiene>

<autonomy_and_persistence>
Persist until the task is fully handled end-to-end within the current turn:
do not stop at analysis or partial fixes; carry changes through implementation,
verification, and a clear explanation of outcomes unless the user explicitly
pauses or redirects.
Unless the user is asking a question, brainstorming, or clearly does not want
code, assume they want code changes — implement them, don't propose them.
If you encounter blockers, attempt to resolve them yourself.
</autonomy_and_persistence>
```

5.4 also tends to overuse nested bullets; clamp shape if you want clean prose:

```
Never use nested bullets. Keep lists flat (single level). If you need hierarchy,
split into separate lists or sections, or place the would-be sub-bullet immediately
after a colon. For numbered lists, use `1. 2. 3.` only — never `1)`.
```

### Personality vs Per-Response Writing Controls

GPT-5.4 separates persistent personality from per-response writing controls:

```xml
<personality_and_writing_controls>
- Persona: <one sentence>
- Channel: <Slack | email | memo | PRD | blog>
- Emotional register: <direct/calm/energized/etc.> + "not <overdo this>"
- Formatting: <ban bullets/headers/markdown if you want prose>
- Length: <hard limit, e.g. <=150 words or 3-5 sentences>
- Default follow-through: if the request is clear and low-risk, proceed without
  asking permission.
</personality_and_writing_controls>
```

Memo / professional-writing mode:

```xml
<memo_mode>
- Write in a polished, professional memo style.
- Use exact names, dates, entities, and authorities when supported by the record.
- Follow domain-specific structure if one is requested.
- Prefer precise conclusions over generic hedging.
- When uncertainty is real, tie it to the exact missing fact or conflicting source.
- Synthesize across documents rather than summarizing each one independently.
</memo_mode>
```

### Phase Parameter (5.4 / 5.5 / Codex)

For long-running or tool-heavy Responses workflows, the assistant `phase` field separates intermediate updates from final answers. `phase` is optional but **strongly recommended**.

- `phase: "commentary"` — intermediate user-visible updates (preambles, tool-related notes).
- `phase: "final_answer"` — the completed answer.
- Do **not** add `phase` to user messages.
- If you use `previous_response_id`, the API preserves prior assistant state automatically.
- If you manually replay assistant items, **preserve each original `phase` value unchanged**. Dropped phases can cause preambles to be interpreted as final answers and degrade behavior on multi-step tasks.

### Small-Model Guidance (`gpt-5.4-mini`, `gpt-5.4-nano`)

Smaller models in the 5.4 line are highly steerable but less likely to infer missing steps or resolve ambiguity implicitly. Prompts for them are typically a bit longer and more explicit.

**`gpt-5.4-mini`:**
- More literal, fewer assumptions; weaker on implicit workflows and ambiguity.
- Put critical rules first.
- Specify the full execution order when tool use or side effects matter.
- Use structural scaffolding (numbered steps, decision rules, explicit action definitions) — do not rely on `you MUST` alone.
- Separate "do the action" from "report the action."
- Define ambiguity behavior explicitly: when to ask, abstain, or proceed.
- Prefer scoped instructions like `after the final JSON, output nothing further` over bare `output nothing else`.

**`gpt-5.4-nano`:**
- Use only for narrow, well-bounded tasks.
- Prefer closed outputs: labels, enums, short JSON, or fixed templates.
- Avoid multi-step orchestration unless the flow is extremely constrained.
- Route ambiguous or planning-heavy tasks to a stronger model.

Default pattern: Task → Critical rule → Exact step order → Edge cases / clarification behavior → Output format → One correct example.

## Migration Checklist

1. **Switch model, keep prompt identical** — isolate the variable
2. **Pin reasoning_effort** — match prior model's latency/depth profile
3. **Run evals** — if results are good, ship
4. **If regressions, tune prompt** — adjust verbosity/format/scope constraints
5. **Re-eval after each small change** — one change at a time

### GPT-4.1 → GPT-5 Adjustments

- Remove explicit encouragement to "gather context thoroughly" — GPT-5 is naturally introspective
- Soften maximization language ("THOROUGH" → "if not confident, gather more information")
- Add agentic persistence explicitly ("keep going until resolved")
- Use `verbosity` API parameter in addition to prompt-level controls
- Leverage Responses API with `previous_response_id`

### GPT-5 → GPT-5.1 Adjustments

- Emphasize persistence and completeness (5.1 can be excessively concise)
- Be explicit about desired output detail (5.1 can occasionally be verbose)
- Migrate apply_patch to named tool implementation (35% fewer failures)
- Check for conflicting instructions — 5.1 is excellent at instruction-following

### GPT-5.1 → GPT-5.2 Adjustments

- Clamp verbosity of user updates (shorter, more focused)
- Make scope discipline explicit
- Adjust for default `none` reasoning — set explicit level if depth needed
- Leverage compaction API for long sessions

### GPT-5.2 → GPT-5.4 Adjustments

- Add `<output_contract>` and `<verbosity_controls>` — 5.4 may overuse bullets/structure
- Add `<tool_persistence_rules>` and `<dependency_checks>` — 5.4 can be weak at early-session tool routing
- Add `<completeness_contract>` and `<empty_result_recovery>` — 5.4 can stop at partial coverage
- Add `<verification_loop>` before high-impact actions
- Round-trip the `phase` field if you replay assistant items manually
- Treat reasoning effort as last-mile; before raising it, add the contracts above

### GPT-5.4 → GPT-5.5 Adjustments

- **Strip over-specification**: legacy step-by-step process prompts often hurt 5.5 — describe the outcome, not every step
- Replace blanket `ALWAYS`/`NEVER`/`must` with **decision rules**, except for true invariants (safety, required output fields, prohibited actions)
- Split persona into **Personality** (sound) and **Collaboration style** (work)
- Add a preamble instruction for streaming UIs (time-to-first-visible-token)
- Add an explicit **retrieval budget** for grounded / search-tool agents
- Add **creative drafting guardrails** for slides / launch copy / customer summaries
- Use `text.verbosity` (`low` / `medium`) before adding prompt-level length rules
- Adopt the suggested 5.5 prompt structure (Role → Personality → Goal → Success criteria → Constraints → Output → Stop rules)

## Web Research Agent Pattern

```xml
<web_search_rules>
- Act as expert research assistant; default to comprehensive, well-structured answers.
- Prefer web research over assumptions whenever facts may be uncertain.
- Research all parts of the query, resolve contradictions, follow implications.
- Do not ask clarifying questions; cover all plausible user intents.
- Write clearly using Markdown (headers, bullets, tables).
</web_search_rules>
```

### Research Methodology
- Start with multiple targeted searches; use parallel searches
- Begin broad, add targeted follow-ups to fill gaps
- Stop only when: answered every subpart / found concrete examples / found sufficient sources
- Include citations after paragraphs with web-derived claims

### Ambiguity Handling (Without Questions)
State best-guess interpretation plainly, then comprehensively cover the most likely intent. If multiple intents, cover each one fully.
