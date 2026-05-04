## G.1 - CG‑Frame‑Ready Generator

**Tag.** architectural pattern; *generator chassis* (design‑time kit / authoring scaffold)  
**Status.** stable (Phase‑2 universalisation)  
**Normativity.** normative, except sections explicitly marked *informative*  
**Stage.** *design‑time* authoring of a generator‑kit with a *run‑time* execution façade (policy‑governed; edition‑aware)  
**Primary output.** the **six‑card chassis** `M1…M6` published as a **complete, reusable CG‑Frame kit**, plus a versioned **kit manifest** `CGKitId` that binds the six cards as a single reusable unit (view‑friendly inventory + wiring surface)  
**Primary hooks.** see **§12 Relations** (notably `G.Core`, `G.0`, `G.2`, `G.5`, `G.10`, `G.11`)  
**Working‑model first (informative).** prefer working models and didactic micro‑examples; escalate to formal harnesses only when risk warrants (per E.8).  
**Non‑duplication note.** universal Part‑G invariants (tri‑state guard, set‑return, penalties→`R_eff`‑only, crossing visibility, typed RSCR triggers, default ownership, P2W split, linkage discipline, shipping boundary) are **single‑owner in `G.Core`** and are **only cited** here.

### G.1:1 - Problem frame

You are authoring a **CG‑Frame** and want a **repeatable scaffold** that connects:

* a declared **scope anchor** (`CG‑FrameContext`, `describedEntity`, contract surfaces),
* a **local SoTA set** (scoped and provenance‑anchored),
* a **variant pool** (candidate ideas / decision options / method variants),
* a **shortlist** (a set/portfolio outcome, not a forced singleton),
* **publication‑ready bindings** into Part‑F artefacts (UTS rows, Name Cards, RSCR tests, worked examples),
* and **refresh readiness** (telemetry hooks + RSCR wiring) without redefining refresh or shipping.

This pattern is intentionally **a chassis**, not a method specification:

* harvesting semantics live in `G.2`,
* selection/dispatch semantics live in `G.5`,
* CHR/CAL payload semantics live in `G.3` / `G.4`,
* shipping ownership lives in `G.10`,
* refresh orchestration ownership lives in `G.11`.

### G.1:2 - Problem

Without a chassis, CG‑Frame authoring tends to fail in repeatable ways:

* **SoTA is not locally scoped**: inputs are “in the air”, not a reconstructible set.
* **Generation is ad‑hoc**: variant candidates are emitted without a stable trace of why/when/how.
* **Selection is opaque**: eligibility/acceptance and assurance are not pinned to explicit surfaces.
* **Outputs don’t land in reusable surfaces**: no clean hand‑off into UTS / RoleDescription / Concept‑Sets / RSCR.
* **No kit‑level snapshot**: the scaffold lacks a versioned manifest, so downstream can’t reliably cite “which chassis edition” was used.
* **Refresh is unplanned**: there is no canonical wiring from edits/telemetry/decay to RSCR causes along the P2W path.

### G.1:3 - Forces

* **Breadth vs. precision:** harvest wide enough to avoid local dogma, but keep the artefact actionable.
* **Generativity vs. assurance:** encourage novelty while keeping evidence, legality, and trust inspectable.
* **Local meaning vs. portability:** keep meaning local by default; crossing must be explicit and auditable.
* **Expressiveness vs. parsimony:** resist inventing new types/slots; prefer reuse and explicit wiring.
* **Stability vs. evolution:** keep stable IDs and pins while allowing SoTA, policies, and editions to evolve.
* **Didactic clarity vs. normative minimalism:** authors need a concrete scaffold, but universal invariants must not be duplicated outside `G.Core`.

### G.1:4 - Solution

#### G.1:4.1 - G.Core linkage (normative)

