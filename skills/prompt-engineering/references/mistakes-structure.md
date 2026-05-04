# Prompt Mistakes: Structural Fragility & Anti-Patterns

Condensed from "The Architecture of Instruction" (2026). Covers formatting sensitivity, reproducibility crisis, prompt smells, and the deliberation ladder.

## Formatting Fragility

LLM performance is **extremely volatile** to meaning-preserving design changes:

- White space, capitalization, example ordering, instructional tone → can determine task success/failure
- In few-shot learning: formatting adjustments caused **up to 76 percentage points** accuracy difference on the same task (LLaMA-2-13B study)
- This variance persists regardless of model size, example count, or instruction tuning
- A format that maximizes one model's performance may suppress another's

**Implication:** Never assume a prompt "works" because it passed one test. Performance correlates weakly across formats and models.

**Fix — FormatSpread:** Evaluate a sampled set of plausible prompt formats for a given task. Report a performance interval rather than relying on a single prompt structure.

## The Reproducibility Crisis

Systematic analysis of 640 research papers (2017-2025) revealed persistent gaps in artifact availability and documentation:

- Highly specific prompt formatting + undisclosed environment → results impossible to reproduce
- Replication experiments on "advanced" techniques (EmotionPrompting, ExpertPrompting, CoT) across GPT-4o, Claude 3 Opus, Llama 3 showed **no statistically significant differences** in reasoning under double-checked benchmarks
- Many proclaimed prompt engineering "advances" may be artifacts of overfitting to formatting

### Reproducibility Smell Categories (RMM)

| Category | Problem |
|----------|---------|
| **Code & Execution** | Missing inference code; hidden pre/post-processing steps |
| **Data** | No train/test separation; data leakage inflates metrics |
| **Documentation** | Undocumented prompt structures, few-shot examples, formatting |
| **Environment & Tooling** | Unspecified library versions, frameworks (e.g., LangChain) |
| **Versioning** | Relying on continuous-release API endpoints without model hash/date |
| **Model & Access** | Proprietary closed-weight models preventing independent verification |

## Prompt Smells Catalog

Surface-level indicators of deeper architectural problems in prompts:

| Anti-Pattern | Description | Failure Mode |
|-------------|-------------|--------------|
| **Overloaded Context** | Excessive backstory, multiple tasks, edge-case laundry lists in one instruction | Token dilution, context rot — model ignores buried instructions |
| **Mixed Instruction Layers** | Tone + format schema + multi-step reasoning in the same sentence | Attention prioritizes wrong vector → malformed outputs |
| **Lack of Role Framing** | No persona, operational boundary, or professional context | Generalized default state → hallucinated/bland responses |
| **Ambiguous Objectives** | No explicit success criteria or task completion definition | Wandering outputs, "simulation distortion" |
| **Negative Instruction Bias** | Prompting mainly by "don't do X" instead of "do Y" | Increased ambiguity; LLMs process positive instructions more efficiently |
| **Monolithic Prompting** | Single 3000+ token prompt for complex multi-stage workflows | High latency, high cost, "lost in the middle" failures |

### Prompt Smells vs. Code Smells

- **Prompt smells** = semantic/linguistic deficiencies in the natural language prompt (imprecise language, overly large action spaces)
- **LLM code smells** = poor practices in the source code orchestrating the LLM (hardcoding brittle logic into prompts instead of using deterministic code for validation)

## The Deliberation Ladder

Framework for resolving monolithic, smelly prompts:

**Two layers of reliability:**
1. **Floor (Validity)** — enforce with deterministic code (Regex, JSON Schema) to block objective failures locally
2. **Ceiling (Quality)** — managed by the LLM

**Solution — Task Decomposition:**
- Break monolithic prompts into smaller, atomic pieces
- Chain multiple focused prompts: verified output of prompt N → input of prompt N+1
- Trade minor latency increase for massive gains in accuracy, reliability, and observability

## Prevention Checklist

1. **Test across formats** — don't rely on a single prompt format; try 3-5 variations
2. **One task per prompt** — split multi-task prompts into focused, atomic prompts
3. **Separate instruction layers** — role, tone, format, and reasoning in distinct sections (use XML tags)
4. **State what TO do** — minimize negative instructions; reserve "don't" only for hard safety rails
5. **Define success criteria** — every prompt should specify what a correct output looks like
6. **Validate deterministically** — use code (not prompts) for format validation, schema checking
7. **Document everything** — exact prompt text, model version, temperature, library versions for reproducibility
8. **Use the deliberation ladder** — deterministic floor (code) + quality ceiling (LLM)

## References

- [13] Quantifying LMs' Sensitivity to Spurious Features in Prompt Design (arXiv 2310.11324)
- [14] Comparative Analysis of Prompt Strategies: Single-Task vs. Multitask (MDPI)
- [17] LLMs for Software Engineering: A Reproducibility Crisis (arXiv 2512.00651)
- [18] A Looming Replication Crisis in Evaluating Behavior in LMs (arXiv 2409.20303)
- [25] Prompt Smells: An Omen for Undesirable AI Outputs (ResearchGate)
- [26] Specification and Detection of LLM Code Smells (arXiv 2512.18020)
- [28] Prompt Engineering is Technical Debt (Reddit r/LocalLLaMA)
