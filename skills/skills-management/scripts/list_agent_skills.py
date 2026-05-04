#!/usr/bin/env python3
"""List skills for any AI coding agent."""

import argparse
import json
import re
import sys
from pathlib import Path

from agents import (
    AGENTS,
    detect_installed_agents,
    get_agent_config,
    get_skills_dir,
    validate_agent,
)


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


def list_skills_for_agent(
    agent: str,
    scope: str | None = None,
    cwd: Path | None = None
) -> list[dict]:
    """List skills for a specific agent.

    Args:
        agent: Agent ID
        scope: "project", "global", or None for both
        cwd: Working directory for project scope

    Returns:
        List of skill info dicts
    """
    skills = []
    config = get_agent_config(agent)
    if not config:
        return skills

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
                        "agent": agent,
                        "agent_display_name": config["display_name"],
                        "path": str(item),
                        "description": metadata["description"],
                    })

    return skills


def list_skills_all_agents(scope: str | None = None, cwd: Path | None = None) -> list[dict]:
    """List skills for all detected agents.

    Args:
        scope: "project", "global", or None for both
        cwd: Working directory for project scope

    Returns:
        List of skill info dicts grouped by agent
    """
    all_skills = []
    detected = detect_installed_agents()

    for agent in detected:
        skills = list_skills_for_agent(agent, scope, cwd)
        all_skills.extend(skills)

    return all_skills


def format_output(skills: list[dict], output_format: str, single_agent: bool = False) -> str:
    """Format skills list for output."""
    if output_format == "json":
        return json.dumps(skills, indent=2)

    if not skills:
        return "No skills found."

    if output_format == "table":
        # Simple table format
        if single_agent:
            lines = ["NAME | SCOPE | DESCRIPTION", "-" * 70]
        else:
            lines = ["AGENT | NAME | SCOPE | DESCRIPTION", "-" * 90]

        for s in skills:
            desc = s["description"][:35] + "..." if len(s["description"]) > 35 else s["description"]
            if single_agent:
                lines.append(f"{s['name']} | {s['scope']} | {desc}")
            else:
                lines.append(f"{s['agent']} | {s['name']} | {s['scope']} | {desc}")
        return "\n".join(lines)

    # Default text format
    lines = []
    current_agent = None
    current_scope = None

    for s in skills:
        # Group by agent first (if showing multiple agents)
        if not single_agent and s["agent"] != current_agent:
            if current_agent is not None:
                lines.append("")
            lines.append(f"=== {s['agent_display_name'].upper()} ({s['agent']}) ===")
            current_agent = s["agent"]
            current_scope = None

        # Then group by scope
        if s["scope"] != current_scope:
            skills_dir = get_skills_dir(s["agent"], s["scope"])
            lines.append(f"\n  [{s['scope'].upper()}] {skills_dir}")
            current_scope = s["scope"]

        lines.append(f"\n    {s['name']}")
        if s["description"]:
            desc = s["description"]
            lines.append(f"      {desc[:80]}")
            if len(desc) > 80:
                lines.append(f"      {desc[80:160]}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="List skills for AI coding agents"
    )
    parser.add_argument(
        "--agent", "-a",
        help="Agent ID to list skills for (e.g., claude-code, cursor)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="List skills for all detected agents"
    )
    parser.add_argument(
        "--scope", "-s",
        choices=["project", "global"],
        help="Filter by scope (default: show both)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "table"],
        default="text",
        help="Output format (default: text)"
    )
    args = parser.parse_args()

    # Validate arguments
    if not args.agent and not args.all:
        parser.error("Either --agent or --all is required")

    if args.agent and args.all:
        parser.error("Cannot use both --agent and --all")

    if args.agent and not validate_agent(args.agent):
        print(f"Error: Unknown agent '{args.agent}'")
        print(f"Valid agents: {', '.join(sorted(AGENTS.keys()))}")
        return 1

    # List skills
    if args.all:
        skills = list_skills_all_agents(args.scope)
        single_agent = False
    else:
        skills = list_skills_for_agent(args.agent, args.scope)
        single_agent = True

    print(format_output(skills, args.format, single_agent))
    return 0 if skills else 1


if __name__ == "__main__":
    sys.exit(main())
