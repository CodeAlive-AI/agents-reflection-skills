#!/usr/bin/env python3
"""Review a Claude Code skill against best practices."""

import argparse
import json
import re
import sys
from pathlib import Path


def get_user_skills_dir() -> Path:
    return Path.home() / ".claude" / "skills"


def get_project_skills_dir() -> Path:
    return Path.cwd() / ".claude" / "skills"


def find_skill(name: str, scope: str | None = None) -> tuple[Path | None, str | None]:
    """Find a skill by name, optionally filtering by scope."""
    scopes_to_check = []
    if scope is None or scope == "user":
        scopes_to_check.append(("user", get_user_skills_dir()))
    if scope is None or scope == "project":
        scopes_to_check.append(("project", get_project_skills_dir()))

    for scope_name, skills_dir in scopes_to_check:
        skill_path = skills_dir / name
        if skill_path.exists() and (skill_path / "SKILL.md").exists():
            return skill_path, scope_name
    return None, None


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (metadata, body)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter = match.group(1)
    body = match.group(2)
    metadata = {}

    for line in frontmatter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"\'')

    return metadata, body


def check_name(name: str) -> list[dict]:
    """Check name against best practices."""
    issues = []

    # Reserved words
    reserved = ["anthropic", "claude"]
    for word in reserved:
        if word in name.lower():
            issues.append({
                "severity": "warning",
                "rule": "reserved-word",
                "message": f"Name contains reserved word '{word}'",
                "suggestion": f"Consider renaming without '{word}' (e.g., 'skills-manager' instead of 'claude-skills-manager')"
            })

    # Naming convention (gerund form preferred)
    if not re.match(r"^[a-z][a-z0-9-]*$", name):
        issues.append({
            "severity": "error",
            "rule": "name-format",
            "message": "Name must be lowercase letters, numbers, and hyphens only",
            "suggestion": "Use format like 'processing-pdfs' or 'managing-databases'"
        })

    if len(name) > 64:
        issues.append({
            "severity": "error",
            "rule": "name-length",
            "message": f"Name exceeds 64 characters ({len(name)} chars)",
            "suggestion": "Shorten the name to 64 characters or less"
        })

    # Check for gerund form (recommended but not required)
    gerund_pattern = r"^[a-z]+-?[a-z]*ing(-[a-z]+)*$|^[a-z]*ing-[a-z]+(-[a-z]+)*$"
    if not re.match(gerund_pattern, name):
        issues.append({
            "severity": "info",
            "rule": "gerund-form",
            "message": "Name doesn't use recommended gerund form (verb + -ing)",
            "suggestion": f"Consider renaming to gerund form (e.g., 'managing-skills' instead of '{name}')"
        })

    return issues


