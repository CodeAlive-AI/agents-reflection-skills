---
name: fpf-problem-solving
description: "First Principles Framework (FPF) — thinking amplifier. Use when user wants to think through a complex problem, architect a system, evaluate alternatives, decompose complexity, classify problems, define quality attributes, or plan rigorously. Also triggers on: FPF, bounded contexts, SoTA packs, assurance calculus, FPF Parts A-K. Not for simple task planning, general philosophy, or Agile unrelated to FPF."
license: MIT
---

# First Principles Framework (FPF)

An "Operating System for Thought" — a transdisciplinary architecture for reasoning,
written in human- and machine-readable pseudo-code. FPF turns raw intelligence (human or machine)
into organisationally usable reasoning: explicit bounded contexts, auditable artefacts, multi-view
descriptions, and disciplined hand-offs between specialised actors.

## Use cases

Use FPF whenever you need to think more rigorously than the situation's default.

- Decompose a messy, cross-domain problem into parts that can be reasoned about independently
- Make a high-stakes decision with incomplete evidence — and know what evidence is still missing
- Get a mixed team to reason together without vocabulary collisions or hidden assumptions
- Audit whether a conclusion is well-founded or just plausible
- Transfer an insight across domains without losing precision or introducing category errors
- Structure a proposal that must survive scrutiny from multiple expert perspectives
- Generate alternatives systematically instead of anchoring on the first idea
- Define what "better" means before comparing options
- Classify what kind of problem you're facing before searching for solutions
- Plan how an AI agent should select and sequence its tools under budget and trust constraints

## How to navigate

The use cases above help decide WHETHER to invoke FPF. The router below decides WHERE to go once invoked.

### Step 1 — Match the thinking need to a starting point

| What you need to do | Start here |
|---|---|
| **Decompose** a complex whole into bounded parts | 04 Kernel → A.1 Holons, A.1.1 Bounded Contexts, A.14 Mereology |
| **Assign** roles and responsibilities | 04 Kernel → A.2 Roles, A.15 Role-Method-Work Alignment |
| **Set boundaries** on what statements mean | 05 Signature Stack → classify as definitions, gates, duties, or evidence |
| **Prevent category errors** (role vs. function, method vs. work) | 06 Constitutional Principles → A.7 Strict Distinction |
| **Evaluate confidence** in a claim or artifact | 07 Part B → B.3 Trust & Assurance; 08 Part C → C.2 F-G-R scoring |
| **Compose** parts into wholes preserving properties | 07 Part B → B.1 Gamma algebra; 08 Part C → C.13 Compose-CAL, C.20 Discipline-CAL |
| **Reason through** a problem systematically | 07 Part B → B.5 Reasoning Cycle, B.5.2 Abductive Loop |
| **Generate alternatives** / explore solution space | 08 Part C → C.18 NQD Open-Ended Search, C.19 Explore-Exploit |
| **Measure and compare** options rigorously | 06 A.V → A.17-A.19 Characteristics, CSLC & SelectorMechanism; 08 Part C → C.16 MM-CHR |
| **Score knowledge** quality (formality, scope, reliability) | 08 Part C → C.2 KD-CAL, C.2.2 Reliability, C.2.3 Formality |
| **Resolve conflicts** across stakeholders or values | 09 Part D → Ethics & Conflict |
| **Unify vocabulary** across teams or domains | 13 F.I Context of Meaning → 14-15 UTS tables → 20 Lexical Debt |
| **Document** for multiple audiences | 11 E-I Constitution → E.17 Multi-View Publication Kit |
| **Sharpen expression** — repair vague wording, surface ambiguity | 11 E-I → E.17.SD.SPR Surface Precision Restoration, E.17.SD.OOTD Object-of-Talk Discipline, E.17.EFP Explanation Faithfulness; 05 A.IV.A → A.6.H Wholeness Unpacking |
| **Survey a discipline** and build a reusable toolkit | 16 Part G → SoTA Packs, TraditionCards, OperatorCards; 08 Part C → C.21 Discipline-CHR (field health & maturity) |
| **Classify** a problem type before solving | 08 Part C → C.22 Problem-CHR, C.3 Kind-CAL (typed reasoning) |
| **Define quality** attributes ("-ilities") as structured bundles | 08 Part C → C.25 Q-Bundle; 06 A.V → A.17-A.19 Characteristics |
| **Orchestrate** agentic tool use under budgets and trust gates | 08 Part C → C.24 Agent-Tools-CAL |
| **Trace provenance** of a claim | 06 A.V → A.10 Evidence Graph; 16 Part G → G.6 Provenance Ledger |

For complex problems, follow paths across multiple sections — the router shows where to start, not where to stop.

### Step 2 — Read the _index.md, then the sub-section

1. Open the `_index.md` of the target section folder — it lists all sub-sections with line counts and descriptions.
2. Read only the specific sub-section file you need.
3. Do NOT load entire sections. Pick the narrowest file that serves the user's question.

### Step 3 — Apply in plain language

Use plain language for the user. Introduce FPF-internal names (U.Holon, Gamma, F-G-R)
only when they add precision the user needs.

### Step 4 — Compose findings across sections

