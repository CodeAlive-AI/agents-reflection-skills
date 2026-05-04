## A.6.3.RT - RepresentationTransduction — same-described-entity representation-scheme transition

**Placement.** Specialization under `A.6.3 U.EpistemicViewing` for same-described-entity representation-scheme transition.  
**Builds on.** `A.6.3 U.EpistemicViewing`; `A.6.2 U.EffectFreeEpistemicMorphing`; `A.7`; `E.10.D2`; `C.2.7`; `E.17.0`; `E.17`; `F.9`; `F.18`.  
**Coordinates with.** `ConservativeRetextualization`; `ExplanationFaithfulnessProfile`; `E.17.ID.CR ComparativeReading`; `A.6.4 U.EpistemicRetargeting`; `A.15`; `A.20`; `A.21`; explicit decoding-access review.

**One-line summary.** `RepresentationTransduction` is a same-described-entity shift in representation scheme that stays inside `A.6.3 U.EpistemicViewing`: it may move between prose, table, diagram, structured notation, or another declared representation regime, but it does **not** silently change `describedEntityRef`, promote geometry or notation into ontology-by-default, or hide decode-mediated recoverability behind surface fluency.

### A.6.3.RT:1 - Problem frame

The same described entity often needs to be carried across more than one representation regime:
- prose into a table that makes comparison or coverage clearer;
- a table into a diagram that foregrounds dependency or topology;
- a diagram into a structured notation suitable for replay or technical review;
- a source representation into another regime that changes reasoning affordances without changing the underlying object-of-talk.

In practice these shifts are often treated as harmless reformatting. But some representation changes alter reasoning affordances, weaken recoverability, or quietly change what appears to be present in the source. FPF already has `A.6.3` for same-described-entity conservative viewing. This pattern names the recurring same-described-entity case where the published result changes representation scheme while the case still remains inside `A.6.3`.

### A.6.3.RT:2 - Problem

Without a dedicated named pattern for representation-scheme transitions:
1. teams treat text-to-table, table-to-diagram, and notation shifts as if they were all the same kind of harmless rewrite;
2. changes in reasoning medium and recoverability remain implicit;
3. latent/distributed cases tempt authors to treat geometry or feature clusters as ontology-by-default;
4. reviewers cannot tell when a case is still same-entity viewing and when it has become retargeting, explanation, carrier work, or decode-mediated reconstruction;
5. representation factors owned near `C.2.7` are discussed rhetorically rather than as explicit deltas.

### A.6.3.RT:3 - Forces

- **Same entity, different reasoning medium.** Teams need different representational forms without silently changing the described entity.
- **Legibility vs recoverability.** A clearer representation is useful only if readers can still recover how it relates to source claims, anchors, and pins.
- **Representation change vs ontology drift.** A new notation or geometry can make structure more visible, but it must not silently become a new object-of-talk.
- **Recoverability before decode ambition.** Start from cases where recoverability can be reviewed directly before leaning on decode-mediated reconstruction.
- **Owner restraint.** This pattern must stay under `A.6.3`, not swallow explanation governance, retargeting, bridge work, or carrier work.

### A.6.3.RT:4 - Solution — same-described-entity representation-scheme transition under `A.6.3`

#### A.6.3.RT:4.1 - Informal definition

> `RepresentationTransduction` is a named pattern specialized under `A.6.3 U.EpistemicViewing` for same-described-entity transitions across declared representation schemes.
>
> It preserves `describedEntityRef`, keeps the transform effect-free, and makes explicit what changes in representation factors, reasoning medium, recoverability, and loss profile.
>
> It may move between prose, table, diagram, structured notation, or another declared representation regime. It may not silently change the described entity, silently import bridge semantics, or treat decode-mediated structure as if it were directly given.

#### A.6.3.RT:4.1.a - Pattern, case, and published rendering distinction

`RepresentationTransduction` is an **intensional pattern** and a named specialization under `A.6.3`. Concrete same-described-entity representation changes are passive episteme-level cases or published renderings reviewed under this pattern; the pattern itself does not act, decide, or publish.

