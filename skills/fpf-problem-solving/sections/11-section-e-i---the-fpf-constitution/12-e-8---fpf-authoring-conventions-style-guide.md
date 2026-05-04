## E.8 - FPF Authoring Conventions & Style Guide

> **Type:** Architectural (A)  
> **Status:** Stable  
> **Normativity:** Normative (unless explicitly marked informative)

### E.8:1 - Problem frame
FPF grows through the addition of patterns written by authors from many
disciplines. Without a shared structure *and* voice, the framework would
fracture, violating Pillars **P‑1 Cognitive Elegance** and
**P‑2 Didactic Primacy**.

### E.8:2 - Problem
*Structural drift* and *stylistic fragmentation* threaten three qualities:

1. **Comparability** – readers cannot align patterns lacking common
   headings.  
2. **Narrative cohesion** – prose swings from dry jargon to informal
   blog style.  
3. **Auditability** – missing sections hide safety checks
   (Archetypal Grounding, Bias‑Annotation).

### E.8:3 - Forces

| Force | Tension |
|-------|---------|
| **Uniformity vs Expressiveness** | Consistent template ↔ freedom for diverse domains. |
| **Rigor vs Readability** | Formal precision ↔ engaging prose. |
| **Brevity vs Completeness** | Concise patterns ↔ mandated safety subsections. |

### E.8:4 - Solution — One template, enriched by style principles

#### E.8:4.1 - Canonical Pattern Template
Within each pattern, the **canonical** section headings **SHALL** appear in the order below.
For each **canonical content section heading (1–12)**, the `<Title>` component (after the heading separator, e.g. ` - `) **MUST** start with the canonical section title (case-insensitive match; canonical capitalisation preferred); an optional clarifier after an em dash is allowed (e.g., `Solution — …`).
The **Footer marker** (section **13**, if present) is a sentinel and is governed by **H‑9** rather than the standard `<FullId> - <Title>` shape.

**Extensibility.**
Authors **MAY** add additional sections. Prefer expressing them as subsections under the nearest canonical section (e.g., `4.1`, `4.1.1` under *Solution*). If an additional top-level section is necessary, it **MUST NOT** delete or reorder the canonical sections and its title **MUST NOT** shadow a canonical title.

**Mandatory vs optional.**
* Canonical sections **1–13** are mandatory in every pattern.
* The escape hatch `Not applicable` is permitted **only** where explicitly stated below; when used, it **MUST** include a short justification (1 paragraph).

**Template:**
- **Title line:** Hashes + FullId + ` - ` + Pattern Title; optional `(informative)` note.
- **Header block:** Type, Status; optional Normativity override.
1. **Problem frame**
2. **Problem**
3. **Forces**
4. **Solution**
5. **Archetypal Grounding** (Tell–Show–Show; System / Episteme; `Not applicable` allowed only with justification)
6. **Bias‑Annotation**
7. **Conformance Checklist**
8. **Common Anti‑Patterns and How to Avoid Them** (`Not applicable` allowed only with justification)
9. **Consequences**
10. **Rationale**
11. **SoTA‑Echoing** (post‑2015 practice alignment; terminology drift & deltas; `Not applicable` allowed only with justification)
12. **Relations**
13. **Footer marker** 

**Footer marker.** End each pattern with a single visible sentinel heading line on its own: `### <PatternId>:End`. This makes truncation detectable even when HTML comments are stripped or surfaced by editors. The footer marker is intentionally content‑free: **do not** place prose under it.

*Note.* Pattern boundaries are still parseable by scanning for the next pattern heading (`## …`), but an explicit `:End` marker helps retrieval pipelines (and LLM prompts) distinguish “this chunk is the whole pattern” from “this chunk was cut mid‑pattern”.

##### E.8:4.1.1 - Heading & ID discipline (human tooling + retrieval)
FPF is often consumed through full‑text search and retrieval (RAG). A reader or an LLM may see a subsection without its parent headings, so headings must be **self‑identifying**.

**H‑1 (Heading shape).** Every pattern heading and every subsection heading inside a pattern **SHALL** follow:
`<hashes> <FullId> - <Title> (optional note of non‑normativity)`

*Exception.* The **Footer marker** is a sentinel heading and is governed by **H‑9**, not by the standard `<FullId> - <Title>` shape.

**H‑2 (Heading separator).** The canonical separator between `<FullId>` and `<Title>` is ` - ` (ASCII, space-hyphen-space).
Legacy text may use ` - `; tooling **SHOULD** treat the two as equivalent, and authors **SHOULD** migrate to ` - ` when touching a heading.

**H‑3 (FullId).** `FullId` is the full hierarchical address.
For a **pattern heading** it is the pattern ID (e.g., `A.2`, `E.10.D1`).
For **headings inside a pattern**, append dot‑separated ordinal section numbers after the colon (`:`) (e.g., `A.2:4.4`, `E.10.D2:3`).
*Exception:* the Footer marker uses the reserved sentinel token `:End` as defined in **H‑9**.
The colon (`:`) is **reserved** for section paths and **MUST NOT** appear in pattern IDs.

**H‑4 (Ordinals).** Ordinals in section paths **SHOULD** track the canonical template numbering (**1 = Problem frame**, …, **13 = Footer marker**) to maximise cross‑pattern comparability. During refactors or in legacy patterns, ordinals **MAY** be local. In that case, the **canonical section title at the start of `<Title>`** is the semantic key; readers and tools **MUST NOT** infer section semantics from the ordinal alone.
*Note:* the Footer marker itself is exempt from ordinal encoding; it uses the reserved token `:End` (see **H‑9**).

