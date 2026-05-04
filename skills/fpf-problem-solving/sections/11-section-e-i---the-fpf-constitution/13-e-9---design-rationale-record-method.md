## E.9 - Design‑Rationale Record (DRR) Method

### E.9:1 - Problem frame
FPF is engineered for Pillar **P‑10 Open‑Ended Evolution**: its normative
rules must adapt as new calculi and insights arrive. But change without a
record of *why* leads to conceptual erosion and undermines auditability.
Hence FPF requires an explicit **Design‑Rationale Record (DRR)**—a
durable *conceptual artefact* that precedes every normative change.

### E.9:2 - Problem
Direct edits to the Core, absent a structured rationale, trigger three
systemic hazards:

1. **Lost provenance** – future authors cannot infer the reasoning behind
   a rule; intent decays.  
2. **Implicit assumptions** – discarded alternatives vanish from memory,
   so debates resurface and churn repeats.  
3. **Conceptual drift** – incremental tweaks slip past the Eleven Pillars
   and Principle Taxonomy lenses, blurring the framework’s foundations.

### E.9:3 - Forces

| Force | Tension |
|-------|---------|
| **Agility vs Rigour** | Evolve swiftly ↔ demonstrate deliberate, Pillar‑aligned decisions. |
| **Transparency vs Efficiency** | Provide a public argument trail ↔ avoid bureaucratic drag on minor edits. |
| **Clarity vs Conciseness** | Capture full reasoning ↔ prevent meta‑text from bloating the Core itself. |

### E.9:4 - Solution — the DRR as a structured argument
Any proposal to add, modify or deprecate a `NORM`, `A`, `D`, or `GOV`
rule **MUST** be accompanied by a **Design‑Rationale Record**. By default,
it contains exactly four conceptual components (below); a lightweight
editorial variant is permitted by CC‑DRR.5.

| Component | Guiding question | Typical content |
|-----------|------------------|-----------------|
| **Problem frame** | *Why are we talking about this?* | Problem statement, triggering insight, or external change. |
| **Decision** | *What will we do?* | Precise normative text to enter the specification. |
| **Rationale** | *Why is this the right thing?* | Comparison of alternatives, Pillar check, taxonomy‑lens balance. |
| **Consequences** | *What happens next?* | Expected benefits, trade‑offs, impacted patterns, risk notes. |

The DRR lives **outside** the normative Core. Upon acceptance, its
*Decision* **SHALL** be applied to the relevant pattern(s) as explicit
normative text (the change is "in the Core"; the DRR is not).

To preserve **P‑2 Didactic Primacy** without duplicating meta‑text,
stable and reusable parts of the DRR’s *Rationale* and *Consequences*
**SHOULD** be **distilled** into the **informative** sections of the
affected pattern(s) (Rationale, Consequences, SoTA‑Echoing, Archetypal
Grounding; per the Pattern Template, E 8). The full DRR remains
external as provenance.

### E.9:5 - Archetypal Grounding (System / Episteme)

| Holon flavour | DRR analogue | Four components illustrated |
|---------------|--------------|-----------------------------|
| **`U.System`** (physical) | Engineering Change Order for pump motor upgrade. | Context: inefficiency; Decision: switch to brushless DC; Rationale: energy gain vs cost; Consequences: new control schema + supplier change. |
| **`U.Episteme`** (knowledge) | Foundational theory revision paper. | Context: conflicting data; Decision: introduce new axiom; Rationale: explains legacy & new data, Pillar alignment; Consequences: fresh predictions, update to curricula. |

### E.9:6 - Conformance Checklist

| ID | Requirement | Purpose |
|----|-------------|---------|
| **CC‑DRR.1** | Any **semantic** change (Δ‑2/Δ‑3) to a `NORM`, `A`, `D`, or `GOV` pattern **SHALL** be preceded by an accepted DRR containing Problem‑frame (Context), Decision, Rationale, Consequences. | Prevents undocumented semantic edits. |
| **CC‑DRR.1a** | When the proposed change is expressed as a (new or revised) pattern written in the standard template (E 8), the DRR **MAY** satisfy its four components by **pointing to** the corresponding pattern sections, rather than duplicating prose. | Avoids “double writing” while keeping the argument recoverable. |
| **CC‑DRR.2** | The *Rationale* element **MUST** assess the proposal against **all Eleven Pillars** and the five Principle‑Taxonomy lenses (`Gov`, `Arch`, `Onto/Epist`, `Prag`, `Did`). | Keeps evolution aligned and cross‑disciplinary. |
| **CC‑DRR.3** | The DRR **SHALL** list every pattern it supersedes, amends, or risks impacting. | Maintains explicit impact graph. |
| **CC‑DRR.4** | Once approved, the *Decision* text **SHALL** be inserted into the Core as the normative change. Other DRR sections **MAY** be distilled into **informative** pattern sections (Rationale/Consequences/SoTA‑Echoing/Grounding) but **SHALL NOT** introduce new normative constraints except via explicit `NORM`/`A`/`D`/`GOV` text. | Preserves brevity while keeping the Core teachable. |
| **CC‑DRR.5** | Minor, non‑substantive edits (Δ‑0/Δ‑1; e.g., typos, wording clarity, didactic rearrangements) **MAY** follow a lightweight DRR variant containing Problem‑frame (Context) + Decision only (“no semantic change”), provided they do not alter semantics. | Avoids bureaucratic drag on editorial work. |
| **CC‑DRR.6 (LAT pointer)** | For Δ‑2/Δ‑3 changes to part F or part G patterns, the DRR **SHALL** include a non‑normative pointer (id/URI) to a published LEX‑AUTH Trace (LAT) archived as `U.Work`; the LAT is evidence, not normative prose. | Binds high‑impact changes to re‑runnable authoring evidence without importing tooling. |

### E.9:7 - Consequences

| Benefits | Trade‑offs / Mitigations |
|----------|-------------------------|
| **Complete audit trail** – every semantic normative change carries a structured “why”. | Adds deliberate friction; mitigated by CC‑DRR.5 (Δ‑0/Δ‑1 lightweight) and CC‑DRR.1a (pointer‑based DRRs). |
| **Higher decision quality** – Pillar & lens check surfaces hidden conflicts early. | Authors must learn taxonomy; template checklist shortens ramp‑up. |
| **Institutional memory** – prevents re‑litigation of rejected alternatives. | DRR archive grows; index stored in a non‑normative annex. |

### E.9:8 - Rationale
FPF evolves by **explicit, reviewable deltas** rather than silent edits.
The DRR is the *minimal structured argument* that keeps **P‑10
Open‑Ended Evolution** compatible with **P‑1 Cognitive Elegance** and
**P‑2 Didactic Primacy**: the Core stays succinct and teachable, while
the “why” is recoverable. Pointer‑based DRRs (CC‑DRR.1a) prevent
duplicated prose, and distillation into informative pattern sections
(CC‑DRR.4) keeps the spec itself learnable.

### E.9:9 - Relations

* **Instantiates:** P‑10 Open‑Ended Evolution, P‑2 Didactic Primacy  
* **Template governed by:** `pat:authoring/pattern‑template` (E 8)  
* **Interacts with:** `pat:guard/bias‑audit` (E 5.4) via lens check  
* **Complemented by:** `pat:authoring/code‑of‑conduct` (E 12) – etiquette for DRR debate  

### E.9:End

