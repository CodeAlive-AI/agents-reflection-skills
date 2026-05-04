## A.21 — GateProfilization: `OperationalGate(profile)` (GateFit core)

**ID:** A.21
**Type:** Architectural pattern

**One-liner.** A single microkernel-style gate aggregates **GateChecks (CV + GF)** into an **order-independent** `GateDecision` via the join-semilattice `abstain ≤ pass ≤ degrade ≤ block`, enforces the **CV⇒GF activation predicate** (and the LaunchGate pre‑run barrier), applies profile-bound folds for `error|timeout|unknown`, and publishes replay-grade traces (MVPK + `DecisionLog` + `EquivalenceWitness`). 

### A.21:1 - Problem frame

#### A.21:1.1 - Intent & scope

This pattern specifies the **GateFit core** of `OperationalGate(profile)` as the **sole** architectural locus for:

* enumerating and referencing `GateCheckKind`s as publication lexemes (CV kinds live in A.20; GF kinds are bounded here) via `GateCheckRef`,
* aggregating per-check outcomes into a single **publication-level** `GateDecision` using the join lattice,
* enforcing the **CV⇒GF** activation boundary (GateFit checks are inactive until aggregated CV is `pass`),
* defining the minimal **publication faces** and `DecisionLog` content required to make gate outcomes auditable and replayable. 
* applying **SWP at the gate**: `OperationalGate(profile)` (and its `GateCheck`s) is **ref‑only** w.r.t. editions/registries and domain artifacts; it publishes **only** `GateDecision` + `DecisionLog` (pins+refs) and MUST NOT author or mutate edition families.

This pattern is **about the semantics of what is published** (and how it composes), not about procedural execution. 

#### A.21:1.2 - Intensional object(s)

* **`OperationalGate(profile)`** — a gate node (`U.Transduction(kind=Check)`) that mediates any **GateCrossing**: any change in `CtxState = ⟨L,P,E⃗,D⟩` **or** entry to `U.WorkEnactment` (via `LaunchGate`). 
* **`GateProfile`** — the profile-bound constraint of the partial function `CtxState_from → CtxState_to`; fully specified in A.26, only *bound* here. 
* **`GateCheckRef`** — the publication lexeme that binds a check to `(aspect, kind, edition, scope)`. 
* **`GateDecision` / `GateDecisionRationale` / `GateDecisionExplanation`** — decision value, structured rationale, and optional narrative (non-decision). 
* **`DecisionLog`** — append-only audit surface linking decisions to check refs, rule anchors, and (where applicable) SquareLaw mismatches. 

#### A.21:1.3 - CV vs GF boundary (what “activation” means)

* **ConstraintValidity (CV)** evaluates *internal step lawfulness*;
* **GateFit (GF)** evaluates *external admissibility vs `GateProfile`* (planes/crossings, freshness, evidence, roles/channels, regulator conformance, etc.). 
* **Ordering & activation.** CV is evaluated before GateFit; **while `CV ≠ pass`, all GateFit checks return `abstain`.**  

#### A.21:1.4 - Failure surfaces (diagnostic lens)

* **CV ✔ / GF ✖**: lawful transformation, but wrong gate/profile/role/timing/evidence. 
* **CV ✖ / GF ?**: fix mechanism validity first; GF is inactive. 
* **CV ✔ / GF ✔**: admissible to proceed (publish/deploy). 

#### A.21:1.5 - Non-goals

* No procedural semantics (no scheduling, no API formats, no automation narratives). 
* No “second ladder” of processes outside the graph: every **check-point** is an `OperationalGate(profile)` node in the same transduction graph; its **pluggable GateChecks** are declared on the node (no floating checks), and only the declared check set + reaction rules vary across gates. 
* No key/hash/cache *formats*: A.21 constrains **equivalence + invalidation conditions**, but not key materialization. 
* No lexical “pseudo-gating”: the lexical layer is non-decisional and MUST NOT be modeled as a GateCheckKind. 


### A.21:2 - Problem

Without a unified GateFit core:

