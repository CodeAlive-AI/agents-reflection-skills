## G.4 - CAL Authoring for a CG-Frame: Operators, Acceptance Clauses, Evidence Wiring

**Tag.** Architectural pattern (publishes `CAL Pack@CG-Frame`; consumes `CHR Pack@CG-Frame`; constrains selector/dispatcher usage; binds GateCrossing discipline; exposes `ReferencePlane` and penalty/guard policy pins to `SCR`)

**Stage.** design‑time (authoring & publication; enables lawful run‑time evaluation)

**Primary output.** A notation‑independent `CAL Pack@CG-Frame` containing:
`CAL.Charter@Context`, `CAL.Operator[]`, `CAL.Acceptance[]`, `CAL.Flow[]`,
`CAL.EvidenceProfiles`, `CAL.ProofLedger`, **optional** `CAL.NQD[]` (when declared),
UTS entries (Name Cards + twin labels + lifecycle notes incl. deprecations and lexical‑continuity notes),
RSCR tests, Worked‑Examples, and a `TaskMap@Context` (`TaskMap`; handoff surface consumed by `G.5`).

**Primary hooks.** `G.Core` (Part‑G invariants + RSCR trigger catalogue + default ownership index), `G.1` (CG‑FrameContext), `G.2` (SoTA Synthesis Pack), `G.3` (CHR Pack), `G.0` (CG‑Spec legality gate), `A.19` (CN‑Spec), `A.18` (CSLC), `A.10` (provenance anchors), `B.3` (trust / freshness / decay), `E.18` + `A.21` + `A.27` (GateCrossing / CrossingSurface harnesses), `F.9` (BridgeCard / CL), `G.6` (EvidenceGraph / PathId / PathSliceId; wired via Extensions), `G.5` (Selector & Dispatch), `G.10` (shipping), `G.11` (refresh orchestration), plus Contexts/UTS/LEX disciplines already fixed elsewhere in the spec.

**Non‑duplication note.** Universal Part‑G invariants (no shadow specs, crossing visibility, tri‑state guard, penalties→`R_eff`‑only, set‑return semantics, P2W split, typed RSCR causes, default ownership discipline, shipping boundary) are single‑owned by `G.Core` and are pulled into `G.4` only through the `G.Core linkage` manifest in **G.4:4.1** (and via explicit delegations in CC).

### G.4:1 - Problem frame

A CG‑Frame has:

* a declared `CG-FrameContext` (scope, described entity, plane),
* a plurality of method traditions and claims (SoTA inputs), and
* CHR‑typed measurement surfaces (`Characteristic/Scale/Coordinate` + legality guard macros).

Before any run‑time selection, comparison, aggregation, or portfolio formation is executed downstream, the CG‑Frame needs an explicit, auditable **calculus layer (CAL)** that:

1. defines *what operators exist* and what they are allowed to do over CHR types,
2. externalizes *fit‑for‑purpose acceptance* as typed predicates (with Context‑local thresholds), and
3. binds these choices to an evidence wiring surface (lanes, provenance anchors, policy pins, and refresh triggers) so that downstream selection, logging, parity, and shipping can cite *stable ids* rather than re‑inventing semantics.

This pattern provides the design‑time authoring kit and the publication surface for CAL artifacts, while delegating Part‑G‑wide invariants to `G.Core` and contract legality to `CG‑Spec`/`CN‑Spec`.

### G.4:2 - Problem

Teams repeatedly face drift and ambiguity in the calculus layer that sits between “typed measurements exist” and “a selector/dispatcher runs”:

* **Illicit operations** slip in (implicit cardinalization, unit laundering, ordinal arithmetic).
* **Acceptance is scattered** (thresholds embedded in code or in CHR prose; predicates not typed; unknown handling inconsistent).
* **Evidence wiring is underspecified** (which provenance anchors matter, what policy ids are in force, what is plane‑scoped, what changes must trigger refresh).
* **Cross‑context imports are silent** (hidden reuse of constructs across contexts/planes/editions without published GateCrossings and loss accounting).
* **Tooling artifacts become semantics** (vendor flags or implementation details substitute for a conceptual contract).

### G.4:3 - Forces

* **Expressiveness vs legality.** CAL must allow useful comparisons/aggregations while staying lawful under CHR typing and legality gates.
* **Pluralism vs comparability.** Multiple method traditions must coexist without forcing premature unification, yet remain cross‑citable and auditable.
* **Decision support vs auditability.** CAL must support selection and portfolio formation while preserving explicit, reviewable assumptions and proofs.
* **Exploration vs assurance.** CAL must support exploratory regimes (probing, novelty, open‑ended search) without letting un‑assured outputs silently become dominance claims.
* **Locality vs portability.** CAL must be Context‑local by default but prepared for explicit reuse via Bridges and published crossing surfaces.

