## E.18 - Transduction Graph Architecture (E.TGA)

> **Tech‑name:** **E.TGA** (pattern label)
> **Plain‑name:** Architecture of the transduction graph
> **Twin labels:** Tech / Plain per E.10; faces emitted via E.17 MVPK (no schemas in Part E). 

### E.18:1 - Intent

Provide a **notation‑independent** architecture for graphs whose vertices are **morphisms (transductions)** and whose edges are **typed transfers**. The architecture is **agnostic to the concrete morphism set** and equips the graph with **publication, comparability, crossing, and budget** disciplines so that **flows** are **valuations over paths** within the same object. Faces appear via **MVPK**; numeric/comparable publication carries **pins** with **Bridge/CL** notes; Φ/CL^plane penalties remain in **R**.  
*Style note:* wording follows the **counterfactual register** of FPF: invariants are stated as model conditions, not deontic obligations (per E.8 style and the assignment).

### E.18:2 - Problem frame

Teams can produce many **valid flows** over the same capability: e.g., the assignment’s reference path
`U.FormalSubstrate → U.PrincipleFrame → U.Mechanism → U.ContextNormalization (UNM) → U.SelectionAndTuning ↔ U.WorkPlanning → U.Work → U.EvaluatingAndRefreshing`
is one **path** among many possible domain paths. Without a common **graph‑level architecture**:

* flows look ad‑hoc and **non‑comparable**;
* cross‑Context **crossings** (plane/Context changes) are undocumented;
* publication surfaces **smuggle arithmetic** or restate I/O;
* set‑returning selection is silently replaced by **single scores**;
* cycles lack **budget** discipline; refresh is **out‑of‑band**.

MVPK already fixes publication drift at the **single‑arrow** level; E.TGA lifts those **publication and comparability laws** to the **graph as a whole**. 

### E.18:3 - Problem

1. **Morphisms ≠ Graph.** A catalog of morphism‑level patterns (e.g., UNM, Selector, Work, Refresh) does not, by itself, explain **how the whole graph is built, constrained, and audited**.
2. **Flow proliferation.** Multiple “reference flows” can be authored; readers need **one orchestration** that keeps them legal and comparable **without privileging any single flow**.
3. **Unsafe publication.** Faces re‑list I/O, hide scalarization, or omit edition/plane pins; cross‑Context reuse lacks **Bridge/CL** citation; **plane penalties** leak to F/G. 
4. **Cycles without norms.** Selection↔Planning loops run without explicit **budget (Γ_time)**, **FreshnessRequest**, or **slice‑scoped** refresh; `FinalizeLaunchValues` (launch‑value slot filling) is performed too early (outside `U.Work` (`U.WorkEnactment`)). 

### E.18:4 - Forces

| Force                                            | Tension                                                                                                                                                                    |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Universality vs specialization**               | One architecture must host supply chains, water networks, ML functionals, and the assignment’s “first‑principles → work” path, **without** baking in any one morphism set. |
| **Publication neutrality vs auditability**       | Keep faces notation‑neutral and non‑mechanistic ↔ require **pins**, **ComparatorSet**, **Bridge/CL**, and **PublicationScope**.                                            |
| **Set legality vs business pressure for totals** | Preserve **return‑sets / lawful partial orders** ↔ stakeholders demand single numbers.                                                                                     |
| **Cross‑Context reuse vs safety**                | Enable reuse across `U.BoundedContext` ↔ enforce **Bridge/CL** with **R‑only penalties**.                                                                                  |
| **Agility vs reproducibility**                   | Permit evolving CG‑Spec/UNM/Comparator editions ↔ require **edition pins** and **re‑emission** on change.                                                                  |
| **Cycles vs convergence**                        | Allow Selection↔Planning iteration ↔ impose **budget** and **slice‑scoped** refresh to prevent thrash.                                                                     |

### E.18:5 - Solution — the E.TGA kit (graph model + choreography)

#### E.18::5.1 - S1 - Graph object (conceptual)

Define a **typed, editioned, directed multigraph**
`TransductionGraph := (V, E, τ_V, τ_E, Γ_time, Bridge, CL, TransportRegistry^Φ)`
with:

* **Vertices `V`:** instances of `U.Morphism` (open world). Common specialisations **include but are not limited to** the assignment’s set: `U.FormalSubstrate`, `U.PrincipleFrame`, `U.Mechanism`, `U.ContextNormalization (UNM)`, `U.SelectionAndTuning`, `U.WorkPlanning`, `U.Work`, `U.EvaluatingAndRefreshing`. This list is **illustrative**, not exhaustive—the graph **does not depend** on this particular set.
* **Edges `E`:** a **single edge kind `U.Transfer`** (typed) carrying artifacts/tokens; all **plane/Context/edition** changes occur **only at nodes via `OperationalGate(profile)`** with **Bridge + CL** annotations; penalties **→ R only**. Transport conversions pin **Φ‑policies** and editions.
* **Scopes:** `Γ_time` (budgets, horizons), `PublicationScope` for faces (E.17), and **slice ids** for refresh (G.11).

 **CtxState (PS‑projection; closed slots):** `CtxState = ⟨L, P, E⃗, D⟩` is the **projection of E.17 Publication Scope**.
 **Slot definitions (normative):**
  • `L := Locus` — an element of a partially ordered **ContextSlice** poset; addresses *where* claims apply (disciplinary / organizational / holonic slice).
  • `P := ReferencePlane` — the reference plane/units registry id; **no plane/unit declarations or translations** occur in CV; crossings remain gated (A.21).
  • `E⃗ := Edition vector` — a **partial map** `edition_key ↦ EditionId` over named families `{CG‑Spec, ComparatorSet, UNM.TransportRegistryΦ}` and optional `{DescriptorMapRef, DistanceDefRef, CharacteristicSpaceRef}` when cited.
  • `D := DesignRunTag` — `design(T^D)` or `run(T^R)`, used by **LaunchGate** and acceptance/telemetry duties.
 **Invariants.** Raw `U.Transfer` preserves `CtxState` (`⟨L,P,E⃗,D⟩`): it does **not** write/update any CtxState slot; any CtxState write/update (or entry to `U.WorkEnactment`) occurs at `OperationalGate(profile)`.
 **Extension discipline.** Any extra slot beyond ⟨L,P,E⃗,D⟩ **SHALL** be registered in the **E.17/LEX “CtxState Extension Registry”** with slot‑id, intent, partial‑order law (neutral/absorbing), and SquareLaw compatibility; unregistered extensions are non‑conformant.
 **Data‑shape location.** Concrete record shapes for `PathId/PathSliceId`, Γ‑pins, and lineage remain in A.22 `FlowSpec`; E.TGA fixes that **flow = valuation** and that `CtxState` is preserved across raw transfers.

 * **Kinds:** `U.Transduction(kind∈{Signature, Mechanism, Work, Check, StructuralReinterpretation})`.  
  **Exact identification (no TGA‑local taxonomy):**  
  — `Signature` **≡** **A.6.0** `U.Signature` (universal, law‑governed declaration).  
  — `Mechanism` **≡** **A.6.1** `U.Mechanism` (law‑governed application over a SubjectKind/BaseType).  
  — `Work` **≡** **A.15** `U.WorkEnactment` (world‑contact; `FinalizeLaunchValues` only here).  
  — `Check` **≡** `OperationalGate(profile)` (universal **gate**; A.* patternisation pending; CC‑TGA catalog applies).  
  — `StructuralReinterpretation` **≡** a species of **A.6.4** `U.EpistemicRetargeting` used as a graph node in E.TGA. **All retargeting semantics** (slot‑level discipline, `DescribedEntitySlot`/`GroundingHolonSlot` behaviour, invariants, Bridges, witnesses) come from **C.2.1** and **A.6.2–A.6.5**; E.TGA does **not** introduce a TGA‑local variant of retargeting.  
  `OperationalGate ≔ U.Transduction(kind=Check)` with DecisionLog aggregation.  
  The only extra discipline E.TGA adds for `StructuralReinterpretation` is **graph‑local**: CtxState and GateCrossing behaviour are governed by **CC‑TGA‑06‑EX** and **CC‑TGA‑11** (projection‑preserving w.r.t. `⟨L,P,E⃗,D⟩`, PathSlice‑local, and “no plane/unit change without a gate”). 

> **MVPK integration (import).** Every vertex with an external surface is published via **MVPK** faces (`PlainView`, `TechCard`, `AssuranceLane`, `InteropCard`) under a declared **PublicationScope** (E.17). E.TGA **reuses** MVPK’s publication laws (pins, lawful‑order discipline, “no new numeric claims / no I/O re‑listing”) and only adds graph‑level constraints in S3 and **CC‑TGA‑09/10**; it does **not** define a second, local publication semantics. 

