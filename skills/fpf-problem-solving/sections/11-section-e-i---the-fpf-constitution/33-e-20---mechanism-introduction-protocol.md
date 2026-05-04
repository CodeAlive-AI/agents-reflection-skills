## E.20 - Mechanism Introduction Protocol

> **Type:** Architectural pattern  
> **Status:** Draft  
> **Normativity:** Normative  

### E.20:1 - Problem frame

FPF is intentionally **open‑ended**: new `U.Mechanism.*` intensions, suite compositions, and SoTA‑driven wiring modules can be added over time. This flexibility creates a recurrent authoring problem: introducing a new mechanism (or revising an existing one) tends to touch **multiple semantic owners** across Parts A/E/F/G and can easily create drift:

* semantics leak into the wrong plane (e.g., Part G wiring starts carrying mechanism meaning),
* suites degrade into “meta‑mechanisms” or hidden gates,
* planned baselines (WorkPlanning) are conflated with execution witnesses (WorkEnactment),
* token drift breaks public references, or
* the corpus accumulates dangling references and “workpad commitments” without ownership.

This pattern defines a **repeatable, owner‑routed protocol** for introducing mechanisms that keeps the kernel coherent while remaining extensible.

### E.20:2 - Problem

When a new mechanism (or mechanism family) is introduced without an explicit authoring protocol:

1. **Ownership ambiguity** causes partial changes: a suite enumerates a new `…IntensionRef`, but the canonical `U.Mechanism.Intension` card is missing or inconsistent.
2. **Boundary erosion** occurs: suite descriptions start to define mechanism semantics; method wiring starts to redefine kernel meaning; publication/telemetry becomes a hidden tail.
3. **Plan/enactment confusion** appears: planned slot fillings start to carry launch values, witnesses, or gate decisions.
4. **Terminology drift** breaks citations: renames happen silently; tokens fragment across registers; downstream references become unstable.
5. **Review becomes non‑local**: every introduction is a bespoke scavenger hunt across patterns, making training, review, and refresh unreliable.

### E.20:3 - Forces

| Force | Tension |
|---|---|
| **Extensibility vs Kernel stability** | New mechanisms must be addable ↔ kernel surfaces must remain citeable and minimal. |
| **Single semantic owner vs cross‑cutting impact** | Each artifact needs one owner ↔ introducing a mechanism often spans suites, plans, wiring, and lexicon. |
| **Didactic usability vs auditability** | Humans need clear “cards” and examples ↔ obligations/pins must remain checkable and non-leaky. |
| **SoTA evolution vs semantic integrity** | Methods evolve fast ↔ mechanism meaning must not silently shift via wiring updates. |
| **Local naming freedom vs global reference continuity** | Context‑local labels are necessary ↔ references must remain stable across editions and refactors. |

### E.20:4 - Solution — the Mechanism Introduction Protocol (MIP)

#### E.20:4.0 - Terminology note (disambiguation)

*This protocol is an authoring-plane route map.* It is **not** a suite protocol (`SuiteProtocol` in `MechSuiteDescription`) and is **not** a runtime gating mechanism (`OperationalGate(profile)` or any gate-level decision log).  
MIP governs **how changes are routed to their semantic owners**, not how systems execute.

#### E.20:4.0.1 - Mint vs reuse

**Mints:**
* **MIP** — Mechanism Introduction Protocol (this pattern).
* **MIP-run** — an authoring event that applies this protocol to a concrete change set, captured as a short manifest (recorded as a DRR-linked change record or an equivalent, explicitly citeable change artifact).

**Reuses:**
* `U.Mechanism.Intension` / `U.Mechanism.IntensionRef`, suite descriptions (`MechSuiteDescription` and specializations), WorkPlanning plan items (`SlotFillingsPlanItem` and specializations), alias docking (F.18), RSCR triggers (G.Core), and PQG profiles (E.19).

#### E.20:4.1 - Step 1: Classify the introduction

A MIP-run SHALL first classify the change, because different classes have different owners:

