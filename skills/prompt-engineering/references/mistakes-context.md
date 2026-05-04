# Prompt Mistakes: Context Rot & "Lost in the Middle"

Condensed from "The Architecture of Instruction" (2026). Covers the U-shaped attention curve, RAG over-retrieval, naive data loading, and context engineering solutions.

## The "Lost in the Middle" Phenomenon

**Fallacy:** "More context is always better."

Transformer attention mechanisms have a finite "attention budget." As context grows, performance degrades via **context rot**.

### The U-Shaped Attention Curve

LLMs exhibit:
- **Primacy bias** — strong attention to information at the **beginning** of the prompt
- **Recency bias** — strong attention to information at the **end** of the prompt
- **Middle blindness** — information buried in the middle is frequently missed

Key finding: Performance on questions where the answer is in the middle of context is sometimes **worse than closed-book** performance (model without the context at all).

This affects all architectures, including models with 100K-200K token windows. The model technically processes all tokens, but **effective context** is much smaller. In practice: facts from the first ~1K tokens and last ~10K tokens are recalled well; directives at token 50K are missed.

## RAG Over-Retrieval

### The Problem

- Injecting 50 retrieved documents vs. 20 yields only ~1.5% accuracy improvement (GPT-3.5-Turbo study)
- Additional context forces reasoning over a vast "middle" section where attention is weakest
- Documents appended in retrieval order (decreasing relevance) place the most critical info in the middle — directly subverting primacy bias

### Naive Data Loading Anti-Pattern

Stuffing vast quantities of retrieved documents into the context window assuming the model will "filter the noise" is a common anti-pattern. Model performance saturates long before retriever recall does.

## Fixes

### 1. Strategic Information Placement

- **Critical instructions** → beginning and end of prompt
- **Supporting context** → middle sections (acceptable to partially miss)
- **Never bury key directives** in the middle of long contexts

### 2. RAG Pipeline Optimization

- **Ranked list truncation** — retrieve fewer, higher-signal documents (20 beats 50)
- **Strategic reranking** — force most relevant information to the beginning or end
- **Design RAG as a transparent pipeline**: indexing → query generation → retrieval → reranking → generation

### 3. Context Engineering (from Prompt Engineering to Context Engineering)

Replace static, monolithic prompts with dynamic, stateful systems:

| Principle | Old Approach | New Approach |
|-----------|-------------|--------------|
| **Examples over rules** | Edge-case laundry lists in system prompt | Curate diverse canonical few-shot examples that demonstrate behavior implicitly |
| **Just-in-time retrieval** | Stuff entire context upfront | Agents dynamically query and load data only when needed |
| **MCP** | Raw data in context | Standardized interface for external data sources, isolated until needed |

### 4. Memory Tools & Context Compaction

For long-horizon tasks:
- Use **file-based memory** (CRUD operations on `/memories` directory) — agent writes findings and patterns to external storage
- **Context editing** — automatically clear old tool results and intermediate reasoning when context grows too large
- Prevents critical early information from being lost; patterns from one session carry to the next

## Quick Decision Guide

| Context Size | Strategy |
|-------------|----------|
| < 4K tokens | Safe to use as-is |
| 4K-32K tokens | Place key info at start/end; summarize middle sections |
| 32K-100K tokens | Use just-in-time retrieval; limit RAG to top 10-20 documents |
| > 100K tokens | Mandatory: context compaction, memory tools, agent-based retrieval |

## References

- [3] Effective context engineering for AI agents (Anthropic)
- [20] Lost in the Middle: How Language Models Use Long Contexts (arXiv 2307.03172)
- [22] Your AI Agent Forgets Everything? (Medium)
- [24] Patterns and Anti-Patterns for Building with LLMs (Medium / Marvelous MLOps)