### G.4:4 - Solution — CAL authoring kit and publication surface

#### G.4:4.1 - G.Core linkage (normative)

**Builds on:** `G.Core` (Part‑G core invariants; routing/delegation hub)

**GCoreLinkageManifest (normative).** Canonical shape, Nil‑elision, and the Expansion rule are defined in `G.Core`.

`GCoreLinkageManifest := ⟨
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

CorePinsRequired := {
UTSRowId[],                 // CAL artefacts are public ids (Name Cards + lifecycle notes)
ΓFoldRef.edition?            // only when an explicit Γ‑fold override is pinned (otherwise use DefaultId)
},

// consumed iff no explicit `ΓFoldRef.edition` override is pinned
DefaultsConsumed := { DefaultId.GammaFoldForR_eff },

RSCRTriggerSetIds := { GCoreTriggerSetId.SoTAHarvestSynthesis },
RSCRTriggerKindIds := {      // deltas (Expansion rule applies)
  RSCRTriggerKindId.PenaltyPolicyEdit,
  RSCRTriggerKindId.DefaultOwnerChange,
  RSCRTriggerKindId.BaselineBindingEdit
}
⟩`

By the `G.Core` Expansion rule, the effective conformance ids / trigger kinds / pin obligations for `G.4` are the expansions of the referenced profiles/sets/pin‑sets plus the explicit deltas above.

Notes (normative intent, routed semantics):

* The semantics of tri‑state outcomes, penalty routing, set‑return discipline, crossing visibility, P2W split, typed RSCR causes, and default ownership are single‑owned by `G.Core` and are not redefined here.
* EvidenceGraph/Path pins (when used) are declared only via **`G.4:Ext.EvidenceGraphWiring`** in **G.4:4.5** (so `G.Core linkage` stays minimal and does not “pull in” `G.6` by default).
* Method‑specific pins (e.g., QD descriptor/distance/insert policy pins; open‑ended transfer rules pins) MUST appear only in **Extensions** blocks (see **G.4:4.5**) and MUST NOT introduce competing defaults.

#### G.4:4.2 - `CAL Pack@CG-Frame` surface (pattern‑owned kit)

`CAL Pack@CG-Frame` is the CG‑Frame’s published calculus layer. Minimally, it provides:

* `CAL.Charter@Context` — scope anchor for this CAL pack:

  * cites `CG-FrameContext`, `describedEntity`, `ReferencePlane`,
  * cites contract surfaces (`CNSpecRef`, `CGSpecRef`) by edition pins,
  * records the “assumption envelope” that acceptance predicates rely on (without minting a new contract surface).
  * emits `TaskMap@Context` (`TaskMap`) as the canonical handoff surface to `G.5` (task→gates/flows/evidence pins).
* `CAL.Operator[]` — typed operator cards (UTS‑published):

  * explicit signature over CHR types,
  * explicit preconditions/postconditions (incl. legality guard macros references),
  * explicit provenance/evidence hooks (by ids/pins, not by tool behavior).
* `CAL.Acceptance[]` — typed predicates with Context‑local thresholds:

  * binds to CHR characteristic ids (and, when inducing numeric comparison/aggregation, to `CG‑Spec.characteristic` ids),
  * exposes unknown handling and failure behavior via policy pins.
* `CAL.Flow[]` — legality‑checked compositions of operator cards:

  * declares result kind (scalar only when lawful; set/portfolio when partial orders remain partial orders),
  * records which acceptance clauses gate which flows.
* `CAL.EvidenceProfiles` — evidence wiring surface:

  * lane tags (`F/G/R`) / provenance anchors / policy pins needed for `SCR` and audit surfaces,
  * explicit freshness/decay hooks (freshness window + decay/Γ_time selectors) as pinned policies/refs (not prose).
  * explicit `ReferencePlane` + penalty routing policy ids (`Φ(CL)`, `Ψ(CL^k)`, `Φ_plane`) as citable pins; any such policy family is justified in `CAL.ProofLedger` (monotone + bounded).
* **Optional** `CAL.NQD[]` — QD/OEE‑related calculus surfaces when declared:

  * descriptor/distance/insertion artifacts are pinned by ids/editions,
  * semantics are owned by method‑specific owners (e.g., `C.18`, `C.19`) and not redefined by CAL.