This distinction matters because the pattern governs **how** a representation change is recognised, justified, and checked. It does **not** turn every table, diagram, or structured notation into a giant standalone review object, and it does not reduce review to a mechanical reformatting step.

#### A.6.3.RT:4.1.b - Local working vocabulary

This pattern uses a small local vocabulary for review.
- **Representation scheme** = the published form in which the same entity is rendered (for example prose, table, diagram, or structured notation).
- **Reasoning medium** = the form-specific affordances readers actually use when inspecting the published material.
- **Semiotic mode** = what kind of meaning-bearing support is doing the main work in the rendering, such as structural likeness, trace/index, conventional code, model-mediated correspondence, or decode-mediated recoverability.
- **Factor delta** = the explicit change in representation factors that matters for review.
- **Source tether** = the visible link back to pinned or otherwise reviewable source material that keeps same-entity support honest.
- **Decode-mediated case** = a case where explicit access to the target representation depends on a declared decoding route rather than direct reading from already published source material.

These terms are local review aids. They do not create a new face family or a new ontology owner.

#### A.6.3.RT:4.2 - Scope and exclusions

**In scope**
- text-to-table shift over the same described entity;
- table-to-diagram shift over the same described entity;
- diagram-to-structured-notation shift where the represented entity and claim-bearing material stay preserved;
- other same-entity representation-scheme changes with explicit recoverability discipline.

**Out of scope**
- any change of `describedEntityRef` or hidden change of object-of-talk (`A.6.4`);
- explanation-facing renderings whose main purpose is didactic or explanatory surface work (`ExplanationFaithfulnessProfile`);
- purely textual rewrites that stay inside one representation regime (`ConservativeRetextualization`);
- carrier work such as rendering, export, upload, serialization, or OCR/parsing-like extraction;
- latent/distributed use without explicit decode route and recoverability evidence.


#### A.6.3.RT:4.2.a - Reader guidance

Use this pattern when the object-of-talk stays fixed but the published result changes representation scheme or reasoning medium.
- If only wording changes, stay in `ConservativeRetextualization`.
- If the target mainly teaches, narrates, or explains, move to `ExplanationFaithfulnessProfile`.
- If same-entity support fails, move to `A.6.4`.

#### A.6.3.RT:4.2.b - What a reviewer checks first

A reviewer usually starts with five questions:
1. Is the described entity still the same, or has the object-of-talk shifted?
2. What changed in representation scheme and reasoning medium?
3. Can the target still be tethered back to source-bearing material strongly enough for same-entity reading?
4. Has the case quietly become explanation, bridge-bearing comparison, retargeting, or carrier work?
5. If decoding is involved, is the evidence class strong enough for the intended face and use?

Only after these questions are answered clearly does a fuller load-bearing review record normally become necessary.

#### A.6.3.RT:4.3 - Working-model first; explicit review record only when the case is load-bearing

Most same-described-entity representation shifts should stay human-usable and reviewable without turning every table, diagram, or structured rendering into a giant metadata block. This pattern therefore follows **E.14's working-model-first discipline**: ordinary non-latent cases need enough explicitness to show what stayed the same, what changed in representation and reasoning medium, what was lost or foregrounded, and where the case would have to reroute.

**Ordinary case (default).** For everyday same-described-entity representation shifts, it is usually enough that the rendering or its surrounding publication keeps explicit:
- which source material is being re-expressed in a different representation regime;
- that `describedEntityRef` remains preserved;
- what changed in representation scheme or reasoning medium;
- what losses, foregrounding choices, or recoverability limits matter for the reader;
- where the case exits if it has turned into explanation, retargeting, bridge-bearing comparison, carrier work, or decode-mediated reconstruction with insufficient support.

