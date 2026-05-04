## A.6.Q - `U.QualityTermPrecisionRestoration` — Quality Term Precision Restoration (Q-TERM)

> **Type:** Architectural (A)
> **Status:** Draft
> **Normativity:** Normative (Core / Draft)

**Plain-name.** Quality-term precision restoration.

**Intent.**
Provide a reusable discipline for repairing overloaded uses of the word **quality** in FPF texts.
This pattern is an **A.6.P RPR specialisation**: it routes bare evaluative prose either into an explicit endpoint-owned evaluative form or, when endpoint selection is still being stabilized, into one explicit, slot-explicit **quality ascription** transitional relation family with a declared **sense family**, lawful **normal form** (`SignalPack | Characteristic | Bundle | Objective`), explicit **change semantics**, explicit **reference-plane accountability**, and lexical guardrails.
It allows philosophical, neuro-symbolic, control-theoretic, engineering, and open-ended-search uses to coexist **without false identity by label**.

**Placement.**
Part A > cluster **A.6 Signature Stack & Boundary Discipline** > specialisation of **A.6.P** for overloaded evaluative umbrella terms centered on *quality*.

**Builds on.**
A.6, A.6.B, A.6.P, A.6.S, A.6.0, A.6.5, A.7, A.2.6, A.17, A.18, C.2.1, C.16, C.25, C.17–C.19, E.8, E.10, F.9, F.18.

**Coordinates with.**
**A.6.A** for affordance / action-invitation exits; **C.2.2a / A.16 / A.16.1 / A.16.2 / B.4.1** for language-state chart positions, lawful moves, early cue routing, responsibility handoff, and lawful retreat when an evaluative publication must be reopened; use **A.16.0** only when lineage, branch, loss, or handoff history itself must be published as an explicit trajectory account; **B.5.2.0** when the strongest lawful continuation is still an open explanatory probe rather than a stable endpoint ascription; **C.2.LS / C.2.4 / C.2.5 / C.2.6 / C.2.7** for articulation, closure, anchoring, and representation-factor facets referenced but not owned here; **E.17.0/E.17/E.18** for viewpoint publication; **A.10/B.3** for evidence and assurance; **A.19/CN** for comparability governance; **F.9.1** for bridge-stance annotations; **C.3.3** for explicit kind-bridge repair when endpoint kind mismatches appear.

**Non-goal.**
This pattern does **not** assert that phenomenal character / qualia, phenomenological preconceptual fit, Pirsig-style dynamic/static quality, latent fit in learned representations, explanatory merit, engineering `-ilities`, QD/NQD selector value, and control adequacy are one concept.
Its job is to publish a disciplined **bridge reading** across those traditions while preventing false identity by shared label.
It also does **not** assert that every trigger use of “quality” is lawfully repaired by `evaluativeAscription(...)`: where the repaired statement is primarily about an **action invitation / affordance** rather than an evaluative ascription, or is primarily about a **requirement / commitment over explicit heads** (for example, *quality requirements* over named Characteristics, Q-Bundle heads, or objective heads), the lawful move may be `changeRelationKind(...)` into a different relation family.

### A.6.Q:1 - Problem frame

FPF repeatedly encounters a predictable precision failure mode around the token **quality**:

authors say:

* “this design has quality”
* “the model quality improved”
* “quality matters before formalisation”
* “quality characteristics”
* “quality in QD / NQD”
* “the world model is higher quality”
* “the explanation is high-quality”

…but the intended meaning is actually one of several different **evaluative families**, for example:

1. **Phenomenal character / qualia** when the experienced quality itself is the topic of description rather than an externally measured characteristic.
2. **Preconceptual fit / felt rightness** before stable object-characterisation.
3. **Latent / distributed fit signals** in learned representations, world models, or active inference loops.
4. **Explanatory merit** of a theory, problem frame, or conjecture.
5. **Architectural-description fitness / compression merit** of an architecture description or architecture model under a declared viewpoint.
6. **Engineering quality families** such as reliability, maintainability, security, evolvability.
7. **Usefulness / selection value** in open-ended search, novelty–quality–diversity, or portfolio selection.
8. **Control adequacy** of a policy/model/controller in a closed loop.

The failure modes are recurrent:

* **Sense elision.** One umbrella noun hides several non-equivalent evaluative kinds.
* **Carrier confusion.** The bearer of the evaluation is unclear: artifact, episode, model, policy, explanation, candidate, architecture, relation, or action loop.
* **Form confusion.** A non-metric signal is rewritten as a metric; a bundle is treated as one scalar; an objective is mistaken for a characteristic.
* **Substrate confusion.** Embodied/preconceptual, latent/distributed, and symbolic/local representations are silently collapsed.
* **Plane confusion.** Quality of the described entity, quality of the description, quality of the carrier, and quality of the publication face are silently collapsed across `ReferencePlane` / A.7 lanes.
* **Bridge illusion.** Similar wording across traditions is mistaken for sameness.
* **Illegal scalarisation.** Composite engineering families or explanatory merit are compressed into one number without a lawful scoring method.
* **Viewpoint conflict.** One stakeholder means architectural attributes, another means usefulness, another means preconceptual fit.

### A.6.Q:2 - Problem

How can FPF let authors use the communicative convenience of the word **quality** while preventing category errors when the term crosses:

* phenomenological / epistemological discourse,
* architecture-description / viewpoint-fit discourse,
* representation-learning / neuro-symbolic discourse,
* Popper/Deutsch-style explanation-and-criticism discourse,
* engineering architecture and quality-characteristic discourse,
* open-ended evolution / NQD / selection discourse,
* control / world-model / active-inference discourse,
* ecological / affordance discourse, including cases that must exit this relation family altogether?

### A.6.Q:3 - Forces

* **Breadth vs precision.** “Quality” is attractive because it is broad; that same breadth makes it unsafe at boundaries.
* **Preconceptuality vs auditability.** Some uses refer to something real but not yet stably characterised.
* **Distributed substrate vs local publication.** Some evaluative signals arise in distributed or embodied substrates but must later be published in explicit local forms.
* **Comparability vs non-reduction.** Engineering and selection settings need comparability, but not every evaluative signal is a lawful metric.
* **Cross-tradition dialogue vs false unification.** The framework should support parallels without asserting identity.
* **Progressive articulation.** A term may begin as a felt signal and later become a bundle, proxy set, or objective.

### A.6.Q:4 - Solution

**Stable lens > Sense Family > Slots > Normal Form > Change Lexicon > Guardrails**

#### A.6.Q:4.0 - Trigger rule

A use of **quality** is in scope for A.6.Q when any of the following holds:

* the token **quality** or **high-quality / low-quality** appears in Tech or normative prose;
* a boundary statement relies on “quality” for admission, selection, explanation, comparison, assurance, or requirement-setting;
* different traditions are compared using the same word *quality*;
* a draft introduces *quality metric*, *quality score*, *quality characteristic*, *quality requirement*, *model quality*, *architecture quality*, *solution quality*, or *quality in QD* without a declared sense;
* the author intends the word to carry more than one of: evaluative fit, measurable characteristic, bundle, utility, or optimization objective.