```
// Canonical form: see G.Core (Nil‑elision + Expansion rule for profiles/sets/pin‑sets).
GCoreLinkageManifest := ⟨
  CoreConformanceProfileIds := {
    GCoreConformanceProfileId.PartG.AuthoringBase,
    GCoreConformanceProfileId.PartG.TriStateGuard,
    GCoreConformanceProfileId.PartG.UTSWhenPublicIdsMinted,
    GCoreConformanceProfileId.PartG.ShippingBoundary
  },

  CorePinSetIds := {
    GCorePinSetId.PartG.AuthoringMinimal,
    GCorePinSetId.PartG.CrossingVisibilityPins
  },

  // Prefer sets; use deltas for pattern‑specific additions.
  RSCRTriggerSetIds := { GCoreTriggerSetId.SoTAHarvestSynthesis },
  RSCRTriggerKindIds := { RSCRTriggerKindId.BaselineBindingEdit },

  // Pattern‑owned kit identifiers (the “six cards”).
  CorePinsRequired := {
    SoTAPaletteDescriptionId,
    SoTA_SetId,
    VariantPoolId,
    ShortlistId,
    CGFrameLibraryId,
    RefreshReadinessCardId,
    CGKitId,

    // Local pointer-map surface for vocabulary + observables-to-CHR anchoring.
    // (May cite `G.0:CG‑Spec.ReferenceMap`; do not duplicate semantics.)
    ReferenceMap,

    // RSCR regression tests used by the chassis (if any).
    RSCRTestId[]?,

    // When the chassis is bound into WorkPlanning (P2W): planned baseline refs.
    SlotFillingsPlanItemRef[]?
  },

  // Consumed defaults (single‑owner; this pattern only cites owners via `G.Core.DefaultOwnershipIndex`).
  DefaultsConsumed := {
    DefaultId.GammaFoldForR_eff,   // owner: CC‑G5.4
    DefaultId.PortfolioMode,       // owner: CC‑G5.23
    DefaultId.DominanceRegime      // owner: CC‑G5.28
  }
⟩
```

**Routing rule (normative):** the semantics of `CC‑GCORE‑*`, `RSCRTriggerKindId.*`, and `DefaultId.*` are **single‑owner** in their canonical owners (primarily `G.Core`, and for the defaults above the owners listed in `G.Core.DefaultOwnershipIndex`). `G.1` MUST NOT restate or redefine those semantics.

#### G.1:4.2 - Six‑module generator chassis (normative)

**Core artefact:** `CGFrameReadyGeneratorKit := ⟨M1, M2, M3, M4, M5, M6⟩`, where each `Mi` is a **card** with an explicit I/O surface and stable identifiers.
`CGKitId` identifies the versioned **kit manifest** (`CG‑Kit@CG‑Frame`) that lists the six card ids and the minimal wiring pins needed to treat the chassis as a reusable unit (this is **not** a shipping pack; shipping remains owned by `G.10`).

The chassis is *view‑friendly*: it is an inventory of “what exists and how it is wired”, not a second specification of CN/CG/CHR/CAL/selection semantics.

##### M1 — CG‑FrameContext Card (scope anchor)

**Owns (kit surface):**

* `CG‑FrameContext` and its **binding pins**:

  * `describedEntity := ⟨GroundingHolon, ReferencePlane⟩` *(pin set: `PartG.AuthoringMinimal`)*
  * `CNSpecRef.edition`, `CGSpecRef.edition` *(pin set: `PartG.AuthoringMinimal`)*
  * `ReferenceMap` *(cite `G.0:CG‑Spec.ReferenceMap`; do not duplicate semantics)*
  * any declared crossing/policy pins *(pin set: `PartG.CrossingVisibilityPins`)*

**Purpose:** provide the *single scope anchor* used by all downstream cards.

**Notes:** any contract/legality content is **cited** via `A.19 (CN‑Spec)` and `G.0 (CG‑Spec)` (delegation target: `CC‑GCORE‑CN‑CG‑1` via `CC‑G1‑CoreRef`); this card does not introduce a local “mini‑spec”.

##### M2 — SoTA_Set@CG‑Frame (harvester output card)

