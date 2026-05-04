# agents-consilium

Multi-agent orchestration skill. Dispatches a query to **Codex (GPT-5.4)**, **Claude Code (Opus)**, **OpenCode (Gemini 3.1 Pro via Zen or Google direct)**, and **Gemini CLI** in parallel, each with a distinct thinking role, then hands the raw responses back to the caller as markdown or XML.

## Why this skill

**Different frontier models see different things.** Each has a slightly different training distribution, tool-use style, and failure mode — so they latch onto different aspects of the same problem. Two concrete payoffs:

- **Brainstorming / problem-solving / feature design.** A fan-out across heterogeneous models yields a wider solution space than any single model alone — you get original, non-obvious alternatives that one model would never surface on its own.
- **Code review.** Different models find different classes of issues. One catches a subtle race; another flags an auth gap; a third questions the architecture. The *union* of their findings is materially broader than a single-reviewer pass.

The skill keeps each agent independent (no debate, no cross-contamination) and the caller adjudicates — you get raw parallel perspectives, not a homogenized committee answer.

## Install

```bash
npx skills add CodeAlive-AI/ai-driven-development@agents-consilium -g -y
```

## Prerequisites

At least one backend CLI must be installed and authenticated:

| Backend | Install | Auth |
|---------|---------|------|
| [Codex CLI](https://github.com/openai/codex) | `npm i -g @openai/codex` | `codex` (ChatGPT login) |
| [OpenCode](https://opencode.ai) | See site | `opencode providers login opencode` (Zen) / `opencode providers login opencode-go` (Go subscription) / `GOOGLE_GENERATIVE_AI_API_KEY` (Google direct) |
| [Claude Code](https://docs.claude.com/claude-code) | See site | `claude /login` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `npm i -g @google/gemini-cli` | `GEMINI_API_KEY` |

Default config enables **codex** + **opencode** (Zen / Gemini 3.1 Pro) + five **OpenCode Go** models (`MiniMax M2.7`, `DeepSeek V4 Pro`, `MiMo V2.5 Pro`, `Kimi K2.6`, `GLM-5.1`). Each model uses the highest reasoning tier its provider exposes — `effort: max` for `DeepSeek V4 Pro` (and for `claude-code`/Opus when enabled), `effort: high` everywhere else (the rest top out at `high` or expose no variants). See [SKILL.md → Discovering OpenCode reasoning variants](SKILL.md#discovering-opencode-reasoning-variants-per-model) for how to enumerate variants per model. `gemini-cli` and `claude-code` are disabled by default — flip `enabled: true` in `config.json` to add them, or disable any OC-Go entry to trim parallelism.

Multiple agents can share one backend (e.g. five OpenCode-Go models all use `backend: "opencode"`). Per-agent config is selected by the entry's id; the dispatcher passes it through `CONSILIUM_AGENT_ID`.

## Quick start

```bash
# 1. See what's configured (dry-run, no agents queried).
scripts/consensus-query.sh --list-agents

# 2. Ask the consensus (markdown report grouped by agent).
scripts/consensus-query.sh "Should we use Postgres or SQLite for this CLI tool?"

# 3. Agent-friendly output (stable XML, CDATA-escaped).
scripts/consensus-query.sh --xml "Review this function" < src/auth.py

# 4. Code review mode (2 specialists, quoted-code validated).
scripts/code-review.sh path/to/file.py
git diff HEAD | scripts/code-review.sh --xml --diff

# 5. Ad-hoc agent selection (no config edit). Repeatable; globs supported.
scripts/consensus-query.sh -a opencode-go-kimi "Q"        # one agent
scripts/consensus-query.sh -a 'opencode-go-*' "Q"          # all OC-Go models
scripts/consensus-query.sh -x codex "Q"                    # everything except codex
scripts/consensus-query.sh -a codex -a opencode-go-kimi "Q"  # composition
CONSILIUM_AGENTS='codex,opencode-go-kimi' scripts/code-review.sh file.py  # env form
```

## What it does

Two modes:

| Mode | When | Entry point |
|------|------|-------------|
| **Consensus query** | Open-ended problems (architecture, design, root-cause, brainstorming) — you want multiple independent takes | `scripts/consensus-query.sh` |
| **Code review** | Focused review of a file or diff — runs 2 fixed specializations (security + correctness), returns XML findings | `scripts/code-review.sh` |

### Consensus query

Each agent is assigned a `role` in config:

- **analyst** — Rigorous Analyst (precision, edge cases, implementation depth). Default: Codex, Claude Opus.
- **lateral** — Lateral Thinker (cross-domain patterns, questioning premises, creative alternatives). Default: OpenCode (Gemini 3.1 Pro), Gemini CLI.

Agents respond with a shared structure (Assessment / Key Findings / Blind Spots / Alternatives / Recommendation + confidence) so the caller can compare section by section.

### Code review

Runs **exactly two specialist passes** — `security` and `correctness` — in parallel across whichever agents are enabled (round-robin; adding a 3rd agent does not add a 3rd pass, cost stays fixed).

Findings come back as XML:

```xml
<finding severity="critical|high|medium|low" category="security|correctness"
         file="..." line-start="N" line-end="N" confidence="0.0..1.0"
         source-agent="..." source-role="..." quote-valid="true|false">
  <title>…</title>
  <rationale><![CDATA[includes one reason this might be a false positive]]></rationale>
  <suggested-fix><![CDATA[…]]></suggested-fix>
  <quoted-code><![CDATA[verbatim source at line-start..line-end]]></quoted-code>
</finding>
```

Every finding's `<quoted-code>` is cross-checked against the real file on disk — mismatches are flagged `quote-valid="false"` so the caller can drop probable hallucinations.

## Key features

- **Heterogeneous models** — different training distributions reduce shared blind spots
- **Agent freedom + read-only guardrails** — each backend runs in the caller's CWD with its native tools (`Read`/`Grep`/`Glob`/`Bash` read-only, web when supported) but cannot `Edit`/`Write`. Enforced per backend: Codex `--sandbox read-only --ask-for-approval never`, Claude Code `--permission-mode plan`, OpenCode `--agent plan`, Gemini `--approval-mode plan`.
- **No coordinator, no debate** — caller adjudicates. Debate rounds empirically entrench errors (CR-Bench 2603.11078).
- **Hypothesis → Validation → Fix-consistency workflow** — specialists must form a hypothesis, validate via path-feasibility / callers / project docs, then write a concrete fix and verify it eliminates the defect (drops when incoherent).
- **Hallucination + actionability gates** (RovoDev 2601.01129) — findings must reference real symbols and carry a concrete fix
- **4-level severity rubric** (synthesized from CVSS v4, OWASP, GitHub Advisory DB, Chromium, MSRC, SEI CERT, SonarQube, Semgrep) — operational definitions, action horizons, security + correctness examples
- **Stable XML output** with CDATA — safe for downstream agent consumers
- **Differentiated exit codes** (0/2/3/4/5) — agent callers can branch on failure mode

## Sources and methodology

Code-review mode is grounded in the 2024-2026 agentic code-review literature:

- **VulAgent** (arXiv:2509.11523), **RepoAudit** (arXiv:2501.18160), **AgenticSCR** (arXiv:2601.19138) — hypothesis-validation workflow
- **LLM4PFA** (arXiv:2506.10322) — path-feasibility filter (72-96% SAST FP reduction)
- **CR-Bench** (arXiv:2603.11078) — debate loops lower precision; avoided
- **RovoDev** (arXiv:2601.01129, Atlassian Bitbucket production) — two-gate filter (hallucination + actionability); 38.7% comment resolution, -30.8% PR cycle time
- **Systematic Overcorrection** (arXiv:2603.00539) — fix-guided verification; "Full" prompting (explain + propose fix) outperforms direct judgment
- **Sphinx** (arXiv:2601.04252) — checklist-coverage metric (reusable as eval harness)
- **RevAgent** (arXiv:2511.00517) — critic-as-selector pattern (adjudicator selects, doesn't re-review)
- **Engagement in Code Review** (arXiv:2512.05309) — output format correlates with developer acceptance: locality, concrete fix, educational tone

Severity rubric synthesized from: CVSS v4.0 (FIRST), OWASP Risk Rating, GitHub Advisory Database, Chromium Security Severity Guidelines, Microsoft MSRC, SEI CERT (L1/L2/L3), SonarQube (Blocker/Critical/Major/Minor), Semgrep/CodeQL (SARIF error/warning/note).

## Configuration

Agents are declared in `config.json`. Each entry:

| Field | Purpose |
|-------|---------|
| `enabled` | Whether it participates in `consensus-query` |
| `backend` | `codex-cli` / `gemini-cli` / `opencode` / `claude-code` |
| `model` | Model id passed to the CLI |
| `role` | `analyst` or `lateral` |
| `label` | Display name in reports (optional) |
| `effort` | **opencode:** `low`/`medium`/`high`/`max` — maps to `opencode run --variant` (provider-specific; enumerate via `opencode models <provider> --verbose`, see [SKILL.md](SKILL.md#discovering-opencode-reasoning-variants-per-model)). **claude-code:** `low`/`medium`/`high`/`xhigh`/`max` — maps to `claude --effort`. Other backends ignore. |

Edit `config.json` to flip agents on/off or change models. Set `CONSILIUM_CONFIG=/path/to/custom.json` to use an override file. See `config.example.json` for a fuller template.

## File structure

```
agents-consilium/
├── SKILL.md                         # Agent-facing instructions (loaded on trigger)
├── README.md                        # This file
├── config.json                      # Default agent config
├── config.example.json              # Fuller template with all backends
└── scripts/
    ├── consensus-query.sh           # Parallel dispatch across enabled agents
    ├── code-review.sh               # 2-specialist code review pipeline
    ├── code_review_validate.py      # Parses findings, validates quoted-code, renders XML/markdown
    ├── common.sh                    # Shared role prompts, exit codes, helpers
    ├── config.sh                    # JSON config loader (Python-backed)
    ├── codex-query.sh               # Codex CLI backend
    ├── claude-query.sh              # Claude Code headless backend
    ├── opencode-query.sh            # OpenCode backend (Zen + Google direct)
    └── gemini-query.sh              # Gemini CLI backend
```

## License

MIT
