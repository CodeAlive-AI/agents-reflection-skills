## B.3.5 - Working-Model Relations & Grounding (CT2R-LOG)

> **One‑line summary.**
> CT2R‑LOG treats the everyday **Working‑Model relations**— **ut:ComponentOf**, **ut:MemberOf**, **ut:PortionOf**, **ut:AspectOf** —as the **publication surface** for structure, while binding each published edge to a **grounding trace** and a **declared `tv:validationMode`**. Authors keep using a short list of relations; reviewers get reconstructible provenance.

### B.3.5:1 - Intent

*Provide a single, human‑facing family of **Working‑Model** relations as the **publication surface**, with explicit hooks for (G) grounding and (R) reliability—without exposing constructor jargon or burdening day‑to‑day authors.*

**What you get (manager/engineer view).**
 The same relations you already know (e.g., **ComponentOf**) remain the **public interface**.

**What changes (auditor/ontologist view).**
* Each published edge carries two additional commitments:

  1. **`tv:groundedBy`** → points to a **reconstructible trace** (e.g., `Γ_m.sum`) whenever the edge is *structural*.
  2. **`validationMode ∈ {axiomatic, inferential, postulate}`** → declares how the author justifies the assertion.

This is the **alias‑plus‑grounding** split: **Compose‑CAL** builds the trace; **CT2R‑LOG** declares the alias pattern and links it; **Lang‑CHR** supplies the labels.

### B.3.5:2 - Problem frame & forces (why this pattern exists)

* **Two audiences, one dial.** Project managers want **one relation family** and stable views; ontologists want **generative completeness** and extensional identity.
* **Parsimony constraint.** The Kernel stays minimal; construction is **outside** the Kernel.
* **Unification inside FPF.** We already unify external vocabularies; the same discipline is applied **internally** so *every* pattern that needs mereology rides on **one generative basis** and **one alias façade**.


### B.3.5:3 - Problem

Declared sub‑relations of `ut:PartOf` (e.g., **ComponentOf**, **MemberOf**) are easy to use but **not self‑justifying**: nothing in their declaration shows *why* a given edge should be trusted, or how to **re‑derive** it if challenged. Conversely, exposing constructor traces everywhere makes the graph unreadable to non‑specialists.

**We need**: a stable **publication surface** for relations *and* a mandatory, **reconstructible** **grounding channel**—plus a visible **validation intent** that downstream assurance can reason about.


### B.3.5:4 - Solution (thumbnail)

CT2R‑LOG introduces a **two‑link discipline** around each canonical edge:

1. **Alias link (concept‑level).**
   **Working‑Model relations** (e.g., `ut:ComponentOf`) are **alias patterns** over a general constructional principle. Denote by **`tv:AliasOf`**.

2. **Grounding link (evidence‑level).**
   Each **edge instance** carries **`tv:groundedBy`**:

   * **MANDATORY** for **all structural edges** (sub-properties of `ut:StructPartOf`): the target is a valid **`Γ_m` trace** from **Compose-CAL** (one of `sum`, `set`, `slice`). **Set** `validationMode=axiomatic`; **`postulate` SHALL NOT be used for structural edges**.
   * **Optional** for **epistemic edges** (e.g., `ConstituentOf`, `RepresentationOf`): if no `Γ_m` trace is appropriate, attach an **evidence object** whose admissibility is governed by the declared **`validationMode ∈ {inferential, postulate}`** (assurance rules).

2. **Validation flag (author intent).**
   Every declared edge or aggregation rule carries **`tv:validationMode`** with one of:
   * **`postulate`** — pragmatic working claim backed by observations;
   * **`inferential`** — reasoned consequence (proof outline);
   * **`axiomatic`** — constructive grounding via a `Γ_m.*` composition.

> **F–G–R alignment.**
> **F** (the published *Fact*): `:PumpA ut:ComponentOf :Skid12`.
> **G** (its *Grounding*): `:e123 tv:groundedBy :trace_Γm_sum_456`.
> **R** (declared *Reliability mode*): `tv:validationMode=axiomatic` → inputs B.3.3’s **AssuranceLevel** assessment.

### B.3.5:5 - Vocabulary & notation (normative)