**Owns (kit surface):**

* `SoTAPaletteDescriptionId` and `SoTA_SetId` bound to `CG‑FrameContext`
* explicit provenance anchors for the set (via `A.10`), and any published UTS stubs/rows when applicable

**Semantic owner:** harvesting discipline and SoTA‑pack payload are owned by `G.2`.
In `G.1`, M2 is a *slot in the chassis* and a wiring surface; it does not redefine the harvesting method.

##### M3 — VariantPool (candidate inventory + emitter trace)

**Owns (kit surface):**

* `VariantPoolId` bound to `CG‑FrameContext`
* per‑candidate minimal traceability fields (emitter identity, `EmitterPolicyRef` (policy‑id/ref; owner‑defined), method/generator refs when declared, edition pins, provenance anchors)
* optional, per‑candidate **assurance preview pointers** (e.g., `PathSliceId?` and/or `SCRId?` when early assurance is recorded) and optional **QD/Open‑Ended scaffolding stubs** (only when introduced by explicit `GPatternExtension` blocks)

**Guardrails (via G.Core):**

* tri‑state eligibility handling, penalties routing, crossing visibility, and set‑return constraints are not defined here; they are enforced via `G.Core` conformance.

**Semantic owner of method payload:** method‑specific emitter semantics live in `Extensions` (e.g., `C.17`, `C.18`, `C.19`).
M3 MUST remain method‑agnostic in its core definition: it is an inventory surface, not an algorithm spec.

##### M4 — Shortlist (selector/assurer output)

**Owns (kit surface):**

* `ShortlistId` bound to `CG‑FrameContext`
* a portfolio/set of selected candidates plus rationale/assurance surfaces (`SCRId` required; `DRRId` optional; cite `PathId/PathSliceId` when applicable)
* optional **front/archive metadata** needed for reproducibility when used: ε‑front parameters and/or archive snapshot hooks, with ownership routed via `G.5` / `C.18` / `C.19` (no local semantics in `G.1`)

**Semantic owner:** selection/dispatch semantics are owned by `G.5`.
M4 MUST preserve *set‑return semantics* (as routed by `G.Core`) and MUST NOT hard‑code a forced singleton outcome.

##### M5 — CG‑FrameLibrary (published bindings index)

**Owns (kit surface):**

* `CGFrameLibraryId` bound to `CG‑FrameContext`
* an index of referenced CG‑Frame artefacts ready for reuse:

  * CHR/CAL/LOG bundles (by their ids; semantics owned by `G.3`, `G.4`, `G.8`)
  * published identifiers (UTS rows, Name Cards) per Part‑F owners
  * additional Part‑F binding surfaces (e.g., RoleDescription templates, Concept‑Set rows) by owner‑ids only
  * RSCR test identifiers (e.g., from `F.15`) and worked examples (where applicable)

**Boundary:** M5 is a **kit/library surface**, not shipping. If a shipped pack is needed, ownership is `G.10`.

##### M6 — RefreshReadiness Card (telemetry hooks + wiring)

**Owns (kit surface):**

* `RefreshReadinessCardId` bound to `CGFrameLibraryId` (and thus to `CG‑FrameContext`)
* `CGKitId` (the versioned kit manifest) binding `M1…M6` into a single reusable unit; it MUST enumerate the card ids and MAY carry references to deprecations/edition bumps minted by the canonical owners
* declared telemetry hooks (what signals are observed, with what pins)
* declared RSCR wiring: which `RSCRTriggerKindId` are relevant (canonical ids), with minimal required payload pins (including `SlotFillingsPlanItemRef[]` when the chassis is bound into WorkPlanning)

**Boundary:** orchestration semantics are owned by `G.11`.
M6 prepares *refresh‑readiness metadata* and wiring stubs; it does not define scheduling/priority heuristics.

#### G.1:4.3 - Minimal I/O surface (normative)

