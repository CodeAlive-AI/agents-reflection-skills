# Prompt Mistakes: Hallucinations & Logical Failures

Condensed from "The Architecture of Instruction" (2026). Covers cognitive biases, hallucinations, logical degradation, and ambiguity-induced failures.

## How Hallucinations Happen

LLMs don't reason — they predict statistically likely next tokens. When a prompt lacks clear contextual boundaries or contains conflicting instructions, the model **confabulates** to bridge semantic gaps. This mirrors human cognitive biases: the brain uses heuristics for incomplete information, LLMs use learned statistical associations.

**Key risk — Automation Bias:** Humans tend to uncritically accept AI-generated outputs over their own judgment. Combined with hallucination, this creates a compounding failure mode in production systems.

## Root Causes

| Cause | Mechanism | Impact |
|-------|-----------|--------|
| **No role framing** | Model stays in generalized default state | Bland, uncertain, or hallucinatory responses |
| **Ambiguous objectives** | No explicit success criteria or task definition | Wandering outputs, "simulation distortion" |
| **Overloaded prompts** | Multiple instructional layers (tone + format + reasoning) in one directive | Attention prioritizes wrong vector — e.g., generates explanation instead of verifying code |
| **Persona without boundaries** | Assigned role activates training data biases associated with that persona | Implicit biases leak into outputs |

## Logical Failures in Verification Tasks

Research shows that **more complex prompting strategies can degrade logical accuracy** in verification tasks (code review, diagnostics):

- Asking an LLM to verify code AND explain AND propose corrections simultaneously → higher misjudgment rate
- Model misclassifies correct code as defective because it focuses computational resources on generating the explanation rather than verifying against the spec
- Without clear role separation, cross-verification, and termination checks, logical errors cascade

**Fix:** Separate verification from explanation. Use one prompt for "is this correct?" and a second for "explain why / suggest fixes."

## Clinical Medicine Findings

Empirical study on LLM agreement with AAOS evidence-based guidelines for osteoarthritis:

| Strategy | Mechanism | Consistency |
|----------|-----------|-------------|
| **Input-Output (IO)** | Direct instruction, no reasoning steps | Lowest — as low as 4.7% |
| **Zero-Shot CoT** | "Think step by step" | Inconsistent on nuanced evidence levels |
| **Reflection of Thoughts (ROT)** | Multi-expert simulation with backtracking | 62.9% overall, 77.5% for strong recommendations |

**Takeaway:** Naive prompts are unreliable for complex reasoning. Structured multi-step techniques (ROT, self-consistency) significantly improve reliability.

## Prevention Checklist

1. **Always assign a role** with explicit operational boundaries — but constrain the persona to avoid training data bias
2. **State success criteria explicitly** — what does a "correct" output look like?
3. **Separate instructional layers** — don't stack tone, format, reasoning, and verification into one sentence
4. **Use multi-step verification** — verify first, explain second
5. **For high-stakes domains** — use Reflection of Thoughts or Self-Consistency rather than basic CoT
6. **Anchor to provided context** — use "Based on the provided data..." to reduce confabulation
7. **Never trust without verification** — always validate LLM outputs against ground truth in production

## References

- [4] AI Hallucinations and Cybersecurity (Arthur Lawrence)
- [7] Both humans and AI hallucinate — but not in the same way (CSIRO)
- [8] Prompt Engineering Debugging: 10 Most Common Issues (Reddit)
- [10] Systematic Failures of LLMs in Verifying Code (arXiv 2508.12358)
- [11] Large Language Model Reasoning Failures (arXiv 2602.06176)
- [12] Prompt engineering in consistency and reliability with evidence (PMC)
