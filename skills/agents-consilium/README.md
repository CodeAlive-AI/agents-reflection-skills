# agents-consilium

Multi-agent orchestration skill. Dispatches a query to **Codex**, **Claude Code**, **OpenCode** (Gemini via Zen or Google direct), and **Gemini CLI** in parallel, each with a distinct thinking role, then hands the raw responses back to the caller as markdown or XML.

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

Default config enables **codex** + **opencode** (Zen / Gemini Pro) + five **OpenCode Go** models (MiniMax, DeepSeek Pro, MiMo, Kimi, GLM). Each model uses the highest reasoning tier its provider exposes — `effort: max` for DeepSeek Pro (and for Claude Code Opus when enabled), `effort: high` everywhere else (the rest top out at `high` or expose no variants). See [SKILL.md → Discovering OpenCode reasoning variants](SKILL.md#discovering-opencode-reasoning-variants-per-model) for how to enumerate variants per model. `gemini-cli` and `claude-code` are disabled by default — flip `enabled: true` in `config.json` to add them, or disable any OC-Go entry to trim parallelism. The exact model id and reasoning tier used for each entry live in `config.json` so they can be bumped without touching this README.

Multiple agents can share one backend (e.g. five OpenCode-Go models all use `backend: "opencode"`). Per-agent config is selected by the entry's id; the dispatcher passes it through `CONSILIUM_AGENT_ID`.

## Quick start

```bash
# 1. See what's configured (dry-run, no agents queried).
scripts/consensus-query.sh --list-agents

# 2. Ask the consensus (markdown report grouped by agent).
scripts/consensus-query.sh "Should we use Postgres or SQLite for this CLI tool?"

# 3. Agent-friendly output (stable XML, CDATA-escaped).
scripts/consensus-query.sh --xml "Review this function" < src/auth.py

# 4. Code review mode (basic = 2 specialists; opt-in 5-specialist deep mode).
scripts/code-review.sh path/to/file.py                       # basic: security + correctness
scripts/code-review.sh --mode specialists path/to/file.py    # +performance, architecture, consistency
git diff HEAD | scripts/code-review.sh --xml --diff

# 5. Ad-hoc agent selection (no config edit). Repeatable; globs supported.
scripts/consensus-query.sh -a opencode-go-kimi "Q"        # one agent
scripts/consensus-query.sh -a 'opencode-go-*' "Q"          # all OC-Go models
scripts/consensus-query.sh -x codex "Q"                    # everything except codex
scripts/consensus-query.sh -a codex -a opencode-go-kimi "Q"  # composition
CONSILIUM_AGENTS='codex,opencode-go-kimi' scripts/code-review.sh file.py  # env form
```

## What it does

Four modes:

| Mode | When | Entry point | Cost (12KB file) |
|------|------|-------------|------------------|
| **Consensus query** | Open-ended problems (architecture, design, root-cause, brainstorming) — you want multiple independent takes | `scripts/consensus-query.sh` | varies |
| **Code review** | Focused review — `--mode basic` (2 specialists: security + correctness) or `--mode specialists` (adds performance + architecture + consistency = 5). Round-robin across enabled agents; caller adjudicates | `scripts/code-review.sh` | basic $0.10–0.30 · specialists $0.30–0.80 |
| **Superreview** | Multi-stage — 7 small-model passes + 2 hand-picked frontier add-ons + LLM judge filtering. Pareto sweet-spot from the bench | `scripts/superreview.sh` | $0.90–1.50 |
| **Ultrareview** | Multi-stage — 4 frontier broad passes + 15 specialists matrix + 1 probe + Opus judge with fallback. Highest severity-weighted recall in the bench | `scripts/ultrareview.sh` | $1.50–3.00 |

### Consensus query

Each agent is assigned a `role` in config:

- **analyst** — Rigorous Analyst (precision, edge cases, implementation depth). Default: Codex, Claude Opus.
- **lateral** — Lateral Thinker (cross-domain patterns, questioning premises, creative alternatives). Default: OpenCode (Gemini Pro), Gemini CLI.

Agents respond with a shared structure (Assessment / Key Findings / Blind Spots / Alternatives / Recommendation + confidence) so the caller can compare section by section.

### Code review

Two modes:

- **`--mode basic`** (default) — 2 fixed specializations: `security` + `correctness`. Empirically the highest-precision pair; readability/perf agents tend to spam nits and drag precision down.
- **`--mode specialists`** — 5 specializations: + `performance`, `architecture`, `consistency`. ~2.5× the cost; use it for high-stakes diffs (auth, money, persistence), not every PR.

Both modes run their N specialists in parallel across whichever agents are enabled (round-robin; adding a 3rd/4th enabled agent does not add a 3rd/4th pass — cost stays fixed at N specializations regardless of agent count).

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

### Multi-stage modes (superreview / ultrareview)

For higher-stakes reviews — code touching money, auth, persistence, or any path you'd otherwise pull two senior engineers off other work for — the skill ships two multi-stage pipelines ported from an internal *ultrareview-bench* (65-issue C# pilot, 9 architectures, severity-weighted scoring). Each one prescribes a fixed agent set and stage layout; configurations were tuned by marginal-uplift analysis against ground truth.

**`scripts/superreview.sh`** — small-swarm + 2 frontier add-ons. 10 LLM calls. Pareto sweet-spot — chosen by marginal-uplift analysis (the small-model base alone closed all `high`-severity issues; the 2 frontier picks were selected to add the medium-severity gaps cheapest).

```
Stage 1: discovery-small (7 parallel)    Two cheap models in a 7-pass matrix
                                         (analyst + lateral + 4 specialists)
Stage 2: discovery-frontier (2 parallel) Frontier analyst + frontier lateral,
                                         hand-picked to maximise marginal recall
Stage 3: dedup (deterministic union)
Stage 4: judge                           Sonnet-class model (default)
```

**`scripts/ultrareview.sh`** — broad-grid + specialists + probe. 21 LLM calls. Highest severity-weighted recall in the bench, lowest false-positive rate (heavier judge does the filtering).

```
Stage 1: broad (4 parallel)         4 frontier analysts of different families
                                    (analyst-roled + one lateral)
Stage 2: specialists (15 parallel)  3 small models × 5 roles
                                    (security/correctness/performance/architecture/consistency),
                                    uniform cap=10 each
Stage 3: probe (1, sequential)      Generic gap-probe — model picks the
                                    highest-risk defect class for THIS input
Stage 4: dedup
Stage 5: judge                      Opus-class judge, with a fallback to a
                                    second model if the primary times out
                                    (the bench saw Opus judges drop on
                                    200+ findings; the fallback is the
                                    production-hardened rescue path)
```

The exact model bound to each slot lives in `config.json` and the script's hardcoded agent set — see `--dry-run` or [SKILL.md → Multi-Stage Review Modes](SKILL.md#multi-stage-review-modes-superreview--ultrareview) for the current binding.

Both modes filter findings via the LLM judge before printing. Verdicts: **VALID** (kept), **DOWNGRADE** (kept, severity adjusted), **DUPLICATE** (dropped), **FALSE_POSITIVE** (dropped).

```bash
scripts/superreview.sh path/to/file.cs
scripts/superreview.sh --xml path/to/file.cs
scripts/superreview.sh --dry-run path/to/file.cs       # config + plan check, no LLM calls
scripts/ultrareview.sh path/to/file.cs
scripts/ultrareview.sh --no-fallback path/to/file.cs   # disable judge fallback (CI)
```

These modes hardcode their agent IDs. The default `config.json` already defines all of them (most are `enabled=false` — multi-stage ignores `enabled` and looks up by id directly). See [SKILL.md → Multi-Stage Review Modes](SKILL.md#multi-stage-review-modes-superreview--ultrareview) for the full schema.

## Benchmark results

We benchmarked 9 review architectures on a 65-issue C# pilot snippet. Severity weights: low=1, medium=3, high=9, critical=27 (max sev-w score = 191). Two architectures from the bench are now shipped as multi-stage modes:

| Skill mode | Architecture | Recall | Sev-weighted | Real cost | Notes |
|------------|---|---:|---:|:---|---|
| `superreview.sh` | small-swarm + 2 frontier add-ons | **67.7%** | **82.7%** | **$0.90–1.53** | Pareto sweet-spot — 96% of ultrareview's sev-w at 55% the cost |
| `ultrareview.sh` | broad-grid + specialists + probe | 72.3% | **86.4%** | $1.47–2.96 | Best sev-w + lowest FP rate (2/52 findings) |

<details>
<summary>Full bench scoreboard (9 architectures, sorted by severity-weighted recall)</summary>

The `ID` column is an internal scoreboard handle (preset name in the harness) — kept here for reproducibility, not meaningful by itself.

| ID | Architecture | Recall | Sev-w | Real cost | Notes |
|----|---|---:|---:|:---|---|
| h3 | broad-grid + specialists + probe (= **ultrareview**) | 72.3% | **86.4%** | $1.47–2.96 | best sev-w + lowest FP |
| h7 | classifier-gated adaptive pipeline | **73.8%** | 85.9% | $1.98–3.59 | highest absolute recall, expensive, not shipped |
| h9 | small-swarm + 2 frontier add-ons (= **superreview**) | 67.7% | 82.7% | $0.90–1.53 | Pareto sweet-spot |
| h1 | frontier-broad + mixed-cap specialist sweep | 69.2% | 82.2% | $2.18–4.45 | dominated by h3 on every axis |
| h4 | peer-context cross-pollination (P2) | 61.5% | 81.7% | $2.33–4.46 | P2 mechanism didn't pay off |
| h8 | small-only set-cover (no frontier) | 61.5% | 78.5% | $0.73–1.08 | cheapest, but recall capped at 61% |
| h5 | role-partition (no cross-role bleed) | 58.5% | 76.4% | $1.40–2.30 | partition cost real signal |
| h6 | frontier-broad set-cover | 55.4% | 75.4% | $1.51–2.59 | 6 frontier + 3 specialists, overfit |
| h2 | specialists-only (no broad pass) | 60.0% | 73.8% | $1.16–1.67 | narrow findings, no broad context |

Total real cost across all 9 presets: **$13.66–$24.63**. Three presets needed Opus-judge rescue (claude-code timed out at 1200s on 200+ findings; rescue via `opencode-gpt5.5-xhigh` ~$0.40–0.50). The Opus-judge fallback shipped in `ultrareview.sh` is the production-hardened version of that rescue.

</details>

### Per-reviewer contribution (averaged across the bench)

Aggregated across all 9 presets, per agent × role (MATCH = judge-confirmed match against ground truth):

| Agent | Best role | Bench appearances | Avg unique GT contributed |
|-------|-----------|------------------:|--------------------------:|
| **Claude Opus 4.7** | analyst (45× lateral) | 6 presets | 37 unique GT (analyst mode) |
| **Codex gpt-5.5 (xhigh)** | analyst + specialist hybrid | 5 presets | up to 47 MATCH per pass |
| **OC-Go DeepSeek V4 Flash** | **architecture specialist** | 9 presets | 47 unique GT (specialist 4× analyst) |
| **OC-Go Qwen 3.6 Plus** | analyst | 9 presets | 15 unique GT |
| **OpenCode Gemini 3.1 Pro** | **lateral** | 7 presets | rare but unique angles (arch/design) |
| **OC-Go Kimi K2.6** | analyst | 1 preset (evidence-thin) | 2 unique GT |

Default config roles are calibrated from this data: Opus/Codex/Qwen/Kimi/DeepSeek-Flash → `analyst`, Gemini-3.1-Pro → `lateral`. DeepSeek V4 Flash gets specialist passes (architecture/correctness) in `ultrareview.sh` because the bench showed its specialist signal dominates analyst signal 4×.

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
├── prompts/                         # Multi-stage mode prompts (superreview/ultrareview)
│   ├── broad-analyst.txt            # Rigorous-analyst broad pass
│   ├── broad-lateral.txt            # Lateral-thinker broad pass
│   ├── specialist.txt               # Parametric specialist (security/correctness/perf/arch/consistency)
│   ├── probe-generic.txt            # Generic gap-probe (model picks focus class)
│   └── judge.txt                    # Production judge (no GT — VALID/DUPLICATE/FP/DOWNGRADE)
└── scripts/
    ├── consensus-query.sh           # Parallel dispatch across enabled agents
    ├── code-review.sh               # 2-specialist code review pipeline (single-stage)
    ├── superreview.sh               # multi-stage: small-swarm + 2 frontier add-ons + sonnet judge
    ├── ultrareview.sh               # multi-stage: broad-grid + specialists + probe + opus judge (w/ fallback)
    ├── code_review_validate.py      # Parses findings, validates quoted-code, renders XML/markdown
    ├── common.sh                    # Shared role prompts, exit codes, helpers
    ├── config.sh                    # JSON config loader (Python-backed)
    ├── codex-query.sh               # Codex CLI backend
    ├── claude-query.sh              # Claude Code headless backend
    ├── opencode-query.sh            # OpenCode backend (Zen + Google direct)
    ├── gemini-query.sh              # Gemini CLI backend
    └── lib/                         # Shared building blocks for multi-stage modes
        ├── discovery-pass.sh        # One LLM discovery pass, tmp-isolated
        ├── judge-runner.sh          # LLM judge runner (no GT)
        └── dedup-findings.py        # Union per-pass XML files into one report
```

## License

MIT