#### A.6.Q:4.0a - Operational repair sequence

When the trigger fires, authors SHOULD follow the A.6.P operational repair path:

1. **Capture the trigger span.**
   Copy the exact surface phrase using *quality* (or a red-flag derivative such as *high-quality*, *quality metric*, *quality characteristic*, *model quality*).

2. **Reconstruct the candidate set.**
   Enumerate plausible candidate senses and, when relevant, candidate endpoint owners plus bearer lanes/facets (A.7: `Object | Description | Carrier`).
   If the occurrence is decision-bearing or publication-bearing, record this as a short **Candidate-Set Note** before selecting a repair.

   **Collision note.**
   This **Candidate-Set Note** is a local RPR disambiguation artifact for `quality` repairs; it is **not** the F.18 naming-process candidate set.

2a. **Check for an out-of-family affordance reading.**
   If the occurrence is primarily about an **action invitation / affordance** rather than an evaluative ascription, do **not** force a `QualitySense`.
   Route it by `changeRelationKind(...)` into the appropriate relation family and treat the quality token as token-under-discussion only.

3. **Select one explicit quality sense.**
   Pick one `QualitySense` token and state why rival senses were rejected in this local context.

4. **Emit an endpoint-explicit or transitional rewrite.**
   Rewrite the sentence either into one explicit endpoint-owned evaluative form (`Characteristic | Q-Bundle | Objective | ExplanatoryMeritBundle | selector-value endpoint`) or, when endpoint choice is still being stabilized, into one explicit `evaluativeAscription(...)` transitional record with bearer, frame, evaluator/viewpoint, normal form, and explicit qualifiers.
5. **Route boundary-bearing consequences.**
   If the repaired statement is used for admissibility, commitments, publication, or evidence-bearing decisions, route the resulting `L/A/D/E` hooks through A.6.B instead of letting “quality” carry that burden by itself.

#### A.6.Q:4.1 - Transitional lens: evaluative routing anchored by `evaluativeAscription(...)`

A.6.Q stabilises the ambiguity cluster by treating every in-scope quality statement as **explicit evaluative material that must route to a named endpoint owner**, not as a bare adjective.
`evaluativeAscription(...)` remains the canonical **transitional/metalinguistic repair record** when the endpoint choice is not yet fixed, but it is not the universal resting place.
Entry into A.6.Q therefore presupposes enough local `AE` to name the bearer, the frame, and at least one candidate evaluative family explicitly. `CD` may remain low while `evaluativeAscription(...)` is still serving as a transitional record, but if the material is still only a cue pack, a routed cue, or an open explanatory probe, it SHOULD remain in `A.16.1` / `B.4.1` / `B.5.2.0` rather than being published here prematurely. If a previously published evaluative record later loses the support needed to keep even that transitional status live, retreat via `A.16.2`.
In A.6.P terms, this pattern fixes one routing discipline plus one canonical transitional relation family:

* **`evaluativeAscription`** — the explicit transitional relation kind for “X has quality / quality improved / high-quality / quality in QD / quality characteristic / model quality” rewrites while routing toward a more specific endpoint owner.
#### A.6.Q:4.1a - RelationKind contract skeleton for `evaluativeAscription`

The family-specific `RelationKind` token is **`evaluativeAscription`**.
Its contract publication SHALL declare, at minimum:

* **(L)** applicability of the token in the local Context/plane set;
* **(L)** bearer-centred polarity (the bearer is the evaluated participant; inverse prose SHALL NOT silently swap bearer and evaluator);
* **(L)** participant SlotSpecs for bearer, sense, evaluation-frame, evaluator, and normal-form positions;
* **(A)** repair paths for bearer-kind mismatches: explicit narrowing, `KindBridge`, and/or explicit `retargetBearer(...)`;
* **(L)** qualifier expectations for `scope`, `Γ_time`, `viewpoint`, `view`, `referencePlane`, `refScheme`, `reprScheme`, `representationSubstrate`, and `bridgeRef`;
* **(D)** qualifier-placement discipline: frame/scope/time MUST NOT be smuggled into adjectives such as *high-quality*;
* **(A/E)** witness discipline for decision/publication lanes;
* **(L/A)** admissible semantic change classes and their edition-fence expectations;
* **(A/E)** cross-context / cross-plane policy when actual reuse is claimed (Bridge id + CL/loss-note policy).

Each in-scope occurrence SHALL be representable as a pattern-specific **QualifiedRelationRecord**:

```text
evaluativeAscriptionRecord :=
⟨
  relationKind            : evaluativeAscription,
  bearerTuple             : …,
  qualitySense            : QualitySense,
  evaluationFrame         : …,
  evaluator?              : …,
  viewpoint?              : U.Viewpoint,
  view?                   : U.View,
  referencePlane?         : ReferencePlane,
  refScheme?              : U.ReferenceScheme,
  reprScheme?             : U.RepresentationScheme,
  normalForm              : SignalPack | Characteristic | Bundle | Objective,
  scope?                  : U.Scope,
  Γ_time?                 : U.GammaTimePolicy,
  representationSubstrate?: embodied-kinesthetic | latent-distributed | symbolic-local | hybrid,
  bridgeRef?              : BridgeId,
  witnesses?              : EvidenceRefSet
⟩
```

So the sentence “X has quality” is never accepted as a terminal form.
It must be rewritten either into an explicit endpoint-owned evaluative form or into an explicit `evaluativeAscription(...)` transitional record with declared routing to that endpoint.

**Discipline note.**
`QualitySense` is a **slot value inside** the transitional relation family; it is not a replacement for endpoint ownership.
The stable intermediate lens is the ascription relation; the sense token refines **what kind of evaluative ascription** is being made while the endpoint target remains explicit.

**Separation note.**
`evaluator` and `viewpoint` are not synonyms.
When both matter, they SHALL be published separately: the evaluator is the observing / criticising / selecting party or policy, while the viewpoint is the declared `U.Viewpoint` under which the ascription is presented.
#### A.6.Q:4.1b - Polarity discipline (bearer-centred; no silent inverse)

`evaluativeAscription` is bearer-centred.
Tech / normative prose SHALL keep the evaluated participant in the bearer position and SHALL publish evaluator/viewpoint separately.

* “Architects rate the system highly” rewrites to `evaluativeAscription(bearer=System, evaluator=ArchitectureReviewBoard, …)`.
* “The benchmark says model quality is high” rewrites to `evaluativeAscription(bearer=Model, evaluator=BenchmarkPolicy, …)`.

There is no inverse token that silently makes the evaluator the bearer.
If inverse wording is used in Plain prose, authors SHALL rewrite it into the bearer-centred form (or mint an explicit inverse RelationKind token and publish its polarity contract).

#### A.6.Q:4.1c - Endpoint-first discipline

When the lawful endpoint owner is already known, authors SHOULD publish the endpoint-owned evaluative form directly and use `evaluativeAscription(...)` only when preserving the transitional ambiguity is itself informative. `evaluativeAscription(...)` is therefore a routing record, not a shadow endpoint owner.

