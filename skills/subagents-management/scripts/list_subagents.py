#!/usr/bin/env python3
"""List all Claude Code subagents from user and project scopes."""

import os
import sys
import re
from pathlib import Path

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    return frontmatter

def list_subagents(scope: str = "all") -> list:
    """
    List subagents from specified scope.

    Args:
        scope: "user", "project", or "all"

    Returns:
        List of dicts with subagent info
    """
    agents = []

    user_dir = Path.home() / ".claude" / "agents"
    project_dir = Path.cwd() / ".claude" / "agents"

    dirs_to_check = []
    if scope in ("user", "all"):
        dirs_to_check.append(("user", user_dir))
    if scope in ("project", "all"):
        dirs_to_check.append(("project", project_dir))

    for scope_name, agents_dir in dirs_to_check:
        if not agents_dir.exists():
            continue

        for md_file in agents_dir.glob("*.md"):
            try:
                content = md_file.read_text()
                frontmatter = parse_frontmatter(content)

                agents.append({
                    "name": frontmatter.get("name", md_file.stem),
                    "description": frontmatter.get("description", "No description"),
                    "tools": frontmatter.get("tools", "inherited"),
                    "model": frontmatter.get("model", "sonnet"),
                    "scope": scope_name,
                    "path": str(md_file)
                })
            except Exception as e:
                print(f"Warning: Could not parse {md_file}: {e}", file=sys.stderr)

    return agents

def main():
    import argparse
    parser = argparse.ArgumentParser(description="List Claude Code subagents")
    parser.add_argument("--scope", choices=["user", "project", "all"], default="all",
                        help="Which scope to list (default: all)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    agents = list_subagents(args.scope)

    if args.json:
        import json
        print(json.dumps(agents, indent=2))
    else:
        if not agents:
            print("No subagents found.")
            return

        print(f"Found {len(agents)} subagent(s):\n")
        for agent in agents:
            print(f"  [{agent['scope'].upper()}] {agent['name']}")
            print(f"    Description: {agent['description'][:60]}...")
            print(f"    Model: {agent['model']}")
            print(f"    Path: {agent['path']}")
            print()

if __name__ == "__main__":
    main()