**H‑5 (Where kind and normativity live).** Pattern **kind** (e.g., Architectural / Definitional) **MUST** be declared in the **Header block**, not encoded into the heading text. Normativity (**normative** / **informative**) **MUST** also live in the Header block when it deviates from the default. If a reminder is needed for readers, authors **MAY** add a short parenthetical note at the end of the heading (e.g., `(informative)` / `(non‑normative)`), but headings **MUST NOT** use square‑bracket tags.

**H‑6 (Heading levels).** Heading levels **MUST** preserve a fixed offset between structural layers (Part or Cluster (flat) → Pattern → Pattern sections):
* Part and Cluster headings **MUST** use `#` (level 1) across the file.
* A Pattern heading **MUST** use `##` (level 2).
* Inside a pattern, each nested section **MUST** add exactly one `#` per level (e.g., `## A.2 - …`, `### A.2:2 - …`, `#### A.2:2.1 - …`).

**H‑7 (Ellipsis discipline).** Authors **MUST NOT** use **three consecutive full stops/dots** (`...`) as punctuation in headings or narrative prose. Authors **MUST** use the Unicode ellipsis `…` (U+2026) instead. For editorial elisions in quotations, authors **SHOULD** prefer `[…]` to make the omission explicit and distinguish it from retrieval truncation.
*Exception:* literal three‑dot sequences that are part of an external language’s syntax **MAY** appear **only inside code spans or fenced code blocks**.

**H‑8 (Normative keywords).** The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as described in RFC 2119, as clarified by RFC 8174 (only when capitalised). Authors **SHOULD** avoid informal deontic phrasing (“need to”, “is required to”) in normative clauses.

**Deontics vs admissibility.** Use RFC keywords only for **deontic obligations** (requirements on authors, reviewers, implementers/tooling, or published artefacts) — i.e., things an agent can choose to do or omit. Do **not** use RFC keywords to state **definitions**, **structural invariants**, **typing rules**, or other **admissibility conditions** of the modeled world.

When you need an enforceable constraint that is *mathematical* rather than *deontic*, express it as a non‑deontic predicate using one of: `Definition:`, `Invariant:`, or `Well‑formedness constraint:` (optionally with formal quantifiers). Prefer mathematical terms like `cardinality 1..1 (total)` / `0..1 (partial)` / `0..n` over deontic adjectives like “mandatory/optional” when the intent is cardinality, not duty.

**Admissibility predicate discipline (recommended shape).**
When expressing admissibility/validity constraints as predicates (`Definition:` / `Invariant:` / `Well‑formedness constraint:`):
* Authors **MUST NOT** use RFC keywords inside the predicate block.
* Authors **SHOULD** give each predicate a stable identifier and short name (e.g., `RA‑1 (Locality)`, `RE‑3 (Method gate)`), so that Conformance Checklist items can reference it without re‑authoring the rule.
* Authors **SHOULD** write the constraint as a declarative predicate (optionally quantified), e.g., `role ∈ Roles(context)`, rather than as “X MUST …”.
* If the constraint needs to be enforceable as part of a pattern’s contract, authors **SHOULD** reference the predicate identifier from the Conformance Checklist (and/or call out validator behaviour), rather than duplicating the predicate with RFC keywords.

**H‑9 (Footer marker sentinel).** Footer marker **SHALL** be a single heading line whose `FullId` is the pattern ID followed by the reserved sentinel token `:End` (no ordinals, no title, no square‑bracket tags): 
`### <PatternId>:End`
It is the only allowed heading *inside* a pattern whose section token is non‑numeric. It **MUST** be the final line of the pattern and **MUST NOT** carry any prose. Tooling and readers **MUST** treat it as a boundary sentinel, not as a semantic section.

*Unification note:* historic A‑ and D‑templates differed only by the presence/absence of **Bias‑Annotation** and **Relations**; the unified template keeps the headings everywhere while allowing explicit `Not applicable` statements when justified.
The Alexandrian pattern canon historically calls *Problem frame* “Context”. FPF avoids that label because **Context** is already overloaded in FPF (e.g., `U.BoundedContext` and its Plain‑register label).

#### E.8:4.2 - Stylistic Principles (S-0 ... S-19)

| # | Principle | Guideline |
|---|-----------|-----------|
| S-0 | Narrative Flow Seven-Step Heuristic | Authors are encouraged to structure major paragraphs or subsections using the seven-step mnemonic. |
| S-1 | Density without Jargon | Short declarative sentences; tool names belong in Pedagogy/Tooling. |
| S-2 | Internal Cohesion | Inline references to Pillars and related patterns. |
| S-3 | Embedded Mini-Definitions | Gloss a new term in parentheses on first appearance. |
| S-4 | Contextualisation | Brief historical or disciplinary lineage anchors. |
| S-5 | Prophylactic Clarification | Pre-empt common misreadings inside the prose. |
| S-6 | Quotable Closers | Finish Solution or Consequences with a memorable aphorism. |
| S-7 | Generative over Prescriptive | Present rules as enabling constraints, not bureaucracy. |
| S-8 | Trans-disciplinary Tie-ins | Illustrate using at least two distinct fields. |
| S-9 | Physical Grounding Reference | Link abstractions to a `Transformer` or physical process. |
| S-10 | Punchy Blocks | <= 5 sentences per paragraph; lists for clarity. |
| S-11 | Narrative Flow | Ensure sections read as a continuous story, not bullet soup. |
| S-12 | Full sentences over tags | Avoid “keyword soup”. Each list item SHOULD contain a subject and a verb; prefer 2-4 sentence micro-paragraphs to bare tag lists. |
| S-13 | SoTA-Echo craft | In the SoTA-Echoing section, present: **claim -> practice -> source -> alignment -> adoption status (adopt/adapt/reject)**; cite Bridges & CL when crossing Contexts/planes. |
| S-14 | Surface sufficiency | New and substantially revised patterns carry enough second/third-surface content to be teachable without nearby project notes. |
| S-15 | Worked slices over scenario labels | Transform-like families show at least one concrete source/result slice; scenario names alone are not enough. |
| S-16 | Ordinary vs load-bearing realism | Keep ordinary use light, and make heavier review records explicit only for disputed, high-risk, or higher-impact cases. |
| S-17 | Self-contained monolith prose | A merged pattern must explain itself inside the monolith; planning shorthand and review-context dependencies are not admissible in live prose. |
| S-18 | Reader-role discipline | Keep live pattern prose addressed to the intended FPF user; move package-development and architecture-placement rationale to separate companion notes or clearly marked informative placement notes. |
| S-19 | Precision before relaxation | In load-bearing prose, restore the head kind named by a generic phrase before treating any qualifier as trustworthy semantic guidance; then restore the burden hidden in the qualifier before allowing any later plain, didactic, or coarsened restatement. |