**GateCrossing (normative)**
**Definition.** A **GateCrossing** is the typed transition at a node that writes/updates any of:
  (i) `U.BoundedContext` (**Context**), (ii) **ReferencePlane**, (iii) any member of the **Edition vector** `E⃗` (e.g., `CG‑Spec`, `ComparatorSet`, `UNM.TransportRegistryΦ`, `DescriptorMapRef`, `DistanceDefRef`, `CharacteristicSpaceRef`), (iv) **DesignRunTag** (`T^D↔T^R`), or (v) **Kind/describedEntity** (only under `StructuralReinterpretation` subject to **CC‑TGA‑06‑EX**).
**Invariants.** Raw `U.Transfer` preserves `CtxState`; a GateCrossing occurs at exactly one `OperationalGate(profile)` (SquareLaw applies).
**Required pins (minimum).** `BridgeCard + UTS row`; `CL` for scope bridges; `CL^plane` for plane crossings; `CL^k` with `bridgeChannel=Kind` for kind transitions; `PublicationScopeId`; `PathSliceId`; Γ‑pins on compare/launch faces.
**Canonical reference.** `CrossingRef := ⟨GateId, channel, from, to, UTS.RowId, PathSliceId⟩`. Any DecisionLog entry whose rationale depends on a crossing **SHALL** cite `CrossingRef`.
**CrossingSurface (normative)**
**Definition.** A **CrossingSurface** is the published bundle that makes a GateCrossing **auditable and replayable** (crossing visibility). It includes:
* the canonical **`CrossingRef`**;
* the matching **UTS row** (**`UTS.RowId`**) for the crossing;
* the required pins **`PublicationScopeId`** and **`PathSliceId`**;
* where a Bridge is involved: the **BridgeCard** (F.9) and its disclosed fields (`BridgeId`, `bridgeChannel`, **CL** and loss notes; **`CL^k`** when `bridgeChannel=Kind`; **`ReferencePlane(src,tgt)`**);
* where planes differ: **`CL^plane`** and the active **`Φ_plane`** as a **`PolicyIdRef`** (policy-id + resolvable refs; F.8:8.1);
* the active penalty policy identifiers **`Φ(CL)`** (and **`Ψ(CL^k)`** if used) as **`PolicyIdRef`** bundles (policy-id + `PolicySpecRef` + `MintDecisionRef?`; F.8:8.1);
* any additional pins mandated by the active **GateProfile** / GateChecks (A.21) for this crossing.

**Obligation.** Every **GateCrossing MUST publish its CrossingSurface**. Missing or non‑conformant CrossingSurface is a **blocking** defect for downstream consumption (selectors, acceptance, audits).

**Term separation.** **Transfer** denotes the sole edge kind `U.Transfer` (graph edges). **Transport** denotes Φ‑governed conversion **policies/registries** (**`TransportRegistry^Φ`** under UNM). Wording “reuse via Transport” refers to registries/policies, not to an additional graph edge.

#### E.18:5.2 - S2 - Flows as valuations (paths + state + guards)
* A **Flow** is a **valuation** `ν` over `U.Transfer` edges and cut‑sets, paired with an **admissible path** `p = v₀ → … → v_k`. The valuation assigns tokens/states under `CtxState` and records publication events under a declared `PublicationScopeId`. **The concrete pins and identifiers (`PathId`, `PathSliceId`, Γ_time on compare/launch faces) are specified in A.22 `FlowSpec` and A.25 `Sentinel & SubFlow`.** This reflects the “graph ≠ flow” norm (flow = valuation), with gates placed exactly on GateCrossings.  
* **Admissible path (definition).** A path `p` is **admissible** iff:  
  (a) node/edge types match the declared `τ_V, τ_E`;  
  (b) any write/update to any member of `⟨L,P,E⃗,D⟩` (or kind‑retargeting under `StructuralReinterpretation`) appears at **exactly one** `OperationalGate(profile)`;  
  (c) each GateCrossing on `p` has a **SquareLaw witness** (CC‑TGA‑23) and, where applicable, a **SquareLaw‑retargeting witness** (CC‑TGA‑06‑EX);  
  (d) no hidden crossings occur across raw transfers;  
  (e) Γ‑pins are present on compare/launch faces;  
  (f) `T^D↔T^R` occurs **only** at `LaunchGate`.

* `U.Transfer` preserves `CtxState` (`⟨L,P,E⃗,D⟩`) and carries **Assurance‑operations** only (see S3b); any crossing of locus/plane/editions or `T^D↔T^R` is placed at `OperationalGate(profile)`.
* A **PathSlice** is a **slice‑scoped execution window** used for refresh/telemetry; faces pin `PathSliceId`; **re‑emission** happens when any pinned edition changes or `SliceRefresh` is triggered by sentinel rules.

> **Consequences.** The assignment’s “reference flow” is simply one `p` in `TransductionGraph`. Other domains (supply chain, water network, NN functional) instantiate different `p` on the **same architecture**.
> 
**Why "flow = valuation" doesn't kill the "something is flowing" intuition**
There are two complementary perspectives:
* **Lagrangian (intuitive):** "water particles" run through pipes; you "track" tokens.
* **Eulerian (architectural):** you define a **function on edges** ("how much/what passes through each edge under a given regime"), with gate laws. E.TGA deliberately fixes the **Eulerian semantics of flow** at the architectural level: "flow (= valuation) + publication log", while the dynamics of "movement" show up as **re-valuation** over a **PathSlice** (the execution/republishing window) under gate rules and the SquareLaw. This yields comparability, reproducibility, and slice-local refresh.

#### E.18:5.3 - S3 - Publication discipline (faces)

E.TGA **imports E.17** wholesale **and associates MVPK faces with `PublicationScope` (USM)**.  
**MVPK remains the normative source** for:
* the set of face kinds (`PlainView`, `TechCard`, `InteropCard`, `AssuranceLane`),
* pin discipline and Publication Characteristics (PC),
* “no new numeric claims / no I/O re‑listing / no Γ‑semantics on faces”.

E.TGA **does not re‑specify** these laws; it only adds **graph‑level obligations** for faces emitted over transduction paths:

1. **Crossings on faces.** When a face participates in a GateCrossing (S1.b/S9), it **SHALL** cite `BridgeId + UTS row + CL` and publish **Φ(CL)/Φ_plane RuleId**; **penalties remain in R‑lane**.
2. **Gate‑requirement on cited editions.** Any face that references editions of `CG‑Spec` / `ComparatorSet` / `UNM.TransportRegistryΦ` includes **`BridgeCard + UTS row`**; faces without this are treated as **non‑consumable downstream**.  (delegated tests → A.27/A.34)  
3. **ComparatorSet & set returns (graph‑scope).** Any `ComparatorSet` and `SetSemanticsRef` used along a transduction path **SHALL** carry **edition identifiers**; flows **re‑emit** faces on edition change; faces with comparison **return sets / lawful partial orders** (no hidden scalarization), reusing MVPK’s lawful‑order discipline.
4. **Γ_time on compare/launch faces.** All compare/launch faces on E.TGA paths pin `Γ_time`; implicit *latest* is illegal. The **shape and evaluation** of `Γ_time` live in A.26; E.TGA only mandates presence. **CHR avoids acceptance thresholds** (*NoThresholdsInCHR*); thresholding and launches surface in G‑patterns and `U.Work`.  (delegated tests → A.32/A.33). **Unknowns remain tri‑state (`pass|degrade|abstain`) and fold per GateProfile (A.21/A.26).**  

> **Reminder.** MVPK already bans “signature” on faces, I/O re‑listing, arithmetic on faces, and unpinned numeric content (E.17 §5.4–5.5). E.TGA **does not weaken or override** those rules; it only constrains how they are used along transduction paths.

**Lean publish‑mode (AssuranceLane‑Lite).** Lean affects **faces only** (`PlainView`/`AssuranceLane` minimal), not checks; publication shows `GateProfile`, `GateCheckRef[]`, and `DecisionLogRef`; the underlying GateChecks list remains unchanged.

**Decision stability & idempotency (delegated).** Gate decisions are **idempotent** under a congruence relation over inputs; the **witness and equivalence criteria** are specified in **A.41 DecisionLog**. E.TGA **does not** prescribe storage formats, key shapes, or hashing schemes.

**KindBridge admissibility (publication).**  
Treat a step as a **describedEntity/kind** transition (including `StructuralReinterpretation` under CC‑TGA‑06‑EX) **iff** the **UTS row**:
  — satisfies the **minimal Bridge row** obligations of A.27 (identity, `ReferencePlane`, `CL/CL^plane`, edition‑pins for `CG‑Spec` / `ComparatorSet` / `UNM.TransportRegistryΦ`, `ComparatorSetRef`, `BridgeId`, `Φ‑RuleIds`), and  
  — is additionally marked as a **KindBridge** per C.3 (`bridgeChannel=Kind`, `CL^k`, mapping or signature‑translation, order‑preservation claims, loss notes, definedness area, determinism).  