* Gate admissibility becomes ad-hoc, **order-dependent**, and hard to audit (especially with multiple independent checks). 
* Gate logic leaks into CV (planes/comparators/freshness/roles appear “inside steps”), collapsing the CV/GF separation. 
* “Unknown / timeout / error” behavior becomes implicit and inconsistent across transitions, undermining reproducibility and safety. 
* Publication faces drift into “extra semantics” (computed scalars / tool encodings) rather than pins + refs, breaking MVPK discipline. 

### A.21:3 - Forces

* **Separation vs convenience.** Keeping CV internal and GF profile-bound avoids leakage, but demands a crisp activation boundary. 
* **Determinism vs incompleteness.** Gates must remain deterministic even when evidence is missing or partial (`unknown`). 
* **Safety vs throughput.** Some profiles must treat ambiguity as `block`, others as `degrade`. 
* **Human comprehension vs formal minimality.** Optional narratives help readers, but must never masquerade as decisions. 
* **Reuse vs freshness.** Decisions may be reusable only under explicit equivalence; otherwise re-aggregation is mandatory. 
* **Scope granularity vs complexity.** Checks are declared with scopes (`lane|locus|subflow|profile`) and merged; duplicates must preserve evidence rather than overwrite it. 

### A.21:4 - Solution

#### A.21:4.1 - Gate = microkernel of checks


> **Note (guards are not GateChecks).** `USM.CompareGuard` / `USM.LaunchGuard` are **not** `GateCheckKind`s; they may emit `GuardFail` events which are **aggregated by the owner gate** under the active profile (`degrade|block`) and recorded in `DecisionLog` (details in A.24). 
`OperationalGate(profile)` is treated as a microkernel: checks are **pluggable** `GateCheck`s; the gate core **aggregates** their outputs **conceptually**, without procedural semantics and without mutating the transduction graph. 

#### A.21:4.2 - Publication lexemes and register discipline

**Per-check reference lexeme.**
`GateCheckRef := { aspect, kind, edition, scope }`, where:
* `aspect ∈ {ConstraintValidity, GateFit}`,
* `scope ∈ {lane|locus|subflow|profile}`.

**Authoring shorthand (deprecated; MUST NOT be surfaced).**
If a short form `GateCheckRefLegacy := { kind, edition, scope }` appears in prose as a local shorthand, it SHALL be interpreted only as a projection of the normative record with `aspect` supplied explicitly at the point of surfacing. Any published face or `DecisionLog` entry MUST use the full `GateCheckRef` with `aspect`.

**Decision terminology separation.**

* `GateDecision` is the published lattice value.
* `GateDecisionRationale` is the minimal structured support of that decision (check outcomes, folds, witness refs).
* `GateDecisionExplanation` is optional, human-readable, derived from the rationale; it **does not carry decision status** and MUST NOT be used as one.  

**Register discipline.** Tech labels are ASCII and twin-labeled where the plain form uses symbolic notation. 
(Example: use `CLPlane` / “CL^plane”, `CLKind` / “CL^k”, `UNM.TransportRegistryPhi` / “UNM.TransportRegistryΦ”, `GammaTimeRule` / “Γ_timeRule”.)

#### A.21:4.3 - CV⇒GF activation predicate (counterfactual boundary)

GateFit checks are *defined* as inactive unless the CV aspect is `pass`:
* Let `CV.Status` be the join-aggregate of all `GateCheckRef` with `aspect=ConstraintValidity`.
* For any `GateCheckRef` with `aspect=GateFit`:
  **If `CV.Status ≠ pass`, the GateFit check outcome is `abstain`.** 
* While `CV.Status ≠ pass` **(or the active profile suppresses narratives)**, any GateFit-oriented `GateDecisionExplanation` **does not apply**. 

This keeps the boundary crisp: CV explains internal lawfulness; GF explains profile-fit **only in the counterfactual world where CV passed**. 

**LaunchGate pre‑run barrier (work‑boundary special case).**

For the unique `LaunchGate` at the entry of each `U.Work`/`U.WorkEnactment`, let `Prev.CV.Status` denote the aggregated `ConstraintValidityStatus` of the **immediately preceding** step on the same `PathSlice`.

* If `Prev.CV.Status ≠ pass`, then (i) all GateFit-scoped LaunchGate checks return `abstain` by activation, and (ii) the **overall LaunchGate** decision is forced to `block` (pre‑run barrier). The rationale MUST record the predecessor CV status and the forced-block rule in `DecisionLog`.

