#!/usr/bin/env python3
"""
Parse <finding> blocks from per-agent code-review responses, validate the
`quoted-code` claim against the real source file, and render a final report
(XML or markdown).

Usage:
    code_review_validate.py \\
        --input-kind (file|diff) \\
        --input-path <source path>  # the file that was reviewed (optional for diff)
        --output-format (xml|markdown) \\
        <response_dir>

<response_dir> contains one `<agent_id>.<role>.out` file per agent run
(the raw stdout captured by code-review.sh). Stderr files are ignored here.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


FINDING_RE = re.compile(
    r"<finding\b([^>]*)>(.*?)</finding>",
    re.DOTALL | re.IGNORECASE,
)
ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
INNER_BLOCK_RE = re.compile(
    r"<(title|rationale|suggested-fix|quoted-code)\b[^>]*>(.*?)</\1>",
    re.DOTALL | re.IGNORECASE,
)
CDATA_RE = re.compile(r"<!\[CDATA\[(.*?)\]\]>", re.DOTALL)


@dataclass
class Finding:
    source_agent: str
    source_role: str
    attrs: dict[str, str]
    title: str = ""
    rationale: str = ""
    suggested_fix: str = ""
    quoted_code: str = ""
    quoted_code_valid: bool | None = None  # None = not validated (e.g. diff input)


def strip_cdata(text: str) -> str:
    m = CDATA_RE.search(text)
    return (m.group(1) if m else text).strip()


def parse_response(agent_id: str, role: str, content: str) -> list[Finding]:
    out: list[Finding] = []
    for m in FINDING_RE.finditer(content):
        attrs = dict(ATTR_RE.findall(m.group(1)))
        body = m.group(2)
        inner = {k.lower(): strip_cdata(v) for k, v in INNER_BLOCK_RE.findall(body)}
        out.append(
            Finding(
                source_agent=agent_id,
                source_role=role,
                attrs=attrs,
                title=inner.get("title", ""),
                rationale=inner.get("rationale", ""),
                suggested_fix=inner.get("suggested-fix", ""),
                quoted_code=inner.get("quoted-code", ""),
            )
        )
    return out


def read_source_lines(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def normalize(s: str) -> str:
    # Normalize whitespace for a forgiving comparison.
    return re.sub(r"\s+", " ", s).strip()


def validate_quote(finding: Finding, lines: list[str]) -> bool | None:
    """
    True  = quoted_code matches source at the given line range
    False = range or content diverges (finding likely hallucinated)
    None  = validation not applicable (missing attrs, no source)
    """
    if not lines:
        return None
    try:
        start = int(finding.attrs.get("line-start", ""))
        end = int(finding.attrs.get("line-end", finding.attrs.get("line-start", "")))
    except ValueError:
        return False
    if start < 1 or end < start or end > len(lines):
        return False
    if not finding.quoted_code:
        return None
    actual = "\n".join(lines[start - 1 : end])
    return normalize(finding.quoted_code) == normalize(actual) or \
        normalize(finding.quoted_code) in normalize(actual) or \
        normalize(actual) in normalize(finding.quoted_code)


def load_responses(response_dir: Path) -> Iterable[tuple[str, str, str]]:
    for path in sorted(response_dir.glob("*.out")):
        name = path.stem  # "<agent>.<role>"
        if "." not in name:
            continue
        agent_id, role = name.split(".", 1)
        yield agent_id, role, path.read_text(encoding="utf-8", errors="replace")


def xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def cdata(s: str) -> str:
    return "<![CDATA[" + s.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def render_xml(
    input_kind: str,
    input_path: str,
    findings: list[Finding],
) -> str:
    lines: list[str] = []
    lines.append(
        f'<code-review-report input-kind="{xml_escape(input_kind)}" '
        f'input-source="{xml_escape(input_path)}" finding-count="{len(findings)}">'
    )
    for i, f in enumerate(findings, 1):
        valid_attr = ""
        if f.quoted_code_valid is not None:
            valid_attr = f' quote-valid="{str(f.quoted_code_valid).lower()}"'
        attr_parts: list[str] = [f'index="{i}"']
        for key in ("severity", "category", "file", "line-start", "line-end", "confidence"):
            v = f.attrs.get(key, "")
            if v:
                attr_parts.append(f'{key}="{xml_escape(v)}"')
        attr_parts.append(f'source-agent="{xml_escape(f.source_agent)}"')
        attr_parts.append(f'source-role="{xml_escape(f.source_role)}"')
        lines.append(f"  <finding {' '.join(attr_parts)}{valid_attr}>")
        if f.title:
            lines.append(f"    <title>{xml_escape(f.title)}</title>")
        if f.rationale:
            lines.append(f"    <rationale>{cdata(f.rationale)}</rationale>")
        if f.suggested_fix:
            lines.append(f"    <suggested-fix>{cdata(f.suggested_fix)}</suggested-fix>")
        if f.quoted_code:
            lines.append(f"    <quoted-code>{cdata(f.quoted_code)}</quoted-code>")
        lines.append("  </finding>")
    lines.append("</code-review-report>")
    return "\n".join(lines)


SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    # Legacy aliases — accepted silently so older specialist outputs still sort.
    "warning": 1,
    "nit": 3,
}


def sort_key(f: Finding):
    sev = SEVERITY_ORDER.get(f.attrs.get("severity", "").lower(), 3)
    try:
        conf = -float(f.attrs.get("confidence", "0"))
    except ValueError:
        conf = 0.0
    return (sev, conf, f.source_agent)


def render_markdown(
    input_kind: str,
    input_path: str,
    findings: list[Finding],
) -> str:
    out: list[str] = []
    out.append(f"# Code Review Report")
    out.append(f"")
    out.append(f"- Input: `{input_path}` ({input_kind})")
    out.append(f"- Findings: {len(findings)}")
    out.append(f"")
    if not findings:
        out.append("_No findings._")
        return "\n".join(out)

    sev_alias = {"warning": "high", "nit": "low"}
    grouped: dict[str, list[Finding]] = {}
    for f in findings:
        raw = f.attrs.get("severity", "unknown").lower()
        sev = sev_alias.get(raw, raw)
        grouped.setdefault(sev, []).append(f)
    for sev in ("critical", "high", "medium", "low", "unknown"):
        items = grouped.get(sev, [])
        if not items:
            continue
        out.append(f"## {sev.capitalize()} ({len(items)})")
        out.append("")
        for i, f in enumerate(items, 1):
            loc = f"{f.attrs.get('file', '?')}:{f.attrs.get('line-start', '?')}"
            end = f.attrs.get("line-end")
            if end and end != f.attrs.get("line-start"):
                loc += f"-{end}"
            conf = f.attrs.get("confidence", "?")
            cat = f.attrs.get("category", "?")
            validity = ""
            if f.quoted_code_valid is False:
                validity = " ⚠ quote-mismatch"
            elif f.quoted_code_valid is True:
                validity = " ✓ quote-verified"
            out.append(
                f"### {i}. {f.title or '(untitled)'}  \n"
                f"`{loc}` · {cat} · conf {conf} · {f.source_agent}/{f.source_role}{validity}"
            )
            if f.rationale:
                out.append("")
                out.append(textwrap.indent(f.rationale.strip(), "> "))
            if f.suggested_fix:
                out.append("")
                out.append("**Suggested fix:**")
                out.append("```")
                out.append(f.suggested_fix.strip())
                out.append("```")
            out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-kind", required=True, choices=("file", "diff", "stdin"))
    ap.add_argument("--input-path", default="(stdin)")
    ap.add_argument("--output-format", required=True, choices=("xml", "markdown"))
    ap.add_argument("response_dir")
    args = ap.parse_args()

    response_dir = Path(args.response_dir)
    if not response_dir.is_dir():
        print(f"response_dir not found: {response_dir}", file=sys.stderr)
        return 4

    # Only validate against real source when we were given a plain file on disk.
    source_lines: list[str] = []
    if args.input_kind == "file":
        src = Path(args.input_path)
        if src.is_file():
            source_lines = read_source_lines(src)

    findings: list[Finding] = []
    for agent_id, role, content in load_responses(response_dir):
        for f in parse_response(agent_id, role, content):
            if source_lines:
                f.quoted_code_valid = validate_quote(f, source_lines)
            findings.append(f)

    findings.sort(key=sort_key)

    if args.output_format == "xml":
        print(render_xml(args.input_kind, args.input_path, findings))
    else:
        print(render_markdown(args.input_kind, args.input_path, findings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