| Module | Consumes                                                                    | Produces                                                                               |
| ------ | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| M1     | CG‑Frame brief + `describedEntity` + `CNSpecRef/CGSpecRef` (edition‑pinned) | `CG‑FrameContext` + context pins                                                       |
| M2     | discovery inputs + inclusion criteria *(via G.2)*                           | `SoTA_SetId` (+ provenance anchors; optional UTS stubs/rows)                           |
| M3     | `SoTA_SetId` + local constraints + emitter policy pins *(via Extensions)*   | `VariantPoolId` (+ candidate trace/provenance; optional method payload via Extensions) |
| M4     | `VariantPoolId` + acceptance/eligibility surfaces *(via G.4/G.5)*           | `ShortlistId` (portfolio/set) + rationale refs                                         |
| M5     | `ShortlistId` + CHR/CAL/LOG bundle refs + UTS/Name refs                     | `CGFrameLibraryId` (library index; publish‑ready bindings)                             |
| M6     | telemetry inputs + freshness/decay policy pins + RSCR tests                 | `CGKitId` + `RefreshReadinessCardId` (wiring to `G.11`; no orchestration ownership)    |

#### G.1:4.4 - Extensions (pattern‑scoped; non‑core)

All method/discipline/generator specifics MUST be expressed as `GPatternExtension` blocks.

> Guard: `G.1:Ext.*` are **PatternScopeId** values (internal, pattern‑scoped), not new patterns and not new `PatternId`.

##### GPatternExtension — `G.1:Ext.HarvesterWiring`

**PatternScopeId:** `G.1:Ext.HarvesterWiring`
**GPatternExtensionId:** `HarvesterWiring`
**GPatternExtensionKind:** `GeneratorSpecific`
**SemanticOwnerPatternId:** `G.2`
**Uses:** `{G.2}`
**⊑/⊑⁺:** `∅`
**RequiredPins/EditionPins/PolicyPins (minimum):**

* `SoTAPaletteDescriptionId`
* `SoTA_SetId`
* `ClaimSheetId[]` / `BridgeMatrixId` *(as referenced by the chosen G.2 pack form)*
* `CNSpecRef.edition`, `CGSpecRef.edition` *(already required via `GCorePinSetId.PartG.AuthoringMinimal`)*
**RSCRTriggerSetIds:** `{GCoreTriggerSetId.SoTAHarvestSynthesis}`
**Notes (wiring‑only):** harvesting semantics (living review funnels, inclusion policy families, SoS indicator families, etc.) are defined by `G.2` and are not duplicated in `G.1`.

##### GPatternExtension — `G.1:Ext.ShortlistWiring`

**PatternScopeId:** `G.1:Ext.ShortlistWiring`
**GPatternExtensionId:** `ShortlistWiring`
**GPatternExtensionKind:** `MethodSpecific`
**SemanticOwnerPatternId:** `G.5`
**Uses:** `{G.5, G.4}`
**⊑/⊑⁺:** `∅`

**RequiredPins/EditionPins/PolicyPins (minimum):**

* `ShortlistId`
* `SCRId` *(assurance/rationale surface by id; semantics owned by the selector/assurance owners)*
* `DRRId?` *(when a decision‑rationale artefact is minted; otherwise omitted)*
* `TaskSignatureRef?` *(if selection is task‑templated; otherwise omitted)*
* `AcceptanceClauseId[]` *(as referenced from `G.4` outputs)*
* any explicit selector policy pins *(policy‑id/ref; owner‑defined)* when not defaulted (default ownership is routed via `G.Core.DefaultOwnershipIndex`)

**Notes (wiring‑only):** `G.1` does not redefine selection: it binds M4’s output surface to the `G.5` selector/dispatcher kernel.

##### GPatternExtension — `G.1:Ext.CreativityCHR`