* `CAL.ProofLedger` — a proof/justification ledger:

  * links legality, monotonicity, boundedness, and other soundness obligations to operator/flow/clause ids.
* Publication layer:

  * UTS Name Cards (twin labels) for all public ids,
  * RSCR tests ids and Worked‑Examples ids,
  * deprecation notices and edition bump notes as lifecycle artifacts.

Boundary discipline (normative):

* **No shadow specs**: CAL artefacts cite `CN‑Spec`/`CG‑Spec` and do not introduce competing “local specs” (delegated; see `CC‑GCORE‑CN‑CG‑1` via **CC‑G4‑CoreRef**).
* **No shipping ownership**: CAL does not own shipping (delegated; see `CC‑GCORE‑SKP‑1` via **CC‑G4‑CoreRef**).
* **No refresh ownership**: CAL does not own refresh orchestration; it only publishes pins/payload for refresh (owner: `G.11`).

**Minimal schema fragments (notation‑independent; fields for citation, not an implementation schema):**

```
CAL.Pack@CG-Frame :=
 ⟨ calPackId, charterId, taskMapId, operatorIds[], acceptanceClauseIds[], flowIds[],
 evidenceProfileIds[], proofLedgerId, nqdIds[]?,
    utsRowIds[], workedExampleIds[], rscrTestIds[], lifecycleNoteIds[] ⟩

CAL.Operator :=
  ⟨ operatorId(UTS), signature(CHR-typed), preconditions[], postconditions[],
  evidenceProfileRefs[]?, failureBehaviorRef?, crossingRefs[]? ⟩

CAL.Acceptance :=
  ⟨ clauseId(UTS), characteristicRefs[], cgSpecCharacteristicRefs[]?,
    predicateRef, unknownHandlingRef, failureBehaviorRef,
    evidenceProfileRefs[]?, crossingRefs[]? ⟩

CAL.Flow :=
  ⟨ flowId(UTS), dag(operatorIds, edges), gateClauses(acceptanceClauseIds),
    resultKind, decisionAidPolicyRef? ⟩

CAL.EvidenceProfile :=
  ⟨ evidenceProfileId(UTS), lanes(F/G/R), anchors(A.10)[],
    freshnessPolicyPins[]?, penaltyPolicyPins[]?, ΓFoldRef.edition? ⟩
```

#### G.4:4.3 - CAL authoring chassis C1–C9 (pattern‑owned kit)

**C1 — CAL Charter (scope anchor).**
Authors declare a `CAL.Charter@Context` that:

* anchors CAL to the CG‑Frame scope (`CG-FrameContext`, `describedEntity`, `ReferencePlane`),
* pins the relevant contract surfaces (`CNSpecRef.edition`, `CGSpecRef.edition`),
* records the local assumption envelope used by acceptance predicates (as explicit statements to be audited, not as hidden algorithmic assumptions),
* declares which CAL artifacts are intended to be cited downstream (UTS ids).
* emits a `TaskMap@Context` (`TaskMap`) that binds each declared `TaskSignature` (or task family) to:
  * eligible `CAL.FlowId[]` / `CAL.OperatorId[]`,
  * gating `AcceptanceClauseId[]` (ids of `CAL.Acceptance` clauses),
  * required `CAL.EvidenceProfileId[]`,
  * and any required policy pins/edition pins for reproducibility.
  This is the canonical “handoff manifest” consumed by `G.5` (thresholds remain only inside `CAL.Acceptance`).

**C2 — Operator Cards (typed & lawful).**
Each `CAL.Operator` is a UTS‑published, typed unit with:

* `OperatorId (UTS)`,
* `Signature` over CHR types,
* `Preconditions` (including references to CHR guard macros where applicable),
* `Postconditions / invariants`,
* `EvidenceProfileRef[]` (or an explicit “none”),
* `FailureBehaviorRef` (policy‑bound) for safe degradations and non‑catastrophic fallbacks.

**C3 — Acceptance Clauses (typed predicates; thresholds live here).**
Each `CAL.Acceptance` is a UTS‑published predicate with:

