#!/usr/bin/env python3
"""Move a Claude Code subagent between user and project scopes."""

import os
import sys
import shutil
import argparse
from pathlib import Path

def find_subagent(name: str) -> tuple:
    """
    Find a subagent by name across both scopes.

    Returns:
        Tuple of (scope, path) or (None, None) if not found
    """
    user_dir = Path.home() / ".claude" / "agents"
    project_dir = Path.cwd() / ".claude" / "agents"

    # Check project first (higher priority)
    project_file = project_dir / f"{name}.md"
    if project_file.exists():
        return ("project", project_file)

    # Check user scope
    user_file = user_dir / f"{name}.md"
    if user_file.exists():
        return ("user", user_file)

    return (None, None)

def move_subagent(name: str, to_scope: str, overwrite: bool = False) -> tuple:
    """
    Move a subagent to a different scope.

    Args:
        name: Subagent name
        to_scope: Target scope ("user" or "project")
        overwrite: Whether to overwrite if exists at target

    Returns:
        Tuple of (old_path, new_path)
    """
    current_scope, current_path = find_subagent(name)

    if not current_path:
        raise FileNotFoundError(f"Subagent '{name}' not found in user or project scope.")

    if current_scope == to_scope:
        raise ValueError(f"Subagent '{name}' is already in {to_scope} scope.")

    # Determine target
    if to_scope == "user":
        target_dir = Path.home() / ".claude" / "agents"
    else:
        target_dir = Path.cwd() / ".claude" / "agents"

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{name}.md"

    if target_path.exists() and not overwrite:
        raise FileExistsError(f"Subagent '{name}' already exists at {target_path}. Use --overwrite to replace.")

    # Move the file
    shutil.move(str(current_path), str(target_path))

    return (str(current_path), str(target_path))

def main():
    parser = argparse.ArgumentParser(description="Move a subagent between user and project scopes")
    parser.add_argument("name", help="Subagent name to move")
    parser.add_argument("--to", "-t", required=True, choices=["user", "project"],
                        help="Target scope")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite if subagent exists at target")

    args = parser.parse_args()

    try:
        old_path, new_path = move_subagent(args.name, args.to, args.overwrite)
        print(f"Moved subagent '{args.name}':")
        print(f"  From: {old_path}")
        print(f"  To:   {new_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
