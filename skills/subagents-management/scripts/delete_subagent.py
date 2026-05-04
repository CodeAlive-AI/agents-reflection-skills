#!/usr/bin/env python3
"""Delete a Claude Code subagent."""

import os
import sys
import argparse
from pathlib import Path

def find_subagent(name: str, scope: str = None) -> tuple:
    """
    Find a subagent by name.

    Args:
        name: Subagent name
        scope: Optional scope to search ("user", "project", or None for both)

    Returns:
        Tuple of (scope, path) or (None, None) if not found
    """
    user_dir = Path.home() / ".claude" / "agents"
    project_dir = Path.cwd() / ".claude" / "agents"

    if scope in (None, "project"):
        project_file = project_dir / f"{name}.md"
        if project_file.exists():
            return ("project", project_file)

    if scope in (None, "user"):
        user_file = user_dir / f"{name}.md"
        if user_file.exists():
            return ("user", user_file)

    return (None, None)

def delete_subagent(name: str, scope: str = None, force: bool = False) -> str:
    """
    Delete a subagent by name.

    Args:
        name: Subagent name
        scope: Optional specific scope ("user" or "project")
        force: Skip confirmation

    Returns:
        Path of deleted file
    """
    found_scope, path = find_subagent(name, scope)

    if not path:
        scope_msg = f" in {scope} scope" if scope else ""
        raise FileNotFoundError(f"Subagent '{name}' not found{scope_msg}.")

    # Delete the file
    path.unlink()
    return str(path)

def main():
    parser = argparse.ArgumentParser(description="Delete a Claude Code subagent")
    parser.add_argument("name", help="Subagent name to delete")
    parser.add_argument("--scope", "-s", choices=["user", "project"],
                        help="Specific scope to delete from (searches both if not specified)")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Skip confirmation")

    args = parser.parse_args()

    # Find the subagent first
    found_scope, path = find_subagent(args.name, args.scope)

    if not path:
        scope_msg = f" in {args.scope} scope" if args.scope else ""
        print(f"Error: Subagent '{args.name}' not found{scope_msg}.", file=sys.stderr)
        sys.exit(1)

    # Confirm unless force
    if not args.force:
        response = input(f"Delete subagent '{args.name}' from {found_scope} scope? ({path}) [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)

    try:
        deleted_path = delete_subagent(args.name, args.scope, args.force)
        print(f"Deleted subagent: {deleted_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