* stable `ClauseId (UTS)` for citation,
* explicit `CharacteristicRefs` (CHR ids) used by the predicate,
* `CGSpecRefs?` required iff the clause induces numeric comparison/aggregation,
* `EvidenceProfileRefs?` identifying evidence consulted (so `SCR` can surface the relevant pins),
* explicit **freshness envelope** (freshness window + decay/Γ_time selector refs/pins) when evidence recency is part of admissibility,
* `UnknownHandling` as a tri‑state choice (via `G.Core` semantics),
* `FailureBehaviorRef` (policy‑bound) for degrade/abstain behavior.
* `GateCrossingId[]` / `CrossingSurfaceId[]` **iff** the clause relies on cross‑context/plane/edition imports (no “silent reuse”).
  Missing required crossing artefacts is a conformance failure and blocks publication of the affected clause/flow (GateCrossing harness: `E.18`/`A.21`/`A.27`; crossing invariants: `G.Core`).

**C4 — Aggregation & comparison flows (safe by construction).**
`CAL.Flow` composes operators into legality‑checked DAGs and declares:

* which acceptance clauses gate the flow,
* which operator outputs are decision‑relevant vs report‑only,
* what the **result kind** is (scalar only where lawful; otherwise set/portfolio).
* any thinning/decision‑aid policy (e.g., ε‑front selection) as an explicit policy pin that **does not** silently replace the declared result kind.

**C5 — Evidence wiring surface.**
`CAL.EvidenceProfile` makes evidence hooks explicit:

* provenance anchor references (A.10‑style carriers/anchors, cited by id),
* lane tags (`F/G/R`) for each evidence contribution (no implicit lane mixing; penalties route only to `R_eff` as routed by `G.Core`),
* pinned policy ids for penalty routing and freshness/decay handling (incl. freshness window + decay/Γ_time selector pins; and `Φ(CL)`/`Ψ(CL^k)`/`Φ_plane` policy ids when used),
* declared inputs needed for `SCR` fields at run‑time (without embedding run‑time “gate decisions” into design‑time artifacts).

**C6 — NQD/OEE surface (optional; method‑specific semantics routed).**
If the CG‑Frame declares QD/OEE‑style regimes, CAL may publish `CAL.NQD[]` as a **surface** that:

* declares descriptor space and distance/insertion artifacts by ids and edition pins,
* records archive/illumination intent and “report‑only vs dominance” gating as explicit policy pins,
* **does not** redefine QD/OEE semantics (those remain owned by method‑specific patterns such as `C.18` / `C.19` and are wired via `Extensions`).

**C7 — ProofLedger (soundness & legality obligations).**
`CAL.ProofLedger` links each operator/flow/clause to:

* legality proof refs (incl. CSLC refs when numeric comparison/aggregation is induced),
* monotonicity/boundedness/stability proof refs for penalty/aggregation policies where relevant,
  * in particular: if an explicit `ΓFoldRef` is pinned (override), ProofLedger includes monotonicity + boundedness/boundary behavior proof refs for that fold.
* explicit statements of degradation conditions (what must happen when assumptions fail).

**C8 — Publication + RSCR + Bridges.**
CAL publication emits:

* UTS entries (Name Cards + twin labels) for all CAL ids,
* Worked‑Examples that exercise legality and acceptance claims,
* RSCR tests ensuring:

  * illegality is detected (e.g., forbidden ordinal arithmetic),
  * guard macro use is coherent,
  * flow legality checks are exercised,
  * acceptance clauses behave as authored on examples.

Any cross‑context/plane/edition import required by CAL publication is handled through GateCrossing/CrossingSurface discipline (as routed by `G.Core`), and CAL publication is blocked if required crossing artifacts are missing.

**C9 — Packaging & refresh readiness (without owning orchestration).**
CAL pack versions:

* record changes as edition‑pinned updates,
* publish deprecations/lifecycle notes for public ids,
* emit RSCR‑relevant trigger payload pins (editions/policies/UTS ids/paths) for refresh orchestration (owner: `G.11`).

#### G.4:4.4 - Interfaces (minimal I/O surface)

| Interface                 | Consumes                                            | Produces                                                                                  |
| ------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `G.4-1 Charter`           | `CG-FrameContext`, SoTA inputs, `CHR Pack@CG-Frame` | `CAL.Charter@Context` + `TaskMap@Context` (`TaskMap`)  |
| `G.4-2 Operators`         | CHR typing + SoTA operator inventory                | `CAL.Operator[]` (UTS ids; typed signatures; refs to evidence profiles & guards)  |
| `G.4-3 Acceptance`        | Task intent + policy pins + CHR characteristics     | `CAL.Acceptance[]` (typed; thresholds; freshness envelope pins; failure behavior refs)    |
| `G.4-4 Flows`             | Operator cards + admissible aggregators             | `CAL.Flow[]` (legality‑checked compositions; declared result kind)                        |
| `G.4-5 NQD Surface`       | Task intent + policy pins + (optional) QD/OEE inputs | `CAL.NQD[]` (descriptor/distance/insertion refs + edition pins; optional)  |
| `G.4-6 Publish`           | All above + proofs + examples  | Versioned `CAL Pack@CG-Frame`, UTS entries, RSCR tests, Worked‑Examples, lifecycle notes |

