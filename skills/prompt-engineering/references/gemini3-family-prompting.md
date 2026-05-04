# Gemini 3 Family Prompting Guide

Covers Gemini 2.5 Pro/Flash and Gemini 3/3.1 Pro. Based on official Google AI documentation and production patterns.

Sources:
- [Gemini 3 Prompting Guide — Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)
- [Gemini API Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Gemini 3 Prompt Practices — Philipp Schmid](https://www.philschmid.de/gemini-3-prompt-practices)
- [Gemini Thinking Mode](https://ai.google.dev/gemini-api/docs/thinking)
- [Function Calling — Gemini API](https://ai.google.dev/gemini-api/docs/function-calling)
- [Structured Output — Gemini API](https://ai.google.dev/gemini-api/docs/structured-output)
- [Gemini API Cookbook](https://github.com/google-gemini/cookbook)

## Model Comparison

| Aspect | Gemini 2.5 Flash | Gemini 2.5 Pro | Gemini 3 Pro | Gemini 3.1 Pro |
|--------|-----------------|----------------|-------------|----------------|
| Thinking control | `thinking_budget` (tokens) | `thinking_budget` (tokens) | `thinking_level` (LOW/HIGH) | `thinking_level` (LOW/HIGH) |
| Default thinking | Dynamic (-1) | Dynamic (-1) | HIGH | HIGH |
| Context window | 1M tokens | 1M tokens | 1M tokens | 1M tokens |
| Key strength | Speed + image gen | Complex reasoning | Direct instruction following | 2x abstract reasoning vs 3.0 |
| Verbosity | Normal | Normal | Less verbose by default | Less verbose by default |
| Temperature | 1.0 (recommended) | 1.0 (recommended) | **1.0 (critical)** | **1.0 (critical)** |

## Critical: Temperature for Gemini 3

**Keep temperature at 1.0.** Lowering temperature below 1.0 may lead to unexpected behavior, looping, or degraded performance, particularly with complex mathematical or reasoning tasks.

This is a significant difference from other model families where lower temperature = more deterministic. Gemini 3's reasoning is optimized specifically for temperature 1.0.

## Thinking Mode Configuration

### Gemini 2.5 (Token-Based Budget)

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=1024)
    )
)
```

| Parameter | Range | Notes |
|-----------|-------|-------|
| `thinking_budget` | 0 – 24,576 | Token count for reasoning |
| `-1` | Dynamic | Auto-adjusts to query complexity (recommended for production) |
| `0` | Disabled | Flash only; Flash-Lite minimum is 512 |

### Gemini 3 (Categorical Level)

```python
response = client.models.generate_content(
    model="gemini-3-pro",
    contents="Your prompt",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="LOW")
    )
)
```

| Level | Use Case |
|-------|----------|
| `LOW` | Simple tasks, lower latency |
| `HIGH` | Complex reasoning (default) |

**Incompatibility warning:** Using `thinking_budget` with Gemini 3 or `thinking_level` with Gemini 2.5 returns an API error.

For lower latency with Gemini 3, combine `thinking_level="LOW"` with system instruction "think silently."

## Constraint Placement Strategy

Gemini 3 may drop constraints placed too early. Structure prompts accordingly:

### Standard Prompts (Short Context)
```
[Role / System Instruction]     ← Behavioral anchor
[Core request / Main task]      ← What to do
[Negative constraints]          ← What NOT to do (last)
[Formatting / quantitative]     ← Output shape (last)
```

### Long Context Prompts (>10k tokens)
```
[Context / Source material]     ← Data first
[Main task instructions]        ← Middle
[Critical restrictions]         ← END (prevents dropping)
```

**Key rule:** Place critical restrictions as the final line of instruction. Complex requests may silently drop constraints that appear too early.

## Core Prompting Patterns

### 1. Directness Over Verbosity

Gemini 3 favors directness. Don't pad prompts with unnecessary persuasion or explanation:

```
# Bad
I would really appreciate it if you could please help me analyze this data.
It would be wonderful if you could provide a thorough and comprehensive
analysis with detailed explanations...

# Good
Analyze this dataset. Output: summary table + 3 key insights.
```

### 2. Consistent Structure

Choose XML tags OR Markdown headings and stick with one. Don't mix.

**XML approach:**
```xml
<role>You are a data extractor.</role>
<instructions>Extract all dates and amounts from the text.</instructions>
<constraints>Output JSON only. No explanations.</constraints>
<output_format>{"dates": [], "amounts": []}</output_format>
```

**Markdown approach:**
```markdown
# Identity
You are a data extractor.

# Instructions
Extract all dates and amounts from the text.

# Constraints
- Output JSON only
- No explanations