Authors use the principles as a *scaffold*, not a straitjacket: the goal
is coherent, engaging insight.

**S-0 (Narrative Flow Seven-Step Heuristic) — explanation**
Narrative flow is recommended to follow these steps: **Hook -> Frame -> Weave -> Anchor -> Bridge -> Flow -> Close**.

Brief explanations:
| Step       | Purpose in a paragraph/section                             |
| ---------- | ---------------------------------------------------------- |
| **Hook**   | Grab attention with a vivid image or paradox.              |
| **Frame**  | State the specific question or problem space.              |
| **Weave**  | Connect to earlier patterns or Pillars.                    |
| **Anchor** | Tie to a concrete System/Episteme or physical process.     |
| **Bridge** | Show the implication for the upcoming claim or rule.       |
| **Flow**   | Deliver the formal content or argument.                    |
| **Close**  | End with a quotable line or payoff that reinforces memory. |

Narrative Flow Heuristic also operationalises S-1 (Density w/o Jargon), S-2 (Internal Cohesion), S-4 (Contextualisation), and S-6 (Quotable Closers).
#### E.8:4.2.1 - Recognition surface and assurance surface
Every canonical pattern SHALL stabilise one governed object early enough that a cold reader can tell what kind of thing the pattern is actually governing. If ordinary forms vary (`note`, `sheet`, `guided UI`, `rendering`, `review aid`), the text must make explicit which of those are merely surface forms of one governed object and which would instead name a different act, process, work-product, or owner lane. Recognition and assurance surfaces may refine that object differently, but they must not silently swap the central object kind.

If a pattern uses a broad umbrella or head together with a narrower operative branch, the text must also make the stack explicit early enough for first reading: what the broad head names, what the current narrowed branch is, what governed object is actually in play, what move is being carried by that object, and what wider work or process remains outside the pattern. A qualifier alone does not restore that stack.

Under `F.18` local-first naming, the canonical pair here is **recognition surface** and **assurance surface**.
The earlier provisional `recognition shell / assurance shell` wording is retired.
These names refer to two reading-order surfaces inside one pattern; they do **not** mint new owner kinds, new publication-surface kinds, or a second face family.
A later third didactic support surface remains optional and is justified only when the family is especially easy to misuse, easy to over-read, or hard to teach without extra scaffolding.

The **recognition surface** is the first reading surface.
It is the part of the pattern that lets a cold working reader recognise the situation quickly enough to decide whether to keep reading.
It should start from a subject-domain or practice moment before internal taxonomy whenever the pattern is meant to help real work rather than only internal canon maintenance.
In practice it usually lives in an early `Use this when` line or equivalent opening, plus the upper parts of `Problem frame`, `Problem`, `Solution`, `Consequences`, and nearby worked slices.
Its job is to make visible:
- what ordinary working situation this pattern is for;
- what goes wrong if the pattern is missed;
- what the pattern buys the reader in practice;
- when this is not the right pattern;
- what governed object is actually being kept stable;
- and, when technical terms must appear early, a pairwise plain gloss for each early high-pressure term.

The **assurance surface** is the second reading surface.
It carries the heavier load-bearing material that makes the pattern reviewable and auditable:
- declaration blocks and typed fields when those are part of the contract;
- representation ontology or object-of-talk discipline;
- any minimal modeling or mathematical lens that keeps the governed object stable;
- law, invariants, admissibility, and reroute or neighbouring-owner conditions;
- `SoTA-Echoing` when it is carrying live explanatory load;
- and the review hooks that let a stronger reading be checked explicitly.

The assurance surface may sharpen, justify, and discipline the recognition surface.
It must **not** silently replace, strengthen, or universalize the claim that the recognition surface made visible.
If the recognition surface says “this pattern helps with a bounded working situation”, the assurance surface must not quietly turn that into a stronger owner, stronger guarantee, or broader universality claim.

If a pattern claims **universal** or **transdisciplinary** status, that claim must already be visible in the recognition surface.
It is not enough for universality to appear only later in a law sheet, declaration block, or `SoTA-Echoing` rationale.
A broad claim should therefore be demonstrated in the recognition surface through at least **three heterogeneous reader or domain situations**.
When a compact matrix helps, `F.16` is the preferred template for showing that breadth.
If `SoTA-Echoing` is load-bearing, the practical implication of those rows should be recoverable from the recognition surface and case bank rather than remaining a late-only justification layer.

