#!/usr/bin/env python3
"""Small dependency-free validator for this Agent Skill package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence


def parse_frontmatter(text: str) -> Dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'.")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter closing delimiter not found.")
    raw = text[4:end].strip().splitlines()
    out: Dict[str, str] = {}
    current = None
    for line in raw:
        if not line.strip() or line.startswith(" "):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            current = k.strip()
            out[current] = v.strip().strip('"')
    return out


def validate(root: Path) -> List[str]:
    errors: List[str] = []
    skill = root / "SKILL.md"
    if not skill.exists():
        return ["Missing SKILL.md"]
    text = skill.read_text(encoding="utf-8")
    try:
        fm = parse_frontmatter(text)
    except ValueError as ex:
        return [str(ex)]
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not name:
        errors.append("Missing required frontmatter field: name")
    if not desc:
        errors.append("Missing required frontmatter field: description")
    if name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("Invalid name: use lowercase letters, numbers, single hyphens; no leading/trailing/consecutive hyphens")
    if name and root.name != name:
        errors.append(f"Directory name '{root.name}' should match skill name '{name}'")
    if len(name) > 64:
        errors.append("name exceeds 64 characters")
    if len(desc) > 1024:
        errors.append("description exceeds 1024 characters")
    body_lines = text[text.find("\n---", 4) + 4 :].splitlines()
    if len(body_lines) > 500:
        errors.append(f"SKILL.md body has {len(body_lines)} lines; recommended under 500")
    for required in ["scripts/history_context.py", "references/ANOMALIES.md", "references/GH_CLI.md", "references/DECISION_ATOMS.md", "references/OUTPUT_SCHEMA.md"]:
        if not (root / required).exists():
            errors.append(f"Missing referenced file: {required}")
    return errors


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate basic Agent Skill package structure and SKILL.md frontmatter.")
    parser.add_argument("root", nargs="?", default=".", help="Skill directory root")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    errors = validate(root)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 1
    print(f"OK: {root.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