When a problem draws from multiple sections:

1. State each pattern's contribution in one line (e.g., "Bounded Contexts gives us the parts; Trust Calculus scores our confidence in each").
2. If patterns from different sections appear to conflict, check for category errors via A.7 Strict Distinction — the conflict is usually a level confusion (role vs. function, method vs. work), not a real contradiction.
3. Synthesize in natural order: decomposition first (what are the parts?), then evaluation (how confident are we?), then resolution (what do we do about gaps?).
4. Do not just list FPF patterns — weave them into a coherent answer to the user's actual question.

## Starter prompt (example — adapt to the user's actual role and need)

> You have the FPF specification loaded.
> Help me structure my project / problem / programme.
> Use plain language for an engineer-manager.
> Propose: (1) bounded contexts / specialisations, (2) decision criteria, (3) key alternatives,
> (4) hand-offs, and (5) missing evidence or tests before commitment.
> Introduce internal FPF names only when they add precision.

## Section INDEX

Structural reference. Each entry is a folder — read its `_index.md` first, then pick the sub-section.

| # | Section | Sub | When to use |
|---|---------|:---:|-------------|
| 01 | [Title page](sections/01-first-principles-framework-core-conceptual-specification/_index.md) | 0 | Authorship, version date, top-level identity. |
| 02 | [Table of Content](sections/02-table-of-content/_index.md) | 0 | Navigate the spec, locate a pattern, trace inter-section dependencies. |
| 03 | [Preface](sections/03-preface/_index.md) | 17 | **Onboard**: reading paths by role, FPF philosophy, purpose and non-goals. |
| 04 | [Part A — Kernel](sections/04-part-a-kernel-architecture-cluster/_index.md) | 19 | **Decompose and assign**: holons, bounded contexts, roles, transformers, method/work separation. |
| 05 | [A.IV.A — Signatures](sections/05-cluster-a-iv-a---signature-stack-boundary-discipline/_index.md) | 20 | **Set boundaries**: classify statements as definitions, gates, duties, or evidence. |
| 06 | [A.V — Principles](sections/06-cluster-a-v---constitutional-principles-of-the-kernel/_index.md) | 29 | **Prevent confusion**: category errors, measuring, comparing, evidence graphs, mechanism suite, flow constraints, gate profiles. |
| 07 | [Part B — Reasoning](sections/07-part-b-trans-disciplinary-reasoning-cluster/_index.md) | 24 | **Compose and evaluate**: aggregation (Gamma), trust scores, emergence, reasoning cycles. |
| 08 | [Part C — Extensions](sections/08-part-c-kernel-extensions-specifications/_index.md) | 30 | **Score and search**: epistemic quality (F-G-R), kinds, measurement, open-ended search, problem typing, discipline composition, agentic tool-use, quality bundles. |
| 09 | [Part D — Ethics](sections/09-part-d-multi-scale-ethics-conflict-optimisation/_index.md) | 1 | **Resolve conflicts**: ethical trade-offs, bias auditing, safety overrides. |
| 10 | [Part E — Constitution](sections/10-part-e---fpf-constitution-and-authoring-cluster/_index.md) | 0 | Entry point for Part E subsections. |
| 11 | [E-I — Constitution](sections/11-section-e-i---the-fpf-constitution/_index.md) | 33 | **Govern and publish**: 11 Pillars, guard-rails, multi-view publication (MVPK), surface discipline, comparative reading, transduction graph, pattern quality gates. |
| 12 | [Part F — Unification](sections/12-part-f-the-unification-suite-concept-sets-sensecells-contextual-role-a/_index.md) | 0 | Entry point for Part F subsections. |
| 13 | [F.I — Meaning](sections/13-cluster-f-i-context-of-meaning-raw-material/_index.md) | 19 | **Align vocabulary**: semantic drift, homonym collisions, Alignment Bridges. |
| 14 | [UTS Layout A](sections/14-block-fpf-u-type-unified-tech-name-unified-plain-name-plain-twin-gover/_index.md) | 0 | **Map concepts** across standards (BPMN, PROV-O, ITIL). |
| 15 | [UTS Layout B](sections/15-block-base-concept-scale-map/_index.md) | 1 | **Map concepts** across disciplines (operations, physics, math). |
| 16 | [Part G — SoTA Kit](sections/16-part-g-discipline-sota-patterns-kit/_index.md) | 15 | **Harvest disciplines**: SoTA Packs, TraditionCards, OperatorCards, benchmarks. |
| 17 | [Part H — Glossary](sections/17-part-h-glossary-definitional-pattern-index/_index.md) | 0 | **Look up terms**: canonical definitions, four-register naming, cross-references. |
| 18 | [Part I — Annexes](sections/18-part-i-annexes-extended-tutorials/_index.md) | 0 | Walkthroughs, change log, external standards mappings. |
| 19 | [Part J — Indexes](sections/19-part-j-indexes-navigation-aids/_index.md) | 0 | Concept-to-pattern, pattern-to-example, principle-trace indexes. |
| 20 | [Part K — Lexical Debt](sections/20-part-k-lexical-debt/_index.md) | 2 | **Fix terminology**: mandatory replacements and migration debt. |