1. **New mechanism kind / new archetypal grounding** (new `U.Mechanism.Intension` archetype).
2. **New mechanism intension within an existing kind** (new `…IntensionRef`, new canonical card).
3. **Mechanism revision** (signature/laws/slots/transport/audit semantics change).
4. **Suite change** (membership, obligations, contract pins, suite protocols, suite audit obligations).
5. **Planned-baseline change** (new or revised `SlotFillingsPlanItem` specialization, or changes to its pins).
6. **Wiring change** (new or revised Part‑G extension modules, SoTA method packs, selectors).
7. **Terminology migration** (renames, token splits/merges, register changes).
8. **Deprecation / supersession / retirement** (marking mechanisms/suites/plan items as deprecated, declaring successors, and preserving citeability; apply E.20:4.9.1).

A single MIP-run MAY span multiple classes, but SHALL treat each class with its correct owner routing (below).

#### E.20:4.2 - Step 2: Declare the semantic owner route map (mandatory)

For every new or modified artifact, the MIP-run SHALL declare **exactly one semantic owner** and route the change there. In FPF, an “owner” is a citeable container that can be patched: a `PatternId` (or `PatternId:SectionPath`) for text, a `PatternScopeId = G.x:Ext.*` for wiring modules, or a `DRRId` (E.9) for a decision/rationale record. The declaration SHALL be captured as a **MIP-run manifest** in a citeable change record (typically DRR-linked) listing, at minimum:

* the change class(es) from E.20:4.1,
* each touched artifact → owner → canonical location (expressed as `PatternId:SectionPath` / `PatternScopeId` / `DRRId`, not as prose),
* any new/changed citeable tokens (`…IntensionRef`, `SlotKind` tokens, `PatternScopeId`, etc.),
* the best-known Delta-Class (Δ‑0…Δ‑3) and an impact radius estimate (E.15) when the run is plausibly Δ‑2/Δ‑3,
* intended RSCR trigger types, and
* the PQG (E.19) profile set used to review the run.

**Note (normative).** If the canonical location is a Part‑G wiring module, it SHALL be cited as a `PatternScopeId` (`G.x:Ext.*`) and the module SHALL declare `SemanticOwnerPatternId` (wiring is binding-only; meaning remains owner-routed).

**Canonical owner route map (normative):**

| Artifact / change kind | Semantic owner | Canonical location | Forbidden move |
|---|---|---|---|
| Mechanism intension meaning (ops/laws/invariants, admissibility, slot contract, transport/audit semantics) | **Mechanism card owner** | Designated mechanism-owner pattern | SHALL NOT “define” the mechanism inside a suite or a wiring module. |
| Suite membership / obligations / contract pins / suite protocols | **Suite owner** | `A.6.7` or `A.6.7.<FamilyKey>` | SHALL NOT smuggle mechanism semantics, **acceptance thresholds / gate criteria**, DecisionLogs, or publish tails into the suite. |
| Planned baseline pins (planned slot fillings; edition-pinned refs; explicit time selector) | **WorkPlanning owner** | `A.15.3` + suite-specific specialization (if needed) | SHALL NOT embed launch values, witnesses, or gate decisions in planning. |
| SoTA method/comparator/generator **definitions** (incl. provenance and evaluation semantics) | **SoTA pack owner** | `G.2` (SoTA synthesis packs) | SHALL NOT rephrase SoTA evolution as kernel semantics. |
| Wiring that binds SoTA packs into flows / tasks | **Extension module owner** | `G.x:Ext.*` (`GPatternExtension` with explicit `PatternScopeId`) | SHALL NOT mint new semantics; SHALL bind/wire only. |
| Token renames and drift management | **Lexical owner** | `F.18` (alias docking) + registers per E.10/F.17 | SHALL NOT silently rewrite tokens or break citations. |
| Change causality taxonomy and regression triggers | **RSCR owner** | `G.Core` | SHALL NOT invent ad hoc “reason kinds” scattered in patterns. |
| Project specializations of a mechanism | **Project owner** | `P.*` patterns (using `⊑/⊑⁺`) | SHALL NOT mutate kernel membership to express project variants. |

**Guard (normative).** Any proposed change that cannot name a semantic owner from the table above SHALL be treated as non-normative workpad content and SHALL NOT be relied upon as an architectural commitment. Such content MAY exist only as explicitly-marked workpad material until routed.

#### E.20:4.3 - Step 3: Card-first canonicalization (eliminate dangling refs)

If the introduction adds a new `U.Mechanism.IntensionRef` anywhere (especially inside a suite):