This is a publication-level safety invariant: it constrains what may be admitted at the work boundary without specifying evaluation order or execution scheduling.

#### A.21:4.4 - Decision algebra: join-semilattice (“worst wins”)


**Decision domain.** `GateDecision ∈ {abstain, pass, degrade, block}`.

**Aggregation rule.** Aggregation over all applicable checks is the **idempotent, commutative, associative join** on
`abstain ≤ pass ≤ degrade ≤ block`, with **neutral = `abstain`** and **absorbing = `block`**. 

Publications surface only:

1. the aggregated `GateDecision`, and
2. its `GateDecisionRationale` recorded in the `DecisionLog`. 

#### A.21:4.5 - Profile-bound folds for `error|timeout|unknown`
A check may encounter `error`, `timeout`, or evidence-level `unknown`. These do **not** become new decision values; they are folded into the decision lattice **by profile and check policy**.
**Normative minimum folds (tri-state).**  

> **Naming note.** Some conformance tables use **Lean** as a label for the `GateProfile=Lite` gating posture. Treat this as an alias only, and do not confuse it with `PublishMode=Lite` (a publication-face reduction mode).

| Active `GateProfile` | `error` fold | `timeout` fold | `unknown` fold (evidence-level) |
| -------------------- | -----------: | -------------: | ------------------------------: |
| `Lite`               |    `degrade` |      `degrade` | per `GateCheck` policy (`abstain` or `degrade`) |
| `Core`               |    `degrade` |      `degrade` | per `GateCheck` policy (`abstain` or `degrade`) |
| `SafetyCritical`     |      `block` |        `block` | per `GateCheck` policy (safety-default: `degrade`) |
| `RegulatedX`         |      `block` |        `block` | per `GateCheck` policy (safety-default: `degrade`); X identity/edition are surfaced in `DecisionLog` |
| `RegulatedX`         |      `block` |        `block` | per `GateCheck` policy (safety-default: `degrade`); X identity/edition are surfaced in `DecisionLog` |

Where a `GateCheck` declares an evidence-level `unknown` strategy, that strategy is part of the check’s intensional definition; the fold applied and its justification are recorded in `DecisionLog`.  

#### A.21:4.6 - GateProfiles: binding only (full spec in A.26)

A.21 binds the following *functional role* of `GateProfile`:

> **Terminology (avoid `Lite`/`Lean` confusion).** `GateProfile=Lite|Core|SafetyCritical|RegulatedX` is the **gating posture** that determines the effective GateCheck set and fold policies. `PublishMode=Lite` is a **publication-face reduction mode** (AssuranceLane‑Lite / TechCard‑Lite) and MUST NOT be interpreted as a weaker `GateProfile`.

* A `GateProfile` is an attribute of a **branch / `PathSlice`**; the default is `Core`. 
* Local overrides may change the active profile for the transition and below **but cannot reduce** the already-effective set of `GateCheckKind`s; only additions are allowed. Weakening requires a new `PathSlice` via sentinel. 
* `PublishMode=Lite` affects *faces only* and does **not** weaken the check set or aggregation rule. 

#### A.21:4.7 - Scope and merge semantics (`lane|locus|subflow|profile`)

* Each `GateCheckRef` declares its scope; `subflow` scope is bounded by a sentinel bridge (restart / refresh boundary). 
* The effective check set is formed by **union across all declared scopes**; duplicates by `kind` merge by the same join rule (“worst wins”), and **all rationales are preserved** in `DecisionLog`.
  * For `RegulatedConformance(X)`, the identity of **X** and its rule/edition reference are part of the rationale surface; multiple `RegulatedConformance(X{…})` may coexist in one gate.
* A check outside its scope reports `abstain`. 

#### A.21:4.8 - Publication repeatability, caching, and re-aggregation triggers
**Repeatability (publication-level).** Gate decisions MUST be replayable from declared pins/refs: no implicit “latest/now”. Any time basis is made explicit via `Γ_time` (or a `Γ_timeRule` that resolves to a concrete basis), and the resolved basis is recorded in `DecisionLog`.