**Explicit review record (only for load-bearing cases).** A fuller record is warranted when the case is assurance-facing, gate-adjacent, cross-context, correspondence-heavy, decode-mediated, policy-bearing, or likely to be disputed. The record may inherit host ids and already-pinned metadata instead of restating them inline. When published, that record normally captures:
- transform placement (`landingForm = specialization under A.6.3`, `hostOwner`, `sourceForm`, `targetForm`, `changeLocus`);
- preservation context (`describedEntityPolicy = preserve`, `boundedContextPolicy`, `viewpointPolicy`, `referenceSchemePolicy`, `representationSchemePolicy`, `groundingPolicy`, `referencePlanePolicy`);
- claim and publication discipline (`claimPolicy`, `claimScopePolicy`, `publicationScopePolicy`, `reliabilityTransportPolicy`, `pinningPolicy`, `provenancePolicy`, `lossProfile`);
- continuity and bridge discipline (`claimContinuityClass`, `microtheoryContinuityClass`, `onticContinuityClass`, `bridgeRequirement`);
- downstream and admissibility discipline (`worldContactPolicy`, `evidencePolicy`, `gatePolicy`, `workCrossing`, `upstreamOwner`, `downstreamOwner`, `admissibleFaces`, `admissibleSurfaces`, `compositionLaw`, `reopenCondition`);
- representation and recoverability discipline (`representationFactorDelta`, `inferenceRegimeDelta`, `semioticModePrimary?`, `semioticModeSupport?`, `semioticModeShift?`, `modeOverreadRisk?`, `salienceShift?`, `topologyShift?`, `actionabilityShift?`, `calibrationShift?`, `interactivityShift?`, `onticScaffoldPreservation`, `onticRecoverabilityClass`, `onticRecoverabilityMode`, `RecoverabilityEvidenceClass`, `decodeMechanismRef`, `CorrespondenceModelRef?` where needed);
- naming and presentation discipline (`publicNamePolicy`).

#### A.6.3.RT:4.3.a - Working admissibility defaults

By default in this pattern:
- primary admissible faces for non-latent cases are `Plain` and `Tech`;
- bounded report-only use is lawful when source pins, provenance, loss notes, and same-described-entity support remain visible;
- `Interop` use is lawful only when the host explicitly permits source-pinned, structure-preserving export without added semantics;
- `Assurance` or gate-bearing use is not default and requires host-explicit policy plus source-pinned same-entity support;
- latent/distributed variants remain bounded until explicit recoverability evidence and decode-route discipline are published.

#### A.6.3.RT:4.4 - Direct and correspondence-mediated profiles

**Direct RepresentationTransduction**
- source and target are representation-scheme variants over one same-described-entity source line;
- no `CorrespondenceModelRef` is required;
- the main burden is explicit factor delta, reasoning-medium delta, and recoverability discipline.

**CorrespondenceRepresentationTransduction**
- the target representation is derived through a declared correspondence between epistemes or views of the same described entity;
- `CorrespondenceModelRef` is required;
- the result remains under `A.6.3` only if same-entity conservativity is still supportable and the correspondence does not silently import extra claims.

Correspondence-mediated representation work does **not** by itself grant bridge licence, substitution licence, or comparative-reading licence. If the case needs those burdens, they must be declared separately rather than hidden inside representation language.

#### A.6.3.RT:4.4.a - Recurring same-entity representation moves

Recurring same-entity moves under this pattern include:
- **Tabulation** — prose or dispersed claims are rendered into a table that exposes comparison or coverage more clearly.
- **Diagramming** — a table or prose relation set is rendered into a diagram that foregrounds structure while remaining source-tethered.
- **Structured notation shift** — prose, table, or diagram material is rendered into a notation better suited for disciplined replay or technical inspection.
- **Correspondence-supported representation shift** — the target representation depends on declared same-entity correspondence support without thereby becoming a bridge case.

These are recurring move shapes under one host relation. They are not separate owners and they do not override `E.17` face discipline.

#### A.6.3.RT:4.4.b - How a reviewer reads representation-factor and reasoning-medium change
A reviewer should be able to say, in one short paragraph, what changed in representational shape, what changed in reasoning medium, and whether the primary change is also a `semioticModeShift` rather than only a scheme change. Typical read-outs are: "the table foregrounds comparability across rows", "the diagram foregrounds dependency shape", or "the notation foregrounds explicit argument positions."

When the case is more demanding, that paragraph should also name whether salience, topology, actionability, calibration, or interactivity materially changed. If the author cannot name those shifts without slipping into new ontology, hidden bridge work, or a changed described entity, the case is not yet ready to stay here. Use `semioarchitecture-representation-delta-review-crib-sheet-v0.1.md` and `semioarchitecture-semiotic-mode-axis-note-v0.1.md` when the deltas need a more normalized read-out.

