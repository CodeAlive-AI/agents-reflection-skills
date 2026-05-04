# semantic-scholar-deep

Deep research over the Semantic Scholar Graph API. Covers the endpoints missing from the official [allenai/asta-plugins](https://github.com/allenai/asta-plugins) `semantic-scholar-lookup` skill — backward **references**, **recommendations**, **batch** lookup (up to 500 IDs per call), **snippet** full-text search, and multi-hop **citation-graph BFS**.

## Install

```bash
npx skills add CodeAlive-AI/ai-driven-development@semantic-scholar-deep -g -y
```

Works anonymously out of the box — most endpoints (paper lookup, references, recommendations, batch) respond without an API key. The keyword `/paper/search` endpoint is heavily rate-limited on the anonymous tier, so for large sweeps set `SEMANTIC_SCHOLAR_API_KEY` (request one at <https://www.semanticscholar.org/product/api#api-key>).

## Prerequisites

This skill stands alone for scripts-only usage (invoke the Python CLIs directly). For the full **deep-research pipeline** (orchestrated by the bundled subagent, see below), you also need:

| Tool | Why | How |
|------|-----|-----|
| **Exa MCP** | Neural paper discovery across arXiv / OpenReview / PubMed / bioRxiv — the S2 `search` endpoint is too rate-limited to be the primary discovery path | `claude mcp add --transport http exa "https://mcp.exa.ai/mcp?tools=web_search_advanced_exa"` |
| **allenai `semantic-scholar-lookup` skill** | First-party `asta papers` CLI for fast metadata + forward citations (complements our backward-references / recommendations coverage) | `npx skills add "allenai/asta-plugins@Semantic Scholar Lookup" -g -y` |
| **Python 3.8+** | Scripts are stdlib-only, no pip install | Usually already present |

Without the above, the bundled subagent falls back to what it can reach (S2-only), but Exa dramatically improves discovery quality and freshness.

## Quick start

Inline usage (one specific endpoint):

```
> Get the references that DOI:10.18653/v1/N18-3011 cites
> Recommend 20 papers related to this paperId
> Batch-resolve these 30 arXiv IDs: 2404.18496 2502.02757 ...
> Build a citation graph of depth 2 around paperId X
```

Delegated usage (multi-step research via the bundled subagent):

```
> Find recent papers on LLM code review
> Do a literature review on retrieval-augmented generation since 2024
> Novelty check: is my idea <X> already published?
```

## What it ships

### Python CLIs (`scripts/`)

- **`ss_client.py`** — stdlib-only S2 client with exponential backoff on HTTP 429/5xx. Subcommands: `search`, `paper`, `citations`, `references`, `recommendations`, `batch`, `author-search`, `author`, `author-papers`, `snippets`.
- **`citation_graph.py`** — BFS traversal around a seed paper. Options: `--direction forward|backward|both`, `--depth N`, `--max-nodes N`. Outputs JSON with `nodes` + `edges`, designed for summarization rather than in-context dumping.

### References (`references/`)

- **`endpoints.md`** — complete field reference, query-parameter list, and ID-format matrix for every endpoint.
- **`workflows.md`** — 5 ready-made deep-research patterns: literature review from a topic, citation graph around a seed, novelty check, author trajectory, evidence for a claim.

### Bundled subagent (`agents/deep-paper-researcher.md`, optional)

A paired subagent definition for token-isolated research. Manually install once:

```bash
cp ~/.agents/skills/semantic-scholar-deep/agents/deep-paper-researcher.md ~/.claude/agents/
```

Then restart the session. Features:

- Input validation — today's date anchoring + caller-paraphrased-window detection (catches cases where the calling agent translates "recent" into an invented "2024-2026" window)
- Freshness Mode classifier — `RECENT` (default last 6 months, sort by publication date), `FOUNDATIONAL` (sort by citations, no date floor), `MIXED` (two slices side-by-side)
- Sort-then-tiebreak ranking — never multiplies `citations × recency` into a single score, so fresh papers with zero citations aren't buried under older high-citation ones
- Compact report format with explicit `Anchor date` / `Mode` / `Window` header — readers can see and redirect the choice

## Key design decisions

- **Stdlib only** — no `requests` dependency. Works on any Python 3.8+ install.
- **Backoff over hard-failure** — HTTP 429 / 5xx get exponential retry up to 30s, honoring `Retry-After`. Anonymous tier is usable for small graphs.
- **Progressive disclosure** — `SKILL.md` stays under 150 lines; deep endpoint-by-endpoint docs and workflow templates live in `references/`.
- **Token hygiene** — scripts emit raw JSON to stdout by design. For graphs >50 nodes, use `--output` to write to disk and summarize via `jq`/`python3` rather than piping full payloads into the agent's context.
- **Not a discovery engine** — keyword `search` works but is the weakest endpoint on the anonymous tier; the bundled subagent delegates discovery to Exa MCP and uses S2 for structured expansion (references, recommendations, batch).

## Rate limits

| Endpoint | Anonymous tier | With API key |
|----------|----------------|--------------|
| `paper` by ID | ~1 RPS, reliable | Much higher |
| `references` / `recommendations` | ~1 RPS, reliable | Much higher |
| `batch` (up to 500 IDs) | ~1 RPS | Much higher |
| `search` (keyword) | Frequently 429 | Reliable |

The client respects `Retry-After` and does up to 5 retries with exponential backoff (1→30s).

## File structure

```
semantic-scholar-deep/
├── SKILL.md                       # Agent-facing instructions (dispatch rule, when to use)
├── README.md                      # This file
├── scripts/
│   ├── ss_client.py              # Full S2 API client (stdlib only)
│   └── citation_graph.py         # BFS traversal
├── references/
│   ├── endpoints.md              # Per-endpoint field and parameter reference
│   └── workflows.md              # 5 deep-research patterns
└── agents/
    └── deep-paper-researcher.md  # Optional paired subagent definition
```

## License

MIT