**Caching constraint (publication-level).** A gate decision may be cached **only** per
`{PathSliceId, GateProfile, GateChecks.editions, editions{…}}`, where `GateChecks.editions` denotes the canonicalized, order-independent listing of the **effective** `GateCheckRef{aspect,kind,edition,scope}` (including their `edition`s) for this gate instance. Cache reuse is valid only while the declared freshness/evidence window remains valid under the active profile.

**Re-aggregation triggers (non-exhaustive, normative).** Re-aggregation is required if any of the following changes (slice-local; no execution procedure implied):


* any component of `editions{…}` changes (any `edition_key ↦ EditionId` bump),
* any `GateCheckRef.edition` changes (including regulator X editions for `RegulatedConformance(X)`),
* the declared `Γ_time` basis changes or resolves differently,
* a relevant `FreshnessTicket` expires/changes or TOCTOU window constraints change,
* a sentinel-bounded `subflow` refresh introduces a new RSCR carrier affecting the rationale surface,
* any input breaks the declared equivalence witness (A.41).

Decision stability is under the equivalence relation of A.41; a witness is surfaced on the `DecisionLog` (see §4.10). A.21 constrains equivalence + invalidation conditions but does not fix key formats.

#### A.21:4.9 - MVPK faces for `OperationalGate(profile)` (minimum pins)

The gate publishes faces to record **what is declared**, not “how it executes”. Faces remain **pins + refs** (no new numeric claims; no I/O re-listing).

**Minimum pins (PlainView / TechCard / AssuranceLane where applicable).**

* View scope: `PublicationScopeId` (with MVPK profile: `Min|Lite|SetReady|Max`)
* Identity: `GateId`, `BridgeId`, `PathId`, `PathSliceId`
* Temporal: `DesignRunTagFrom`, `DesignRunTagTo`
* Profile: `GateProfile` (PublishMode affects only face reduction)
* Checks: list of `GateCheckRef` (`aspect`, `kind`, `edition`, `scope`)
* CV: aggregated `ConstraintValidityStatus` and optional `ConstraintValidityWitnessRef` (refs only)
* Editions: `editions{…}` vector + `EditionPins{CGSpec, ComparatorSet, UNM.TransportRegistryPhi}`
  * **Gate-requirement on edition refs.** Any face that cites `CGSpec` / `ComparatorSet` / `UNM.TransportRegistryΦ` editions MUST also include `BridgeCard + UTS row` (A.27); otherwise downstream consumption is non-conformant.
* ReferencePlane & CL: source/target `ReferencePlane` pins; `CLPlane` / “CL^plane” (for non-crossings `CL^plane = none` is allowed, but pins are still explicit); any Φ penalties are surfaced as rule refs and route to the **R-channel only**
* Freshness: declared `GammaTime` / “Γ_time” pin and presence/absence of `FreshnessTicket` (refs)
* Evidence: SCR/RSCR carrier anchors (refs) + VALATA (VA/LA/TA) presence on AssuranceLane
* Guards: `USM.CompareGuard` / `USM.LaunchGuard` applicability pins (presence-only; GuardFail is handled by the owner gate per A.24)
* Decision: aggregated `GateDecision` and `DecisionLogRef`

**Lean face (PublishMode=Lite).** It MAY fold to `GateProfile / GateChecks / EditionPins / GateDecision + DecisionLogRef`, but:

* it MUST keep `GateProfile` and `DecisionLogRef`,
* it MUST not weaken GateChecks or the aggregation algebra, and
* if `EditionPins` are present, it MUST still include `BridgeCard + UTS row` (A.27) and preserve the “red lines” on crossings (explicit `ReferencePlane`, `CLPlane`, and Φ → R-channel only).

#### A.21:4.10 - DecisionLog (minimum composition)

`DecisionLog` is an append-only record of reasons and references: 