**PatternScopeId:** `G.1:Ext.CreativityCHR`
**GPatternExtensionId:** `CreativityCHR`
**GPatternExtensionKind:** `DisciplineSpecific`
**SemanticOwnerPatternId:** `C.17`
**Uses:** `{C.17, G.3}`
**⊑/⊑⁺:** `∅`
**RequiredPins/EditionPins/PolicyPins (minimum):**

* `CHRPackId?` *(if creativity characteristics are published/typed)*
* edition/policy pins required by the chosen creativity characteristic set (owned by `C.17`)

**Notes (wiring‑only):** `G.1` only records which creativity characteristics are used for M3/M4 wiring; legality/typing lives in the CHR owners.

##### GPatternExtension — `G.1:Ext.NQD`

**PatternScopeId:** `G.1:Ext.NQD`
**GPatternExtensionId:** `NQD`
**GPatternExtensionKind:** `MethodSpecific`
**SemanticOwnerPatternId:** `C.18`
**Uses:** `{C.18, C.19}`
**⊑/⊑⁺:** `∅`
**RequiredPins/EditionPins/PolicyPins (minimum):**

* `DescriptorMapRef.edition`
* `DistanceDefRef.edition`
* `InsertionPolicyRef` *(policy id / ref, as defined by the owner)*
* `TaskSignatureRef?` *(when QD is enabled via TaskSignature flags/traits rather than by an external switch)*
* `DHCMethodRef.edition?` *(when illumination/coverage summaries are pinned to a method)*
* `EmitterPolicyRef` *(policy‑id/ref; points to the exploration governance owner, e.g., `C.19` when E/E‑LOG is used)*

**RSCRTriggerKindIds:** `{RSCRTriggerKindId.EditionPinChange, RSCRTriggerKindId.PolicyPinChange, RSCRTriggerKindId.TelemetryDelta, RSCRTriggerKindId.FreshnessOrDecayEvent}`

**Notes (wiring‑only):** QD/QD‑adjacent algorithm families and their parameterisations belong to `C.18/C.19`; `G.1` only fixes the pins needed to make the VariantPool and Shortlist reproducible.

##### GPatternExtension — `G.1:Ext.OpenEndedFamilyWiring`

**PatternScopeId:** `G.1:Ext.OpenEndedFamilyWiring`
**GPatternExtensionId:** `OpenEndedFamilyWiring`
**GPatternExtensionKind:** `GeneratorSpecific`
**SemanticOwnerPatternId:** `G.2` *(family semantics live in SoTA cards; this block only wires pins; selector‑side wiring is owned by `G.5`.)*
**Uses:** `{G.2, G.5, C.19, C.23}`
**⊑/⊑⁺:** `∅`
**RequiredPins/EditionPins/PolicyPins (minimum):**

* `GeneratorFamilyId[]`
* `TransferRulesRef.edition` *(mandatory when Open‑Ended is enabled)*
* `EnvironmentValidityRegionRef?`
* `CoEvoCouplerRef[]?`
* `SoSLogBranchId[]?` *(when validity of generated tasks is gated by explicit branches)*

**RSCRTriggerKindIds:** `{RSCRTriggerKindId.EditionPinChange, RSCRTriggerKindId.PolicyPinChange, RSCRTriggerKindId.TelemetryDelta, RSCRTriggerKindId.FreshnessOrDecayEvent}`

**Notes (wiring‑only):** this block enables portfolios of `{Environment, MethodFamily}` pairs without redefining generator semantics in `G.1`; it should cite/align with the selector‑side wiring in `G.5:Ext.OpenEndedFamilyWiring`.

##### GPatternExtension — `G.1:Ext.RefreshWiring`

**PatternScopeId:** `G.1:Ext.RefreshWiring`
**GPatternExtensionId:** `RefreshWiring`
**GPatternExtensionKind:** `GeneratorSpecific`
**SemanticOwnerPatternId:** `G.11`
**Uses:** `{G.11}`
**⊑/⊑⁺:** `∅`
**RequiredPins/EditionPins/PolicyPins (minimum):**

