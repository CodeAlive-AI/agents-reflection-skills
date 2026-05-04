# Remote Skill Assessment

Framework for evaluating skills from the skills.sh ecosystem before installation.

## When to Assess

Trigger assessment when ANY of these hold:

- `npx skills find` returns **3+ results** for the query
- Multiple results have **similar names** or overlapping descriptions
- User explicitly asks to **compare**, **review**, **evaluate**, or pick the **best** skill
- A single result has **suspicious metrics** (very high installs for a niche topic, or very new with very high count)

## How to Assess

1. Run `npx skills find [query]` to get candidate list
2. For each candidate, fetch its page: `https://skills.sh/<owner>/<repo>/<skill>`
3. Extract: description, weekly installs, first seen date, agent distribution, feature list
4. Apply the quality signals below
5. Rank candidates and present a verdict for each

Fetch 3-6 candidates at a time. If more than 6 results, focus on the top candidates by install count plus any that look particularly relevant by name.

## Quality Signals

| Signal | What to check | Good | Bad |
|--------|--------------|------|-----|
| **Install count** | Weekly installs relative to category | Proportional to topic popularity | Niche topic with 50K+ installs |
| **Agent distribution** | How installs spread across agents | Claude Code leads, others trail with varied counts | All agents within 5% of each other |
| **Age vs installs** | First seen date vs install count | Months old with gradual growth | Days old with thousands of installs |
| **Description** | What the skill page says it does | Specific features, technical detail | Vague marketing, buzzwords |
| **Relevance** | Match to user's actual need | Directly addresses the query | Tangentially related or different problem |
| **Overlap** | Comparison with installed skills | Fills a gap | Duplicates existing capability |
| **Source** | Repository owner/org | Known org or active developer | Unknown account, single-repo |
| **Dependencies** | External requirements | Self-contained or uses stdlib | Requires paid API keys, external services |

## Red Flags

**Inflated installs**: Agent distribution is suspiciously uniform (all agents showing near-identical counts like 88, 87, 86, 85). Organic adoption always shows uneven distribution — Claude Code typically leads with 2-5x more than other agents.

**Ad disguised as skill**: Description mentions "premium features", pricing, "subscribe", or "powered by [service]". The skill exists to funnel users to a paid product.

**External API dependency**: Requires an API key for a third-party service (e.g., Gemini, OpenAI) when the host agent could handle the task natively. A Claude Code skill shouldn't need a Gemini API key for brainstorming.

**Over-engineered workflow**: Mandates file output structures, image generation, subagent delegation, or multi-step pipelines for simple tasks. If writing a Reddit post requires saving to `reddit/<slug>/post.md` + generating an image, the skill is optimizing for demo impressions, not usability.

**Very new + very popular**: First seen within the last week but already showing thousands of installs. Legitimate viral growth is possible but rare — investigate the repo and owner.

**Fork clusters**: Same skill name appearing under 3+ different owners (e.g., `inference-sh-1/skills@X`, `inference-sh/skills@X`, `skill-zero/s@X`). Usually the same content repackaged to inflate visibility.

## Overlap Check

Before recommending a skill, check what the user already has:

```bash
python3 scripts/list_skills.py -s user
python3 scripts/list_skills.py -s project
```

If an installed skill already covers the same domain, note the overlap and assess whether the new skill adds enough value to justify installation.

## Verdicts

After assessing signals, assign one verdict per skill:

| Verdict | When to use |
|---------|-------------|
| **Recommended** | High quality, relevant, organic installs, fills a gap |
| **Consider** | Decent but has caveats: partial overlap, narrow scope, young but promising |
| **Skip** | Low quality, irrelevant, ad for paid service, suspicious metrics, or fully redundant |

## Output Format

Present results as a ranked summary:

```
## 1. skill-name (owner/repo) — Recommended
   Installs: X/week | Age: Y months
   [1-2 sentence assessment: what it does, why it fits]

## 2. skill-name (owner/repo) — Consider
   Installs: X/week | Age: Y months
   [1-2 sentence assessment: what it does, caveat]

## 3. skill-name (owner/repo) — Skip
   Installs: X/week | Age: Y months
   [1-2 sentence reason: ad, irrelevant, duplicate, suspicious]
```

After the ranked list, state a clear recommendation: which skill(s) to install, or none if nothing fits.
