#!/usr/bin/env python3
"""Detect installed AI coding agents on the system."""

import argparse
import json
import sys
from pathlib import Path

# Import from local agents module
from agents import AGENTS, detect_installed_agents, get_agent_config


def format_output(agents: list[dict], output_format: str, show_all: bool) -> str:
    """Format agent list for output.

    Args:
        agents: List of agent info dicts
        output_format: "text", "json", or "table"
        show_all: Whether showing all agents or just detected

    Returns:
        Formatted string
    """
    if output_format == "json":
        return json.dumps(agents, indent=2)

    if not agents:
        if show_all:
            return "No agents configured."
        return "No AI coding agents detected."

    if output_format == "table":
        lines = ["NAME | DISPLAY NAME | INSTALLED | GLOBAL DIR", "-" * 80]
        for a in agents:
            installed = "Yes" if a.get("installed", True) else "No"
            lines.append(f"{a['name']} | {a['display_name']} | {installed} | {a['global_dir']}")
        return "\n".join(lines)

    # Default text format
    if show_all:
        lines = ["=== ALL SUPPORTED AGENTS ===", ""]
        for a in agents:
            installed = " [INSTALLED]" if a.get("installed") else ""
            lines.append(f"  {a['display_name']} ({a['name']}){installed}")
            lines.append(f"    Project: {a['project_dir']}")
            lines.append(f"    Global:  {a['global_dir']}")
            lines.append("")
    else:
        lines = ["=== DETECTED AI CODING AGENTS ===", ""]
        for a in agents:
            lines.append(f"  {a['display_name']} ({a['name']})")
            lines.append(f"    Global skills: {a['global_dir']}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Detect installed AI coding agents"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Show all supported agents, not just detected ones"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "table"],
        default="text",
        help="Output format (default: text)"
    )
    args = parser.parse_args()

    if args.all:
        # Show all supported agents with installation status
        detected = set(detect_installed_agents())
        agents = []
        for agent_id, config in AGENTS.items():
            agents.append({
                "name": config["name"],
                "display_name": config["display_name"],
                "project_dir": config["project_dir"],
                "global_dir": config["global_dir"],
                "installed": agent_id in detected,
            })
    else:
        # Show only detected agents
        detected_ids = detect_installed_agents()
        agents = []
        for agent_id in detected_ids:
            config = get_agent_config(agent_id)
            if config:
                agents.append({
                    "name": config["name"],
                    "display_name": config["display_name"],
                    "project_dir": config["project_dir"],
                    "global_dir": config["global_dir"],
                })

    print(format_output(agents, args.format, args.all))
    return 0 if agents else 1


if __name__ == "__main__":
    sys.exit(main())
