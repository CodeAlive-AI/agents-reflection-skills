---
name: agents-consilium
description: "Query external AI agents (Codex, Gemini, OpenCode, Claude Code headless) in parallel for independent second opinions, code review, bug investigation, and consensus on high-stakes decisions. Agents and models are configurable in config.json. Use for architecture choices, security review, or ambiguous problems where independent perspectives matter. Not for simple questions answerable from docs or the codebase — use web search or repo exploration instead."
---

# Consilium: Multi-Agent Orchestration

Query external AI agents for independent, unbiased expert opinions. Each agent has a distinct thinking role and responds in a structured format for easy comparison.

## Why this skill

**Different frontier models see different things.** Each has a slightly different training distribution, tool-use style, and failure mode — so they latch onto different aspects of the same problem.

- **Brainstorming / problem-solving / feature design.** Querying Codex + Claude + OpenCode/Gemini (or any subset) in parallel yields a wider solution space than any single model alone. You get original, non-obvious alternatives that one model would never surface on its own.
- **Code review.** Different models find different issues. One catches a subtle race condition; another flags an auth gap; a third questions the architecture. The union of their findings is materially broader than a single-reviewer pass.

The skill keeps each agent independent (no debate, no cross-contamination) and lets the caller adjudicate — you get raw parallel perspectives, not a homogenized committee answer.

## Contents