A **third didactic support surface** means enough didactic and operational support that the pattern survives without nearby project documents. Typical signs include:
- at least one concrete source/result slice in Archetypal Grounding when the pattern governs transforms or publication change;
- at least one boundary-heavy example or anti-example when nearby owners are easy to confuse;
- reviewer guidance that tells what to inspect first and what failure mode forces reroute;
- local mini-definitions or glossary support for recurring terms that would otherwise be recovered only from project context.

Pattern density is therefore not “more metadata” and not “longer tag lists”. It is the presence of enough recognition, assurance, and, when needed, extra didactic support that a reader can understand the pattern, apply it lightly in ordinary cases, and recognise when a heavier review path is required.
#### E.8:4.2.2 - Package-form and host-relation role-word discipline

FPF pattern prose is not free-form descriptive English. When authors name a *package-form* or a *host relation*, they must use role words with stable semantic intent.

Use the following distinctions explicitly:

This is a cross-cutting review discipline, not a replacement for local host lexica. For example, `A.6.7` / `A.19.CHR` already carry the suite/kit/pack distinction, and `E.17.1` already carries the viewpoint bundle/family/library distinction.
- **owner** = the pattern that owns the primary semantic law surface for the family;
- **specialization** = a named refinement under an existing owner;
- **overlay** = a cross-cutting governance or reading layer over existing owners;
- **profile** = a declarative review/use surface derived from a host owner rather than a replacement owner;
- **family** = a recurring class of cases governed by one owner surface;
- **bundle** = a packaged set of defaults, allowances, or coordinated members;
- **cluster** = a navigation or reading grouping; not by itself an owner claim;
- **suite** = a coordinated set of members with explicit suite semantics under the right host law;
- **pack** = an editorial or review grouping, not automatically a semantic owner;
- **kit** = a reusable coordinated publication or contract surface with kit-level semantics under the right host law;
- **record** = a case/report/review artefact;
- **umbrella** = a provisional or review-stage head spanning possible subfamilies before final owner freeze.

These words are not interchangeable. In particular, authors must not let `cluster`, `bundle`, `suite`, `family`, `profile`, `overlay`, or `umbrella` do the work of an unnamed host relation. When the host relation matters, it must be stated directly: `specialization under ...`, `hosted profile under ...`, `overlay over ...`, `bundle under ...`, or another equally explicit formulation.

A pattern may reuse a host-native role word when that role is already owned and defined by the host pattern. Outside that case, authors must not improvise near-synonyms or shift between role words for stylistic variety.

#### E.8:4.2.3 - Reader-role discipline for live pattern prose

A live pattern is written for its intended FPF user: the person who will use the pattern to organise thought, inspect a case, publish a note, or review a result under that pattern.
Its load-bearing sections therefore explain what the pattern lets that user do, what it forbids, what it costs, and how it relates to neighbouring patterns in user terms.

Authors must keep FPF-development or package-architecture material separate from that user-facing body.
In particular, `Problem`, `Solution`, `Consequences`, `Rationale`, worked slices, and ordinary-vs-load-bearing guidance must not do the work of:
- arguing that the material is worth isolating;
- justifying overlay/profile/owner choice as a package decision;
- discussing owner freeze, naming freeze, merge posture, blast radius, or safest landing form;
- or narrating future package promotion or defer decisions.

If architecture-placement commentary is still helpful, the default home is a separate companion note or ADR-like architecture surface.
A live pattern may include a short optional informative subsection such as `Architectural placement note (informative)` only when that placement materially helps users avoid misuse; even then, it must stay clearly separated from the user-facing solution and rationale rather than replacing them.

#### E.8:4.2.4 - Human-facing fit beyond surface correctness
Human-facing fit is also subject-domain fit. A recognition surface that starts from internal taxonomy, owner-lane convenience, or package-architecture wording before the problem-owning domain moment is still under-authored even if its later law surface is correct. When a broader umbrella name and a narrower operative branch are both live, the first surface should also tell the reader which stack is actually active rather than leaving that reconstruction to a later declaration block or companion note.

A pattern can already be surface-clean, boundary-clean, and reader-role-clean, yet still fail the first minute of use for a cold working reader.
That failure usually appears when the text is lawful but does not yet make the working situation, practical payoff, governed object, or first reading surface visible enough.

For canonical patterns, the first reading surface should behave as a **recognition surface** and the heavier burden should remain in an **assurance surface**.
When a pattern claims practice guidance or is meant to be used by engineers, managers, researchers, or other working readers, authors should make the following visible before the heavier harness takes over:
- a recognisable `Use this when` or equivalent first-minute entry;
- a concrete working situation in `Problem frame`, not only taxonomic or owner-lane language;
- a short statement of what goes wrong if the pattern is missed or misread;
- a short statement of what this pattern buys the reader in practice;
- a short `Not this pattern when` boundary for the ordinary nearby misroutes;
- one minimally viable worked case or use slice that shows what changes in practice;
- when a typed declaration block, formal lens, or other compact modeling support is load-bearing, a short user-facing statement of what kind of object the pattern is governing and what minimal lens keeps that object reviewable;
- pairwise plain glosses for any high-pressure technical terms that must appear before the heavier declaration surface arrives;
- when `SoTA-Echoing` is carrying live explanatory load, a short working-reader implication for each row or cluster of rows and a visible link back to the case bank or worked slices that those rows discipline;
- a visible split between the recognition surface and the heavier declaration / review / assurance surface;
- and, if the draft implicitly serves several reader families, an explicit primary working reader, primary concern surface, or primary viewpoint.

If the pattern claims broad, universal, or transdisciplinary usefulness, that breadth should already be visible in the recognition surface.
At minimum the recognition surface should show at least three heterogeneous reader or domain situations rather than one narrow lane with a later broad claim attached.
When a compact matrix helps, `F.16` is the preferred template for making that breadth legible.