Typical direct endpoints are:

* engineering `-ility` heads published as one `Characteristic` or one `Q-Bundle`,
* selector-context uses published as an `Objective` headed by `QS.UseValue` unless overridden explicitly,
* architecture-description uses published under the description-side evaluative head already selected by the viewpoint bundle,
* explanatory-merit uses published under the explicit merit bundle when that bundle head is already known.

#### A.6.Q:4.2 - Core construct: `QualitySense`

Every in-scope use SHALL resolve to an explicit **`QualitySense` token**.

A `QualitySense` token publishes at least:

```text
QualitySense :=
  ⟨
    senseId,
    bearerArity,
    articulationMode,
    representationSubstrate,
    defaultNormalForm,
    admissibleNormalForms,
    evaluationFrameKind,
    admissibleEvidenceModes,
    admissibleChangeClasses,
    bridgePolicy
  ⟩
```

Where:

* **`articulationMode`** ∈
  `{ preconceptual, exemplar-grounded, proxy-grounded, characteristic-bound, bundle-bound, objective-bound }`
* **`representationSubstrate`** ∈
  `{ embodied-kinesthetic, latent-distributed, symbolic-local, hybrid }`
* **`defaultNormalForm`** ∈
  `{ SignalPack, Characteristic, Bundle, Objective }`
* **`admissibleNormalForms`** is the explicitly declared set of lawful publication forms for the sense.
  `defaultNormalForm` names the primary publication form; any additional forms MUST be declared here rather than inferred ad hoc.

#### A.6.Q:4.3 - Normative starter set of sense families

A Context MAY add local senses, but the following starter set is normative as the initial disambiguation menu:

| `QualitySense` token               | Use when “quality” means…                                                                                      | Default normal form | Typical substrate                | Must **not** be silently collapsed into                                    |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------: | -------------------------------- | -------------------------------------------------------------------------- |
| `QS.PreconceptualFit`              | preconceptual fit, felt rightness, “quality before definition”, kinesthetic/embodied salience                |         `SignalPack` | `embodied-kinesthetic` or `hybrid` | Characteristic, utility, fitness score                                     |
| `QS.PhenomenalCharacter`           | phenomenal character / qualia / felt characteristic when the experienced quality itself is described          |         `SignalPack` | `embodied-kinesthetic` or `hybrid` | `QS.PreconceptualFit`, engineering quality, utility                        |
| `QS.LatentFit`                     | distributed fit/tension in learned representations, world models, probes, prediction structures              |         `SignalPack` | `latent-distributed` or `hybrid` | `QS.PreconceptualFit`, engineering quality, explanatory merit              |
| `QS.ExplanatoryMerit`              | epistemic merit of an explanation, conjecture, problem frame, or theory                                      |             `Bundle` | `symbolic-local` or `hybrid`     | engineering `-ilities`, use-value                                          |
| `QS.ArchitecturalDescriptionFitness` | task-fit / compression merit of an architecture description, architecture model, or viewpoint bundle as a description of structure for downstream reasoning |             `Bundle` | `symbolic-local` or `hybrid`     | `QS.EngineeringQualityFamily`, `QS.ExplanatoryMerit`, publication polish   |
| `QS.EngineeringQualityFamily`      | reliability/availability/security/maintainability/evolvability/usability/etc.                                |             `Bundle` | `symbolic-local` or `hybrid`     | function/capability statements, preconceptual fit                          |
| `QS.UseValue`                      | usefulness of a candidate under a declared goal/CG-frame; the “Q” head in NQD/QD by default                  |          `Objective` | `symbolic-local` or `hybrid`     | engineering quality family, explanatory merit                              |
| `QS.ControlAdequacy`               | adequacy of a policy/model/controller in a closed action loop                                                |             `Bundle` | `hybrid`                         | bare model “quality”, felt fit                                             |

**Default-form note.**
`QS.EngineeringQualityFamily` and `QS.ControlAdequacy` default to `Bundle`.
A local Context MAY operationalize one explicit head as a `Characteristic`, but that is a declared operationalization, not a second default normal form.

**Normative rewrite note.**

* In **NQD / QD / selector** contexts, bare *quality* SHALL rewrite to **`QS.UseValue`** unless a different `QualitySense` is explicitly declared.
* In **engineering** contexts, bare *quality* SHALL rewrite either to:

  * one explicit **`U.Characteristic` + CSLC Scale**, or
  * one explicit **`Bundle`**, preferably authored as a **`Q-Bundle`** when composite.
* In **phenomenological** contexts, bare *quality* SHALL rewrite to **`QS.PhenomenalCharacter`** when the experienced quality itself is the topic of description, and to **`QS.PreconceptualFit`** when the talk is about preconceptual fit / felt rightness before stable characterisation.
* In **representation-learning / world-model** contexts, bare *model quality* SHALL rewrite to **`QS.LatentFit`** and/or **`QS.ControlAdequacy`**, with the distinction made explicit.
* In **epistemic evaluation** contexts, “good explanation” SHALL rewrite to **`QS.ExplanatoryMerit`**.
* In **architecture-description / viewpoint** contexts, bare *architecture quality* / *architectural quality* SHALL first disambiguate the bearer lane: if the bearer is the described system, route to **`QS.EngineeringQualityFamily`**; if the bearer is the description/episteme, route to **`QS.ArchitecturalDescriptionFitness`**.

#### A.6.Q:4.4 - Required slots for a conforming `evaluativeAscription`

A conforming `evaluativeAscription` SHALL make explicit:

1. **Bearer tuple.**
   What is being evaluated, with arity explicit.

2. **`QualitySense`.**
   Which evaluative family is intended.

3. **Evaluation frame.**
   The criterion-basis under which the ascription is made.
   Examples: exemplar pack, probe pack, criticism/test pack, Q-bundle definition, CG-frame, acceptance spec, control horizon.

4. **Evaluator or viewpoint.**
   State the evaluator (observer, critic, selector policy, stakeholder family, or review body) and, when relevant, the `U.Viewpoint`, separately.
   The two SHALL NOT be silently collapsed when they differ.

5. **Normal form.**
   Whether the ascription is published as `SignalPack`, `Characteristic`, `Bundle`, or `Objective`.

6. **Scope and time when relevant.**
   The relevant USM scope (`U.ClaimScope`, `U.WorkScope`, `U.PublicationScope`, or generic `U.Scope`) and `Γ_time` SHALL be explicit when omission changes meaning.
   Freshness windows, qualification windows, or evidence decay windows SHALL be declared in the appropriate evidence or capability lane rather than smuggled into “quality” as an adjective.

7. **Reference plane when relevant.**
   Especially when the same surface phrase can refer to the described entity, its description, its carrier, or a publication face under a different `ReferencePlane`.

8. **Reference / representation scheme when relevant.**
   Especially when the ascription depends on a declared reference scheme, representation scheme, or viewpoint-specific decoding convention.

9. **Representation substrate when relevant.**
   Especially when discussing parallels between preconceptual, latent-distributed, and symbolic-local treatments.

