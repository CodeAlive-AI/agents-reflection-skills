# Semantic Scholar API — Endpoint Reference

## Contents

- [Paper IDs accepted everywhere](#paper-ids-accepted-everywhere)
- [Paper Fields](#paper-fields-subset-pass-comma-separated-via-fields)
- [`/paper/search`](#endpoint-papersearch) — keyword search
- [`/paper/search/bulk`](#endpoint-papersearchbulk) — large sweeps
- [`/paper/{id}`](#endpoint-paperpaper_id) — single paper
- [`/paper/{id}/citations`](#endpoint-paperpaper_idcitations) — forward
- [`/paper/{id}/references`](#endpoint-paperpaper_idreferences) — backward
- [`POST /paper/batch`](#endpoint-post-paperbatch) — up to 500 IDs
- [`/recommendations/v1/papers/forpaper/{id}`](#endpoint-recommendationsv1papersforpaperpaper_id)
- [`/author/*`](#endpoint-authorsearch-authorid-authoridpapers)
- [`/snippet/search`](#endpoint-snippetsearch)
- [Citation contexts / intents](#citation-contexts-and-intents)
- [Rate Limits](#rate-limits)

Base URLs:
- Graph API: `https://api.semanticscholar.org/graph/v1`
- Recommendations: `https://api.semanticscholar.org/recommendations/v1`

## Paper IDs accepted everywhere

| Form | Example |
|------|---------|
| S2 paper ID | `204e3073870fae3d05bcbc2f6a8e263d9b72e776` |
| CorpusId | `CorpusId:215416146` |
| DOI | `DOI:10.18653/v1/N18-3011` |
| arXiv | `ARXIV:2106.15928` |
| MAG | `MAG:112218234` |
| ACL | `ACL:W12-3903` |
| PubMed | `PMID:19872477` |
| PubMed Central | `PMCID:2323736` |
| URL | `URL:https://arxiv.org/abs/2106.15928v1` |

## Paper Fields (subset; pass comma-separated via `fields=`)

- `paperId`
- `externalIds` — `{DOI, ArXiv, CorpusId, MAG, ACL, PubMed, DBLP}`
- `url`, `openAccessPdf` — `{url, status}`
- `title`, `abstract`, `tldr` — `{model, text}`
- `venue`, `publicationVenue`, `publicationDate`, `year`
- `publicationTypes` — `JournalArticle | Conference | Review | ...`
- `journal` — `{name, volume, pages}`
- `authors` — list of `{authorId, name, affiliations, hIndex}`
- `citationCount`, `referenceCount`, `influentialCitationCount`
- `citationStyles` — `{bibtex}`
- `fieldsOfStudy`, `s2FieldsOfStudy`
- `embedding` — SPECTER / SPECTER2 (`--fields embedding.specter_v2`)

## Endpoint: `/paper/search`

Query a keyword. Relevance-ranked, up to 100 per page.

Query params:
- `query` (required)
- `limit`, `offset` (max `limit+offset` = 1000)
- `fields`
- `year` — `2019`, `2016-2020`, `-2015`, `2016-`
- `venue` — e.g. `Nature,Radiology`
- `fieldsOfStudy` — e.g. `Computer Science,Medicine`
- `publicationTypes` — e.g. `Review,JournalArticle`
- `openAccessPdf` — presence flag
- `minCitationCount` — int
- `publicationDateOrYear` — `YYYY-MM-DD:YYYY-MM-DD`

## Endpoint: `/paper/search/bulk`

Up to 1000 per page, continuation via `token`. Sorted by relevance/year — use for large sweeps.

## Endpoint: `/paper/{paper_id}`

Get single paper. All fields available. Use `fields=references.title,references.paperId` to embed shallow lists.

## Endpoint: `/paper/{paper_id}/citations`

Forward citations. Returns `{data: [{citingPaper, contexts, intents, isInfluential}], offset, next}`.
- `limit` up to 1000
- `fields` applied to the `citingPaper` sub-object

## Endpoint: `/paper/{paper_id}/references`

Backward references. Same shape as citations but `citedPaper` instead of `citingPaper`.

## Endpoint: `POST /paper/batch`

Body: `{"ids": ["<id>", ...]}` — up to 500 IDs per request.
Query param: `fields` (comma-separated).
Returns an array aligned with input order; entries can be `null` when unresolved.

## Endpoint: `/recommendations/v1/papers/forpaper/{paper_id}`

Related papers.
- `limit` up to 500
- `from=recent` (default) or `from=all-cs`
- `fields` applied to recommended papers

POST variant: `/recommendations/v1/papers` with `{positivePaperIds, negativePaperIds}` — better signal for curated seeds.

## Endpoint: `/author/search`, `/author/{id}`, `/author/{id}/papers`

Author fields: `authorId`, `name`, `affiliations`, `aliases`, `homepage`,
`paperCount`, `citationCount`, `hIndex`, `papers.{...}`.

## Endpoint: `/snippet/search`

Full-text snippet search across the S2 corpus.
Params: `query`, `limit`. Returns snippets with `section`, `text`, `paperId`, `score`.

## Citation `contexts` and `intents`

When listing citations/references include `fields=contexts,intents,isInfluential`:
- `contexts` — array of text snippets where citation appears
- `intents` — `background | method | result`
- `isInfluential` — boolean from S2's influence model

These are the payload for fine-grained citation analysis (who cites *for what purpose*).

## Rate Limits

- Anonymous: ~1 RPS shared, 100 req / 5min bursts.
- Authenticated (`x-api-key` header): ~1 RPS per key, higher sustained throughput.
- On `429` the server sets `Retry-After`. The client honors it with exponential fallback.
