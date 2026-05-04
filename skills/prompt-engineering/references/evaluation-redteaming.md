# Evaluation Metrics, Red-Teaming & Tooling

Condensed from "Prompt Engineering Failures" deep research report. Covers evaluation metrics by failure mode, red-teaming workflows, tooling ecosystem, CI gating, and open research questions.

## Core Principle

Prompt engineering quality is not measurable with a single score. Mature practice uses a **portfolio of metrics and test suites** aligned to failure modes.

## Evaluation Metrics by Failure Mode

### Factuality / Hallucination

| Tool/Benchmark | What It Measures | How It Works |
|---------------|-----------------|--------------|
| **TruthfulQA** | Truthfulness under misconception pressure | Short-form Q&A; measures "imitative falsehoods" — false answers learned from human text |
| **FActScore** | Atomic factual accuracy in long-form text | Decomposes generations into checkable claims; scores each against sources |
| **SelfCheckGPT** | Hallucination detection via instability | Sampling-based self-consistency; unstable claims across samples indicate hallucination |

### Robustness / Brittleness

| Tool/Benchmark | What It Measures |
|---------------|-----------------|
| **PromptRobust** | Performance under systematic prompt perturbations |
| **PromptBench** | Performance spread across format/wording variations |

Both systematically perturb prompts and measure output variance. Use as regression tests.

### Safety & Security

| Tool/Benchmark | What It Measures |
|---------------|-----------------|
| **OWASP Top 10 for LLMs** | Operational taxonomy: injection, insecure output handling as primary risk classes |
| **MLCommons AILuminate** | Safety/security hazard taxonomy with large standardized prompt sets |

### LLM-as-a-Judge

LLM-based evaluation (rubric scoring with a strong model) is popular but has recognized issues:
- **Verbosity bias** — judges prefer longer outputs
- **Position bias** — judges prefer outputs in certain positions
- **Self-enhancement bias** — models rate their own outputs higher
- **Language/task variance** — reliability varies across languages and domains

Use meta-evaluation benchmarks and debiasing strategies. "Judge correctness" remains a moving target.

## Tooling Ecosystem

Four practical tool categories:

### 1. Eval Harnesses & CI-Friendly Testing

CI-gated prompt testing — treat prompt changes like code changes:
- Store eval fixtures alongside prompt templates
- Run automated evals on every prompt change
- Set pass/fail thresholds before deployment
- Track metrics over time for drift detection

### 2. Red-Teaming Frameworks

Systematic probing for safety and injection issues:
- Generate harmful test cases using models themselves (scales coverage beyond manual tests)
- Automated adversarial prompt generation for transferable jailbreak-like prompts
- Assume adaptive attackers — static defenses are insufficient

### 3. Guardrail / Policy Enforcement

Programmable input/output checks:
- PII detection and redaction
- Toxicity classification
- Jailbreak pattern detection
- Structured output enforcement
- Policy compliance validation

### 4. Observability & Online Evaluation

Trace and evaluate agentic workflows in production:
- Retrieval quality monitoring
- Tool correctness validation
- Policy compliance checking
- Catches "works on prompts, fails in orchestration" problems

## CI Workflow for Prompt Development

```
Define task + acceptance criteria
    ↓
Draft prompt template + output schema
    ↓
Build eval set: gold + adversarial + edge cases
    ↓
Run automated evals in CI
    ↓
Pass thresholds? → No → back to drafting
    ↓ Yes
Deploy behind feature flag
    ↓
Monitor: drift, safety, leakage, cost
    ↓
Periodic red-team + update evals
    ↓
(cycle back to eval set)
```

**You cannot "prompt your way out" of missing tests and monitoring.**

## System-Level Controls

For detailed defense strategies (input sanitization, privilege separation, prompt hardening, output validation, multi-layer defense), see [mistakes-security.md](mistakes-security.md).

**Key principle not covered elsewhere:** Prompt engineering is **complementary to**, not a replacement for, training-time alignment (RLHF, Constitutional AI). In high-risk domains, both are required.

## Open Research Questions

| Question | Status | Why It Matters |
|----------|--------|---------------|
| **Robust instruction/data separation** | No universal solution | Indirect injection persists because LLMs treat text as single channel |
| **Secure agentic tool use** | Active research | Attack surface expands with more tools (output injection, permission misuse, supply-chain, covert channels) |
| **Faithful, monitorable reasoning** | Actively explored | CoT can be unfaithful; affects safety (detecting risky behavior) and usability (trusting explanations) |
| **Eval under distribution shift** | Emerging standards | Static benchmarks saturate and get contaminated; dynamic approaches proposed but not standardized |
| **Reliable LLM-as-a-judge** | Moving target | Systematic biases persist; meta-evaluation benchmarks and debiasing converging |
| **Regulatory alignment** | Evolving | Legal treatment of AI outputs, training data, privacy varies across jurisdictions (EU AI Act, US Copyright Office) |

## References

- TruthfulQA benchmark (truthfulness under misconception pressure)
- FActScore (atomic fact scoring for long-form text)
- SelfCheckGPT (sampling-based hallucination detection)
- PromptRobust, PromptBench (robustness benchmarks)
- OWASP Top 10 for LLM Applications
- MLCommons AILuminate benchmark family
- OpenAI Evals framework
- NeMo Guardrails, Llama Guard
- InstructGPT, Constitutional AI (training-time alignment)
- EU AI Act, US Copyright Office reports