* gate identity + `PathSliceId` (+ `PublicationScopeId` when the log is surfaced via a face bundle)
* each `GateCheckKind`, its `GateCheckRef.edition`, and its folded outcome (`pass|degrade|block|abstain`) including the applied `error|timeout|unknown` fold
* rule anchors / evidence anchors (SCR/RSCR carriers + VALATA bindings); where relevant, mismatched pins (SquareLaw) are called out explicitly
* policy-id dependencies used by checks (as `PolicyIdRef` bundles per F.8:8.1), including `Φ(CL)`, `Φ_plane`, and `Ψ(CL^k)` where relevant, plus any gate-local policy-ids consulted by the active profile
* `GuardFail` events (from `USM.Guards`) aggregated by the owner gate with the applied profile rule (`degrade|block`)
* `EquivalenceWitness` (or `EquivalenceWitnessRef`) as a publication surface per A.41, minimally: `{ keys, E⃗, Γ_time(basis), PathSliceId?, ReturnShapeClass, ComparatorSetRef?, profile }`
* the declared publish reaction for `degrade|block` (including any local “degrade mode” notes when permitted by profile)
* for `RegulatedConformance(X)`: the identity of X and the rule/edition references used

#### A.21:4.11 - GateChecks admissibility (GateFit-only catalog boundary)

**Mandatory on LaunchGate.** `FreshnessUpToDate`, `DesignRunTagConsistency`.  
**Allowed GateFit checks (non-exhaustive, normative minima).** 

* `DesignRunTagConsistency` (mandatory on LaunchGate; may appear elsewhere)
* `FreshnessUpToDate` (mandatory on LaunchGate; may appear elsewhere)
* `ReferencePlaneCrossing`
* `ComparatorConstraintRules (CSLC)`
* `EvidenceCompleteness`
* `SafetyEnvelope`
* `RegulatedConformance(X)` (X identity + edition/rule refs are surfaced in `DecisionLog`)
* `Role/ChannelFit` (roles are Kernel `U.Role` tokens, not alias strings)
* `EquivalencePreservation`
* `OutflowAudit`
* `SnapshotConsistency`

**Forbidden (hard boundary).**

* Modeling CV classes “as GateFit” (CV classes remain CV; GF remains GF). 
* Any “LEX gate checks” or lexical pseudo-checking (lexical views do not participate in decisions).  

#### A.21:4.12 - SquareLaw compatibility at crossings
For every GateCrossing, the SquareLaw constraint must hold:
`gate_out ∘ transfer = transfer' ∘ gate_in`. 

Profile selection/inheritance does not weaken this requirement; inconsistency yields `block|degrade` within the active profile and is recorded in the DecisionLog. LaunchGate is a work-boundary GateCrossing case, so SquareLaw is mandatory there as well.

#### A.21:4.13 - Lexical mediation (optional trace, non-decisional)

A gate MAY publish a `LexicalResolutionRef` / `LexicalView` for traceability of alias resolution, but:

* it does **not** participate in aggregation, and
* it does **not** influence `GateDecision`.  

### A.21:5 - Archetypal Grounding

#### A.21:5.1 - System vignette — “Regulated release gate”

**Tell.** A flow reaches a `LaunchGate` just before a `U.WorkEnactment` that can finalize binding. The active profile is `RegulatedX`. The gate publishes a single `GateDecision` and a `DecisionLog` that explains *why* the release is admissible (or not), without encoding any execution procedure.

**Show A (CV ✔, GF ✖).** CV checks are `pass`, activating GateFit. `RegulatedConformance(X)` is present but evidence anchors are incomplete (`EvidenceCompleteness` folds to `degrade` under `Core/RegulatedX` policy), so the join yields `degrade`. The DecisionLog records which `GateCheckRef` caused the fold and the declared publish reaction for degraded release. 

**Show B (CV ✖, GF n/a).** CV aggregate is `degrade`. All GateFit checks return `abstain` by activation, and any GateFit-oriented explanation is inapplicable. The gate’s published decision is driven by CV; the DecisionLog shows CV status and the “inactive GF” boundary rather than a fabricated GF narrative.  

#### A.21:5.2 - Episteme vignette — “Cross-plane comparability gate”

**Tell.** A flow transitions into a comparability-critical step (CSLC). The gate must surface `BridgeId + UTS + CLPlane` and edition pins for downstream consumers, and must remain stable under A.41 equivalence.

