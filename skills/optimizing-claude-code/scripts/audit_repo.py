#!/usr/bin/env python3
"""
optimizing-claude-code: Repository audit script (stdlib only)

Outputs a JSON report with:
- Repo scale metrics (tracked file count, directory hotspots)
- CLAUDE.md / CLAUDE.local.md discovery and quality metrics
- @import validation for memory files
- Claude Code settings discovery and analysis
- MCP configuration discovery
- Skill and subagent discovery
- Readability/maintainability signals
- Large-repo threshold flag (>3000 files) for scaling recommendations
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Regex for @imports (best-effort, ignores inline code spans)
IMPORT_RE = re.compile(r'(?<!`)\B@([~/.\w\-\s/]+[.\w\-\s/])')


@dataclass
class MemoryFileReport:
    path: str
    exists: bool
    bytes: int = 0
    lines: int = 0
    word_count: int = 0
    has_headings: bool = False
    heading_count: int = 0
    imports: List[str] = field(default_factory=list)
    missing_imports: List[str] = field(default_factory=list)
    last_git_commit_iso: Optional[str] = None
    scope: str = "project"  # user, project, or local
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class SettingsFileReport:
    path: str
    exists: bool
    scope: str  # user, project, local, managed
    bytes: int = 0
    has_allowed_tools: bool = False
    has_deny_tools: bool = False
    has_custom_instructions: bool = False
    has_mcp_servers: bool = False
    mcp_server_count: int = 0
    issues: List[str] = field(default_factory=list)


@dataclass
class MCPConfigReport:
    path: str
    exists: bool
    scope: str  # user or project
    server_count: int = 0
    servers: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)


@dataclass
class SkillReport:
    path: str
    name: str
    scope: str  # user or project
    has_description: bool = False
    has_scripts: bool = False
    has_references: bool = False
    has_assets: bool = False
    skill_md_lines: int = 0
    issues: List[str] = field(default_factory=list)


@dataclass
class SubagentReport:
    path: str
    name: str
    scope: str  # user or project
    has_description: bool = False
    agent_md_lines: int = 0
    issues: List[str] = field(default_factory=list)


def _run(cmd: List[str], cwd: Path) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    p = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def _is_git_repo(root: Path) -> bool:
    return (root / ".git").exists()


def _git_tracked_files(root: Path) -> Optional[List[str]]:
    rc, out, _ = _run(["git", "ls-files"], root)
    if rc != 0:
        return None
    return [line for line in out.splitlines() if line.strip()]


def _git_last_commit_iso(root: Path, rel_path: str) -> Optional[str]:
    rc, out, _ = _run(["git", "log", "-1", "--format=%cI", "--", rel_path], root)
    if rc != 0 or not out:
        return None
    return out.splitlines()[0].strip()


def _safe_read_text(path: Path, max_bytes: int = 2_000_000) -> str:
    """Read file text safely, truncating if too large."""
    try:
        data = path.read_bytes()
        if len(data) > max_bytes:
            data = data[:max_bytes]
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def _safe_read_json(path: Path) -> Optional[Dict]:
    """Read and parse JSON file."""
    try:
        text = _safe_read_text(path)
        return json.loads(text)
    except Exception:
        return None


def _resolve_import(base_dir: Path, raw: str, repo_root: Path) -> Path:
    """Resolve an @import path."""
    raw = raw.strip()
    if raw.startswith("~"):
        return Path(os.path.expanduser(raw))
    p = Path(raw)
    if p.is_absolute():
        return p
    return (base_dir / p).resolve()


def _extract_imports(text: str) -> List[str]:
    """Extract @import references from text."""
    found = [m.group(1).strip() for m in IMPORT_RE.finditer(text)]
    # Filter out email-like patterns
    return [x for x in found if "@" not in x]


def _count_headings(text: str) -> int:
    """Count markdown headings."""
    return len(re.findall(r'^#{1,6}\s+', text, re.MULTILINE))


def _discover_memory_files(root: Path) -> List[Tuple[Path, str]]:
    """Discover CLAUDE.md and CLAUDE.local.md files with their scope."""
    candidates = []

    # Project-level locations
    project_locations = [
        (root / "CLAUDE.md", "project"),
        (root / ".claude" / "CLAUDE.md", "project"),
        (root / "CLAUDE.local.md", "local"),
        (root / ".claude" / "CLAUDE.local.md", "local"),
    ]

    for path, scope in project_locations:
        candidates.append((path, scope))

    # Find nested CLAUDE.md files (monorepos)
    for p in root.rglob("CLAUDE.md"):
        if p not in [c[0] for c in candidates]:
            candidates.append((p, "project-nested"))

    for p in root.rglob("CLAUDE.local.md"):
        if p not in [c[0] for c in candidates]:
            candidates.append((p, "local-nested"))

    return candidates


def _analyze_memory_file(path: Path, scope: str, root: Path, tracked: Optional[List[str]]) -> MemoryFileReport:
    """Analyze a single CLAUDE.md file."""
    try:
        rel = str(path.relative_to(root))
    except ValueError:
        rel = str(path)

    report = MemoryFileReport(path=rel, exists=path.exists() and path.is_file(), scope=scope)

    if not report.exists:
        return report

    text = _safe_read_text(path)
    report.bytes = path.stat().st_size
    report.lines = text.count("\n") + (1 if text else 0)
    report.word_count = len(text.split())
    report.has_headings = bool(re.search(r'^#{1,6}\s+', text, re.MULTILINE))
    report.heading_count = _count_headings(text)
    report.imports = _extract_imports(text)

    # Validate imports
    base_dir = path.parent
    for imp in report.imports:
        imp_path = _resolve_import(base_dir, imp, root)
        if not imp_path.exists():
            report.missing_imports.append(imp)

    # Git freshness
    if tracked is not None:
        report.last_git_commit_iso = _git_last_commit_iso(root, rel)

    # Analyze issues and recommendations
    if "local" in scope:
        report.issues.append("CLAUDE.local.md is deprecated; prefer @imports in CLAUDE.md")

    if report.lines > 500:
        report.issues.append(f"Very large ({report.lines} lines); consider splitting via @imports")
        report.recommendations.append("Keep top-level CLAUDE.md concise; extract details to imported files")
    elif report.lines > 300:
        report.recommendations.append("Consider splitting larger sections into @imported files")

    if report.missing_imports:
        report.issues.append(f"Missing @imports: {', '.join(report.missing_imports)}")

    if not report.has_headings:
        report.issues.append("No markdown headings; structure may be hard for agents to parse")
        report.recommendations.append("Add section headings for Commands, Architecture, Conventions, etc.")

    if report.word_count < 50 and report.exists:
        report.recommendations.append("Very minimal content; consider adding project conventions and commands")

    # Check for essential sections
    text_lower = text.lower()
    missing_sections = []
    if "build" not in text_lower and "test" not in text_lower and "lint" not in text_lower:
        missing_sections.append("commands (build/test/lint)")
    if "architecture" not in text_lower and "structure" not in text_lower:
        missing_sections.append("architecture overview")

    if missing_sections:
        report.recommendations.append(f"Consider adding: {', '.join(missing_sections)}")

    return report


def _discover_settings_files(root: Path) -> List[Tuple[Path, str]]:
    """Discover Claude Code settings.json files."""
    home = Path.home()
    candidates = [
        (home / ".claude" / "settings.json", "user"),
        (root / ".claude" / "settings.json", "project"),
        (root / ".claude" / "settings.local.json", "local"),
    ]

    # Check for managed settings (enterprise)
    managed_paths = [
        Path("/etc/claude/settings.json"),
        home / ".config" / "claude" / "managed-settings.json",
    ]
    for mp in managed_paths:
        if mp.exists():
            candidates.append((mp, "managed"))

    return candidates


def _analyze_settings_file(path: Path, scope: str) -> SettingsFileReport:
    """Analyze a Claude Code settings file."""
    report = SettingsFileReport(path=str(path), exists=path.exists(), scope=scope)

    if not report.exists:
        return report

    report.bytes = path.stat().st_size
    data = _safe_read_json(path)

    if data is None:
        report.issues.append("Invalid JSON format")
        return report

    report.has_allowed_tools = bool(data.get("permissions", {}).get("allow"))
    report.has_deny_tools = bool(data.get("permissions", {}).get("deny"))
    report.has_custom_instructions = bool(data.get("customInstructions"))

    mcp_servers = data.get("mcpServers", {})
    report.has_mcp_servers = bool(mcp_servers)
    report.mcp_server_count = len(mcp_servers)

    # Check for potential issues
    if report.has_allowed_tools:
        allowed = data.get("permissions", {}).get("allow", [])
        if "Bash(*)" in allowed or "Bash(*)'" in str(allowed):
            report.issues.append("Overly permissive Bash(*) in allowed tools - security risk")

    return report


def _discover_mcp_configs(root: Path) -> List[Tuple[Path, str]]:
    """Discover MCP configuration files."""
    home = Path.home()
    return [
        (home / ".claude" / "mcp.json", "user"),
        (root / ".mcp.json", "project"),
        (root / ".claude" / "mcp.json", "project"),
    ]


def _analyze_mcp_config(path: Path, scope: str) -> MCPConfigReport:
    """Analyze an MCP configuration file."""
    report = MCPConfigReport(path=str(path), exists=path.exists(), scope=scope)

    if not report.exists:
        return report

    data = _safe_read_json(path)
    if data is None:
        report.issues.append("Invalid JSON format")
        return report

    servers = data.get("mcpServers", {})
    report.server_count = len(servers)
    report.servers = list(servers.keys())

    # Check for issues
    if report.server_count > 10:
        report.issues.append(f"Many MCP servers ({report.server_count}); may impact context with lazy loading disabled")

    return report


def _discover_skills(root: Path) -> List[Tuple[Path, str]]:
    """Discover Claude Code skills."""
    home = Path.home()
    skills = []

    # User skills
    user_skills_dir = home / ".claude" / "skills"
    if user_skills_dir.exists():
        for skill_dir in user_skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skills.append((skill_dir, "user"))

    # Project skills
    project_skills_dir = root / ".claude" / "skills"
    if project_skills_dir.exists():
        for skill_dir in project_skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skills.append((skill_dir, "project"))

    return skills


def _analyze_skill(skill_dir: Path, scope: str, root: Path) -> SkillReport:
    """Analyze a Claude Code skill."""
    skill_md = skill_dir / "SKILL.md"

    try:
        rel = str(skill_dir.relative_to(root))
    except ValueError:
        rel = str(skill_dir)

    report = SkillReport(
        path=rel,
        name=skill_dir.name,
        scope=scope,
        has_scripts=(skill_dir / "scripts").exists(),
        has_references=(skill_dir / "references").exists(),
        has_assets=(skill_dir / "assets").exists(),
    )

    if skill_md.exists():
        text = _safe_read_text(skill_md)
        report.skill_md_lines = text.count("\n") + 1

        # Check for description in frontmatter
        if "description:" in text:
            report.has_description = True
        else:
            report.issues.append("Missing description in SKILL.md frontmatter")

        if report.skill_md_lines > 500:
            report.issues.append(f"SKILL.md very large ({report.skill_md_lines} lines); consider using references/")

    return report


def _discover_subagents(root: Path) -> List[Tuple[Path, str]]:
    """Discover Claude Code subagents."""
    home = Path.home()
    agents = []

    # User agents
    user_agents_dir = home / ".claude" / "agents"
    if user_agents_dir.exists():
        for agent_file in user_agents_dir.glob("*.md"):
            agents.append((agent_file, "user"))

    # Project agents
    project_agents_dir = root / ".claude" / "agents"
    if project_agents_dir.exists():
        for agent_file in project_agents_dir.glob("*.md"):
            agents.append((agent_file, "project"))

    return agents


def _analyze_subagent(agent_path: Path, scope: str, root: Path) -> SubagentReport:
    """Analyze a Claude Code subagent."""
    try:
        rel = str(agent_path.relative_to(root))
    except ValueError:
        rel = str(agent_path)

    report = SubagentReport(
        path=rel,
        name=agent_path.stem,
        scope=scope,
    )

    if agent_path.exists():
        text = _safe_read_text(agent_path)
        report.agent_md_lines = text.count("\n") + 1

        if "description:" in text.lower() or text.strip():
            report.has_description = True

    return report


def _get_directory_stats(root: Path, tracked: Optional[List[str]]) -> List[Dict[str, Any]]:
    """Get top directories by file count."""
    top_dirs: Dict[str, int] = {}

    if tracked is not None:
        for f in tracked:
            parts = f.split("/", 1)
            top = parts[0] if len(parts) > 1 else "."
            top_dirs[top] = top_dirs.get(top, 0) + 1
    else:
        for p in root.iterdir():
            if p.is_dir() and p.name not in (".git", "node_modules", "dist", "build", ".venv", "__pycache__"):
                count = sum(1 for _ in p.rglob("*") if _.is_file())
                top_dirs[p.name] = count

    sorted_dirs = sorted(top_dirs.items(), key=lambda kv: kv[1], reverse=True)[:20]
    return [{"dir": d, "files": n} for d, n in sorted_dirs]


def audit(root: Path, include_user_scope: bool = True) -> Dict[str, Any]:
    """Run full audit on repository."""
    root = root.resolve()

    # Repo scale
    tracked = _git_tracked_files(root) if _is_git_repo(root) else None
    if tracked is not None:
        file_count = len(tracked)
        file_count_source = "git ls-files"
    else:
        file_count = 0
        exclude_dirs = {"node_modules", ".git", "dist", "build", ".venv", "__pycache__"}
        for p in root.rglob("*"):
            if p.is_file() and not any(part in exclude_dirs for part in p.parts):
                file_count += 1
        file_count_source = "filesystem walk (excludes node_modules/.git/dist/build/.venv/__pycache__)"

    large_repo = file_count > 3000

    # Memory files
    memory_files = _discover_memory_files(root)
    memory_reports = [_analyze_memory_file(p, s, root, tracked) for p, s in memory_files]

    # Settings
    settings_files = _discover_settings_files(root)
    settings_reports = [_analyze_settings_file(p, s) for p, s in settings_files]
    if not include_user_scope:
        settings_reports = [r for r in settings_reports if r.scope != "user"]

    # MCP configs
    mcp_configs = _discover_mcp_configs(root)
    mcp_reports = [_analyze_mcp_config(p, s) for p, s in mcp_configs]
    if not include_user_scope:
        mcp_reports = [r for r in mcp_reports if r.scope != "user"]

    # Skills
    skills = _discover_skills(root)
    skill_reports = [_analyze_skill(p, s, root) for p, s in skills]
    if not include_user_scope:
        skill_reports = [r for r in skill_reports if r.scope != "user"]

    # Subagents
    subagents = _discover_subagents(root)
    subagent_reports = [_analyze_subagent(p, s, root) for p, s in subagents]
    if not include_user_scope:
        subagent_reports = [r for r in subagent_reports if r.scope != "user"]

    # Directory stats
    dir_stats = _get_directory_stats(root, tracked)

    # Compile recommendations
    all_issues = []
    all_recommendations = []

    # Memory issues
    existing_memory = [r for r in memory_reports if r.exists]
    if not existing_memory:
        all_issues.append({
            "priority": "P0",
            "category": "memory",
            "message": "No CLAUDE.md found; create one to provide project context to Claude Code"
        })

    for r in memory_reports:
        for issue in r.issues:
            all_issues.append({
                "priority": "P1" if "missing" in issue.lower() else "P2",
                "category": "memory",
                "file": r.path,
                "message": issue
            })
        for rec in r.recommendations:
            all_recommendations.append({
                "priority": "P2",
                "category": "memory",
                "file": r.path,
                "message": rec
            })

    # Settings issues
    for r in settings_reports:
        for issue in r.issues:
            all_issues.append({
                "priority": "P1",
                "category": "settings",
                "file": r.path,
                "message": issue
            })

    # MCP issues
    for r in mcp_reports:
        for issue in r.issues:
            all_issues.append({
                "priority": "P2",
                "category": "mcp",
                "file": r.path,
                "message": issue
            })

    # Skill issues
    for r in skill_reports:
        for issue in r.issues:
            all_issues.append({
                "priority": "P2",
                "category": "skills",
                "file": r.path,
                "message": issue
            })

    # Large repo recommendation
    if large_repo:
        all_recommendations.append({
            "priority": "P1",
            "category": "scale",
            "message": f"Repo has {file_count} files (>3000 threshold). Consider a context engine or retrieval layer for reliable agent context."
        })

    now_iso = datetime.now(timezone.utc).isoformat()

    return {
        "meta": {
            "tool": "optimizing-claude-code.audit_repo",
            "generated_at": now_iso,
            "root": str(root),
        },
        "repo_scale": {
            "file_count": file_count,
            "file_count_source": file_count_source,
            "large_repo_threshold": 3000,
            "is_large_repo": large_repo,
            "is_git_repo": _is_git_repo(root),
            "top_level_dirs_by_file_count": dir_stats,
        },
        "claude_memory": {
            "discovered_files": [asdict(r) for r in memory_reports if r.exists],
            "missing_standard_locations": [
                asdict(r) for r in memory_reports
                if not r.exists and r.scope in ("project", "local")
            ],
        },
        "claude_settings": {
            "discovered_files": [asdict(r) for r in settings_reports if r.exists],
        },
        "mcp_configuration": {
            "discovered_files": [asdict(r) for r in mcp_reports if r.exists],
            "total_servers": sum(r.server_count for r in mcp_reports if r.exists),
        },
        "skills": {
            "discovered": [asdict(r) for r in skill_reports],
            "total_count": len(skill_reports),
        },
        "subagents": {
            "discovered": [asdict(r) for r in subagent_reports],
            "total_count": len(subagent_reports),
        },
        "issues": sorted(all_issues, key=lambda x: (x["priority"], x["category"])),
        "recommendations": sorted(all_recommendations, key=lambda x: (x["priority"], x["category"])),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Audit a repository for Claude Code optimization opportunities"
    )
    ap.add_argument("--root", default=".", help="Repository root directory")
    ap.add_argument("--format", default="json", choices=["json"], help="Output format")
    ap.add_argument("--include-user-scope", action="store_true",
                    help="Include user-scope files (outside project)")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Error: {root} does not exist", file=sys.stderr)
        return 1

    report = audit(root, include_user_scope=args.include_user_scope)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