1. The MIP-run SHALL first create a **canonical mechanism card** at the owning pattern location that publishes the `…IntensionRef` and the minimal identity surface (names, intent, and “this is a distinct mechanism”).
2. The card MAY be a **stub** initially, but SHALL reserve:
  * the stable `…IntensionRef` (and its lexical register entry per E.10/F.17),
   * the intended kind/species placement, and
  * a DRR pointer for completing semantics (including any missing register/twin-label work).

Only after (1) is in place MAY suites or protocols enumerate the new `…IntensionRef`.

#### E.20:4.4 - Step 4: Mechanism semantics completion (what “done” means)

**Definition-of-done note (delegated).** MIP uses two completion checkpoints for mechanism cards:

* **Stub done** — a *resolvable canonical target* created to eliminate dangling references (E.20:4.3). A stub **SHALL** (i) exist at the mechanism-card owner’s canonical location, (ii) reserve and publish the stable `…IntensionRef` (and its lexical/register entries), (iii) set `IntensionHeader.status = draft`, and (iv) carry an explicit DRR pointer for completing semantics. A stub **SHALL** also list the *A.6.1* conformance checklist item IDs it does **not** yet satisfy (without duplicating that checklist here). A stub is sufficient to unblock suite/protocol enumeration, but **MUST NOT** be treated as an “introduced” mechanism for reuse/import decisions.
* **Introduced done** — a mechanism card that can be relied upon as a `U.Mechanism.Intension`. “Introduced done” is defined by *A.6.1* conformance: the card **SHALL** satisfy the applicable *A.6.1:7 Conformance Checklist* items (**CC‑UM.\***), with the baseline items designated by *A.6.1* (e.g., **CC‑UM.0** and **CC‑UM.1**) being the minimum requirement.

The list below is **informative** only (semantic orientation); the normative structure and “done” criteria are delegated to *A.6.1*’s CC items to avoid drift between this protocol and the canonical mechanism definition.

To be considered “introduced” (beyond a stub), a mechanism card SHOULD make the following semantic surfaces explicit:

* **Operation surface**: the named operations that the mechanism provides (signature-level intent).
* **Law / invariant surface**: the invariants that govern the operations (incl. legality constraints when applicable).
* **Admissibility surface**: preconditions/eligibility predicates for valid operation (not a gate decision log, and not per-run outcomes).
* **Slot contract**: required inputs/outputs as slot kinds, with stable kinds and explicit ref modes.
* **Specialisation discipline (when `⊑/⊑⁺` is declared):** explicit parent+morphism kind; SlotKind invariance; monotone ValueKind narrowing; no new mandatory inputs to inherited operations (per A.6.1:4.2.1 / CC‑UM.8).
* **Transport**: declarative transport semantics (no hidden crossings; crossings are surfaced via Bridges where required).
* **Audit obligations**: which evidence anchors must exist when the mechanism is used.

If the mechanism introduces new slot kinds shared across a family/suite, apply E.20:4.5.

#### E.20:4.5 - Step 5: SlotKind lexicon discipline (prevent slot drift)

If the mechanism belongs to a suite or family where multiple member mechanisms share slot vocabulary:

1. The suite owner SHALL provide a **suite-level SlotKind lexicon** (or update it if already present) in the suite owner’s canonical location (`A.6.7` / `A.6.7.<FamilyKey>`), or as a dedicated lexicon card explicitly referenced from there.
2. Mechanism cards SHALL cite slot kinds from that lexicon (rather than minting local near-duplicates).
3. New slot kinds SHALL be introduced into the lexicon first, then referenced by member mechanisms. If any citeable `SlotKind` tokens are minted/renamed, apply E.20:4.9.

This step is specifically intended to prevent the “same idea, different slot token” drift that makes planned baselines and audits non‑portable.

#### E.20:4.6 - Step 6: Suite integration (if the mechanism is a suite member)

If the introduction affects a suite (`MechSuiteDescription` or specialization):