10. **Witness / evidence mode.**
   Exemplars, probes, measurements, bundle members, tests, traces, or closed-loop performance carriers.

#### A.6.Q:4.5 - Normal-form discipline

A `QualitySense` SHALL declare one lawful **default** normal form and MAY declare additional admissible normal forms explicitly.

**QNF-1 — `SignalPack`.**
Use for `QS.PhenomenalCharacter`, `QS.PreconceptualFit`, and many cases of `QS.LatentFit`.

A conforming `SignalPack` publishes:

* exemplar/contrast set or probe set,
* articulation notes,
* source episode / carrier / observer,
* optional ordinal or thresholded summaries,
* explicit warning that the signal is **not** yet a `Characteristic` unless a lawful proxy is later declared.

**QNF-2 — `Characteristic`.**
Use only when the sense is truly one measurable characteristic on one declared scale.
This routes through **A.17/A.18/C.16** and inherits full scale legality.

**QNF-3 — `Bundle`.**
Use when the sense is composite.
Typical for `QS.ExplanatoryMerit`, many engineering quality families, and `QS.ControlAdequacy`.

A conforming bundle publishes:

* member heads,
* whether each head is Characteristic / status / mechanism / scope / test,
* aggregation policy if any,
* prohibition on hidden scalarisation.

**Engineering note.**
For engineering `-ility` families, the preferred bundle form is **`Q-Bundle`** (C.25), because it keeps **Measures[CHR]** distinct from **ClaimScope/WorkScope** and from **Mechanisms/Status**.
`Q-Bundle` is a **C.25 authoring profile of `Bundle`**, not a fifth normal form beside `SignalPack | Characteristic | Bundle | Objective`.
Do not publish a free-floating bundle with hidden metric semantics.

**QNF-4 — `Objective`.**
Use for `QS.UseValue` in selection/generation/search contexts.

A conforming objective publishes:

* CG-frame / objective owner,
* admissible comparators,
* acceptance / selector policy,
* reference plane and window,
* relation to novelty/diversity/constraints.

#### A.6.Q:4.6 - Functional vs quality-family discipline

A.6.Q SHALL prevent the collapse of **function/capability** claims into **quality-family** claims.

* A statement about **what a system does** belongs to functional/procedural description.
* A statement about **how well / how safely / how robustly / how maintainably** it does so belongs to `QS.EngineeringQualityFamily`.
* “Quality characteristic” and “functional characteristic” SHALL NOT be used as interchangeable labels.
* In engineering contexts, `-ility` names are **quality-family labels**, not automatically Characteristics.
  They become lawful only as one explicit `U.Characteristic` or one explicit `Bundle` (preferably authored as `Q-Bundle` when composite).
* Cross-references are allowed; category collapse is not.

#### A.6.Q:4.7 - Bridge discipline across traditions

Whenever two different traditions are compared using the word *quality*, the author SHALL publish an explicit **bridge stance** and loss note.

Allowed bridge stances:

* **`localRename`** — near-synonymous within one Context.
* **`operationalizes`** — one sense is turned into a proxy or measurable form.
* **`partialAnalogy`** — structurally similar but not identical.
* **`projection`** — one richer sense is projected into a narrower evaluative frame.
* **`nonEquivalent`** — same word, no lawful bridge asserted.

Examples:

* `QS.PreconceptualFit` - `QS.LatentFit` is usually `partialAnalogy`, not identity.
* `QS.PreconceptualFit` - `QS.PhenomenalCharacter` is usually a progression-by-articulation relation, not identity.
* `QS.PreconceptualFit` > engineering measures is usually `operationalizes` or `projection`, with loss notes.
* `QS.EngineeringQualityFamily` > `QS.UseValue` is usually `projection` under a CG-frame.
* `QS.ExplanatoryMerit` - `QS.UseValue` is **not** identity unless a Context explicitly defines such a projection.
* Pirsig-style **dynamic quality** usually routes to `QS.PreconceptualFit` (sometimes `QS.LatentFit`) only as `localRename` / `partialAnalogy` under a declared Context; it is not identity by label.
* Pirsig-style **static quality** usually routes to `Characteristic` / `Bundle` publication under some other declared sense; it is not identity with dynamic quality.
* `QS.ArchitecturalDescriptionFitness` - `QS.EngineeringQualityFamily` is usually `projection` or `nonEquivalent` unless the Context explicitly states which heads of description-fitness are intended to proxy which system-side characteristics.

#### A.6.Q:4.8 - Change lexicon

A conforming pattern SHALL narrate changes with a stable change lexicon aligned to A.6.P:

* **`declareevaluativeAscription(...)`** — create a new explicit quality ascription record.
* **`withdrawevaluativeAscription(...)`** — retire a prior record.
* **`retargetBearer(...)`** — change the evaluated bearer tuple while keeping the same relation family.
* **`reviseSense(...)`** — change the value in the `qualitySense` slot.
* **`reArticulate(...)`** — change `articulationMode` while preserving sense family.
* **`reProxy(...)`** — change proxy/probe/operationalisation details.
* **`reBundle(...)`** — change bundle members or aggregation policy.
* **`reScale(...)`** — change characteristic scale or scale type.
* **`reFrame(...)`** — change evaluation frame.
* **`reView(...)`** — change evaluator/viewpoint.
* **`rescope(...)`** — change `U.Scope`.
* **`retime(...)`** — change `Γ_time`.
* **`refreshWitnesses(...)`** — refresh evidence or witness bindings.
* **`changeRelationKind(...)`** — semantic move to a different relation family; never edit in place silently.

A silent **sense rewrite** is a breaking semantic change.
If the ascription ceases to mean “quality ascription” at all, use `changeRelationKind(...)` rather than pretending the same record survived unchanged.

**A.6.P rewrite note.**
`retargetBearer(...)` is the family-specific form of `retargetParticipant(BearerSlot, …)`.
`reviseSense(...)`, `reArticulate(...)`, `reProxy(...)`, `reBundle(...)`, `reScale(...)`, `reFrame(...)`, and `reView(...)` are family-specific refinements of `reviseByValue(...)` and SHALL preserve the A.6.5 distinction between ref retargeting and by-value edits.

#### A.6.Q:4.8a - A.6.B routing template for `evaluativeAscription`

When a repaired quality statement becomes boundary-bearing, route it explicitly:

* **L** — `evaluativeAscription` contract skeleton, `QualitySense` semantics, normal-form lawfulness, and declared bridge stances;
* **A** — admissibility conditions for using the ascription in selector / gating / publication lanes (required qualifiers, witnesses, thresholds, qualification windows);
* **D** — author / publisher obligations (lexical firewall, mandatory rewrites, publication duties);
* **E** — carrier-anchored evidence/work effects (measurements, traces, critique sheets, probe packs, selector logs).

Where this family is published as a reusable boundary surface, authors SHOULD materialize stable `L-Q*` / `A-Q*` / `D-Q*` / `E-Q*` claim ids (or explicitly cite the reused routed claim set by location) and SHALL avoid paraphrase drift across quadrants.
Do not let the bare word *quality* carry L/A/D/E force by itself.