* **Working-Model relations (front‑stage).**
 `ut:ComponentOf`, `ut:PortionOf`, `ut:AspectOf` are **publication-grade** sub-properties of `ut:StructPartOf` **(structural)**; `ut:MemberOf` is a sub-property of `ut:EpiPartOf` **(epistemic)**. 

* **Alias principle (lexical).**
  `tv:AliasOf` links a **relation type** to its **generative rule schema** (e.g., “`ComponentOf` aliases the result of a `Γ_m.sum` with role=component”).

* **Grounding (per‑edge).**
 `tv:groundedBy` on an *edge instance* **MUST** point to a **Γₘ trace** (`sum|set|slice`) for **structural** edges (**set** `validationMode=axiomatic`); for **epistemic** edges it **MAY** point to an **evidence object** or a logical proof per declared `validationMode ∈ {inferential, postulate}`. 

* **Trace family.**
  `Γ_m.sum`, `Γ_m.set`, `Γ_m.slice` are the only normative constructors for structural grounding; no temporal or workflow constructor is added here (time slices live in Sys‑CAL; parallelism via `set`).

* **Validation flag.**
 `tv:validationMode ∈ {postulate, inferential, axiomatic}` is **required** on every declared edge or aggregation rule; **for structural edges `postulate` is disallowed**.

### B.3.5:6 - Running example (didactic)

> **Story.** A refinery team publishes `:PumpA ut:ComponentOf :Skid12`.

* **Publication — Working-Model surface.**
  They mint one edge with the **Working-Model** relation **ComponentOf** and **declare the surface’s `U.Formality`** (typically **F≈F3**, controlled narrative). Only the publication surface is visible to readers.

* **Constructive grounding (Γₘ).**
  In the background, the edge node records `tv:groundedBy :trace_Γₘ_sum_456`. That trace is a **Compose-CAL** “sum” that lists the parts aggregated into the skid. Any auditor can **replay** the trace to prove extensional identity. *(Grounding does not change the surface’s F; it sets `validationMode=axiomatic` and contributes to **R** in the **VA** lane.)*

* **Assurance stance & R-lane.**
 Because the edge is construction-backed, authors set `tv:validationMode=axiomatic`. B.3.3 reads the flag and assigns an **AssuranceLevel** in the appropriate **R** lane (scale defined in B.3.3). **F**, **G**, and **R** remain **orthogonal**: this move raises assurance without changing claim scope (**G**) or the surface’s formality (**F**).

* **Contrast (epistemic).**
When the same team asserts `:MassFlowRepresentation RepresentationOf :FlowModel`, they declare `validationMode=postulate` and attach a calibration dataset (Empirical Validation) instead of a **Γₘ** trace. The edge remains publishable, but reviewers record a lower-confidence stance, and B.3.4’s **evidence ageing** policy will decay its trust over time.
  
Result: **one** visible relation for engineers, **two** hidden anchors for assurance.

### B.3.5:7 - Author Standard (at a glance)

When you add or import a relation edge:

1. **Pick a Working‑Model relation** (ComponentOf/MemberOf/…); avoid raw `ut:PartOf` unless you are drafting meta‑level axioms.
   
2. **Attach `tv:groundedBy`**:

   * Structural? → **must** be a `Γ_m` trace ID.
   * Epistemic? → `Γ_m` trace *or* evidence object.
3. **Declare `tv:validationMode`** (**postulate** / **inferential** / **axiomatic**).

> **What managers see:** nothing new in the graph picture.
> **What auditors get:** a reliable trail from every published edge back to a principled constructor or an evidence pack.


### B.3.5:8 - Compatibility & cross‑references

* **B.3.2 (LOG‑use).** CT2R‑LOG supplies the **places to hang proofs/evidence** that B.3.2 formalizes.
* **B.3.3 (Assurance levels).** `validationMode` + presence/quality of `tv:groundedBy` are the **inputs** to compute `AssuranceLevel (L0–L2)`.
* **B.3.4 (Evidence ageing).** If an edge relies on **postulated evidence**, its confidence **decays** per that pattern until refreshed; **axiomatic** edges from `Γ_m` traces do not age, but their **inputs** (tokens) might.