1. **Membership set semantics (WF‑MS‑1).** `mechanisms` is a set: duplicates are nonconformant and list order carries no semantics.
2. **Ordering is only in protocols.** If ordering matters, express it only in `suite_protocols`.
3. **Protocol closure (WF‑MS‑2).** If `suite_protocols` is present, then for every `ProtocolStep` in every `SuiteProtocol`, `step.mechanism ∈ mechanisms`.
4. **No hidden tails.** Required stages (e.g., normalization/aggregation/Γ‑fold) are explicit protocol steps; do not hide them inside other steps.
5. **Guard/gate separation.** Suites and mechanisms SHALL NOT publish `GateDecision`/`DecisionLog`. `AdmissibilityConditions` and tri‑state `GuardDecision` remain mechanism-owned; `OperationalGate(profile)` acceptance thresholds and pass/fail criteria remain gate/acceptance-level concerns.
6. **Suite is descriptive only (WF‑MS‑3/4).** Any publish/telemetry continuation is outside the suite protocol and terminates via publication surfaces (packs/modules); suites SHALL NOT define mechanism blocks (`OperationAlgebra`, `LawSet`, `Transport`, `Audit`, …).

**Kernel stability rule (recommended).** If the suite is a kernel suite, and the change adds a new required stage, prefer creating a **suite variant** rather than mutating the kernel membership. If mutation is unavoidable, pair it with terminology continuity (E.20:4.9) and RSCR triggers (E.20:4.10).

#### E.20:4.7 - Step 7: Planned baseline & P2W seam (if planning is affected)

If the mechanism introduction changes what a WorkPlanning baseline must pin (e.g., selected comparator specs, method descriptions, time selector, guard pins):

1. Introduce or revise a `SlotFillingsPlanItem` specialization under the WorkPlanning owner.
2. The plan item SHALL remain planning-only:
   * pins/refs only (ByValue or `<RefKind>`),
   * no launch values,
   * no `FinalizeLaunchValues` witnesses,
   * no gate decisions or decision logs.
   * time is explicit: include `Γ_time_selector` or `Γ_time_rule_ref` (XOR); implicit “latest/current” is nonconformant.
3. The plan item SHALL target exactly one **Description-level, edition-addressable** slot owner via `target_slot_owner_ref` (typically a kit or suite) and SHALL NOT target a `U.Mechanism.IntensionRef`. If a “standalone mechanism baseline” is required, introduce an explicit Description-level slot-owner wrapper (e.g., a mech kit or a suite-of-one) and target that.

This step exists to keep the P2W seam crisp: planning defines **planned fillers**, enactment witnesses **actual runs**.

#### E.20:4.8 - Step 8: Wiring & SoTA updates (keep method evolution out of kernel)

If the introduction involves methods, comparators, selectors, or other SoTA-sensitive choices:

1. Put method/comparator family semantics in **SoTA packs** (G.2) and reference them by edition‑pinned refs.
2. Pin the chosen SoTA refs for a baseline in WorkPlanning plan items (E.20:4.7); wiring consumes pins rather than silently overriding them.
3. Put flow/task binding logic in **wiring modules** (`GPatternExtension`), with an explicit `PatternScopeId` and declared semantic owner.
4. If a SoTA update requires changing a mechanism’s signature/laws, that semantic change SHALL be performed in the mechanism card owner (A.6.1) and SHALL emit RSCR triggers (E.20:4.10).

#### E.20:4.9 - Step 9: Terminology continuity (alias docking)

If the introduction renames any public token or changes canonical naming:

1. Use lexical alias docking (F.18) so old tokens remain citeable.
2. Update registers and twin labels per lexical discipline.
3. Avoid silent rewrites: the MIP-run SHALL make the migration explicit.

#### E.20:4.9.1 - Deprecation / supersession / retirement (preserve citeability)