# Output Format
{"dates": [], "amounts": []}
```

### 3. Explicit Term Definition

Don't assume model shares your understanding of domain terms:

```
# Bad
Classify the sentiment.

# Good
Classify the sentiment as one of: positive, negative, neutral, mixed.
"Mixed" means the text contains both positive and negative elements
with roughly equal weight.
```

### 4. Deduction vs. External Knowledge

Avoid broad negatives like "do not infer." Instead, be specific:

```xml
<instructions>
You are expected to perform calculations and logical deductions based
strictly on the provided text. Do not introduce external information.
</instructions>
```

Open-ended instructions like "do not infer" may cause failures at basic logic.

### 5. Split-Step Verification

For topics without sufficient information:

```
Step 1: Check if the provided context contains information about [topic].
Step 2: If yes, answer based only on that context. If no, state that
the information is not available in the provided context.
```

### 6. Persona Seriousness

Gemini 3 takes assigned personas very seriously, sometimes prioritizing them over conflicting instructions. Use this deliberately:

```xml
<role>
You are a data extractor. You are forbidden from clarifying, explaining,
or expanding terms. Output text exactly as it appears.
</role>
```

### 7. Grounding in Hypothetical Context

When context contradicts real-world facts:

```
You are a strictly grounded assistant limited to the information provided
in the User Context. Treat the provided context as the absolute limit
of truth. Do not supplement with external knowledge.
```

### 8. Multi-Source Synthesis

For long documents, anchor reasoning after context:

```
[... lengthy document ...]

Based on the entire document above, provide a comprehensive answer.
Synthesize all relevant information from all sections.
```

## System Instruction Template

```xml
<role>
You are Gemini 3, a specialized assistant for [Domain].
You are precise, analytical, and persistent.
</role>

<instructions>
1. Plan: Create step-by-step plans, decompose into subtasks
2. Execute: Carry out plans; reflect before tool calls
3. Validate: Review output against user tasks
4. Format: Present answers in requested structures
</instructions>

<constraints>
- Verbosity: [Low/Medium/High]
- Tone: [Formal/Casual/Technical]
- Handling Ambiguity: Make reasonable assumptions; state them
</constraints>
```

### Security Note

System instructions don't fully prevent jailbreaks or leaks. They guide but don't guarantee compliance. Exercise caution with sensitive information.

## Function Calling Best Practices

### Tool Descriptions

Clear descriptions directly impact model's ability to select the right tool:

```python
# Bad
tools = [{"name": "get_data", "description": "Gets data"}]

# Good
tools = [{
    "name": "get_stock_price",
    "description": "Retrieves the current stock price for a given ticker symbol. "
                   "Use when the user asks about stock prices or market data.",
    "parameters": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "Stock ticker symbol, e.g., 'AAPL', 'GOOGL'"
            }
        },
        "required": ["ticker"]
    }
}]
```

### Key Rules

- **Limit active tools**: Keep to 10–20 maximum per request. More tools = higher chance of wrong selection
- **Use enums**: For fixed-value parameters, constrain with enums
- **Parameter examples**: Include examples in parameter descriptions
- **Error handling**: Return meaningful error messages to model; wrap execution in error handling
- **Mode**: Use `AUTO` (default) — model decides whether to call a function or respond directly

### Multiple Function Calls

Gemini can issue multiple function calls in a single turn:
- Execute functions asynchronously
- Results mapped back via `tool_use_id`
- Don't need to return results in same order

### Prompting for Tools

```
You are a helpful weather assistant. Use the get_weather function to look up
current conditions. Don't guess dates; always use a future date for forecasts.
```

## Structured Output / JSON Mode

### Schema Design

```python
response = client.models.generate_content(
    model="gemini-3-pro",
    contents="Extract entities from this text...",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Entity name"},
                            "type": {"type": "string", "enum": ["PERSON", "ORG", "LOCATION"]},
                            "confidence": {"type": "number", "description": "0.0 to 1.0"}
                        },
                        "required": ["name", "type"]
                    }
                }
            }
        }
    )
)
```

### Key Guidelines

- **Field names matter**: Use clear, intuitive names; they influence model output quality
- **Use descriptions**: Add `description` field inside schema properties
- **Syntactic vs semantic**: Structured output guarantees valid JSON syntax but NOT semantic correctness. Always validate in application code
- **Schema complexity limits**: Complex schemas can cause `InvalidArgument` errors

### Reducing Schema Complexity

If getting errors, try:
- Shorten property/enum names
- Flatten nested arrays
- Reduce optional properties
- Reduce enum values count
- Simplify nested objects

## Agentic Patterns

### Core Agent Loop

```
Observe → Think → Act → Observe (repeat until task complete)
```

### Components
1. **Model (Brain)**: Reasons through ambiguity, plans, decides when external help needed
2. **Tools (Hands)**: Functions the agent can execute
3. **Context/Memory**: Information accessible at any moment
4. **Loop**: The observe-think-act cycle

### Reflection / Self-Correction

```xml
<planning_process>
1. Parse all goals and sub-goals
2. Validate information completeness
3. Identify solutions beyond standard approaches
4. Create structured outline
5. Validate understanding before proceeding
</planning_process>

