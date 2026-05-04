#!/usr/bin/env python3
"""
Validate Claude Code hooks configuration.

Usage:
    python3 validate_hooks.py <settings-file>
    python3 validate_hooks.py ~/.claude/settings.json

Validates:
- JSON syntax
- Required fields
- Valid event names
- Matcher patterns (regex validity)
- Hook type and required type-specific fields

Exit codes:
    0: Valid configuration
    1: Invalid configuration (errors printed to stderr)
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

VALID_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "PermissionRequest",
    "UserPromptSubmit",
    "Notification",
    "Stop",
    "SubagentStop",
    "PreCompact",
    "SessionStart",
    "SessionEnd",
}

# Events that require/support matchers
MATCHER_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "PermissionRequest",
    "Notification",
    "PreCompact",
    "SessionStart",
}

VALID_HOOK_TYPES = {"command", "prompt"}

# Events that support prompt hooks
PROMPT_SUPPORTED_EVENTS = {
    "PreToolUse",
    "PermissionRequest",
    "UserPromptSubmit",
    "Stop",
    "SubagentStop",
}


def validate_regex(pattern: str) -> tuple[bool, str | None]:
    """Validate a regex pattern."""
    if pattern in ("*", ""):
        return True, None
    try:
        re.compile(pattern)
        return True, None
    except re.error as e:
        return False, str(e)


def validate_hook(hook: dict[str, Any], event: str, path: str) -> list[str]:
    """Validate a single hook configuration."""
    errors = []

    # Check type field
    if "type" not in hook:
        errors.append(f"{path}: missing required field 'type'")
        return errors

    hook_type = hook["type"]
    if hook_type not in VALID_HOOK_TYPES:
        errors.append(f"{path}: invalid type '{hook_type}', must be one of {VALID_HOOK_TYPES}")
        return errors

    # Check type-specific required fields
    if hook_type == "command":
        if "command" not in hook:
            errors.append(f"{path}: type 'command' requires 'command' field")
        elif not isinstance(hook["command"], str):
            errors.append(f"{path}: 'command' must be a string")
        elif not hook["command"].strip():
            errors.append(f"{path}: 'command' cannot be empty")

    elif hook_type == "prompt":
        if event not in PROMPT_SUPPORTED_EVENTS:
            errors.append(f"{path}: prompt hooks not supported for event '{event}'")
        if "prompt" not in hook:
            errors.append(f"{path}: type 'prompt' requires 'prompt' field")
        elif not isinstance(hook["prompt"], str):
            errors.append(f"{path}: 'prompt' must be a string")
        elif not hook["prompt"].strip():
            errors.append(f"{path}: 'prompt' cannot be empty")

    # Check timeout if present
    if "timeout" in hook:
        timeout = hook["timeout"]
        if not isinstance(timeout, (int, float)):
            errors.append(f"{path}: 'timeout' must be a number")
        elif timeout <= 0:
            errors.append(f"{path}: 'timeout' must be positive")

    # Check once if present
    if "once" in hook and not isinstance(hook["once"], bool):
        errors.append(f"{path}: 'once' must be a boolean")

    return errors


def validate_matcher_entry(entry: dict[str, Any], event: str, idx: int) -> list[str]:
    """Validate a matcher entry (contains matcher and hooks array)."""
    errors = []
    path = f"hooks.{event}[{idx}]"

    # Check matcher if event supports it
    if event in MATCHER_EVENTS:
        if "matcher" in entry:
            matcher = entry["matcher"]
            if not isinstance(matcher, str):
                errors.append(f"{path}.matcher: must be a string")
            else:
                valid, regex_err = validate_regex(matcher)
                if not valid:
                    errors.append(f"{path}.matcher: invalid regex pattern '{matcher}': {regex_err}")

    # Check hooks array
    if "hooks" not in entry:
        errors.append(f"{path}: missing required field 'hooks'")
        return errors

    hooks = entry["hooks"]
    if not isinstance(hooks, list):
        errors.append(f"{path}.hooks: must be an array")
        return errors

    if not hooks:
        errors.append(f"{path}.hooks: array cannot be empty")
        return errors

    for i, hook in enumerate(hooks):
        if not isinstance(hook, dict):
            errors.append(f"{path}.hooks[{i}]: must be an object")
            continue
        errors.extend(validate_hook(hook, event, f"{path}.hooks[{i}]"))

    return errors


def validate_hooks_config(config: dict[str, Any]) -> list[str]:
    """Validate the hooks configuration."""
    errors = []

    if "hooks" not in config:
        return []  # No hooks configured, valid

    hooks = config["hooks"]
    if not isinstance(hooks, dict):
        errors.append("hooks: must be an object")
        return errors

    for event, entries in hooks.items():
        # Check event name
        if event not in VALID_EVENTS:
            errors.append(f"hooks.{event}: invalid event name, must be one of {sorted(VALID_EVENTS)}")
            continue

        # Check entries array
        if not isinstance(entries, list):
            errors.append(f"hooks.{event}: must be an array")
            continue

        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                errors.append(f"hooks.{event}[{i}]: must be an object")
                continue
            errors.extend(validate_matcher_entry(entry, event, i))

    return errors


def validate_file(filepath: str) -> tuple[bool, list[str]]:
    """Validate a settings file containing hooks."""
    path = Path(filepath)
    errors = []

    if not path.exists():
        return False, [f"File not found: {filepath}"]

    try:
        content = path.read_text()
    except Exception as e:
        return False, [f"Could not read file: {e}"]

    # Handle empty file
    if not content.strip():
        return True, []  # Empty file is valid (no hooks)

    try:
        config = json.loads(content)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    if not isinstance(config, dict):
        return False, ["Configuration must be a JSON object"]

    errors = validate_hooks_config(config)
    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_hooks.py <settings-file>", file=sys.stderr)
        print("Example: validate_hooks.py ~/.claude/settings.json", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    valid, errors = validate_file(filepath)

    if valid:
        print(f"✓ Valid hooks configuration: {filepath}")
        sys.exit(0)
    else:
        print(f"✗ Invalid hooks configuration: {filepath}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