If the change class includes deprecation/supersession/retirement (E.20:4.1 #8), the MIP-run SHALL preserve reference continuity while making the status change explicit:

1. **Preserve the canonical target.** The deprecated artifact (mechanism card / suite description / plan item / wiring module) SHALL remain resolvable at its canonical location; deprecation MUST NOT be implemented by removal that would break citations.
2. **Keep the public token citeable.** The deprecated token (`…IntensionRef`, suite token, plan-item token, etc.) SHALL remain citeable. If a successor token/name is introduced, the old token SHALL be alias-docked per F.18 (E.20:4.9).
3. **Declare successor (or “no successor”).** The deprecated artifact SHALL declare a successor pointer (or explicitly declare that there is none) using the project’s established deprecation/supersession fields.
4. **Route downstream updates by owner.** Any required suite membership/protocol changes, WorkPlanning pins, or wiring changes SHALL be performed via their respective semantic owners (E.20:4.2), preferably by introducing a suite variant rather than silently swapping kernel membership.
5. **Emit RSCR triggers.** Deprecation/supersession SHALL emit typed RSCR triggers and extend the regression envelope (E.20:4.10), including checks for dangling refs and alias coverage.

#### E.20:4.10 - Step 10: RSCR triggers + regression envelope

A MIP-run that changes any of:
* mechanism signatures,
* suite membership/protocols,
* planned baseline pins,
* slot vocabulary / SlotKind lexicon,
* terminology/alias docking affecting citeable tokens,
* or other reference surfaces

SHALL emit typed RSCR triggers via the RSCR owner and SHALL extend the regression envelope to include, at minimum:

* no dangling `…IntensionRef` enumerations,
* suite membership set semantics + protocol closure,
* guard/gate separation preservation,
* P2W seam preservation (planning vs enactment).

**Guard (normative).** Trigger kind identifiers (e.g., `RSCRTriggerKindId`) SHALL be selected from the RSCR trigger catalogue owned in `G.Core`. A MIP-run SHALL NOT mint ad hoc trigger kinds (“reason kinds”) scattered in arbitrary patterns/modules.

**Manifest hook (recommended).** The MIP-run manifest SHOULD list emitted trigger types and the regression envelope deltas as checkable items.

#### E.20:4.11 - Step 11: Apply PQG profiles (E.19) and close the run

Every MIP-run SHALL be reviewed using PQG (E.19) with:

* **PCP‑BASE** always, and
* the triggered profiles implied by the change class (at least):
  * **PCP‑SUITE** if any suite surface changed,
  * **PCP‑P2W** if any planned-baseline surface changed,
  * **PCP‑TERM** if any new terms/renames are introduced,
  * **PCP‑SOTA** if SoTA packs are introduced/modified,
  * **PCP‑NORM** if the run introduces/changes normative requirements or conformance items,
  * **PCP‑DEONT** if RFC keyword clauses are introduced/modified (or if invariant/predicate vs deontic form is ambiguous),
  * **PCP‑BRIDGE** if cross-context reuse / crossings / bridges are introduced or changed,
  * **PCP‑REFRESH** if refresh-sensitive claims (SoTA lists, “current practice”, enumerations) are touched,
  * plus any applicable modularity / boundary / normativity profiles required by the delta.

**MIP-run outcomes (normative set).**
A reviewed MIP-run SHALL be closed as one of:

1. **Proceed (single change set).**
2. **Proceed via split routing** (mandatory when semantics were placed in the wrong owner; the change is split into owner-correct patches).
3. **Proceed via suite variant** (preferred when kernel stability is threatened by adding new required stages).
4. **Defer** (insufficient semantics; stub exists but completion is DRR-tracked).
5. **Reject** (violates invariants such as suite-as-gate, plan-as-enactment, or semantic owner ambiguity).

### E.20:5 - Archetypal Grounding *(Tell–Show–Show)*

|  | Tell | Show #1 — add a mechanism to an existing suite *variant* | Show #2 — introduce a new mechanism family + suite |
|---|---|---|---|
| **Scene** | Mechanisms evolve: new stages appear, methods mature, and planning surfaces must remain citeable. | A team wants an additional “stage” in a characterization pipeline, but does not want to mutate the kernel suite. | A new domain needs a mechanism kind not yet present in any existing mechanism-profile cluster (for characterization: `A.19.*`), plus a suite that composes several distinct mechanisms with a P2W hook. |
| **Owner routing** | Each artifact has one semantic owner; changes are routed, not smeared. | 1) Add the new mechanism card under the mechanism owner. 2) Add a suite variant under the suite owner. 3) Pin the variant via a planned-baseline specialization. 4) Wire the variant via a `GPatternExtension`. | 1) Add a new archetypal grounding under oner pattern. 2) Add `A.6.7.<FamilyKey>` describing the suite. 3) Add a suite-specific `SlotFillingsPlanItem` specialization. 4) Add SoTA packs + wiring modules. |
| **Card-first** | No suite enumerates a missing `…IntensionRef`. | Create the new `…IntensionRef` card stub first; then update the suite variant membership. | Create the new kind’s canonical card(s) first; then publish suite membership by `…IntensionRef`. |
| **Suite discipline** | Suites are descriptive: membership, obligations, pins, protocols; not mechanisms and not gates. | The variant’s `suite_protocols` explicitly names the new stage; publish/telemetry remains outside the suite. | The new suite defines shared obligations and allowed pipelines without embedding mechanism semantics. |
| **P2W seam** | Planning pins refs; enactment witnesses runs. | The plan item pins the chosen suite variant and any method/spec refs; no launch values or decision logs. | The plan item specialization defines the planned fillers/pins that downstream flows cite. |
| **SoTA updates** | Methods change faster than kernel meaning; wiring is where choices live. | A `GPatternExtension` selects a post-2015 scoring method by edition‑pinned ref; no kernel mutation required. | The family ships method packs and wiring modules; kernel cards remain the semantic source of mechanism meaning. |

