# ubiquitous-language

Maintain a project thesaurus (domain glossary) following DDD ubiquitous language principles. Ensures all names in the codebase are consistent, descriptive, and aligned with the shared domain vocabulary.

## Install

```bash
npx skills add CodeAlive-AI/ai-driven-development@ubiquitous-language -g -y
```

## Quick start

After installing, try these in your project:

```
> Create a domain thesaurus for this project
> What should I call the entity that tracks user payments?
> Audit naming consistency in this codebase
```

## What it does

Three modes:

| Mode | When | What loads |
|------|------|-----------|
| **Naming consultation** | Every time the agent names anything | `SKILL.md` (389 lines) |
| **Thesaurus generation** | User asks to create/update the thesaurus | `references/generating-thesaurus.md` (416 lines) |
| **Naming audit** | User asks to check naming consistency | `references/naming-audit.md` (220 lines) |

### Naming consultation (frequent)

Before proposing any name, the agent reads the project's `THESAURUS.md` and uses the existing canonical term. If the concept is new, it tries four levers before minting a new term: Reuse, Compose, Qualify, Ask. Includes DDD naming rules for aggregates, entities, value objects, events, commands, queries, services, and repositories.

### Thesaurus generation (rare)

Scans high-signal structural files (DB schemas, API contracts, domain layer, directory structure) to extract domain terms. Separates active from legacy/obsolete terms. Collects ambiguities into an `## Unresolved` section, then surfaces them to the user for resolution. Updates agent instruction files (`CLAUDE.md`, `GEMINI.md`, etc.) so the thesaurus is used even without the skill installed.

### Naming audit (periodic)

8-check protocol: synonym violations, weasel words, technical jargon leaks, synonym drift, polysemy, translation chains, abbreviation inconsistency, orphan terms. Produces a structured report grouped by severity (Critical / Warning / Info) with recommended fix priority.

## Key features

- **Codebase is primary evidence, not automatic authority** — supports both "as-is" (document current naming) and "to-be" (define target vocabulary) modes
- **Flat-first thesaurus** — no bounded contexts by default; only introduced when polysemy is confirmed by the user with the invariant test
- **Forbidden Lexicon** — maintained list of terms banned from the domain layer (weasel words, implementation details)
- **Polysemy unpacking** — detects overloaded terms and forces disambiguation into explicit facets
- **Cross-context bridges** — when bounded contexts exist, documents the relationship and loss notes between shared terms
- **Legacy term tracking** — continuity relations (rename/split/merge/retire/deprecate) with alias parsimony
- **Framework-aware** — doesn't fight Active Record patterns; distinguishes domain noun from framework coupling
- **Language-agnostic** — works with any programming language, no framework-specific rules
- **Non-English domain support** — uses the domain's original language for canonical terms

## Sources and methodology

This skill was built through a structured research and review process:

### Primary sources

1. **Domain-Driven Design** by Eric Evans — ubiquitous language, bounded contexts, aggregate naming, anti-corruption layers
2. **Learning Domain-Driven Design** by Vlad Khononov — practical DDD patterns including brownfield adoption strategy, co-creation (not extraction) of domain language, tacit knowledge handling, translation chain anti-pattern, thesaurus scoping heuristics
3. **[First Principles Framework (FPF)](https://github.com/ailev/FPF/blob/main/FPF-Spec.md)** — formal tools for semantic precision:
   - A.1.1 `U.BoundedContext` — bounded contexts as declared semantic frames with the invariant test for justification
   - A.6.8 Service Polysemy Unpacking — "can you X it?" disambiguation tests for overloaded terms
   - A.6.9 Cross-Context Sameness Disambiguation — bridges with loss notes, direction, and relationship types
   - E.5.1 DevOps Lexical Firewall — protecting domain vocabulary from transient implementation jargon
   - F.2 Term Harvesting & Normalisation — context-local harvesting discipline
   - F.5 Naming Discipline — "name what the invariants make true", minimal generality
   - F.13 Lexical Continuity & Deprecation — five continuity relations (rename/alias/split/merge/retire)
   - F.14 Anti-Explosion Control — "four levers before minting a new name"
4. **ISO 25964 / SKOS** — thesaurus relationship types (broader, narrower, part-of, related, synonym)
5. **Martin Fowler**, **Vaughn Vernon** — bounded context maps, anti-corruption layers, context boundaries as language boundaries

### Web research

- DDD ubiquitous language best practices and common failures (synonym drift, naming chaos, acronym problems)
- Domain glossary/thesaurus management formats and standards
- DDD naming rules by construct type (aggregates, entities, value objects, events, commands)
- Naming anti-patterns in domain code (weasel words, technical jargon leaks, implementation-driven naming)
- Codebase auditing approaches for naming consistency

### Multi-agent review

The skill was reviewed by external AI agents (OpenAI Codex CLI / GPT-5.4 and Google Gemini CLI / Gemini 3.1 Pro) via the [agents-consilium](../agents-consilium/) skill for independent, unbiased assessment. The review identified 6 critical operational issues:

1. **Scanning impossibility** — original instructions assumed whole-codebase scanning; replaced with bounded high-signal hub strategy
2. **O(N^2) audit check** — field-overlap comparison replaced with grep-friendly stem+suffix heuristics
3. **External system assumptions** — translation chain check rewritten for local-only filesystem access (git log, test descriptions, local docs)
4. **Missing language idiom exceptions** — added durability boundary: DDD naming for domain-bearing identifiers, standard idioms (`err`, `ctx`, `i`) exempt
5. **Source of truth dogma** — "trust the code" replaced with "code is evidence, not authority" with explicit brownfield/legacy override
6. **Framework antagonism** — added caveat for Active Record patterns where domain and persistence are intentionally blended

### Design decisions

- **Progressive disclosure**: SKILL.md (naming consultation) loads on every trigger; references load only on demand — saves ~600 lines of context on the common path
- **Flat-first thesaurus**: bounded contexts are opt-in, not default — the agent cannot reliably determine context boundaries, so it surfaces evidence and asks the user
- **Unresolved section**: ambiguities collected during scanning, surfaced as a batch after file creation — no blocking questions during generation
- **Agent instruction updates**: after creating the thesaurus, the skill updates CLAUDE.md/GEMINI.md/etc. so the thesaurus works even without the skill installed

## File structure

```
ubiquitous-language/
├── SKILL.md                         # Naming consultation (loaded on every trigger)
├── README.md                        # This file
└── references/
    ├── generating-thesaurus.md      # Thesaurus generation workflow
    └── naming-audit.md             # 8-check naming audit protocol
```

## License

MIT
