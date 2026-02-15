#!/usr/bin/env python3
"""List all Claude Code skills from user and project scopes."""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def get_user_skills_dir() -> Path:
    """Get the user-level skills directory."""
    return Path.home() / ".claude" / "skills"


def get_project_skills_dir() -> Path:
    """Get the project-level skills directory (current working directory)."""
    return Path.cwd() / ".claude" / "skills"


def parse_skill_metadata(skill_path: Path) -> dict | None:
    """Parse SKILL.md frontmatter to extract name and description."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    try:
        content = skill_md.read_text()
        # Parse YAML frontmatter between --- markers
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return {"name": skill_path.name, "description": "(no frontmatter)"}

        frontmatter = match.group(1)
        metadata = {"name": skill_path.name, "description": ""}

        for line in frontmatter.split("\n"):
            if line.startswith("name:"):
                metadata["name"] = line.split(":", 1)[1].strip().strip('"\'')
            elif line.startswith("description:"):
                metadata["description"] = line.split(":", 1)[1].strip().strip('"\'')

        return metadata
    except Exception as e:
        return {"name": skill_path.name, "description": f"(error reading: {e})"}


def list_skills(scope: str | None = None, output_format: str = "text") -> list[dict]:
    """List skills from specified scope(s).

    Args:
        scope: "user", "project", or None for both
        output_format: "text", "json", or "table"

    Returns:
        List of skill info dicts
    """
    skills = []

    scopes_to_check = []
    if scope is None or scope == "user":
        scopes_to_check.append(("user", get_user_skills_dir()))
    if scope is None or scope == "project":
        scopes_to_check.append(("project", get_project_skills_dir()))

    for scope_name, skills_dir in scopes_to_check:
        if not skills_dir.exists():
            continue

        for item in sorted(skills_dir.iterdir()):
            if item.is_dir() and (item / "SKILL.md").exists():
                metadata = parse_skill_metadata(item)
                if metadata:
                    skills.append({
                        "name": metadata["name"],
                        "directory": item.name,
                        "scope": scope_name,
                        "path": str(item),
                        "description": metadata["description"],
                    })

    return skills


def format_output(skills: list[dict], output_format: str) -> str:
    """Format skills list for output."""
    if output_format == "json":
        return json.dumps(skills, indent=2)

    if not skills:
        return "No skills found."

    if output_format == "table":
        # Simple table format
        lines = ["NAME | SCOPE | DESCRIPTION", "-" * 60]
        for s in skills:
            desc = s["description"][:40] + "..." if len(s["description"]) > 40 else s["description"]
            lines.append(f"{s['name']} | {s['scope']} | {desc}")
        return "\n".join(lines)

    # Default text format
    lines = []
    current_scope = None
    for s in skills:
        if s["scope"] != current_scope:
            if current_scope is not None:
                lines.append("")
            lines.append(f"=== {s['scope'].upper()} SKILLS ({get_user_skills_dir() if s['scope'] == 'user' else get_project_skills_dir()}) ===")
            current_scope = s["scope"]

        lines.append(f"\n  {s['name']}")
        if s["description"]:
            # Wrap description
            desc = s["description"]
            lines.append(f"    {desc[:80]}")
            if len(desc) > 80:
                lines.append(f"    {desc[80:160]}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="List Claude Code skills")
    parser.add_argument(
        "--scope", "-s",
        choices=["user", "project"],
        help="Filter by scope (default: show both)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "table"],
        default="text",
        help="Output format (default: text)"
    )
    args = parser.parse_args()

    skills = list_skills(args.scope, args.format)
    print(format_output(skills, args.format))

    return 0 if skills else 1


if __name__ == "__main__":
    sys.exit(main())