### E.20:6 - Bias-Annotation

Lenses tested: **Governance** (semantic ownership, continuity), **Architecture** (boundary hygiene and modularity), **Onto/Epist** (meaning placement and type discipline), **Pragmatic authoring** (reviewability, split routing), **Didactic** (Tell–Show–Show training affordance).

### E.20:7 - Conformance Checklist (normative)

| ID | Requirement | Purpose |
|---|---|---|
| **CC‑E20‑1 (Owner routing declared).** | Every MIP-run **SHALL** provide a MIP-run manifest that lists each new/changed artifact → exactly one semantic owner → canonical location, and each artifact **SHALL** be authored in the owner’s canonical location. | Prevents “floating commitments” and semantic leakage. |
| **CC‑E20‑2 (Card-first canonicalization).** | Any new `U.Mechanism.IntensionRef` enumerated anywhere **SHALL** resolve to a canonical mechanism card (stub allowed) before suite/protocol enumeration. | Eliminates dangling refs. |
| **CC‑E20‑3 (Suite discipline preserved).** | If a suite is touched, it **SHALL** preserve: membership set semantics, protocol closure, no hidden tails, no gate decisions/logs, no publication payloads. | Prevents suite-as-gate and suite-as-mechanism drift. |
| **CC‑E20‑4 (SlotKind lexicon used when shared).** | If mechanisms share slot vocabulary in a family/suite, a suite-level lexicon **SHALL** exist and member mechanisms **SHALL** cite it. | Stops slot token drift. |
| **CC‑E20‑5 (P2W seam preserved).** | If planned baselines are touched, plan items **SHALL** remain WorkPlanning-only (pins/refs only), **SHALL** target exactly one Description-level slot owner via `target_slot_owner_ref` (and **SHALL NOT** target a `U.Mechanism.IntensionRef`), and **SHALL NOT** contain enactment witnesses, launch values, or gate decisions. | Keeps planning and enactment separable and auditable. |
| **CC‑E20‑6 (Kernel stability handled).** | If a kernel suite would gain a new required stage, the change **SHOULD** be expressed as a suite variant; if mutation occurs, it **SHALL** include continuity measures (alias docking and explicit delta). | Minimizes blast radius of kernel edits. |
| **CC‑E20‑7 (SoTA wiring, not kernel semantics).** | Method/comparator choices **SHALL** be represented via SoTA packs and wiring modules; if a SoTA update requires semantic change, it **SHALL** be made in the mechanism owner and not “by wiring”. | Prevents silent semantic shifts. |
| **CC‑E20‑8 (Terminology continuity).** | Any rename affecting citeable tokens **SHALL** use alias docking and register updates; silent rewrites are non‑conformant. | Preserves reference stability. |
| **CC‑E20‑9 (RSCR triggers + regressions).** | Any semantic or reference-surface change **SHALL** emit RSCR triggers and extend the regression envelope to cover dangling refs + suite closure + guard/gate separation + P2W seam. | Makes change impact explicit and testable. |
| **CC‑E20‑10 (PQG coverage).** | Every MIP-run **SHALL** be reviewed under PQG (E.19) with PCP‑BASE and the triggered profiles implied by the change. | Normalizes review and refresh. |
| **CC‑E20‑11 (Deprecation preserves citeability).** | Any deprecation/supersession/retirement action **SHALL** preserve citeability of the deprecated token (alias docking if renamed), keep the canonical artifact resolvable, and declare a successor pointer or “no successor” explicitly (E.20:4.9.1). | Prevents broken citations and orphaned semantics during evolution. |