<output_critique>
Before responding, verify:
- Intent understanding: accurate?
- Tone: authentic, not corporate?
- Assumptions: all flagged?
</output_critique>
```

### Self-Updating TODO Tracker

```
Progress:
- [x] Parse input data
- [x] Identify key entities
- [ ] Generate analysis
- [ ] Format output
```

### Safety Measures

- **Max iterations**: Implement `max_iterations` breaks (e.g., 15 turns)
- **Guardrails**: Use `system_instruction` with hard rules or external classifiers
- **Human-in-the-loop**: For sensitive actions (send_email, execute_code), require user confirmation

## Multimodal Prompting

### Media Order

For single-media prompts, add the media first, then the text prompt.

### Best Practices

1. **Be specific about visual elements**: "Describe the bar chart showing quarterly revenue" not just "describe the image"
2. **Few-shot with multimodal**: Provide input-output pairs including visual examples
3. **Step-by-step for visual reasoning**: "Think step by step" for tasks combining visual + reasoning
4. **Cross-modal references**: Explicitly instruct model to synthesize across modalities rather than isolate them

### Media Capabilities

| Media | Capabilities |
|-------|-------------|
| Images | Captioning, VQA, comparing, object detection, text detection |
| Audio | Transcription, chapterization, key event detection, translation |
| Video | Audio+visual simultaneous processing, descriptions, QA |

## Context Window Management

### Strategy: Use 70–80% Max

Accuracy drops near the limit. Target 70–80% of the full context window.

### Context Caching

Most effective cost optimization. Cache frequently reused context (system instructions, reference docs).

### Long Context Tips

- Pre-summarize long files before analysis
- Chain tasks logically instead of one giant prompt
- Use RAG for datasets exceeding context limits
- Set reasonable `max_output_tokens`
- Use streaming for long outputs

## Gemini vs GPT: Key Prompting Differences

| Aspect | Gemini | GPT-5.* |
|--------|--------|---------|
| Temperature | **Must be 1.0** for Gemini 3 | Standard 0.0–2.0 range |
| Thinking control | Token budget (2.5) or categorical level (3) | `reasoning_effort` parameter |
| Context window | 1M–2M tokens | 128K–200K tokens |
| Constraint placement | End of prompt (critical) | Throughout (XML tags) |
| Verbosity default | Direct, less verbose (Gemini 3) | Varies by model version |
| Multimodal | Native multimodal with video + audio | Text + images primarily |
| Structured output | `response_mime_type` + schema | `response_format` + JSON schema |
| System instructions | Separate API field; persist across turns | Part of conversation; `instructions` field |
| Tool selection | AUTO mode; 10–20 tool limit recommended | Flexible; supports allowlists |

## Domain-Specific Patterns

### Research & Analysis

```xml
<instructions>
- Decompose topic into research questions
- Analyze sources independently
- Synthesize findings
- Every claim must be immediately followed by a reference [Source ID]
</instructions>
```

### Creative Writing

```xml
<constraints>
- Identify target audience and goals
- Avoid corporate jargon ("synergy", "protocols", "ensure") when empathy is needed
- Read drafts internally for humanity before outputting
</constraints>
```

### Problem-Solving

```xml
<instructions>
1. Restate the problem in your own words
2. Identify standard solutions
3. Identify "power user" solutions beyond standard approaches
4. Prioritize effective methods over requested format
5. Sanity-check solutions before presenting
</instructions>
```

### Error Handling

```xml
<error_handling>
If required information is missing:
- DO NOT attempt to generate a solution
- DO NOT make up data
- Output a polite request for the missing information
</error_handling>
```

## Image Generation (Gemini 2.5 Flash)

### Prompt Structure for Images

```
Subject: [what must be in-frame]
Composition: [framing, background, depth of field]
Lighting/Camera: [time of day, style, lens notes]
Style/References: [visual style, art movements, color palette]
```

### Key Tips

- Use photographic/cinematic language (camera angles, lens types, lighting)
- Be hyper-specific: "ornate elven plate armor, etched with silver leaf patterns" not "fantasy armor"
- Use descriptive narratives, not disconnected keywords
- Include "Do not change the input aspect ratio" when editing
- Iterate conversationally to refine results
