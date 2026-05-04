#!/usr/bin/env python3
"""
Initialize a new Claude Code plugin with proper structure.

Usage:
    python init_plugin.py <plugin-name> [--path <output-directory>] [--with-commands] [--with-agents] [--with-skills] [--with-hooks] [--with-mcp]
"""

import argparse
import json
import os
import sys
from pathlib import Path


def create_plugin_json(plugin_name: str, author_name: str = "Your Name") -> dict:
    """Create the plugin.json manifest."""
    return {
        "name": plugin_name,
        "description": f"TODO: Add description for {plugin_name}",
        "version": "1.0.0",
        "author": {
            "name": author_name
        },
        "keywords": []
    }


def create_readme(plugin_name: str) -> str:
    """Create README.md content."""
    return f"""# {plugin_name.replace('-', ' ').title()}

## Description

TODO: Describe what this plugin does.

## Installation

### Add the Marketplace

```bash
/plugin marketplace add <marketplace-source>
```

### Install the Plugin

```bash
/plugin install {plugin_name}@<marketplace>
```

## Usage

TODO: Describe how to use the plugin.

## Features

- Feature 1
- Feature 2

## License

MIT License
"""


def create_command_template(command_name: str) -> str:
    """Create a command markdown file."""
    return f"""---
description: TODO: Describe what /{command_name} does
---

# {command_name.replace('-', ' ').title()} Command

TODO: Add instructions for Claude when this command is invoked.
"""


def create_agent_template(agent_name: str) -> str:
    """Create an agent markdown file."""
    return f"""---
description: TODO: Describe this agent's specialty
---

# {agent_name.replace('-', ' ').title()} Agent

TODO: Add detailed instructions and expertise for this agent.

## Capabilities

- Capability 1
- Capability 2

## When to Use

Use this agent when...
"""


def create_skill_template(skill_name: str) -> str:
    """Create a SKILL.md file."""
    return f"""---
name: {skill_name}
description: TODO: What this skill does. Use when ...
---

# {skill_name.replace('-', ' ').title()}

## Capability

TODO: Describe what this skill enables.

## Usage

TODO: How to use this skill.
"""


def create_hooks_json() -> dict:
    """Create hooks.json template."""
    return {
        "hooks": {
            "PostToolUse": [
                {
                    "matcher": "Write|Edit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
                            "description": "TODO: Replace with actual hook"
                        }
                    ]
                }
            ]
        }
    }


def create_mcp_json() -> dict:
    """Create .mcp.json template."""
    return {
        "mcpServers": {
            "example-server": {
                "command": "node",
                "args": ["./servers/server.js"],
                "env": {}
            }
        }
    }


def init_plugin(
    plugin_name: str,
    output_path: str,
    with_commands: bool = True,
    with_agents: bool = False,
    with_skills: bool = False,
    with_hooks: bool = False,
    with_mcp: bool = False,
    author_name: str = "Your Name"
) -> Path:
    """Initialize a new plugin directory structure."""

    # Validate plugin name
    if not plugin_name or not plugin_name.replace('-', '').replace('_', '').isalnum():
        raise ValueError(f"Invalid plugin name: {plugin_name}. Use kebab-case with alphanumeric characters.")

    # Create plugin directory
    plugin_dir = Path(output_path) / plugin_name
    if plugin_dir.exists():
        raise FileExistsError(f"Directory already exists: {plugin_dir}")

    plugin_dir.mkdir(parents=True)

    # Create .claude-plugin directory and plugin.json
    claude_plugin_dir = plugin_dir / ".claude-plugin"
    claude_plugin_dir.mkdir()

    plugin_json = create_plugin_json(plugin_name, author_name)
    with open(claude_plugin_dir / "plugin.json", "w") as f:
        json.dump(plugin_json, f, indent=2)

    # Create README.md
    with open(plugin_dir / "README.md", "w") as f:
        f.write(create_readme(plugin_name))

    # Create LICENSE
    with open(plugin_dir / "LICENSE", "w") as f:
        f.write("MIT License\n\nCopyright (c) 2024\n\nTODO: Add full license text")

    # Create optional components
    if with_commands:
        commands_dir = plugin_dir / "commands"
        commands_dir.mkdir()
        with open(commands_dir / "example.md", "w") as f:
            f.write(create_command_template("example"))

    if with_agents:
        agents_dir = plugin_dir / "agents"
        agents_dir.mkdir()
        with open(agents_dir / "example-agent.md", "w") as f:
            f.write(create_agent_template("example-agent"))

    if with_skills:
        skills_dir = plugin_dir / "skills" / "example-skill"
        skills_dir.mkdir(parents=True)
        with open(skills_dir / "SKILL.md", "w") as f:
            f.write(create_skill_template("example-skill"))

    if with_hooks:
        hooks_dir = plugin_dir / "hooks"
        hooks_dir.mkdir()
        with open(hooks_dir / "hooks.json", "w") as f:
            json.dump(create_hooks_json(), f, indent=2)

    if with_mcp:
        with open(plugin_dir / ".mcp.json", "w") as f:
            json.dump(create_mcp_json(), f, indent=2)
        servers_dir = plugin_dir / "servers"
        servers_dir.mkdir()
        with open(servers_dir / ".gitkeep", "w") as f:
            f.write("")

    return plugin_dir


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Code plugin"
    )
    parser.add_argument("plugin_name", help="Name of the plugin (kebab-case)")
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--author", "-a",
        default="Your Name",
        help="Author name for plugin.json"
    )
    parser.add_argument(
        "--with-commands",
        action="store_true",
        default=True,
        help="Include commands directory (default: True)"
    )
    parser.add_argument(
        "--no-commands",
        action="store_true",
        help="Exclude commands directory"
    )
    parser.add_argument(
        "--with-agents",
        action="store_true",
        help="Include agents directory"
    )
    parser.add_argument(
        "--with-skills",
        action="store_true",
        help="Include skills directory"
    )
    parser.add_argument(
        "--with-hooks",
        action="store_true",
        help="Include hooks directory"
    )
    parser.add_argument(
        "--with-mcp",
        action="store_true",
        help="Include MCP server configuration"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include all optional components"
    )

    args = parser.parse_args()

    with_commands = not args.no_commands
    with_agents = args.with_agents or args.all
    with_skills = args.with_skills or args.all
    with_hooks = args.with_hooks or args.all
    with_mcp = args.with_mcp or args.all

    try:
        plugin_dir = init_plugin(
            plugin_name=args.plugin_name,
            output_path=args.path,
            with_commands=with_commands,
            with_agents=with_agents,
            with_skills=with_skills,
            with_hooks=with_hooks,
            with_mcp=with_mcp,
            author_name=args.author
        )

        print(f"✅ Plugin '{args.plugin_name}' initialized at: {plugin_dir}")
        print("\nCreated structure:")
        for root, dirs, files in os.walk(plugin_dir):
            level = root.replace(str(plugin_dir), '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = '  ' * (level + 1)
            for file in files:
                print(f"{subindent}{file}")

        print("\nNext steps:")
        print("1. Edit .claude-plugin/plugin.json with your plugin details")
        print("2. Update README.md with documentation")
        print("3. Add your commands, agents, skills, hooks, or MCP servers")
        print("4. Run validation: claude plugin validate .")

    except (ValueError, FileExistsError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
