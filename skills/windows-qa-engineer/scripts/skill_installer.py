#!/usr/bin/env python3
"""
skill_installer.py — General-purpose installer for Claude Code skills.

Reads install.yaml from a skill directory and executes the declared steps:
platform check, python check, git clone, venv, pip install, MCP config, verify.

Usage:
    python skill_installer.py [--skill-dir PATH] [--project-dir PATH]

Options:
    --skill-dir   Path to the skill root (default: parent of this script)
    --project-dir Path to the project root for .mcp.json (default: cwd)
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def load_manifest(skill_dir: Path) -> dict[str, Any]:
    """Load and parse install.yaml from the skill directory."""
    manifest_path = skill_dir / "install.yaml"
    if not manifest_path.exists():
        fail(f"install.yaml not found at {manifest_path}")

    try:
        import yaml
    except ImportError:
        # Fall back to a minimal YAML parser for simple manifests
        return _parse_simple_yaml(manifest_path)

    with open(manifest_path) as f:
        return yaml.safe_load(f)


def _parse_simple_yaml(path: Path) -> dict[str, Any]:
    """Minimal YAML parser for install.yaml without PyYAML dependency.

    Handles the subset of YAML used by install.yaml: scalars, lists,
    nested mappings (one level of indent), block scalars (|).
    """
    import re

    result: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list | None = None
    current_map: dict | None = None
    current_map_key: str | None = None
    block_scalar_key: str | None = None
    block_scalar_lines: list[str] = []
    block_scalar_indent: int = 0
    list_of_maps: bool = False
    list_maps: list[dict] = []
    current_list_map: dict | None = None
    # Track nesting: top-level key that owns a map value
    map_owner: str | None = None

    lines = path.read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip comments and blank lines (unless in block scalar)
        if block_scalar_key:
            indent = len(line) - len(line.lstrip())
            if stripped == "" or indent >= block_scalar_indent:
                block_scalar_lines.append(line[block_scalar_indent:] if indent >= block_scalar_indent else "")
                i += 1
                continue
            else:
                # Block scalar ended
                text = "\n".join(block_scalar_lines).rstrip("\n") + "\n"
                if map_owner and current_map is not None:
                    current_map[block_scalar_key] = text
                else:
                    result[block_scalar_key] = text
                block_scalar_key = None
                block_scalar_lines = []
                # Fall through to process current line

        if stripped == "" or stripped.startswith("#"):
            i += 1
            continue

        indent = len(line) - len(line.lstrip())

        # List item inside a list-of-maps (e.g., repos entries)
        if list_of_maps and indent >= 2 and stripped.startswith("- "):
            # Save previous map
            if current_list_map is not None:
                list_maps.append(current_list_map)
            current_list_map = {}
            # Parse key: value from "- key: value"
            item = stripped[2:].strip()
            if ":" in item:
                k, v = item.split(":", 1)
                current_list_map[k.strip()] = _yaml_val(v.strip())
            i += 1
            continue

        if list_of_maps and current_list_map is not None and indent >= 4 and ":" in stripped:
            k, v = stripped.split(":", 1)
            v = v.strip()
            if v == "|":
                block_scalar_key = k.strip()
                block_scalar_indent = indent + 2
                block_scalar_lines = []
                map_owner = None  # block scalar target is current_list_map handled separately
                # Actually for list maps we need special handling
                # For simplicity, read ahead
                i += 1
                while i < len(lines):
                    bl = lines[i]
                    bi = len(bl) - len(bl.lstrip())
                    if bl.strip() == "" or bi >= block_scalar_indent:
                        block_scalar_lines.append(bl[block_scalar_indent:] if bi >= block_scalar_indent else "")
                        i += 1
                    else:
                        break
                current_list_map[k.strip()] = "\n".join(block_scalar_lines).rstrip("\n") + "\n"
                block_scalar_key = None
                block_scalar_lines = []
                continue
            else:
                current_list_map[k.strip()] = _yaml_val(v)
            i += 1
            continue

        # End list-of-maps context on dedent
        if list_of_maps and indent == 0:
            if current_list_map is not None:
                list_maps.append(current_list_map)
                current_list_map = None
            result[current_key] = list_maps
            list_of_maps = False
            list_maps = []
            current_key = None
            # Fall through

        # End current map context on dedent
        if map_owner and indent == 0:
            result[map_owner] = current_map
            current_map = None
            map_owner = None
            current_key = None

        # End simple list on dedent
        if current_list is not None and indent == 0 and not stripped.startswith("-"):
            result[current_key] = current_list
            current_list = None
            current_key = None

        # Simple list item (e.g., "  - fastmcp")
        if current_list is not None and stripped.startswith("- "):
            current_list.append(_yaml_val(stripped[2:].strip()))
            i += 1
            continue

        # Map sub-key (indent >= 2, inside a map owner)
        if map_owner and current_map is not None and indent >= 2 and ":" in stripped:
            k, v = stripped.split(":", 1)
            v = v.strip()
            if v == "|":
                block_scalar_key = k.strip()
                block_scalar_indent = indent + 2
                block_scalar_lines = []
                i += 1
                continue
            current_map[k.strip()] = _yaml_val(v)
            i += 1
            continue

        # Top-level key
        if indent == 0 and ":" in stripped and not stripped.startswith("-"):
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip()

            if v == "" or v.startswith("#"):
                # Next lines define a nested structure — peek ahead
                current_key = k
                j = i + 1
                while j < len(lines) and (lines[j].strip() == "" or lines[j].strip().startswith("#")):
                    j += 1
                if j < len(lines):
                    next_stripped = lines[j].strip()
                    if next_stripped.startswith("- url:") or next_stripped.startswith("- url :"):
                        list_of_maps = True
                        list_maps = []
                        current_list_map = None
                    elif next_stripped.startswith("- "):
                        current_list = []
                    else:
                        # Nested map
                        map_owner = k
                        current_map = {}
            elif v == "|":
                block_scalar_key = k
                block_scalar_indent = 2
                block_scalar_lines = []
            else:
                result[k] = _yaml_val(v)
            i += 1
            continue

        i += 1

    # Flush any remaining context
    if block_scalar_key:
        text = "\n".join(block_scalar_lines).rstrip("\n") + "\n"
        result[block_scalar_key] = text
    if list_of_maps:
        if current_list_map is not None:
            list_maps.append(current_list_map)
        result[current_key] = list_maps
    if current_list is not None:
        result[current_key] = current_list
    if map_owner and current_map is not None:
        result[map_owner] = current_map

    return result


def _yaml_val(s: str) -> Any:
    """Convert a YAML scalar string to a Python value."""
    # Strip inline comments
    if "  #" in s:
        s = s[: s.index("  #")].strip()
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if s in ("null", "None", "~"):
        return None
    # Strip quotes
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------

def check_platform(manifest: dict) -> dict:
    """Check that current platform matches the manifest requirement."""
    required = manifest.get("platform", "any")
    if required == "any":
        return {"step": "platform", "status": "ok", "detail": platform.platform()}

    current = sys.platform  # win32, darwin, linux
    mapping = {"windows": "win32", "macos": "darwin", "linux": "linux"}
    expected = mapping.get(required, required)

    if current == expected:
        return {"step": "platform", "status": "ok", "detail": platform.platform()}

    return {
        "step": "platform",
        "status": "failed",
        "detail": f"Requires {required} but running on {platform.platform()}",
    }


def check_python(manifest: dict) -> dict:
    """Check that current Python meets version constraint."""
    constraint = manifest.get("python")
    if not constraint:
        return {"step": "python", "status": "ok", "detail": platform.python_version()}

    import re
    match = re.match(r"([><=!]+)([\d.]+)", constraint)
    if not match:
        return {"step": "python", "status": "ok", "detail": f"Unparsed constraint: {constraint}"}

    op, ver_str = match.groups()
    required = tuple(int(x) for x in ver_str.split("."))
    current = sys.version_info[:len(required)]

    ops = {
        ">=": current >= required,
        ">": current > required,
        "<=": current <= required,
        "<": current < required,
        "==": current == required,
        "!=": current != required,
    }

    if ops.get(op, True):
        return {"step": "python", "status": "ok", "detail": platform.python_version()}

    return {
        "step": "python",
        "status": "failed",
        "detail": f"Requires Python {constraint} but running {platform.python_version()}",
    }


def process_repos(manifest: dict) -> tuple[list[dict], Path | None]:
    """Clone repos, create venvs, install requirements. Returns (steps, venv_python)."""
    repos = manifest.get("repos", [])
    steps = []
    venv_python: Path | None = None

    for repo in repos:
        url = repo["url"]
        target = Path(os.path.expanduser(repo["target"]))

        # Clone
        if target.exists():
            steps.append({"step": "clone", "status": "skipped", "detail": f"{target} already exists"})
        else:
            run(["git", "clone", url, str(target)])
            steps.append({"step": "clone", "status": "ok", "detail": str(target)})

        # Venv
        if repo.get("venv"):
            venv_dir = target / ".venv"
            if venv_dir.exists():
                steps.append({"step": "venv", "status": "skipped", "detail": f"{venv_dir} already exists"})
            else:
                run([sys.executable, "-m", "venv", str(venv_dir)])
                steps.append({"step": "venv", "status": "ok", "detail": str(venv_dir)})

            # Resolve venv python
            if sys.platform == "win32":
                venv_python = venv_dir / "Scripts" / "python.exe"
            else:
                venv_python = venv_dir / "bin" / "python"

        # Requirements
        if repo.get("requirements"):
            req_file = target / repo["requirements"]
            pip_exe = venv_python or Path(sys.executable)
            run([str(pip_exe), "-m", "pip", "install", "-r", str(req_file)])
            steps.append({"step": "deps", "status": "ok", "detail": str(req_file)})

    return steps, venv_python


def install_pip_packages(manifest: dict, venv_python: Path | None) -> dict | None:
    """Install additional pip packages."""
    packages = manifest.get("pip", [])
    if not packages:
        return None

    pip_exe = venv_python or Path(sys.executable)
    run([str(pip_exe), "-m", "pip", "install"] + packages)
    return {"step": "pip", "status": "ok", "detail": ", ".join(packages)}


def configure_mcp(
    manifest: dict,
    skill_dir: Path,
    project_dir: Path,
    venv_python: Path | None,
) -> dict | None:
    """Register the MCP server in .mcp.json."""
    mcp_conf = manifest.get("mcp")
    if not mcp_conf:
        return None

    mcp_json_path = project_dir / ".mcp.json"

    # Read existing
    existing: dict[str, Any] = {}
    if mcp_json_path.exists():
        with open(mcp_json_path) as f:
            existing = json.load(f)

    servers = existing.setdefault("mcpServers", {})

    # Build command — use venv python if available
    python_cmd = str(venv_python) if venv_python else "python"
    script_path = str(skill_dir / mcp_conf["script"])

    # Build env
    env: dict[str, str] = {}

    # PYTHONPATH from repos with pythonpath: true
    pythonpaths = []
    for repo in manifest.get("repos", []):
        if repo.get("pythonpath"):
            pythonpaths.append(str(Path(os.path.expanduser(repo["target"]))))
    if pythonpaths:
        env["PYTHONPATH"] = os.pathsep.join(pythonpaths)

    # Merge env from manifest
    if mcp_conf.get("env"):
        env.update(mcp_conf["env"])

    # Build server entry
    entry: dict[str, Any] = {
        "type": "stdio",
        "command": python_cmd,
        "args": [script_path],
    }
    if env:
        entry["env"] = env

    servers[mcp_conf["name"]] = entry

    # Write atomically
    tmp_fd, tmp_path = tempfile.mkstemp(dir=project_dir, suffix=".mcp.json.tmp")
    try:
        with os.fdopen(tmp_fd, "w") as f:
            json.dump(existing, f, indent=2)
            f.write("\n")
        os.replace(tmp_path, mcp_json_path)
    except Exception:
        os.unlink(tmp_path)
        raise

    return {"step": "mcp", "status": "ok", "detail": f"{mcp_json_path} updated"}


def run_verify(manifest: dict, venv_python: Path | None) -> dict | None:
    """Run the verify script."""
    verify = manifest.get("verify")
    if not verify or not verify.get("script"):
        return None

    python_cmd = str(venv_python) if venv_python else sys.executable

    # Build PYTHONPATH
    pythonpaths = []
    for repo in manifest.get("repos", []):
        if repo.get("pythonpath"):
            pythonpaths.append(str(Path(os.path.expanduser(repo["target"]))))

    env = os.environ.copy()
    if pythonpaths:
        existing_pp = env.get("PYTHONPATH", "")
        new_pp = os.pathsep.join(pythonpaths)
        env["PYTHONPATH"] = f"{new_pp}{os.pathsep}{existing_pp}" if existing_pp else new_pp

    result = subprocess.run(
        [python_cmd, "-c", verify["script"]],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode == 0:
        detail = result.stdout.strip() or "passed"
        return {"step": "verify", "status": "ok", "detail": detail}
    else:
        detail = result.stderr.strip() or result.stdout.strip() or "verification failed"
        return {"step": "verify", "status": "failed", "detail": detail}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd: list[str]) -> subprocess.CompletedProcess:
    """Run a subprocess, raising on failure."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        detail = stderr or stdout or f"Command failed with exit code {result.returncode}"
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{detail}")
    return result