### E.20:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | Symptom | Why it fails | Repair |
|---|---|---|---|
| **Wiring carries semantics** | Part G extensions start redefining what a mechanism “means”. | Meaning becomes edition-fragile and non-local. | Move semantics back to the mechanism owner; keep extensions as binding only. |
| **Suite becomes a meta-mechanism** | Suite text defines ops/laws or embeds thresholds/decisions. | Breaks level separation; creates hidden gate behavior. | Restore suite as description-only; push thresholds to acceptance/gate level. |
| **Plan becomes enactment** | Plan items contain launch values, witnesses, or decisions. | Destroys P2W seam; breaks audit semantics. | Strip enactment content; pin only refs/policies/time selectors. |
| **Kernel churn by convenience** | New required stage is added directly to kernel suite membership. | Expands blast radius; destabilizes citations. | Prefer suite variant; if not possible, pair with alias docking and explicit deltas. |
| **Token drift by silent rename** | “Just rename UNM to …” without aliasing. | Breaks citations and downstream reasoning. | Use F.18 alias docking; update registers explicitly. |
| **Owner ambiguity** | “We’ll put it somewhere later.” | Guarantees incompleteness and drift. | Declare owner up front; otherwise treat as non-normative. |

### E.20:9 - Consequences

**Benefits**
* Mechanism introductions become **trainable and reviewable** (a repeatable route map).
* Reduces drift by enforcing **single semantic ownership** and preventing semantic leakage.
* Keeps suites descriptive and the P2W seam crisp, improving auditability.
* Supports SoTA evolution without destabilizing kernel meaning.

**Costs**
* Introductions require more explicit routing artifacts (owner map, PQG coverage).
* Some changes will be split into multiple patches (by design), which increases authoring overhead.
* Kernel stability discipline can feel “slow” when a team wants a quick mutation.

### E.20:10 - Rationale

Mechanisms are high-leverage semantic units: a small change can affect suites, planned baselines, wiring modules, and audits. Without a protocol, the corpus tends toward **semantic smearing** (meaning duplicated across planes) and **non-local correctness** (you can’t know what changed without reading everything).

Owner‑routed authoring is a pragmatic compromise: it does not require tooling, yet it produces a stable “map of truth” that makes future review and refresh feasible.

### E.20:11 - SoTA-Echoing

| Need | SoTA practice (post‑2015) | Primary source (post‑2015) | How MIP aligns |
|---|---|---|---|
| Explicit concerns and viewpoints for architecture evolution | Architecture descriptions separate concerns, viewpoints, and stakeholder needs | ISO/IEC/IEEE 42010:2022 | MIP forces explicit owner routing and separates semantic planes (kernel vs wiring vs planning). |
| Repeatable evaluation of pattern quality and change admission | Pattern validation uses explicit criteria and review profiles | Riehle et al., 2020 | MIP requires PQG coverage with triggered profiles rather than ad hoc review. |
| Grounding abstract guidance in teachable vignettes | Pattern languages emphasize grounded, repeatable “Tell–Show–Show” teaching | Iba, 2021 | MIP includes archetypal grounding to make the protocol teachable. |
| Bounded context ownership and boundary hygiene | Context mapping emphasizes ownership and explicit boundary contracts | Vernon, 2016 | MIP’s owner route map is a boundary discipline applied to spec authoring. |
| Modular vocabularies for knowledge systems | Knowledge graph practice emphasizes modular vocabulary control and stable identifiers | Hogan et al., 2021 | MIP’s lexicon discipline + alias docking preserve stable references under evolution. |

### E.20:12 - Relations

**Builds on:**
* **E.8** (pattern structure and normative authoring discipline)
* **E.10 / F.17–F.18** (lexical registers, twin labels, alias docking)
* **E.19** (PQG/PCP profile-based review)
* **E.15** (evolution discipline; DRR/edition thinking)

**Coordinates with:**
* **A.6.1** (`U.Mechanism.Intension` ownership)
* **A.6.7** (`MechSuiteDescription` integrity)
* **A.15.3** (`SlotFillingsPlanItem` and planned baseline seam)
* **E.18** (E.TGA flows that cite planned baselines)
* **G.Core** (RSCR trigger catalogue)
* **G.2** (SoTA synthesis packs)
* **G.x:Ext.\*** (wiring modules via `GPatternExtension`)

**Constrains:**
* Any change set that introduces or revises mechanisms, suites, planned baselines, or wiring in a way that affects citeable surfaces.

### E.20:End

