# Deep-Research Workflows

## Contents

- [Workflow 1: Literature Review from a Topic](#workflow-1-literature-review-from-a-topic)
- [Workflow 2: Citation Graph around a Seed Paper](#workflow-2-citation-graph-around-a-seed-paper)
- [Workflow 3: Novelty Check for an Idea](#workflow-3-novelty-check-for-an-idea)
- [Workflow 4: Author Trajectory](#workflow-4-author-trajectory)
- [Workflow 5: Evidence for a Claim](#workflow-5-evidence-for-a-claim)
- [Token Hygiene](#token-hygiene)
- [Failure Modes](#failure-modes)

## Workflow 1: Literature Review from a Topic

1. **Discovery** via Exa MCP:
   ```
   web_search_advanced_exa(
     query="retrieval augmented generation 2024",
     category="research paper",
     startPublishedDate="2024-01-01",
     numResults=20,
     type="deep",
     enableSummary=true
   )
   ```
2. Extract DOI/arXiv IDs from Exa results (domain URL parsing).
3. **Batch-resolve** to S2 IDs:
   ```
   python3 ss_client.py batch DOI:10.1145/... ARXIV:2401.12345 ... \
       --fields paperId,title,year,citationCount,tldr
   ```
4. Sort by `citationCount`, pick top 5 seeds.
5. **Expand each seed** via recommendations:
   ```
   python3 ss_client.py recommendations <seedId> --limit 30
   ```
6. Merge + de-dup by `paperId`.
7. Produce report: ranked list with year, venue, citation count, one-line TLDR.

## Workflow 2: Citation Graph around a Seed Paper

Given a single anchor paper (user provides DOI or title):

1. Resolve to S2 ID:
   ```
   python3 ss_client.py paper DOI:10.xxxx --fields paperId,title,year,citationCount
   ```
2. Build the graph:
   ```
   python3 citation_graph.py <paperId> \
       --direction both --depth 2 --max-nodes 150 --output graph.json
   ```
3. Analyze `graph.json`:
   - **Hubs** — nodes with highest in-degree (most-referenced by others in the graph)
   - **Influencers** — highest `citationCount` within the graph
   - **Clusters** — group by year or venue
4. Present top 10 papers per category + one-sentence rationale per pick.

## Workflow 3: Novelty Check for an Idea

User describes an idea in ≤3 sentences; confirm prior art exists.

1. Extract 3-5 keyword groups from the description.
2. For each group, run:
   ```
   python3 ss_client.py search "<group>" --limit 10 --year 2020- \
       --min-citation-count 5
   ```
3. Deduplicate across groups by `paperId`.
4. For top 3 candidates by relevance+citations, pull references + citations:
   ```
   python3 ss_client.py references <id> --limit 20
   python3 ss_client.py citations <id> --limit 20
   ```
5. Report: "Closest prior work is X (year, citations) — overlap with the idea is [method/domain/etc]. Gap to user's idea: [...]".

## Workflow 4: Author Trajectory

1. `author-search` to resolve a name to `authorId`:
   ```
   python3 ss_client.py author-search "Geoffrey Hinton"
   ```
2. `author-papers` with `--limit 200` to pull career history.
3. Group by year; plot topical drift via `fieldsOfStudy`.

## Workflow 5: Evidence for a Claim

1. `snippets` to find exact passages:
   ```
   python3 ss_client.py snippets "attention scales quadratically with sequence length"
   ```
2. For each hit, fetch full paper metadata:
   ```
   python3 ss_client.py paper <paperId> --fields paperId,title,year,venue,tldr,authors
   ```
3. Rank by venue quality + recency.

## Token Hygiene

- Never return raw `graph.json` (>50 nodes) into the main conversation — summarize or extract the top-N.
- Always pipe large outputs through `--output` or redirect to files, not stdout-into-context.
- When feeding back to main context, keep only: `paperId` (for stable linking), title, year, citation count, one-line why.

## Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `HTTP 404` on paper lookup | wrong ID prefix | try `DOI:`, `ARXIV:`, `CorpusId:`, or URL form |
| `HTTP 429` persistently | rate limit or missing key | set `SEMANTIC_SCHOLAR_API_KEY` env var |
| Empty `data` for citations | paper too new or not cited yet | confirm with `paper <id>` that `citationCount > 0` |
| `references.data[i].citedPaper == null` | external paper not in S2 corpus | filter nulls before traversal |
| Graph explodes past `max-nodes` | seed is a very popular paper | lower `--per-hop-limit` and `--depth` |
