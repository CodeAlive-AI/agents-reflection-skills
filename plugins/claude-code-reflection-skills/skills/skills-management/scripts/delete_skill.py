#!/usr/bin/env python3
"""Delete a skill from AI coding agents."""

import argparse
import shutil
import sys
from pathlib import Path

from agents import (
    AGENTS,
    detect_installed_agents,
    get_agent_config,
    get_skills_dir,
    validate_agent,
)


def get_user_skills_dir() -> Path:
    """Get the user-level skills directory."""
    return Path.home() / ".claude" / "skills"


def get_project_skills_dir() -> Path:
    """Get the project-level skills directory (current working directory)."""
    return Path.cwd() / ".claude" / "skills"


def remove_path(path: Path) -> None:
    """Remove a path, handling both symlinks and real directories."""
    if path.is_symlink():
        path.unlink()
    else:
        shutil.rmtree(path)


def find_skill(name: str, scope: str | None = None) -> tuple[Path | None, str | None]:
    """Find a skill by name in Claude Code scopes.

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
        if skill_path.exists() and (
            (skill_path / "SKILL.md").exists() or skill_path.is_symlink()
        ):
            return skill_path, scope_name

    return None, None


def find_skill_in_agents(name: str) -> list[tuple[str, str, str, Path]]:
    """Find a skill across all detected agents.

    Returns:
        List of (agent_id, display_name, scope, path) tuples
    """
    found = []
    seen_paths = set()

    for agent_id in detect_installed_agents():
        config = get_agent_config(agent_id)
        if not config:
            continue

        for scope in ("global", "project"):
            skills_dir = get_skills_dir(agent_id, scope)
            if not skills_dir:
                continue

            skill_path = skills_dir / name
            resolved = str(skill_path.resolve()) if skill_path.exists() else str(skill_path)

            if skill_path.exists() and resolved not in seen_paths:
                if (skill_path / "SKILL.md").exists() or skill_path.is_symlink():
                    seen_paths.add(resolved)
                    found.append((agent_id, config["display_name"], scope, skill_path))

    return found


def delete_skill_default(name: str, scope: str | None = None, force: bool = False) -> bool:
    """Delete a skill from Claude Code scopes (default behavior).

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
    if skill_path.is_symlink():
        print(f"Type: symlink -> {skill_path.resolve()}")

    if not force:
        if not skill_path.is_symlink():
            files = list(skill_path.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            print(f"Contains {file_count} file(s)")

        response = input("\nDelete this skill? [y/N]: ").strip().lower()
        if response != "y":
            print("Cancelled.")
            return False

    try:
        remove_path(skill_path)
        print(f"Deleted skill '{name}' from {found_scope} scope.")
    except Exception as e:
        print(f"Error deleting skill: {e}")
        return False

    # Warn about remaining copies in other agents
    remaining = find_skill_in_agents(name)
    if remaining:
        print(f"\nWarning: '{name}' still exists in {len(remaining)} other location(s):")
        for agent_id, display_name, agent_scope, path in remaining:
            print(f"  - {display_name} ({agent_id}) [{agent_scope}]: {path}")
        print("Use --all-agents to delete from all agents.")

    return True


def delete_skill_agents(
    name: str,
    agents: list[str] | None = None,
    all_agents: bool = False,
    force: bool = False,
) -> bool:
    """Delete a skill from specific agents or all detected agents.

    Args:
        name: Skill name (directory name)
        agents: Specific agent IDs to delete from
        all_agents: Delete from all detected agents
        force: Skip confirmation prompt

    Returns:
        True if all deletions succeeded, False otherwise
    """
    if all_agents:
        locations = find_skill_in_agents(name)
        if not locations:
            print(f"Error: Skill '{name}' not found in any detected agent.")
            return False
    else:
        locations = []
        for agent_id in agents:
            config = get_agent_config(agent_id)
            if not config:
                continue
            for scope in ("global", "project"):
                skills_dir = get_skills_dir(agent_id, scope)
                if not skills_dir:
                    continue
                skill_path = skills_dir / name
                if skill_path.exists() and (
                    (skill_path / "SKILL.md").exists() or skill_path.is_symlink()
                ):
                    locations.append((agent_id, config["display_name"], scope, skill_path))

        if not locations:
            agent_names = ", ".join(agents)
            print(f"Error: Skill '{name}' not found in: {agent_names}")
            return False

    # Show what will be deleted
    print(f"Found '{name}' in {len(locations)} location(s):")
    for agent_id, display_name, scope, path in locations:
        link_info = f" (symlink)" if path.is_symlink() else ""
        print(f"  - {display_name} ({agent_id}) [{scope}]: {path}{link_info}")

    if not force:
        response = input(f"\nDelete from all {len(locations)} location(s)? [y/N]: ").strip().lower()
        if response != "y":
            print("Cancelled.")
            return False

    # Delete from each location
    results = []
    for agent_id, display_name, scope, path in locations:
        try:
            remove_path(path)
            results.append((agent_id, display_name, scope, path, True, "Deleted"))
        except Exception as e:
            results.append((agent_id, display_name, scope, path, False, str(e)))

    # Print results
    print(f"\n=== DELETE RESULTS ===\n")
    success_count = 0
    for agent_id, display_name, scope, path, success, message in results:
        status = "OK" if success else "FAILED"
        print(f"[{status}] {display_name} ({agent_id})")
        print(f"      {message}: {path}")
        if success:
            success_count += 1
        print()

    print(f"Deleted from {success_count}/{len(results)} location(s).")
    return success_count == len(results)


def main():
    parser = argparse.ArgumentParser(description="Delete a skill from AI coding agents")
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
    parser.add_argument(
        "--agent", "-a",
        action="append",
        dest="agents",
        help="Target agent(s) to delete from (can be repeated)"
    )
    parser.add_argument(
        "--all-agents",
        action="store_true",
        help="Delete from all detected agents where the skill exists"
    )
    args = parser.parse_args()

    # Validate flag combinations
    if args.agents and args.all_agents:
        parser.error("Cannot use both --agent and --all-agents")

    if (args.agents or args.all_agents) and args.scope:
        parser.error("Cannot use --scope with --agent or --all-agents")

    # Validate agent IDs
    if args.agents:
        for agent in args.agents:
            if not validate_agent(agent):
                print(f"Error: Unknown agent '{agent}'")
                print(f"Valid agents: {', '.join(sorted(AGENTS.keys()))}")
                return 1

    # Route to appropriate handler
    if args.agents or args.all_agents:
        success = delete_skill_agents(args.name, args.agents, args.all_agents, args.force)
    else:
        success = delete_skill_default(args.name, args.scope, args.force)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
