#!/usr/bin/env python3
"""Create a new Claude Code subagent with proper structure."""

import os
import sys
import argparse
from pathlib import Path

TEMPLATE = '''---
name: {name}
description: {description}
tools: {tools}
model: {model}
---

{prompt}
'''

AVAILABLE_TOOLS = [
    "Read", "Write", "Edit", "Glob", "Grep", "Bash", "Task",
    "WebFetch", "WebSearch", "NotebookEdit", "TodoWrite", "AskUserQuestion"
]

AVAILABLE_MODELS = ["sonnet", "opus", "haiku", "inherit"]

PERMISSION_MODES = ["default", "acceptEdits", "dontAsk", "bypassPermissions", "plan"]

def create_subagent(
    name: str,
    description: str,
    prompt: str,
    scope: str = "project",
    tools: str = None,
    model: str = "sonnet",
    permission_mode: str = None,
    disallowed_tools: str = None,
    overwrite: bool = False
) -> str:
    """
    Create a new subagent markdown file.

    Args:
        name: Subagent name (lowercase with hyphens)
        description: When Claude should delegate to this subagent
        prompt: System prompt for the subagent
        scope: "user" or "project"
        tools: Comma-separated list of tools (default: all inherited)
        model: Model to use (sonnet, opus, haiku, inherit)
        permission_mode: Permission mode override
        disallowed_tools: Tools to deny
        overwrite: Whether to overwrite existing file

    Returns:
        Path to created file
    """
    # Validate name format
    if not name.replace("-", "").replace("_", "").isalnum():
        raise ValueError(f"Invalid name '{name}'. Use lowercase letters, numbers, and hyphens.")

    # Determine target directory
    if scope == "user":
        agents_dir = Path.home() / ".claude" / "agents"
    else:
        agents_dir = Path.cwd() / ".claude" / "agents"

    # Create directory if needed
    agents_dir.mkdir(parents=True, exist_ok=True)

    # Check for existing file
    target_file = agents_dir / f"{name}.md"
    if target_file.exists() and not overwrite:
        raise FileExistsError(f"Subagent '{name}' already exists at {target_file}. Use --overwrite to replace.")

    # Build frontmatter
    frontmatter_lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
    ]

    if tools:
        frontmatter_lines.append(f"tools: {tools}")

    if disallowed_tools:
        frontmatter_lines.append(f"disallowedTools: {disallowed_tools}")

    frontmatter_lines.append(f"model: {model}")

    if permission_mode:
        frontmatter_lines.append(f"permissionMode: {permission_mode}")

    frontmatter_lines.append("---")

    # Combine with prompt
    content = "\n".join(frontmatter_lines) + "\n\n" + prompt.strip() + "\n"

    # Write file
    target_file.write_text(content)
    return str(target_file)

def main():
    parser = argparse.ArgumentParser(description="Create a new Claude Code subagent")
    parser.add_argument("name", help="Subagent name (lowercase with hyphens)")
    parser.add_argument("--description", "-d", required=True, help="When to use this subagent")
    parser.add_argument("--prompt", "-p", required=True, help="System prompt for the subagent")
    parser.add_argument("--scope", "-s", choices=["user", "project"], default="project",
                        help="Scope: user (~/.claude/agents) or project (.claude/agents)")
    parser.add_argument("--tools", "-t", help=f"Comma-separated tools: {', '.join(AVAILABLE_TOOLS)}")
    parser.add_argument("--model", "-m", choices=AVAILABLE_MODELS, default="sonnet",
                        help="Model to use (default: sonnet)")
    parser.add_argument("--permission-mode", choices=PERMISSION_MODES, help="Permission mode override")
    parser.add_argument("--disallowed-tools", help="Tools to deny")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing subagent")

    args = parser.parse_args()

    try:
        path = create_subagent(
            name=args.name,
            description=args.description,
            prompt=args.prompt,
            scope=args.scope,
            tools=args.tools,
            model=args.model,
            permission_mode=args.permission_mode,
            disallowed_tools=args.disallowed_tools,
            overwrite=args.overwrite
        )
        print(f"Created subagent at: {path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
