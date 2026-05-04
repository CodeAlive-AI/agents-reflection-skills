---
name: repo-explorer
description: >
  Explore and analyze any repository (local path or remote GitHub/GitLab URL) by
  delegating to Claude Code CLI (`claude -p`) in non-interactive mode with read-only
  access. Use when the user asks to explore, analyze, investigate, or research a
  repository or codebase. Triggers on "explore repo", "analyze repo", "investigate repo",
  "research codebase", "what does this repo do", "how does this codebase work",
  "ask about repo", "codebase question", "explore repository",
  "what API does this project have", "analyze this GitHub repo",
  "explore https://github.com/...", or any request to understand a repository's
  structure, API, architecture, or implementation details. Works with both local paths
  and remote URLs (GitHub, GitLab, Bitbucket).
---

# Repo Explorer

Launch a separate Claude Code CLI process (`claude -p --model haiku`) with read-only
tools to explore a repository and answer questions about it. Supports both local
repositories and remote URLs.

## Workflow

### 1. Determine repo source and question

From the user's message extract:

- **source**: one of:
  - **local path** (`~/projects/foo`, `/opt/services/bar`, `.` or omitted = cwd)
  - **remote URL** (`https://github.com/owner/repo`, `git@github.com:owner/repo.git`)
  - **shorthand** (`owner/repo` — treat as `https://github.com/owner/repo`)
- **question**: what to find out about the repository.

### 2. For remote repos — clone to temp directory

If the source is a remote URL or shorthand, clone it first:

```bash
REPO_DIR=$(mktemp -d) && git clone --depth 1 <url> "$REPO_DIR" && echo "$REPO_DIR"
```

- Use `--depth 1` for speed (shallow clone, only latest commit)
- If the user asks about a specific branch/tag: `git clone --depth 1 --branch <ref> <url> "$REPO_DIR"`
- Store `$REPO_DIR` to clean up later

### 3. Run the CLI command

Use the Bash tool with **timeout: 600000** (10 min) since exploration of large repos
can take several minutes.

```
cd <repo_path> && CLAUDECODE= claude -p "<question>" \
  --model haiku \
  --output-format text \
  --max-turns 15 \
  --allowedTools "Read" "Grep" "Glob" "Bash(find *)" "Bash(ls *)" "Bash(wc *)" "Bash(git log *)" "Bash(git show *)" "Bash(git diff *)" "Bash(git branch *)" "Bash(head *)" "Bash(tail *)" \
  --append-system-prompt "You are a code exploration expert. Thoroughly explore the repository to answer the user's question. Strategy: 1) Glob to discover project structure. 2) Grep to find patterns, definitions, routes, classes. 3) Read to examine key files. Always cite file paths and line numbers. Give a structured answer based on code facts."
```

**IMPORTANT:** The `CLAUDECODE=` prefix (setting the env var to empty) is required to allow
launching Claude Code as a subprocess. Without it, the nested session will be blocked.

Rules:
- **Always** include `CLAUDECODE=` directly before `claude -p` (no `&&`, it's an inline env override)
- Escape double quotes in the question with `\"`
- Wrap repo paths containing spaces in quotes
- For very large repos, increase `--max-turns` to 25
- If user explicitly requests sonnet or opus, replace `--model haiku`

### 4. Clean up (remote repos only)

After presenting the result, remove the temp directory:

```bash
rm -rf "$REPO_DIR"
```

### 5. Present the result

Display the CLI output to the user. If empty or error, report the issue and suggest
retrying with a more specific question.

## Examples

**Local repo:**
```
cd ~/projects/my-api && CLAUDECODE= claude -p "What REST endpoints are defined? List each with HTTP method, path, and handler." --model haiku --output-format text --max-turns 15 --allowedTools "Read" "Grep" "Glob" "Bash(find *)" "Bash(ls *)" "Bash(wc *)" "Bash(git log *)" "Bash(git show *)" "Bash(git diff *)" "Bash(git branch *)" "Bash(head *)" "Bash(tail *)" --append-system-prompt "You are a code exploration expert. Thoroughly explore the repository to answer the user's question. Strategy: 1) Glob to discover project structure. 2) Grep to find patterns, definitions, routes, classes. 3) Read to examine key files. Always cite file paths and line numbers. Give a structured answer based on code facts."
```

**Remote repo (GitHub URL):**
```bash
REPO_DIR=$(mktemp -d) && git clone --depth 1 https://github.com/expressjs/express "$REPO_DIR"
```
Then:
```
cd "$REPO_DIR" && CLAUDECODE= claude -p "How is routing implemented? Describe the Router class and middleware chain." --model haiku --output-format text --max-turns 15 --allowedTools "Read" "Grep" "Glob" "Bash(find *)" "Bash(ls *)" "Bash(wc *)" "Bash(git log *)" "Bash(git show *)" "Bash(git diff *)" "Bash(git branch *)" "Bash(head *)" "Bash(tail *)" --append-system-prompt "You are a code exploration expert. Thoroughly explore the repository to answer the user's question. Strategy: 1) Glob to discover project structure. 2) Grep to find patterns, definitions, routes, classes. 3) Read to examine key files. Always cite file paths and line numbers. Give a structured answer based on code facts."
```
Then: `rm -rf "$REPO_DIR"`

**Shorthand (owner/repo):** treat `vercel/next.js` as `https://github.com/vercel/next.js`.

**Current directory (no path):** run `claude -p` without `cd`.
