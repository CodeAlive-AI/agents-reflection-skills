#!/usr/bin/env python3
"""Delete a Claude Code skill."""

import argparse
import shutil
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


def delete_skill(name: str, scope: str | None = None, force: bool = False) -> bool:
    """Delete a skill by name.

    Args:
        name: Skill name (directory name)
        scope: "user", "project", or None to search both
        force: Skip confirmation prompt

    Returns:
        True if deleted, False otherwise
    """
    skill_path, found_scope = find_skill(name, scope)

    if not skill_path:
        if scope:
            print(f"Error: Skill '{name}' not found in {scope} scope.")
        else:
            print(f"Error: Skill '{name}' not found in user or project scope.")
        return False

    print(f"Found skill '{name}' at: {skill_path}")
    print(f"Scope: {found_scope}")

    if not force:
        # List contents
        files = list(skill_path.rglob("*"))
        file_count = len([f for f in files if f.is_file()])
        print(f"Contains {file_count} file(s)")

        response = input("\nDelete this skill? [y/N]: ").strip().lower()
        if response != "y":
            print("Cancelled.")
            return False

    try:
        shutil.rmtree(skill_path)
        print(f"Deleted skill '{name}' from {found_scope} scope.")
        return True
    except Exception as e:
        print(f"Error deleting skill: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Delete a Claude Code skill")
    parser.add_argument("name", help="Name of the skill to delete")
    parser.add_argument(
        "--scope", "-s",
        choices=["user", "project"],
        help="Scope to search (default: search both, user takes precedence)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Skip confirmation prompt"
    )
    args = parser.parse_args()

    success = delete_skill(args.name, args.scope, args.force)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