* `RefreshReadinessCardId`
* `RSCRTestId[]`
* canonical `RSCRTriggerKindId[]` emitted/recorded (aliases only as labels, if any)
**RSCRTriggerSetIds:** `{GCoreTriggerSetId.RefreshOrchestration}`
**Notes (wiring‑only):** M6 declares readiness and wiring; orchestration semantics (queueing, prioritisation, cadence) are owned by `G.11`.

##### GPatternExtension — `G.1:Ext.ShippingWiring`

**PatternScopeId:** `G.1:Ext.ShippingWiring`  
**GPatternExtensionId:** `ShippingWiring`  
**GPatternExtensionKind:** `GeneratorSpecific`  
**SemanticOwnerPatternId:** `G.10`  
**Uses:** `{G.10}`  
**⊑/⊑⁺:** `∅`  
**RequiredPins/EditionPins/PolicyPins (minimum):**

* `CGFrameLibraryId`
* `SoTAPaletteDescriptionId`, `SoTA_SetId`
* `CHRPackId?`, `CALPackId?`, `SoS‑LOGBundleId?`, `ParityReportId?` *(as present in the library index)*
* `EvidenceGraphId?`, `BridgeMatrixId?`, `BridgeCalibrationTableId?` *(when cited by the shipped artefacts)*
* `UTSRowId[]?` *(when any public ids are minted/published)*
* `SlotFillingsPlanItemRef[]?` *(when planned baseline is bound by id into the shipment surface)*
**Notes (wiring‑only):** this block does not define shipping; it only records the minimum wiring from the chassis/library index to `G.10` when shipping is performed.

### G.1:5 - Archetypal Grounding — Tell–Show–Show (informative)

**Tell.** Use the six‑card chassis to make a CG‑Frame authoring effort reproducible: a scoped SoTA set, a traceable candidate pool, a set‑return shortlist, a publishable library index, and refresh readiness—without redefining contract/legality/selection/refresh owners.

**Show A (R&D multi‑criteria decisions; post‑2015 SoTA workflow).**

* **M1:** define `CG‑FrameContext` for “R&D decision options”, pin `CNSpecRef/CGSpecRef` editions, and publish `describedEntity` + `ReferencePlane`.
* **M2:** build `SoTA_SetId` via `G.2` using a living‑review style funnel (e.g., PRISMA‑like trace + update cadence) and publish UTS stubs for reusable constructs.
* **M3:** emit a `VariantPoolId` where each candidate cites its emitter policy and provenance; if QD is used, wire `DescriptorMapRef.edition` and `DistanceDefRef.edition` via `G.1:Ext.NQD`.
* **M4:** produce `ShortlistId` as a portfolio set via `G.5`, with acceptance predicates sourced from `G.4`.
* **M5:** publish a `CGFrameLibraryId` indexing the chosen CHR/CAL/LOG bundles and UTS rows; register RSCR tests.
* **M6:** declare refresh readiness (telemetry pins + canonical RSCR trigger kinds) and wire to `G.11`.

**Show B (clinical operations; safety‑first acceptability).**

* **M1:** scope a CG‑Frame around dose adjustment decisions; pin legality and evidence minima explicitly.
* **M2:** harvest SoTA models and safety constraints as a reconstructible set (owned by `G.2`).
* **M3:** generate policy‑constrained candidate protocols; emitter trace and evidence pins are mandatory.
* **M4:** shortlist remains a set; “choose one” is deferred to explicit policy, not silently baked into the generator.
* **M5/M6:** publish and wire refresh (decay events, policy changes, and evidence updates retrigger along the P2W path).

### G.1:6 - Bias‑Annotation (informative)

* **Recency bias:** “newest paper wins” (mitigate with explicit inclusion criteria and update cadence in `G.2` wiring).
* **Novelty bias:** over‑rewarding novelty at the expense of legality/assurance (mitigate by making acceptance and assurance pins explicit and owned).
* **Algorithmic favoritism:** baking a preferred generator into “the chassis” (mitigate by keeping M3 method‑agnostic and pushing methods into Extensions).
* **Scalarisation bias:** collapsing portfolios/partial orders into a single score (mitigate by set‑return discipline routed via `G.Core`).
* **Hidden‑crossing bias:** implicit reuse across contexts (mitigate by explicit crossing pins and Bridge‑only routing via `G.Core`).