Otherwise this KindBridge explanation does not apply (the step falls back to a gated crossing). When the gate owns the crossing, `CrossingRef` is surfaced and linked from the `DecisionLog`.

#### E.18:5.4 - S4 - Assurance‑operations on `U.Transfer` (counterfactual admissibility)
On `U.Transfer` edges, an operation is interpreted as a **declarative assurance‑operation** **iff** it is one of  
`ConstrainTo(rule)` - `CalibrateTo(map|standard)` - `CiteEvidence(anchor)` - `AttributeTo(agent|role)`; otherwise this explanation does not apply.
Under this interpretation, `CtxState⟨L,P,E⃗,D⟩` is preserved.  
If an effect entails a plane/unit change, the assurance‑operations explanation does not apply and the step is handled as a gated crossing (`OperationalGate(profile)+Bridge+UTS`).  
If Φ assigns penalties, they appear in the R‑lane; otherwise no penalties are surfaced here.

#### E.18:6.5 - S5 - Comparability & aggregation (normalize‑then‑compare; counterfactual form)

The comparison explanation applies under the following admissibility conditions:

* If a path segment intends to compare/aggregate, it is admissible as a comparison **only when** UNM precedes it; UNM is **method‑independent**, publishes **TransportRegistry^Φ** and **CG‑Spec** anchors, and faces cite those editions; otherwise this comparison explanation does not apply.
* If the comparator defines a **lawful partial order**, then returns are **sets/archives** (Pareto/Archive); if a **total order** is declared, it is the one provided by the comparator; otherwise set semantics apply and covert scalarization is out of scope here.
* If a claim is **ordinal‑only**, then only comparisons are surfaced; arithmetic transforms (e.g., means/z‑scores) are out of scope of this explanation and belong to declared comparators or downstream policy.

**Edition‑aware artifacts (e.g., QD archives) MUST pin `DescriptorMapRef.edition` / `DistanceDefRef.edition` (and `CharacteristicSpaceRef.edition` when applicable); refresh is slice‑local.**  (delegated tests → A.34/A.37)  

#### E.18:5.6 - S6 - Cycle discipline (Selection ↔ Planning)

* The architecture centers the loop between `U.SelectionAndTuning` and `U.WorkPlanning`.
* The loop operates under a local **budget / max_iter** in `Γ_time`; at expiry, the selector emits the **current `CandidateSet`** and **`MethodTuning`** with a **partial‑optimality** flag; further improvement rolls into the **next `PathSlice`**.
* **UNM occurs before the loop**; if measurements are missing/stale, UNM emits a **FreshnessRequest** which is **planned** in `U.WorkPlanning` and **executed** in `U.Work`. Transfers, units, and calibrations are surfaced publication‑wise as `CalibrateTo(map|standard)` and pinned to `TransportRegistry^Φ` (**R‑channel only** for penalties).
* **WorkEnactment is the only site for launch‑value slot filling** (`FinalizeLaunchValues / FinalizeLaunchValuesOnlyInWork`). 
> **Refresh orchestration.** Telemetry from `U.WorkEnactment` and publications are **slice‑scoped**, editions re‑pinned, faces **re‑emitted**. 

#### E.18:5.7 - S7 - Selector semantics (G.5) & parity harness (G.9)

* **Selectors return sets.** Default **DominanceRegime** is `ParetoOnly`; **IlluminationSummary** (telemetry summary) and any coverage/regret (telemetry metrics) are **report‑only telemetry** (reported), excluded from dominance **unless** a CAL policy promotes them (policy‑id in SCR).

If `PortfolioMode=Archive`, a **QD archive** may be returned; when generation is in scope, pairs `{environment, method}` are managed under declared **EnvironmentValidityRegion** and **TransferRulesRef**; parity artefacts and `PathSliceId` are pinned on publication. Details of comparator semantics and archive pinning live in **A.28/A.34**.

