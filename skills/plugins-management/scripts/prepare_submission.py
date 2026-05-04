#!/usr/bin/env python3
"""
Prepare a Claude Code plugin for submission to the Anthropic Plugin Directory.

This script gathers all information needed for the submission form and can
automatically fetch repository details using `gh` CLI.

Usage:
    python prepare_submission.py <plugin-path> [options]

Options:
    --email EMAIL           Primary contact email (required for submission)
    --company-url URL       Company/Organization URL (required for submission)
    --open-form             Open the submission form in browser
    --json                  Output as JSON
    --output FILE           Save submission info to file
"""

import argparse
import json
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Optional


# Anthropic Plugin Submission Form URL
SUBMISSION_FORM_URL = "https://forms.gle/YourFormID"  # Replace with actual form URL when known

# Documentation URLs
PLUGIN_DOCS_URL = "https://code.claude.com/docs/en/plugins"
MARKETPLACE_DOCS_URL = "https://code.claude.com/docs/en/plugin-marketplaces"
REFERENCE_DOCS_URL = "https://code.claude.com/docs/en/plugins-reference"


def run_command(cmd: list[str], cwd: str = None) -> tuple[bool, str]:
    """Run a shell command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30
        )
        return result.returncode == 0, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return False, str(e)


def get_git_info(plugin_path: str) -> dict:
    """Get git repository information using git and gh CLI."""
    git_info = {
        "repo_url": None,
        "full_sha": None,
        "branch": None,
        "is_clean": False,
        "has_remote": False,
        "errors": []
    }

    # Check if it's a git repository
    success, _ = run_command(["git", "rev-parse", "--git-dir"], cwd=plugin_path)
    if not success:
        git_info["errors"].append("Not a git repository")
        return git_info

    # Get full SHA
    success, sha = run_command(["git", "rev-parse", "HEAD"], cwd=plugin_path)
    if success:
        git_info["full_sha"] = sha
    else:
        git_info["errors"].append("Could not get commit SHA")

    # Get current branch
    success, branch = run_command(["git", "branch", "--show-current"], cwd=plugin_path)
    if success:
        git_info["branch"] = branch

    # Check if working directory is clean
    success, status = run_command(["git", "status", "--porcelain"], cwd=plugin_path)
    if success:
        git_info["is_clean"] = len(status) == 0

    # Try to get remote URL using gh
    success, repo_url = run_command(["gh", "repo", "view", "--json", "url", "-q", ".url"], cwd=plugin_path)
    if success and repo_url:
        git_info["repo_url"] = repo_url
        git_info["has_remote"] = True
    else:
        # Fallback to git remote
        success, remote_url = run_command(["git", "remote", "get-url", "origin"], cwd=plugin_path)
        if success and remote_url:
            # Convert SSH URL to HTTPS if needed
            if remote_url.startswith("git@github.com:"):
                remote_url = remote_url.replace("git@github.com:", "https://github.com/")
            if remote_url.endswith(".git"):
                remote_url = remote_url[:-4]
            git_info["repo_url"] = remote_url
            git_info["has_remote"] = True
        else:
            git_info["errors"].append("No remote repository found. Push to GitHub first.")

    return git_info


def gather_plugin_info(plugin_path: str, email: str = None, company_url: str = None) -> dict:
    """Gather all information needed for plugin submission."""
    plugin_dir = Path(plugin_path).resolve()
    info = {
        "plugin_path": str(plugin_dir),
        "validation": {"passed": True, "issues": [], "warnings": []},
        "metadata": {},
        "git": {},
        "components": {},
        "form_fields": {}
    }

    # Get git information
    info["git"] = get_git_info(str(plugin_dir))

    # Read plugin.json
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        info["validation"]["passed"] = False
        info["validation"]["issues"].append("Missing .claude-plugin/plugin.json")
        # Set empty form fields for display
        info["form_fields"] = {
            "link_to_plugin": info["git"].get("repo_url", ""),
            "full_sha": info["git"].get("full_sha", ""),
            "plugin_homepage": "",
            "company_url": company_url or "",
            "primary_contact_email": email or "",
            "plugin_name": "",
            "plugin_description": "",
        }
        return info

    try:
        with open(plugin_json_path) as f:
            plugin_data = json.load(f)
            info["metadata"] = plugin_data
    except json.JSONDecodeError as e:
        info["validation"]["passed"] = False
        info["validation"]["issues"].append(f"Invalid plugin.json: {e}")
        # Set empty form fields for display
        info["form_fields"] = {
            "link_to_plugin": info["git"].get("repo_url", ""),
            "full_sha": info["git"].get("full_sha", ""),
            "plugin_homepage": "",
            "company_url": company_url or "",
            "primary_contact_email": email or "",
            "plugin_name": "",
            "plugin_description": "",
        }
        return info

    # Check required fields
    required = ["name", "description", "version", "author"]
    for field in required:
        if field not in plugin_data:
            info["validation"]["passed"] = False
            info["validation"]["issues"].append(f"Missing required field: {field}")

    # Check for TODO placeholders
    description = plugin_data.get("description", "")
    if "TODO" in description:
        info["validation"]["passed"] = False
        info["validation"]["issues"].append("Description contains TODO placeholder")

    # Check description length (50-100 words recommended)
    word_count = len(description.split())
    if word_count < 50:
        info["validation"]["warnings"].append(f"Description is only {word_count} words (50-100 recommended)")
    elif word_count > 100:
        info["validation"]["warnings"].append(f"Description is {word_count} words (50-100 recommended)")

    # Gather component info
    components = info["components"]

    # Commands
    commands_dir = plugin_dir / "commands"
    if commands_dir.exists():
        commands = list(commands_dir.glob("*.md"))
        components["commands"] = [c.stem for c in commands]

    # Agents
    agents_dir = plugin_dir / "agents"
    if agents_dir.exists():
        agents = list(agents_dir.glob("*.md"))
        components["agents"] = [a.stem for a in agents]

    # Skills
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        components["skills"] = skills

    # Hooks
    hooks_json = plugin_dir / "hooks" / "hooks.json"
    if hooks_json.exists():
        components["hooks"] = True

    # MCP servers
    mcp_json = plugin_dir / ".mcp.json"
    if mcp_json.exists():
        try:
            with open(mcp_json) as f:
                mcp_data = json.load(f)
            components["mcp_servers"] = list(mcp_data.get("mcpServers", {}).keys())
        except json.JSONDecodeError:
            pass

    # Check README
    readme = plugin_dir / "README.md"
    if not readme.exists():
        info["validation"]["passed"] = False
        info["validation"]["issues"].append("Missing README.md")
    elif "TODO" in readme.read_text():
        info["validation"]["warnings"].append("README.md contains TODO placeholders")

    # Check LICENSE
    license_file = plugin_dir / "LICENSE"
    if not license_file.exists():
        info["validation"]["warnings"].append("Missing LICENSE file (recommended)")

    # Check git requirements
    if not info["git"]["has_remote"]:
        info["validation"]["passed"] = False
        info["validation"]["issues"].append("Plugin must be pushed to GitHub before submission")

    if not info["git"]["is_clean"]:
        info["validation"]["warnings"].append("Working directory has uncommitted changes")

    # Prepare form fields
    info["form_fields"] = {
        "link_to_plugin": info["git"].get("repo_url", ""),
        "full_sha": info["git"].get("full_sha", ""),
        "plugin_homepage": plugin_data.get("homepage", "") or info["git"].get("repo_url", ""),
        "company_url": company_url or "",
        "primary_contact_email": email or plugin_data.get("author", {}).get("email", ""),
        "plugin_name": plugin_data.get("name", ""),
        "plugin_description": description,
    }

    # Validate form fields
    if not info["form_fields"]["link_to_plugin"]:
        info["validation"]["issues"].append("Link to Plugin is required")
    if not info["form_fields"]["full_sha"]:
        info["validation"]["issues"].append("Full SHA is required")
    if not info["form_fields"]["plugin_homepage"]:
        info["validation"]["issues"].append("Plugin Homepage is required")
    if not info["form_fields"]["company_url"]:
        info["validation"]["warnings"].append("Company/Organization URL not provided (use --company-url)")
    if not info["form_fields"]["primary_contact_email"]:
        info["validation"]["warnings"].append("Primary Contact Email not provided (use --email)")

    return info


def print_form_fields(info: dict):
    """Print form fields in a copy-paste friendly format."""
    fields = info["form_fields"]
    validation = info["validation"]
    git = info["git"]

    print("\n" + "=" * 70)
    print("📋 ANTHROPIC PLUGIN SUBMISSION FORM DATA")
    print("=" * 70)

    # Validation status
    if validation["passed"]:
        print("\n✅ Validation: PASSED")
    else:
        print("\n❌ Validation: FAILED")
        for issue in validation["issues"]:
            print(f"   ❌ {issue}")

    if validation["warnings"]:
        print("\n⚠️  Warnings:")
        for warning in validation["warnings"]:
            print(f"   ⚠️  {warning}")

    # Git info
    print(f"\n📂 Repository Info:")
    print(f"   Branch: {git.get('branch', 'N/A')}")
    print(f"   Clean: {'Yes' if git.get('is_clean') else 'No (has uncommitted changes)'}")

    # Form fields
    print("\n" + "-" * 70)
    print("📝 FORM FIELDS (copy these to the submission form)")
    print("-" * 70)

    print(f"\n1. Link to Plugin *")
    print(f"   {fields['link_to_plugin'] or '[REQUIRED - push to GitHub first]'}")

    print(f"\n2. Full SHA of version you want added *")
    print(f"   {fields['full_sha'] or '[REQUIRED - commit first]'}")

    print(f"\n3. Plugin Homepage *")
    print(f"   {fields['plugin_homepage'] or '[REQUIRED]'}")

    print(f"\n4. Company/Organization URL *")
    print(f"   {fields['company_url'] or '[REQUIRED - use --company-url]'}")

    print(f"\n5. Primary Contact Email *")
    print(f"   {fields['primary_contact_email'] or '[REQUIRED - use --email]'}")

    print(f"\n6. Plugin Name *")
    print(f"   {fields['plugin_name']}")

    print(f"\n7. Plugin Description * (50-100 words)")
    print(f"   {fields['plugin_description']}")

    # Components summary
    components = info["components"]
    if components:
        print("\n" + "-" * 70)
        print("🧩 Plugin Components (for reference)")
        print("-" * 70)
        if components.get("commands"):
            print(f"   Commands: {', '.join(components['commands'])}")
        if components.get("agents"):
            print(f"   Agents: {', '.join(components['agents'])}")
        if components.get("skills"):
            print(f"   Skills: {', '.join(components['skills'])}")
        if components.get("hooks"):
            print(f"   Hooks: Configured")
        if components.get("mcp_servers"):
            print(f"   MCP Servers: {', '.join(components['mcp_servers'])}")

    print("\n" + "=" * 70)


def copy_to_clipboard(text: str) -> bool:
    """Try to copy text to clipboard."""
    try:
        # macOS
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return process.returncode == 0
    except FileNotFoundError:
        try:
            # Linux with xclip
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return process.returncode == 0
        except FileNotFoundError:
            return False


def generate_submission_json(info: dict) -> str:
    """Generate JSON with all submission data."""
    return json.dumps({
        "form_fields": info["form_fields"],
        "validation": info["validation"],
        "git": info["git"],
        "components": info["components"],
        "metadata": info["metadata"]
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Prepare a Claude Code plugin for submission to Anthropic's Plugin Directory"
    )
    parser.add_argument(
        "plugin_path",
        help="Path to the plugin directory"
    )
    parser.add_argument(
        "--email", "-e",
        help="Primary contact email (required for submission)"
    )
    parser.add_argument(
        "--company-url", "-c",
        help="Company/Organization URL (required for submission)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Save submission data to file (JSON format)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--open-form",
        action="store_true",
        help="Open the submission form in browser"
    )
    parser.add_argument(
        "--copy-sha",
        action="store_true",
        help="Copy the full SHA to clipboard"
    )

    args = parser.parse_args()

    print(f"🔍 Analyzing plugin at: {args.plugin_path}")

    info = gather_plugin_info(
        args.plugin_path,
        email=args.email,
        company_url=args.company_url
    )

    if args.json:
        print(generate_submission_json(info))
    else:
        print_form_fields(info)

        if args.output:
            with open(args.output, "w") as f:
                f.write(generate_submission_json(info))
            print(f"\n📄 Submission data saved to: {args.output}")

        if args.copy_sha and info["git"].get("full_sha"):
            if copy_to_clipboard(info["git"]["full_sha"]):
                print(f"\n📋 Full SHA copied to clipboard!")
            else:
                print(f"\n⚠️  Could not copy to clipboard")

    if args.open_form:
        import webbrowser
        # The actual Google Form URL would go here
        form_url = "https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform"
        print(f"\n🌐 Opening submission form...")
        print(f"   Note: Copy the form fields above and paste into the form")
        webbrowser.open(form_url)

    # Exit with error if validation failed
    if not info["validation"]["passed"]:
        print("\n⚠️  Please fix validation errors before submitting.")
        sys.exit(1)

    print("\n✨ Ready for submission! Copy the form fields above to the submission form.")


if __name__ == "__main__":
    main()