**Show A (Core, clean crossing).** The gate publishes `EditionPins{CGSpec, ComparatorSet, TransportRegistryPhi}`, `ComparatorSetRef`, `CL/CLPlane`, and a `GateDecision=pass` with a rationale that cites the relevant `GateCheckRef`s and editions. 

**Show B (SquareLaw mismatch).** A crossing attempts to change plane pins without the commutative-square witness; the SquareLaw check yields `block` (or `degrade` under a weaker profile), and the DecisionLog records the mismatched pins as the reason.  

### A.21:6 - Bias-Annotation

This pattern’s built-in biases are stated across the five Principle-Taxonomy lenses (Gov, Arch, Onto/Epist, Prag, Did). 

* **Gov.** Bias toward auditability and explicit responsibility (DecisionLog + profile-bound folds). Risk: gate owners become de facto governors; mitigation: keep profiles explicit, inheritable, and pinned to `PathSliceId` for reviewable replay. 
* **Arch.** Bias toward a microkernel of checks (pluggable GateChecks + join aggregation). Risk: “check sprawl”; mitigation: scope discipline + forbidden LEX pseudo-checking + CC-based profile minima. 
* **Onto/Epist.** Bias toward a 4-value admissibility lattice and explicit “does not apply” boundaries. Risk: oversimplifying nuanced epistemic uncertainty; mitigation: preserve structured rationales and allow check-level `unknown` policies rather than inventing new global decision values. 
* **Prag.** Bias toward determinism and replayability (cache invalidation by pinned vectors). Risk: higher publication overhead; mitigation: PublishMode=Lite for faces (never for weakening checks). 
* **Did.** Bias toward explicit separation (CV vs GF) and “what is published” clarity. Risk: more concepts to learn; mitigation: archetypal grounding + stable minimal pins across faces. 

### A.21:7 - Conformance Checklist

Minimum unified conformance for A.21 (and any flow that claims GateFit discipline): 

#### A.21:7.1 - Core gate semantics

* [ ] **CC‑TGA‑06**: all GateCrossings (CtxState changes, and work-boundary crossings via LaunchGate) are mediated by `OperationalGate(profile)` and have a `DecisionLog`. 
* [ ] **CC‑TGA‑07**: CV⇒GF activation predicate holds (`CV≠pass ⇒ GF=abstain`). 
* [ ] **CC‑TGA‑21**: decision stability witness is present on the `DecisionLog` surface (A.41 `EquivalenceWitness`). 
* [ ] **CC‑TGA‑21a**: aggregation is the join on `abstain ≤ pass ≤ degrade ≤ block`; `GateDecisionExplanation` is optional and non-decisional. 
* [ ] **CC‑TGA‑22**: `error|timeout` folds are profile-bound; `unknown` folds per GateCheck policy. 

#### A.21:7.2 - LaunchGate discipline (pre-run barrier)

* [ ] **CC‑TGA‑08**: every `U.WorkEnactment` has exactly one `LaunchGate` with mandatory `FreshnessUpToDate` + `DesignRunTagConsistency`; **pre‑run barrier:** if the immediately preceding aggregated `ConstraintValidityStatus ≠ pass`, then all LaunchGate GateFit checks are `abstain` and the overall LaunchGate decision is `block` (logged). 
* [ ] **Pre‑Run barrier** is satisfied for any `U.Work` where `FinalizeLaunchValues` is possible. 

#### A.21:7.3 - Publication and evidence

* [ ] **CC‑TGA‑20**: `PublishMode=Lite` affects faces only; required GateChecks remain intact. 
* [ ] **CC‑TGA‑25**: AssuranceLane surfaces `GateProfile`, `GateCheckRef` list, edition pins, `GateDecision`, and `DecisionLogRef` with the two-layer evidence scheme (SCR/RSCR + VALATA). 

#### A.21:7.4 - Cross-boundary additions (when the gate is a crossing)

* [ ] **CC‑TGA‑11**: crossings publish `BridgeId + UTS + CLPlane/CL^plane`, penalties route to the R-channel only. 
* [ ] **CC‑TGA‑23**: SquareLaw holds on crossings; mismatch yields `block|degrade` per profile and is logged. 

#### A.21:7.5 - Lexical norms (E.10 discipline)