#### A.6.3.RT:4.5 - Shared representation law packet

##### A.6.3.RT:4.5.a. Preservation law
`RepresentationTransduction` preserves the same described-entity line, bounded context, and declared claim-bearing source while changing the representation scheme and, often, the reasoning medium. It must state what remains preserved about the ontic scaffold, claim scope, publication scope, pins, provenance, and grounding. It must also state whether the case remains direct or correspondence-mediated.

##### A.6.3.RT:4.5.a.1. Local conservativity witness
For this pattern, a new intensional claim is introduced when the target rendering:
- upgrades a source-visible relation into a stronger relation theory or stronger dependency semantics;
- turns geometry, notation, embedding proximity, or decoder output into ontology-by-default;
- adds bridge, substitution, comparative-reading, or mechanism claims not already licensed by the source line or declared correspondence;
- collapses source alternatives, uncertainty, or bounded scope into one stronger commitment;
- or treats decode-mediated recoverability as if it were direct givenness.

Conservativity is approximated here by checking, together, `describedEntityPolicy = preserve`, source-tether strength, factor delta, reasoning-medium delta, loss profile, ontic scaffold preservation, and whether each target-side connective can be pointed back to pinned source material or declared same-entity correspondence support.

##### A.6.3.RT:4.5.b. Loss and reliability law
A reviewed case under this pattern makes explicit which distinctions, affordances, or local cues are lost, foregrounded, or rearranged by the shift in representation regime. Reliability transport may remain source-bounded or be explicitly downgraded, but it must never be silently strengthened just because the target form looks clearer, more structured, or more formal.

##### A.6.3.RT:4.5.c. Authority and handoff law
A case reviewed under this pattern stays same-entity and episteme-level. It does not own retargeting, bridge stance, explanation governance, executable docking, gate authority, or work enactment. If the shift depends on decode-mediated recovery, intervention-backed extraction, or world/gate consequences, those dependencies must stay explicit and may restrict the target to exploratory or report-only use.

##### A.6.3.RT:4.5.c.1. Same-entity entry condition for decode-mediated cases
A decode-mediated case may stay here only when the target rendering is tethered back to already pinned and provenance-bearing source material for the same described entity. A decode-mediated result alone does not establish the same described entity strongly enough for this pattern.

##### A.6.3.RT:4.5.d. Composition and reopen law
Repeated same-regime normalization may be idempotent, but heterogeneous regime shifts are generally order-sensitive. The case must reopen whenever recoverability assumptions, pins, provenance, correspondence support, or target-face admissibility change. A representation shift also reopens if what looked like one same-entity line turns out to require a new described entity or a decode route stronger than currently declared.

#### A.6.3.RT:4.6 - Hard boundary rules

A case reviewed under this pattern keeps the following explicit:
- `describedEntityPolicy = preserve` is mandatory;
- any change of `DescribedEntityRef` exits to `A.6.4`;
- purely textual rewrite cases stay with `ConservativeRetextualization`;
- explanation-facing cases stay with `ExplanationFaithfulnessProfile`;
- carrier work stays outside this pattern;
- geometry, notation, embedding space, or feature clustering must not become ontology-by-default;
- the family changes representation scheme, not face ownership, and it therefore stays under existing `E.17.0 / E.17` face discipline rather than creating a new publication family.

If recoverability depends on decoding, probing, or intervention, the evidence class must bound admissible use; otherwise the case stays exploratory, report-only, or outside the admissible same-described-entity path under `A.6.3.RT`. Low-evidence decode-mediated results are not weaker canonical publications; they are bounded exploratory or report-only renderings. Non-latent cases remain the default entry path until decode-mediated recoverability is made explicit.

### A.6.3.RT:5 - Archetypal grounding

#### A.6.3.RT:5.1 - Same-entity text-to-table shift
**Source slice.** `Service S showed three recurring latency spikes in the evening batch window. Trace T-44 and dashboard pin D-17 identify the same service and time window.`

**Published table slice.** `| Service | Window | Spike count | Source pins |
| Service S | Evening batch | 3 | T-44, D-17 |`