def check_description(description: str) -> list[dict]:
    """Check description against best practices."""
    issues = []

    if not description:
        issues.append({
            "severity": "error",
            "rule": "description-required",
            "message": "Description is empty",
            "suggestion": "Add a description that explains what the skill does and when to use it"
        })
        return issues

    if len(description) > 1024:
        issues.append({
            "severity": "error",
            "rule": "description-length",
            "message": f"Description exceeds 1024 characters ({len(description)} chars)",
            "suggestion": "Shorten the description to 1024 characters or less"
        })

    # Check for trigger words
    trigger_patterns = [
        r"\buse when\b",
        r"\buse for\b",
        r"\btrigger[s]? on\b",
        r"\bwhen (the )?user\b",
        r"\bwhen asked\b",
    ]
    has_trigger = any(re.search(p, description.lower()) for p in trigger_patterns)
    if not has_trigger:
        issues.append({
            "severity": "warning",
            "rule": "missing-triggers",
            "message": "Description doesn't include trigger conditions",
            "suggestion": "Add 'Use when...' to help Claude know when to invoke this skill"
        })

    # Check for first/second person (should be third person)
    first_second_person = [
        (r"\bI can\b", "I can"),
        (r"\bI will\b", "I will"),
        (r"\bI help\b", "I help"),
        (r"\byou can\b", "you can"),
        (r"\byou will\b", "you will"),
        (r"\bwe can\b", "we can"),
    ]
    for pattern, phrase in first_second_person:
        if re.search(pattern, description, re.IGNORECASE):
            issues.append({
                "severity": "warning",
                "rule": "third-person",
                "message": f"Description uses '{phrase}' instead of third person",
                "suggestion": "Rewrite in third person (e.g., 'Processes files...' not 'I process files...')"
            })
            break

    # Check for vague descriptions
    vague_patterns = [
        (r"^helps with \w+$", "Too vague"),
        (r"^processes data$", "Too vague"),
        (r"^does stuff", "Too vague"),
        (r"^utility for", "Too vague"),
        (r"^helper for", "Too vague"),
    ]
    for pattern, reason in vague_patterns:
        if re.search(pattern, description.lower()):
            issues.append({
                "severity": "warning",
                "rule": "vague-description",
                "message": f"Description is too vague: {reason}",
                "suggestion": "Be specific about what the skill does and include key terms"
            })
            break

    return issues


def check_body(body: str, skill_path: Path) -> list[dict]:
    """Check SKILL.md body against best practices."""
    issues = []
    lines = body.split("\n")
    line_count = len(lines)

    # Line count check
    if line_count > 500:
        issues.append({
            "severity": "warning",
            "rule": "body-length",
            "message": f"SKILL.md body exceeds 500 lines ({line_count} lines)",
            "suggestion": "Split content into separate reference files using progressive disclosure"
        })

    # Check for time-sensitive information
    time_patterns = [
        (r"\b(before|after) (january|february|march|april|may|june|july|august|september|october|november|december) \d{4}\b", "date reference"),
        (r"\b(before|after) \d{4}\b", "year reference"),
        (r"\bas of \d{4}\b", "as of year"),
        (r"\bstarting (in )?\d{4}\b", "starting year"),
        (r"\buntil \d{4}\b", "until year"),
    ]
    for pattern, desc in time_patterns:
        matches = re.findall(pattern, body.lower())
        if matches:
            issues.append({
                "severity": "warning",
                "rule": "time-sensitive",
                "message": f"Body contains time-sensitive information ({desc})",
                "suggestion": "Move time-sensitive info to 'Old patterns' section or remove"
            })
            break

    # Check for Windows-style paths
    if re.search(r"[a-zA-Z]:\\|\\\\", body):
        issues.append({
            "severity": "warning",
            "rule": "windows-paths",
            "message": "Body contains Windows-style paths (backslashes)",
            "suggestion": "Use forward slashes for cross-platform compatibility"
        })

    # Check for deeply nested references (more than one level)
    ref_files = re.findall(r"\[.*?\]\(([^)]+\.md)\)", body)
    for ref_file in ref_files:
        ref_path = skill_path / ref_file
        if ref_path.exists():
            ref_content = ref_path.read_text()
            nested_refs = re.findall(r"\[.*?\]\(([^)]+\.md)\)", ref_content)
            if nested_refs:
                issues.append({
                    "severity": "info",
                    "rule": "nested-references",
                    "message": f"Reference file '{ref_file}' contains further references",
                    "suggestion": "Keep references one level deep from SKILL.md for reliable file reading"
                })

    # Check for table of contents in long files
    if line_count > 100:
        toc_patterns = [r"## contents", r"## table of contents", r"- \[.*\]\(#"]
        has_toc = any(re.search(p, body.lower()) for p in toc_patterns)
        if not has_toc:
            issues.append({
                "severity": "info",
                "rule": "missing-toc",
                "message": "Long file (>100 lines) without table of contents",
                "suggestion": "Add a table of contents to help Claude navigate the content"
            })

    return issues