#### G.4:4.5 - Extensions (pattern‑scoped; non‑core)

`G.4` supports method‑family and discipline‑specific calculus variations exclusively via pattern‑scoped extensions.

**GPatternExtension block: `G.4:Ext.EvidenceGraphWiring`**
- **PatternScopeId:** `G.4:Ext.EvidenceGraphWiring`
- **GPatternExtensionId:** `EvidenceGraphWiring`
- **GPatternExtensionKind:** `InteropSpecific`
- **SemanticOwnerPatternId:** `G.6`
- **Uses:** `{G.6}`
- **⊑/⊑⁺:** `∅`
- **RequiredPins/EditionPins/PolicyPins (minimum):**
  - `EvidenceGraphId?`
  - `PathId[]/PathSliceId[]`
  - `UTSRowId[]` (for cited artifacts)
- **RSCRTriggerSetIds:** `∅`
- **RSCRTriggerKindIds:** `{RSCRTriggerKindId.EvidenceSurfaceEdit, RSCRTriggerKindId.EditionPinChange, RSCRTriggerKindId.PolicyPinChange}`
- **Notes (wiring‑only):** This block does not define EvidenceGraph semantics; it only fixes that CAL proofs/examples may cite evidence by Path ids.

**GPatternExtension block: `G.4:Ext.NQD`**
- **PatternScopeId:** `G.4:Ext.NQD`
- **GPatternExtensionId:** `NQD`
- **GPatternExtensionKind:** `MethodSpecific`
- **SemanticOwnerPatternId:** `C.18`
- **Uses:** `{C.18}`
- **⊑/⊑⁺:** `∅`
- **RequiredPins/EditionPins/PolicyPins (minimum):**
  - `DescriptorMapRef.edition`
  - `DistanceDefRef.edition`
  - `InsertionPolicyRef`
  - `ArchiveRef?`
  - `TaskSignatureRef?` (if activation is TaskSignature‑bound)
- **RSCRTriggerSetIds:** `∅`
- **RSCRTriggerKindIds:** `{RSCRTriggerKindId.EditionPinChange, RSCRTriggerKindId.PolicyPinChange, RSCRTriggerKindId.TelemetryDelta, RSCRTriggerKindId.FreshnessOrDecayEvent}`
- **Notes (wiring‑only):** CAL does not redefine QD semantics; it only pins the artifacts needed for reproducible archive/descriptor behavior. Any archive/illumination summaries (e.g., coverage / QD‑score / occupancyEntropy / filledCells) are published as report‑only outputs unless an explicit CAL acceptance clause/policy authorizes promotion.

**GPatternExtension block: `G.4:Ext.EELog`**
- **PatternScopeId:** `G.4:Ext.EELog`
- **GPatternExtensionId:** `EELog`
- **GPatternExtensionKind:** `MethodSpecific`
- **SemanticOwnerPatternId:** `C.19`
- **Uses:** `{C.19}`
- **⊑/⊑⁺:** `∅`
- **RequiredPins/EditionPins/PolicyPins (minimum):**
  - `ExploreExploitBudgetPolicyRef`
  - `ProbeAccountingRef?`
  - `FailureBehaviorRef?` (if probe/sandbox is policy‑bound)
- **RSCRTriggerSetIds:** `∅`
- **RSCRTriggerKindIds:** `{RSCRTriggerKindId.PolicyPinChange, RSCRTriggerKindId.TelemetryDelta, RSCRTriggerKindId.FreshnessOrDecayEvent}`

**GPatternExtension block: `G.4:Ext.SoSLogBranches`**
- **PatternScopeId:** `G.4:Ext.SoSLogBranches`
- **GPatternExtensionId:** `SoSLogBranches`
- **GPatternExtensionKind:** `MethodSpecific`
- **SemanticOwnerPatternId:** `C.23`
- **Uses:** `{C.23}`
- **⊑/⊑⁺:** `∅`
- **RequiredPins/EditionPins/PolicyPins (minimum):**
  - `SoSLogRuleId[]`
  - `SoSLogBranchId[]`
  - `FailureBehaviorPolicyId`