This is a lawful direct `RepresentationTransduction` if no new claims are introduced, the same described entity stays explicit, and the representation-factor delta is declared. In ordinary engineering use, this usually needs a visible source tether, explicit loss notes if anything was omitted, and a clear statement that the table is still about the same service occurrence rather than a new derived object.

#### A.6.3.RT:5.2 - Same-entity table-to-diagram shift
**Source table slice.** `| Node | Depends on |
| CoolingLoop | Sensor A |
| CoolingLoop | Valve B |`

**Published diagram slice.** `CoolingLoop -> Sensor A; CoolingLoop -> Valve B`

The move stays in this pattern only if the described entity is preserved, the diagram does not silently add new semantic commitments, and reasoning-medium change is declared. If the diagram starts asserting a stronger dependency theory than the source table actually states, the case must reopen and may leave this pattern.

#### A.6.3.RT:5.2.a - Correspondence-mediated text-to-table shift
**Source prose slice.** `In the safety view, CL-2 maintains the required temperature condition during standard load.`

**Published table slice.** `| View | Entity | Condition | Correspondence model |
| Safety | CL-2 | required temperature condition during standard load | CM-12 |`

The move stays in this pattern only if the correspondence remains explicit, the described entity stays preserved, and the resulting table does not quietly import bridge semantics or a changed object-of-talk. Because the correspondence burden is doing real work here, a fuller review record is often warranted instead of relying only on the rendered table.

#### A.6.3.RT:5.2.b - Same-entity diagram-to-structured-notation shift
**Source diagram slice.** `CoolingLoop -> Sensor A; CoolingLoop -> Valve B`

**Published notation slice.** `dependsOn(CoolingLoop, SensorA)`
`dependsOn(CoolingLoop, ValveB)`

This remains under `RepresentationTransduction` when the notation stays tethered to the same relation line already visible in the diagram, the described entity remains preserved, and no stronger dependency theory is silently imported by the notational rendering.

#### A.6.3.RT:5.3 - Boundary to textual rewrite
A source prose note is shortened, reordered, or translated but remains essentially textual. That case stays with `ConservativeRetextualization`, not this pattern.

#### A.6.3.RT:5.4 - Boundary to explanation surfaces
A representation shift is performed mainly to teach or narrate rather than to publish another same-entity representation regime. That case should leave this pattern and be reviewed under explanation governance.

#### A.6.3.RT:5.4.a - Boundary to bridge-bearing comparison
**Source slice.** `Local reliability note: Pump P-2 remained within operating range during test window W-3.`

**Published comparative slice.** `Pump P-2 in W-3 behaves like Unit U-7 in Plant B and can therefore be treated as operationally equivalent for this comparison.`

This does **not** stay in `RepresentationTransduction`. The rendering has moved from a same-described-entity representation shift to comparative or bridge-bearing reading across contexts. Once the publication starts asserting cross-context equivalence, substitution, or comparative licence, the case must leave this pattern and move to explicit bridge-governed review.

#### A.6.3.RT:5.4.b - Boundary to carrier/export work
**Source rendering slice.** `| Service | Window | Spike count | Source pins |`

**Published export slice.** `latency-report.csv` and dashboard PNG generated from the same table.

This also stays outside `RepresentationTransduction`. The representation scheme was already chosen; what follows is carrier formatting, export, packaging, or rendering work on that representation. The didactic point is that not every change in visible form is a new same-described-entity representation transition.

#### A.6.3.RT:5.5 - Boundary to decode-mediated latent cases
A reviewer or decode path tries to restate a latent region or distributed feature cluster as explicit object/relation content. This stays outside the admissible same-described-entity path under `A.6.3.RT` unless an explicit decoding-access profile, `RecoverabilityEvidenceClass`, and an explicit decode route are already present. Readable decode output alone is not enough.

#### A.6.3.RT:5.5.a - Guarded decode-mediated readout
**Pinned source cluster.** `Probe run P-8 is tied to model-state log M-12 and evaluation bundle EV-4 for the same diagnostic case.`

