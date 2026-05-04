#!/usr/bin/env python3
"""Convert a URL to Markdown using trafilatura (https://github.com/adbar/trafilatura).

Default extractor for fetch-url-as-markdown skill. Runs entirely locally,
no API key required. Sends a real-browser User-Agent (configured in
settings.cfg next to this script) so anti-bot sites like github.com return
real HTML instead of a stub.

Exit codes:
  0  success — Markdown printed to stdout
  1  download failed (network, HTTP 4xx/5xx, timeout, anti-bot 403)
  2  extraction failed — page downloaded but yielded no usable main
     content (SPA shell, JS-only render, captcha/Cloudflare wall, login wall)
  4  unsupported content type (binary: PDF, image, archive, video, octet-stream)
  3  trafilatura is not installed
The skill's fallback (Exa MCP crawl) should be tried on exit 1 or 2 — not on 4.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import trafilatura
    from trafilatura.settings import use_config
except ImportError:
    sys.stderr.write(
        "trafilatura not installed. Install with:\n"
        "  python3 -m pip install --break-system-packages trafilatura\n"
    )
    sys.exit(3)

SETTINGS_PATH = Path(__file__).with_name("settings.cfg")
_CONFIG = use_config(str(SETTINGS_PATH)) if SETTINGS_PATH.exists() else use_config()

# Content types we accept. Anything outside this set triggers UnsupportedContentTypeError.
_HTML_CT_RE = re.compile(
    r"^(text/html|application/xhtml\+xml|text/plain|application/xml|text/xml)\b",
    re.IGNORECASE,
)

# Substrings that strongly indicate the page is a JS/anti-bot wall, not real content.
# Matched on a case-insensitive normalized snippet of the *raw HTML*.
_WALL_MARKERS = (
    "please enable javascript",
    "javascript is required",
    "javascript is disabled",
    "enable javascript to run",
    "you need to enable javascript",
    "checking your browser before accessing",  # Cloudflare interstitial
    "just a moment...",                          # Cloudflare interstitial
    "verifying you are human",                   # Cloudflare Turnstile
    "verify you are a human",
    "attention required! | cloudflare",
    "ddos protection by cloudflare",
    "access denied | cloudflare",
    "ray id:",                                    # cloudflare error page
    "captcha-delivery.com",                       # DataDome captcha
    "incapsula incident id",                      # Imperva
    "<title>access denied</title>",
    "<title>403 forbidden</title>",
    "<title>error 1020</title>",                  # Cloudflare access denied
)

# Below this length the extracted markdown is almost certainly a stub
# (e.g. "Loading..." or "Please enable JS"). Tuned low enough to accept
# tiny-but-valid pages like example.com (~110 body chars) while still
# catching SPA shells.
_MIN_MARKDOWN_BODY_CHARS = 50


class DownloadError(RuntimeError):
    """Network/HTTP/anti-bot failure — could not retrieve the page bytes."""


class UnsupportedContentTypeError(RuntimeError):
    """The URL points to a binary/non-HTML resource (PDF, image, archive, …)."""


class ExtractionError(RuntimeError):
    """HTML retrieved, but contains no extractable main content (or a JS/anti-bot wall)."""


def _looks_like_wall(html: str) -> str | None:
    """Return the marker that matched, or None if no wall detected."""
    snippet = html[:8000].lower()
    for marker in _WALL_MARKERS:
        if marker in snippet:
            return marker
    return None


def _markdown_body_chars(markdown: str, with_metadata: bool) -> int:
    """Count characters in the body of the Markdown, excluding the YAML frontmatter."""
    if with_metadata and markdown.startswith("---"):
        # Strip the leading YAML block: from the first '---' to the next one
        end = markdown.find("\n---", 3)
        if end != -1:
            return len(markdown[end + 4 :].strip())
    return len(markdown.strip())


def fetch_url_as_markdown(
    url: str,
    include_links: bool = True,
    include_tables: bool = True,
    include_images: bool = False,
    include_comments: bool = False,
    with_metadata: bool = True,
    favor_precision: bool = False,
    favor_recall: bool = True,
    min_body_chars: int = _MIN_MARKDOWN_BODY_CHARS,
) -> str:
    """Fetch a URL and return its main content as Markdown.

    Defaults aim at "clean readable article body": metadata header on,
    structural formatting (headings, lists) on, links on, recall favored.

    Raises:
        DownloadError: page could not be retrieved.
        UnsupportedContentTypeError: response is binary (PDF, image, …).
        ExtractionError: HTML retrieved but no usable main content
            (empty extract, JS/anti-bot wall, or below min_body_chars).
    """
    response = trafilatura.fetch_response(
        url, with_headers=True, decode=True, config=_CONFIG
    )
    if response is None or response.html is None:
        raise DownloadError(f"Failed to download: {url}")

    content_type = (response.headers or {}).get("content-type", "")
    if content_type and not _HTML_CT_RE.match(content_type):
        raise UnsupportedContentTypeError(
            f"Unsupported content-type {content_type!r} at {url} — "
            "this skill only handles HTML/XML."
        )

    html = response.html
    wall_marker = _looks_like_wall(html)
    if wall_marker is not None:
        raise ExtractionError(
            f"Anti-bot or JS wall detected at {url} (marker: {wall_marker!r})"
        )

    markdown = trafilatura.extract(
        html,
        url=url,
        output_format="markdown",
        include_formatting=True,
        include_links=include_links,
        include_tables=include_tables,
        include_images=include_images,
        include_comments=include_comments,
        with_metadata=with_metadata,
        favor_precision=favor_precision,
        favor_recall=favor_recall and not favor_precision,
        deduplicate=True,
        config=_CONFIG,
    )
    if not markdown:
        raise ExtractionError(f"No extractable main content at: {url}")

    body_chars = _markdown_body_chars(markdown, with_metadata)
    if body_chars < min_body_chars:
        raise ExtractionError(
            f"Extracted body is too short ({body_chars} chars < {min_body_chars}) "
            f"at {url} — likely a JS-only render or stub page."
        )
    return markdown


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch a URL and print clean Markdown to stdout (trafilatura).",
    )
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument(
        "--no-links", action="store_true", help="Strip hyperlinks from output"
    )
    parser.add_argument(
        "--no-tables", action="store_true", help="Strip tables from output"
    )
    parser.add_argument(
        "--images", action="store_true", help="Include images (experimental)"
    )
    parser.add_argument(
        "--comments", action="store_true", help="Include user comments"
    )
    parser.add_argument(
        "--no-metadata", action="store_true", help="Skip YAML metadata header"
    )
    parser.add_argument(
        "--precision",
        action="store_true",
        help="Favor precision over recall (terser, drops borderline content)",
    )
    parser.add_argument(
        "--min-body",
        type=int,
        default=_MIN_MARKDOWN_BODY_CHARS,
        help=f"Minimum body chars for a successful extraction (default: {_MIN_MARKDOWN_BODY_CHARS}). "
        "Set to 0 to disable the stub-page check.",
    )
    args = parser.parse_args()

    try:
        markdown = fetch_url_as_markdown(
            args.url,
            include_links=not args.no_links,
            include_tables=not args.no_tables,
            include_images=args.images,
            include_comments=args.comments,
            with_metadata=not args.no_metadata,
            favor_precision=args.precision,
            min_body_chars=args.min_body,
        )
    except DownloadError as e:
        sys.stderr.write(f"DownloadError: {e}\n")
        sys.exit(1)
    except ExtractionError as e:
        sys.stderr.write(f"ExtractionError: {e}\n")
        sys.exit(2)
    except UnsupportedContentTypeError as e:
        sys.stderr.write(f"UnsupportedContentTypeError: {e}\n")
        sys.exit(4)

    sys.stdout.write(markdown)
    if not markdown.endswith("\n"):
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