def fail(message: str) -> None:
    """Print error JSON and exit."""
    report = {"success": False, "error": message, "steps": []}
    print(json.dumps(report, indent=2))
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Install skill dependencies from install.yaml")
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Path to the skill root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project root for .mcp.json placement (default: cwd)",
    )
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    project_dir = args.project_dir.resolve()

    manifest = load_manifest(skill_dir)
    steps: list[dict] = []
    success = True

    # 1. Platform check
    step = check_platform(manifest)
    steps.append(step)
    if step["status"] == "failed":
        success = False
        report = {"success": False, "steps": steps, "mcp_configured": False, "restart_required": False}
        print(json.dumps(report, indent=2))
        sys.exit(1)

    # 2. Python check
    step = check_python(manifest)
    steps.append(step)
    if step["status"] == "failed":
        success = False
        report = {"success": False, "steps": steps, "mcp_configured": False, "restart_required": False}
        print(json.dumps(report, indent=2))
        sys.exit(1)

    # 3. Repos (clone, venv, requirements)
    try:
        repo_steps, venv_python = process_repos(manifest)
        steps.extend(repo_steps)
    except RuntimeError as e:
        steps.append({"step": "repos", "status": "failed", "detail": str(e)})
        success = False
        report = {"success": False, "steps": steps, "mcp_configured": False, "restart_required": False}
        print(json.dumps(report, indent=2))
        sys.exit(1)

    # 4. Additional pip packages
    try:
        pip_step = install_pip_packages(manifest, venv_python)
        if pip_step:
            steps.append(pip_step)
    except RuntimeError as e:
        steps.append({"step": "pip", "status": "failed", "detail": str(e)})
        success = False
        report = {"success": False, "steps": steps, "mcp_configured": False, "restart_required": False}
        print(json.dumps(report, indent=2))
        sys.exit(1)

    # 5. MCP config
    mcp_configured = False
    try:
        mcp_step = configure_mcp(manifest, skill_dir, project_dir, venv_python)
        if mcp_step:
            steps.append(mcp_step)
            mcp_configured = True
    except Exception as e:
        steps.append({"step": "mcp", "status": "failed", "detail": str(e)})
        success = False

    # 6. Verify
    if success:
        verify_step = run_verify(manifest, venv_python)
        if verify_step:
            steps.append(verify_step)
            if verify_step["status"] == "failed":
                success = False

    # 7. Report
    report = {
        "success": success,
        "steps": steps,
        "mcp_configured": mcp_configured,
        "restart_required": mcp_configured and success,
    }
    print(json.dumps(report, indent=2))

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
