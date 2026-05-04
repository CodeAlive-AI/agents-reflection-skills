#!/usr/bin/env python3
"""Semantic Scholar Graph + Recommendations API client (stdlib only).

CLI:
    python3 ss_client.py search "attention is all you need" --limit 10
    python3 ss_client.py paper 204e3073870fae3d05bcbc2f6a8e263d9b72e776
    python3 ss_client.py citations <paperId> --limit 100
    python3 ss_client.py references <paperId> --limit 100
    python3 ss_client.py recommendations <paperId> --limit 20
    python3 ss_client.py batch <id1> <id2> ... --fields paperId,title,year,citationCount
    python3 ss_client.py author-search "Ashish Vaswani"
    python3 ss_client.py author <authorId>
    python3 ss_client.py snippets "retrieval augmented generation"

Env:
    SEMANTIC_SCHOLAR_API_KEY — optional; higher rate limits when set.

All commands print JSON to stdout. Non-zero exit on terminal errors.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

GRAPH_BASE = "https://api.semanticscholar.org/graph/v1"
RECS_BASE = "https://api.semanticscholar.org/recommendations/v1"

DEFAULT_PAPER_FIELDS = (
    "paperId,title,abstract,year,venue,authors,citationCount,"
    "referenceCount,influentialCitationCount,externalIds,openAccessPdf,tldr"
)
LIGHT_PAPER_FIELDS = "paperId,title,year,authors.name,citationCount,venue"


class SemanticScholarError(RuntimeError):
    pass


def _headers() -> dict[str, str]:
    h = {"User-Agent": "semantic-scholar-deep/1.0"}
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        h["x-api-key"] = api_key
    return h


def _request(
    method: str,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: Any = None,
    timeout: int = 30,
    max_retries: int = 5,
) -> Any:
    if params:
        cleaned = {k: v for k, v in params.items() if v is not None}
        if cleaned:
            url = f"{url}?{urllib.parse.urlencode(cleaned, doseq=True)}"

    data: bytes | None = None
    headers = _headers()
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, method=method, headers=headers)

    backoff = 1.0
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                return json.loads(body) if body else None
        except urllib.error.HTTPError as e:
            if e.code == 429 or 500 <= e.code < 600:
                if attempt == max_retries:
                    raise SemanticScholarError(
                        f"HTTP {e.code} after {max_retries} retries: {url}"
                    ) from e
                retry_after = e.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else backoff
                time.sleep(wait)
                backoff = min(backoff * 2, 30)
                continue
            raise SemanticScholarError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e
        except urllib.error.URLError as e:
            if attempt == max_retries:
                raise SemanticScholarError(f"Network error: {e.reason}") from e
            time.sleep(backoff)
            backoff = min(backoff * 2, 30)


def search(
    query: str,
    *,
    limit: int = 20,
    offset: int = 0,
    fields: str = DEFAULT_PAPER_FIELDS,
    year: str | None = None,
    fields_of_study: str | None = None,
    venue: str | None = None,
    min_citation_count: int | None = None,
    open_access_pdf: bool = False,
    bulk: bool = False,
) -> dict:
    path = "/paper/search/bulk" if bulk else "/paper/search"
    params = {
        "query": query,
        "limit": min(limit, 100) if not bulk else min(limit, 1000),
        "offset": offset,
        "fields": fields,
        "year": year,
        "fieldsOfStudy": fields_of_study,
        "venue": venue,
        "minCitationCount": min_citation_count,
    }
    if open_access_pdf:
        params["openAccessPdf"] = ""
    return _request("GET", f"{GRAPH_BASE}{path}", params=params)


def paper(paper_id: str, *, fields: str = DEFAULT_PAPER_FIELDS) -> dict:
    return _request("GET", f"{GRAPH_BASE}/paper/{paper_id}", params={"fields": fields})


def citations(
    paper_id: str, *, limit: int = 100, offset: int = 0, fields: str = LIGHT_PAPER_FIELDS
) -> dict:
    return _request(
        "GET",
        f"{GRAPH_BASE}/paper/{paper_id}/citations",
        params={"limit": min(limit, 1000), "offset": offset, "fields": fields},
    )


def references(
    paper_id: str, *, limit: int = 100, offset: int = 0, fields: str = LIGHT_PAPER_FIELDS
) -> dict:
    return _request(
        "GET",
        f"{GRAPH_BASE}/paper/{paper_id}/references",
        params={"limit": min(limit, 1000), "offset": offset, "fields": fields},
    )


def recommendations(
    paper_id: str, *, limit: int = 100, fields: str = LIGHT_PAPER_FIELDS, pool: str = "recent"
) -> dict:
    return _request(
        "GET",
        f"{RECS_BASE}/papers/forpaper/{paper_id}",
        params={"limit": min(limit, 500), "fields": fields, "from": pool},
    )


def batch(ids: list[str], *, fields: str = DEFAULT_PAPER_FIELDS) -> list:
    if len(ids) > 500:
        raise ValueError("batch supports up to 500 ids")
    return _request(
        "POST",
        f"{GRAPH_BASE}/paper/batch",
        params={"fields": fields},
        json_body={"ids": ids},
    )


def author_search(query: str, *, limit: int = 20, fields: str = "authorId,name,affiliations,paperCount,citationCount,hIndex") -> dict:
    return _request(
        "GET",
        f"{GRAPH_BASE}/author/search",
        params={"query": query, "limit": limit, "fields": fields},
    )


def author(author_id: str, *, fields: str = "authorId,name,affiliations,paperCount,citationCount,hIndex") -> dict:
    return _request("GET", f"{GRAPH_BASE}/author/{author_id}", params={"fields": fields})


def author_papers(
    author_id: str, *, limit: int = 100, offset: int = 0, fields: str = LIGHT_PAPER_FIELDS
) -> dict:
    return _request(
        "GET",
        f"{GRAPH_BASE}/author/{author_id}/papers",
        params={"limit": limit, "offset": offset, "fields": fields},
    )


def snippet_search(query: str, *, limit: int = 10) -> dict:
    return _request(
        "GET",
        f"{GRAPH_BASE}/snippet/search",
        params={"query": query, "limit": limit},
    )


def _emit(obj: Any) -> None:
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def _main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Semantic Scholar API client")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("search")
    sp.add_argument("query")
    sp.add_argument("--limit", type=int, default=20)
    sp.add_argument("--offset", type=int, default=0)
    sp.add_argument("--fields", default=DEFAULT_PAPER_FIELDS)
    sp.add_argument("--year")
    sp.add_argument("--fields-of-study")
    sp.add_argument("--venue")
    sp.add_argument("--min-citation-count", type=int)
    sp.add_argument("--open-access-pdf", action="store_true")
    sp.add_argument("--bulk", action="store_true")

    pp = sub.add_parser("paper")
    pp.add_argument("paper_id")
    pp.add_argument("--fields", default=DEFAULT_PAPER_FIELDS)

    for name in ("citations", "references"):
        cp = sub.add_parser(name)
        cp.add_argument("paper_id")
        cp.add_argument("--limit", type=int, default=100)
        cp.add_argument("--offset", type=int, default=0)
        cp.add_argument("--fields", default=LIGHT_PAPER_FIELDS)

    rp = sub.add_parser("recommendations")
    rp.add_argument("paper_id")
    rp.add_argument("--limit", type=int, default=100)
    rp.add_argument("--fields", default=LIGHT_PAPER_FIELDS)
    rp.add_argument("--pool", choices=["recent", "all-cs"], default="recent")

    bp = sub.add_parser("batch")
    bp.add_argument("ids", nargs="+")
    bp.add_argument("--fields", default=DEFAULT_PAPER_FIELDS)

    asp = sub.add_parser("author-search")
    asp.add_argument("query")
    asp.add_argument("--limit", type=int, default=20)

    ap = sub.add_parser("author")
    ap.add_argument("author_id")

    app = sub.add_parser("author-papers")
    app.add_argument("author_id")
    app.add_argument("--limit", type=int, default=100)
    app.add_argument("--offset", type=int, default=0)

    snp = sub.add_parser("snippets")
    snp.add_argument("query")
    snp.add_argument("--limit", type=int, default=10)

    args = p.parse_args(argv)

    try:
        if args.cmd == "search":
            _emit(search(
                args.query, limit=args.limit, offset=args.offset, fields=args.fields,
                year=args.year, fields_of_study=args.fields_of_study, venue=args.venue,
                min_citation_count=args.min_citation_count,
                open_access_pdf=args.open_access_pdf, bulk=args.bulk,
            ))
        elif args.cmd == "paper":
            _emit(paper(args.paper_id, fields=args.fields))
        elif args.cmd == "citations":
            _emit(citations(args.paper_id, limit=args.limit, offset=args.offset, fields=args.fields))
        elif args.cmd == "references":
            _emit(references(args.paper_id, limit=args.limit, offset=args.offset, fields=args.fields))
        elif args.cmd == "recommendations":
            _emit(recommendations(args.paper_id, limit=args.limit, fields=args.fields, pool=args.pool))
        elif args.cmd == "batch":
            _emit(batch(args.ids, fields=args.fields))
        elif args.cmd == "author-search":
            _emit(author_search(args.query, limit=args.limit))
        elif args.cmd == "author":
            _emit(author(args.author_id))
        elif args.cmd == "author-papers":
            _emit(author_papers(args.author_id, limit=args.limit, offset=args.offset))
        elif args.cmd == "snippets":
            _emit(snippet_search(args.query, limit=args.limit))
        else:
            p.error(f"unknown command: {args.cmd}")
    except SemanticScholarError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