### B.3.5:9 - Rule‑set — CT2R‑LOG (conceptual, human‑first)

**Intent (one line).** Make **Working‑Model** relations the canonical interface for authors, while providing a **clean, optional bridge** to formal assurance by way of *aliasing* and *grounding* semantics.

#### B.3.5:9.1 - Vocabulary & Roles (what the words mean in this pattern)

* **Working‑Model relation.** A human‑oriented statement an engineer would naturally write, using U.Type relations such as `ut:ComponentOf`, `ut:PortionOf`, `ut:AspectOf`, `ut:MemberOf`. This is the **canonical publication surface** for structure for readers and reviewers in Part B. (Didactic primacy governs this choice.)

* **Assurance Layer.** Three complementary kinds of support an author MAY attach:

  * **Constructive** grounding: a *generative* narrative that reconstructs the relation via the three mereological aggregators (`Γ_m.sum | Γ_m.set | Γ_m.slice`) from **Compose‑CAL**. (No formal notation is required in this pattern—only a reconstructible *story of construction*.)
  * **Logical** grounding: a *reasoned* chain (think KD‑CAL style arguments) that shows why the relation follows from stated premises.
  * **Mapping** grounding: a *type/lexical alignment* that shows the domain label truly denotes the intended U.Type relation (Kind-CAL / Lang‑CHR stance).
    These three kinds of support are *complementary*, not exclusive.

* **Empirical Validation.** How a published relation meets reality (observations, calibration scenarios). It lives beside, not inside, the relation. (See B.3 family.)

* **Grounding vocabulary (`tv:`).**

  * `tv:AliasOf` — declares that a Working‑Model relation is the **canonical projection** of a more general pattern (its “principle of use”).
  * `tv:groundedBy` — points to the **author’s grounding narrative** (Constructive, Logical, or Mapping, as applicable).
    The `tv:` namespace is part of the Core conceptual lexicon; it is **notation‑agnostic** and **tool‑agnostic**.

* **`tv:validationMode ∈ {postulate, inferential, axiomatic}`.** A **declaration by the author** of the *confidence stance* for a relation instance:
  *postulate* — a pragmatic working claim;
  *inferential* — a reasoned consequence;
  *axiomatic* — a constructively grounded identity (mereological extensionality is exhibited). (Modes align with the B.3 cluster’s trust model.) 

> **Authoring note.** This pattern defines *meanings*, not formats. The words above SHALL be used consistently and without reference to any specific notations or execution environments (Guard‑Rails: Notational Independence).


#### B.3.5:9.2 - Normative rules (MUST/SHALL clauses for thinking‑and‑writing)

**S‑1 (Working-Model first).**
Authors **SHALL** publish structural claims in the **Working‑Model** form (`ut:*Of` relations). This is the canonical interface for human readers and cross‑disciplinary teams. Formal reconstructions are **optional** and live in the Assurance Layer.

**S‑2 (Alias declaration).**
If a Working‑Model relation follows a known general principle, the author **SHOULD** declare `tv:AliasOf <Principle>`, thereby making the intended *use‑pattern* explicit for reviewers and future readers. (This improves comparability without introducing extra formality.)

**S‑3 (Grounding by mode).**
For every relation instance the author **MUST** set `validationMode` and follow the corresponding grounding stance:

* **S‑3.a `postulate`.** The author **MAY** omit `Γ_m` grounding; the relation stands as a pragmatic working claim within a stated scope. The author **SHOULD** supply brief empirical cues (where the claim tends to hold) to ease later validation. (Empirical Validation is tracked in B.3.)

* **S‑3.b `inferential`.** The author **SHALL** outline a *reasoned chain* (plain‑language steps) that makes the relation a consequence of previously admitted statements. No formal calculus is required in this pattern; the outline must be sufficient for a peer to follow. (Think KD‑CAL stance, conceptually.)

* **S‑3.c `axiomatic`.** The author **SHALL** provide a *constructive grounding narrative* that reconstructs the relation as a `Γ_m.sum | Γ_m.set | Γ_m.slice` composition and **SHALL** link it with `tv:groundedBy`. The narrative **MUST** be reconstructible by a competent peer *without introducing new primitives* (parsimony). (Compose‑CAL’s three aggregators are the only constructive moves assumed here.)

