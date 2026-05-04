# Claude Family Prompting Guide

Covers Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, and Claude Haiku 4.5. Based on official Anthropic documentation.

Sources:
- [Prompting Best Practices — Claude 4](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Adaptive Thinking](https://docs.anthropic.com/en/docs/build-with-claude/adaptive-thinking)
- [Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Token-Efficient Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/token-efficient-tool-use)
- [Structured Outputs](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs)
- [Citations](https://docs.anthropic.com/en/docs/build-with-claude/citations)
- [Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Context Windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
- [Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision)
- [Migrating to Claude 4](https://docs.anthropic.com/en/docs/about-claude/models/migrating-to-claude-4)
- [Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [The "Think" Tool](https://www.anthropic.com/engineering/claude-think-tool)
- [Introducing Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)
- [API Release Notes](https://docs.anthropic.com/en/release-notes/api)

## Model Comparison

| Aspect | Opus 4.7 | Opus 4.6 | Sonnet 4.6 | Sonnet 4.5 | Haiku 4.5 |
|--------|----------|----------|------------|------------|-----------|
| Context window | 1M (beta) | 1M (beta) | 200K (1M beta) | 200K | 200K |
| Default thinking | Adaptive | Adaptive | Adaptive | Extended (`budget_tokens`) | None |
| Effort parameter | Yes — `low / medium / high / xhigh` (default: high) | Yes (default: high) | Yes (default: high) | No | No |
| Legacy `thinking.budget_tokens` | **400 error** (removed) | Supported (deprecated path) | Supported (deprecated path) | Yes | n/a |
| `task_budget` (agentic loop) | Beta | — | — | — | — |
| Prefill support | **No** (deprecated) | **No** (deprecated) | **No** (deprecated) | Yes | Yes |
| Structured outputs | Yes (`strict: true`) | Yes (`strict: true`) | Yes | Yes | Limited |
| Token-efficient tools | Built-in (no header) | Built-in (no header) | Built-in (no header) | Built-in (no header) | Built-in (no header) |
| Default tool eagerness | Reasoning-first; can **under-trigger** at low effort | Calibrated | Calibrated | n/a | n/a |
| Tokenizer | New — up to ~1.35× more text tokens; images up to ~3× (max 2576px long edge) | Prior tokenizer | Prior tokenizer | Prior tokenizer | Prior tokenizer |
| Cyber Verification gate | Yes (auto-blocks unverified high-risk security prompts) | No | No | No | No |
| Cost (in/out per 1M) | $15/$75 | $15/$75 | $3/$15 | $3/$15 | $0.80/$4 |
| Key strength | Top-tier reasoning, longer-running agents, more literal instruction-following | Hardest problems, deep research | Fast agentic coding, balance | Extended thinking with budget | Speed, volume |

## Thinking Modes

### Adaptive Thinking (Claude 4.6 / 4.7 — Recommended)

Claude dynamically decides when and how much to think based on query complexity and the `effort` parameter.

```python
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # xhigh, high, medium, low
    messages=[{"role": "user", "content": "..."}],
)
```

**Effort levels (Opus 4.7):** `low | medium | high | xhigh`. Note: `max` from earlier docs is gone; `xhigh` replaces the top of the scale and is the new ceiling for hardest reasoning / agentic work. Existing `medium` calls on 4.6 can often be downgraded to `low` on 4.7 without quality loss (low-effort 4.7 ≈ medium-effort 4.6).

**Effort levels (Opus 4.6 / Sonnet 4.6):** `low | medium | high`. Default is `high`.

| Effort | Best for |
|---|---|
| `low` | High-volume, latency-sensitive workloads; chat/non-coding on 4.6; many 4.7 production tasks |
| `medium` | Recommended starting point for most 4.6 applications |
| `high` | Default on 4.6/4.7; balanced for production agents |
| `xhigh` | **Opus 4.7 only.** Hardest reasoning, long-horizon agents, intelligence-sensitive coding tasks |

**When adaptive thinking wins:**
- Autonomous multi-step agents (coding, data analysis, bug finding)
- Computer use agents (best-in-class accuracy)
- Bimodal workloads (mix of easy and hard tasks)

**Steering adaptive thinking:**
If the model thinks too often (common with complex system prompts):

```
Extended thinking adds latency and should only be used when it will
meaningfully improve answer quality — typically for problems that require
multi-step reasoning. When in doubt, respond directly.
```

### Breaking Change: Legacy Extended-Thinking Block on Opus 4.7

The legacy `thinking={"type": "enabled", "budget_tokens": N}` block is **fully removed for Opus 4.7 and later**. It is not silently ignored — the API returns a **400 error**. Migrate any scaffold or template before pointing it at 4.7:

```python
# Will 400 on Opus 4.7
thinking={"type": "enabled", "budget_tokens": 16384}

# Use this instead
thinking={"type": "adaptive"}
output_config={"effort": "high"}   # or "xhigh"
```

Sonnet 4.5 and Haiku 4.5 still accept the legacy block.

### `task_budget` (Opus 4.7 Beta — Agentic Loop Cost Control)

Opus 4.7 introduces a beta `task_budget` parameter that gives the model a **token countdown across the entire agentic loop** — thinking tokens + tool calls + tool results + final output. The model sees the running budget and prioritizes work to finish gracefully before exhaustion.

Use this **above** `effort` for long-horizon agents where total cost matters more than per-call depth. `effort` still controls per-step thinking; `task_budget` caps the whole loop.

```python
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "xhigh"},
    task_budget={"max_tokens": 200000},   # whole-loop ceiling
    tools=[...],
    messages=[...],
)
```

When to use:
- Multi-tool agents that may run dozens of iterations
- Workloads where you want predictable invoice ceilings
- Production agents that must "finish what they can" before shutting down

When **not** to use:
- Single-shot Q&A (use `effort` and `max_tokens` only)
- Workflows where mid-task abandonment is unacceptable

### Extended Thinking (Claude Sonnet 4.5 and older)

Manual token budget for reasoning.

```python
client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=64000,
    thinking={"type": "enabled", "budget_tokens": 16384},
    messages=[{"role": "user", "content": "..."}],
)
```

- Minimum `budget_tokens`: 1,024
- Must be less than `max_tokens`
- Accuracy improves logarithmically with thinking tokens
- Claude often won't use the entire budget, especially above 32K

### Interleaved Thinking (Sonnet 4.6 with Extended)

Sonnet 4.6 supports thinking between tool calls when using extended mode:

```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16384,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "..."}],
)
```

### Overthinking Prevention (Opus 4.6)

Opus 4.6 explores extensively at higher effort. If undesirable:

```
When deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning. If you're weighing two approaches, pick one and
see it through.
```

For Sonnet 4.6: switch from adaptive to extended thinking with a `budget_tokens` cap for a hard ceiling on thinking costs.

### The "Think" Tool

A lightweight alternative to extended thinking — a tool with no side effects that gives Claude a scratchpad for multi-step reasoning:

```json
{
    "name": "think",
    "description": "Use this tool to think through complex problems step-by-step before responding.",
    "input_schema": {
        "type": "object",
        "properties": {
            "thought": {
                "type": "string",
                "description": "Your step-by-step thinking about the problem."
            }
        },
        "required": ["thought"]
    }
}
```

Best used when extended thinking is disabled but you want structured reasoning at specific points.

## Prefill Deprecation (Claude 4.6)

Prefilling the assistant turn is **no longer supported** on Claude 4.6 models.

### Migration Paths

| Previous Prefill Use | New Approach |
|---------------------|-------------|
| Force JSON output (`{`) | Structured Outputs (`strict: true`) |
| Skip preamble (`Here is...`) | System prompt: "Respond directly without preamble" |
| Avoid bad refusals | Improved in Claude 4.6; clear user-message prompting sufficient |
| Continue partial response | Move continuation text to user message |
| Context hydration | Inject reminders in user turn or via tools |

## General Prompting Principles

### Be Clear and Direct

Claude responds well to explicit instructions. Think of Claude as a brilliant new employee lacking your context.

**Golden rule:** Show your prompt to a colleague with minimal context. If they'd be confused, Claude will be too.

```
# Less effective
Create an analytics dashboard

# More effective
Create an analytics dashboard. Include as many relevant features and
interactions as possible. Go beyond the basics to create a fully-featured
implementation.
```

### Add Context / Motivation

Explain WHY behind instructions. Claude generalizes from explanations:

```
# Less effective
NEVER use ellipses

# More effective
Your response will be read aloud by a text-to-speech engine, so never use
ellipses since the engine won't know how to pronounce them.
```

### Use Examples (Few-Shot)

3–5 well-crafted examples dramatically improve accuracy. Make them:
- **Relevant** — mirror actual use cases
- **Diverse** — cover edge cases
- **Structured** — wrap in `<example>` / `<examples>` tags

### XML Tags for Structure

Use semantic XML tags to separate concerns:
- `<instructions>`, `<context>`, `<input>`, `<documents>`
- Consistent tag names across prompts
- Nest naturally: `<documents><document index="1">...</document></documents>`

### Role Setting

```python
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    system="You are a helpful coding assistant specializing in Python.",
    messages=[{"role": "user", "content": "..."}],
)
```

## Output & Formatting Control

### Claude 4.6 / 4.7 Communication Style

More concise and natural than previous models:
- More direct and grounded (fact-based, not self-celebratory)
- More conversational and less machine-like
- Less verbose — may skip summaries after tool calls
- Opus 4.7 is **even more direct** — less validation-forward, less warm by default

If you need more visibility (especially on 4.7, where post-tool silence is the default):

```
After completing a task that involves tool use, provide a brief summary
of the work you've done.
```

If your product depends on a warmer register, review voice/style prompts when migrating from 4.6 to 4.7 — 4.6's defaults won't carry over.

### Literal Instruction Following on Opus 4.7

Opus 4.7 is **more literal** at low/medium effort and does not silently generalize instructions across items or infer unstated requests. Two implications:

**Prompts written for 4.6 that relied on implicit generalization need explicit rewrites.** If a 4.6 prompt said "Format the first item like X" expecting all items to follow, 4.7 will format only the first.

```
# Brittle on 4.7
Format the first row as "id: name (status)".

# Robust on 4.7
For every row, format as "id: name (status)".
```

**Conversely**, structured-extraction and pipeline prompts become **more reliable** on 4.7 — fewer cases of the model "helpfully" adding fields, sections, or commentary that weren't requested.

### Steer Format Positively

Tell Claude what to do, not what NOT to do:
- Instead of "Do not use markdown" → "Compose smoothly flowing prose paragraphs"
- Use XML format indicators: "Write in `<prose>` tags"
- Match prompt style to desired output style (removing markdown from prompts reduces markdown in output)

### Minimize Markdown/Bullets

```xml
<avoid_excessive_markdown_and_bullet_points>
Write in clear, flowing prose using complete paragraphs. Reserve markdown
for inline code, code blocks, and simple headings.
DO NOT use ordered/unordered lists unless: a) presenting truly discrete items,
or b) user explicitly requests a list.
Instead of bullets, incorporate items naturally into sentences.
</avoid_excessive_markdown_and_bullet_points>
```

### LaTeX Control (Opus 4.6)

Opus 4.6 defaults to LaTeX for math. To prevent:
```
Format in plain text only. Do not use LaTeX, MathJax, or markup notation
such as \( \), $, or \frac{}{}. Write math using standard text characters.
```

## Tool Use Best Practices

### Explicit Action Instructions

Claude may suggest rather than act. Be explicit:
```
# Claude will only suggest
Can you suggest some changes to improve this function?

# Claude will make changes
Change this function to improve its performance.
```

### Proactive vs Conservative Action

**Proactive (default to action):**
```xml
<default_to_action>
By default, implement changes rather than only suggesting them. If user intent
is unclear, infer the most useful likely action and proceed, using tools to
discover missing details instead of guessing.
</default_to_action>
```

**Conservative (default to analysis):**
```xml
<do_not_act_before_instructions>
Do not jump into implementation unless clearly instructed. When intent is
ambiguous, default to providing information and recommendations. Only proceed
with edits when explicitly requested.
</do_not_act_before_instructions>
```

### Parallel Tool Calling

Claude 4.6 excels at parallel execution. Boost to ~100% success:

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between
calls, make all independent calls in parallel. Prioritize simultaneous
execution whenever actions can be done in parallel. Never use placeholders
or guess missing parameters.
</use_parallel_tool_calls>
```

To reduce parallel execution:
```
Execute operations sequentially with brief pauses between each step.
```

### Tool Eagerness — 4.6 vs 4.7

**Opus 4.6** is *more responsive* to system prompts. Aggressive tool instructions from older models cause overtriggering:

```
# Too aggressive (was needed for older models)
CRITICAL: You MUST use this tool when...

# Appropriate for 4.6
Use this tool when...
```

**Opus 4.7 inverts this problem.** 4.7 favors reasoning over tool calls by default and can **under-trigger** tools at low/medium effort, especially in knowledge-work agents that previously relied on subagent delegation. Levers, in order of preference:

1. **Raise `effort`** to `high` or `xhigh` — the recommended way to increase tool invocation on 4.7.
2. **Be explicit** about when tools (and subagents) are desirable, e.g. "Use the `search_docs` tool whenever the user mentions a specific repository, file, or PR — do not answer from memory."
3. **Constrain the alternative**: "Do not infer code structure without reading the file."

### Subagent Delegation on 4.7

Opus 4.7 spawns **fewer subagents by default** than 4.6 (reasoning-first bias). For research and parallel-workstream tasks where 4.6 delegated automatically, 4.7 often does the work inline. To restore delegation:

```xml
<subagent_policy>
For independent research subtasks, parallel evidence gathering, or work that
benefits from isolated context, delegate to a subagent rather than handling
inline. Specifically delegate when:
- Two or more lines of inquiry can run in parallel.
- A subtask requires reading >5 files or >10 search results before synthesis.
- The subtask's intermediate output is large but the final summary is small.
For simple lookups or single-file edits, work directly.
</subagent_policy>
```

### Structured Outputs (Tool-Based)

Add `strict: true` to tool definitions for guaranteed schema validation:
```json
{
    "name": "extract_data",
    "description": "Extract structured data from text",
    "strict": true,
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "category": {"type": "string", "enum": ["A", "B", "C"]}
        },
        "required": ["name", "category"]
    }
}
```

Eliminates type mismatches and missing fields. Enable with beta header: `structured-outputs-2025-11-13`.

**Note:** Cannot use with Citations (citations require interleaving blocks).

## Long Context Best Practices

### Document Placement

Place long documents (20K+ tokens) at the **top** of the prompt, above queries and instructions. Up to 30% quality improvement.

### Document Structure

```xml
<documents>
  <document index="1">
    <source>annual_report_2023.pdf</source>
    <document_content>{{ANNUAL_REPORT}}</document_content>
  </document>
  <document index="2">
    <source>competitor_analysis.xlsx</source>
    <document_content>{{COMPETITOR_ANALYSIS}}</document_content>
  </document>
</documents>

Analyze the annual report and competitor analysis.
```

### Ground Responses in Quotes

Ask Claude to quote relevant parts before answering:
```
Find quotes from the patient records relevant to diagnosing symptoms.
Place these in <quotes> tags. Then, based on these quotes, list diagnostic
information in <info> tags.
```

### 1M Token Context (Beta)

Available for Opus 4.6 and Sonnet 4.6 with header `context-1m-2025-08-07`. Requests exceeding 200K auto-charged at premium long-context rates.

## Prompt Caching

### Cost Savings

- Cache writes: 1.25x input price
- Cache reads: 0.1x input price (90% savings)
- Up to 85% latency reduction

### Strategy

- Place cacheable content at prompt beginning
- Use `cache_control` breakpoints to separate cacheable sections
- Ensure cached sections are byte-identical across requests
- Calls must occur within 5-minute (default) or 1-hour cache lifetime

### Best Use Cases

- Long system instructions + documents
- Few-shot examples (dozens of diverse examples)
- Conversational agents with persistent context
- Agentic search with repeated tool definitions

## Citations

Ground answers in source documents with sentence-level granularity.

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "text", "media_type": "text/plain", "data": doc_text},
                "citations": {"enabled": True}
            },
            {"type": "text", "text": "Summarize the key findings."}
        ]
    }]
)
```

- Supports PDF and plain text
- `cited_text` doesn't count toward output tokens
- Up to 15% improvement in recall accuracy
- **Cannot combine with Structured Outputs**

## Vision

### Image Placement

Best performance: images before text (image-then-text structure).

### Capabilities

- Chart interpretation and analysis
- Form content extraction
- Document processing
- Image evaluation and comparison
- Up to 100 images per request (API), 20 per request (Claude.ai)

### Image Resolution & Token Cost (Opus 4.7)

Opus 4.7 supports a higher max image resolution: **2576px on the long edge** (up from prior limits). High-resolution images can cost up to ~4784 tokens vs ~1600 on 4.6 — roughly **3× more tokens for images at the new max**.

Practical guidance:
- **Downsample explicitly** when full resolution is not required for the task.
- Recompute cached-token math and batch-discount math against the new tokenizer (see "Tokenizer Changes").
- Re-run `/v1/messages/count_tokens` for any image-heavy workload before pricing.

### Crop Tool for Accuracy Uplift

Pairs especially well with Opus 4.7's higher resolution support — give Claude a crop/zoom tool so it can examine regions at full fidelity instead of paying the full-image token cost up front:
- Provide a crop/zoom tool in tool definitions
- Claude selects relevant regions to examine in detail
- Consistent benchmark uplift on detailed analysis tasks

## Agentic Patterns

### Long-Horizon State Tracking

Claude 4.6 excels at maintaining orientation across extended sessions through incremental progress.

#### Context Awareness

Claude 4.6/4.5 tracks remaining context window. If using compaction or external files:

```
Your context window will be automatically compacted as it approaches its limit.
Do not stop tasks early due to token budget concerns. As you approach the limit,
save current progress and state to memory before the context window refreshes.
```

#### Multi-Context Window Workflows

1. **First window**: Set up framework (write tests, create setup scripts)
2. **Subsequent windows**: Iterate on todo-list
3. **Write tests in structured format**: e.g., `tests.json` — "It is unacceptable to remove or edit tests"
4. **Create QoL tools**: `init.sh` to start servers, run tests, linters
5. **Starting fresh vs compacting**: Claude 4.6 is extremely effective at discovering state from filesystem
6. **Provide verification tools**: Playwright MCP, computer use for UI testing

#### State Management

- **Structured formats** for state data (JSON for test results, task status)
- **Freeform text** for progress notes
- **Git** for state tracking across sessions — Claude 4.6 excels at this

### Cyber Verification Program (Opus 4.7)

Opus 4.7 ships with **hardened cybersecurity safeguards** that automatically block requests flagged as prohibited or high-risk. Legitimate security work — penetration testing, vulnerability research, red-teaming, exploit development — that was permitted on 4.6 may now be **refused on 4.7** without enrollment in Anthropic's **Cyber Verification Program**.

Practical implications for prompt design:
- Prompts that previously worked for security use cases on 4.6 may need updated framing or model fallback to 4.6.
- For verified workflows, frame the legitimate research context explicitly (engagement scope, defensive intent, authorization).
- Do **not** try to bypass via roleplay or prompt obfuscation — the gate is policy-level, not prompt-level.

### Autonomy vs Safety

```
Consider the reversibility and potential impact of your actions. Take local,
reversible actions freely (editing files, running tests), but for hard-to-reverse
or shared-system actions, ask the user before proceeding.

Examples warranting confirmation:
- Destructive: deleting files/branches, dropping tables, rm -rf
- Hard to reverse: git push --force, git reset --hard
- Visible to others: pushing code, commenting on PRs, sending messages
```

### Subagent Orchestration

Claude 4.6 proactively delegates to subagents without explicit instruction. Control overuse:

```
Use subagents when tasks can run in parallel, require isolated context, or
involve independent workstreams. For simple tasks, sequential operations,
or single-file edits, work directly rather than delegating.
```

### Research Pattern

```
Search for this information in a structured way. As you gather data, develop
competing hypotheses. Track confidence levels. Regularly self-critique your
approach. Update a hypothesis tree or research notes file. Break down complex
research systematically.
```

### Anti-Overengineering

```xml
<avoid_overengineering>
Only make changes directly requested or clearly necessary. Keep solutions simple:
- Don't add features, refactor code, or "improve" beyond what was asked
- Don't add docstrings/comments/annotations to unchanged code
- Don't add error handling for impossible scenarios
- Don't create abstractions for one-time operations
- Don't design for hypothetical future requirements
</avoid_overengineering>
```

### Anti-Hallucination in Agentic Coding

```xml
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific
file, you MUST read the file before answering. Investigate and read relevant files
BEFORE answering questions about the codebase. Never make claims about code before
investigating.
</investigate_before_answering>
```

### Anti-Test-Hacking

```
Write a high-quality, general-purpose solution using standard tools.
Do not hard-code values or create solutions that only work for specific test inputs.
Implement the actual logic that solves the problem generally.
Tests verify correctness, not define the solution.
If tests are incorrect, inform me rather than working around them.
```

## Server-Side Compaction (Beta)

Now in **public beta** for Opus 4.7, Opus 4.6, and Sonnet 4.6. Anthropic automatically summarizes earlier conversation turns server-side when the conversation approaches the context limit, allowing multi-turn agents to run **beyond** the model's nominal context window.

When to prefer it:
- Long-running multi-turn agents (assistants, support copilots).
- Workloads where you'd otherwise truncate or roll your own compaction.

When **not** to use it (use manual structured compaction instead):
- Workflows that must preserve exact text of earlier turns (legal, audit).
- Cases where you depend on inspecting compacted state.

Design implications:
- Treat compacted turns as **opaque** — don't parse or rely on internals.
- Structure persistent state into **external artifacts** (files, NOTES.md, todo lists) so a fresh session can rehydrate quickly even after compaction.
- Compaction is a complement to, not a replacement for, prompt caching — caching applies to cached prefixes, compaction applies to mid-conversation state.

## Managed Agents — Memory in Public Beta

Anthropic's **Managed Agents** harness is in public beta with multi-session memory. Required header on all endpoints:

```
anthropic-beta: managed-agents-2026-04-01
```

Provides:
- Secure sandboxing
- Built-in tools (web search, file ops, code execution)
- SSE streaming for long runs
- Multi-session memory patterns (see "Using agent memory" docs)

Use when you'd otherwise be hand-rolling sandboxing + memory + tool plumbing. Skip when your harness already gives you those primitives.

## Context Engineering

### The "Right Altitude" for System Prompts

Avoid two failure modes:
1. **Overly brittle**: Hardcoded if-else logic — fragile, high maintenance
2. **Overly vague**: High-level guidance without concrete signals

**Optimal:** Specific enough to guide behavior, flexible enough for strong heuristics.

### Three Strategies for Long-Horizon Tasks

**1. Compaction**
- Summarize conversations approaching context limits
- Preserve architectural decisions, unresolved bugs, implementation details
- Discard redundant tool outputs
- Start by maximizing recall, then iterate for precision

**2. Structured Note-Taking (Agentic Memory)**
- Agent writes notes persisted outside context window
- Enables multi-hour task sequences with context resets
- Claude Code uses to-do lists; custom agents use NOTES.md

**3. Sub-Agent Architectures**
- Specialized agents handle focused tasks with clean context
- Return condensed summaries (1,000–2,000 tokens)
- Achieves separation between detailed search and synthesis

### Tool Result Trimming

Remove raw tool results from deep message history. Once a tool is called, the agent needs the summary, not raw output. This is the "safest, lightest touch" form of compaction.

### Just-In-Time Context Retrieval

Maintain lightweight identifiers (file paths, queries) and dynamically load data at runtime via tools, rather than pre-processing all data upfront.

Claude Code hybrid: pre-load CLAUDE.md files, use glob/grep for just-in-time retrieval.

## Tokenizer Changes (Opus 4.7)

Opus 4.7 ships with a **new tokenizer**. Same text can produce up to **~1.35× more tokens** than 4.6, and high-res images up to **~3×** more (see Vision section). Implications:

- `/v1/messages/count_tokens` returns different numbers for 4.7 vs 4.6 — re-run it for any prompt where token cost matters.
- All cached-token, batch-discount, and budget math must be **rechecked** with 4.7 token counts before assuming carry-over savings.
- If your prompt was tuned to fit a specific token budget on 4.6 (system prompt sizing, document chunking, RAG context windows), revalidate on 4.7.
- Model routing logic that switches based on token thresholds needs new thresholds.

## Token Efficiency

### Token-Efficient Tool Use — Built-In on All Claude 4 Models

The historical `token-efficient-tools-2025-02-19` beta header **only works with Claude 3.7 Sonnet**. For all Claude 4 models (Opus 4.6 / 4.7, Sonnet 4.5 / 4.6, Haiku 4.5) the optimization is built-in. **Remove the header** — sending it has no effect and is a dead code smell.

### Key Optimizations

| Technique | Savings |
|-----------|---------|
| Tool Search Tool | 85% token reduction while maintaining full tool library |
| Programmatic tool calling | 37% reduction (43,588 → 27,297 tokens) |
| Tool call output token reduction | 70% for tool calling (14% average overall) |
| Lower extended thinking budget | ~70% reduction in hidden thinking costs |
| Model routing (Sonnet for 80% of tasks) | 60% cost reduction |
| Context compaction at 50% vs 95% | Healthier sessions, less degradation |
| `task_budget` (Opus 4.7) | Predictable whole-loop ceiling for agentic workloads |

### Temperature & Sampling

- **Temperature** (0.0–1.0, default 1.0):
  - Near 0.0 for analytical/classification tasks
  - Near 1.0 for creative/generative tasks
- **Critical:** Since Opus 4.1, temperature AND top_p cannot both be specified (API-level enforcement). Use only temperature for typical use cases.

## Frontend Design

Claude 4.6 excels at web applications but can default to "AI slop" aesthetics without guidance:

```xml
<frontend_aesthetics>
Avoid generic "AI slop" aesthetics. Make creative, distinctive frontends.
Focus on:
- Typography: Choose beautiful, unique fonts. Avoid Arial, Inter, Roboto.
- Color: Commit to a cohesive aesthetic. Dominant colors with sharp accents.
  Use CSS variables. Draw from IDE themes and cultural aesthetics.
- Motion: Prioritize CSS-only animations. Focus on high-impact moments:
  one well-orchestrated page load with staggered reveals.
- Backgrounds: Create atmosphere and depth, not solid colors.

Interpret creatively and make unexpected choices. Vary between light/dark
themes, different fonts, different aesthetics across generations.
</frontend_aesthetics>
```

## Migration to Claude 4.6

### Key Changes

1. **Prefills deprecated** — use Structured Outputs or instructions instead
2. **Adaptive thinking replaces extended thinking** — use `effort` parameter
3. **Dial back aggressive tool prompts** — 4.6 overtriggers on CAPS/MUST language
4. **Be specific about desired behavior** — add modifiers for quality/detail
5. **Request features explicitly** — animations, interactions won't appear unless asked
6. **Anti-laziness prompts may backfire** — 4.6 is already proactive

### Sonnet 4.5 → Sonnet 4.6

- Set `effort` explicitly (default `high` may increase latency)
- `medium` for most applications; `low` for high-volume
- Set large `max_tokens` (64K recommended at medium/high effort)
- For coding: start with `medium` effort
- For chat/non-coding: start with `low` effort

### Extended → Adaptive Thinking Migration

```python
# Before (Sonnet 4.5)
thinking={"type": "enabled", "budget_tokens": 32000}

# After (Opus/Sonnet 4.6)
thinking={"type": "adaptive"},
output_config={"effort": "high"}
```

### When to Use Opus vs Sonnet 4.6

- **Opus 4.6**: Hardest problems, large-scale code migrations, deep research, extended autonomous work
- **Sonnet 4.6**: Fast turnaround, cost efficiency, most production workloads

## Migration to Claude Opus 4.7

### Breaking Changes (Must-Fix Before Pointing at 4.7)

1. **Legacy `thinking={"type": "enabled", "budget_tokens": N}` returns 400.** Migrate to `thinking={"type": "adaptive"}` + `output_config={"effort": ...}`. Same fix as 4.6, but on 4.7 it is enforced — no silent fallback.
2. **`token-efficient-tools-2025-02-19` beta header is dead.** It only ever applied to Claude 3.7 Sonnet. Built-in for all Claude 4 models — remove it from your client.
3. **New tokenizer changes token counts.** Re-run `/v1/messages/count_tokens` against any prompt where token cost or context-fit matters. Up to ~1.35× more text tokens, up to ~3× more image tokens at the new 2576px max edge.
4. **Cyber Verification gate.** Security-domain prompts (pen-test, vuln research, exploit dev) that worked on 4.6 may auto-refuse on 4.7 unless enrolled in the Cyber Verification Program.

### Behavioral Shifts (Likely Prompt Tweaks)

5. **Tool eagerness inverts.** 4.6 over-triggers (dial down `MUST`/`CRITICAL`); 4.7 *under*-triggers at low/medium effort. Lever: raise `effort` to `high`/`xhigh`, or be explicit about when tools are required.
6. **Fewer subagents by default.** Add an explicit `<subagent_policy>` block if your 4.6 setup relied on automatic delegation.
7. **More literal instruction following.** Promote implicit "first item" / "for example" patterns to explicit "for every item" rules.
8. **Less validation-forward voice.** If your product depended on 4.6's warmer register, audit voice/style prompts before switching.
9. **Post-tool summaries are skipped by default.** Add `After completing a task involving tool use, provide a brief summary of the work done.` if you need visibility.

### New Capabilities to Adopt

10. **`xhigh` effort** — new ceiling for hardest reasoning / long-running agents. `low` on 4.7 ≈ `medium` on 4.6, so many calls can be downgraded one notch.
11. **`task_budget`** (beta) — whole-loop token ceiling for agentic workloads, complementary to `effort`.
12. **Server-side compaction** (beta) — auto-summarizes earlier turns when conversations approach the context limit. Available on Opus 4.7, Opus 4.6, Sonnet 4.6.
13. **Managed Agents memory** (beta header `managed-agents-2026-04-01`) — sandboxed harness with multi-session memory.

### Recommended Effort Mapping (4.6 → 4.7)

| Current Opus 4.6 setting | Suggested Opus 4.7 start | Notes |
|---|---|---|
| `low` | `low` | Latency-sensitive chat / classification |
| `medium` | `low` | 4.7 `low` ≈ 4.6 `medium` for most workloads |
| `high` (default) | `high` (default) | Match for production agents |
| `high` (intelligence-sensitive coding/agents) | `xhigh` | New ceiling for hardest tasks |
| `high` (chronic timeouts) | `medium` + `task_budget` | Cap whole-loop cost instead of raising effort |

### Migration Checklist

1. Switch model string to `claude-opus-4-7`. Keep prompt and effort identical first.
2. Strip dead headers (`token-efficient-tools-2025-02-19`).
3. Replace any legacy `thinking.budget_tokens` blocks.
4. Re-run token counts for cost/context-fit-critical prompts.
5. Run evals. If results regress on tool-driven workloads, raise `effort` first; if results regress on tone, audit voice prompts; if results regress on generalization, promote implicit instructions to explicit ones.
6. Adopt `xhigh` and `task_budget` only after baseline parity is established.

### When to Use Opus 4.7 vs Opus 4.6

- **Opus 4.7**: New top-tier choice — hardest reasoning, longest-running agents, workloads where literal instruction-following or `task_budget` cost predictability matters.
- **Opus 4.6**: Continue to use for security-domain workflows pending Cyber Verification, for prompts that depend on 4.6's warmer voice, or where the new tokenizer's higher token count would push you past a budget.
- **Sonnet 4.6**: Fast turnaround, cost efficiency, most production workloads — unchanged recommendation.
