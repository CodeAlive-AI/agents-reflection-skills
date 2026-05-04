# fetch-url-as-markdown

Fetch any web URL and get clean, readable Markdown — main content only, no navigation, ads, or footer. Runs locally on [trafilatura](https://github.com/adbar/trafilatura) with a real-browser User-Agent and structured exit codes that tell the host agent when to fall back to a remote crawler (Exa MCP).

## Install

```bash
npx skills add CodeAlive-AI/ai-driven-development@fetch-url-as-markdown -g -y
```

## Prerequisites

- Python 3.10+
- [`trafilatura`](https://pypi.org/project/trafilatura/) ≥ 2.0:

  ```bash
  python3 -m pip install --break-system-packages trafilatura
  ```

  (The script exits with code `3` and prints this hint if the import fails.)

- *Optional* — an Exa MCP server in your agent host (e.g. `mcp__exa__web_search_advanced_exa`). Used only as a fallback when local extraction can't recover the page.

## Quick start

After installing, ask your agent things like:

```
> Read https://github.com/adbar/trafilatura and summarize the README
> Fetch https://docs.python.org/3/library/json.html and quote the section on encoders
> Pull this blog post as Markdown so I can paste it into my notes
```

The agent will run the bundled script directly:

```bash
python3 ~/.claude/skills/fetch-url-as-markdown/scripts/fetch_url.py "https://example.com"
python3 ~/.claude/skills/fetch-url-as-markdown/scripts/fetch_url.py "https://example.com" --no-metadata --min-body 0
```

## What it does

One entry point — a single CLI script with one job: *URL → clean Markdown to stdout.*

| Stage | Behaviour |
|---|---|
| **Download** | `trafilatura.fetch_response()` with a real Chrome User-Agent and 30 s timeout (config in `scripts/settings.cfg`) |
| **Content-Type guard** | Anything outside `text/html \| application/xhtml+xml \| text/plain \| application/xml \| text/xml` is rejected up-front (exit `4`) so PDFs/images/archives don't get mis-parsed as HTML |
| **Anti-stub guard** | Sniffs the raw HTML for Cloudflare / "Please enable JavaScript" / Imperva / DataDome wall markers and bails with exit `2` instead of returning a useless 30-character "Just a moment…" page |
| **Extract** | `trafilatura.extract(output_format="markdown", include_formatting=True, include_links=True, include_tables=True, favor_recall=True, deduplicate=True, with_metadata=True)` — keeps headings/lists/code where the source HTML uses real `<h1..h6>`, with a YAML frontmatter (title, author, date, url, hostname) on top |
| **Min-body guard** | Bodies under 50 chars (configurable via `--min-body N`, `0` to disable) are treated as stubs → exit `2` |

### Exit codes (the contract for the host agent)

| Code | Meaning | Recommended action |
|---:|---|---|
| `0` | Markdown printed to stdout | done |
| `1` | `DownloadError` — network/HTTP/timeout/anti-bot block at fetch | fall back to Exa MCP |
| `2` | `ExtractionError` — empty extract, JS/Cloudflare wall, or stub body | fall back to Exa MCP |
| `3` | trafilatura not installed | install (see Prerequisites), then retry |
| `4` | `UnsupportedContentTypeError` — URL is binary | **don't** fall back to Exa; route to a content-specific skill (e.g. `pdf` for PDFs) |

`SKILL.md` instructs the agent on this fallback flow, so for the common case the user just says "fetch this URL" and gets Markdown — local first, Exa second, no manual orchestration.

## Key features

- **Local-first, free, no API key needed for the happy path** — extraction runs entirely on `trafilatura` ≥ 2.0
- **Real browser User-Agent baked into `settings.cfg`** — fixes the silent failure where `github.com` and other anti-bot sites return empty bodies for trafilatura's default UA
- **Structured exit codes 0/1/2/3/4** — the script tells the host agent *why* it failed, so the fallback decision is mechanical, not interpretive
- **Content-Type and anti-stub guards** — prevent the classic "trafilatura returned 30 chars from a Cloudflare interstitial, so we silently passed garbage downstream" failure mode
- **Defaults tuned for LLM-friendly output** — `include_formatting=True`, `favor_recall=True`, `deduplicate=True`, YAML metadata header on by default
- **Drop-in replacement for the built-in `WebFetch`** — the description in `SKILL.md` instructs the agent to prefer this skill whenever the user asks to "read / fetch / scrape / summarize / quote a URL"

## Sources and methodology

- **trafilatura** by Adrien Barbaresi — [GitHub](https://github.com/adbar/trafilatura), [docs](https://trafilatura.readthedocs.io). Configuration patterns (`use_config`, `settings.cfg`, `USER_AGENTS`) follow the official [Settings](https://trafilatura.readthedocs.io/en/latest/settings.html) and [Downloads](https://trafilatura.readthedocs.io/en/latest/downloads.html) docs.
- **Extract flag selection** — informed by Barbaresi 2021 ([ACL anthology](https://aclanthology.org/2021.acl-demo.15/)) and the [Bevendorff et al. 2023 extraction benchmark](https://webis.de/downloads/publications/papers/bevendorff_2023b.pdf), which rank trafilatura first among open-source extractors on ROUGE-LSum.
- **Real-world reference implementation** — [`vakovalskii/searcharvester`](https://github.com/vakovalskii/searcharvester) (`simple_tavily_adapter/main.py`) uses `trafilatura.extract(output_format="markdown", include_formatting=True, include_links=True, include_tables=True, favor_recall=True)` for its `/extract` and `/search` endpoints — the same flag set we ship as default.
- **Anti-stub markers** — collected from Cloudflare interstitial copy ("Just a moment…", "Verifying you are human"), Imperva (`Incapsula Incident ID`), DataDome (`captcha-delivery.com`) and standard `<noscript>` patterns. Matched on a case-insensitive snippet of the first 8 KB of the response body.

## File structure

```
skills/fetch-url-as-markdown/
├── SKILL.md                     # agent-facing contract (workflow, exit-code routing)
├── README.md                    # this file
└── scripts/
    ├── fetch_url.py             # CLI entry point
    └── settings.cfg             # trafilatura config: real-browser UA, 30s timeout, retries
```

## License

MIT