* [ ] Tech names are ASCII and twin-labeled; required token classes are registered under LEX (including `GateProfile`, `GateCheckKind`, `GateCheckRef`, `DecisionLog`). 
* [ ] Any lexical alias view is trace-only and does not affect decisions. 

### A.21:8 - Consequences

**Benefits**

* **Deterministic gating.** Join-semilattice aggregation makes decisions order-independent and idempotent (modulo declared equivalence), enabling consistent audit and replay. 
* **Clean CV/GF separation.** Activation boundary prevents profile concerns from leaking into mechanism validity. 
* **Profile clarity.** Fold policies (`error|timeout|unknown`) are explicit and profile-bound, making safety posture reviewable. 
* **Publication hygiene.** MVPK faces remain pins+refs (no new numeric claims), and DecisionLog captures rationale without procedural commitments. 

**Trade-offs**

* **More artifacts to publish.** Decisions are not “just pass/fail”: they require rationales, pins, and logs. 
* **Two-stage reasoning.** Users must internalize “GF does not apply until CV passes”; mitigated by explicit inapplicability rules and optional narratives only when applicable. 
* **Scope complexity.** Multi-scope merge semantics can feel heavy; mitigated by union + worst-wins + preserved rationales. 

### A.21:9 - Rationale

* The microkernel framing preserves a single graph semantics: checks are nodes and publications, not an external pipeline; this blocks the emergence of a “second ladder” of hidden processes. 
* The join lattice provides a minimal, monotone aggregation that supports:

  * early absorption at `block` without specifying execution strategy, and
  * deterministic publication semantics (commutative + associative + idempotent). 
* CV⇒GF activation is the mechanism that keeps orthogonality strict while still publishing a single gate decision surface: GF results never “mask” CV failures. 
* Explicit folds for `error|timeout|unknown` make safety posture reviewable and profile-specific without inventing new decision values. 

### A.21:10 - SoTA-Echoing

Anchors (post-2015) that this pattern **adopts/adapts/rejects**, consistent with the assignment’s intent (assured lanes, open graphs/hypergraph categories, join-semantics). 

* **Adopt.** *Join-semilattice aggregation as deterministic, order-independent merge* (distributed systems / CRDT literature, e.g., Kleppmann 2017; Kleppmann & Beresford 2017): A.21 reuses the algebraic idea to make gate outcomes commutative/associative/idempotent without prescribing evaluation order.
* **Adapt.** *Compositional reasoning with commuting diagrams* (applied category theory, e.g., Fong & Spivak 2019): A.21 adapts the intuition by making SquareLaw a gate-audited invariant on crossings, while keeping publications human-first and pin-based.
* **Adapt.** *Supply-chain provenance / policy gating via attestations* (software supply-chain security, e.g., in-toto 2019; SLSA 2021+): A.21 adapts the “attestation + policy check + logged decision” structure, but expresses it as MVPK pins + `DecisionLog`, not tool-specific workflows.
* **Reject.** *Narrative-as-authority.* Any approach where human-readable explanations function as decision-bearing artifacts is rejected; in A.21, narratives remain optional derivatives of structured rationales and are explicitly non-decisional. 

### A.21:11 - Relations

* **E.TGA →hosts→ A.21.** GateFit-scoped GateChecks are aggregated by `OperationalGate(profile)`; enumeration and publication shape of GateChecks live here. 
* **A.20 →couples_to→ A.21 via CV⇒GF.** CV is evaluated inside transformations; while CV≠pass, GF is `abstain` and GF explanations do not apply. 
* **A.26 →fully_specifies→ GateProfile.** A.21 binds to A.26 for the profile matrix, inheritance rules, and detailed mandatory check sets. 
* **A.25 (Sentinel/SubFlow) →provides→ scope boundaries.** `subflow` scope is bounded and restartable; weakening check sets requires new `PathSlice`. 
* **A.27 (Bridge+UTS) →required_by→ any edition-citing face.** Whenever gate faces cite editions, the compatibility surface (BridgeCard + UTS + `CL/CLPlane`) is required for downstream consumption. 
* **A.41 →defines→ equivalence for decision stability.** Gate decisions are stable only under the declared equivalence witness; breaking equivalence implies re-aggregation. 

### A.21:End