#### A.6.Q:4.9 - Lexical guardrails

In **Tech / normative prose**:

* bare **quality** MUST NOT appear without immediate resolution to a `QualitySense`;
* **high-quality / low-quality / quality metric / quality score / quality requirement / model quality / architecture quality / solution quality** are red-flag tokens;
* **quality characteristic** MAY appear only as:

  * a bridge label to an external standard/tradition, or
  * a family label immediately rewritten into one explicit `U.Characteristic` or `Q-Bundle`;
* **quality requirement / quality requirements** MUST NOT remain bare noun phrases; authors SHALL rewrite them into explicit `RequirementRole` / `U.Commitment` / `U.PromiseContent.acceptanceSpec` structures over one named `U.Characteristic`, one `Q-Bundle` head, or one explicit objective head;
* **architecture quality / architectural quality** MUST NOT appear without an explicit bearer lane (`Object | Description | Carrier`) and, when omission changes meaning, an explicit `referencePlane`;
* in QD/NQD contexts, bare **quality** MUST default to **`QS.UseValue`**;
* preconceptual uses MUST NOT be presented as if they were already Characteristics;
* latent/distributed fit MUST NOT be presented as if it were automatically explanatory merit;
* if the occurrence is primarily **affordance / action-invitation** talk, authors MUST NOT force a `QualitySense`; they SHALL exit to the appropriate relation family;
* scope words (*applicability*, *envelope*, *generality*, *validity*) MUST NOT be used as hidden substitutes for `U.Scope`, `U.ClaimScope (G)`, or `U.WorkScope`;
* quoted metalinguistic uses of the token *quality* are allowed, but SHALL be marked as **token-under-discussion**, not as a contract-bearing term.

#### A.6.Q:4.10 - Progressive elaboration

A.6.Q supports monotone elaboration:

1. Start by selecting a **`QualitySense`** and capturing rival candidates when ambiguity is live.
2. Declare bearer, frame, viewpoint, and substrate.
3. Choose a lawful **normal form**.
4. Add exemplars / probes / characteristic heads / bundle members / objective pins.
5. Add bridges and loss notes if comparing traditions.
6. If the repaired sentence is boundary-bearing, emit `L/A/D/E` routing hooks rather than letting “quality” carry them implicitly.
7. Never move between sense families silently.

### A.6.Q:5 - Archetypal Grounding

#### A.6.Q:5.1 - Tell

If a draft says *quality*, the author has not yet named the evaluative family.
A conforming rewrite publishes either one explicit endpoint-owned evaluative form or one explicit `evaluativeAscription(...)` transitional record with one `QualitySense`, one bearer tuple, one evaluation frame, one evaluator/viewpoint, one lawful normal form, explicit scope/time/bridge qualifiers when they matter, and declared routing toward the target endpoint owner.
#### A.6.Q:5.2 - Show (System lane)

**Draft:** “The model quality improved.”

**Repair A — latent representation line**
`evaluativeAscription(
  bearer = Model_v5,
  qualitySense = QS.LatentFit,
  evaluationFrame = ProbePack_PP2,
  evaluator = RepLearningReviewBoard,
  normalForm = SignalPack,
  Γ_time = Window_W5,
  witnesses = {ProbeSeparationRun_22, AliasRiskCard_9}
)`

**Repair B — closed-loop control line**
`evaluativeAscription(
  bearer = PolicyModelPair_PM5,
  qualitySense = QS.ControlAdequacy,
  evaluationFrame = Horizon_H × EnvClass_E,
  evaluator = ControlReviewBoard,
  viewpoint = ControlView_VP,
  normalForm = Bundle,
  scope = U.WorkScope(ControlDeploymentScope_7),
  Γ_time = RunWindow_RW,
  witnesses = {ClosedLoopTraceSet_41}
)`

#### A.6.Q:5.3 - Show (Episteme lane)

**Draft:** “Quality matters before definition.”

**Repair A — preconceptual / phenomenological line**
`evaluativeAscription(
  bearer = ProblemFramingEpisode_PF3,
  qualitySense = QS.PreconceptualFit,
  evaluationFrame = ExemplarPack_EP3,
  evaluator = ReviewerGroup_A,
  normalForm = SignalPack,
  representationSubstrate = embodied-kinesthetic,
  witnesses = {EpisodeNotes_3}
)`

**Repair B — explanatory line**
`evaluativeAscription(
  bearer = Explanation_N5,
  qualitySense = QS.ExplanatoryMerit,
  evaluationFrame = CriticismBundle_CB4,
  evaluator = TheoryReviewPanel,
  referencePlane = epistemic,
  normalForm = Bundle,
  witnesses = {CritiqueSheet_14, CounterexampleSet_2}
)`

#### A.6.Q:5.3a - Show (Architecture description lane)

**Draft:** “The architecture quality improved.”

**Repair A — quality of the described system**
`evaluativeAscription(
  bearer = PaymentPlatform_v4,
  qualitySense = QS.EngineeringQualityFamily,
  evaluationFrame = Q_Bundle_AvailabilitySecurityEvolvability_3,
  evaluator = ArchitectureReviewBoard,
  viewpoint = TEVB_ArchitectureViewpointSet,
  referencePlane = world/external,
  normalForm = Bundle,
  witnesses = {AvailabilityReport_8, CouplingCheck_3, EvolvabilityNote_2}
)`

**Repair B — quality of the architecture description**
`evaluativeAscription(
  bearer = ArchitectureDescription_AD12,
  qualitySense = QS.ArchitecturalDescriptionFitness,
  evaluationFrame = ViewpointBundle_TEVB × DecisionQuestionSet_DQ7,
  evaluator = ArchitectureReviewBoard,
  viewpoint = TEVB_ArchitectureViewpointSet,
  referencePlane = epistemic,
  normalForm = Bundle,
  witnesses = {CoverageMatrix_4, CorrespondenceCheck_7, ViewConsistencyNote_2}
)`

#### A.6.Q:5.4 - Show (QD / selector lane)

**Draft:** “Quality in our QD loop.”

**Repair**
`evaluativeAscription(
  bearer = Candidate_7,
  qualitySense = QS.UseValue,
  evaluationFrame = CG_Frame_9,
  evaluator = SelectorPolicy_P4,
  normalForm = Objective,
  Γ_time = SelectionWindow_SW,
  witnesses = {ObjectiveCard_9, AcceptanceSpec_4}
)`

### A.6.Q:6 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Universal** for overloaded evaluative uses of *quality* in FPF prose.

* **Gov bias:** this pattern favors explicit evaluative publication and explicit routing hooks, which improves auditability but adds authoring overhead.
* **Arch bias:** this pattern prefers one stable ascription relation over free-form philosophical prose, which improves reuse but can feel rigid in exploratory notes.
* **Onto/Epist bias:** this pattern refuses to collapse preconceptual, latent, explanatory, engineering, and selector senses into one concept; that increases honesty at the cost of extra lexical work.
* **Prag bias:** this pattern defaults QD/NQD uses toward `UseValue`, which improves selector clarity but can feel narrower than colloquial “quality”.
* **Did bias:** this pattern is intentionally teachable through repeated rewrites; the risk is over-formalizing early exploratory language.

