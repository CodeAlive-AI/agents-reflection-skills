---
name: semantic-scholar-deep
description: Deep research over the Semantic Scholar Graph API. Covers endpoints missing from allenai's lookup skill — paper references (backward citations), recommendations, batch paper lookup (up to 500 IDs), snippet search, and multi-hop citation graph traversal (BFS forward/backward). Use when the user asks to build a citation graph, expand a literature seed, find related work, run a reference network traversal, explore what a paper cites or what cites it beyond simple lookup, or batch-resolve many DOI/arXiv/S2 IDs. For multi-step research questions, delegate to the deep-paper-researcher subagent to keep the main context clean. Not for single paper-by-ID lookups (use semantic-scholar-lookup) or topical discovery (use web_search_advanced_exa).
allowed-tools: Bash(python3:*), Read, Write, Edit, Glob, Grep, Agent
---

# Semantic Scholar — Deep Research

Purpose: fill the gaps that `semantic-scholar-lookup` (allenai) leaves — `references`, `recommendations`, `batch`, and multi-hop citation-graph traversal.

## Contents

- [Dispatch Rule](#dispatch-rule-read-first) — inline vs delegate; model selection
- [When to Use](#when-to-use) — trigger scenarios
- [Scripts](#scripts) — `ss_client.py` + `citation_graph.py`
- [Authentication & Rate Limits](#authentication--rate-limits)
- [Progressive Disclosure](#progressive-disclosure) — deeper references
- [Output Hygiene](#output-hygiene)
- [Integration](#integration) — typical pipeline with the subagent

## Dispatch Rule (read first)

Two execution modes:

### Inline (run the Bash scripts yourself)

Use when the user asks for **one specific endpoint**:
- "get references of paper X" → `ss_client.py references <id>`
- "recommendations for paper Y" → `ss_client.py recommendations <id>`
- "batch-resolve these 30 DOIs" → `ss_client.py batch ...`
- "find the snippet where X is said" → `ss_client.py snippets "..."`

Fast, cheap, no orchestration overhead.

### Delegate to `deep-paper-researcher` subagent

Use when the task is **multi-step** or would otherwise flood the context:
- Literature review on a topic
- Citation graph / network analysis around a seed paper
- Novelty check for an idea
- State-of-the-art survey
- Anything that requires merging Exa discovery + S2 graph + ranking

**Mandatory prompt contents.** The subagent runs in isolated context with no access to this conversation's system reminders. Include exactly these two things:

1. **Today's date** — inline as `Today is YYYY-MM-DD.` Pull from the `currentDate` system-reminder field, or run `date -I` via Bash before delegating if it's missing. Never rely on training-data intuitions about the current year.
2. **User's request, verbatim** — pass the user's original phrasing (topic + any freshness words like "современные / recent / классические / seminal" and any explicit dates like "since 2024"). Translate language if needed but do not paraphrase trigger words into date windows.

**Do NOT do any of these:**
- Do NOT classify freshness yourself (RECENT/FOUNDATIONAL/MIXED). The subagent does that from the verbatim user request.
- Do NOT invent a date window. If the user said "современные / recent / latest" without a year, the subagent defaults to last 6 months — don't preempt it with "2024-2026".
- Do NOT drop the trigger words. The subagent relies on them to pick the right mode.

Call:
```
Agent(
  subagent_type="deep-paper-researcher",
  description="<3–5 word task>",
  prompt="Today is 2026-04-22.\n\nUser's request: найди современные 10 статей про AI Code Review на arXiv.\n\n<optional: output format hints, language preference>"
  # model: "opus"  ← add only when the user opts in (see below)
)
```

The subagent's Freshness Mode section handles classification; keep this layer thin.

### Model selection (Sonnet default, Opus on demand)

The subagent's `model` frontmatter is `sonnet` — that's the default.

Override to Opus by passing `model: "opus"` to the `Agent` tool **only if the user explicitly requests deeper reasoning**. Triggers (any of):
- English: "deep dive", "thorough", "rigorous", "use Opus", "high quality", "comprehensive", "exhaustive"
- Russian: "глубокий/глубже", "тщательный/тщательно", "подробно", "в режиме Опус/Opus", "максимально качественно", "серьёзный ресерч"

Never auto-upgrade to Opus without a user signal — Sonnet handles the default literature-review workflow fine and costs less.

## When to Use

Trigger this skill for:
- **Citation graph / network** over a seed paper or topic
- **Backward references** (what does this paper cite?) — *not* covered by allenai
- **Forward citations** with pagination beyond 1000 results
- **Recommendations** — related-paper discovery from a seed
- **Batch lookup** — resolve 50-500 DOI/arXiv/CorpusId/S2 IDs in one call
- **Snippet search** — find specific passages across the S2 corpus

**Do NOT use** for:
- Simple "get paper by ID" or "who cited this" — use `semantic-scholar-lookup` (faster, no Python)
- Broad topical discovery — use `web_search_advanced_exa` with `category: "research paper"` (Exa MCP)
- Consumer-level literature questions — use the `deep-paper-researcher` subagent, which orchestrates all three tools

## Scripts

Located under `${SKILL_DIR}/scripts/`.

### `ss_client.py` — raw API client

Subcommands (all output JSON on stdout):

| Command | Endpoint | Notes |
|---------|----------|-------|
| `search <query>` | `/graph/v1/paper/search` | `--bulk` switches to `/search/bulk` (up to 1000/page) |
| `paper <id>` | `/graph/v1/paper/{id}` | ID forms: raw, `DOI:`, `ARXIV:`, `CorpusId:`, `PMID:`, `URL:` |
| `citations <id>` | `/graph/v1/paper/{id}/citations` | paginated; up to 1000 per page |
| `references <id>` | `/graph/v1/paper/{id}/references` | paginated; up to 1000 per page |
| `recommendations <id>` | `/recommendations/v1/papers/forpaper/{id}` | `--pool recent|all-cs` |
| `batch <id1> <id2> ...` | `POST /graph/v1/paper/batch` | up to 500 IDs |
| `author-search <query>` | `/graph/v1/author/search` | |
| `author <id>` | `/graph/v1/author/{id}` | |
| `author-papers <id>` | `/graph/v1/author/{id}/papers` | |
| `snippets <query>` | `/graph/v1/snippet/search` | Full-text snippets |

Common flags: `--limit`, `--offset`, `--fields`, `--year`, `--fields-of-study`, `--venue`, `--min-citation-count`.

### `citation_graph.py` — BFS traversal

```
python3 ${SKILL_DIR}/scripts/citation_graph.py <paperId> \
    --direction both \
    --depth 2 \
    --max-nodes 200 \
    --per-hop-limit 50 \
    --output graph.json
```

Directions: `forward` (citations), `backward` (references), `both`. Output schema described in the script docstring — `nodes: {paperId → metadata+depth}`, `edges: [{src, dst, direction}]`.

## Authentication & Rate Limits

- Without API key: ~1 RPS shared, 100 queries/5min bursts. Fine for small graphs.
- With `SEMANTIC_SCHOLAR_API_KEY` env var: much higher limits.
- Apply: https://www.semanticscholar.org/product/api#api-key
- The client does exponential backoff (1→30s) on HTTP 429/5xx, respects `Retry-After`.

## Progressive Disclosure

- `references/endpoints.md` — complete field list per endpoint + query examples
- `references/workflows.md` — lit-review, novelty-check, seed-expansion patterns

## Output Hygiene

Scripts emit raw JSON — redirect to files for anything beyond ~20 results. For graphs >50 nodes always pass `--output graph.json` to avoid flooding the conversation context.

## Integration

Typical pipeline inside the `deep-paper-researcher` subagent:

1. **Discovery** — `mcp__exa__web_search_advanced_exa` (neural + multi-source)
2. **ID resolution** — `ss_client.py search` / `batch` to get `paperId` from titles or DOIs
3. **Graph expansion** — `citation_graph.py` with the top 3-5 seeds
4. **Synthesis** — distill nodes/edges into a ranked report

## Optional: Bundled Subagent

A paired subagent definition ships alongside the skill at `agents/deep-paper-researcher.md`. It orchestrates Exa MCP + allenai `semantic-scholar-lookup` + this skill's scripts into a token-isolated research agent with:

- Mandatory input validation (today's date anchoring + caller-paraphrased-window detection)
- Freshness Mode classifier (RECENT / FOUNDATIONAL / MIXED)
- Sort-then-tiebreak ranking (never multiplies citations × recency into a single score)
- Compact report format with explicit `Anchor date` / `Mode` / `Window` header

To install for Claude Code (manual, one-time):

```bash
cp ~/.agents/skills/semantic-scholar-deep/agents/deep-paper-researcher.md ~/.claude/agents/
```

(Path may differ on other agents — copy to the agent's subagents directory, then restart the session.)

Prerequisites for full pipeline: Exa MCP connected, `allenai/asta-plugins@"Semantic Scholar Lookup"` skill installed.