This is not a request to flatten the pattern into plain language only.
It is a rule about ordering, layering, and surface consistency: the recognition surface must help a working reader recognise the pattern early, while the assurance surface continues to carry the full semantic burden.
If the pattern uses technical lexicon, ontological distinctions, or a mathematical lens, those supports must remain recoverable, but the first reading surface should not require the reader to decode that full stack before recognising the working situation.
The assurance surface may tighten or discipline the recognition surface; it must not silently shift what the recognition surface claimed.
If a pattern or example claims **autonomy** for any Role/Method/Service:
1) Add a subsection **“Autonomy (RoC‑E.16)”** that lists:
   * `AutonomyBudgetDeclRef` (id, version, Scope (G), Γ_time),
   * `Aut-Guard policy-id (PolicyIdRef)`,
   * `OverrideProtocolRef` (SpeechAct names, SoD),
   * pointer to where **Green‑Gate** applies in the Method steps,
   * where **AutonomyLedgerEntry** is recorded on `U.Work`.
2) Include one **Tell‑Show‑Show** vignette that demonstrates **depletion** and **override** handling.
3) Use **LEX‑BUNDLE** terms (Scope (G), Γ_time, Role/Method/Work). Avoid “validity”, “process”, “actor”, “system”, “mechanism” unless mapped to kernel types.

### E.8:5 - Archetypal Grounding (System / Episteme)

| Template element | `U.System` illustration | `U.Episteme` illustration |
|------------------|------------------------|---------------------------|
| Section order | Pump‑assembly pattern follows sections **1–12** (and, optionally, **13**). | Meta‑analysis pattern follows the same sections. |
| S‑1 Density w/o Jargon | “The pump boundary is the sealing plane.” | “This episteme raises **F (Formality)** by making falsifiers testable.” |
| Hook‑Weave‑Anchor | Opens with field anecdote → weaves in Γ‑core → anchors to motor torque. | Opens with historical paradox → weaves in **A.10** anchors → anchors to peer‑review data. |

*Note:* Prefer examples that reuse FPF’s own characteristics vocabulary (e.g., **F (Formality)** rather than “F‑score”) unless you explicitly mean an external metric and name it as such.

### E.8:6 - Bias‑Annotation
Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Universal** for the authoring conventions in this pattern.
This guidance biases toward **Did** (readability, narrative flow) and **Arch** (template regularity) by design; the mitigation is explicit optionality (`Not applicable`) and the requirement to justify omissions in‑text.

### E.8:7 - Conformance Checklist

**CC style (canonical).**
Conformance Checklist items are obligations/conditions in the **authoring plane**: they constrain artefacts that claim conformance (and the reviewers/validators that accept them). A CC clause of the form “X SHALL ...” is to be read as “In a conforming artefact, X SHALL ...”, not as a deontic statement about the modeled world.

