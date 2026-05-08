#!/usr/bin/env python3
"""Collect compact Git + GitHub provenance evidence for a code change.

This script is intentionally dependency-free. It emits structured JSON or a
compact markdown report so an AI coding agent can reason over history without
loading huge raw git/PR output into context.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHORT_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
RISKY_WORDS = re.compile(
    r"\b(compat|compatibility|breaking|public api|security|race|deadlock|"
    r"perf|performance|allocation|migration|schema|legacy|workaround|revert|"
    r"rollback|fix[- ]?forward|flaky|do not|must not|must|by design|invariant)\b",
    re.IGNORECASE,
)
GENERATED_PATH_RE = re.compile(
    r"(^|/)(node_modules|vendor|third_party|dist|build|generated|snapshots?)(/|$)|"
    r"(package-lock\.json|pnpm-lock\.yaml|yarn\.lock|Cargo\.lock|go\.sum)$",
    re.IGNORECASE,
)


class CommandError(RuntimeError):
    def __init__(self, cmd: Sequence[str], code: int, stdout: str, stderr: str):
        super().__init__(f"Command failed ({code}): {' '.join(map(shlex.quote, cmd))}\n{stderr.strip()}")
        self.cmd = cmd
        self.code = code
        self.stdout = stdout
        self.stderr = stderr


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def run(cmd: Sequence[str], cwd: Optional[Path] = None, check: bool = True, timeout: int = 60) -> str:
    proc = subprocess.run(
        list(cmd),
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    if check and proc.returncode != 0:
        raise CommandError(cmd, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout


def run_optional(cmd: Sequence[str], cwd: Optional[Path] = None, timeout: int = 60) -> Tuple[int, str, str]:
    proc = subprocess.run(
        list(cmd),
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr


def json_dump(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=False)


def flatten_pages(obj: Any) -> Any:
    """Flatten `gh api --paginate --slurp` output."""
    if isinstance(obj, list) and obj and all(isinstance(x, list) for x in obj):
        out: List[Any] = []
        for page in obj:
            out.extend(page)
        return out
    if isinstance(obj, list) and obj and all(isinstance(x, dict) for x in obj):
        # Could be either normal list or slurped list of object pages. Return as-is.
        return obj
    return obj


def gh_api(endpoint: str, repo: str, paginate: bool = False, cache: str = "1h", fields: Optional[Dict[str, str]] = None) -> Any:
    cmd = ["gh", "api", "-H", "Accept: application/vnd.github+json"]
    if cache:
        cmd += ["--cache", cache]
    if paginate:
        cmd += ["--paginate", "--slurp"]
    if fields:
        for k, v in fields.items():
            cmd += ["-f", f"{k}={v}"]
    endpoint = endpoint.replace("{repo}", repo)
    cmd.append(endpoint)
    out = run(cmd, timeout=90)
    if not out.strip():
        return []
    try:
        parsed = json.loads(out)
    except json.JSONDecodeError as ex:
        raise RuntimeError(f"Could not parse gh JSON for {endpoint}: {ex}\nFirst 500 chars:\n{out[:500]}")
    return flatten_pages(parsed)


def gh_search_issues(repo: str, query: str, per_page: int = 20) -> List[Dict[str, Any]]:
    cmd = [
        "gh", "api", "-X", "GET", "search/issues",
        "-f", f"q={query}",
        "-F", f"per_page={per_page}",
        "--cache", "1h",
    ]
    code, out, err = run_optional(cmd, timeout=90)
    if code != 0:
        eprint(f"warning: GitHub search failed: {err.strip()}")
        return []
    try:
        return json.loads(out).get("items", [])
    except Exception:
        return []


def repo_root(repo_dir: Path) -> Path:
    out = run(["git", "rev-parse", "--show-toplevel"], cwd=repo_dir)
    return Path(out.strip())


def parse_repo_from_remote(url: str) -> Optional[str]:
    url = url.strip()
    patterns = [
        r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return f"{m.group('owner')}/{m.group('repo')}"
    return None


def github_repo_slug(root: Path, explicit: Optional[str] = None, use_gh: bool = True) -> Optional[str]:
    if explicit:
        return explicit
    if use_gh:
        code, out, _ = run_optional(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"], cwd=root, timeout=30)
        if code == 0 and out.strip():
            return out.strip()
    code, out, _ = run_optional(["git", "config", "--get", "remote.origin.url"], cwd=root, timeout=10)
    if code == 0:
        return parse_repo_from_remote(out)
    return None


def relpath(root: Path, p: str) -> str:
    pp = Path(p)
    if pp.is_absolute():
        try:
            return str(pp.relative_to(root))
        except ValueError:
            return str(pp)
    return str(pp)


def unique_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x and x not in seen:
            out.append(x)
            seen.add(x)
    return out


def compact_text(s: Optional[str], limit: int = 600) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= limit:
        return s
    return s[: limit - 1].rstrip() + "…"


def token_set(text: str) -> set:
    return {t.lower() for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}|[0-9]{3,}", text or "")}


def normalize_patch_lines(patch: str) -> List[str]:
    out = []
    for line in patch.splitlines():
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue
        if line.startswith("+") or line.startswith("-"):
            normalized = re.sub(r"\s+", "", line[1:]).strip().lower()
            if normalized:
                out.append((line[0] + normalized)[:300])
    return out


def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def git_commit_summary(root: Path, sha: str) -> Dict[str, Any]:
    fmt = "%H%x1f%h%x1f%ct%x1f%an%x1f%s"
    code, out, _ = run_optional(["git", "show", "-s", f"--format={fmt}", sha], cwd=root, timeout=20)
    if code != 0 or not out.strip():
        return {"sha": sha}
    parts = out.strip().split("\x1f", 4)
    d: Dict[str, Any] = {"sha": sha}
    if len(parts) == 5:
        ts = int(parts[2]) if parts[2].isdigit() else 0
        d.update({
            "short_sha": parts[1],
            "author": parts[3],
            "timestamp": ts,
            "date": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(),
            "summary": parts[4],
        })
    return d


def git_changed_files(root: Path, sha: str) -> List[str]:
    code, out, _ = run_optional(["git", "show", "--name-only", "--format=", sha], cwd=root, timeout=30)
    if code != 0:
        return []
    return [x.strip() for x in out.splitlines() if x.strip()]


def git_patch(root: Path, sha: str, path: Optional[str] = None) -> str:
    cmd = ["git", "show", "--format=", "--find-renames=50%", "--find-copies=50%", "--unified=2", sha]
    if path:
        cmd += ["--", path]
    code, out, _ = run_optional(cmd, cwd=root, timeout=60)
    return out if code == 0 else ""


def git_patch_id(root: Path, sha: str) -> Optional[str]:
    patch = git_patch(root, sha)
    if not patch.strip():
        return None
    proc1 = subprocess.Popen(["git", "patch-id", "--stable"], cwd=str(root), text=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = proc1.communicate(patch, timeout=30)
    if proc1.returncode == 0 and stdout.strip():
        return stdout.strip().split()[0]
    return None


def blame_commits(root: Path, path: str, start: Optional[int], end: Optional[int]) -> Tuple[List[Dict[str, Any]], List[str]]:
    if start is None or end is None:
        return [], []
    cmd = ["git", "blame", "-w", "-M", "-C", "-C", "-C", "--line-porcelain", "-L", f"{start},{end}"]
    ignore_file = root / ".git-blame-ignore-revs"
    if ignore_file.exists():
        cmd += ["--ignore-revs-file", str(ignore_file)]
    cmd += ["--", path]
    code, out, err = run_optional(cmd, cwd=root, timeout=90)
    warnings = []
    if code != 0:
        return [], [f"git blame failed: {err.strip()}"]
    records: Dict[str, Dict[str, Any]] = {}
    cur_sha = None
    for line in out.splitlines():
        m = re.match(r"^([0-9a-f]{40})\s+", line)
        if m:
            cur_sha = m.group(1)
            records.setdefault(cur_sha, {"sha": cur_sha, "line_count": 0, "paths": set()})
            continue
        if cur_sha is None:
            continue
        if line.startswith("author "):
            records[cur_sha]["author"] = line[len("author "):]
        elif line.startswith("author-time "):
            ts = int(line[len("author-time "):])
            records[cur_sha]["timestamp"] = ts
            records[cur_sha]["date"] = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
        elif line.startswith("summary "):
            records[cur_sha]["summary"] = line[len("summary "):]
        elif line.startswith("filename "):
            records[cur_sha]["paths"].add(line[len("filename "):])
        elif line.startswith("\t"):
            records[cur_sha]["line_count"] += 1
    result = []
    for rec in records.values():
        rec["paths"] = sorted(rec["paths"])
        result.append(rec)
    result.sort(key=lambda r: (-r.get("line_count", 0), r.get("timestamp", 0)))
    if ignore_file.exists():
        warnings.append("Used .git-blame-ignore-revs")
    return result, warnings


def log_commits_for_path(root: Path, path: str, limit: int) -> List[Dict[str, Any]]:
    fmt = "%H%x1f%h%x1f%ct%x1f%an%x1f%s"
    cmd = ["git", "log", "--follow", "--find-renames=30%", f"--format={fmt}", f"-{limit}", "--", path]
    code, out, err = run_optional(cmd, cwd=root, timeout=90)
    if code != 0:
        eprint(f"warning: git log --follow failed: {err.strip()}")
        return []
    rows = []
    for line in out.splitlines():
        parts = line.split("\x1f", 4)
        if len(parts) != 5:
            continue
        ts = int(parts[2]) if parts[2].isdigit() else 0
        rows.append({
            "sha": parts[0],
            "short_sha": parts[1],
            "timestamp": ts,
            "date": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else None,
            "author": parts[3],
            "summary": parts[4],
            "reason": "path_history",
        })
    return rows


def pickaxe_commits(root: Path, path: str, tokens: Sequence[str], limit_per_token: int = 8) -> List[Dict[str, Any]]:
    out_rows: List[Dict[str, Any]] = []
    fmt = "%H%x1f%h%x1f%ct%x1f%an%x1f%s"
    for tok in tokens[:8]:
        if len(tok) < 3:
            continue
        # -S is literal-ish and safer than regex. Scope to path when possible.
        cmd = ["git", "log", "--all", f"-S{tok}", f"--format={fmt}", f"-{limit_per_token}"]
        if path:
            cmd += ["--", path]
        code, stdout, _ = run_optional(cmd, cwd=root, timeout=60)
        if code != 0:
            continue
        for line in stdout.splitlines():
            parts = line.split("\x1f", 4)
            if len(parts) != 5:
                continue
            ts = int(parts[2]) if parts[2].isdigit() else 0
            out_rows.append({
                "sha": parts[0],
                "short_sha": parts[1],
                "timestamp": ts,
                "date": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else None,
                "author": parts[3],
                "summary": parts[4],
                "reason": f"pickaxe:-S {tok}",
            })
    # de-dupe by sha preserving first reason
    seen = set()
    uniq = []
    for r in out_rows:
        if r["sha"] not in seen:
            uniq.append(r)
            seen.add(r["sha"])
    return uniq


def rename_lineage(root: Path, path: str, limit: int = 80) -> Dict[str, Any]:
    cmd = [
        "git", "log", "--follow", "--name-status", "--find-renames=20%", "--find-copies=20%",
        f"-{limit}", "--format=commit %H", "--", path,
    ]
    code, out, err = run_optional(cmd, cwd=root, timeout=90)
    if code != 0:
        return {"renames": [], "warnings": [f"rename lineage failed: {err.strip()}"]}
    renames = []
    current_commit = None
    for line in out.splitlines():
        if line.startswith("commit "):
            current_commit = line.split()[1]
            continue
        parts = line.split("\t")
        if not parts:
            continue
        status = parts[0]
        if status.startswith("R") and len(parts) >= 3:
            renames.append({"commit": current_commit, "similarity": status[1:], "from": parts[1], "to": parts[2], "kind": "rename"})
        elif status.startswith("C") and len(parts) >= 3:
            renames.append({"commit": current_commit, "similarity": status[1:], "from": parts[1], "to": parts[2], "kind": "copy"})
    return {"renames": renames, "warnings": []}


def extract_keywords(question: str, symbols: Sequence[str]) -> List[str]:
    candidates = []
    for s in symbols:
        candidates.extend(re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", s))
    candidates.extend(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", question or ""))
    stop = {
        "this", "that", "with", "from", "into", "remove", "change", "why", "what", "when", "can", "should",
        "does", "code", "safe", "file", "line", "function", "class", "constraint", "behavior", "behaviour",
    }
    out = []
    for c in candidates:
        if c.lower() not in stop and c not in out:
            out.append(c)
    return out[:12]


def pr_number_from_url(url: str) -> Optional[int]:
    m = re.search(r"/pull/(\d+)", url or "")
    return int(m.group(1)) if m else None


def fetch_pr_bundle(repo: str, number: int, max_comments: int = 80) -> Dict[str, Any]:
    pr = gh_api(f"repos/{repo}/pulls/{number}", repo, paginate=False)
    files = gh_api(f"repos/{repo}/pulls/{number}/files", repo, paginate=True)
    commits = gh_api(f"repos/{repo}/pulls/{number}/commits", repo, paginate=True)
    reviews = gh_api(f"repos/{repo}/pulls/{number}/reviews", repo, paginate=True)
    review_comments = gh_api(f"repos/{repo}/pulls/{number}/comments", repo, paginate=True)
    issue_comments = gh_api(f"repos/{repo}/issues/{number}/comments", repo, paginate=True)
    if not isinstance(files, list):
        files = []
    if not isinstance(commits, list):
        commits = []
    if not isinstance(reviews, list):
        reviews = []
    if not isinstance(review_comments, list):
        review_comments = []
    if not isinstance(issue_comments, list):
        issue_comments = []
    return {
        "number": number,
        "title": pr.get("title"),
        "body": compact_text(pr.get("body"), 2000),
        "state": pr.get("state"),
        "merged_at": pr.get("merged_at"),
        "merge_commit_sha": pr.get("merge_commit_sha"),
        "author": (pr.get("user") or {}).get("login"),
        "url": pr.get("html_url"),
        "base": {"ref": (pr.get("base") or {}).get("ref"), "sha": (pr.get("base") or {}).get("sha")},
        "head": {"ref": (pr.get("head") or {}).get("ref"), "sha": (pr.get("head") or {}).get("sha")},
        "files": [
            {
                "filename": f.get("filename"),
                "previous_filename": f.get("previous_filename"),
                "status": f.get("status"),
                "additions": f.get("additions"),
                "deletions": f.get("deletions"),
                "changes": f.get("changes"),
                "patch": f.get("patch"),
            }
            for f in files
        ],
        "commits": [
            {
                "sha": c.get("sha"),
                "message": compact_text(((c.get("commit") or {}).get("message") or "").split("\n")[0], 300),
                "author": (((c.get("commit") or {}).get("author") or {}).get("name")),
                "date": (((c.get("commit") or {}).get("author") or {}).get("date")),
            }
            for c in commits
        ],
        "reviews": [
            {
                "id": r.get("id"),
                "state": r.get("state"),
                "author": (r.get("user") or {}).get("login"),
                "body": compact_text(r.get("body"), 800),
                "submitted_at": r.get("submitted_at"),
                "url": r.get("html_url"),
            }
            for r in reviews[:max_comments]
        ],
        "review_comments": [
            {
                "id": c.get("id"),
                "path": c.get("path"),
                "line": c.get("line"),
                "original_line": c.get("original_line"),
                "start_line": c.get("start_line"),
                "original_start_line": c.get("original_start_line"),
                "commit_id": c.get("commit_id"),
                "original_commit_id": c.get("original_commit_id"),
                "author": (c.get("user") or {}).get("login"),
                "body": compact_text(c.get("body"), 1000),
                "diff_hunk": compact_text(c.get("diff_hunk"), 1200),
                "url": c.get("html_url"),
            }
            for c in review_comments[:max_comments]
        ],
        "issue_comments": [
            {
                "id": c.get("id"),
                "author": (c.get("user") or {}).get("login"),
                "body": compact_text(c.get("body"), 1000),
                "created_at": c.get("created_at"),
                "url": c.get("html_url"),
            }
            for c in issue_comments[:max_comments]
        ],
        "api_counts": {
            "files": len(files),
            "commits": len(commits),
            "reviews": len(reviews),
            "review_comments": len(review_comments),
            "issue_comments": len(issue_comments),
        },
    }


def associated_prs_for_commit(repo: str, sha: str) -> List[Dict[str, Any]]:
    try:
        res = gh_api(f"repos/{repo}/commits/{sha}/pulls", repo, paginate=True)
    except Exception as ex:
        eprint(f"warning: commit→PR lookup failed for {sha[:12]}: {ex}")
        return []
    if isinstance(res, dict):
        res = [res]
    out = []
    for pr in res or []:
        if not isinstance(pr, dict):
            continue
        out.append({
            "number": pr.get("number"),
            "title": pr.get("title"),
            "url": pr.get("html_url"),
            "state": pr.get("state"),
            "merged_at": pr.get("merged_at"),
            "relation": "exact_commit_association",
            "source_commit": sha,
        })
    return [x for x in out if x.get("number")]


def build_candidate_search_queries(repo: str, path: str, symbols: Sequence[str], keywords: Sequence[str]) -> List[str]:
    terms: List[str] = []
    base = Path(path).name if path else ""
    if base:
        terms.append(base)
    terms.extend(symbols[:4])
    terms.extend(keywords[:6])
    # Build a few small queries rather than one huge brittle query.
    queries = []
    for term in unique_preserve([t for t in terms if len(t) >= 3])[:8]:
        qterm = f'"{term}"' if re.search(r"\W", term) else term
        queries.append(f"repo:{repo} is:pr is:merged {qterm}")
    return queries


def score_pr_bundle(
    bundle: Dict[str, Any],
    path: str,
    symbols: Sequence[str],
    keywords: Sequence[str],
    seed_commit_patches: Dict[str, List[str]],
    exact_sources: Sequence[str],
) -> Dict[str, Any]:
    reasons: List[str] = []
    warnings: List[str] = []
    score = 0.0
    relation = "search_candidate"

    filenames = [f.get("filename") for f in bundle.get("files", []) if f.get("filename")]
    prevs = [f.get("previous_filename") for f in bundle.get("files", []) if f.get("previous_filename")]
    all_paths = set(filenames + prevs)
    if path in all_paths:
        score += 0.35
        reasons.append("same path or previous_filename")
    elif path and any(Path(path).name == Path(p).name for p in all_paths):
        score += 0.12
        reasons.append("same basename")

    if any(GENERATED_PATH_RE.search(p or "") for p in all_paths):
        warnings.append("generated/vendor/lock-file path present; downweight if this is not the true API surface")

    body_text = " ".join([
        bundle.get("title") or "",
        bundle.get("body") or "",
        " ".join(r.get("body") or "" for r in bundle.get("reviews", [])),
        " ".join(c.get("body") or "" for c in bundle.get("review_comments", [])),
        " ".join(c.get("body") or "" for c in bundle.get("issue_comments", [])),
    ])
    body_tokens = token_set(body_text)
    query_tokens = {x.lower() for x in list(symbols) + list(keywords) if len(x) >= 3}
    semantic_overlap = len(body_tokens & query_tokens)
    if semantic_overlap:
        bump = min(0.25, 0.04 * semantic_overlap)
        score += bump
        reasons.append(f"discussion/title/body matches {semantic_overlap} query token(s)")

    risky_hits = RISKY_WORDS.findall(body_text)
    if risky_hits:
        score += 0.08
        reasons.append("discussion contains risk/constraint language")

    pr_patch_lines: List[str] = []
    for f in bundle.get("files", []):
        if f.get("patch"):
            pr_patch_lines.extend(normalize_patch_lines(f["patch"]))
    best_hunk = 0.0
    best_sha = None
    for sha, lines in seed_commit_patches.items():
        sim = jaccard(lines, pr_patch_lines)
        if sim > best_hunk:
            best_hunk = sim
            best_sha = sha
    if best_hunk >= 0.65:
        score += 0.55
        relation = "probable_squash_or_patch_equivalent"
        reasons.append(f"high hunk similarity to commit {best_sha[:12]} ({best_hunk:.2f})")
    elif best_hunk >= 0.25:
        score += 0.25
        reasons.append(f"partial hunk similarity to commit {best_sha[:12]} ({best_hunk:.2f})")

    exact_sources_set = set(exact_sources)
    pr_commit_shas = {c.get("sha") for c in bundle.get("commits", []) if c.get("sha")}
    if exact_sources_set & pr_commit_shas:
        score += 0.5
        relation = "pr_commit_contains_seed_commit"
        reasons.append("PR commit list contains seed commit")

    number = bundle.get("number")
    if bundle.get("_exact_commit_sources"):
        score += 1.0
        relation = "exact_commit_association"
        reasons.insert(0, f"GitHub associated commit(s): {', '.join(s[:12] for s in bundle['_exact_commit_sources'])}")

    if bundle.get("api_counts", {}).get("files", 0) >= 3000:
        warnings.append("PR files may be incomplete because GitHub PR file listing can be capped")
    if any((f.get("patch") is None and f.get("changes", 0)) for f in bundle.get("files", [])):
        warnings.append("one or more file patches are absent; patch evidence may be incomplete")

    # Normalize score to [0, 1]
    score = min(1.0, score)
    confidence = "high" if score >= 0.82 else "medium" if score >= 0.55 else "low"
    if relation == "search_candidate" and score >= 0.82:
        confidence = "medium"  # semantic/path search should not become high alone.
    return {
        "number": number,
        "title": bundle.get("title"),
        "url": bundle.get("url"),
        "relation": relation,
        "score": round(score, 3),
        "confidence": confidence,
        "why_relevant": reasons or ["candidate fetched but no strong signal found"],
        "warnings": warnings,
        "best_hunk_similarity": round(best_hunk, 3),
    }


def select_relevant_comments(bundle: Dict[str, Any], path: str, symbols: Sequence[str], keywords: Sequence[str], max_items: int) -> List[Dict[str, Any]]:
    qtokens = {t.lower() for t in list(symbols) + list(keywords) if len(t) >= 3}
    items: List[Tuple[float, Dict[str, Any]]] = []

    def score_text(text: str, extra: float = 0.0) -> float:
        toks = token_set(text)
        score = extra + 0.05 * len(toks & qtokens)
        if RISKY_WORDS.search(text or ""):
            score += 0.2
        return score

    for c in bundle.get("review_comments", []):
        extra = 0.25 if c.get("path") == path else 0.0
        s = score_text((c.get("body") or "") + " " + (c.get("diff_hunk") or ""), extra)
        if s > 0 or c.get("path") == path:
            items.append((s, {"kind": "review_comment", **c}))
    for c in bundle.get("issue_comments", []):
        s = score_text(c.get("body") or "")
        if s > 0:
            items.append((s, {"kind": "issue_comment", **c}))
    for r in bundle.get("reviews", []):
        s = score_text(r.get("body") or "")
        if s > 0:
            items.append((s, {"kind": "review", **r}))
    items.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in items[:max_items]]


def infer_decision_atoms(comments: Sequence[Dict[str, Any]], pr_number: int, path: str, symbols: Sequence[str]) -> List[Dict[str, Any]]:
    atoms = []
    patterns = [
        ("compatibility_constraint", re.compile(r"compat|legacy|backwards?|breaking", re.I)),
        ("security_invariant", re.compile(r"security|auth|permission|leak|secret|injection", re.I)),
        ("performance_constraint", re.compile(r"perf|performance|alloc|allocation|hot path|latency", re.I)),
        ("concurrency_invariant", re.compile(r"race|deadlock|lock|concurr|async|thread", re.I)),
        ("rejected_approach", re.compile(r"reject|rejected|don'?t|do not|must not|avoid|not safe", re.I)),
        ("test_requirement", re.compile(r"test|coverage|regression|flaky", re.I)),
        ("known_bug_or_workaround", re.compile(r"workaround|known bug|hack|temporary|fix forward", re.I)),
        ("constraint", re.compile(r"must|should|by design|invariant|required", re.I)),
    ]
    for c in comments:
        body = c.get("body") or ""
        if not body:
            continue
        matched = None
        for typ, pat in patterns:
            if pat.search(body):
                matched = typ
                break
        if not matched:
            continue
        claim = compact_text(body, 220)
        atoms.append({
            "claim": claim,
            "type": matched,
            "scope": f"{path}" + ((":" + ",".join(symbols[:2])) if symbols else ""),
            "confidence": 0.65 if c.get("kind") == "review_comment" else 0.5,
            "superseded": False,
            "evidence": [{
                "kind": c.get("kind"),
                "pr": pr_number,
                "url": c.get("url"),
                "path": c.get("path"),
                "line": c.get("line") or c.get("original_line"),
            }],
        })
        if len(atoms) >= 8:
            break
    return atoms


def inspect(args: argparse.Namespace) -> Dict[str, Any]:
    root = repo_root(Path(args.repo_dir).resolve())
    path = relpath(root, args.path)
    repo = github_repo_slug(root, args.github_repo, use_gh=not args.no_gh)
    warnings: List[str] = []
    if GENERATED_PATH_RE.search(path):
        warnings.append("Target path looks generated/vendor/lock-like; downweight history unless it is the actual API surface.")

    keywords = extract_keywords(args.question or "", args.symbol or [])
    if args.keyword:
        keywords = unique_preserve(list(args.keyword) + keywords)

    blame, blame_warnings = blame_commits(root, path, args.start, args.end)
    warnings.extend(blame_warnings)
    path_history = log_commits_for_path(root, path, args.max_commits)
    pickaxe = pickaxe_commits(root, path, unique_preserve(list(args.symbol or []) + keywords), limit_per_token=5)
    lineage = rename_lineage(root, path)
    warnings.extend(lineage.get("warnings", []))

    seed_reasons: Dict[str, List[str]] = defaultdict(list)
    for b in blame:
        seed_reasons[b["sha"]].append(f"blame:{b.get('line_count', 0)} lines")
    for c in path_history[: min(len(path_history), args.max_commits)]:
        seed_reasons[c["sha"]].append("path_history")
    for c in pickaxe:
        seed_reasons[c["sha"]].append(c.get("reason", "pickaxe"))

    seed_shas = list(seed_reasons.keys())[: args.max_commits]
    seed_commits = []
    for sha in seed_shas:
        summ = git_commit_summary(root, sha)
        summ["reasons"] = seed_reasons[sha]
        summ["changed_files"] = git_changed_files(root, sha)[:30]
        summ["patch_id"] = git_patch_id(root, sha)
        seed_commits.append(summ)

    seed_commit_patches = {sha: normalize_patch_lines(git_patch(root, sha, path)) for sha in seed_shas[:20]}

    pr_sources: Dict[int, List[str]] = defaultdict(list)
    pr_seed_relation: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    gh_available = False
    if repo and not args.no_gh:
        code, _, _ = run_optional(["gh", "auth", "status"], cwd=root, timeout=20)
        gh_available = code == 0
        if not gh_available:
            warnings.append("gh is not authenticated or unavailable; GitHub PR evidence was not fetched.")
    elif not repo and not args.no_gh:
        warnings.append("Could not determine GitHub OWNER/REPO; pass --github-repo OWNER/REPO for PR evidence.")

    if repo and gh_available:
        for sha in seed_shas[: args.max_commit_pr_lookups]:
            for pr in associated_prs_for_commit(repo, sha):
                pr_sources[int(pr["number"])].append(sha)
                pr_seed_relation[int(pr["number"])].append(pr)

        # Search fallback for squash/lost PRs. Keep small for context and rate limits.
        for q in build_candidate_search_queries(repo, path, args.symbol or [], keywords)[: args.max_search_queries]:
            for item in gh_search_issues(repo, q, per_page=args.search_per_page):
                n = item.get("number") or pr_number_from_url(item.get("html_url", ""))
                if n:
                    pr_seed_relation[int(n)].append({
                        "number": int(n),
                        "title": item.get("title"),
                        "url": item.get("html_url"),
                        "relation": "search_candidate",
                        "search_query": q,
                    })

    candidate_numbers = list(pr_seed_relation.keys())[: args.max_prs * 3]
    bundles = []
    scored = []
    decision_atoms: List[Dict[str, Any]] = []
    relevant_comments_by_pr: Dict[str, Any] = {}
    if repo and gh_available:
        for n in candidate_numbers:
            try:
                bundle = fetch_pr_bundle(repo, n, max_comments=args.max_comments)
                bundle["_exact_commit_sources"] = pr_sources.get(n, [])
                s = score_pr_bundle(bundle, path, args.symbol or [], keywords, seed_commit_patches, pr_sources.get(n, []))
                comments = select_relevant_comments(bundle, path, args.symbol or [], keywords, max_items=args.max_comments_per_pr)
                relevant_comments_by_pr[str(n)] = comments
                atoms = infer_decision_atoms(comments, n, path, args.symbol or [])
                decision_atoms.extend(atoms)
                scored.append(s)
                # Keep a compact form only.
                bundle_compact = {k: bundle[k] for k in ["number", "title", "body", "state", "merged_at", "merge_commit_sha", "author", "url", "base", "head", "api_counts"]}
                bundle_compact["files"] = [
                    {kk: f.get(kk) for kk in ["filename", "previous_filename", "status", "additions", "deletions", "changes"]}
                    for f in bundle.get("files", [])[:50]
                ]
                bundles.append(bundle_compact)
            except Exception as ex:
                warnings.append(f"Failed to fetch PR #{n}: {ex}")

    scored.sort(key=lambda x: x["score"], reverse=True)
    scored = scored[: args.max_prs]

    all_pr_warnings = [w for s in scored for w in s.get("warnings", [])]
    evidence_completeness = {
        "local_git": "complete" if seed_commits else "partial",
        "github_prs": "complete" if gh_available and repo else "not_run",
        "review_comments": "complete" if gh_available and repo else "not_run",
        "api_truncation_possible": any("incomplete" in w or "capped" in w for w in all_pr_warnings),
        "notes": unique_preserve(warnings + all_pr_warnings)[:20],
    }

    risk_level = "unknown"
    risk_conf = 0.0
    action = "ask_human"
    if scored:
        top = scored[0]
        if top["confidence"] == "high" and decision_atoms:
            risk_level = "high" if any(a["type"] in {"compatibility_constraint", "security_invariant", "concurrency_invariant", "public_api_contract", "rejected_approach"} for a in decision_atoms) else "medium"
            risk_conf = min(0.9, top["score"])
            action = "modify_plan" if risk_level in {"medium", "high"} else "proceed"
        elif top["confidence"] == "high":
            risk_level = "medium"
            risk_conf = top["score"]
            action = "modify_plan"
        elif top["confidence"] == "medium":
            risk_level = "unknown"
            risk_conf = min(0.55, top["score"])
            action = "ask_human"
    elif gh_available and repo:
        action = "ask_human"
        warnings.append("No strong PR candidates found; possible direct commit, private/missing PR, or poor search terms.")

    report: Dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "scope": {
            "repo_dir": str(root),
            "github_repo": repo,
            "path": path,
            "line_range": {"start": args.start, "end": args.end} if args.start is not None or args.end is not None else None,
            "symbols": args.symbol or [],
            "question": args.question,
            "keywords": keywords,
        },
        "evidence_completeness": evidence_completeness,
        "seed_commits": seed_commits[: args.max_commits],
        "file_lineage": lineage,
        "relevant_prs": scored,
        "pr_bundles_compact": bundles[: args.max_prs],
        "relevant_comments_by_pr": {k: v for k, v in relevant_comments_by_pr.items() if int(k) in {p["number"] for p in scored}},
        "decision_atoms": decision_atoms[:12],
        "risk": {
            "level": risk_level,
            "confidence": round(risk_conf, 3),
            "recommended_action": action,
        },
        "unknowns": unique_preserve(warnings)[:20],
    }
    return report


def as_markdown(report: Dict[str, Any]) -> str:
    scope = report["scope"]
    lines = []
    lines.append("## History context report")
    lines.append("")
    lines.append(f"Scope inspected: `{scope.get('github_repo') or 'unknown repo'}` `{scope.get('path')}`")
    if scope.get("line_range"):
        lr = scope["line_range"]
        lines.append(f"Lines: {lr.get('start')}–{lr.get('end')}")
    if scope.get("symbols"):
        lines.append(f"Symbols: {', '.join(scope['symbols'])}")
    if scope.get("question"):
        lines.append(f"Question: {scope['question']}")
    lines.append("")

    comp = report["evidence_completeness"]
    lines.append("### Evidence completeness")
    lines.append(f"- Local git: {comp['local_git']}")
    lines.append(f"- GitHub PRs: {comp['github_prs']}")
    lines.append(f"- Review comments: {comp['review_comments']}")
    lines.append(f"- API truncation possible: {comp['api_truncation_possible']}")
    for note in comp.get("notes", [])[:6]:
        lines.append(f"- Note: {note}")
    lines.append("")

    lines.append("### Seed commits")
    for c in report.get("seed_commits", [])[:8]:
        lines.append(f"- `{c.get('short_sha') or c.get('sha','')[:12]}` {c.get('date','')} — {compact_text(c.get('summary'), 160)}")
        if c.get("reasons"):
            lines.append(f"  - reasons: {', '.join(c['reasons'][:4])}")
        if c.get("patch_id"):
            lines.append(f"  - patch-id: `{c['patch_id'][:16]}…`")
    if not report.get("seed_commits"):
        lines.append("- No seed commits found.")
    lines.append("")

    lines.append("### Relevant PR candidates")
    for pr in report.get("relevant_prs", [])[:10]:
        lines.append(f"- PR #{pr['number']} — {compact_text(pr.get('title'), 140)}")
        lines.append(f"  - relation: {pr['relation']}; score: {pr['score']}; confidence: {pr['confidence']}")
        if pr.get("url"):
            lines.append(f"  - url: {pr['url']}")
        for why in pr.get("why_relevant", [])[:4]:
            lines.append(f"  - why: {why}")
        for warn in pr.get("warnings", [])[:3]:
            lines.append(f"  - warning: {warn}")
    if not report.get("relevant_prs"):
        lines.append("- No PR candidates found or GitHub lookup was not available.")
    lines.append("")

    if report.get("decision_atoms"):
        lines.append("### Decision atoms")
        for a in report["decision_atoms"][:8]:
            ev = a.get("evidence", [{}])[0]
            ref = f"PR #{ev.get('pr')} {ev.get('kind')}" if ev else "evidence"
            lines.append(f"- {a['type']}: {compact_text(a['claim'], 180)}")
            lines.append(f"  - confidence: {a['confidence']}; evidence: {ref} {ev.get('url') or ''}")
        lines.append("")

    if report.get("relevant_comments_by_pr"):
        lines.append("### Selected comments")
        for prn, comments in list(report["relevant_comments_by_pr"].items())[:5]:
            if not comments:
                continue
            lines.append(f"PR #{prn}:")
            for c in comments[:4]:
                where = f" {c.get('path')}:{c.get('line') or c.get('original_line')}" if c.get("path") else ""
                lines.append(f"- {c.get('kind')}{where}: {compact_text(c.get('body'), 220)}")
                if c.get("url"):
                    lines.append(f"  - {c.get('url')}")
        lines.append("")

    risk = report["risk"]
    lines.append("### Risk")
    lines.append(f"- Level: {risk['level']}")
    lines.append(f"- Confidence: {risk['confidence']}")
    lines.append(f"- Recommended action: {risk['recommended_action']}")
    if report.get("unknowns"):
        lines.append("- Unknowns/warnings:")
        for u in report["unknowns"][:8]:
            lines.append(f"  - {u}")
    lines.append("")
    lines.append("Use this report as evidence input. The agent must still synthesize a final history note and avoid high-confidence claims from weak evidence.")
    return "\n".join(lines)


def cmd_commit_prs(args: argparse.Namespace) -> Dict[str, Any]:
    root = repo_root(Path(args.repo_dir).resolve())
    repo = github_repo_slug(root, args.github_repo, use_gh=not getattr(args, "no_gh", False))
    if not repo:
        raise SystemExit("Could not determine GitHub repo. Pass --github-repo OWNER/REPO.")
    out = []
    for sha in args.commit:
        out.append({"commit": sha, "associated_prs": associated_prs_for_commit(repo, sha)})
    return {"github_repo": repo, "results": out}


def cmd_lineage(args: argparse.Namespace) -> Dict[str, Any]:
    root = repo_root(Path(args.repo_dir).resolve())
    path = relpath(root, args.path)
    return {"repo_dir": str(root), "path": path, "file_lineage": rename_lineage(root, path, args.limit)}


def write_output(data: Dict[str, Any], args: argparse.Namespace) -> None:
    fmt = getattr(args, "format", "json")
    text = as_markdown(data) if fmt == "markdown" else json_dump(data)
    if getattr(args, "output", None):
        Path(args.output).write_text(text, encoding="utf-8")
        eprint(f"wrote {args.output}")
    else:
        print(text)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Collect compact local Git + GitHub PR provenance evidence for code history investigations.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--version", action="version", version="history_context.py 1.0.0")
    sub = p.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo-dir", default=".", help="Local git repository directory to inspect.")
    common.add_argument("--github-repo", help="GitHub slug OWNER/REPO. Auto-detected via gh or origin remote if omitted.")
    common.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format.")
    common.add_argument("--output", help="Write output to this file instead of stdout.")

    i = sub.add_parser("inspect", parents=[common], help="Inspect code provenance for a path/line/symbol/question.")
    i.add_argument("--path", required=True, help="Repository-relative file path to inspect.")
    i.add_argument("--start", type=int, help="Start line for blame.")
    i.add_argument("--end", type=int, help="End line for blame.")
    i.add_argument("--symbol", action="append", default=[], help="Symbol/function/class/API name. Repeatable.")
    i.add_argument("--keyword", action="append", default=[], help="Additional keyword for pickaxe/search. Repeatable.")
    i.add_argument("--question", default="", help="Natural-language question/change being investigated.")
    i.add_argument("--max-commits", type=int, default=30, help="Maximum seed commits to summarize.")
    i.add_argument("--max-prs", type=int, default=12, help="Maximum PR candidates to include.")
    i.add_argument("--max-comments", type=int, default=80, help="Maximum raw comments to fetch per PR endpoint before compacting.")
    i.add_argument("--max-comments-per-pr", type=int, default=6, help="Maximum selected relevant comments per PR in output.")
    i.add_argument("--max-commit-pr-lookups", type=int, default=20, help="Maximum seed commits for exact commit→PR lookup.")
    i.add_argument("--max-search-queries", type=int, default=8, help="Maximum GitHub issue-search queries for fuzzy PR candidates.")
    i.add_argument("--search-per-page", type=int, default=10, help="Search results per query.")
    i.add_argument("--no-gh", action="store_true", help="Skip GitHub CLI calls and return local Git evidence only.")
    i.set_defaults(func=inspect)

    c = sub.add_parser("commit-prs", parents=[common], help="List GitHub PRs associated with one or more commits.")
    c.add_argument("--commit", action="append", required=True, help="Commit SHA. Repeatable.")
    c.add_argument("--no-gh", action="store_true", help="Skip `gh` for slug auto-detection; rely on `git remote` only.")
    c.set_defaults(func=cmd_commit_prs)

    l = sub.add_parser("lineage", parents=[common], help="Show rename/copy lineage for a path.")
    l.add_argument("--path", required=True, help="Repository-relative file path.")
    l.add_argument("--limit", type=int, default=80, help="Maximum git log entries to inspect.")
    l.set_defaults(func=cmd_lineage)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        data = args.func(args)
        write_output(data, args)
        return 0
    except CommandError as ex:
        eprint(str(ex))
        return 2
    except subprocess.TimeoutExpired as ex:
        eprint(f"Timed out running command: {ex.cmd}")
        return 3
    except Exception as ex:
        eprint(f"error: {ex}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
