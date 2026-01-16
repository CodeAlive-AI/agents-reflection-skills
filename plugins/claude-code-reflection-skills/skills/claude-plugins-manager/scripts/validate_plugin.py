#!/usr/bin/env python3
"""
Validate a Claude Code plugin structure and manifest.

Usage:
    python validate_plugin.py <plugin-path>
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple


class ValidationResult:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def add_error(self, msg: str):
        self.errors.append(msg)

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def add_info(self, msg: str):
        self.info.append(msg)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def print_report(self):
        if self.info:
            print("\n📋 Info:")
            for msg in self.info:
                print(f"   {msg}")

        if self.warnings:
            print("\n⚠️  Warnings:")
            for msg in self.warnings:
                print(f"   {msg}")

        if self.errors:
            print("\n❌ Errors:")
            for msg in self.errors:
                print(f"   {msg}")

        if self.is_valid:
            print("\n✅ Plugin is valid!")
        else:
            print(f"\n❌ Plugin validation failed with {len(self.errors)} error(s)")


def validate_plugin_name(name: str) -> Tuple[bool, str]:
    """Validate plugin name format (kebab-case)."""
    if not name:
        return False, "Plugin name is empty"
    if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$|^[a-z]$', name):
        return False, f"Plugin name '{name}' should be kebab-case (e.g., 'my-plugin')"
    if '--' in name:
        return False, f"Plugin name '{name}' should not have consecutive dashes"
    return True, ""


def validate_version(version: str) -> Tuple[bool, str]:
    """Validate semantic version format."""
    if not re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$', version):
        return False, f"Version '{version}' should follow semver (e.g., '1.0.0')"
    return True, ""


def validate_plugin_json(plugin_dir: Path, result: ValidationResult) -> dict | None:
    """Validate plugin.json exists and has required fields."""
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"

    if not plugin_json_path.exists():
        result.add_error(f"Missing .claude-plugin/plugin.json")
        return None

    try:
        with open(plugin_json_path) as f:
            plugin_data = json.load(f)
    except json.JSONDecodeError as e:
        result.add_error(f"Invalid JSON in plugin.json: {e}")
        return None

    # Required fields
    required_fields = ["name", "description", "version", "author"]
    for field in required_fields:
        if field not in plugin_data:
            result.add_error(f"Missing required field '{field}' in plugin.json")

    # Validate name
    if "name" in plugin_data:
        valid, msg = validate_plugin_name(plugin_data["name"])
        if not valid:
            result.add_error(msg)

    # Validate version
    if "version" in plugin_data:
        valid, msg = validate_version(plugin_data["version"])
        if not valid:
            result.add_error(msg)

    # Validate author
    if "author" in plugin_data:
        if not isinstance(plugin_data["author"], dict):
            result.add_error("'author' should be an object with 'name' field")
        elif "name" not in plugin_data["author"]:
            result.add_error("'author' object must have 'name' field")

    # Validate description
    if "description" in plugin_data:
        desc = plugin_data["description"]
        if len(desc) < 10:
            result.add_warning("Description is very short, consider adding more detail")
        if "TODO" in desc:
            result.add_warning("Description contains TODO placeholder")

    # Optional fields validation
    if "keywords" in plugin_data:
        if not isinstance(plugin_data["keywords"], list):
            result.add_error("'keywords' should be an array")

    result.add_info(f"Plugin: {plugin_data.get('name', 'unknown')} v{plugin_data.get('version', 'unknown')}")

    return plugin_data


def validate_commands(plugin_dir: Path, result: ValidationResult):
    """Validate commands directory and files."""
    commands_dir = plugin_dir / "commands"
    if not commands_dir.exists():
        return

    md_files = list(commands_dir.glob("*.md"))
    if not md_files:
        result.add_warning("commands/ directory exists but contains no .md files")
        return

    result.add_info(f"Found {len(md_files)} command(s)")

    for md_file in md_files:
        content = md_file.read_text()

        # Check for frontmatter
        if not content.startswith("---"):
            result.add_warning(f"Command '{md_file.name}' missing YAML frontmatter")
            continue

        # Check for description in frontmatter
        if "description:" not in content.split("---")[1] if len(content.split("---")) > 1 else "":
            result.add_warning(f"Command '{md_file.name}' missing description in frontmatter")


def validate_agents(plugin_dir: Path, result: ValidationResult):
    """Validate agents directory and files."""
    agents_dir = plugin_dir / "agents"
    if not agents_dir.exists():
        return

    md_files = list(agents_dir.glob("*.md"))
    if not md_files:
        result.add_warning("agents/ directory exists but contains no .md files")
        return

    result.add_info(f"Found {len(md_files)} agent(s)")

    for md_file in md_files:
        content = md_file.read_text()
        if not content.startswith("---"):
            result.add_warning(f"Agent '{md_file.name}' missing YAML frontmatter")


def validate_skills(plugin_dir: Path, result: ValidationResult):
    """Validate skills directory structure."""
    skills_dir = plugin_dir / "skills"
    if not skills_dir.exists():
        return

    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
    if not skill_dirs:
        result.add_warning("skills/ directory exists but contains no skill subdirectories")
        return

    result.add_info(f"Found {len(skill_dirs)} skill(s)")

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            result.add_error(f"Skill '{skill_dir.name}' missing SKILL.md")


def validate_hooks(plugin_dir: Path, result: ValidationResult):
    """Validate hooks configuration."""
    hooks_dir = plugin_dir / "hooks"
    if not hooks_dir.exists():
        return

    hooks_json = hooks_dir / "hooks.json"
    if not hooks_json.exists():
        result.add_warning("hooks/ directory exists but missing hooks.json")
        return

    try:
        with open(hooks_json) as f:
            hooks_data = json.load(f)
        result.add_info("Found hooks configuration")

        valid_events = ["PrePrompt", "PostToolUse"]
        for event in hooks_data.keys():
            if event not in valid_events:
                result.add_warning(f"Unknown hook event: {event}")

    except json.JSONDecodeError as e:
        result.add_error(f"Invalid JSON in hooks.json: {e}")


def validate_mcp(plugin_dir: Path, result: ValidationResult):
    """Validate MCP server configuration."""
    mcp_json = plugin_dir / ".mcp.json"
    if not mcp_json.exists():
        return

    try:
        with open(mcp_json) as f:
            mcp_data = json.load(f)

        if "mcpServers" not in mcp_data:
            result.add_error(".mcp.json missing 'mcpServers' key")
            return

        servers = mcp_data["mcpServers"]
        result.add_info(f"Found {len(servers)} MCP server(s)")

        for name, config in servers.items():
            if "command" not in config:
                result.add_error(f"MCP server '{name}' missing 'command' field")

    except json.JSONDecodeError as e:
        result.add_error(f"Invalid JSON in .mcp.json: {e}")


def validate_readme(plugin_dir: Path, result: ValidationResult):
    """Validate README.md exists and has content."""
    readme = plugin_dir / "README.md"
    if not readme.exists():
        result.add_error("Missing README.md")
        return

    content = readme.read_text()
    if len(content) < 100:
        result.add_warning("README.md is very short, consider adding more documentation")
    if "TODO" in content:
        result.add_warning("README.md contains TODO placeholders")


def validate_license(plugin_dir: Path, result: ValidationResult):
    """Check for LICENSE file."""
    license_file = plugin_dir / "LICENSE"
    if not license_file.exists():
        result.add_warning("Missing LICENSE file (recommended for distribution)")


def validate_plugin(plugin_path: str) -> ValidationResult:
    """Run all validation checks on a plugin."""
    result = ValidationResult()
    plugin_dir = Path(plugin_path).resolve()

    if not plugin_dir.exists():
        result.add_error(f"Plugin directory does not exist: {plugin_dir}")
        return result

    if not plugin_dir.is_dir():
        result.add_error(f"Path is not a directory: {plugin_dir}")
        return result

    # Run all validators
    validate_plugin_json(plugin_dir, result)
    validate_commands(plugin_dir, result)
    validate_agents(plugin_dir, result)
    validate_skills(plugin_dir, result)
    validate_hooks(plugin_dir, result)
    validate_mcp(plugin_dir, result)
    validate_readme(plugin_dir, result)
    validate_license(plugin_dir, result)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Claude Code plugin"
    )
    parser.add_argument(
        "plugin_path",
        help="Path to the plugin directory"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only show errors"
    )

    args = parser.parse_args()

    print(f"🔍 Validating plugin at: {args.plugin_path}")

    result = validate_plugin(args.plugin_path)

    if not args.quiet or not result.is_valid:
        result.print_report()

    sys.exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
