#!/usr/bin/env python3
"""Union per-pass findings XML files into a single <code-review-report>.

Usage:
    dedup-findings.py <out.xml> <pass-1.xml> <pass-2.xml> ...

Each input file is expected to contain <finding>...</finding> elements
emitted by the broad/specialist/probe prompts (CDATA-wrapped fields). The
script:

  1. Extracts all <finding> elements via regex (we deliberately avoid an
     XML parser — agent output is frequently malformed CDATA-wise).
  2. Tags each with source-agent + source-role attrs derived from the
     input filename pattern `<stage>__<agent>__<role>.xml` (or, if not
     matching the pattern, the raw basename minus ".xml").
  3. Re-numbers them with a global `index="N"` attribute so the judge
     prompt can refer to them stably.
  4. Sorts by (severity desc, confidence desc, file, line-start) so the
     judge sees the high-impact cluster first.
  5. Wraps in a <code-review-report total="N"> element.

Note: this is *not* an actual deduplicator — semantic dedup is the judge's
job. We only union, tag, and renumber. Lexically-identical findings are
left intact so the judge can mark them DUPLICATE.
"""
from __future__ import annotations

import pathlib
import re
import sys

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

FINDING_RE = re.compile(r"<finding\b[^>]*>.*?</finding>", re.DOTALL)
ATTR_RE = re.compile(r'(\w+(?:-\w+)*)="([^"]*)"')


def extract_findings(xml_text: str) -> list[str]:
    return FINDING_RE.findall(xml_text)


def parse_attrs(open_tag: str) -> dict:
    return dict(ATTR_RE.findall(open_tag))


def attach_source_attrs(finding: str, agent: str, role: str) -> str:
    """Inject source-agent and source-role attrs into the <finding ...> open tag."""
    head_end = finding.find(">")
    head = finding[:head_end]
    rest = finding[head_end:]
    if "source-agent=" not in head:
        head += f' source-agent="{agent}"'
    if "source-role=" not in head:
        head += f' source-role="{role}"'
    return head + rest


def reindex(finding: str, idx: int) -> str:
    """Replace or insert index="N" into the <finding ...> open tag."""
    head_end = finding.find(">")
    head = finding[:head_end]
    rest = finding[head_end:]
    if re.search(r'\bindex="[^"]*"', head):
        head = re.sub(r'\bindex="[^"]*"', f'index="{idx}"', head)
    else:
        head = head.replace("<finding", f'<finding index="{idx}"', 1)
    return head + rest


def parse_filename(path: pathlib.Path) -> tuple[str, str]:
    """Decode `<stage>__<agent>__<role>.xml` → (agent, role). Fall back gracefully."""
    stem = path.stem
    parts = stem.split("__")
    if len(parts) >= 3:
        return parts[1], parts[2]
    if len(parts) == 2:
        return parts[0], parts[1]
    return stem, ""


def sort_key(finding: str) -> tuple:
    attrs = parse_attrs(finding[: finding.find(">")])
    sev = SEVERITY_ORDER.get(attrs.get("severity", "low"), 4)
    conf = -float(attrs.get("confidence", "0") or "0")
    fname = attrs.get("file", "")
    line = int(attrs.get("line-start", "0") or "0")
    return (sev, conf, fname, line)


def main() -> int:
    if len(sys.argv) < 3:
        sys.stderr.write(f"usage: {sys.argv[0]} <out.xml> <input.xml> [more inputs ...]\n")
        return 2

    out_path = pathlib.Path(sys.argv[1])
    inputs = [pathlib.Path(p) for p in sys.argv[2:]]

    all_findings: list[str] = []
    for p in inputs:
        if not p.is_file() or p.stat().st_size == 0:
            sys.stderr.write(f"[dedup] skip empty/missing {p}\n")
            continue
        agent, role = parse_filename(p)
        text = p.read_text(errors="replace")
        for f in extract_findings(text):
            all_findings.append(attach_source_attrs(f, agent, role))

    all_findings.sort(key=sort_key)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as fh:
        fh.write(f'<code-review-report total="{len(all_findings)}">\n')
        for i, f in enumerate(all_findings, start=1):
            fh.write(reindex(f, i))
            fh.write("\n")
        fh.write("</code-review-report>\n")

    sys.stderr.write(
        f"[dedup] {len(inputs)} input(s) → {len(all_findings)} finding(s) → {out_path}\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
