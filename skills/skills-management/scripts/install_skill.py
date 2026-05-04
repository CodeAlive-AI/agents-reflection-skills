#!/usr/bin/env python3
"""Install a skill to one or more AI coding agents."""

import argparse
import re
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


# Files to exclude when copying skills (per add-skill pattern)
EXCLUDE_FILES = {"README.md", "metadata.json"}


def parse_skill_name(skill_path: Path) -> str | None:
    """Parse skill name from SKILL.md frontmatter.

    Args:
        skill_path: Path to skill directory

    Returns:
        Skill name from frontmatter, or directory name as fallback
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    try:
        content = skill_md.read_text()
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            for line in frontmatter.split("\n"):
                if line.startswith("name:"):
                    return line.split(":", 1)[1].strip().strip('"\'')
    except Exception:
        pass

    return skill_path.name


def sanitize_name(name: str) -> str:
    """Sanitize a skill name to prevent path traversal.

    Args:
        name: Raw skill name

    Returns:
        Sanitized name safe for use in paths
    """
    # Remove path separators and null bytes
    sanitized = re.sub(r'[/\\:\0]', '', name)
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    # Remove leading dots (prevent ..)
    sanitized = sanitized.lstrip('.')

    if not sanitized:
        sanitized = "unnamed-skill"

    # Limit length
    if len(sanitized) > 255:
        sanitized = sanitized[:255]

    return sanitized


def is_excluded(name: str) -> bool:
    """Check if a file should be excluded from copying."""
    if name in EXCLUDE_FILES:
        return True
    if name.startswith('_'):
        return True
    return False


def copy_skill_directory(src: Path, dest: Path) -> None:
    """Copy a skill directory, excluding certain files.

    Args:
        src: Source directory
        dest: Destination directory
    """
    dest.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        if is_excluded(item.name):
            continue

        dest_path = dest / item.name

        if item.is_dir():
            copy_skill_directory(item, dest_path)
        else:
            shutil.copy2(item, dest_path)


def install_skill(
    source: Path,
    agent: str,
    scope: str = "project",
    force: bool = False,
    cwd: Path | None = None
) -> tuple[bool, str]:
    """Install a skill to a specific agent.

    Args:
        source: Path to skill directory
        agent: Target agent ID
        scope: "project" or "global"
        force: Overwrite existing skill
        cwd: Working directory for project scope

    Returns:
        Tuple of (success, message)
    """
    # Validate source
    if not source.exists():
        return False, f"Source path does not exist: {source}"

    if not source.is_dir():
        return False, f"Source is not a directory: {source}"

    skill_md = source / "SKILL.md"
    if not skill_md.exists():
        return False, f"Source does not contain SKILL.md: {source}"

    # Get skill name
    skill_name = parse_skill_name(source)
    if not skill_name:
        skill_name = source.name
    skill_name = sanitize_name(skill_name)

    # Get target directory
    target_base = get_skills_dir(agent, scope, cwd)
    if not target_base:
        return False, f"Could not determine skills directory for {agent}"

    target_path = target_base / skill_name

    # Check if target exists
    if target_path.exists():
        if not force:
            return False, f"Skill '{skill_name}' already exists at {target_path}. Use --force to overwrite."
        if target_path.is_symlink():
            target_path.unlink()
        else:
            shutil.rmtree(target_path)

    # Copy skill
    try:
        copy_skill_directory(source, target_path)
        return True, f"Installed '{skill_name}' to {agent} ({scope}): {target_path}"
    except Exception as e:
        return False, f"Error installing skill: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Install a skill to one or more AI coding agents"
    )
    parser.add_argument(
        "path",
        help="Path to the skill directory to install"
    )
    parser.add_argument(
        "--agent", "-a",
        action="append",
        dest="agents",
        help="Target agent(s) to install to (can be repeated)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Install to all detected agents"
    )
    parser.add_argument(
        "--scope", "-s",
        choices=["project", "global"],
        default="project",
        help="Target scope (default: project)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite if skill exists"
    )
    args = parser.parse_args()

    # Validate arguments
    if not args.agents and not args.all:
        parser.error("Either --agent or --all is required")

    if args.agents and args.all:
        parser.error("Cannot use both --agent and --all")

    # Determine target agents
    if args.all:
        target_agents = detect_installed_agents()
        if not target_agents:
            print("Error: No AI coding agents detected on this system.")
            return 1
    else:
        target_agents = []
        for agent in args.agents:
            if not validate_agent(agent):
                print(f"Error: Unknown agent '{agent}'")
                print(f"Valid agents: {', '.join(sorted(AGENTS.keys()))}")
                return 1
            target_agents.append(agent)

    # Resolve source path
    source = Path(args.path).resolve()

    # Install to each agent
    results = []
    for agent in target_agents:
        config = get_agent_config(agent)
        success, message = install_skill(source, agent, args.scope, args.force)
        results.append((agent, config["display_name"], success, message))

    # Print results
    print(f"\n=== INSTALL RESULTS ===\n")
    success_count = 0
    for agent, display_name, success, message in results:
        status = "OK" if success else "FAILED"
        print(f"[{status}] {display_name} ({agent})")
        print(f"      {message}")
        if success:
            success_count += 1
        print()

    print(f"Installed to {success_count}/{len(results)} agents.")

    return 0 if success_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