### G.1:7 - Conformance Checklist (normative)

| ConformanceId     | Statement   |
| ----------------- | ----------- |
| **CC‑G1‑CoreRef** | The pattern MUST satisfy the **effective** `CoreConformanceIds` implied by `G.1:4.1` (`GCoreConformanceProfileId` expansion + deltas), per `G.Core` expansion rules.   |
| CC‑G1‑01          | The deliverable MUST include all six cards `M1…M6` with stable ids **and** a versioned kit manifest `CGKitId`, including at minimum: `{CGKitId, CG‑FrameContext, SoTAPaletteDescriptionId, SoTA_SetId, VariantPoolId, ShortlistId, CGFrameLibraryId, RefreshReadinessCardId}`.  |
| CC‑G1‑02          | `M1` MUST bind the kit to a single `CG‑FrameContext` and MUST expose the required pins from `GCorePinSetId.PartG.AuthoringMinimal` (including `describedEntity` and `CNSpecRef/CGSpecRef` editions). `M1` MUST also expose (or explicitly cite) a `ReferenceMap` surface and MUST NOT restate its semantics (cite `G.0:CG‑Spec.ReferenceMap`).  |
| CC‑G1‑03          | `M2` MUST be wired to `G.2` (or explicitly cite the `G.2` owner artefacts) and MUST be reconstructible as a scoped set, including `SoTAPaletteDescriptionId` + `SoTA_SetId` (not free‑floating prose). Provenance MUST be anchored via `A.10` for the emitted set.  |
| CC‑G1‑04          | `M3` MUST record emitter provenance as a wiring surface, including `EmitterPolicyRef` (policy‑id/ref), edition pins, and provenance anchors (via `A.10`). Any method‑specific fields MUST be introduced only via `GPatternExtension` blocks.   |
| CC‑G1‑05          | `M4` MUST be wired to `G.5` (or explicitly cite `G.5` owner artefacts) and MUST preserve set/portfolio outcomes. `SCRId` MUST be present (or explicitly cited to the owner surface) so assurance is id‑addressable; `DRRId` SHOULD be present when a decision‑rationale artefact is minted.   |
| CC‑G1‑06          | `M5` MUST publish a library/index surface that points to referenced CHR/CAL/LOG artefacts and to any minted public ids (`UTSRowId[]`, Name Cards) via the canonical owners (Part F), without introducing shadow specs (delegation target: `CC‑GCORE‑CN‑CG‑1` via `CC‑G1‑CoreRef`).    |
| CC‑G1‑07          | `M6` MUST publish `CGKitId` and expose refresh‑readiness wiring: canonical `RSCRTriggerKindId[]` applicability + minimal payload pins (including `SlotFillingsPlanItemRef[]` when applicable) and RSCR test ids; orchestration semantics MUST be cited to `G.11`.  |
| CC‑G1‑08          | Any method/discipline/generator specificity in `G.1` MUST be located in `G.1:4.4` as `GPatternExtension` blocks with `PatternScopeId`, `GPatternExtensionKind`, and `SemanticOwnerPatternId` (or `owner TBD` only for Phase‑3 seeds). If QD/illumination or Open‑Ended generator families are declared, the corresponding extension blocks MUST be present and MUST carry the owner‑required edition/policy pins. |


### G.1:8 - Common Anti‑Patterns and How to Avoid Them (informative)

* **Anti‑pattern: “Shadow CN/CG spec inside the chassis.”**
  *Avoid:* keep CN/CG as cited contract surfaces; use pins and owner references only.

* **Anti‑pattern: “Chassis hard‑codes a favourite algorithm.”**
  *Avoid:* keep M3 core method‑agnostic; add algorithm families only via Extensions with explicit owner patterns and edition pins.