* **S-3.d Structural constraint.** For **structural** edges, `tv:groundedBy → Γ_m.*` is **REQUIRED regardless of `validationMode`**; the `postulate` mode **MUST NOT** be used for structural mereology. 

**S-4 (Relation-kind sense-making).**
* For **structural** subtypes of `ut:StructPartOf` (Component/Portion/Aspect), constructive grounding (`tv:groundedBy → Γ_m.*`) is **REQUIRED** in all modes; **`postulate` MUST NOT be used** for structural mereology (see S-3.d).

* For **epistemic/constitutive** links (e.g., representation, usage), constructive grounding is **OPTIONAL** in all stances; authors prefer *inferential* or *postulate* with empirical cues.

**S‑5 (Order and time are not mereology).**
Authors **SHALL NOT** encode execution order, parallelism, or temporal slicing as part‑whole. Such concerns belong to `Γ_method` and `Γ_time` families and **SHOULD** appear as method/time statements adjacent to, not inside, Working‑Model structure. (This prevents conceptual leakage between planes.)

**S‑6 (Unidirectional dependence).**
CT2R‑LOG may *consume* Compose‑CAL and KD‑CAL conceptually; it **SHALL NOT** redefine them. Meaning flows **downward only** (Kernel → Extention → Context → Instance).

**S‑7 (Register discipline).**
When naming principles in `tv:AliasOf`, authors **SHOULD** use Tech/Plain *twin labels* where available and obey minimal‑generality and rewrite rules (LEX‑BUNDLE), so that aliases are recognisable across context of meaning.

**S‑8 (No tool talk).**
Core prose **MUST NOT** introduce CI/CD terms, file formats, APIs, or machine‑oriented notations in place of concepts. If examples are needed, they **MAY** be plain‑language narratives or domain vignettes. (This pattern is conceptual by Standard.)


#### B.3.5:9.3 - Scope & Non‑Goals (to keep the plane clean)

* **In scope.**
  Canonical publication of relations for humans; alias‑to‑principle clarity; conceptual grounding stories; author‑declared *validationMode*; separation of structure vs order/time.

* **Out of scope.**
  Any machinery that *executes* checks; any binding to specific notations; any process/workflow mechanics; any discussion of file formats. (Those belong to Tooling/Pedagogy artefacts and SHALL NOT be imported by the Conceptual Core.)
  
* **Edge placements.**
  When a claim is chiefly about *naming fit* across Contexts, prefer **Mapping** grounding (Kind-CAL/Lang‑CHR stance). When it is chiefly about *why* it follows, prefer **Logical** grounding. When it is about *what the whole is, from its parts*, prefer **Constructive** grounding. (Authors MAY combine them.)


#### B.3.5:9.4 - Author’s working moves (micro‑playbook, notation‑free)

**M‑1.** State the relation in **Working‑Model** form (e.g., “Impeller `ComponentOf` Pump”).
**M‑2.** Pick `validationMode`:

* If you’re sketching and exploring → choose **postulate**; add one‑sentence scope.
* If you’re justifying from known statements → choose **inferential**; list the 2–4 steps in plain language.
* If you require extensional identity → choose **axiomatic**; narrate the `Γ_m.*` reconstruction in a short paragraph.

**M‑3.** Add `tv:AliasOf` to the principle you intend readers to recognise (e.g., “Component = sum of parts”).
**M‑4.** Keep *order/time* adjacent, not embedded: if you need “assembled in two parallel lines”, write that as a **method/time** statement next to the structure, not as a part‑of edge.
**M‑5.** Stop when the *reader can follow without guessing*. This is the stopping rule for Quarter 2: clarity before formality. (Didactic primacy.)

### B.3.5:10 - Bias‑Annotation (auditable, human‑first)

The purpose of this section is to make **typical cognitive slips** visible and name the **counter‑moves** an author (or reviewer) should apply **in thought**—not with tools. These biases are generic; the remedies point to earlier FPF guard‑rails and neighbouring patterns.