**Published exploratory slice.** `A decode-mediated readout suggests a cluster that may correspond to the same failure episode already pinned in P-8 / M-12 / EV-4. This rendering stays exploratory and report-only until stronger recoverability evidence is published.`

This example remains guarded-open rather than green. The didactic point is that a decode-mediated rendering may still be useful, but it does not become a normal same-entity publication merely because the result looks readable.

### A.6.3.RT:6 - Bias-Annotation

Lenses tested: **Arch**, **Onto/Epist**, **Prag**, **Did**.
This pattern intentionally biases toward same-entity representation shifts and away from hidden retargeting, explanation inflation, or ontology-by-default through notation or geometry. The main mitigation is explicit recoverability discipline, preserve-vs-retarget escape rules, and directly reviewable entry cases before decode-mediated ones.

### A.6.3.RT:7 - Conformance Checklist

1. **CC-RT-1 — Same described entity remains explicit.**
   The case preserves `describedEntityRef` without special pleading.
2. **CC-RT-2 — Representation shift is the right family.**
   The result is genuinely a representation-scheme shift rather than mere textual rewrite or explanation work.
3. **CC-RT-3 — Factor, reasoning-medium, and mode deltas are explicit.**
   `representationFactorDelta`, `inferenceRegimeDelta`, and any load-bearing `semioticModeShift` are explicit.
4. **CC-RT-4 — Extended delta axes are explicit when load-bearing.**
   `salienceShift`, `topologyShift`, `actionabilityShift`, `calibrationShift`, and `interactivityShift` are named whenever they materially shape review or misuse risk.
5. **CC-RT-5 — Recoverability is explicit.**
   Recoverability is stated explicitly through `onticRecoverabilityClass` and `onticRecoverabilityMode`.
6. **CC-RT-6 — Decode-mediated cases carry stronger evidence.**
   If the case is decode-mediated or latent/distributed, `RecoverabilityEvidenceClass` and decode route are explicit.
7. **CC-RT-7 — Loss / provenance / pinning / reliability are explicit.**
   Losses, provenance, pinning, and reliability transport are explicit.
8. **CC-RT-8 — Preserve-vs-retarget reroute is explicit.**
   If the case fails any of the checks above, the reroute path is explicit (`ConservativeRetextualization`, `ExplanationFaithfulnessProfile`, `A.6.4`, or another owner).
9. **CC-RT-9 — Direct vs correspondence split is explicit.**
   The case states whether it is direct or correspondence-mediated; if correspondence-mediated, `CorrespondenceModelRef` is explicit.
10. **CC-RT-10 — Non-default face/surface admissibility is explicit.**
    Any `Interop`, `Assurance`, gate-bearing, or decode-bounded use states host-explicit admissibility and keeps same-entity support visible.
11. **CC-RT-11 — Decode-mediated same-entity entry tether is explicit.**
    A decode-mediated case states how the target rendering is tethered back to already pinned and provenance-bearing source material for the same described entity.
12. **CC-RT-12 — No hidden bridge or face-family inflation.**
    The case makes clear that representation work does not by itself grant bridge, substitution, or comparative-reading licence and does not create a new face family.
13. **CC-RT-13 — Reopen triggers are explicit when recoverability, admissibility, or primary mode changes.**
    If recoverability assumptions, pins, provenance, correspondence support, target-face admissibility, or the primary semiotic mode change, the case records the reopen trigger explicitly.

### A.6.3.RT:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | Why it is wrong | How to avoid it |
|---|---|---|
| Treating every format shift as harmless formatting | representation changes can alter reasoning affordances and recoverability | publish factor delta and reasoning-medium delta explicitly |
| Collapsing representation-scheme shift, semiotic-mode shift, and viewpoint shift into one vague change | reviewers cannot tell what actually changed or what burden is primary | name scheme, mode, and viewpoint separately and use the canonical boundary exemplars when only one of them changed |
| Letting notation become ontology-by-default | diagram or geometry starts pretending to define the world rather than represent it | keep ontic scaffold preservation and recoverability explicit |
| Hiding retargeting under representation language | a changed object-of-talk is mislabeled as same-entity representation work | exit to `A.6.4` whenever `DescribedEntityRef` changes |
| Starting with latent/distributed cases before recoverability is explicit | decode burden overwhelms same-entity review | keep decode-mediated cases out until decoding access and evidence class are explicit |