* **Anti‑pattern: “Shortlist = one winner.”**
  *Avoid:* preserve set/portfolio returns; any singleton choice must be an explicit downstream decision rule (policy‑bound).

* **Anti‑pattern: “Refresh plan described as prose triggers.”**
  *Avoid:* record canonical `RSCRTriggerKindId` and payload pins; aliases only as labels and only if docked.

* **Anti‑pattern: “Packaging implies shipping ownership.”**
  *Avoid:* treat M5 as a library index; treat M6 as readiness wiring; ship only via `G.10`.

### G.1:9 - Consequences (informative)

* **Repeatable authoring:** CG‑Frame work becomes reconstructible: what exists, what it depends on, and how it is refreshed.
* **Method pluralism with discipline:** multiple generator/selector families can coexist without turning the chassis into a shadow method spec.
* **Better reuse:** outputs land directly in published artefacts (UTS/Name/RSCR‑ready) rather than remaining local notes.
* **Lower refactor cost:** method changes localise to Extensions; core invariants remain stable and single‑owner.

### G.1:10 - Rationale (informative)

* **Why six cards?** It matches the minimal decomposition needed to keep scope, harvesting, generation, selection, publication, and refresh **explicitly separable** (and thus auditable and evolvable).
* **Why “kit/index” rather than “pack”?** A CG‑Frame authoring effort must stay modular; shipping is a separate ownership boundary (`G.10`).
* **Why push method content into Extensions?** It prevents conflating (i) universal invariants, (ii) frame‑specific kit surfaces, and (iii) method/generator families—supporting Phase‑2 universalisation goals.
* **Why working‑model first?** Many CG‑Frames fail due to premature formalism; a chassis with didactic micro‑examples improves correctness of pins, names, and boundaries before deep formalisation.

### G.1:11 - SoTA‑Echoing (informative)

This chassis is designed to stay compatible with modern (post‑2015) practice without confusing “SoTA” with “currently popular”:

* **Evidence synthesis:** living systematic review workflows (e.g., PRISMA‑style traceability and update cadence) map naturally to M2 wiring owned by `G.2`.
* **Quality‑Diversity and archives:** modern QD families (MAP‑Elites‑class, CMA‑ME‑class, and related archive‑based exploration) fit as M3/M4 extensions (`C.18`/`C.19`) because they require explicit descriptor/distance/insertion pins and preserve set‑valued outcomes.
* **Open‑ended exploration:** post‑2015 open‑endedness systems (POET‑class, paired/adversarial environment generation lines, and modern curriculum‑generation approaches) fit when treated as generator‑family wiring (owned elsewhere) rather than as chassis semantics.
* **Set‑valued decision outputs:** modern multi‑objective and set‑valued evaluation practices align with the `G.Core` set‑return discipline, preventing hidden scalarisation.
* **Governed traceability:** contemporary reproducibility and accountability norms (mechanism disclosure, provenance anchors, and audit trails) are supported via pinned policies/editions and explicit module boundaries, without introducing data‑governance machinery.

### G.1:12 - Relations

**Builds on:** `G.Core`, `E.8`, `E.10`, `E.19`.
**Uses:** `A.10 (Provenance Anchors)`, `A.15.3 (SlotFillingsPlanItem)`, `A.19 (CN‑Spec)`, `G.0 (CG‑Spec)`, `G.2 (SoTA Synthesis Pack)`, `G.3 (CHR Pack@CG‑Frame)`, `G.4 (CAL Pack@CG‑Frame)`, `G.5 (Selector & Dispatch)`, `G.10 (Shipping)`, `G.11 (Refresh Orchestration)`, and (via Extensions) `C.17/C.18/C.19`.
**Publishes to / consumes from:** Part‑F publication surfaces (UTS, naming, RSCR tests, Role/Concept artefacts) as cited by their owners.

### G.1:End

