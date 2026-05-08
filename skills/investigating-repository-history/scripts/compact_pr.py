#!/usr/bin/env python3
"""Fetch compact PR evidence using GitHub CLI.

Dependency-free helper for agents that need to inspect a specific PR without
loading huge raw API payloads.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def run(cmd: Sequence[str], cwd: Optional[Path] = None, timeout: int = 60) -> str:
    proc = subprocess.run(list(cmd), cwd=str(cwd) if cwd else None, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(map(shlex.quote, cmd))}\n{proc.stderr.strip()}")
    return proc.stdout


def flatten_pages(obj: Any) -> Any:
    if isinstance(obj, list) and obj and all(isinstance(x, list) for x in obj):
        out: List[Any] = []
        for page in obj:
            out.extend(page)
        return out
    return obj


def gh_api(endpoint: str, paginate: bool = False, cache: str = "1h") -> Any:
    cmd = ["gh", "api", "-H", "Accept: application/vnd.github+json", "--cache", cache]
    if paginate:
        cmd += ["--paginate", "--slurp"]
    cmd.append(endpoint)
    out = run(cmd, timeout=90)
    return flatten_pages(json.loads(out)) if out.strip() else []


def detect_repo(repo_dir: Path, explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    proc = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"], cwd=str(repo_dir), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode == 0 and proc.stdout.strip():
        return proc.stdout.strip()
    raise RuntimeError("Could not determine GitHub repo. Pass --github-repo OWNER/REPO.")


def compact_text(text: Optional[str], limit: int) -> str:
    if not text:
        return ""
    s = re.sub(r"\s+", " ", text).strip()
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "…"


def fetch(repo: str, pr_num: int, max_comments: int) -> Dict[str, Any]:
    pr = gh_api(f"repos/{repo}/pulls/{pr_num}")
    files = gh_api(f"repos/{repo}/pulls/{pr_num}/files", paginate=True)
    reviews = gh_api(f"repos/{repo}/pulls/{pr_num}/reviews", paginate=True)
    review_comments = gh_api(f"repos/{repo}/pulls/{pr_num}/comments", paginate=True)
    issue_comments = gh_api(f"repos/{repo}/issues/{pr_num}/comments", paginate=True)
    return {
        "number": pr_num,
        "title": pr.get("title"),
        "state": pr.get("state"),
        "merged_at": pr.get("merged_at"),
        "merge_commit_sha": pr.get("merge_commit_sha"),
        "author": (pr.get("user") or {}).get("login"),
        "url": pr.get("html_url"),
        "body": compact_text(pr.get("body"), 1800),
        "files": [
            {
                "filename": f.get("filename"),
                "previous_filename": f.get("previous_filename"),
                "status": f.get("status"),
                "additions": f.get("additions"),
                "deletions": f.get("deletions"),
                "changes": f.get("changes"),
                "has_patch": bool(f.get("patch")),
                "patch_excerpt": compact_text(f.get("patch"), 800),
            }
            for f in (files or [])[:80]
        ],
        "reviews": [
            {
                "state": r.get("state"),
                "author": (r.get("user") or {}).get("login"),
                "submitted_at": r.get("submitted_at"),
                "body": compact_text(r.get("body"), 700),
                "url": r.get("html_url"),
            }
            for r in (reviews or [])[:max_comments]
        ],
        "review_comments": [
            {
                "path": c.get("path"),
                "line": c.get("line"),
                "original_line": c.get("original_line"),
                "author": (c.get("user") or {}).get("login"),
                "body": compact_text(c.get("body"), 900),
                "diff_hunk": compact_text(c.get("diff_hunk"), 900),
                "url": c.get("html_url"),
            }
            for c in (review_comments or [])[:max_comments]
        ],
        "issue_comments": [
            {
                "author": (c.get("user") or {}).get("login"),
                "created_at": c.get("created_at"),
                "body": compact_text(c.get("body"), 900),
                "url": c.get("html_url"),
            }
            for c in (issue_comments or [])[:max_comments]
        ],
        "api_counts": {
            "files": len(files or []),
            "reviews": len(reviews or []),
            "review_comments": len(review_comments or []),
            "issue_comments": len(issue_comments or []),
        },
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch compact GitHub PR evidence for repository-history investigations.")
    parser.add_argument("--repo-dir", default=".", help="Local repo directory used for gh repo detection.")
    parser.add_argument("--github-repo", help="GitHub slug OWNER/REPO. Auto-detected if omitted.")
    parser.add_argument("--pr", action="append", type=int, required=True, help="PR number. Repeatable.")
    parser.add_argument("--max-comments", type=int, default=80, help="Maximum reviews/comments per endpoint to include.")
    parser.add_argument("--output", help="Write JSON to file instead of stdout.")
    args = parser.parse_args(argv)
    try:
        repo = detect_repo(Path(args.repo_dir), args.github_repo)
        data = {"github_repo": repo, "pull_requests": [fetch(repo, n, args.max_comments) for n in args.pr]}
        text = json.dumps(data, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
            eprint(f"wrote {args.output}")
        else:
            print(text)
        return 0
    except Exception as ex:
        eprint(f"error: {ex}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
