#!/usr/bin/env python3
"""Show detailed information about a Claude Code skill."""

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


def find_skill(name: str, scope: str | None = None) -> tuple[Path | None, str | None]:
    """Find a skill by name, optionally filtering by scope.

    Returns:
        Tuple of (skill_path, scope_name) or (None, None) if not found
    """
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


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from SKILL.md content."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    frontmatter = match.group(1)
    metadata = {}

    current_key = None
    current_value = []

    for line in frontmatter.split("\n"):
        # Check for new key
        key_match = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if key_match:
            # Save previous key if exists
            if current_key:
                value = "\n".join(current_value).strip()
                metadata[current_key] = value.strip('"\'')

            current_key = key_match.group(1)
            current_value = [key_match.group(2)]
        elif current_key and line.startswith("  "):
            # Continuation of multi-line value
            current_value.append(line.strip())

    # Save last key
    if current_key:
        value = "\n".join(current_value).strip()
        metadata[current_key] = value.strip('"\'')

    return metadata


def get_skill_info(skill_path: Path, scope: str) -> dict:
    """Get comprehensive information about a skill."""
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()

    # Parse frontmatter
    metadata = parse_frontmatter(content)

    # Get body (everything after frontmatter)
    body_match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", content, re.DOTALL)
    body = body_match.group(1).strip() if body_match else content

    # Count body lines/words
    body_lines = len(body.split("\n"))
    body_words = len(body.split())

    # Get directory structure
    files = []
    dirs = set()
    total_size = 0

    for item in skill_path.rglob("*"):
        rel_path = item.relative_to(skill_path)
        if item.is_file():
            size = item.stat().st_size
            total_size += size
            files.append({
                "path": str(rel_path),
                "size": size,
                "type": item.suffix or "(no extension)"
            })
        elif item.is_dir():
            dirs.add(str(rel_path))

    # Check for standard directories
    has_scripts = (skill_path / "scripts").exists()
    has_references = (skill_path / "references").exists()
    has_assets = (skill_path / "assets").exists()

    return {
        "name": metadata.get("name", skill_path.name),
        "directory": skill_path.name,
        "scope": scope,
        "path": str(skill_path),
        "description": metadata.get("description", ""),
        "metadata": metadata,
        "body_lines": body_lines,
        "body_words": body_words,
        "file_count": len(files),
        "total_size": total_size,
        "files": files,
        "directories": list(dirs),
        "has_scripts": has_scripts,
        "has_references": has_references,
        "has_assets": has_assets,
    }


def format_size(size: int) -> str:
    """Format size in human-readable form."""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    else:
        return f"{size / (1024 * 1024):.1f} MB"


def show_skill(name: str, scope: str | None = None, output_format: str = "text", show_files: bool = False) -> bool:
    """Show information about a skill.

    Args:
        name: Skill name
        scope: Optional scope filter
        output_format: "text" or "json"
        show_files: Include file listing

    Returns:
        True if skill found, False otherwise
    """
    skill_path, found_scope = find_skill(name, scope)

    if not skill_path:
        if scope:
            print(f"Error: Skill '{name}' not found in {scope} scope.")
        else:
            print(f"Error: Skill '{name}' not found in user or project scope.")
        return False

    try:
        info = get_skill_info(skill_path, found_scope)
    except Exception as e:
        print(f"Error reading skill: {e}")
        return False

    if output_format == "json":
        print(json.dumps(info, indent=2))
        return True

    # Text format
    print(f"{'=' * 60}")
    print(f"Skill: {info['name']}")
    print(f"{'=' * 60}")
    print(f"Scope:       {info['scope']}")
    print(f"Path:        {info['path']}")
    print(f"")
    print(f"Description:")
    print(f"  {info['description']}")
    print(f"")

    # Metadata
    if info['metadata']:
        other_meta = {k: v for k, v in info['metadata'].items() if k not in ('name', 'description')}
        if other_meta:
            print(f"Other Metadata:")
            for k, v in other_meta.items():
                print(f"  {k}: {v}")
            print(f"")

    # Stats
    print(f"Statistics:")
    print(f"  SKILL.md body: {info['body_lines']} lines, {info['body_words']} words")
    print(f"  Total files:   {info['file_count']}")
    print(f"  Total size:    {format_size(info['total_size'])}")
    print(f"")

    # Structure
    print(f"Structure:")
    print(f"  scripts/:    {'Yes' if info['has_scripts'] else 'No'}")
    print(f"  references/: {'Yes' if info['has_references'] else 'No'}")
    print(f"  assets/:     {'Yes' if info['has_assets'] else 'No'}")

    if show_files and info['files']:
        print(f"")
        print(f"Files:")
        for f in sorted(info['files'], key=lambda x: x['path']):
            print(f"  {f['path']} ({format_size(f['size'])})")

    return True


def main():
    parser = argparse.ArgumentParser(description="Show information about a Claude Code skill")
    parser.add_argument("name", help="Name of the skill to show")
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
    parser.add_argument(
        "--files",
        action="store_true",
        help="Include file listing"
    )
    args = parser.parse_args()

    success = show_skill(args.name, args.scope, args.format, args.files)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