### A.6.Q:7 - Conformance Checklist (CC-A.6.Q)

A text or pattern conforms to A.6.Q iff:

1. **CC-A.6.Q-1 - Explicit endpoint routing and explicit sense.**
   Every in-scope use of *quality* resolves either to one declared endpoint-owned evaluative form or to one declared `evaluativeAscription(...)` transitional record with one declared `QualitySense` and explicit endpoint routing.
2. **CC-A.6.Q-2 - Explicit bearer and arity.**
   The evaluated bearer tuple is explicit.

3. **CC-A.6.Q-3 - Explicit frame.**
   Evaluation frame is explicit and reviewable.

4. **CC-A.6.Q-4 - Evaluator/viewpoint is explicit.**
   The ascription states who evaluates, from which viewpoint, or under which selector/observer policy.

5. **CC-A.6.Q-5 - Substrate and referencePlane are declared when relevant.**
   Cross-talk between preconceptual, latent-distributed, symbolic-local, and world/concept/epistemic uses is not allowed without an explicit substrate and/or `referencePlane` declaration when those distinctions are live.

6. **CC-A.6.Q-6 - Scope and `Γ_time` are explicit when omission changes meaning.**
   If scope or time selection affects interpretation, the ascription declares `U.Scope` and/or `Γ_time` explicitly.

7. **CC-A.6.Q-7 - Lawful normal form.**
   The ascription is published as `SignalPack`, `Characteristic`, `Bundle`, or `Objective`, with the corresponding discipline observed.

8. **CC-A.6.Q-8 - No illegal scalarisation.**
   Composite senses are not collapsed into one score without an explicit scoring method.

9. **CC-A.6.Q-9 - No silent sense rewrite.**
   Any semantic change in the ascription uses the declared change lexicon; changing sense silently is forbidden.

10. **CC-A.6.Q-10 - QD default.**
   In search/selection/NQD contexts, *quality* resolves to `QS.UseValue` unless overridden explicitly.

11. **CC-A.6.Q-11 - Engineering family discipline.**
   Engineering `-ility` uses resolve to one explicit `U.Characteristic` or one explicit `Bundle` (preferably authored as `Q-Bundle` when composite); they are not left as free-floating adjectives.

12. **CC-A.6.Q-12 - Functional separation.**
    Function/capability claims remain distinct from quality-family claims.

13. **CC-A.6.Q-13 - Bridge accountability.**
    Cross-tradition parallels publish bridge stance and loss notes; cross-context or cross-plane reuse cites explicit Bridge ids and CL policy where applicable.

14. **CC-A.6.Q-14 - Boundary-routing hook when needed.**
    If a repaired quality ascription is used for admissibility, commitments, publication, or adjudication, the downstream `L/A/D/E` hooks are explicit rather than carried implicitly by the word *quality*.

15. **CC-A.6.Q-15 - Lexical firewall.**
    Bare *quality* is absent from Tech/normative prose except as quoted metalinguistic discussion.

16. **CC-A.6.Q-16 - `evaluativeAscription` contract skeleton is published.**
    The family-specific `RelationKind` token `evaluativeAscription` resolves to a contract skeleton that publishes polarity, participant SlotSpecs, qualifier expectations, repair paths for bearer-kind mismatches, witness discipline, admissible change classes, and cross-context/plane policy.

17. **CC-A.6.Q-17 - Candidate-Set Note is used when ambiguity is live.**
    If sense selection, bearer facet, or A.7 lane (`Object | Description | Carrier`) is non-obvious, the text records a short Candidate-Set Note before the rewrite is treated as decision-bearing or publication-bearing.

18. **CC-A.6.Q-18 - Evaluator and viewpoint are not silently collapsed.**
    When both an evaluator and a `U.Viewpoint` matter, they are represented as separate slots or fields.

19. **CC-A.6.Q-19 - Family-specific change verbs dock cleanly with A.6.P / A.6.5.**
    `retargetBearer(...)` is used only for ref retargeting; sense/frame/bundle/scale/view edits are narrated as explicit by-value revisions; silent retyping is forbidden.

### A.6.Q:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | Symptom | Why it fails | How to avoid / repair |
| --- | --- | --- | --- |
| **Magic scalar quality** | one number silently stands for several evaluative families | collapses senses, carriers, and scoring legality | publish one explicit `QualitySense` and a lawful normal form |
| **Preconceptual-as-metric** | felt fit is presented as if it were already a measured characteristic | erases articulation stage and overstates evidence | keep it as `SignalPack` until a lawful proxy is declared |
| **Engineering adjective drift** | *reliable / maintainable / high-quality* appear with no explicit Characteristic or Q-Bundle | hides measurement shape and scope | rewrite to one `U.Characteristic` or one `Q-Bundle` |
| **Selector ambiguity** | *quality in QD/NQD* is left undefined | breaks comparability and selection semantics | default to `QS.UseValue` unless another objective head is declared explicitly |
| **Model-quality collapse** | latent fit, explanatory merit, and control adequacy are merged under one phrase | destroys carrier and frame distinctions | split into separate `evaluativeAscription(...)` records |
| **Architecture-vs-description collapse** | *architecture quality* is used with no explicit bearer lane | collapses the described system into its description/carrier/publication face | publish the bearer lane explicitly and route to `QS.EngineeringQualityFamily` or `QS.ArchitecturalDescriptionFitness` |
| **Affordance-as-quality** | action invitations are narrated as if they were evaluations | wrong relation family; the rewrite hides action semantics instead of clarifying them | stop the Q-rewrite and `changeRelationKind(...)` into the appropriate affordance/action-invitation family |
| **Bridge-by-label** | two traditions both use *quality*, so the draft implies they are the same | creates false identity and silent loss | publish one bridge stance with loss notes |

### A.6.Q:9 - Consequences

**Benefits.**
This pattern makes evaluative language auditable across phenomenology, engineering, and search/selection contexts.
It also makes later lexical migration easier because the repair is carried by one explicit relation family rather than by ad hoc prose rules.

**Trade-offs / mitigations.**
The pattern adds authoring overhead and can feel heavy in exploratory notes.
Mitigation: allow bare *quality* in Plain commentary during exploration, but require repair before the term enters Tech/normative, boundary, selector, or assurance surfaces.

### A.6.Q:10 - Rationale

A.6.Q makes one strategic move:

> **The word “quality” is not treated as one concept. It is treated as a family of evaluative ascriptions whose members differ by substrate, articulation mode, bearer, frame, and lawful publication form.**

This lets FPF discuss:

* Pirsig-like preconceptual fit,
* representation-learning and neuro-symbolic latent fit,
* explanation quality in criticism-driven inquiry,
* architecture-description fitness under a viewpoint,
* engineering quality families,
* use-value in open-ended evolution,
* control adequacy in action loops,

without forcing them into one false universal scalar.