### A.6.3.RT:9 - Consequences

- Same-entity representation shifts get a lawful place without inventing a new heavy owner.
- Representation-factor and reasoning-medium changes become explicit rather than rhetorical.
- Recoverability and decode dependence become reviewable instead of hidden behind cleaner surfaces.
- The pattern remains safely bounded by `A.6.3`, `A.6.4`, explanation governance, and carrier work.

### A.6.3.RT:10 - Rationale

This pattern is worth splitting out because representation changes are already happening in practice and they are not well served by treating every such case as either mere rewriting or full retargeting. Keeping the family under `A.6.3` preserves owner safety while making representation-factor and recoverability burdens explicit.

### A.6.3.RT:11 - SoTA-Echoing

**SoTA note.** This section does not mint an independent second rule layer. It is a load-bearing alignment surface: the Solution, Conformance Checklist, boundary rules, and Relations of this pattern must match the stance stated here or explicitly justify any divergence.

**Claim 1.** Best-known current architecture-description and model-based practice treats views, representation schemes, and reasoning media as load-bearing rather than as decorative formatting.
**Practice / source / alignment / adoption.** ISO/IEC/IEEE 42010:2022 and current SysML v2 view practice treat viewpoint, view, model kind, and rendering discipline as explicit review objects rather than mere layout choices. This pattern **adopts** explicit representation-scheme review, **adapts** it to same-described-entity viewing under `A.6.3`, and **rejects** the shortcut where a clearer table, diagram, or notation is treated as if it had automatically earned stronger ontology or authority.

**Claim 2.** Best-known contemporary notation-and-reasoning practice treats tables, diagrams, and structured notations as reasoning media with different affordances, not as neutral surface restyling.
**Practice / source / alignment / adoption.** Post-2015 model-based and notation-sensitive review practice treats representational form as something that changes what readers can inspect, compare, or replay. This pattern **adopts** reasoning-medium review, **adapts** it through explicit factor and medium deltas, and **rejects** hidden dependency-theory uplift or silent semantic strengthening by prose-to-diagram or diagram-to-notation moves.

**Claim 3.** Best-known representation-aware AI practice treats latent geometry and decode-mediated structure as evidence-bounded interpretation rather than ontology-by-default.
**Practice / source / alignment / adoption.** Byte Latent Transformer (2024) and Large Concept Model (2024) both reinforce that representation regime matters, but neither licenses silent promotion from geometry, cluster structure, or decoder output to canonical object/relation ontology. This pattern **adopts** representation-aware review, **adapts** it through `RecoverabilityEvidenceClass`, decode-route explicitness, and same-entity source tethering, and **rejects** the popular shortcut where readable decode output is treated as if it were direct givenness.

**Local stance.** The load-bearing SoTA claim for this pattern is narrow: representation regime and reasoning medium are lawful review targets, but geometry, notation, or a decode-mediated result do not become ontology-by-default.

### A.6.3.RT:12 - Relations

- **Builds on:** `A.6.3`, `A.6.2`, `A.7`, `E.10.D2`, `C.2.7`, `E.17.0`, `E.17`, `F.9`, `F.18`
- **Coordinates with:** `ConservativeRetextualization`, `ExplanationFaithfulnessProfile`, `E.17.ID.CR ComparativeReading`, `A.6.4`, `A.15`, `A.20`, `A.21`, explicit decoding-access review
- **Impact radius:** primary touch `A.6.3`; secondary review surfaces `C.2.7`, `E.17.0`, `E.17`, `F.9`, decode-mediated recoverability review; failed same-entity or recoverability conditions exit to `A.6.4`, explanation governance, or later world/gate owners
- **Boundary notes:** textual same-regime rewrites stay with `ConservativeRetextualization`; explanation-facing renderings stay with `ExplanationFaithfulnessProfile`; bounded comparative review surfaces exit to `E.17.ID.CR ComparativeReading`; described-entity changes exit to `A.6.4`; decode-mediated world/gate consequences remain bounded by explicit evidence and downstream handoff.

### A.6.3.RT:End