- **RSCRTriggerSetIds:** `∅`
- **RSCRTriggerKindIds:** `{RSCRTriggerKindId.PolicyPinChange, RSCRTriggerKindId.MaturityRungChange, RSCRTriggerKindId.TelemetryDelta}`
- **Notes (wiring‑only):** This block only pins branch/rule ids for degrade/abstain explanation; it does not redefine rule semantics.

**GPatternExtension block: `G.4:Ext.AcceptanceRiskControl`** *(Phase‑3 seed)*
- **PatternScopeId:** `G.4:Ext.AcceptanceRiskControl`
- **GPatternExtensionId:** `AcceptanceRiskControl`
- **GPatternExtensionKind:** `Phase3Seed`
- **SemanticOwnerPatternId:** `owner TBD`
- **Uses:** `∅`
- **⊑/⊑⁺:** `∅`
- **RequiredPins/EditionPins/PolicyPins (minimum):**
  - `RiskControlPolicyRef`
  - `CalibrationWindowRef?`
  - `CoverageTargetRef?`
- **RSCRTriggerSetIds:** `∅`
- **RSCRTriggerKindIds:** `{RSCRTriggerKindId.PolicyPinChange, RSCRTriggerKindId.TelemetryDelta, RSCRTriggerKindId.FreshnessOrDecayEvent}`
- **Notes (non‑normative seed):** Intended for post‑2015 acceptance families such as conformal risk control / set‑valued selective prediction, distributionally‑robust acceptance envelopes, and calibrated abstention policies; semantics must be owned elsewhere before becoming normative.

### G.4:5 - Archetypal Grounding

**Tell.** A CG‑Frame must choose and justify a set of candidate methods (possibly a portfolio) under explicit legality, evidence, and scope constraints. CHR provides the typed measurement surface; CAL turns it into executable, auditable predicates and flows.

**Show 1 (in‑context CAL pack skeleton).**
Context: R&D portfolio choice. CHR defines `SafetyClass(ord↑)`, `CostUSD_2026(ratio↓)`, `Readiness(nominal)`.

* `CAL.Operator: DominatesPareto`
  Signature over CHR types, precondition references CHR guard macros.
* `CAL.AcceptanceClause: AC_SafetyGate`
  Typed predicate binding `SafetyClass` (and its levels) with Context‑local thresholds; unknown handling uses tri‑state pins.
* `CAL.Flow: Flow_ParetoPortfolio`
  Produces a set/portfolio result kind; gates by `AC_SafetyGate` and `AC_Budget`.
* `CAL.EvidenceProfile: EP_SafetyEvidence`
  Declares anchor ids and freshness policy pins required for `SCR`.

Downstream, `G.5` consumes only the handoff manifest: clause ids, operator ids, and evidence profile ids (no embedded thresholds).

**Show 2 (explicit cross‑context import).**
A `SafetyClass` value is imported from a different Context/plane. CAL may still author an acceptance clause using that value, but only after the reuse is made explicit as a published crossing surface and the CAL artifacts cite the relevant ids/pins. The CAL pack remains Context‑local; portability is achieved through explicit crossings and citations, not by silently widening scope.

### G.4:6 - Bias-Annotation

CAL is where “what counts as acceptable” is encoded. Typical bias vectors include:

* threshold‑selection bias (arbitrary floors masquerading as natural laws),
* measurement bias amplified by illegitimate arithmetic or hidden scalarization,
* survivorship bias in Worked‑Examples and probe telemetry,
* Goodhart pressures when report‑only telemetry is accidentally treated as dominance.

The pattern mitigates these by requiring typed acceptance clauses, explicit policy pins, and an auditable proof/justification ledger, while keeping cross‑context reuse explicit and penalized only through the routed assurance lane.

### G.4:7 - Conformance Checklist (normative)