**Preferred wording for new or edited CC items:** start with an explicit conformance subject (e.g., “Authors ...”, “Reviewers ...”, “A conforming implementation ...”, “A validator ...”). If a CC item is enforcing an admissibility predicate, it **SHOULD** cite the predicate’s identifier (from a `Definition:` / `Invariant:` / `Well-formedness constraint:` block) rather than restating the predicate as “X MUST ...”. For boundary/interface/protocol/contract patterns, prefer A.6.B-routed claim IDs (L/A/D/E) or cite an existing Claim Register (A.6.B:7) instead of restating mixed prose.

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC-SG.0 (Heading discipline).** | Pattern and subsection headings **SHALL** follow **H-1 ... H-9** (FullId prefix, reserved punctuation, heading levels, ellipsis discipline). The Footer marker **SHALL** follow **H-9**. | Makes chunks self-contained; reduces ambiguity between author elision and retrieval truncation. |
| **CC-SG.1** | Every new pattern **SHALL** follow the section order defined in the Canonical Template (Title block -> ... -> Footer marker). | Guarantees structural comparability. |
| **CC-SG.2 (Grounding required).** | Every pattern **MUST** include an *Archetypal Grounding* section. If **System** or **Episteme** grounding is inapplicable, authors **MUST** state `Not applicable` and give a one-paragraph justification. | Keeps patterns teachable and reduces “definition-only” ambiguity. |
| **CC-SG.3** | The *Bias-Annotation* section **SHALL** cite the five Principle-Taxonomy lenses and declare either “Universal” or an explicit scope limitation. | Keeps cross-disciplinary neutrality explicit (ties to Guard-Rail 4). |
| **CC-SG.4** | Deontic normative sentences **MUST** use only RFC-style keywords (see **H-8**); RFC keywords **MUST NOT** appear inside `Definition:`/`Invariant:`/`Well-formedness constraint:` blocks. When enforceable, admissibility/validity predicates **SHOULD** be referenced by id from the Conformance Checklist (rather than duplicated as “X MUST ...”). Informal deontic verbs are prohibited in normative clauses. | Prevents ambiguity between obligation language and model validity; improves auditability. |
| **CC-SG.5** | Pattern prose **SHOULD** demonstrate adherence to Style Principles **S-0 ... S-19**; reviewers are empowered to request revision when clarity or didactic quality suffers. | Embeds common narrative voice without rigid policing. |
| **CC-SG.6 (SoTA-Echo required).** | Every pattern **SHALL** include a **SoTA-Echoing** section and clearly state divergence of its Solution from SoTA with explanation of why. Architectural patterns **SHALL** satisfy the full obligations below; Definitional patterns **MAY** satisfy the reduced obligations (terminology drift + >= 1 post-2015 primary source) when a full SoTA comparison is not meaningful. | Ensures explicit lineage and guards against vocabulary drift. |
| **CC-SG.7 (Post-2015, multi-Tradition).** | For Architectural patterns, SoTA-Echoing **SHALL** cite >= 3 post-2015 sources across >= 2 Traditions; each item **MUST** carry adoption status (adopt/adapt/reject) with reason. | Guards against monoculture; makes intent explicit. |
| **CC-SG.8 (Bridge & CL on reuse).** | Any cross-Context or plane reuse mentioned in SoTA-Echoing **MUST** cite **Bridge id + CL** and (if planes differ) **Φ(CL)**/**Φ_plane** policy-ids; penalties **-> R_eff** only. | Safe, auditable reuse. |
| **CC-SG.9 (Lexical hygiene).** | The term **mapping** **SHALL NOT** appear in SoTA-Echoing except in the precise E.10 sense; use **alignment/Bridge/relation** instead. | Avoids overloading reserved vocabulary. |
| **CC-SG.10 (No keyword soup).** | SoTA-Echoing items **MUST** be written as sentences (not bare noun phrases); bullet lists are acceptable only with complete clauses. | Improves didactic quality and comparability. |
| **CC-SG.11 (Anti-patterns).** | Every pattern **SHALL** include a **Common Anti-Patterns and How to Avoid Them** section. It **MAY** be `Not applicable` only with a one-paragraph justification. | Makes misuse paths explicit and reduces review churn. |
| **CC-SG.12 (Boundary routing).** | If a pattern’s subject is a boundary/interface/protocol/contract (API boundary, protocol, connector, “contract” description, or a published boundary surface), it **MUST** either (a) provide an **A.6.B**-routed atomic claim set (`L-*`/`A-*`/`D-*`/`E-*`, with stable IDs), or (b) explicitly cite an existing **A.6.B Claim Register** / routed claim set that it reuses. | Pulls A.6.B into the authoring contour, prevents “contract soup”, and makes review more explicit and repeatable. |
| **CC-SG.13 (Didactic sufficiency).** | New patterns and substantial revisions **MUST** remain understandable without project-planning notes. When a pattern introduces a new named family/profile/specialization, or adds a non-trivial host-derived note, its Solution and Grounding **SHALL** carry enough second/third-surface content: explicit host relation, ordinary-vs-load-bearing guidance, at least one concrete source/result slice where applicable, and visible reroute cues. | Prevents skeleton-only patterns and project-context leakage. |
| **CC-SG.14 (Controlled prose, not free shorthand).** | Load-bearing prose **SHALL NOT** rely on bare relation words or planning shorthand whose host relation is left implicit (e.g., bare “species”, “branch”, “flow”, or API-like “input/output” language). When a host relation matters, authors **MUST** name it explicitly (`specialization under ...`, `hosted profile under ...`, `overlay over ...`, etc.). | Keeps pattern prose precise and self-identifying. |
| **CC-SG.15 (Package-form and host-relation role-word discipline).** | When a pattern names a package-form or the host relation of a family (`owner`, `specialization`, `profile`, `overlay`, `family`, `bundle`, `cluster`, `suite`, `pack`, `kit`, `record`, `umbrella`), the chosen role word **MUST** match the intended ontology and **MUST NOT** be swapped for stylistic variety or left to implication. | Prevents semantic blur in pattern prose and keeps host relations auditable. |
| **CC-SG.16 (Reader-role discipline).** | Authors **MUST** keep live pattern sections user-facing. FPF-development or package-architecture reasoning about isolation, overlay or owner choice, freeze, merge posture, or planned evolution **MUST NOT** occupy `Problem`, `Solution`, `Consequences`, `Rationale`, or worked slices; if such material is still needed, it **MUST** live in a separate companion note or a clearly marked informative placement note. | Keeps pattern prose aligned with its intended reader and prevents package-governance leakage into live use guidance. |
| **CC-SG.17 (Recognition surface and assurance surface).** | Admission or substantial revision runs **MUST** check that a canonical pattern exposes a recognition surface early enough for the intended working reader and an assurance surface that carries declaration, law, modeling, and review burden without silently shifting the recognition-surface claim. The recognition surface **MUST** surface a recognisable working situation, what goes wrong if the pattern is missed, what the pattern buys, and a clear ordinary `not this pattern when` boundary. Any load-bearing typed declaration or modeling lens **MUST** be surfaced by a short user-facing statement of the governed object, early high-pressure technical terms **MUST** receive nearby pairwise plain glosses, and any `SoTA-Echoing` used as live explanatory support **MUST** state a short practitioner or manager implication plus visible linkage to the worked cases or boundary slices it disciplines. If the pattern claims universal or transdisciplinary reach, the recognition surface **MUST** demonstrate that claim through at least three heterogeneous reader or domain situations, preferably using an `F.16`-style example matrix or an equally explicit alternative. | Prevents surface-clean but reader-opaque patterns and keeps broad claims visible where cold readers actually enter the text. |
| **CC-SG.18 (Precision before relaxation).** | In load-bearing prose, authors **MUST NOT** leave a generic head noun or burden-carrying qualifier uninterpreted when that phrase carries semantic, boundary, or authority load. A narrowing qualifier by itself does **not** restore the head kind. Authors **MUST** restore head kind first, then qualifier burden, then any comparison/escalation axis before stronger use. If a later Plain, didactic, or coarsened rendering is kept, the more precise upstream reading **MUST** remain recoverable. | Prevents ambiguity from being hidden inside ordinary-looking phrases and keeps softened prose subordinate to an explicit authoritative reading. |

### E.8:8 - Common Anti-Patterns and How to Avoid Them

These failure modes recur in drafts and in downstream application. They are predictable ways the Forces in this pattern get violated.

| Anti-pattern | Symptom | Why it fails (force violated) | How to avoid / repair |
|-------------|---------|------------------------------|-----------------------|
| **Template cargo-culting** | Headings exist, but each section is a thin bullet list with no narrative. | Satisfies Uniformity but loses Readability and Didactic Primacy. | Use S-0 narrative flow per section; write 2-4 sentence micro-paragraphs before any list/table. |
| **Un-grounded abstractions** | Problem/Solution stay abstract; no concrete System/Episteme Tell-Show-Show. | Breaks teachability and makes misuse likely. | Fill Archetypal Grounding first; then back-propagate concrete nouns into Problem/Forces/Solution. |
| **SoTA name-dropping** | SoTA-Echoing is a list of nouns/buzzwords with no adopt/adapt/reject rationale. | Violates CC-SG.7 and CC-SG.10; readers cannot audit alignment. | For each source, state what is adopted/adapted/rejected and why (complete clauses, 2-4 sentences). |
| **Tool-bound normativity** | A vendor tool, file format, or schema is described as required to apply the pattern. Data governance implied. | Violates Guard-Rails (lexical firewall; notation independence, data governance absence); reduces portability and conceptual clarity. | Keep normative content conceptual; move tooling and data governance into Context-local Profiles. |
| **Hidden trade-offs** | Solution sounds universally good; Consequences lists only benefits. | Removes decision-support value; applicability cannot be judged. | In Consequences, include at least one trade-off and a mitigation; if none exists, explain why. |
| **Skeleton-only pattern** | The template is present, but the pattern gives only one compressed definition block and scenario labels. | Passes form while failing didactic sufficiency. | Add second/third-surface content: local decomposition, concrete slices, reviewer cues, and reroute guidance. |
| **Project-context leakage** | A reader needs architecture memos or planning notes to understand the pattern. | The monolith stops being self-sufficient. | Move the essential problem framing, worked slices, and rationale into the pattern itself; keep project reviews informative only. |
| **Generic-head underspecification** | A load-bearing phrase uses a generic head such as `note`, `view`, `guidance`, `output`, or `artifact`, but the text never restores what kind of thing that phrase names. | The reader cannot tell what ontology the sentence is actually governing. | Restore the head kind first in host-local terms before any stronger claim or comparison is made. |
| **Qualifier-smuggled burden** | A modifier such as `comparative`, `safe`, `interactive`, `reliable`, or `faithful` is doing the semantic work while the text leaves its burden implicit. | The sentence sounds precise without actually stating its comparison basis, relation burden, or stronger-use boundary. | Unpack the qualifier into explicit burden, criteria, or reroute language rather than relying on the modifier alone. |
| **Mixed comparison axis** | One sentence compares or ranks artifact-like, process-like, authority-like, or owner-like things on one axis. | The sentence becomes ontologically incoherent even if each local noun sounds plausible. | First restore head kind, then qualifier burden, then rewrite the comparison through a homogeneous burden/threshold/handoff axis. |
| **Implicit relation shorthand** | Words like “species”, “branch”, or process metaphors do the semantic work without naming the actual host relation. | Readers infer the wrong ontology or workflow. | State the host relation explicitly and remove shorthand that only makes sense inside project discussions. |
| **Package-form and host-relation drift** | Words like `bundle`, `cluster`, `profile`, `overlay`, `family`, `suite`, or `kit` are swapped as if they were stylistic variants. | Readers cannot tell whether the text is naming an owner, a navigation grouping, a review surface, or a packaged set of defaults. | Pick one role word by ontology, keep the host relation explicit, and do not vary the noun unless the ontology really changes. |
| **Reader-role leakage** | Live sections start telling the reader why the pattern was isolated, what landing form is safest, or why freeze/merge is premature. | The pattern stops teaching the user and starts narrating FPF-development decisions. | Move package-development reasoning to companion notes; keep live sections about lawful use, costs, boundaries, and reroutes for the intended user. |
| **Role-clean but pragmatically foggy** | The pattern addresses the right reader in principle, but a cold practitioner still cannot recognise the working situation, practical payoff, governed object, first useful move, or project-level implication of the `SoTA-Echoing` early enough. | The text passes role hygiene but still fails `E.12`/`E.13`/`E.14` as a working artifact. | Bring a manager-first or practitioner-first entry higher, add one minimally viable worked case, state what changes in practice, surface the governed object and any minimal modeling lens in plain user-facing prose, add plain glosses for early high-pressure terms, and keep `SoTA-Echoing` tied to visible practitioner or manager implications plus nearby case linkage rather than lineage alone. |
| **Hybrid audience blob** | One main narrative tries to serve engineers, managers, auditors, architects, and researchers at once with no primary working reader or concern surface. | The text becomes globally polite but locally blurry; no reader knows which concern governs the first surface. | Make the primary working reader / concern / viewpoint explicit and route other audiences into secondary support, other faces, or an explicit out-of-scope note. |

### E.8:9 - Consequences

| Benefits | Trade‑offs / Mitigations |
|----------|-------------------------|
| **Predictable skeleton** – readers instantly know where to find context, forces, and criteria. | Limits author freedom in macro layout; mitigated by flexibility inside the Solution subsection. |
| **Cohesive voice** – S‑principles give FPF a recognisable style, aiding memorability. | Reviewers must read for style, not only semantics; checklists ease load. |
| **Embedded pedagogy** – Tell‑Show‑Show and Hook → Close heuristics turn the spec into a self‑teaching text. | Slightly longer patterns; justified by better comprehension and fewer clarifying DRRs. |

### E.8:10 - Rationale
Structure and style function as FPF’s *grammar*. By unifying what were
once separate “template” and “style guide” patterns, authors face a
single reference point that satisfies:

* **P‑1 Cognitive Elegance** – uniform, minimal surprises.  
* **P‑2 Didactic Primacy** – narrative flow, dual archetype examples.  
* Guard‑Rails 1 & 2 – no tool jargon, no notation lock‑in inside prose.

A unified template also improves retrieval: a chunk containing `A.2:<n> - Bias‑Annotation` remains self‑identifying even when parent headings are missing, and the recommended footer marker makes truncation detectable.

International and industry standards often speak in terms of *conformance criteria*. FPF uses the label **Conformance Checklist** to make adoption easier for engineers and managers.

### E.8:11 - SoTA‑Echoing  *(normative; lineage & deltas to contemporary State‑of‑the‑Art)*

**Purpose.** Make each pattern’s relationship to contemporary best-known practice explicit and comparable without importing tooling or data governance. This section is prose‑first and notation‑independent. It does not mint an independent second rule layer, but it is a load-bearing alignment surface: the Solution, Conformance Checklist, Relations, and other load-bearing sections must reflect the stance stated here or explicitly justify divergence.

**Minimum contents (obligations).**
1) **Evidence binding (no duplicate SoTA).** If a **SoTA Synthesis Pack** exists (G.2), this section **SHALL cite** its **ClaimSheet IDs** / **CorpusLedger entries** / **BridgeMatrix rows** as the source‑of‑truth for claims and report `adopt/adapt/reject` **consistent with those IDs**. Avoid forking an untracked SoTA narrative.
2) **Sources (post‑2015).** For **Architectural patterns**, cite ≥ 3 primary SoTA sources (standards/papers/books), with at least **two independent Traditions**. For **Definitional patterns**, cite ≥ 1 post‑2015 primary source and, where relevant, a short note on terminology drift/deprecations.
3) **Best-known, not merely popular.** Authors **SHALL** distinguish best-known currently defensible practice from merely widespread or fashionable defaults. If the pattern adopts, adapts, or rejects a popular-but-weaker practice, that divergence **MUST** be stated explicitly.
4) **Practice alignment.** For each cited item, state **what is adopted/adapted/rejected** and **why** (2–4 sentences).
5) **Scale legality.** If numeric operations are implied, bind to ComparatorSet/CG‑Spec and declare partial‑order stance (no hidden scalarisation).
6) **Cross‑Context reuse.** Any reuse across `U.BoundedContext` must surface Bridge+CL/Φ_plane policy‑ids (penalties affect only `R_eff`).
7) **Lexical hygiene.** Avoid “mapping” unless you mean an explicit Bridge/translation relation with loss notes.

**Writing guidance (readability).**
*Write short paragraphs, not tag lists.* For each Tradition, provide (a) a one‑sentence capsule of the practice, (b) a one‑sentence comparison to the pattern’s Solution, (c) a one‑sentence adoption status with reason. Where helpful, add one **System** and one **Episteme** micro‑example (Tell–Show–Show).

**Format: human‑first.** A small table is allowed, but each row **MUST** be accompanied by 1–2 sentences as above. Vendor/tool tokens, file formats, or data schemas are out of scope.

#### E.8:11.1 - SoTA alignment for this pattern (E.8 self‑echo)

| Claim (E.8 need) | SoTA practice (post‑2015) | Primary source (post‑2015) | Alignment with E.8 | Adoption status |
|---|---|---|---|---|
| Pattern texts must be teachable, not just “correct”. | Use a stable skeleton (context/problem/forces/solution/actions/consequences) plus illustration and checklists to keep patterns readable and actionable. | Iba (2021), “How to Write Patterns …” (PLoP 2021 PLoPourri). | Canonical Template mirrors the skeleton and adds Archetypal Grounding + Conformance Checklist as first‑class sections. | **Adopt/Adapt.** Adopt the skeleton; adapt by making bias and conformance explicit sections. |
| Pattern quality needs explicit validation beyond folklore. | Critique of ad‑hoc validation (incl. “rule of three”) and push toward more rigorous discovery/validation methods. | Riehle et al. (2020), “Pattern Discovery and Validation Using Scientific Research Methods”. | E.8 encodes validation as Conformance Checklist + SoTA‑Echoing with adoption status and evidence binding. | **Adopt.** Adopt auditability goals; keep the mechanism lightweight (checklists + evidence binding). |
| Governance should constrain structure, not mandate tools. | Specify conformance and structure; do not prescribe processes, notations, tools, or recording media. | ISO/IEC/IEEE 42010:2022 (architecture description). | E.8 is template‑ and conformance‑centric, with guard‑rails against tool/notation lock‑in in core narrative. | **Adopt.** Direct alignment. |
| Pattern languages are networks; visuals often mislead. | Systematic surveys report low consensus on what to visualise and ambiguous/inexpressive visuals; relations need clear definition in text. | Quirino, Barcellos, Falbo (2018), survey of visual notations for software pattern languages (SBES 2018). | E.8 requires a Relations section and keeps diagrams optional, placing primacy on textual structure and explicit links. | **Adapt.** Use the finding as rationale for text‑first, relation‑explicit authoring. |

### E.8:12 - Relations

* **Builds on:** E.6, E.7  
* **Constrained by:** Guard‑Rails E.5.1–E.5.4 (lexical firewall, notation independence, etc.)  
* **Constrains:** All patterns; the DRR template references the same section order.  

### E.8:End