| Bias (name)                     | Symptom in the model                                                                                                          | Cognitive counter‑move (conceptual only)                                                                                                                                                                          | Where to check                                                       |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Formalism capture**           | Treating a constructive trace as “the real thing” and the human relation (e.g., *ComponentOf*) as an optional label.          | Re‑assert **canonical‑first**: the Working‑Model relation is the canonical publication. A constructive trace is a **grounding** you may attach when assurance demands it. Choose a **validationMode** explicitly. | CC‑CT2R‑1, CC‑CT2R‑2; B.3 skeleton for assurance conservatism.       |
| **Canonical inversion**         | Demanding a constructive grounding for **epistemic** claims by default. *(For **structural** claims, Constructive grounding is mandatory; epistemic remains progressive.)*                    | Keep **progressive assurance**: declare `validationMode ∈ {postulate, inferential, axiomatic}`; reserve *axiomatic* with **Constructive** grounding for structural; use **Logical/Mapping**/**Empirical** where appropriate. Express formality via **F** (C.2.3), not tiers. | CC-CT2R-2; B.3.3 relation-kind discipline & validation modes.         |
| **Order/time leakage**          | Encoding sequence or phase as part‑whole edges.                                                                               | Apply **Strict Distinction**: order/time belong to Γ\_method / Γ\_time, not to mereology or CT2R relations.                                                                                                       | B.3 “keep order/time in their own lanes”; cross‑ref Γ\_ctx/Γ\_time.  |
| **Notation lock‑in**            | Letting a diagram or syntax define the meaning (“it’s true because the diagram says so”).                                     | Enforce **Notational Independence**: meaning is defined in prose/maths; renderings are illustrative only.                                                                                                         | Part E guard‑rail on notational independence.                        |
| **Congruence blindness**        | Composing strong parts through weak mappings without acknowledging the fit penalty.                                           | Make **edge‑fit first‑class**: reason about Congruence Level (CL) on connections; penalise low fit conceptually.                                                                                                  | B.3 universal aggregation skeleton (Φ(CL)); anti‑patterns list.      |
| **Collection/composition swap** | Using **MemberOf** to stand in for **PartOf** (or vice versa), then carrying over reliability as if it were a structural sum. | Re‑separate **MemberOf** (collections) from **part‑whole** mereology; read A.14 notes in Γ\_epist context.                                                                                                        | Γ\_epist context / A.14 compliance.                                  |
| **Design/run chimera**          | Mixing design‑time and run‑time evidence into one “assurance” line.                                                           | Split the **scope** of the claim: `S ∈ {design, run}`; compare side‑by‑side rather than merging.                                                                                                                  | B.3 typed claim tuple & anti‑pattern “design/run chimera”.           |

> **Reviewer reminder.** Bias audit is a **reading aid**. It never licenses tooling talk in Core; use the guard‑rails in Part E to keep semantics primacy and unidirectional dependence of layers.


### B.3.5:11 - Conformance Checklist (normative, author‑facing)

The following obligations regulate **how to think and write** CT2R content. They are **notation‑agnostic** and purely conceptual.

| ID                                              | Requirement                                                                                                                                                                                                                                   | Purpose                                                                   |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **CC‑CT2R‑1 (Canonical‑first).**                | A relation published for readers **SHALL** be stated in Working‑Model terms (`ut:*Of`) as the canonical form; any constructive or logical basis is recorded as **grounding** (not as the definition).                                         | Preserve human‑first canon and didactic primacy.                          |
| **CC‑CT2R‑2 (Mode declaration).**               | For every declarative relation or rule, the author **SHALL** declare `tv:validationMode ∈ {postulate, inferential, axiomatic}` in prose (no silent defaults).                                                                                | Make assurance intent explicit and auditable by reading.                  |
| **CC‑CT2R‑3 (Structural axiomatic grounding).** | If the relation is **structural** (a subtype of `ut:StructPartOf`) **and** the author chooses `axiomatic`, they **SHALL** provide a **grounding narrative** that can be reconstructed as one of the Γ\_m aggregators (*sum*, *set*, *slice*). | Tie high‑assurance claims to constructive identity without tool mandates. |
| **CC‑CT2R‑4 (No order/time in parts).**         | Authors **SHALL NOT** encode order (`Serial/Parallel`) or phase/time as part‑whole relations; handle them via `Γ_method` / `Γ_time` when relevant to the claim.                                                                               | Maintain the structure/order/time firewall.                               |
| **CC‑CT2R‑5 (Collection vs part).**             | Authors **SHALL** keep **MemberOf** (collections) distinct from **PartOf** (structure) and refrain from carrying reliability as if membership implied structural composition.                                                                 | Prevent category errors flagged in B.3 anti‑patterns.                     |
| **CC‑CT2R‑6 (Fit is explicit).**                | Where mappings or alignments matter, the author **SHALL** reason about **fit** explicitly (Congruence Level, conceptually) and acknowledge that weak fit reduces the effective reliability of any composed claim.                             | Keep integration quality first‑class.                                     |
| **CC‑CT2R‑7 (Notational independence).**        | Core meaning **MUST NOT** hinge on any specific diagram or syntax; illustrative renderings, if present, are labelled *informative*.                                                                                                           | Ensure longevity and cross‑discipline portability.                        |
| **CC‑CT2R‑8 (Layer direction).**                | Grounding flows **downwards** from Working‑Model to Assurance layers (Mapping/Logical/Constructive). Authors **SHALL** avoid back‑defining the canonical relation by its grounding artefact.                                                  | Preserve unidirectional dependence of layers.                             |
| **CC‑CT2R‑9 (Scope split).**                    | When assurance is discussed, authors **SHALL** state the **typed claim** and **scope** `S ∈ {design, run}` and keep them distinct in reasoning.                                                                                               | Prevent design/run chimeras.                                              |


### B.3.5:12 - Consequences (benefits, trade‑offs, mitigations)

**Benefits**

* **Cognitive clarity for authors and readers.** By making Working‑Model relations canonical and keeping formal bases as optional groundings, CT2R reduces the barrier to disciplined reasoning while preserving a path to higher assurance when necessary.  This honours the B.3 family's “few characteristics, conservative aggregation” ethos and keeps order/time outside of structure.
* **Progressive assurance without tooling commitments.** The *postulate → inferential → axiomatic* ladder lets teams raise assurance deliberately, matching their context and risk, in line with B.3.3’s maturity logic.
* **Explicit fit management.** Treating edge‑fit (CL) as a first‑class concern prevents silent over‑confidence: weak mappings visibly cap reliability of composed claims.
* **Cleaner separation of concerns.** Distinguishing collections from compositions and keeping sequence/time in Γ\_method / Γ\_time prevents recurrent category errors and preserves Γ‑algebra reviewability.

**Trade‑offs & mitigations**

* **Extra prose discipline.** Declaring `validationMode` and writing a short grounding narrative (when *axiomatic*) adds authoring effort. *Mitigation:* reuse local templates; keep narratives concise and Γ\_m‑oriented by idea rather than notation.
* **Temptation to stay “forever postulate.”** Teams may stop at Working‑Model relations. *Mitigation:* use B.3.3’s subtypes/levels as a **planning aid** to decide where *axiomatic* or *inferential* grounding is worth the cost.
* **Perceived conservatism.** Acknowledging weak fit (CL) may lower effective reliability of otherwise strong parts. *Mitigation:* treat CL as a guide to improvement (reconcile terms, align units, verify interfaces) rather than a punishment.

> **One‑line takeaway for managers.**
> CT2R lets you **talk in natural, domain‑meaningful relations** while preserving a clear, optional path to formal grounding and empirical checking—so confidence can grow deliberately without dragging your model into tooling or syntax.


### B.3.5:13 - Rationale (informative)

**13.1 Why canonical‑first?**
CT2R‑LOG treats the **human‑readable, task‑appropriate relation** (e.g., `ut:ComponentOf`) as the **canonical publication form** because that is what engineers and managers actually use to reason, decide, and communicate. The formal layers exist to **support** that form—not to replace it. This is consistent with the authoring Standard in Part E (pattern template and style guide), which privileges **clarity, purpose and didactics** over premature formalism in the body text. Authors write *for people first*, then point to the kind of assurance they are invoking.

**13.2 Why two `tv:` links—and why concept‑only?**
`tv:AliasOf` and `tv:groundedBy` name **conceptual bridges** between a Working‑Model relation and its assurance. They are *not* mandates for any particular notational scheme; they are **mental handles** that keep authors honest about *what* grounds their claims (constructive, logical, mapping) and *when* that grounding is expected to be present. This honours the **Notational Independence** guard‑rail in Part E: we adopt **concepts and obligations**, not file formats or tool Standards, in the normative text.

**13.3 Why a triad of `validationMode`?**
The triad **{postulate, inferential, axiomatic}** expresses a **scalable formality ladder** compatible with the FPF stance on staged assurance: start with what the team can responsibly claim now, and climb to stricter justification where risk or context demands it. That mirrors the “ladder” patterns in Part E and gives reviewers a shared vocabulary for **how strong** a claim is meant to be—without changing the canonical relation itself.

**13.4 Why keep order/time out of mereology?**
CT2R‑LOG aligns with A.14’s **firewall**: structure (parthood) is distinct from **order** and **temporal coverage**. The former is published as `ut:StructPartOf` sub‑relations; the latter live in `Γ_method` / `Γ_time` and must **not** be smuggled into part‑trees. This separation avoids classic modelling failures (temporal smearing, pseudo‑components for quantities) and keeps reasoning crisp across the Γ‑family.

**13.5 Why point to `Γ_m.sum | set | slice` (Compose‑CAL) for constructive grounding?**
Three constructive moves—**sum, set, slice**—are sufficient to narrative‑rebuild all structural trees while preserving **extensional identity**. When an author selects the *axiomatic* stance, a brief `grounding narrative` can always be told in those terms, without expanding the kernel or inventing bespoke constructors. This satisfies **parsimony (C‑5)** and keeps formal power **outside** the kernel, in a calculus.

**13.6 Why mental obligations rather than process mandates?**
Part E requires that patterns govern **thinking** and **authoring**; enforcement and automation, if any, are external concerns. CT2R‑LOG therefore states obligations as **self‑contained cognitive checks**: declare your mode; tell the constructive story only when you claim *axiomatic* strength; keep order/time in their places. This keeps the core specification **evergreen and tool‑agnostic**, as required.

### B.3.5:14 - Relations

**Builds on**
• **A.14 Advanced Mereology** — structural catalogue and the firewall that excludes roles/recipes and distinguishes Portion/Phase/Component/Constituent; CT2R‑LOG preserves these distinctions at publication time.
• **A.11 Ontological Parsimony (C‑5)** — constructive grounding lives in a calculus; the kernel remains minimal.
• **B.1 Universal Γ** — shared invariants and the placement of order/time in their respective Γ‑flavours.
• **Part E authoring rules** — canonical pattern template and notational independence, which CT2R‑LOG explicitly follows.

**Coordinates with**
• **Compose-CAL (Γ_m)** — provides the **constructive** shoulder of the Assurance layer for **structural** relations; CT2R-LOG’s `tv:groundedBy` points *conceptually* to traces narratable as **sum/set/slice**.
• **KD‑CAL** — provides the **logical** shoulder (inferential justification) when authors pick `validationMode = inferential`.
• **Kind-CAL / Lang‑CHR** — provide the **mapping** shoulder (type alignment and language hygiene) supporting alias policies without altering Working-Model relations.

**Constrained by**
• **Notational Independence (E.5.2)** — CT2R‑LOG refuses to prescribe formats, keeping all obligations conceptual.

**Specialises / feeds**
• **B.3.1–B.3.4** — supplies the publication discipline (Working-Model relations, declared **relation kind** and **validationMode**; **F** per C.2.3 where relevant) that B.3’s trust calculus expects; interacts with ageing and assurance-level assessments without changing the relations themselves.


**Non‑relations**
**No introduction of order/time** — CT2R‑LOG does **not** define `SerialStepOf` / `ParallelFactorOf` / temporal **phases**; those belong to **Method‑CAL** and **Sys‑CAL (TemporalPart)** respectively.  

### B.3.5:End