| ConformanceId     | Statement                                                                                                                                                                                                                                                                                                      |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CC‑G4‑CoreRef** | Conformance with `G.4` requires satisfying the effective `G.Core` obligations referenced by the `GCoreLinkageManifest` in **G.4:4.1** (profiles, pin sets, consumed defaults, and trigger kinds).                                                                                                              |
| **CC‑G4‑01**      | `CAL Pack@CG-Frame` is published as a notation‑independent object with stable UTS ids (Name Cards + twin labels) for `CAL.Charter`, `TaskMap`, all operator/acceptance/flow/evidence artifacts, Worked‑Examples, and lifecycle notes (incl. deprecations and lexical‑continuity notes). Tooling/vendor details remain non‑normative. |
| **CC‑G4‑02**      | `CAL.Charter@Context` pins `CG-FrameContext`, `describedEntity` (incl. `ReferencePlane`), and the relevant contract references by edition pins (`CNSpecRef.edition`, `CGSpecRef.edition`).                                                                                                                     |
| **CC‑G4‑03**      | Every `CAL.Operator` has an explicit CHR‑typed signature and explicit preconditions; any legality guard macros referenced are cited by id (no “implicit legality”).                                                                                                                                             |
| **CC‑G4‑04**      | Every `CAL.Acceptance` binds to CHR ids (`CharacteristicRefs`) and declares unknown handling and failure behavior via pins/refs; thresholds and cutoffs appear only here (not inside CHR artifacts and not inside operator prose). If the clause depends on cross‑context/plane/edition imports, it cites `GateCrossingId[]/CrossingSurfaceId[]`. |
| **CC‑G4‑05**      | If an acceptance clause, operator, or flow induces numeric comparison/aggregation, it cites the relevant `CG‑Spec.characteristic` ids and links to legality proof refs (CSLC) in the ProofLedger; otherwise it must be authored so that downstream can degrade/abstain rather than perform illegal operations. |
| **CC‑G4‑06**      | Every `CAL.Flow` declares its result kind and the set of gating acceptance clauses; any thinning/selection‑aid policies (e.g., ε‑front selection) are explicitly policy‑bound and do not silently replace the underlying result kind.                                                                      |
| **CC‑G4‑07**      | Every `CAL.EvidenceProfile` declares: provenance anchors (A.10), evidence lanes (`F/G/R`), freshness/decay pins (incl. freshness window + decay/Γ_time selector refs), and any penalty routing policy pins (`Φ(CL)`, `Ψ(CL^k)`, `Φ_plane`) needed for run‑time `SCR` surfacing. It either pins an explicit `ΓFoldRef.edition` override or (if absent) cites `DefaultId.GammaFoldForR_eff` (via `G.Core.DefaultOwnership`). Penalty policies affect `R_eff` only and do not define dominance. Any referenced penalty policy family is justified in the ProofLedger (monotone + bounded).  |
| **CC‑G4‑08**      | `CAL.ProofLedger` exists and is UTS‑citable; it links each operator/flow/clause to required proof/justification refs and records explicit degradation conditions when assumptions fail. If an explicit `ΓFoldRef` is pinned, it includes monotonicity + boundedness/boundary behavior proof refs for that fold. |
| **CC‑G4‑09**      | CAL publication includes RSCR tests and Worked‑Examples sufficient to detect illegality (incl. unit laundering / ordinal arithmetic), to exercise authored acceptance/flow behavior, and to validate the authored freshness envelope when it is part of admissibility; missing tests/examples are treated as an auditable gap, not as “assumed OK”. |
| **CC‑G4‑10**      | `TaskMap@Context` (`TaskMap`) is present and provides `G.5` with acceptance clause ids (`AcceptanceClauseId[]`; selector gates), operator/flow ids, and evidence profile ids required for explainability and audit; selector implementations must not embed thresholds or duplicate acceptance semantics.    |
| **CC‑G4‑11**      | Any method/discipline specifics are placed under `G.4:4.5 Extensions` as `GPatternExtension` blocks (stable `PatternScopeId`, explicit owner, pins, and RSCR triggers); no extension introduces competing defaults or replaces `G.Core` invariants. |
| **CC‑G4‑12**      | `CAL Pack@CG-Frame` includes lifecycle artifacts for public ids (deprecations / edition bumps / lexical‑continuity notes) and exposes refresh payload pins (editions/policies/UTS ids and, when present, PathId/PathSliceId) sufficient for `G.11` to plan RSCR without inferring semantics from prose. |
| **CC‑G4‑13**      | When `G.4:Ext.NQD` is present, `CAL.NQD[]` is present and is wired only via the declared semantic owner (`C.18`): at minimum it pins `DescriptorMapRef.edition`, `DistanceDefRef.edition`, and `InsertionPolicyRef`, and it treats archive/illumination summaries as report‑only unless explicitly promoted by a CAL acceptance clause/policy. |
| **CC‑G4‑14** | CAL does not mint new universal types to encode “strategy/policy”. Strategy is expressed as authored flows + acceptance clauses + policy/task pins (and downstream registry/composition in `G.5`); any specialization is introduced only via `GPatternExtension` wiring blocks or cited semantic owners.  |

### G.4:8 - Common Anti-Patterns and How to Avoid Them

* **Hidden thresholds.**
  Avoid: embedding cutoffs in CHR prose or in operator descriptions.
  Prefer: `CAL.AcceptanceClause` with explicit ids and pins.