It also makes the distributed-vs-local issue explicit:

* some senses originate in **embodied** or **latent-distributed** substrates,
* some are only publishable as **symbolic-local** CHR/bundle/objective forms,
* and some require an explicit **projection** from the first into the second.

It also makes the bearer/plane issue explicit:

* some uses evaluate the **described entity**,
* some evaluate its **description** under a viewpoint,
* some evaluate a **carrier** or **publication face**,
* and those readings must not be collapsed without an explicit bearer lane and, when needed, a declared `referencePlane`.

That is exactly where semantic drift usually starts; A.6.Q turns that drift into an auditable design choice.

### A.6.Q:11 - SoTA-Echoing

**Evidence binding note.** If your Context maintains a **SoTA Synthesis Pack** for evaluative language, architecture-quality vocabularies, selector/objective semantics, world-model evaluation, or embodied/preconceptual articulation, this section **SHALL cite** its ClaimSheet IDs / CorpusLedger entries / BridgeMatrix rows and keep the adoption stances below consistent with those IDs. Otherwise, treat the table below as the source-of-truth seed list for this pattern revision.

This section follows the required craft: **claim > practice > source > alignment > adoption status**. A.6.Q aligns with contemporary practice across architecture-description standards, software-quality standards, evolutionary architecture, QD search, active inference/world-model research, phenomenology/TAE, affordance theory, and philosophy of explanation—while making one explicit FPF move that those traditions usually leave implicit: the overloaded token *quality* is repaired into explicit evaluative endpoint forms, with `evaluativeAscription(...)` available as a declared transitional record carrying `QualitySense`, bearer, frame, lawful normal form, and bridge stance while routing remains open.

| Claim (A.6.Q need) | SoTA practice (post-2015) | Primary source (post-2015) | Alignment with A.6.Q | Adoption status |
|---|---|---|---|---|
| Description-side quality must not be confused with system-side quality. | Contemporary architecture-description practice distinguishes the **entity of interest** from the **architecture description** and structures discourse through viewpoints, concerns, and model kinds. | ISO/IEC/IEEE 42010:2022, *Software, systems and enterprise — Architecture description*. | A.6.Q mirrors this split by separating `QS.ArchitecturalDescriptionFitness` from system-side `QS.EngineeringQualityFamily`, and by requiring an explicit bearer lane plus `referencePlane` when phrases such as *architecture quality* appear. | **Adopt/Adapt.** Adopt the entity-vs-description split; adapt by making lexical repair and bearer-lane publication mandatory. |
| Engineering “quality” should resolve to explicit heads, not free adjectives. | Contemporary systems/software quality practice works through named **characteristics** and **subcharacteristics** used to specify, measure, and evaluate quality, and to define acceptance criteria and requirements. | ISO/IEC 25010:2023, *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model*. | A.6.Q adopts the explicit-head discipline by routing engineering uses either to one lawful `Characteristic` or to one explicit `Bundle` / `Q-Bundle`, and by refusing to leave *quality requirement(s)* as bare noun phrases. | **Adopt/Adapt.** Adopt explicit quality heads; adapt by treating composite families as bundles rather than pretending that every family label is already a scalar. |
| Evolutionary architecture needs continuously checked heads rather than generic “quality”. | Evolutionary-architecture practice uses **fitness functions** to drive, manage, and automate change across architectural concerns, and ties structure to the capacity to support change. | Ford, Parsons, Kua, Sadalage (2022), *Building Evolutionary Architectures*, 2nd ed. | A.6.Q aligns by treating engineering quality families and change-support concerns as explicit evaluative heads under declared frames, not as one rhetorical “high quality” scalar. | **Adopt/Adapt.** Adopt the fitness-function discipline; adapt by keeping `QS.EngineeringQualityFamily`, `QS.ControlAdequacy`, and `QS.UseValue` distinct and by forbidding function/quality-family collapse. |
| In QD / NQD / selector settings, “quality” is an objective head under a declared search frame. | Modern QD work is explicit that search returns a **collection** of solutions that are high with respect to an objective and diverse with respect to declared measures / behavior descriptors; the archive is not a synonym for one hidden global score. | Fontaine, Togelius, Nikolaidis, Hoover (2020), *Covariance matrix adaptation for the rapid illumination of behavior space*; Fontaine & Nikolaidis (2023), *Covariance Matrix Adaptation MAP-Annealing*. | A.6.Q therefore defaults selector-context *quality* to `QS.UseValue` in `Objective` form, while keeping novelty/diversity/constraints explicit and separate. | **Adopt/Adapt.** Adopt objective-explicit selector semantics; adapt by making the Q-head a named `QualitySense` and by rejecting unexplained scalar collapse. |
| Latent fit, world-model adequacy, and closed-loop control must not collapse into one phrase. | Contemporary world-model and active-inference work evaluates generative/predictive models, planning, action, uncertainty reduction, and intrinsic objectives in explicitly multi-layered terms rather than through one undifferentiated “model quality”. | Parr, Pezzulo, Friston (2022), *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior*; LeCun (2022), *A Path Towards Autonomous Machine Intelligence*; Friston et al. (2024), *Designing Ecosystems of Intelligence from First Principles*. | A.6.Q adapts this by separating `QS.LatentFit`, `QS.ControlAdequacy`, and `QS.UseValue`, and by requiring explicit evaluation frames and witnesses for each ascription. | **Adapt.** Adapt multi-layer evaluation into one repair discipline; reject the colloquial habit of letting *model quality* silently cover representation, prediction, control, and utility at once. |
| Preconceptual felt fit should remain pre-metric until lawfully articulated. | TAE-style practice treats felt dimensions of thinking as something that can be clarified progressively with tentative language that stays responsive to lived experience and widens conceptual structure. | Schoeller (2022), *Thinking at the Edge in the context of embodied critical thinking: Finding words for the felt dimension of thinking within research*. | A.6.Q uses this as direct support for `QS.PreconceptualFit` in `SignalPack` form, with exemplars, articulation notes, and an explicit ban on premature promotion to `Characteristic`. | **Adopt/Adapt.** Adopt progressive articulation from felt sense to wording; adapt by giving that articulation a lawful publication form and explicit witness discipline. |
| Some trigger uses of “quality” are really about action invitation, not evaluative ascription. | Recent affordance work treats affordances as perceptually available action possibilities, and in some accounts as invitations or action-guiding structures that position the agent to act. | Hansen (2024), *Perceiving affordances and the problem of visually indiscernible kinds*; Jorba & Lopez-Silva (2024), *Mind in action: expanding the concept of affordance*. | A.6.Q adopts this as an explicit carve-out: when the trigger use is primarily affordance / action-invitation talk, the lawful move is to `changeRelationKind(...)` out of `evaluativeAscription` rather than forcing an evaluative reading. | **Adopt/Adapt.** Adopt the action-guiding insight; adapt by making relation-family exit explicit and auditable. |
| Explanation quality is an epistemic merit family, not engineering quality or selector utility. | Contemporary philosophy of explanation treats understanding, explanatory value, and the cognitive significance of explanations as a distinct epistemic topic. | Khalifa (2017), *Understanding, Explanation, and Scientific Knowledge*. | A.6.Q therefore treats explanatory evaluation as `QS.ExplanatoryMerit`, typically `Bundle`-shaped, and rejects silent collapse into engineering `-ilities`, bare usefulness, or one unexplained “high-quality explanation” score. | **Adapt.** Adapt explanatory-value practice into a slot-explicit evaluative family; reject cross-family scalarization by label. |

