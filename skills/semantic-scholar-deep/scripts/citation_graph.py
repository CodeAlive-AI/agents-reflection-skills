#!/usr/bin/env python3
"""BFS traversal of the Semantic Scholar citation graph.

Example:
    python3 citation_graph.py <paperId> --depth 2 --direction both --max-nodes 200 \
        --output graph.json

Output JSON schema:
    {
      "seed": "<paperId>",
      "direction": "forward|backward|both",
      "depth": 2,
      "nodes": {
        "<paperId>": {
          "paperId": "...",
          "title": "...",
          "year": 2022,
          "citationCount": 123,
          "authors": [{"name": "..."}],
          "venue": "...",
          "depth": 1
        }
      },
      "edges": [
        {"src": "<paperId>", "dst": "<paperId>", "direction": "citation|reference"}
      ]
    }

Directions:
    forward   — follow *citations* (who cites this paper). Good for tracking impact.
    backward  — follow *references* (what this paper cites). Good for literature grounding.
    both      — union of both per hop.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ss_client  # type: ignore


def _extract_neighbor(entry: dict, key: str) -> dict | None:
    node = entry.get(key)
    if not node or not isinstance(node, dict):
        return None
    if not node.get("paperId"):
        return None
    return node


def traverse(
    seed: str,
    *,
    direction: str = "both",
    depth: int = 2,
    max_nodes: int = 200,
    per_hop_limit: int = 50,
) -> dict:
    assert direction in {"forward", "backward", "both"}
    seed_info = ss_client.paper(
        seed,
        fields="paperId,title,year,authors.name,citationCount,venue,externalIds",
    )
    seed_id = seed_info["paperId"]

    nodes: dict[str, dict] = {seed_id: {**seed_info, "depth": 0}}
    edges: list[dict] = []
    queue: deque[tuple[str, int]] = deque([(seed_id, 0)])

    while queue and len(nodes) < max_nodes:
        paper_id, cur_depth = queue.popleft()
        if cur_depth >= depth:
            continue

        if direction in {"forward", "both"}:
            resp = ss_client.citations(paper_id, limit=per_hop_limit)
            for entry in resp.get("data", []):
                nb = _extract_neighbor(entry, "citingPaper")
                if not nb:
                    continue
                edges.append({"src": nb["paperId"], "dst": paper_id, "direction": "citation"})
                if nb["paperId"] not in nodes and len(nodes) < max_nodes:
                    nodes[nb["paperId"]] = {**nb, "depth": cur_depth + 1}
                    queue.append((nb["paperId"], cur_depth + 1))

        if direction in {"backward", "both"} and len(nodes) < max_nodes:
            resp = ss_client.references(paper_id, limit=per_hop_limit)
            for entry in resp.get("data", []):
                nb = _extract_neighbor(entry, "citedPaper")
                if not nb:
                    continue
                edges.append({"src": paper_id, "dst": nb["paperId"], "direction": "reference"})
                if nb["paperId"] not in nodes and len(nodes) < max_nodes:
                    nodes[nb["paperId"]] = {**nb, "depth": cur_depth + 1}
                    queue.append((nb["paperId"], cur_depth + 1))

    return {
        "seed": seed_id,
        "direction": direction,
        "depth": depth,
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "truncated": len(nodes) >= max_nodes,
        },
    }


def _main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Citation graph BFS on Semantic Scholar")
    p.add_argument("seed", help="paperId (supports DOI:, ARXIV:, CorpusId: prefixes)")
    p.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    p.add_argument("--depth", type=int, default=2)
    p.add_argument("--max-nodes", type=int, default=200)
    p.add_argument("--per-hop-limit", type=int, default=50)
    p.add_argument("--output", help="write JSON here instead of stdout")

    args = p.parse_args(argv)

    try:
        graph = traverse(
            args.seed,
            direction=args.direction,
            depth=args.depth,
            max_nodes=args.max_nodes,
            per_hop_limit=args.per_hop_limit,
        )
    except ss_client.SemanticScholarError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    dump = json.dumps(graph, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(dump, encoding="utf-8")
        print(
            f"wrote {graph['stats']['total_nodes']} nodes, {graph['stats']['total_edges']} edges → {args.output}",
            file=sys.stderr,
        )
    else:
        print(dump)
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