#### E.18:5.8 - S8 - Guard ownership and handling (USM §1.2)
* **USM.CompareGuard**/**USM.LaunchGuard** **publish `GuardOwnerGateId`**. Guard failures are **events** aggregated by the owner gate (not GateChecks).
* **Ownership rules:** (i) `USM.LaunchGuard.owner = LaunchGateId(U.WorkEnactment)`; (ii) inside a Subflow, `USM.CompareGuard.owner = OperationalGate(InSentinel)`; Join‑nodes cannot own guard pins.

**GateProfile data shape (cross‑reference).** The **entire data shape** (SoD/quorum, declassify, budgets, TOCTOU/freshness windows, editions vector, scopes) is **specified in A.26**. E.TGA **only names** the structure and defers its fields to A.26.

**Bridge‑aware guards (cross‑reference).** USM guards apply bridge‑translation semantics (`translate(Bridge, Scope)`) with CL penalties in R‑lane; the conceptual macro is defined in **A.24 USM.Guards**.

**Error/timeout/unknown (profile‑bound).** GateCheck errors/timeouts fold to **`degrade`** under `Lean|Core` and to **`block`** under `SafetyCritical|RegulatedX`; `unknown` follows the GateCheck’s intensional rule (safety‑default: `degrade`). **The DecisionLog shape and the idempotency witness are defined in A.41; E.TGA does not define storage or key structures.**  

#### E.18:5.9 - S9 - Transport & crossings
* Cross‑Context or cross‑plane edges appear as **GateCrossings** that include a **Bridge** with **CL** policy; **Φ(CL)/Φ_plane** are published; penalties route **to R only**; **Scope membership** (USM) is unchanged by crossings. **SquareLaw is checked within a single `DesignRunTag`; a `T^D↔T^R` change is modelled as a pair of coordinated gates with `DesignRunTagFrom/To` and an external enactor (see A.29).** 
* When *describedEntity/kind* changes across a boundary, declare an explicit **KindBridge (`CL^k`)** in addition to plane/context CL; cross‑context reuse of UNM **must** go via `Transport`, with any `CL^plane` penalties routed to **R‑lane** only.

#### E.18:5.10 - S10 - Non‑mechanism boundary

* Publication is a **typed projection**, not execution. Any build/render/upload is **Work on carriers**; **no Γ‑semantics** may leak into faces. 

#### E.18:5.11 - S11 - Coordination thread (optional)
Introduce **CoordinationFlow** as a named thread laid over `U.TransductionFlow__P2W`; crossings with production flow go via **Bridge+UTS**; coordination publishes **LexicalView** labels only and adds **no checks** or mechanisms.

#### E.18:5.12 - S12 - Viewpoint families → E.TGA constructs (neutral, holonic)

E.TGA does not mint new viewpoint or view kinds. It **imports** the generic multi‑view machinery of E.17.0 `U.MultiViewDescribing`, bundles from E.17.1, and the TEVB engineering bundle from E.17.2. S12 only describes how these existing `U.Viewpoint` / `U.ViewpointBundle` ids are *used* in transduction graphs and in `UTS.ViewpointMap`; intent/concern semantics live in E.17.0–E.17.2.

**Two‑layer use of TEVB and MVPK (ISO 42010 summary, no local re‑definition).**

* **Engineering viewpoints.** For engineering holons, E.TGA assumes a TEVB bundle with `ViewFamilyId = VF.TEVB.ENG`. `EngineeringVPId` is one of `{VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}`, and TEVB is the normative source for their semantics. E.TGA does not refine these viewpoints.  
* **Publication viewpoints.** Publication viewpoints come from MVPK (E.17); `PublicationVPId` is a `MVPK.ViewpointId` that governs faces under a `PublicationScope`.  
* **Architecture description.** Under ISO 42010, an architecture description for a holon is: (i) an E.TGA transduction graph over that holon, plus (ii) MVPK faces emitted for its morphisms, with correspondences per E.17.0 linking each face to the engineering view(s) it implements. Crossings and penalties follow E.TGA’s gating rules (S9; CC‑TGA‑11/23) but do not change viewpoint semantics.  
* **Separation of roles.** `VP.*` from TEVB are **EngineeringVPId** values only; they are not surfaces. `PublicationVPId` values live in MVPK. The mapping between them is entirely via ISO‑style correspondences and the `UTS.ViewpointMap`; E.TGA does not define a second notion of viewpoint.

**Entities‑of‑interest (summary).**

* **EoI‑ENG.** The engineering entity described by TEVB/E.TGA is a holon (`U.System` or `U.Episteme`) per TEVB’s `EoIClassSpec`. E.TGA does not broaden or narrow this set.  
* **EoI‑PUB.** MVPK may treat the *architecture description* itself as an entity‑of‑interest; publication viewpoints for that AD are defined in MVPK, not here. E.TGA only requires that such faces honour MVPK discipline and E.TGA’s crossing rules.

**Naming rules (aligned with E.17.0/E.17.1/E.17.2).**  
* `ViewFamilyId` is the `U.ViewpointBundle.viewFamilyId` (e.g. `VF.TEVB.ENG` for TEVB); its lexical and ontological discipline is governed by E.17.1.  
* `EngineeringVPId : ViewpointId` is always a `U.ViewpointId` drawn from some bundle (for TEVB, one of `{VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}`). E.TGA never defines new `VP.*` ids.  
* `PublicationVPId : ViewpointId` is a `MVPK.ViewpointId` defined in E.17; TEVB viewpoints are **never** reused as publication viewpoints (per TEVB guard and MVPK).  
* The legacy unqualified column name `ViewpointId` MUST NOT be used. Where it exists, it is interpreted as `PublicationVPId` and is DEPRECATED (sunset when E.23 is published).

**Terminology guards (no local semantics).**
* Within S12, “viewpoint”, “view” and “correspondence” have exactly the meanings given in E.17.0; “publication surface” means an MVPK face (`PlainView`, `TechCard`, `InteropCard`, `AssuranceLane`) under some `PublicationVPId`.  
* Faces are **carriers for views**: a face is part of a view only when linked via an ISO‑style `CorrespondenceRef` to an engineering `U.View` under some `EngineeringVPId`; S12 does not add extra conditions beyond E.17.0/E.17.2.  
* Labels such as “Functional view”, “Procedural view”, “Role‑Enactor view”, “Module‑Interface view” in this section are lexical aliases for TEVB viewpoints; they MUST NOT be interpreted as extra viewpoint kinds or as surface types.

**Purpose.** Provide a neutral (F.18) mapping from TEVB engineering *viewpoint families* — bundle `VF.TEVB.ENG` with `VP.Functional / VP.Procedural / VP.RoleEnactor / VP.ModuleInterface` — to E.TGA constructs so that the same holon can be described functionally, procedurally, structurally, or as a module‑and‑interface architecture **without changing the underlying graph**. S12 does not introduce new `U.Viewpoint` or `U.View` kinds; it reuses those defined in E.17.0/E.17.2.

**Holon target.** The mapping applies to any holon, with the constraint that only `U.System` enacts `U.Work` (A.3/A.15). Supervisory and structural hierarchies remain distinct (B.2.5).

**Viewpoint family → primary E.TGA constructs (TEVB‑aligned)**  
*All four families referenced below are TEVB engineering viewpoints; the “what …” clauses are interpretive glosses for how they *use* E.TGA constructs. Formal intent/concerns/allowed episteme kinds remain in TEVB (E.17.2).*
1) **Function‑Oriented View (`EngineeringVPId = VP.Functional`, capability‑flow)** — “what transformation is achieved under roles”
    * **Flow substrate:** `U.TransductionFlow__P2W` through nodes `SubstrateFormalization → OntologyAuthoring → CHRAuthoring → PrincipleFraming → MechanismRealization → UNM.Usage (ContextNormalization) → SelectionAndTuning ↔ WorkPlanning → WorkEnactment → EvaluatingAndRefreshing`.
    * **Publication:** MVPK publication surfaces per E.17; comparable claims pin to `CG‑Spec/ComparatorSet` editions; crossings surface via `Bridge+UTS` and `CL/CL^plane` (penalties → **R‑lane** only). 
    * **Checks:** A.20 (CV) inside transformations; A.21 (GateFit) at gates; enforce CSLC/No‑Hidden‑Scalarization per A.28. 
    *  **Holonic note:** `U.Episteme` does not *act*; it is used by systems acting on carriers; `U.Work` appears only for `U.System`. 
2) **Procedure‑Oriented View (`EngineeringVPId = VP.Procedural`, step/time storyboard)** — “what steps occur and when”
    * **Artifacts:** `U.WorkPlan` (A.15.2) for intent/schedule; `U.WorkEnactment` for enactment.
    * **Boundary:** entry into `U.WorkEnactment` is via `OperationalGate(profile)` with `USM.LaunchGuard`; `DesignRunTag` separates design time from run time; `DesignRunTagFrom/To` appear only at gates. 
    * **Holonic note:** Applies to any `U.System` scope (single holon or a supervised sub‑holon cluster); supervisory layering is handled by roles rather than structural mereology (B.2.5).
3) **Role‑Enactor / Device‑Structure View (`EngineeringVPId = VP.RoleEnactor`)** — “what carrier/ports/constraints exist; who typically enacts it”
    * **Artifacts:** Module *interfaces* are `Signature` nodes; module realizations are `MechanismRealization` nodes; inter‑module dependencies traverse `U.Transfer`, with gates on crossings. 
    * **Publication:** MVPK faces are **typed projections**, not executable artifacts; faces add **no new numeric claims** (E.17). Constraints and compatibility appear as CV checks (A.20). 
    * **Holonic note:** Structural mereology (part/whole of the carrier) is modeled in Part A; E.TGA ties interface/exposure semantics to morphisms and gates.
    * **Device‑View reading (Transduction↔Transductor).** The same capability‑flow MAY be read as a **device** that performs the transduction (**transductor**) without changing the graph: model with `Signature` + `Mechanism` only; do **not** introduce extra edge kinds. If describedEntity retargets (function↔element), use `StructuralReinterpretation` with a **`KindBridge (CL^k)`** on **UTS** and a **SquareLaw‑Retargeting witness**; preserve `⟨L,P,E⃗,D⟩` and treat it as a non‑crossing (**CC‑TGA‑06‑EX**; witness shape §4.7).  
    * **Role‑label guard.** `TypicalEnactorRoleName` is **pedagogical only** and MUST NOT be used as a GateFit role; GateFit uses `U.Role` (A.21).
4) **Module‑Interface View (`EngineeringVPId = VP.ModuleInterface`, physical/logical architecture)** — “what modules exist and how they contract across interfaces”
    * **Artifacts:** Module *interfaces* are `Signature` nodes; module realizations are `Mechanism` nodes; inter‑module dependencies traverse `U.Transfer`, with gates on crossings. 
    * **describedEntity note:** Functional↔element reinterpretation follows the **Device‑View reading** rule above (Role‑Enactor family) and **CC‑TGA‑06‑EX**; see **§4.7** for the retargeting witness shape and CV witness linkage.
    * **Holonic note:** The same module may appear as a holon in multiple views; supervisory loops (B.2.5) remain orthogonal to structural composition.
This is an expandable list of viewpoint families; TGA is intentionally viewpoint‑neutral. Additional engineering bundles beyond TEVB (safety, mission, information, …) are introduced as separate `U.ViewpointBundle` species via E.17.1/E.17.2; S12 does not define them.

**Alias families for transduction species (LEX‑only).**
*Scope.* Authors MAY declare `AliasesInViewFamilies[]` for `U.Transduction` species so readers can recognise familiar engineering view families. All semantics come from the referenced bundles (typically TEVB) and MVPK; aliases are purely lexical.

*Norms.*
1. Each `U.Transduction` species MAY publish `AliasesInViewFamilies[]` — an open list of records  
   `{ ViewFamilyId, EngineeringVPId?, Alias : TechASCII }`.  
   * If `ViewFamilyId = VF.TEVB.ENG`, then `EngineeringVPId` MUST be one of `{VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}` (TEVB; CC‑TEVB‑1/6).  
   * Other `ViewFamilyId` values MUST denote `U.ViewpointBundle` instances defined elsewhere (e.g. safety/assurance/information bundles), not ad‑hoc local families.
2. Aliases are LEX‑only: **no arithmetic, no new claims, no check participation, no `CtxState` slot writes/updates (incl. `DesignRunTag`)**. They do not create MVPK faces.  
3. Aliases MUST NOT be used as `PublicationVPId`; publication viewpoints remain in MVPK.  
4. Twin registers are allowed (Tech/Plain) per E.10; naming follows F.18 local‑first discipline.  
5. Do not name transductions by operands/effects (operation ≠ operand).  
6. `TypicalEnactorRoleName` MAY be added for pedagogy; it SHALL NOT be used as a GateFit role (GateFit uses `U.Role` only).  
7. Morphology: ASCII TitleCase; conjunctions via `And`; for composite actions use `XingAndYing` (or `XAndYing` if grammar requires).  
8. The P2W reference species table (SubstrateFormalization … EvaluatingAndRefreshing with functional/procedural aliases and `TypicalEnactorRoleName`) is **informative** and does not change kind or viewpoint semantics.

**Deliverable — `UTS.ViewpointMap` (normative, TEVB‑aligned).**  
Publish a UTS block named `ViewpointMap` that ties engineering viewpoints (from bundles such as TEVB) to E.TGA constructs and MVPK faces.

*Minimum row schema (per row).*
* `ViewFamilyId` — `U.ViewpointBundle.viewFamilyId` (e.g. `VF.TEVB.ENG` for TEVB, or another bundle id).  
* `EngineeringVPId : ViewpointId` — a viewpoint from that bundle (for TEVB, one of `{VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}`).  
* `PublicationVPId : ViewpointId?` — MVPK publication viewpoint id that governs faces implementing this engineering view (optional if not publishing).  
* `TargetHolon ∈ {U.System, U.Episteme}` *(extended species may add `{U.PromiseContent|U.MethodFamily}`; if `TargetHolon ≠ U.System`, no `U.Work` enactment appears).*  
* `PrimaryTGAConstructs` — nodes/edges/gates actually used for this `(ViewFamilyId, EngineeringVPId, TargetHolon)` (typically one of the four families above).  
* `Crossings{BridgeId, CL/CL^plane?}` — crossings involved; penalties route to R‑lane only.  
* `EditionPins{…}` whenever comparable claims appear (bind to CG‑Spec/ComparatorSet editions; any face citing editions includes `BridgeCard + UTS` row per MVPK/UNM).  
* `SenseCells[]` (≥ 2 per row), each citing Context name + edition (F.17/E.10 discipline; UTS‑wide coverage rules still apply).  
* *(REQUIRED when publishing)* `CorrespondenceRef[]` — ISO 42010 correspondences linking emitted faces to the engineering view(s) they implement; may cross architecture descriptions.  
* *(RECOMMENDED)* `ConcernsCovered[]` — ISO 42010 stakeholder concerns addressed by this row via GateProfiles/check catalogues.

**Conformance (S12‑scoped).**  
(i) `UTS.ViewpointMap` exists.  
(ii) For each holon that claims TEVB alignment, there are ≥ 4 rows whose `{ViewFamilyId, EngineeringVPId}` cover `{VF.TEVB.ENG × {VP.Functional, VP.Procedural, VP.RoleEnactor, VP.ModuleInterface}}` (per CC‑TEVB‑1/6).  
(iii) Rows that surface editions also include `BridgeCard + UTS` rows per A.27; edition‑bearing faces that lack such rows MUST NOT be used for downstream consumption.  
(iv) Each row has ≥ 2 `SenseCells` and the sheet meets global UTS coverage rules.  
(v) Any `TargetHolon = U.System` that reaches `U.Work` shows `LaunchGate` with `DesignRunTag` consistency.  
(vi) Crossings referenced in `ViewpointMap` follow CC‑TGA‑11; comparability along the mapped paths follows CC‑TGA‑10.  
(vii) Rows MUST NOT use an unqualified `ViewpointId`; they MUST use `EngineeringVPId` and/or `PublicationVPId` explicitly.  
(viii) When faces are published, `CorrespondenceRef[]` MUST be present and resolvable to `U.Viewpoint` ids.  
(ix) Additional bundles (e.g. assurance, information, mission) MAY appear as extra `ViewFamilyId` values but MUST be declared as `U.ViewpointBundle` species; they do not extend `VF.TEVB.ENG`.

### E.18:6 - Archetypal Grounding (Tell–Show–Show; concise)

*Show‑A (Supply chain).* Nodes: procurement → inbound QC (UNM) → selection (supplier set; lawful order) ↔ planning (lotting/schedule; budget) → execution (receipts; **WorkEnactment enacts (world‑contact)**) → refresh (quality telemetry; re‑emit faces). Crossings: vendor Context via **Bridge/CL**; penalties **→ R only**; comparators pinned to CG‑Spec edition. 

*Show‑B (Neural‑net functional).* Nodes: formal substrate (typed tensor ops) → mechanism (combinator algebra) → UNM (dataset normalization; **TransportRegistry^Φ**) → selection (architecture/hyperparam set; Pareto set over accuracy@ratio & FLOPs@ratio) ↔ planning (compute budget horizon) → Work (training runs; Δ anchored) → refresh (parity inserts; slice‑scoped). Faces pin **DescriptorMapRef.edition / DistanceDefRef.edition** when QD metrics are shown; illumination remains a **report-only telemetry metric** by default. 

> *Post‑2015 SoTA echoes (illustrative):* **TAMP/MPC**, **MAP‑Elites / QD (incl. CMA‑ME)**, **refinement‑typed stacks**, **profunctor optics**. **Worked‑examples and Tell–Show–Show vignettes move to A.31/A.34/A.37; E.TGA keeps only the carcass‑level alignment.**

### E.18:7 - Conformance — **Unified checklist (normative)**

| ID | Requirement | Practical test |
|----|-------------|----------------|
| **CC‑TGA‑01 — Single edge kind** | The graph uses exactly one edge kind `U.Transfer`; all plane/Context/edition transitions occur only at nodes via `OperationalGate(profile)`. | Model lint finds no auxiliary edge kinds for unit/plane changes; crossings sit on declared gates. |
| **CC‑TGA‑02 — Nodes are morphisms** | Nodes are intensional `U.Transduction(kind∈{Signature,Mechanism,Work,Check,StructuralReinterpretation})`. This enumeration is a **minimal roles baseline**. **Domain‑specific species are open‑world** and non‑exhaustive; they bind to one of these kinds. Adding a **new kind** requires an explicit E.TGA update. `StructuralReinterpretation` nodes are **projection‑preserving** (no mutation of `⟨L,P,E⃗,D⟩`) and carry CV/GF obligations per A.20/A.21/A.45. **Mapping to A.\*** (normative): the enumeration is **not** a TGA‑local taxonomy; each `kind` is identified 1‑to‑1 with its A.\* anchor: `Signature→A.6.0`, `Mechanism→A.6.1`, `Work→A.15`, `Check→OperationalGate` (until a dedicated A.\* pattern is published). | Type registry shows at least the listed kinds; additional species map to one of them; checks realized as `OperationalGate` (see CC‑TGA‑06‑EX/11). **Lint:** registry/table exposes `{species → {kind, KindDefinition}}`; missing or mismatched `KindDefinition` fails. |
| **CC‑TGA‑03 — Identity, composition, functorial faces** | Identities exist; path composition associative; publication is functorial: `Emit_s(t₂∘t₁)=Emit_s(t₂)∘Emit_s(t₁)`. | Pick two‑step path; MVPK faces commute (Square witness). |
| **CC‑TGA‑04 — Graph spec** | Spec declares `τ_V, τ_E`, `Γ_time`, Transport/Bridge registries. | Spec file shows typed registries and Γ policy. |
| **CC‑TGA‑05 — CtxState pins** | `CtxState=⟨L,P,E⃗,D⟩` is pinned on ports/tokens; raw `U.Transfer` does **not** write/update it. | Along a raw transfer, ⟨L,P,E⃗,D⟩ is preserved. |
| **CC‑TGA‑06 — Operational gates only** | Any write/update to any member of ⟨L,P,E⃗,D⟩ or entry into `U.WorkEnactment` is mediated by `OperationalGate(profile)` with aggregated `DecisionLog`. | Diff CtxState across edges; if any member differs, exactly one gate exists with DecisionLog. |
| **CC‑TGA‑06‑EX (strictly limited) — Projection retargeting without gate** | A node of kind **`StructuralReinterpretation`** MAY retarget the **published projection** without invoking `OperationalGate` **only if all hold**: **(a)** `⟨L,P,E⃗,D⟩` is preserved; **(b)** any **describedEntity** change has a **KindBridge** (`CL^k`) entry on MVPK/**UTS**; **(c)** a **SquareLaw‑retargeting witness** is present (on UTS); **(d)** the operation is **PathSlice‑local** (`PathSliceId` pinned); **(e)** **no plane/unit change** occurs (plane/unit changes remain gated); **(f)** **CV.ReinterpretationEquivalence** (A.20) is `pass`; **(g)** **NoHiddenScalarization** — if the step concerns a comparable return shape, set/partial‑order semantics are preserved and comparators remain ref‑only (cf. A.28). | UTS row includes `bridgeChannel=Kind` and `CL^k`; SquareLaw‑retargeting witness present; PathSliceId pinned; CV status recorded; no scalarization detected. |
| **CC‑TGA‑07 — CV⇒GF activation predicate** | Until **aggregated `ConstraintValidity` = `pass`**, all **GateFit** checks return `abstain`. | Simulate CV failure ⇒ GateFit `abstain`. |
| **CC‑TGA‑08 — LaunchGate discipline (incl. pre‑run barrier)** | Each `U.WorkEnactment` has exactly one `LaunchGate` owning `USM.LaunchGuard`; **mandatory** checks: `FreshnessUpToDate`, `DesignRunTagConsistency`. If preceding step’s CV ≠ `pass`, LaunchGate decision is `block` (cause logged). | Owner resolution `GuardOwnerGateId = LaunchGateId(U.WorkEnactment)`; CV≠pass ⇒ `block` with log. |
| **CC‑TGA‑09 — MVPK publication discipline** | Every surfaced node uses MVPK; faces carry `PublicationScopeId`, presence‑pins, **edition ids**, Γ pins; **no I/O duplication** or arithmetic; faces add no new numeric claims. | Cards show `PublicationScopeId`; pins present; no “signature”/math on faces. |
| **CC‑TGA‑10 — Normalize→Compare (CSLC)** | Any comparison cites **UNM/CG‑Spec** editions and **ComparatorSetRef**; ordinal claims are compare‑only; partial orders return sets; edition‑aware artifacts (QD/archives) pin `{DescriptorMapRef, DistanceDefRef, CharacteristicSpaceRef?}.edition`; **any face citing editions includes `BridgeCard + UTS row`**. **NoHiddenScalarization — detection criteria:** (1) return shape is **set/poset**, not scalar; (2) `ComparatorSetRef` is present and edition‑pinned; (3) MVPK faces add **no new numeric claims**; (4) any summarisation is **order‑preserving & set‑valued**; otherwise conformance fails. | Faces show comparator pins; archive pins present; linter rejects edition cites without UTS; scalarisation checks pass.
| **CC‑TGA‑11 — Crossings gated** | Cross‑Context/plane crossings publish **BridgeId + UTS + CL/CL^plane** and are mediated by `OperationalGate(profile)`; **Φ/Φ_plane penalties → R‑lane only**; describedEntity change publishes **KindBridge (CL^k)**. **Exception (StructuralReinterpretation):** a **projection‑only** describedEntity retargeting is surfaced **without** a gate **iff** **CC‑TGA‑06‑EX** holds; then the UTS row includes `bridgeChannel=Kind`, `CL^k`, and a **retargeting witness**; any plane/unit change falls back to a gated crossing; `PathSliceId` is pinned; UNM reuse cross‑context continues via `Transport`. | Crossing surfaces show Bridge/UTS/CL pins; penalties routing audited. |
| **CC‑TGA‑12 — Set‑returning selection** | `U.SelectionAndTuning` returns sets/archives under declared comparators (`ParetoOnly` by default) — no covert scalarization. | Selector output is a set/archive; policy id present if escalated. |
| **CC‑TGA‑13 — Budgeted Selection↔Planning loop** | The loop declares **budget / max_iter**; on expiry selector publishes partial‑optimal set + `MethodTuning`; next **PathSlice** scheduled. | Logs show budget stop and slice rollover. |
| **CC‑TGA‑14 — UNM before loop & Freshness lifecycle** | UNM runs before selection; stale/missing inputs produce **FreshnessTicket/FreshnessRequest** planned in `WorkPlanning` and executed in `WorkEnactment`; calibrations appear as `CalibrateTo(map|standard)` with Φ pins. | Ticket state machine Issued→Planned→Executed→Closed; calibrations pinned. |
| **CC‑TGA‑15 — FinalizeLaunchValues only in WorkEnactment** | Only `U.WorkEnactment` performs `FinalizeLaunchValues` and fills launch‑value slots. | Any earlier attempt blocks at LaunchGate; a `FinalizeLaunchValues` witness is present in Work. |
| **CC‑TGA‑16 — Guard ownership & semantics** | `USM.CompareGuard`/`USM.LaunchGuard` publish owner gate; guards are **events**, not GateChecks; failures are aggregated by owner’s gate per profile. | Guard pins show owner; GuardFail routed to owner’s DecisionLog. |
| **CC‑TGA‑17 — Assurance ops on Transfer** | On `U.Transfer` only `ConstrainTo/CalibrateTo/CiteEvidence/AttributeTo`; none write/update `⟨L,P,E⃗,D⟩`. | Edge audit shows ops; CtxState unchanged across the edge. |
| **CC‑TGA‑17a — Assurance ops contracts (normative)** | **ConstrainTo(region|policy)**: tightens declared region/policy; **pre**: region⊆current; **post**: `⟨L,P,E⃗,D⟩` unchanged; **idem.** and **monotone** under composition. **CalibrateTo(map|standard)**: attaches **editioned** calibration map/standard with Φ‑policy id; lawful per CG‑Spec; **post**: `⟨L,P,E⃗,D⟩` unchanged; **idem.** on same edition; penalties **→ R only**. **CiteEvidence(anchor)**: binds carriers via **SCR/RSCR**; adds no numeric claims; **idem.**; missing carriers ⇒ **abstain**. **AttributeTo(role|source)**: provenance only; decision algebra unaffected; **idem.** Hidden GateChecks, plane/unit changes, or edition writes on edges are **forbidden**. | Contracts visible on edge audit; violations fail lint. |
| **CC‑TGA‑18 — Flow = valuation & slice‑local refresh** | A flow declares valuation `ν` over `U.Transfer` plus `PublicationScopeId` and `PathSliceId`; **sentinel‑bounded** refresh; re‑emit on edition change or sentinel rule. | FlowSpec shows ν; sentinel bump triggers slice‑local recompute. |
| **CC‑TGA‑19 — Γ_time on compare/launch** | All compare/launch faces pin `Γ_time`; no implicit *latest*. | Face audit shows Γ pins; LaunchGate blocks on stale. |
| **CC‑TGA‑19a — Γ_time pin shape (normative)** | The `Γ_time` pin is one of: `snapshot(t)`, `interval[t1,t2]` (closed), or `policy(Γ_timeRuleId)` that resolves to either; CV computations record the **resolved time basis** in `DecisionLog` and do not widen Γ at publication time. | DecisionLog shows basis; linter rejects missing/implicit Γ. |
| **CC‑TGA‑20 — Lean publish‑mode ≠ weaken** | `AssuranceLane‑Lite` affects faces only; required GateChecks for the active profile remain intact. | Gate in Lean/Core shows minimal pins; GateChecks list unchanged. |
| **CC‑TGA‑21 — Decision stability & idempotency witness** | Gate decisions are stable under the equivalence relation defined in **A.41**; a **witness of equivalence** is present on the DecisionLog surface; any change that breaks equivalence requires re‑aggregation. **Minimum lexeme (CV‑relevant surfaces):** `EquivalenceWitness := { keys, E⃗, Γ_time(basis), PathSliceId?, ReturnShapeClass, ComparatorSetRef?, profile }`. | Modify any input outside the declared equivalence ⇒ re‑aggregation; DecisionLog records the witness (A.41); lexeme present.
| **CC‑TGA‑21a — Decision join (publication algebra)** | Aggregation over GateChecks is the **idempotent, commutative, associative join** on the lattice `abstain ≤ pass ≤ degrade ≤ block` with **neutral = `abstain`** and **absorbing = `block`**. The algebra is conceptual; publications surface only (i) the aggregated **GateDecision** and (ii) its **GateDecisionRationale** recorded in the **DecisionLog**. A **GateDecisionExplanation** is an optional human‑readable narrative derived from the GateDecisionRationale; it is **not** a decision and MUST NOT be used as one. If aggregated `ConstraintValidity ≠ pass` or the active profile suppresses narratives, any GateFit‑oriented GateDecisionExplanation **does not apply**. | Review a gate with multiple GateChecks: the aggregated decision matches the lattice join; no per‑check arithmetic is introduced on faces. |
| **CC‑TGA‑22 — Errors/unknowns fold by profile** | Errors/timeouts fold to `degrade` under `Lean|Core` and to `block` under `SafetyCritical|RegulatedX`; `unknown` folds per GateCheck policy (safety‑default: `degrade`). | DecisionLog shows folds; profile switch changes fold behavior accordingly. |
| **CC‑TGA‑23 — SquareLaw on crossings** | For every GateCrossing, `gate_out ∘ transfer = transfer' ∘ gate_in`; LaunchGate case is mandatory. | MVPK shows commuting square; inconsistency yields `block|degrade` per profile. |
| **CC‑TGA‑24 — UNM single‑writer** | `CG‑Spec`, `ComparatorSet`, `UNM.TransportRegistryΦ` editions are authored only by `UNM.Authoring` (others ref‑only). | Authorship cards: UNM is sole writer; others have refs only. |
| **CC‑TGA‑25 — Evidence lanes & DecisionLogs** | AssuranceLane surfaces GateProfile, GateCheckRef list, edition pins, aggregated decision, `DecisionLogRef`; **evidence pins follow a two‑layer scheme**: **carriers** are pinned via **`SCR/RSCR`**, and **value annotations** are surfaced under **`VALATA (VA/LA/TA)`**. | Gate surfaces include these pins; logs retrievable. |

> **Coupling note.** `CC‑TGA‑07 (CV⇒GF)` and `CC‑TGA‑21a (Decision join)` together ensure that any GateFit‑scoped GateCheckRef **returns `abstain`** until the aggregated CV status equals `pass`; CV/GF separation remains intact. 
> **Authoring note (scope of E.TGA vs A.*):** Detailed, mechanism‑level checks and most publication content are specified in the **A.* patterns** (A.20…A.42). E.TGA fixes only carcass‑level obligations above.

**Glossary (additions)**  
* *Open‑world species* — non‑exhaustive domain‑level specializations of `U.Transduction` that map to the minimal kind set.  
* *Signature (TGA kind)* — `U.Transduction(kind=Signature)`; **identical to** **A.6.0** `U.Signature` (universal block). **Not** a `C.3.2 KindSignature`.  
* *KindSignature (C.3.2)* — intensional definition of a `U.Kind` (intent/extent, F); **unrelated** to TGA kinds; never a `genus`.  
* *Species (domain‑level)* — typed specialisations `speciesOf(kind=…)` that **MUST** declare `KindDefinition=A.*` id (e.g., `kind=Mechanism; KindDefinition=A.6.1`).  
* *KindBridge (`CL^k`)* — a compatibility surface on UTS for describedEntity/kind transitions; required by CC‑TGA‑06‑EX and crossings (CC‑TGA‑11).
* *Eulerian interpretation* — operational stance where a flow is treated as a valuation over `U.Transfer` and edges perform assurance‑only operations (no token‑passing semantics).
* **GateCheckRef shape (publication lexeme, normative here).** Where GateChecks are surfaced, a **GateCheckRef** is a record
  `GateCheckRef := { aspect, kind, edition, scope }` with:
  `aspect ∈ {ConstraintValidity, GateFit}`, `kind ∈ GateCheckKind`, `edition ∈ Editions`, and `scope ∈ {lane | locus | subflow | profile}`. 
* **GateDecision / GateDecisionRationale / GateDecisionExplanation (terminology).**
  — **GateDecision** — the aggregated lattice value produced by `OperationalGate(profile)` for a specific `{GateProfile, GateCheckRef[]}`.
  — **GateDecisionRationale** — the minimal structured support **for that GateDecision**: per‑check outcomes, profile‑bound folds, and surfaced evidence/witness references on the DecisionLog; it records **why the GateDecision is admissible** under the active profile.
  — **GateDecisionExplanation** — an optional human‑readable narrative derived from the GateDecisionRationale; it **does not carry decision status**. While aggregated `ConstraintValidity ≠ pass`, GateFit‑scoped checks return `abstain`; any GateFit‑oriented GateDecisionExplanation **does not apply**.
> **Clarity note.** **GateDecision ≠ GateDecisionExplanation**; narratives are optional and derivative of GateDecisionRationale.

* **GateFit (aspect, not an entity).** GateFit names the **aspect** of checks that evaluate **profile‑fit**; there is no separate GateFit entity. “Gate decision under GateFit” means “the gate’s decision computed from GateChecks with `aspect=GateFit`”.

  This shape is publication‑level only; it introduces no new execution steps and no arithmetic on faces.  (Couples to A.20/A.21 without duplicating their check catalogs.)
* *VALATA (VA/LA/TA)* — value‑annotation scheme used on **AssuranceLane**; **carriers** are referenced via **SCR/RSCR**; detailed obligations live in A.10/A.29. Included here so evidence pins are self‑describing in E‑level texts.
* *Transfer vs Transport* — **Transfer** = the sole graph edge kind `U.Transfer`. **Transport** = Φ‑policy/registry‑defined conversions (`TransportRegistry^Φ`) referenced by UNM; “reuse via Transport” refers to the latter.
* *GateCrossing* — a typed node transition that writes/updates a CtxState slot or the kind‑channel; see **S1.b** for the normative list and required pins.
* *Admissible path* — a typed path obeying the GateCrossing discipline (no hidden crossings; witnesses present), Γ‑pinned on compare/launch, and `T^D↔T^R` only at `LaunchGate`; see **S2**.

### E.18:8 - Gating Profiles (applied to E.TGA)

> Gating is expressed as **publication‑gating** per E.17 profiles. The graph model aligns with the **CC items** listed for the chosen profile; higher profiles include all lower‑profile items.

| Profile                          | Required CC‑items                                         | Additional notes                                                                               |                                                                  |
| -------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Lean**                         | 01–06, 08–09, 11–12, 15, 19–21, 25                                                                                                           | Minimal MVPK presence; LaunchGate keeps `FreshnessUpToDate` & `DesignRunTagConsistency`. |
| **Core**                         | **Lean** + 07, 10, 13–14, 16–18, 22–23, 24                                                                                                  | Adds CV⇒GF order, CSLC pins, budgeted loop, guards, valuation/sentinel refresh, error folds, SquareLaw, UNM single‑writer. |
| **Safety‑Critical / RegulatedX** | **Core** + profile‑specific GateChecks (safety envelope, regulator id/editions) with stricter folds per **CC‑TGA‑22**; SquareLaw audits tightened | — |

**Recommended defaults (non‑normative, tie‑in to A.26).** Profiles inherit along a `PathSlice`; local overrides may only **add** GateChecks; weakening requires a new `PathSlice` via sentinel (cf. A.26/A.25).

### E.18:9 - TGA LEX discipline (registration)
Register Tech tokens (ASCII) used by this architecture with twin‑labels: `U.TransductionGraph`, `U.TransductionFlow`, `StructuralReinterpretation`, `OperationalGate`, `GateProfile`, `GateCheckRef`, **`GateCheckKind`**, `DecisionLog`, `USM.CompareGuard`, `USM.LaunchGuard`, `KindBridge`, `SubflowRef`, `FlowEmbed`, `SentinelId`, `PathSliceId`, `SliceRefresh`, `FinalizeLaunchValues`, `VALATA`. Add an ASCII alias **`CLKind`** ↔ Plain `CL^k` (cf. `CLPlane` ↔ `CL^plane`). Reference MVPK E.17 naming for faces.  
**CtxState Extension Registry.** Register any extra CtxState slot beyond ⟨L,P,E⃗,D⟩ with: slot id, informal intent, partial‑order law (with neutral/absorbing), SquareLaw compatibility note, and the owning Gate profile(s) that may change it. Absence of registration ⇒ **non‑conformant**.

### E.18:10 - Consequences

**Benefits.**

1. **Universality with discipline:** one edge kind and explicit gates eliminate “second process ladders” and make cross‑domain flows (ML, supply‑chain, TAMP/MPC, scientific workflows) uniformly analyzable and auditable.
2. **Comparability & replayability:** CSLC and edition‑pinned comparators prevent covert scalarization and enable lawful set returns and reproducible decisions.
3. **Locality of change:** sentinel subflows restrict refresh to affected `PathSlice`s; large graphs remain stable under frequent edition bumps.
4. **Clean design/run fold:** LaunchGate and `DesignRunTagConsistency` stop premature launch‑value slot filling; acceptance and telemetry live where they occur (`U.Work`).
5. **Assurance visibility:** MVPK makes GateProfile/DecisionLog surfaces locally checkable and cacheable for the same `{PathSlice, GateChecks, Editions}`.

**Trade‑offs.**
a) **Higher upfront modeling cost:** explicit Bridge/UTS pins and GateProfiles demand care; mitigated by Lean profile and templates.
b) **Longer edge surfaces:** MVPK faces are verbose by design; Lean surfaces can be used for low‑risk segments.
c) **Tooling alignment:** some incumbent DAG‑only orchestrators conflict with budgeted cycles and set‑return semantics; adapters must project E.TGA semantics to their interop layer (never the other way round).

### E.18:10 - Rationale

E.TGA enforces **strict separation of concerns** (carcass‑level only); **specialized semantics live in A.* patterns**:

* **What the graph is:** typed intensional morphisms and a single transport edge `U.Transfer`.
* **Where/when it may cross contexts:** **only** at `OperationalGate(profile)`, with Bridge+UTS, CL/CL^plane, and Φ routed to R‑lane.
* **How comparability works:** UNM authors units/planes/transports (single writer) and selectors operate **only** on normalized, edition‑pinned comparators, returning sets/archives—not totals. **Edition‑aware pins and archive semantics are tested in A.28/A.34/A.37 (not repeated here).**
* **How change propagates:** sentinel‑bounded `PathSlice` refresh; editions are monotone; LaunchGate is the only binder of launch‑values.

This arrangement guarantees **functorial publication** (commuting squares on crossings) and **orthogonality** of inner technical validity (ConstraintValidity) to context fit (GateFit), which in turn makes gate aggregation **order‑independent** and cements the CV⇒GF activation predicate.

### E.18:11 - SoTA‑Echoing (post‑2015, multi‑Tradition)

> Each item states **Adopt / Adapt / Reject**, and why. Vendor/tool tokens are kept as *informative*, not normative.

1. **Applied category theory (compositional open systems).**
   **Adopt.** Monoidal composition and wiring justify “nodes as morphisms, edges as carriers” and functorial publication of faces; they also provide algebraic laws for joining subflows. (Fong & Spivak, *Seven Sketches in Compositionality*, 2019).

2. **Operads / wiring diagrams / hypergraph categories.**
   **Adopt/Adapt.** Typed ports and decorated cospans model interfaces and “Bridge” junctions; we adapt the operadic composition to require CL/Φ pins on every crossing (publication‑level requirement not present in the math). (Spivak, *Operads of Wiring Diagrams*, 2021; Baez & Fong, *A Compositional Framework for Passive Linear Circuits*, 2015).

3. **Open‑graph/string‑diagram rewriting.**
   **Adapt.** Rewriting systems capture subflow refactors, but E.TGA binds rewrites to edition bumps and sentinel scopes rather than global rewrites, to preserve auditability and replay. (Bonchi et al., *Graphical Linear Algebra*, 2019; Kissinger—survey lineage).

4. **Publication discipline & artefact portability.**  
**Adopt.** Edition‑pinning and immutable registries echo contemporary reproducibility practice; E⃗ stays explicit and compositional at the publication layer.

5. **Reproducibility & content addressability.**  
   **Adopt.** Edition‑pinning and immutable registries echo modern content‑addressable reproducibility (conceptual); E⃗ stays explicit and compositional at the publication layer.

6. **TAMP/MPC (integrated planning and control).**
   **Adopt/Adapt.** The budgeted Selection↔Planning loop follows contemporary TAMP practice; MPC‑style freshness/constraint checks motivate **FreshnessUpToDate** as a hard LaunchGate module and “bind‑in‑Work‑only”. (Garrett, Lozano‑Pérez, Kaelbling, *Integrated Task and Motion Planning*, 2021; Rawlings et al., MPC updates).

7. **Quality‑Diversity (QD) search.**
   **Adopt.** QD (e.g., CMA‑ME, 2020) justifies **set‑return** and archive semantics in `U.SelectionAndTuning`; E.TGA bans covert scalarization that would collapse archives to single “bests”.

8. **Profunctor optics (modular projections).**
   **Adopt/Adapt.** Optics motivate view/projection discipline behind MVPK faces; we adapt by forbidding MVPK faces from introducing new claims (they are pure projections, not transformations). (Pickering, Gibbons, Wu, **Profunctor Optics**, 2019).

*Cross‑tradition note.* Items 1–3 (category‑theoretic), 4–5 (publication/reproducibility concepts), 6 (controls/robotics), 7 (evolutionary search), and 8 (PL/semantics) jointly anchor E.TGA across multiple traditions, per E.8.

### E.18:12 - Bias‑Annotation (per E.8 SG‑bias slot)

* **Acyclic‑bias risk.** Tooling accustomed to DAGs may discourage legal feedback loops; E.TGA explicitly permits loops with budget/sentinel controls (CC‑TGA‑13,‑18).
* **Scalarization‑bias risk.** Cultural defaults to single‑score rankings can suppress Pareto/QD sets; E.TGA requires lawful orders and return‑sets (CC‑TGA‑10,‑12).
* **Interop‑dominance risk.** File/format ecosystems (CWL/RO‑Crate/lineage) can leak into semantics; E.TGA places them in **InteropCard** and keeps intensional semantics in nodes/gates.
* **Over‑formalization risk.** Category‑theoretic formalisms can obscure operational guard‑rails; E.TGA grounds crossings in Bridge/UTS/CL/Φ pins and SquareLaw audits (CC‑TGA‑11,‑17).
* **Retrospective rewrite risk.** Global rewrites break replay; E.TGA confines them to edition bumps and slice‑local refresh (CC‑TGA‑16).

**Mitigations.** Profile‑gated publication, audit of `DecisionLog`, mandatory edition pins, Lean‑to‑Core upgrade paths, and conformance tests tied to PathSlice replay.

### E.18:13 - Relations (explicit pattern‑to‑pattern edges)

> Directed edges (→) are typed as **builds_on / constrains / hosts / specializes / publishes_on / requires / provides_checks_for**.

**Foundations**
* **E.TGA →builds_on→ E.17 MVPK (for Morphisms).** Faces, pins, lanes, functorial publication, Lean/Core/Regulated profiles.
* **E.TGA →builds_on→ A.6.0 U.Signature / A.6.1 U.Mechanism.** Node kinds and intensional content boundaries.
* **E.TGA →builds_on→ A.7 Strict Distinction (I/D/S vs Surface).** No new claims on faces; faces project morphisms.

**Flow semantics & checks**
* **E.TGA →hosts→ A.20 U.Flow (ConstraintValidity scope).** CV checks live inside transformations; no declaration/translation of planes/units in CV; **error/timeout/unknown folds** follow **CC‑TGA‑22** as the **minimum default** (profiles may be stricter).
  **Terminology discipline (A.20 boundary).** In CV scope, publications use **status/witness** language; **GateDecisionRationale/GateDecisionExplanation** are reserved for gating and do not apply to CV.
* **E.TGA →hosts→ A.21 GateProfilization (GateFit scope).** **GateFit-scoped GateChecks** are aggregated by `OperationalGate(profile)` with CV⇒GF activation; the **enumeration and publication shape** of GateChecks live in **A.21**. **Equivalently:** a GateFit decision different from `abstain` appears only when aggregated `ConstraintValidity = pass`; otherwise the **GateDecisionExplanation (GateFit‑oriented)** does not apply.
* **E.TGA →requires→ USM.CompareGuard / USM.LaunchGuard.** Guards publish scope & ownership; guard failures route to owner gate.
* **E.TGA →constrains→ F.* (Bridge+UTS, CL/CL^plane, Φ→R).** A transition is treated as a **Crossing** iff `Bridge+UTS` and the appropriate `CL/CL^plane` are surfaced; otherwise this crossing explanation does not apply. Where Φ defines penalties, they appear in the R‑lane only.
* **Operational interpretation (default): Eulerian.** A flow is a **valuation** over `U.Transfer`; edges carry **assurance‑only operations** (see CC‑TGA‑17); no token‑passing semantics are assumed.

**UNM & comparability**
* **E.TGA →constrains→ UNM.Authoring / UNM.Usage.** Single‑writer for `CG‑Spec/ComparatorSet/UNM.TransportRegistryΦ`; normalize‑then‑compare is mandatory.
* **E.TGA →constrains→ G.5 SelectionAndTuning.** Set‑returning, comparator‑pinned decisions, no hidden scalarization; `MethodTuning` without launch‑value slot filling.
* **E.TGA →constrains→ G.11 EvaluatingAndRefreshing.** EditionBumpProposal, two‑phase commit in UNM.Authoring, path‑local refresh.

**Work boundary**
* **E.TGA →requires→ A.15 U.WorkEnactment (`FinalizeLaunchValuesOnlyInWork`).** Single point of `FinalizeLaunchValues`; `FreshnessUpToDate` hard at LaunchGate; acceptance/telemetry published here.

**Structure & reuse**
* **E.TGA →specializes→ U.TransductionFlow (and its family).** The graph architecture is the common substrate on which flow patterns (e.g., P2W, EvaluatingAndRefreshing) are defined; E.TGA ensures their crossings, guards, and MVPK faces are coherent.
* **E.TGA →publishes_on→ E.17 MVPK views** (`PlainView`, `TechCard`, `InteropCard`, `AssuranceLane`) for every edge/node where publication occurs; Lean mode allowed only as per profile.

### E.18:14 - Conformance evidence (how to show you comply)

1. **Model lint:** run static checks for CC‑TGA‑01…25 (edge kind, gates on crossings, CV⇒GF, guard ownership, single‑writer UNM, SquareLaw).
2. **Publication audit:** sample a commuting square and a sentinel‑bounded subflow; verify pins and DecisionLog behavior on *block/degrade*.
3. **Replay test:** freeze editions; re‑run selection on a PathSlice; observe identical return‑sets; apply a bump; see only affected `PathSlice`s refresh.
4. **StructuralReinterpretation probe:** construct a minimal reinterpretation step; confirm `CL^k` with `bridgeChannel=Kind` on UTS, a SquareLaw‑retargeting witness on UTS, `PathSliceId` pinned, **CV.ReinterpretationEquivalence=pass**, and absence of hidden scalarization.

[20]: https://webstore.ansi.org/preview-pages/ISO/preview_ISO%2B23247-1-2021.pdf?srsltid=AfmBOooAUXpg38IpkTlUFtcCpaMVOjivkewJWDIUd1VemIJO91abNEkG "INTERNATIONAL STANDARD ISO 23247-1"

### E.18:End

