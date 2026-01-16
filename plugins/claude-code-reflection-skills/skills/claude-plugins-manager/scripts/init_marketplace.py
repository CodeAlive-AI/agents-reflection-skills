#!/usr/bin/env python3
"""
Initialize a new Claude Code plugin marketplace.

Usage:
    python init_marketplace.py <marketplace-name> [--path <output-directory>] [--with-plugin <plugin-name>]
"""

import argparse
import json
import os
import sys
from pathlib import Path


def create_marketplace_json(name: str, owner_name: str = "Your Name") -> dict:
    """Create the marketplace.json manifest."""
    return {
        "name": name,
        "owner": {
            "name": owner_name
        },
        "metadata": {
            "description": f"TODO: Add description for {name} marketplace",
            "version": "1.0.0"
        },
        "plugins": []
    }


def create_marketplace_readme(name: str) -> str:
    """Create README.md content for marketplace."""
    return f"""# {name.replace('-', ' ').title()} Marketplace

A Claude Code plugin marketplace.

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add <github-username>/{name}
```

Or with a full URL:

```bash
/plugin marketplace add https://github.com/<username>/{name}
```

## Available Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| TODO | Add plugins | 1.0.0 |

## Adding a Plugin

To add a new plugin to this marketplace:

1. Create your plugin in the `plugins/` directory
2. Add an entry to `.claude-plugin/marketplace.json`
3. Update this README

## Contributing

Contributions welcome! Please open a pull request.

## License

MIT License
"""


def add_plugin_to_marketplace(marketplace_json: dict, plugin_name: str, plugin_path: str) -> dict:
    """Add a plugin entry to marketplace.json."""
    plugin_entry = {
        "name": plugin_name,
        "source": plugin_path,
        "description": f"TODO: Add description for {plugin_name}",
        "version": "1.0.0"
    }
    marketplace_json["plugins"].append(plugin_entry)
    return marketplace_json


def init_marketplace(
    name: str,
    output_path: str,
    owner_name: str = "Your Name",
    initial_plugins: list = None
) -> Path:
    """Initialize a new marketplace directory structure."""

    marketplace_dir = Path(output_path) / name
    if marketplace_dir.exists():
        raise FileExistsError(f"Directory already exists: {marketplace_dir}")

    marketplace_dir.mkdir(parents=True)

    # Create .claude-plugin directory
    claude_plugin_dir = marketplace_dir / ".claude-plugin"
    claude_plugin_dir.mkdir()

    # Create marketplace.json
    marketplace_json = create_marketplace_json(name, owner_name)

    # Add initial plugins if provided
    if initial_plugins:
        for plugin_name in initial_plugins:
            plugin_path = f"./plugins/{plugin_name}"
            marketplace_json = add_plugin_to_marketplace(
                marketplace_json, plugin_name, plugin_path
            )
            # Create plugin directory
            plugin_dir = marketplace_dir / "plugins" / plugin_name
            plugin_dir.mkdir(parents=True)
            # Create minimal plugin structure
            (plugin_dir / ".claude-plugin").mkdir()
            with open(plugin_dir / ".claude-plugin" / "plugin.json", "w") as f:
                json.dump({
                    "name": plugin_name,
                    "description": f"TODO: Add description for {plugin_name}",
                    "version": "1.0.0",
                    "author": {"name": owner_name}
                }, f, indent=2)
            with open(plugin_dir / "README.md", "w") as f:
                f.write(f"# {plugin_name}\n\nTODO: Add documentation\n")

    with open(claude_plugin_dir / "marketplace.json", "w") as f:
        json.dump(marketplace_json, f, indent=2)

    # Create plugins directory
    plugins_dir = marketplace_dir / "plugins"
    if not plugins_dir.exists():
        plugins_dir.mkdir()
        with open(plugins_dir / ".gitkeep", "w") as f:
            f.write("")

    # Create README.md
    with open(marketplace_dir / "README.md", "w") as f:
        f.write(create_marketplace_readme(name))

    # Create LICENSE
    with open(marketplace_dir / "LICENSE", "w") as f:
        f.write("MIT License\n\nCopyright (c) 2024\n\nTODO: Add full license text")

    return marketplace_dir


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Code plugin marketplace"
    )
    parser.add_argument(
        "marketplace_name",
        help="Name of the marketplace (kebab-case)"
    )
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--owner", "-o",
        default="Your Name",
        help="Owner name for marketplace.json"
    )
    parser.add_argument(
        "--with-plugin",
        action="append",
        dest="plugins",
        help="Create marketplace with initial plugin(s) (can be used multiple times)"
    )

    args = parser.parse_args()

    try:
        marketplace_dir = init_marketplace(
            name=args.marketplace_name,
            output_path=args.path,
            owner_name=args.owner,
            initial_plugins=args.plugins
        )

        print(f"✅ Marketplace '{args.marketplace_name}' initialized at: {marketplace_dir}")
        print("\nCreated structure:")
        for root, dirs, files in os.walk(marketplace_dir):
            level = root.replace(str(marketplace_dir), '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = '  ' * (level + 1)
            for file in files:
                print(f"{subindent}{file}")

        print("\nNext steps:")
        print("1. Edit .claude-plugin/marketplace.json with your details")
        print("2. Add plugins to the plugins/ directory")
        print("3. Update README.md with plugin list")
        print("4. Push to GitHub/GitLab for distribution")
        print("\nUsers can add your marketplace with:")
        print(f"   /plugin marketplace add <username>/{args.marketplace_name}")

    except FileExistsError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