def check_structure(skill_path: Path) -> list[dict]:
    """Check skill directory structure."""
    issues = []

    # Check for reference files longer than 100 lines without TOC
    for md_file in skill_path.glob("**/*.md"):
        if md_file.name == "SKILL.md":
            continue
        content = md_file.read_text()
        lines = content.split("\n")
        if len(lines) > 100:
            toc_patterns = [r"## contents", r"## table of contents", r"- \[.*\]\(#"]
            has_toc = any(re.search(p, content.lower()) for p in toc_patterns)
            if not has_toc:
                rel_path = md_file.relative_to(skill_path)
                issues.append({
                    "severity": "info",
                    "rule": "reference-toc",
                    "message": f"Reference file '{rel_path}' exceeds 100 lines without TOC",
                    "suggestion": "Add table of contents to help Claude navigate"
                })

    return issues


def review_skill(name: str, scope: str | None = None, output_format: str = "text") -> dict:
    """Review a skill against best practices.

    Returns:
        Dict with skill info and issues found
    """
    skill_path, found_scope = find_skill(name, scope)

    if not skill_path:
        return {
            "error": f"Skill '{name}' not found",
            "found": False
        }

    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()
    metadata, body = parse_frontmatter(content)

    skill_name = metadata.get("name", skill_path.name)
    description = metadata.get("description", "")

    all_issues = []
    all_issues.extend(check_name(skill_name))
    all_issues.extend(check_description(description))
    all_issues.extend(check_body(body, skill_path))
    all_issues.extend(check_structure(skill_path))

    # Count by severity
    error_count = len([i for i in all_issues if i["severity"] == "error"])
    warning_count = len([i for i in all_issues if i["severity"] == "warning"])
    info_count = len([i for i in all_issues if i["severity"] == "info"])

    # Calculate score (simple scoring)
    max_score = 100
    score = max_score - (error_count * 20) - (warning_count * 10) - (info_count * 2)
    score = max(0, score)

    return {
        "found": True,
        "name": skill_name,
        "scope": found_scope,
        "path": str(skill_path),
        "description": description,
        "body_lines": len(body.split("\n")),
        "issues": all_issues,
        "summary": {
            "errors": error_count,
            "warnings": warning_count,
            "info": info_count,
            "score": score
        }
    }


def format_output(result: dict, output_format: str) -> str:
    """Format review results for output."""
    if output_format == "json":
        return json.dumps(result, indent=2)

    if not result.get("found"):
        return f"Error: {result.get('error', 'Unknown error')}"

    lines = [
        f"{'=' * 60}",
        f"Skill Review: {result['name']}",
        f"{'=' * 60}",
        f"Scope: {result['scope']}",
        f"Path:  {result['path']}",
        f"Lines: {result['body_lines']}",
        f"",
        f"Score: {result['summary']['score']}/100",
        f"  Errors:   {result['summary']['errors']}",
        f"  Warnings: {result['summary']['warnings']}",
        f"  Info:     {result['summary']['info']}",
    ]

    if result["issues"]:
        lines.append("")
        lines.append("Issues Found:")
        lines.append("-" * 40)

        for issue in result["issues"]:
            severity = issue["severity"].upper()
            icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(issue["severity"], "•")
            lines.append(f"")
            lines.append(f"{icon} [{severity}] {issue['rule']}")
            lines.append(f"   {issue['message']}")
            lines.append(f"   → {issue['suggestion']}")
    else:
        lines.append("")
        lines.append("✅ No issues found! Skill follows best practices.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Review a Claude Code skill against best practices"
    )
    parser.add_argument("name", help="Name of the skill to review")
    parser.add_argument(
        "--scope", "-s",
        choices=["user", "project"],
        help="Scope to search (default: search both)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    args = parser.parse_args()

    result = review_skill(args.name, args.scope, args.format)
    print(format_output(result, args.format))

    if not result.get("found"):
        return 1
    return 0 if result["summary"]["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