**Short alignment notes.**

**Architecture-description practice.** ISO 42010 is the clearest contemporary guard against collapsing the described entity into its description. A.6.Q adopts that guardrail and strengthens it lexically: a draft may not say *architecture quality* without publishing which bearer lane is under evaluation and whether the evaluation is description-side or system-side.

**Engineering quality practice.** ISO 25010 gives a mainstream reason not to leave *quality* as a free noun: contemporary quality work is organized around named characteristics and subcharacteristics that are specified, measured, and evaluated. A.6.Q adopts that explicit-head discipline, but adapts it by routing composite cases to `Bundle` / `Q-Bundle` and by treating *quality requirement(s)* as requirements over explicit heads rather than as self-standing nouns.

**Evolutionary-architecture practice.** Fitness functions treat architecture-relevant concerns as continuously monitored heads tied to change and governance, not as one mystical scalar. A.6.Q adopts that operational spirit, but adapts it by keeping engineering-family evaluation, control adequacy, and selector value distinct and by forbidding function/quality-family collapse.

**QD / NQD practice.** Modern QD work is explicit that search returns a collection of solutions that are high with respect to an objective and diverse with respect to declared measures. A.6.Q therefore adopts the default rewrite of selector-context *quality* to `QS.UseValue` in `Objective` form and rejects any rewrite that silently blends novelty, diversity, constraints, and utility into an unexplained scalar.

**World-model and active-inference practice.** Contemporary world-model and active-inference work uses generative/predictive models for perception, planning, learning, and action, which makes evaluation inherently multi-layered: latent representation quality, model evidence or predictive adequacy, policy adequacy, and task/objective value are not one thing. A.6.Q adapts this by separating `QS.LatentFit`, `QS.ControlAdequacy`, and `QS.UseValue`, and by requiring explicit evaluation frames and witnesses for each ascription.

**Phenomenology / TAE practice.** TAE-style work treats a felt sense as something that can be clarified and worded progressively, with tentative language that stays responsive to lived experience. A.6.Q adopts this progressive-articulation stance by giving `QS.PreconceptualFit` a lawful `SignalPack` form and by keeping `QS.PhenomenalCharacter` separately available when the experienced character itself—not action-guiding fit—is the topic.

**Affordance practice.** Recent affordance work emphasizes that affordances can be perceptually experienced as action possibilities that position or invite the agent to act. A.6.Q adopts that insight as a routing rule: when the trigger use of *quality* is really action-invitation talk, the author should `changeRelationKind(...)` out of `evaluativeAscription` rather than forcing an evaluative reading.

**Explanation practice.** Contemporary philosophy of explanation keeps explanatory understanding and epistemic value distinct from engineering performance or utility maximization. A.6.Q adapts this by publishing `QS.ExplanatoryMerit` as its own evaluative family—typically `Bundle`-shaped—and by rejecting hidden scalarization into “high-quality explanation” without explicit heads.

**Scale legality.** The rows above do **not** license free arithmetic on the word *quality*. Whenever A.6.Q operationalizes engineering heads, selector objectives, or control adequacy numerically, it **SHALL** bind the comparison to an explicit `ComparatorSet` / `CG-Spec` / declared aggregation policy and **SHALL** reject covert scalarization of bundles, explanations, or preconceptual signals.

**Cross-Context / plane note.** This section states alignment and non-identity only; it does **not** assert silent sameness across `U.BoundedContext`s or across planes. Any actual reuse of a quality vocabulary, selector head, or viewpoint-bound quality family across Contexts/planes **SHALL** publish `BridgeId` + `CL` / loss-note policy and, where planes differ, the relevant `Φ(CL)` / `Φ_plane` policy-ids.

**Historical-lineage note.** Earlier touchstones such as Pirsig, Popper, and Deutsch remain useful as lineage and local-gloss resources, but A.6.Q does not use them as the formal SoTA anchors here because E.8 requires post-2015 primary sources for Architectural patterns.

This SoTA alignment supports the pattern’s central move: *quality* is not one universal evaluative noun. In contemporary practice, the relevant work is already distributed across explicit characteristics, objectives, viewpoints, world-model criteria, explanatory virtues, felt signals, and action invitations; A.6.Q makes that distribution first-class and auditable.

### A.6.Q:12 - Relations

* **Specialises:** **A.6.P** as an RPR pattern for overloaded evaluative language centered on *quality*.
* **Builds on:** **A.2.6** for explicit scope and `Γ_time`, **A.17/A.18/C.16** for lawful measurable characteristics, **C.25** for engineering `Q-Bundle` authoring.
* **Coordinates with:** **A.6.A** for relation-family exits into action-invitation repair; **C.2.2a / A.16 / A.16.1 / A.16.2 / B.4.1** for language-state chart positions, lawful moves, early cue routing, responsibility handoff, and lawful retreat/reopen; use **A.16.0** only when lineage, branch, loss, or handoff history itself must be published as an explicit trajectory account; **B.5.2.0** for prompt-shaped continuations that are not yet stable endpoint publication; **C.2.LS / C.2.4 / C.2.5 / C.2.6 / C.2.7** for language-state facet ownership; **C.17/C.18/C.19** for `QS.UseValue`, novelty/diversity discipline, and selector policy; **E.17.0/E.17.2** for architecture-description/viewpoint bundles; **F.9 / F.9.1** for Bridges, CL, and bridge-stance annotations; **A.6.B** when repaired ascriptions become boundary-bearing.
* **Recommends publication via:** **E.10 / F.17 / F.18** when the `evaluativeAscription` contract skeleton, the `QualitySense` starter set, and the red-flag rewrites become stable shared vocabulary.

#### A.6.Q:12.1 - Language-space refactor note
This pattern uses **endpoint-first routing** rather than universal ownership of all quality language. `evaluativeAscription(...)` remains useful as a transitional repair record, but it is not the required resting place for every repaired use of `quality`.

#### A.6.Q:12.2 - Explicit endpoint routing
Lawful endpoints after repair include:
- a single `Characteristic`,
- a `Q-Bundle`,
- an `Objective`,
- an explanatory-merit bundle,
- a selector-value endpoint.

Bare `quality` on Tech surfaces should therefore be banned or routed immediately to an explicit endpoint owner. If that owner is already known, `evaluativeAscription(...)` need not remain in the published normal form.

#### A.6.Q:12.3 - Ownership boundary
This pattern does not own articulation-state axes, bridge stances, or representation axes. Those remain owned by `A.16`, `C.2.LS`, `C.2.4`, `C.2.5`, `C.2.6`, `C.2.7`, and `F.9.1`.
### A.6.Q:End