* **Untyped “score(x)”.**
  Avoid: operators with implicit units and untracked legality assumptions.
  Prefer: explicit CHR‑typed operator signatures + cited legality checks.

* **Silent cross‑context reuse.**
  Avoid: importing constructs across Contexts/planes/editions without published crossings.
  Prefer: explicit crossing artifacts and citations; keep CAL pack Context‑local.

* **Acceptance as implementation detail.**
  Avoid: acceptance embedded in tool logic.
  Prefer: publish acceptance as citable CAL artifacts; downstream consumes ids.

* **Exploratory telemetry treated as dominance.**
  Avoid: letting probe/illumination telemetry quietly become a dispatch criterion.
  Prefer: keep it report‑only unless an explicit policy‑bound acceptance clause authorizes promotion.

### G.4:9 - Consequences

* CAL becomes a stable, citable calculus layer: operator/acceptance semantics are explicit artifacts, not tacit code behavior.
* Legality failures are surfaced as authoring defects (RSCR‑testable) rather than run‑time surprises.
* Downstream patterns (`G.5`, `G.8`, `G.9`, `G.10`, `G.11`) can reference stable ids/pins without redefining acceptance or operator semantics.
* Method pluralism is supported: multiple calculi can coexist as separate operator/flow/acceptance families, wired via Extensions rather than mixed into the core kit.

### G.4:10 - Rationale

CAL sits at the boundary where typed measurement becomes actionable choice. Making CAL a published, typed, and testable artifact reduces semantic drift and prevents “shadow legality gates” from emerging in tools or in downstream prose.

The design separates concerns:

* CHR owns measurement typing and legality guard macros,
* CG‑Spec/CN‑Spec own contract surfaces,
* `G.Core` owns Part‑G invariants and trigger/default discipline,
* `G.4` owns the CAL kit: authoring objects, publication surface, and handoff manifest.

This yields modularity (single owner per invariant/default), auditability (pins/ids and proof refs), and extensibility (method families attach through explicit extension modules).

### G.4:11 - SoTA-Echoing

CAL authoring is compatible with post‑2015 best practice families without confusing “popular” with “best‑available”:

* **Risk‑controlled acceptance**: modern conformal / selective / set‑valued prediction families where “abstain” is a first‑class, audited outcome (fits tri‑state gating + explicit calibration pins).
* **Robust acceptance envelopes**: distribution‑shift‑aware and distributionally‑robust acceptance styles, expressed as policy‑pinned predicates rather than hidden heuristics.
* **Modern multi‑objective practice**: preference‑aware, interactive, and set‑returning multi‑objective decision families that preserve partial orders and portfolios.
* **Quality‑Diversity after 2015**: archive‑based search families (e.g., CMA‑ME‑class) attach as wiring via edition‑pinned descriptor/distance/insertion artifacts.
* **Open‑ended exploration after 2015**: environment‑method co‑evolution families (e.g., POET‑class) attach through explicit generator family wiring and policy‑bound acceptance branches.

All of these remain method‑specific semantics and therefore belong in `Extensions` blocks (or their semantic owners), while `G.4` keeps the calculus kit stable and auditable.

### G.4:12 - Relations

**Builds on:** `G.Core` (and the pattern template discipline in `E.8`).

**Uses:** `G.1` (CG‑FrameContext), `G.2` (SoTA Synthesis Pack), `G.3` (CHR Pack), `G.0` (CG‑Spec legality gate), `A.19` (CN‑Spec), `A.18` (CSLC), `A.10` (provenance anchors), `B.3` (trust/freshness/decay), `E.18` + `A.21` + `A.27` (GateCrossing harness), `F.9` (BridgeCard/CL).

**Uses (via Extensions):** `G.6` (EvidenceGraph/Path citation; when `G.4:Ext.EvidenceGraphWiring` is present), `C.18` (NQD), `C.19` (E/E‑LOG), `C.23` (SoS‑LOG).

**Used by:** `G.5` (selector/dispatcher), `G.8` (SoS‑LOG bundles), `G.9` (parity), `G.10` (shipping), `G.11` (refresh orchestration).
**Publishes to:** UTS (public ids + lifecycle), RSCR (tests + trigger emissions), `G.5` (handoff manifest), and (as cited payload) shipped packs owned by `G.10`.

**Constrains:** any run‑time LOG implementation that executes CAL operators/flows must treat CAL artifacts as citable contracts and must not re‑invent acceptance semantics.

### G.4:End

