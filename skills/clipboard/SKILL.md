---
name: clipboard
description: Copy text to clipboard with optional rich formatting. Triggers on "copy to clipboard", "copy that", "pbcopy", "copy formatted", "copy rich text".
---

# Clipboard

Copy the most recent relevant text block from the conversation to the macOS system clipboard.

## Plain Text Copy (Default)

Use a heredoc to safely handle special characters (quotes, apostrophes, backticks, dollar signs):

```bash
cat <<'CLIPBOARD' | pbcopy
<text to copy>
CLIPBOARD
```

## Rich Text Copy (Formatted)

Use when the user wants formatting preserved for pasting into Slack, Word, Google Docs, Notion, etc. Sets both HTML and plain text on the clipboard via Swift, so the receiving app picks the richest format it supports.

**Step 1:** Write the HTML content to a temp file:

```bash
cat <<'CLIPBOARD_HTML' > /tmp/_clipboard_rich.html
<html><body>
<h2>Title</h2>
<p>Paragraph with <b>bold</b> and <i>italic</i>.</p>
<ul><li>Item one</li><li>Item two</li></ul>
</body></html>
CLIPBOARD_HTML
```

**Step 2:** Write the plain text fallback to a temp file:

```bash
cat <<'CLIPBOARD_TEXT' > /tmp/_clipboard_rich.txt
Title

Paragraph with bold and italic.

- Item one
- Item two
CLIPBOARD_TEXT
```

**Step 3:** Set clipboard with both HTML and plain text using Swift:

```bash
swift -e '
import AppKit

let html = try Data(contentsOf: URL(fileURLWithPath: "/tmp/_clipboard_rich.html"))
let text = try String(contentsOfFile: "/tmp/_clipboard_rich.txt", encoding: .utf8)

let pb = NSPasteboard.general
pb.clearContents()
pb.setData(html, forType: .html)
pb.setString(text, forType: .string)
'
```

**Step 4:** Clean up temp files:

```bash
rm -f /tmp/_clipboard_rich.html /tmp/_clipboard_rich.txt
```

## When to Use Rich vs Plain

- **Rich (HTML)**: User says "copy formatted", "copy as rich text", "copy for Slack/LinkedIn/Word/Docs/Notion", or the content has meaningful formatting (bold, headers, lists, code blocks). **This is also the correct way to copy for Slack and LinkedIn** — they accept HTML rich text from clipboard and render it with proper formatting (bold, lists, code, etc.). Do NOT use Slack mrkdwn or markdown syntax for clipboard copy — use HTML rich text instead, it works universally.
  - **⚠️ Slack does NOT render HTML `<table>` tags.** Tables pasted into Slack appear as a broken mess of text. Instead of `<table>`, present tabular data as plain-text lines (e.g. `Label: value` per line, or use `<pre>` for aligned columns). This also applies to LinkedIn and most chat apps.
- **Plain**: Default for code snippets, terminal output, simple text, or when user says "copy to clipboard" without formatting context

## Rules

1. Identify the most recent text block the user wants copied (message, code block, drafted text, etc.)
2. If ambiguous, ask what to copy
3. Use single-quoted heredoc delimiters (`'CLIPBOARD'`, `'CLIPBOARD_HTML'`, `'CLIPBOARD_TEXT'`) to prevent shell expansion
4. For rich copy, convert markdown-style content to proper HTML (use `<b>`, `<i>`, `<code>`, `<ul>/<li>`, `<h1>`-`<h6>`, `<pre>`, etc.). **Do NOT use `<table>` for Slack/chat targets** — use line-per-row text instead.
5. Always provide a plain text fallback alongside HTML
6. Confirm success after copying, noting whether plain or rich format was used
