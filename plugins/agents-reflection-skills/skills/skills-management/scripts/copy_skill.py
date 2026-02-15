#!/usr/bin/env python3
"""Copy a skill between AI coding agents."""

import argparse
import shutil
import sys
from pathlib import Path

from agents import (
    AGENTS,
    get_agent_config,
    get_skills_dir,
    validate_agent,
)


def find_skill_in_agent(
    name: str,
    agent: str,
    scope: str | None = None,
    cwd: Path | None = None
) -> tuple[Path | None, str | None]:
    """Find a skill by name in an agent's skills directories.

    Args:
        name: Skill name (directory name)
        agent: Agent ID
        scope: Specific scope to search, or None for both
        cwd: Working directory for project scope

    Returns:
        Tuple of (skill_path, scope_name) or (None, None) if not found
    """
    scopes_to_check = []
    if scope is None or scope == "global":
        global_dir = get_skills_dir(agent, "global")
        if global_dir:
            scopes_to_check.append(("global", global_dir))
    if scope is None or scope == "project":
        project_dir = get_skills_dir(agent, "project", cwd)
        if project_dir:
            scopes_to_check.append(("project", project_dir))

    for scope_name, skills_dir in scopes_to_check:
        skill_path = skills_dir / name
        if skill_path.exists() and (skill_path / "SKILL.md").exists():
            return skill_path, scope_name

    return None, None


def copy_skill(
    name: str,
    from_agent: str,
    to_agent: str,
    from_scope: str | None = None,
    to_scope: str = "project",
    force: bool = False,
    cwd: Path | None = None
) -> tuple[bool, str]:
    """Copy a skill from one agent to another.

    Args:
        name: Skill name (directory name)
        from_agent: Source agent ID
        to_agent: Target agent ID
        from_scope: Source scope (None to auto-detect)
        to_scope: Target scope
        force: Overwrite if exists
        cwd: Working directory for project scope

    Returns:
        Tuple of (success, message)
    """
    # Find source skill
    source_path, found_scope = find_skill_in_agent(name, from_agent, from_scope, cwd)
    if not source_path:
        scope_msg = f" in {from_scope} scope" if from_scope else ""
        return False, f"Skill '{name}' not found in {from_agent}{scope_msg}"

    # Get target path
    target_base = get_skills_dir(to_agent, to_scope, cwd)
    if not target_base:
        return False, f"Could not determine skills directory for {to_agent}"

    target_path = target_base / name

    # Check same path
    if source_path.resolve() == target_path.resolve():
        return False, f"Source and target are the same path"

    # Check if target exists
    if target_path.exists():
        if not force:
            return False, f"Skill '{name}' already exists at {target_path}. Use --force to overwrite."
        if target_path.is_symlink():
            target_path.unlink()
        else:
            shutil.rmtree(target_path)

    # Copy
    try:
        target_base.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, target_path)

        from_config = get_agent_config(from_agent)
        to_config = get_agent_config(to_agent)

        return True, (
            f"Copied '{name}': {from_config['display_name']} ({found_scope}) -> "
            f"{to_config['display_name']} ({to_scope})\n"
            f"  From: {source_path}\n"
            f"  To:   {target_path}"
        )
    except Exception as e:
        return False, f"Error copying skill: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Copy a skill between AI coding agents"
    )
    parser.add_argument(
        "name",
        help="Name of the skill to copy (directory name)"
    )
    parser.add_argument(
        "--from",
        dest="from_agent",
        required=True,
        help="Source agent ID (e.g., claude-code)"
    )
    parser.add_argument(
        "--to",
        dest="to_agent",
        required=True,
        help="Target agent ID (e.g., cursor)"
    )
    parser.add_argument(
        "--from-scope",
        choices=["project", "global"],
        help="Source scope (default: auto-detect)"
    )
    parser.add_argument(
        "--to-scope",
        choices=["project", "global"],
        default="project",
        help="Target scope (default: project)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite if skill exists in target"
    )
    args = parser.parse_args()

    # Validate agents
    if not validate_agent(args.from_agent):
        print(f"Error: Unknown source agent '{args.from_agent}'")
        print(f"Valid agents: {', '.join(sorted(AGENTS.keys()))}")
        return 1

    if not validate_agent(args.to_agent):
        print(f"Error: Unknown target agent '{args.to_agent}'")
        print(f"Valid agents: {', '.join(sorted(AGENTS.keys()))}")
        return 1

    # Copy skill
    success, message = copy_skill(
        args.name,
        args.from_agent,
        args.to_agent,
        args.from_scope,
        args.to_scope,
        args.force
    )

    print(message)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
