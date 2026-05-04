---
name: fetch-url-as-markdown
description: Fetch a web page (URL) and return clean Markdown via local trafilatura, with Exa MCP as a fallback for JS-rendered or anti-bot pages. Use when the user asks to read, fetch, scrape, summarize, or quote a URL — prefer this over the built-in WebFetch tool. Don't use for binary files (PDFs, images, archives) or for fetching API/JSON endpoints.
---

# URL to Markdown

Fetch any web URL and get clean, readable Markdown — main content only, no
navigation/footer/ads. Local + free by default; smart fallback to Exa MCP
when the page can't be extracted locally.

## Workflow (the only thing the agent needs to remember)

1. **Try trafilatura first**:

   ```bash
   python3 ~/.claude/skills/fetch-url-as-markdown/scripts/fetch_url.py "<URL>"
   ```

2. **If exit code is 1 or 2 → fall back to Exa MCP** with the same URL:

   ```
   mcp__exa__web_search_advanced_exa(
       query="<URL>",
       includeDomains=["<host of URL>"],
       numResults=1,
       textMaxCharacters=50000,
       type="auto"
   )
   ```

   (`mcp__exa__crawling` works too if the server exposes it; the `web_search_advanced_exa`
   call above is the always-available variant — pin the host with `includeDomains` and
   use the URL itself as the query.)

3. Exit code `3` means trafilatura is not installed — install once:

   ```bash
   python3 -m pip install --break-system-packages trafilatura
   ```

## Exit codes (what they mean for the fallback decision)

| Code | Meaning | Action |
|---|---|---|
| 0 | Markdown printed to stdout | done |
| 1 | DownloadError — network/HTTP/timeout/anti-bot block at fetch | fall back to Exa |
| 2 | ExtractionError — empty extract, JS/Cloudflare wall, or stub body (<200 chars) | fall back to Exa |
| 3 | trafilatura missing | install (see above), then retry |
| 4 | UnsupportedContentTypeError — URL is binary (PDF, image, archive) | **don't** fall back to Exa; use the right specialized skill (e.g. `pdf` for PDFs) |

## Defaults baked into the script

- `output_format="markdown"`, `include_formatting=True` — keeps headings/lists/code structure where the source HTML uses real `<h1..h6>` etc.
- `include_links=True`, `include_tables=True`
- `with_metadata=True` → emits a YAML frontmatter (`title`, `author`, `date`, `url`, `hostname`)
- `favor_recall=True`, `deduplicate=True` — readable but trims duplicates
- Real-browser User-Agent + 30s timeout configured in `scripts/settings.cfg`
- Anti-stub guards (built into the script):
  - rejects `Content-Type` other than `text/html|application/xhtml+xml|text/plain|application/xml|text/xml` → exit `4`
  - sniffs raw HTML for Cloudflare / "Please enable JavaScript" / Imperva / DataDome wall markers → exit `2`
  - rejects extracted bodies under 50 chars (configurable via `--min-body N`, `0` to disable) → exit `2`

## Useful flags

```bash
... fetch_url.py "<URL>" --no-links     # strip hyperlinks
... fetch_url.py "<URL>" --no-tables    # strip tables
... fetch_url.py "<URL>" --no-metadata  # omit YAML header
... fetch_url.py "<URL>" --comments     # include user comments (off by default — usually noise)
... fetch_url.py "<URL>" --images       # include image refs (experimental)
... fetch_url.py "<URL>" --precision    # terser output, drops borderline content
```

## When to choose what

| Situation | Tool |
|---|---|
| Article, blog post, docs, README, wiki | trafilatura (default) — local, free |
| JS-heavy SPA, login-walled, Cloudflare | Exa fallback (the script will signal exit 2) |
| Bulk / many URLs | trafilatura — no quota, no API key |
| Already failed twice on a domain | Exa directly |