- [Quick Start](#quick-start)
- [Design Principles](#design-principles)
- [Anti-Bias Protocol](#anti-bias-protocol)
- [Agent Freedom and Read-Only Guardrails](#agent-freedom-and-read-only-guardrails)
- [Configuration](#configuration)
  - [OpenCode provider choice: Zen vs Google direct vs OpenAI direct](#opencode-provider-choice-zen-vs-google-direct-vs-openai-direct)
  - [Claude Code backend](#claude-code-backend)
- [Scripts](#scripts)
  - [Flags & Exit Codes](#flags--exit-codes)
- [Code Review Mode](#code-review-mode)
- [Multi-Stage Review Modes: superreview & ultrareview](#multi-stage-review-modes-superreview--ultrareview)
- [When to Use Which](#when-to-use-which)
- [Synthesizing Responses](#synthesizing-responses)
- [Prompt Patterns](#prompt-patterns)
- [Environment Variables](#environment-variables)
- [Prerequisites](#prerequisites)

## Quick Start

```bash
# 1. See what's configured (XML plan — dry-run, no agents run).
scripts/consensus-query.sh --list-agents

# 2. Ask the consensus (human-readable markdown).
scripts/consensus-query.sh "Should we use Postgres or SQLite for this CLI tool?"

# 3. Agent-friendly output (stable XML, escaped via CDATA).
scripts/consensus-query.sh --xml "Review this function" < src/auth.py

# 4. Code review mode (2 specialists, quoted-code validated, XML or markdown).
scripts/code-review.sh path/to/file.py
git diff HEAD | scripts/code-review.sh --xml --diff
```

Edit `config.json` to enable/disable agents or swap models. See `config.example.json` for a fuller template with multiple backends.

### Passing the prompt

The prompt is a **positional** argument. Three ways to pass it, pick whichever is convenient:

```bash
# (a) Inline string — best for short prompts.
scripts/consensus-query.sh --xml "review this design"

# (b) From a file via stdin — best for long multi-line prompts.
#     With NO positional argument, stdin is treated as the prompt.
scripts/consensus-query.sh --xml < prompt.txt
cat prompt.txt | scripts/consensus-query.sh --xml

# (c) From a file via flag — same as (b) but uses RAW mode
#     (no role/principles/template wrapping; agents see the file verbatim).
#     Use this for benchmarks/evals where wrapper differences would skew results.
scripts/consensus-query.sh --xml --prompt-file prompt.txt
```

**When BOTH a positional prompt and stdin are given**, stdin is appended to the prompt as `--- Input ---` context. That is the existing pattern for piping a file under review:

```bash
cat src/auth.py | scripts/consensus-query.sh "review this code"
#       └── stdin = context ────┘   └── positional = the prompt ─┘
```

## Design Principles

**Intellectual independence**: Agents are instructed to think from first principles, challenge the framing of questions, and propose alternatives not mentioned in the query. They are free thinkers within the given context, not yes-men.

**Role differentiation** (set per agent in `config.json`):
- **analyst** = Rigorous Analyst — precision, code correctness, edge cases, implementation depth, security (default for Codex)
- **lateral** = Lateral Thinker — cross-domain patterns, creative alternatives, questioning premises, big picture (default for Gemini / OpenCode with Gemini-3.1-Pro)

**Structured output**: All agents respond using a common template (Assessment, Key Findings, Blind Spots, Alternatives, Recommendation with confidence level), making synthesis straightforward.

## Anti-Bias Protocol

When formulating queries for consilium, follow these rules to maximize the value of independent opinions:

1. **State the problem, not your solution.** Instead of "Should we use X?", describe the constraints and goals.
2. **Don't lead.** Avoid "I think X is best, what do you think?" — this anchors the response.
3. **Include raw context.** Pipe code files or paste error logs directly rather than summarizing them (summaries carry your interpretation).
4. **Omit your hypothesis when possible.** Let agents form their own before revealing yours.

## Agent Freedom and Read-Only Guardrails

Agents are spawned **in the caller's current working directory** with their native agentic toolchain intact. They can:

- `Read`, `Grep`, `Glob`, `find_references`, `git log/blame` across the real repository
- Consult `CLAUDE.md`, `AGENTS.md`, `README`, config files, tests, call sites, neighboring modules
- Use web search / fetch if their backend supports it (Claude Code, OpenCode, Codex all do)
- Run SAST-style introspection via their built-in shells

What they **cannot** do (enforced per backend):

| Backend | Read-only guard |
|---------|-----------------|
| Codex | `--sandbox read-only --ask-for-approval never` |
| Claude Code | `--permission-mode plan` |
| OpenCode | `--agent plan` (plan is opencode's built-in read-only agent) |
| Gemini CLI | `--approval-mode plan` |

No `Edit`, `Write`, `Bash(git commit ...)`, `Bash(rm ...)`, or any write-back tool is authorized. Implementation of recommendations is the caller's job. If a backend tries to escalate (e.g. needs to run a command that violates read-only), the call fails rather than silently escalating.

## Configuration

Agents are declared in `config.json` at the skill root. Each agent has:

| Field | Purpose |
|-------|---------|
| `enabled` | Whether it participates in `consensus-query` |
| `backend` | CLI that actually runs: `codex-cli`, `gemini-cli`, `opencode`, `claude-code` |
| `model` | Model id passed to that CLI |
| `role` | `analyst` (deep/precise) or `lateral` (broad/creative) |
| `label` | Display name in reports (optional) |
| `effort` | Reasoning effort. **opencode:** maps to `opencode run --variant` (e.g. `low`, `medium`, `high`, `max`) — provider-specific, see [Discovering reasoning variants](#discovering-opencode-reasoning-variants-per-model) below. **claude-code:** maps to `claude --effort` (`low`, `medium`, `high`, `xhigh`, `max`). Other backends ignore it. |

Default config (`config.json`):
- `codex` (backend=codex-cli, model=gpt-5.5, role=analyst) — **enabled**
- `gemini-cli` (backend=gemini-cli, model=gemini-3.1-pro-preview, role=lateral) — **disabled**
- `opencode` (backend=opencode, model=opencode/gemini-3.1-pro, role=lateral, effort=high) — **enabled**
- `claude-code` (backend=claude-code, model=opus, effort=max, role=analyst) — **disabled**
- `opencode-go-minimax` (backend=opencode, model=opencode-go/minimax-m2.7, role=lateral, effort=high) — **enabled**
- `opencode-go-deepseek` (backend=opencode, model=opencode-go/deepseek-v4-pro, role=analyst, effort=max) — **enabled**
- `opencode-go-mimo` (backend=opencode, model=opencode-go/mimo-v2.5-pro, role=lateral, effort=high) — **enabled**
- `opencode-go-kimi` (backend=opencode, model=opencode-go/kimi-k2.6, role=analyst, effort=high) — **enabled**
- `opencode-go-glm` (backend=opencode, model=opencode-go/glm-5.1, role=lateral, effort=high) — **enabled**
- `opencode-openai` (backend=opencode, model=openai/gpt-5.5, role=analyst, effort=high) — **disabled** (reference entry; flip on if you want OpenAI direct)

Effort policy: `max` is used wherever the model exposes it (`claude-code`, `opencode-go/deepseek-v4-pro`); `high` is the fallback for models that top out at `high` (`opencode/gemini-3.1-pro`, `opencode-go/mimo-v2.5-pro`, `openai/gpt-5.5` if you don't want `xhigh`) or expose no variants at all (`minimax`, `kimi`, `glm` — `effort` is set but ignored by the provider).

Multiple agents can share one backend — the dispatcher passes the entry id through `CONSILIUM_AGENT_ID`, so each backend script reads its own slice of `config.json`.

Edit `config.json` to flip agents on/off or change models. Set `CONSILIUM_CONFIG=/path/to/custom.json` to use an override file.

### OpenCode provider choice: Zen vs Google direct vs OpenAI direct

The `opencode` backend works with any provider/model that OpenCode supports. For Gemini 3.1 Pro you have two options:

- **Zen** (default): `"model": "opencode/gemini-3.1-pro"` — goes through OpenCode Zen. Works out of the box once `opencode providers login opencode` (or a valid Zen credential) is configured.
- **Google direct**: `"model": "google/gemini-3.1-pro-preview"` — goes straight to Google's v1beta API. Requires `GOOGLE_GENERATIVE_AI_API_KEY` (OpenCode does **not** pick up `GEMINI_API_KEY` for this provider).

For OpenAI flagship models (GPT-5.5, GPT-5.4, etc.) there's a third path:

- **OpenAI direct**: `"model": "openai/gpt-5.5"` — goes straight to OpenAI's API via the `openai/*` provider in OpenCode. Requires either an `opencode auth login` session for OpenAI (oauth) or `OPENAI_API_KEY` in the environment. The default config ships an `opencode-openai` entry **disabled** as a reference; flip `enabled=true` if you want a GPT-5.5 voice in the consilium. Variants: `none / low / medium / high / xhigh` — pick `xhigh` if you want the heaviest reasoning, otherwise `high` is the safe default.

Flip between providers by editing the `model` field; the rest of the config stays the same.

### Discovering OpenCode reasoning variants per model

`opencode run --variant <effort>` is provider-specific — each model exposes its own set (or none). Don't guess: enumerate them from the CLI before setting `effort` in `config.json`.

**One-liner — list every model with its supported variants:**

```bash
opencode models opencode --verbose 2>&1 | python3 -c '
import sys, json
lines = sys.stdin.read().split("\n")
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("opencode/") or line.startswith("opencode-go/"):
        model_id, json_lines, depth, started = line, [], 0, False
        i += 1
        while i < len(lines):
            s = lines[i]; json_lines.append(s)
            for c in s:
                if c == "{": depth += 1; started = True
                elif c == "}": depth -= 1
            i += 1
            if started and depth == 0: break
        try:
            v = list(json.loads("\n".join(json_lines)).get("variants", {}).keys())
            print(f"{model_id}\t{v}")
        except Exception: pass
    else:
        i += 1
'
```

Swap `opencode` for `opencode-go` (or any other provider id) to scan a different namespace; drop the provider arg to scan everything `opencode models` knows.

**Interpreting the result:**

- Non-empty list (e.g. `['low', 'medium', 'high', 'max']`) → set `effort` to the highest one you want.
- `[]` → the model has no reasoning variants. `--variant` is silently ignored; setting `effort` in config is harmless but does nothing.
- If a variant in your config isn't on the list, `opencode run` rejects the call. Re-enumerate after upgrading `opencode` — providers add/remove tiers between releases.

**Snapshot of the currently configured opencode models** (re-run the one-liner if you change the set):

| Model | Variants | `effort` in default config |
|-------|----------|----------------------------|
| `opencode/gemini-3.1-pro` | low, medium, high | `high` (no `max`) |
| `opencode-go/deepseek-v4-pro` | low, medium, high, **max** | `max` |
| `opencode-go/mimo-v2.5-pro` | low, medium, high | `high` (no `max`) |
| `opencode-go/minimax-m2.7` | — | `high` (ignored) |
| `opencode-go/kimi-k2.6` | — | `high` (ignored) |
| `opencode-go/glm-5.1` | — | `high` (ignored) |
| `openai/gpt-5.5` | none, low, medium, high, xhigh | `high` (entry **disabled** by default) |

### Claude Code backend

The `claude-code` backend shells out to `claude -p` (headless mode, see [docs](https://code.claude.com/docs/en/headless)). Useful when you want a second Claude in the consilium — e.g. Opus as analyst cross-checking Codex.

- `model`: a shortname (`opus`, `sonnet`, `haiku`) or full id (`claude-opus-4-7`, `claude-sonnet-4-6`).
- `effort`: maps to `claude --effort` — accepts `low`, `medium`, `high`, `xhigh`, `max`. Default config sets `max` for opus; omit the field to fall back to the skill's default of `max` for the claude-code backend.
- Runs in the caller's CWD with `--permission-mode plan` — Claude can freely `Read`/`Grep`/`Glob`/`Bash` read-only across the project, but cannot `Edit`/`Write`. Override with `CLAUDE_PERMISSION_MODE` only if you know what you're doing.
- Authentication uses the same Claude Code credentials the CLI is already logged in with (`claude /login`).

Note: `claude-code` is disabled in the default config to avoid spawning another Claude session accidentally. Flip `enabled` to `true` in `config.json` (or `CONSILIUM_CONFIG`) when you want it in the consensus run.

## Scripts

All scripts in `scripts/` directory. The skill auto-detects its install location.

### Single Agent Queries

Per-agent scripts always execute when invoked. The `enabled` field in `config.json` is consulted **only** by `consensus-query.sh` to build the default agent set (when neither `-a` nor `-x` is given). Direct invocation of a per-agent script ignores `enabled` — that's by design (single source of truth for the run/skip decision lives in the dispatcher).

When `-a`/`-x` causes `consensus-query.sh` to run an `enabled=false` agent, the dispatcher emits a stderr line like `[<Label>] forced via --agents (enabled=false in config)` so the override is visible.

```bash
# Codex (analyst by default)
scripts/codex-query.sh "question" [context_file]
cat file.py | scripts/codex-query.sh "review this"

# Gemini CLI (lateral by default; disabled in default config)
scripts/gemini-query.sh "question" [context_file]
cat file.py | scripts/gemini-query.sh "review this"

# OpenCode (lateral by default, model per config.json)
scripts/opencode-query.sh "question" [context_file]
cat file.py | scripts/opencode-query.sh "review this"

# Claude Code (analyst by default; disabled in default config)
scripts/claude-query.sh "question" [context_file]
cat file.py | scripts/claude-query.sh "review this"
```

### Consensus Query (All Enabled Agents in Parallel)

```bash
scripts/consensus-query.sh "architecture question"
cat file.py | scripts/consensus-query.sh "review this code"
scripts/consensus-query.sh --xml "review this"            # XML report for agent consumers
scripts/consensus-query.sh --list-agents                   # dry-run: dump plan, don't query
```

`consensus-query.sh` reads `config.json`, launches every agent with `enabled=true` in parallel, and prints their responses grouped by label. Add/remove agents permanently by editing the config; for ad-hoc runs use `-a/--agents` and `-x/--exclude` (see below).

### Flags & Exit Codes

All scripts accept `-h` / `--help`. Both `consensus-query.sh` and `code-review.sh` accept:

| Flag | Effect |
|------|--------|
| `--xml` | Emit `<consilium-report>` (or `<code-review-report>`) with each agent wrapped in `<agent>…<response><![CDATA[…]]></response></agent>`. Stable for agent consumers (no markdown-heading collision). |
| `--list-agents` *(consensus only)* | Print `<consilium-plan>` (every configured agent, enabled/disabled, with `backend-available`) and exit. No queries are run — use this as an inspection / dry-run. |
| `-a, --agents <ID\|GLOB>` | Override the active agent set with this id or glob (e.g. `'opencode-go-*'`). **Repeatable**; comma-separated values also accepted (`-a codex,opencode-go-kimi`). When given, the per-agent `enabled` flag in `config.json` is ignored — only matched agents run. Falls back to env `CONSILIUM_AGENTS`. |
| `-x, --exclude <ID\|GLOB>` | Subtract matching agents from the active set. Repeatable. Combine with `--agents` for include-then-exclude composition. Falls back to env `CONSILIUM_EXCLUDE`. |

**Ad-hoc agent selection examples:**
```bash
# Single agent
scripts/consensus-query.sh -a opencode-go-kimi "Q"

# All OC-Go models (glob)
scripts/consensus-query.sh -a 'opencode-go-*' "Q"

# Everything-except-codex
scripts/consensus-query.sh -x codex "Q"

# Composition: only OC-Go but skip MiniMax
scripts/consensus-query.sh -a 'opencode-go-*' -x opencode-go-minimax "Q"

# Same via env (scriptable)
CONSILIUM_AGENTS='codex,opencode-go-kimi' scripts/consensus-query.sh "Q"
```

Exit codes (stable across all scripts):

| Code | Meaning |
|------|---------|
| `0` | Success (all queried agents replied; or, for `consensus-query.sh`, the active agent set may be smaller than the configured set if some are disabled or filtered) |
| `2` | **Consensus only:** partial failure (≥1 succeeded, ≥1 failed) |
| `3` | **Consensus only:** every queried agent failed |
| `4` | Config error (missing CLI, invalid config, unknown role/agent id) |
| `5` | Usage error (missing prompt, unknown flag) |
| other | Propagated from the backend CLI (e.g. `124` on timeout) |

## Code Review Mode

`scripts/code-review.sh` is a focused pipeline for reviewing a single file or a unified diff. It runs **exactly two specialist passes** — `security` and `correctness` — in parallel, then validates each finding's `quoted-code` against the real source.

Design choices are grounded in the 2024-2026 multi-agent code review literature:

- **Two specializations only** (security + correctness). Readability/perf agents empirically produce nit spam and hurt precision.
- **No coordinator / no debate.** The caller (you) adjudicates. Debate rounds empirically entrench errors (Wu et al. 2025; Choi et al. 2025).
- **Heterogeneous models** via the existing config (Codex + OpenCode by default) reduce shared blind spots.
- **Fixed cost.** Adding a 3rd enabled agent does not add a 3rd pass; the skill always runs 2 passes and rotates agents round-robin.
- **Hallucinated line numbers are caught locally.** Every finding carries `<quoted-code>`, and the validator cross-checks it against the source file (`quote-valid="true|false"`).

### Usage

```bash
# File on disk (quoted-code validated against the file)
scripts/code-review.sh path/to/file.py
scripts/code-review.sh --xml path/to/file.py

# Unified diff piped on stdin (quoted-code validation is skipped)
git diff HEAD | scripts/code-review.sh --diff
git diff HEAD | scripts/code-review.sh --xml --diff
```

### Finding schema (XML output)

```xml
<finding index="N" severity="critical|high|medium|low" category="security|correctness"
         file="..." line-start="N" line-end="N" confidence="0.0..1.0"
         source-agent="..." source-role="security|correctness"
         quote-valid="true|false">
  <title>...</title>
  <rationale><![CDATA[includes one reason this might be a false positive]]></rationale>
  <suggested-fix><![CDATA[...]]></suggested-fix>
  <quoted-code><![CDATA[verbatim source at line-start..line-end]]></quoted-code>
</finding>
```

Findings are sorted `severity desc, confidence desc`. No severity filtering by default — triage is the caller's job.

### Severity rubric

Unified across security + correctness. Specialists score each finding on two axes (worst-case impact × likelihood/reachability) and pick the tier that matches. Synthesized from CVSS v4, OWASP Risk Rating, GitHub Advisory DB, Chromium, MSRC, SEI CERT, SonarQube, Semgrep.

| Severity | Action horizon | Operational definition | Security examples | Correctness examples |
|----------|----------------|------------------------|-------------------|----------------------|
| **critical** | Merge blocker | RCE / trust-boundary bypass / data loss / guaranteed outage, with a concrete exploit or dataflow trace | SQLi on public endpoint with concatenated query; unsafe deserialization of untrusted input; hardcoded prod credential | Payment/ledger math silently corrupts balances; unconditional null deref on hot request path; race on shared mutable state under prod load |
| **high** | Fix before release | Critical-tier impact gated by a non-trivial precondition (auth, specific config), OR moderate impact with high reachability | Stored XSS in authenticated admin view; CSRF on state-changing endpoint; path traversal behind login; missing authz on tenant resource | Unhandled exception on documented error path crashing a worker; file/DB-handle leak exhausting pools; retry logic that double-charges |
| **medium** | Schedule | Limited impact (info disclosure, localized incorrectness, degraded-but-recoverable), OR critical impact gated by implausible preconditions | Stack traces leaked to end users; missing `HttpOnly`/`Secure` on non-session cookie; weak-but-not-broken crypto parameter | Incorrect edge-case handling in non-critical helper; missing input validation that callers already satisfy; N+1 query degrading a list endpoint |
| **low** | Optional / backlog | Cosmetic, stylistic, defense-in-depth; minimal real-world impact | Missing `nosniff` header where CSP already mitigates; `Math.random()` for non-security id | Dead code; inconsistent naming; redundant null check after non-null assertion |

Adjustments: downgrade one level on mitigating factors (auth required, non-default config, unusual interaction). Speculative findings stay at the lower tier — upgrade only with a working PoC or trace.

### Using the results (for the caller)

You are the adjudicator. Specialists emit independent findings — your job is to **select and synthesize**, not re-review (RovoDev 2601.01129, RevAgent 2511.00517).

1. **Drop quote-mismatched findings** (`quote-valid="false"`) — likely hallucinations.
2. **Merge duplicates across specialists.** Same root cause in different framings → one item; keep the clearer rationale and note both agents.
3. **Surface conflicts without resolving them.** If Security says "sanitize X" and Correctness says "X is fine" — present both to the user and let them adjudicate; don't break the tie yourself.
4. **Gate by action horizon** using the severity rubric above: `critical` = block the merge, `high` = fix before release, `medium` = track, `low` = optional.
5. **Do not re-review.** Do not generate new findings inside the adjudication step. Do not run a debate loop — adversarial re-reviewing empirically reduces precision (CR-Bench 2603.11078).

### When NOT to use code-review mode

- **Open-ended architecture questions** → use `consensus-query.sh`; specialists will be too narrow.
- **Huge files (>1000 lines)** → split into function-sized diffs first; LLMs degrade past that length.
- **Multi-file cross-references** → not modelled here; rerun per file and stitch findings.

## Multi-Stage Review Modes: superreview & ultrareview

`code-review.sh` is single-stage and caller-judged. For higher-stakes reviews
where you want the union of many panels filtered automatically by an LLM judge,
the skill ships two multi-stage pipelines ported from the *ultrareview-bench*
(see `docs/blog/code-review-2pass-pilot/` if you have access). Each one
prescribes a fixed agent set and stage layout — they're not configurable
per-call, by design, because the configurations were tuned by marginal-uplift
analysis on a 65-issue ground-truth pilot.

> **Important:** these are heavy modes. Don't run them on every diff. Use them
> when you'd otherwise pull two senior engineers off other work for a deep
> review, or for code that touches money / auth / persistence.

### `scripts/superreview.sh` — small-swarm + 2 frontier add-ons

10 LLM calls; ~$0.90–1.50 on a 12KB file (linear with size). Pareto sweet-spot
in the bench at 67.7% recall / 82.7% sev-w on snippet1.cs.

```
Stage 1: discovery-small (parallel)    7 small/cheap passes
  - opencode-go-deepseek-flash analyst       uncapped
  - opencode-go-qwen36-plus    analyst       uncapped
  - opencode-go-qwen36-plus    lateral       uncapped
  - opencode-go-deepseek-flash architecture  uncapped
  - opencode-go-deepseek-flash correctness   cap=10
  - opencode-go-qwen36-plus    architecture  cap=3
  - opencode-go-qwen36-plus    security      uncapped
Stage 2: discovery-frontier (parallel) 2 hand-picked add-ons
  - opencode-gpt5.5-xhigh      analyst       uncapped
  - claude-code (Opus 4.7 max) lateral       uncapped
Stage 3: dedup (deterministic union)
Stage 4: judge — claude-sonnet (default)
```

Usage:
```bash
scripts/superreview.sh path/to/file.cs
scripts/superreview.sh --xml path/to/file.cs
git diff HEAD | scripts/superreview.sh --diff
scripts/superreview.sh --dry-run path/to/file.cs   # plan + config check, no LLM calls
scripts/superreview.sh --judge claude-code path/to/file.cs   # override judge
```

### `scripts/ultrareview.sh` — broad-grid + specialists + probe

21 LLM calls; ~$1.50–3.00 on a 12KB file. Best severity-weighted recall in the
bench (86.4%). Slower and more expensive than superreview; use when you need
maximum coverage and lowest false-positive rate.

```
Stage 1: broad (parallel)         4 frontier analysts
  - codex (gpt-5.5 high)         analyst      uncapped
  - claude-code (Opus 4.7 max)   analyst      uncapped
  - opencode (gemini-3.1-pro)    lateral      uncapped
  - opencode-go-deepseek (Pro)   analyst      uncapped
Stage 2: specialists (parallel)   5×3 matrix, uniform cap=10
  - 3 small models × 5 roles (security/correctness/performance/architecture/consistency)
Stage 3: probe (sequential)       1 generic gap probe (model picks focus)
  - opencode-go-deepseek-flash auditor cap=10
Stage 4: dedup
Stage 5: judge — claude-code (Opus 4.7 max)
                fallback: opencode-gpt5.5-xhigh on primary failure
```

Usage:
```bash
scripts/ultrareview.sh path/to/file.cs
scripts/ultrareview.sh --xml path/to/file.cs
scripts/ultrareview.sh --dry-run path/to/file.cs       # plan check
scripts/ultrareview.sh --no-fallback path/to/file.cs   # disable judge fallback
```

The Opus-judge fallback is intentional — Claude Code's `claude -p` backend
timed out at 1200s on 200+ findings during the bench. Setting `--no-fallback`
lets you treat a primary judge failure as fatal (useful in CI).

### Output filtering

Both modes filter findings via the LLM judge before printing. Verdicts are:

- **VALID** — kept as-is.
- **DOWNGRADE** — kept, severity adjusted to `new_severity` from the judge.
- **DUPLICATE** — dropped (judge marks the canonical finding it duplicates).
- **FALSE_POSITIVE** — dropped (hallucination, vague advice, fix doesn't fit
  the defect, etc.).

The default markdown output groups kept findings by severity. The `--xml`
form preserves the full `<code-review-report>` schema and adds a
`<judge-summary>` element with verdict counts.

### Required `config.json` entries

These modes hardcode their agent IDs. The default `config.json` already has
all of them defined (most are `enabled=false`, which is fine — multi-stage
modes ignore `enabled` and look up the entry by id directly):

| ID | Where used |
|---|---|
| `codex` | ultrareview broad |
| `opencode` | ultrareview broad |
| `claude-code` | both, plus ultrareview judge |
| `claude-sonnet` | superreview judge |
| `opencode-go-deepseek` | ultrareview broad |
| `opencode-go-deepseek-flash` | both, specialist + probe |
| `opencode-go-qwen36-plus` | both |
| `opencode-gpt5.5-xhigh` | superreview frontier add-on, ultrareview judge fallback |
| `opencode-gemini-3-flash` | ultrareview specialist |

If any are missing the script exits 4 with the list of missing IDs.

### When NOT to use multi-stage modes

- **Quick diff review** → use `code-review.sh`. Multi-stage adds 5-10× cost.
- **Code under 50 lines** → judge has nothing to do; use `code-review.sh`.
- **CI without a judge LLM** → use `--xml` from `code-review.sh` and parse
  findings yourself.
- **Files >2000 lines** → split first; even with the judge, the union XML
  becomes hard to score reliably.

## When to Use Which

Pick by role, not by vendor. The default config has Codex (`analyst`) + OpenCode/Gemini-3.1-Pro (`lateral`) enabled; flip `claude-code` or `gemini-cli` on in `config.json` when you want an additional voice.

| Situation | Script | Role(s) involved |
|-----------|--------|-------------------|
| Code review, security audit | per-agent `analyst` script (`codex-query.sh` or `claude-query.sh`) | analyst — precision, edge cases |
| Architecture decision, design choice | `consensus-query.sh` | analyst + lateral — depth + breadth |
| "Are we solving the right problem?" | per-agent `lateral` script (`opencode-query.sh` or `gemini-query.sh`) | lateral — challenges premises |
| Bug investigation, root cause analysis | per-agent `analyst` script | analyst — goes deep into implementation |
| Exploring alternatives, brainstorming | per-agent `lateral` script | lateral — cross-domain analogies |
| High-stakes or irreversible decision | `consensus-query.sh` | all enabled — reduce blind spots |
| Agent-to-agent integration (downstream parser) | `consensus-query.sh --xml` | any — stable structured output |

## Synthesizing Responses

Agents respond with a shared structure. Compare section by section:

- **Assessment vs Assessment**: Do they frame the problem differently? A framing difference often reveals the most insight.
- **Blind Spots**: Union of both agents' blind spots is your risk map.
- **Alternatives**: Check if either agent proposed something neither you nor the other agent considered.
- **Recommendations**: Agreement = high confidence. Divergence = investigate the reasoning, not just the conclusion.

### Response Patterns

When comparing the two responses, classify the pattern and act accordingly:

- **Agreement**: Both recommend same approach — high confidence, proceed
- **Complementary**: Different valid points that don't conflict — combine insights into a richer picture
- **Contradiction**: Conflicting recommendations — present both with reasoning, let user decide
- **Unique insight**: One agent caught something the other missed — highlight it, this is often the most valuable output

## Prompt Patterns

### Architecture Decision (unbiased framing)
```bash
scripts/consensus-query.sh "We need real-time updates for ~100 concurrent users.
Updates are server-initiated only. Current stack: [describe your stack].
Latency target: under 500ms from event to UI update.
What approach would you recommend and why?"
```

### Code Review (pipe raw code, let agents form opinions)
```bash
cat src/services/auth.py | scripts/codex-query.sh \
  "Review this authentication service. Focus on whatever concerns you most."
```

### Problem Investigation (provide facts, not hypotheses)
```bash
scripts/codex-query.sh "Database query returns empty result.
Direct query with same filter returns 5 documents.
[paste query here]
What's happening?"
```

## Environment Variables

- `CONSILIUM_CONFIG`: Path to a custom JSON config (default: `<skill>/config.json`)
- `CODEX_MODEL`: Override Codex model at runtime (default: value from config)
- `GEMINI_MODEL`: Override Gemini CLI model at runtime (default: value from config)
- `OPENCODE_MODEL`: Override OpenCode model at runtime (default: value from config)
- `OPENCODE_AGENT`: Override OpenCode built-in agent (default: `plan`, read-only)
- `OPENCODE_EFFORT`: Override OpenCode reasoning effort (default: config `effort` field, or `high`)
- `CLAUDE_MODEL`: Override Claude Code model at runtime (alias like `opus` or full id)
- `CLAUDE_PERMISSION_MODE`: Override Claude Code permission mode (default: `plan`)
- `CLAUDE_EFFORT`: Override Claude Code reasoning effort (default: config `effort` field, or `max` if both unset). Levels: `low`, `medium`, `high`, `xhigh`, `max`.
- `CODEX_EFFORT`: Override Codex reasoning effort (default: config `effort` field, or `high` if both unset). Levels: `minimal`, `low`, `medium`, `high`, `xhigh`.
- `GEMINI_API_KEY`: Required for the `gemini-cli` backend (v1beta model access)
- `GOOGLE_GENERATIVE_AI_API_KEY`: Required if the `opencode` backend uses `google/...` models
- `OPENAI_API_KEY`: Required if the `opencode` backend uses `openai/...` models and OpenCode is not already logged in via `opencode auth login`
- `AGENT_TIMEOUT`: Timeout seconds (default: 1200)

## Prerequisites

- [Codex CLI](https://github.com/openai/codex) installed and authenticated (`codex --version`) — for the `codex-cli` backend
- [OpenCode CLI](https://opencode.ai) installed (`opencode --version`) — for the `opencode` backend. For Zen models (`opencode/...`) run `opencode providers login opencode` once; for Google direct models (`google/...`) set `GOOGLE_GENERATIVE_AI_API_KEY`; for OpenAI direct models (`openai/...`) either run `opencode auth login` and pick OpenAI, or set `OPENAI_API_KEY`.
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) installed (`gemini --version`) — for the `gemini-cli` backend (optional; falls back to direct API)
- [Claude Code CLI](https://docs.claude.com/claude-code) installed and logged in (`claude --version`, `claude /login`) — for the `claude-code` backend
- `GEMINI_API_KEY` environment variable — required only when `gemini-cli` backend is enabled (get key at https://ai.google.dev/gemini-api/docs/api-key)
- Python 3 (for config parsing and Gemini API fallback)
