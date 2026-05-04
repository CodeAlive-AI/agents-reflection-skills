## E.17.EFP - ExplanationFaithfulnessProfile — explanation classification over existing MVPK faces

**Placement.** Hosted profile under `E.17.0 / E.17` host review.  
**Builds on.** `E.17.0 U.MultiViewDescribing`; `E.17` MVPK; `A.7`; `E.10.D2`; `A.6.B`; `F.9`; `F.18`.  
**Coordinates with.** `ConservativeRetextualization`; `RepresentationTransduction`; `E.17.ID.CR ComparativeReading`; `A.6.4`; `A.15`; `A.20`; `A.21`.

**One-line summary.** `ExplanationFaithfulnessProfile` classifies explanation-facing renderings over already available claims, traces, and pins on existing MVPK faces. It helps reviewers distinguish source-pinned rendering, source-linked reconstruction, didactic retelling, and speculative retelling without creating a second face family or a second semantic rule track.

### E.17.EFP:1 - Problem frame

The same underlying claim set often needs explanation-facing renderings on more than one existing face:
- an engineer-manager-readable rendering of a technical claim set;
- a technical explanation that makes source linkage more visible than the original source prose;
- a didactic retelling for onboarding or review preparation;
- a clearly marked speculative retelling that helps discussion but does not pretend to be canonical content.

FPF already has `E.17.0` for viewpoints, views, and correspondences, and `E.17` for typed publication faces. A compact review profile is still needed to say what kind of explanation-facing rendering is being published, how strongly it stays tied to source material, and where it is admissible.

### E.17.EFP:2 - Problem

Without a dedicated profile:
1. source-pinned rendering, reconstruction, didactic simplification, and speculation blur together;
2. explanation prose starts behaving like a second semantic rule track;
3. reviewers cannot tell which faces remain lawful for a given explanation class;
4. pins, provenance, and evidence binding become optional rhetorical extras instead of explicit publication conditions;
5. explanation work quietly drifts into new claims, hidden bridge work, or gate-facing misuse.

### E.17.EFP:3 - Forces

- **Clarity vs semantic restraint.** Explanation may help readers, but it must not mint new semantic commitments on publication faces.
- **Face discipline vs reader fit.** The same source may need different renderings, but all of them still live on existing MVPK faces.
- **Traceability vs accessibility.** Simpler renderings are useful only if readers can still recover how they relate to the source.
- **Didactic usefulness vs policy misuse.** A didactic or speculative retelling may help humans, but it must not masquerade as assurance or gate-bearing content.
- **Explanation vs interpretation.** Some moves still belong to explanation rendering; others should exit toward interpretation, retargeting, or world/gate owners.

### E.17.EFP:4 - Solution — review profile for explanation renderings on existing MVPK faces

#### E.17.EFP:4.1 - Informal definition

> `ExplanationFaithfulnessProfile` is a hosted review profile for explanation-facing renderings over already available claims, traces, and pins on existing MVPK faces.
>
> It does not create a new face family. It classifies how an explanation relates to its source material, what kind of augmentation is allowed, how strongly evidence remains bound, and on which existing faces the rendering may lawfully appear.

#### E.17.EFP:4.1.a - Profile, case, and published rendering distinction

`ExplanationFaithfulnessProfile` is an **intensional hosted profile** under `E.17.0 / E.17`. Concrete explanation-facing renderings are passive published renderings or reviewed cases classified under this profile; the profile itself does not act, decide, or publish.

This distinction matters because the profile governs **how** a rendering is classified and reviewed. It does not turn every explanatory paragraph into a giant standalone record, and it does not replace MVPK face ownership with a second semantic track.

#### E.17.EFP:4.1.b - How to read this profile

This profile does not decide whether a claim is true. It says how an explanation rendering relates to already available claim-bearing material and where that rendering may lawfully appear.
- Class names are publication-behaviour labels, not merit labels.
- Faces stay owned by `E.17`; the profile only constrains what sort of explanation is lawful on them.
- If a rendering begins to add new semantic commitments, it has left this profile even if the prose still looks explanatory.
- It helps reviewers classify one published rendering relative to already pinned source material.

#### E.17.EFP:4.1.c - Local working vocabulary

This profile uses a small local vocabulary for review.
- **Source material** = already pinned claims, traces, notes, or other reviewable source-bearing material.
- **Rendering** = one published explanation-facing text on one existing face.
- **Class assignment** = the explanation-class assigned to that rendering on that face.
- **Bundle-level difference** = a case where two renderings in one bundle lawfully carry different explanation classes.

These are review aids, not new owner kinds. Faces remain owned by `E.17`; this profile only qualifies explanation behaviour on those faces.

#### E.17.EFP:4.2 - Core profile fields

A rendering reviewed under this profile should make explicit at least:
- `landingForm = profile under E.17/E.17.0 host review`;
- `hostOwner = E.17 / E.17.0`;
- `sourceForm`;
- `targetForm`;
- `changeLocus`;
- `describedEntityPolicy = preserve` for explanation renderings over the same underlying claim-bearing material;
- `boundedContextPolicy`;
- `viewpointPolicy`;
- `referenceSchemePolicy`;
- `representationSchemePolicy`;
- `groundingPolicy`;
- `referencePlanePolicy`;
- `claimPolicy`;
- `claimScopePolicy`;
- `publicationScopePolicy`;
- `reliabilityTransportPolicy`;
- `pinningPolicy`;
- `provenancePolicy`;
- `lossProfile`;
- `claimContinuityClass`;
- `microtheoryContinuityClass`;
- `onticContinuityClass`;
- `bridgeRequirement`;
- `worldContactPolicy`;
- `evidencePolicy`;
- `gatePolicy`;
- `workCrossing`;
- `upstreamOwner` / `downstreamOwner`;
- `admissibleFaces`;
- `admissibleSurfaces`;
- `publicNamePolicy`;
- `sourceRelation`;
- `augmentationRelation`;
- `addedLinkPolicy` when `SourceLinkedReconstruction` adds bounded connective prose;
- `targetUserModel?` when reader-fit materially shapes the rendering;
- `interactionMode?` when the explanation is more than one static explanatory paragraph;
- `contrastiveQuestion?` when the rendering is answering a specific user-facing contrast or why-question;
- `allowedUptake?` when downstream use must be bounded by reader role or task;
- `misuseRisk?` when over-reading pressure is part of the review burden;
- `evidenceRelation`;
- `noNewBoundaryClaims = true` on explanation faces;
- `compositionLaw`;
- `reopenCondition`.

Where explanation crosses from source rendering into new claim production, hidden bridge work, gate-bearing semantics, or world-facing intervention claims, the profile no longer suffices and the case must leave this profile.

#### E.17.EFP:4.2.a - Working-model first

Ordinary reviewed renderings do not need to restate every field from scratch. When the host face, pinned source material, and already published provenance anchors already fix a field honestly, the rendering may inherit that condition by explicit reference.

A fuller review record becomes necessary when:
- explanation class differs across faces in the same publication bundle;
- the rendering relies on bounded connective prose that is not obvious from the source wording alone;
- didactic or speculative wording creates a real risk of policy, assurance, or gate misuse;
- source linkage, provenance, or reliability transport would otherwise become unclear.

#### E.17.EFP:4.2.b - What a reviewer checks first

A reviewer usually starts with four questions:
1. What exactly is the source-bearing material for this rendering?
2. Which explanation class is being claimed for this rendering on this face?
3. Are the pins, provenance anchors, and evidence relation visible enough for that class?
4. Has the rendering quietly begun to add new semantic commitments or new face-like behaviour?

If these questions are answered clearly, the rendering often remains lightweight. If they are not, a fuller face-by-face review record is usually warranted.

#### E.17.EFP:4.2.c - Interpretant-side block

This profile still governs explanation renderings on existing faces, not full interactive explanation systems.

However, when reader-help, onboarding, or contrastive explanation is doing real work, the rendering should also make visible:
- who the rendering is fit for (`targetUserModel`);
- whether the interaction is static, guided, contrastive, or another bounded mode (`interactionMode`);
- what question the rendering is helping answer (`contrastiveQuestion`);
- what uptake remains lawful (`allowedUptake`);
- and what stronger uptake would be wrongful (`misuseRisk`).

These fields do not create a new owner. Their current role is narrower: stop explanation prose from pretending that every rendering is audience-neutral, and make misuse boundaries explicit when reader-fit is part of the explanation burden.

#### E.17.EFP:4.3 - Explanation class set

The explanation-class set used in this profile is:
- `SourcePinnedRendering`
- `SourceLinkedReconstruction`
- `DidacticRetelling`
- `SpeculativeRetelling`

These classes are not mere style labels. They state how the explanation relates to the source, how much augmentation is tolerated, what reliability transport is still honest, and which faces remain lawful.

Class assignment is per published rendering on a face, not one blanket label for a whole multi-face bundle. If a Plain rendering stays source-pinned while a Tech rendering adds bounded connective prose, the bundle must state that class difference explicitly.

#### E.17.EFP:4.3.a - Ordinary class-selection guidance

A practical reading order is:
- start with `SourcePinnedRendering` if the rendering stays close to the source wording and keeps direct pins visible;
- move to `SourceLinkedReconstruction` when bounded connective prose is added but source linkage remains explicit;
- move to `DidacticRetelling` when reader-help dominates and some phrasing is intentionally more pedagogical than canonical;
- move to `SpeculativeRetelling` only when the rendering openly goes beyond source-backed explanation and remains confined to exploratory or didactic use.

The profile should not be used to make a rendering sound more respectable than its actual source relation warrants.

#### E.17.EFP:4.3.b - `SourceLinkedReconstruction` added-link policy

When a rendering claims `SourceLinkedReconstruction`, it should publish a compact `addedLinkPolicy` whenever the connective move is not already explicit in the source wording.

Minimum reading burden:
- `addedLinkKind` — what bounded connective move is being added;
- `sourceAnchorSet` — which pinned claims, traces, or notes support that move;
- `boundednessReason` — why the added link does not become a stronger theory, modality lift, causal claim, bridge burden, or policy-bearing reading;
- `forbiddenLinkClass` — which stronger connective move is explicitly excluded;
- `reopenTrigger` — what would force downgrade, reroute, or fuller review.

Working rule:
- if `addedLinkPolicy` cannot be stated plainly, the rendering should drop to a weaker class, move to a more restricted face/surface, or leave `E.17.EFP`;
- `SourceLinkedReconstruction` may not hide new relation theory, bridge equivalence, design-level generalization, or policy-bearing guidance inside "bounded" connective prose.

#### E.17.EFP:4.4 - Working admissibility matrix

| Class | Source relation | Augmentation relation | Evidence relation | Usually admissible faces | Usually admissible surfaces | Usually forbidden uses |
|---|---|---|---|---|---|---|
| `SourcePinnedRendering` | rendering | omission-only | trace-bound | Plain, Tech | `PublicationSurface`; `InteropSurface` only when the host explicitly permits source-pinned, structure-preserving export without added semantics | Assurance or gate-bearing use if required pins/evidence are absent |
| `SourceLinkedReconstruction` | reconstruction | bounded link-addition | trace-supported | Plain, Tech | `PublicationSurface` on bounded explanatory use | Interop or Assurance unless host policy explicitly allows it with source linkage kept visible |
| `DidacticRetelling` | reconstruction | omission + didactic addition | trace-supported or partly trace-free | Plain | `PublicationSurface` on didactic or onboarding use only | Tech, Interop, Assurance, or policy-bearing use when it could be mistaken for canonical semantics |
| `SpeculativeRetelling` | speculation | link-addition or counterfactual augmentation | trace-free or weakly trace-supported | Plain | `PublicationSurface` on clearly marked exploratory or didactic use only | Tech, Interop, Assurance, gate-adjacent, or policy-bearing use |

`ExplanationFaithfulnessProfile` ordinarily stays on `PublicationSurface`. Any appearance on `InteropSurface` must remain source-pinned and structure-preserving, and must never smuggle explanation-specific semantics into interop publication. Didactic or speculative restrictions are use-profile restrictions over existing faces, not new face kinds.

Source-pinned explanation on Assurance-facing publication is exceptional rather than ordinary. Unless the host explicitly permits that use with visible evidence carriers, source pins, and no added semantics, reviewers should treat Assurance-facing explanation rendering as non-admissible.

Every concrete explanation rendering must also publish the source claim IDs, pins, trace refs, or equivalent provenance anchors that justify its class on that face. If those anchors cannot be made visible on the chosen face or surface, the rendering must drop to a weaker class, move to a more restricted use profile, or leave the face.

When reader-help, onboarding, or contrastive explanation is part of the case, the rendering should also publish or inherit its `targetUserModel`, `interactionMode`, `contrastiveQuestion`, `allowedUptake`, and `misuseRisk` so that user-fit does not quietly become stronger policy guidance.

#### E.17.EFP:4.5 - Shared explanation law packet

##### E.17.EFP:4.5.a. Preservation law
Explanation-facing renderings under this profile preserve the same underlying described-entity line, bounded context, and source-pinned claim-bearing material. Viewpoint, reference scheme, representation scheme, grounding, and reference-plane handling must stay explicit rather than being left to prose. `SourcePinnedRendering` and `SourceLinkedReconstruction` are expected to remain claim-conservative; `DidacticRetelling` may be claim-attenuating but must stay source-linked; `SpeculativeRetelling` may widen explanatory language only when kept clearly off canonical faces and off gate-bearing use.

##### E.17.EFP:4.5.b. Loss and reliability law
A rendering assigned to one of these explanation classes declares what is omitted, reordered, simplified, or newly connected. Reliability transport may stay source-bounded or be explicitly downgraded, but it must never be silently strengthened by more persuasive prose. Didactic and speculative renderings also state forbidden downstream uses whenever omissions, weakening, or trace-free additions occur.

When reader-fit is part of the explanation burden, `allowedUptake` and `misuseRisk` should be explicit enough that a didactic or contrastive rendering cannot be mistaken for stronger assurance, policy, or gate-bearing guidance.

##### E.17.EFP:4.5.c. Authority and handoff law
This profile stays explanation-facing and episteme-level. It does not own bridge stance, retargeting, route selection, executable docking, gate authority, or work enactment. If a case starts carrying one bounded comparative review surface, rival interpretations, bridge-mediated comparison burdens, or world/gate consequences, it must hand off to the appropriate downstream owner (`E.17.ID.CR`, `F.9.1`, `B.5.2`, `A.6.4`, `A.15`, `A.20`, `A.21`).

Interpretant-side fields do not weaken that handoff rule. They only bound reader uptake; they do not authorize stronger downstream guidance.

##### E.17.EFP:4.5.d. Composition and reopen law
Repeated `SourcePinnedRendering` over the same pinned source may be idempotent. `SourceLinkedReconstruction` and `DidacticRetelling` are order-sensitive and must reopen when the source claim set, pins, provenance, or admissible-face assumptions change. `SpeculativeRetelling` must reopen whenever stronger source binding becomes available or whenever the rendering starts to look like a canonical explanation rather than a clearly bounded exploratory retelling.

#### E.17.EFP:4.6 - Hard boundary rules

A rendering reviewed under this profile keeps the following explicit:
- it does **not** create a second face family;
- it does **not** turn faces into a second semantic rule track;
- it does **not** license new `L/A/D/E` claims on explanation faces;
- it does **not** replace bridge discipline, retargeting discipline, or world/gate handoff discipline;
- it does **not** let `PublicationSurface` and `InteropSurface` collapse into one undifferentiated explanation channel.

If explanation text starts carrying new semantic commitments instead of rendering or licensed explanation over existing ones, the case must leave this profile.

### E.17.EFP:5 - Archetypal grounding

#### E.17.EFP:5.1 - Source-pinned explanation across multiple faces
**Source claim slice.** `Claim D-14: Cooling loop CL-2 maintains the required temperature margin during standard load. Evidence pins: T-44, E-17.`

**Plain rendering.** `Cooling loop CL-2 keeps the required temperature margin in standard operation. Source pins: T-44, E-17.`

**Tech rendering.** `D-14 remains source-pinned to T-44 and E-17; this rendering only shortens and reorders the claim.`

This stays within `SourcePinnedRendering` because the rendering changes readability, not the semantic burden.

#### E.17.EFP:5.2 - Source-linked reconstruction
**Source slice.** `Claims D-14 and D-18 jointly constrain the safe operating window, but the relation is left implicit in the original note.`

**Published reconstruction.** `Claims D-14 and D-18 jointly bound the safe operating window; see the pinned source notes for the original wording and evidence anchors.`

This stays within `SourceLinkedReconstruction` if the connective prose remains bounded and does not add new claims.

A minimal `addedLinkPolicy` for this slice would say:
- `addedLinkKind = relation-explication only`;
- `sourceAnchorSet = {D-14, D-18}`;
- `boundednessReason = makes an already implied joint constraint explicit without adding a new mechanism, policy conclusion, or stronger modality`;
- `forbiddenLinkClass = design-level robustness or gate-sufficiency claim`.

#### E.17.EFP:5.2.a - Mixed-face bundle with different explanation classes
**Source slice.** `Claim D-31 and trace set T-8 jointly show that the reserve path remains available during the short overload interval.`

**Plain rendering.** `The reserve path stays available during the short overload interval. Source pins: D-31, T-8.`

**Tech rendering.** `D-31 and T-8 jointly support availability of the reserve path during the short overload interval; this rendering adds bounded connective prose to make the support relation explicit.`

The Plain rendering may stay `SourcePinnedRendering` while the Tech rendering is `SourceLinkedReconstruction`. The bundle is lawful only if that class difference is stated rather than hidden under one blanket label.

#### E.17.EFP:5.3 - Didactic retelling
**Source slice.** `The pressure-control condition is satisfied whenever the reserve valve opens within 80 ms.`

**Didactic rendering.** `For onboarding: the system stays safe here because the reserve valve opens quickly enough; the exact threshold and source claim remain in the pinned technical note.`

This stays in `DidacticRetelling` only if it is kept off Tech/Assurance faces where it could be mistaken for canonical semantics.

#### E.17.EFP:5.4 - Speculative retelling
**Source slice.** `The source materials record the observed recovery, but they do not explain why the recovery was so rapid.`

**Speculative rendering.** `One possible reading is that a temporary coupling effect accelerated recovery, but this is a reflective aid for discussion, not a source-backed claim.`

This is lawful only as a clearly marked exploratory or didactic use on an existing face; it must not appear as policy-bearing, gate-bearing, or assurance-bearing content.

#### E.17.EFP:5.4.a - Anti-example: explanation that quietly becomes a new claim
**Source slice.** `The pinned materials show the reserve path remained available during the short overload interval.`

**Overreaching rendering.** `The reserve-path design is therefore robust against short overloads.`

This no longer stays inside explanation classification. The rendering introduces a stronger design-level commitment than the pinned source actually states, so the case must reopen and route toward the appropriate owner instead of hiding inside a face-level explanation label.

#### E.17.EFP:5.4.b - Anti-example: reader help that quietly becomes policy-bearing use
**Source slice.** `The onboarding note explains, in simplified prose, that the reserve valve usually opens quickly enough to keep the local pressure condition inside the tolerated window.`

**Overreaching rendering on a stronger face.** `Operators may rely on this explanation as sufficient assurance that short overloads stay inside the tolerated window.`

This also exits the profile. The rendering is no longer only reader help over existing claims; it starts acting like policy-bearing or assurance-bearing guidance. The case must reopen, drop the explanation class, or move toward the appropriate downstream owner rather than staying on an explanation face.

#### E.17.EFP:5.5 - Class-specific reopen cues in the worked slices
- **`SourcePinnedRendering`** reopens when the pinned source claim set, source pins, or admissible-face assumptions change so that the rendering can no longer remain omission-only and visibly source-bound.
- **`SourceLinkedReconstruction`** reopens when the connective prose begins carrying a stronger relation than the source justifies, or when the source claim set changes enough that the bounded reconstruction is no longer plainly source-linked.
- **`DidacticRetelling`** reopens when the rendering moves onto Tech or Assurance-facing use, or when reader-help prose starts functioning as policy-bearing, design-bearing, or gate-bearing guidance.
- **`SpeculativeRetelling`** reopens when stronger source binding becomes available, or when the rendering starts to behave like canonical explanation rather than clearly bounded exploratory help.

#### E.17.EFP:5.6 - Boundary to interpretation and world handoff
If the rendering starts generating one bounded comparative review surface, rival interpretations, bridge-mediated comparative claims, new hypotheses, or world/gate consequences, it must leave this profile and move toward the appropriate owner track (`E.17.ID.CR`, `F.9.1`, `B.5.2`, `A.6.4`, `A.15`, `A.20`, `A.21`).

### E.17.EFP:6 - Bias-Annotation

Lenses tested: **Arch**, **Onto/Epist**, **Prag**, **Did**.
This profile intentionally biases toward explanation restraint on existing faces and against face inflation. The main mitigation is explicit admissibility by face, strong no-new-`L/A/D/E` discipline, and hard exits to interpretation, retargeting, and world/gate owners when explanation stops being only explanation.

### E.17.EFP:7 - Conformance Checklist

1. **CC-EF-1 — Explanation class is explicit.**
   The explanation class is explicitly named.
2. **CC-EF-2 — Admissible faces and surfaces are explicit.**
   The rendering states admissible faces and surfaces explicitly.
3. **CC-EF-3 — Pinning, provenance, and reliability transport are explicit.**
   Pinning, provenance, and reliability transport are stated explicitly.
4. **CC-EF-4 — Interpretant-side block is explicit when reader-fit does real work.**
   When onboarding, contrastive explanation, or other reader-fit shaping matters, `targetUserModel`, `interactionMode`, `contrastiveQuestion`, `allowedUptake`, and `misuseRisk` are visible enough to review.
5. **CC-EF-5 — No new `L/A/D/E` claims on explanation faces.**
   The no-new-boundary-claims rule is explicit on explanation faces.
6. **CC-EF-6 — Boundary to interpretation, retargeting, and world/gate handoff is explicit.**
   The reroute boundary is explicit.
7. **CC-EF-7 — No second face family.**
   A reviewer can tell why the case remains explanation-facing rather than becoming a second semantic rule track.
8. **CC-EF-8 — Bundle-level class differences are explicit.**
   When one publication bundle carries different explanation classes across faces, that difference is stated explicitly rather than hidden under one bundle-wide label.
9. **CC-EF-9 — Weakened classes publish forbidden downstream uses.**
   Didactic or speculative renderings, and any rendering with downgraded reliability transport, state their forbidden downstream uses explicitly.
10. **CC-EF-10 — Reopen triggers match the class.**
   The published review surface makes class-relevant reopen triggers visible when source claim set, pins, provenance, or admissible-face assumptions change.
11. **CC-EF-11 — `SourceLinkedReconstruction` publishes `addedLinkPolicy` when needed.**
   When bounded connective prose is doing real review work, the rendering states what link is added, why it remains bounded, and which stronger link class is explicitly forbidden.

### E.17.EFP:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | Why it is wrong | How to avoid it |
|---|---|---|
| Treating every explanatory prose block as equally faithful | rendering, reconstruction, didactic work, and speculation have different burdens | publish the explanation-class set and admissibility matrix |
| Letting reader-fit stay implicit when explanation is clearly tailored | a didactic or contrastive rendering can be over-read as general or policy-bearing guidance | publish the interpretant-side block whenever user model, uptake, or misuse boundaries are load-bearing |
| Using explanation faces as a second rule track | new semantic commitments hide behind reader-friendly prose | keep explanation faces tied to existing claim IDs, pins, and provenance |
| Calling connective reconstruction "bounded" without naming the added link | source-linked explanation quietly imports stronger relation theory or bridge burden | require `addedLinkPolicy` with source anchors, boundedness reason, and forbidden link class |
| Letting speculative prose enter technical or assurance use | speculative retelling starts to look canonical | restrict speculative retelling to clearly marked exploratory or didactic use on existing faces |
| Collapsing face and surface discipline | explanation appears to create a new publication family | stay on existing MVPK faces and keep surface/carrier policy explicit |

### E.17.EFP:9 - Consequences

- Explanation classes become explicit and reviewable.
- Existing MVPK face discipline stays intact.
- Pins, provenance, and evidence-binding become structural, not rhetorical extras.
- The boundary to interpretation, retargeting, and world/gate work becomes easier to review.

### E.17.EFP:10 - Rationale

This profile is worth stating explicitly because explanation-facing rendering is already happening on top of existing publication faces, but without a compact discipline reviewers have to reconstruct by hand whether a rendering is source-pinned, reconstructive, didactic, or speculative. A profile-first move is safer than freezing a heavier owner too early.

### E.17.EFP:11 - SoTA-Echoing

**SoTA note.** This section does not mint an independent second rule layer. It is a load-bearing alignment surface: the Solution, Conformance Checklist, boundary rules, and Relations of this pattern must match the stance stated here or explicitly justify any divergence.

**Traditions covered.** This profile binds itself to architecture-description governance, explainability and reliability guidance, and faithfulness evaluation for natural-language explanations.

| Claim need | SoTA practice (post-2015) | Primary source (post-2015) | Alignment with `E.17.EFP` | Adoption status |
|---|---|---|---|---|
| Explanation renderings must remain subordinate to governed views, published claims, and source-bearing material rather than quietly becoming a second semantic layer. | Architecture-description practice keeps views, viewpoints, correspondences, and architecture descriptions explicit instead of letting reader-help prose replace governed source. | ISO/IEC/IEEE 42010:2022 | `E.17.EFP` adopts this by keeping explanation on existing MVPK faces, tying class assignment to source-bearing material, and rejecting a second face family or second semantic rule track. | **Adopt.** |
| Explanation quality is use- and audience-sensitive and must make knowledge limits visible rather than collapse all explanations into one generic mode. | Explainable-AI guidance distinguishes explanation obligations by user, purpose, and stated limits instead of one universal explanation class. | Phillips et al. (2021), *Four Principles of Explainable Artificial Intelligence* | `E.17.EFP` adapts this into explicit explanation classes, admissible faces, and forbidden downstream uses, while keeping the host face system unchanged. | **Adopt/Adapt.** |
| Faithfulness is not the same as plausibility; explanation evaluation must stay tethered to the underlying source or decision basis. | Faithfulness work in interpretable NLP treats explanation as source-sensitive and warns against equating persuasive prose with faithful interpretation. | Jacovi & Goldberg (2020), *Towards Faithfully Interpretable NLP Systems* | `E.17.EFP` adopts this by requiring source relation, evidence relation, pins, provenance, and class-per-rendering review rather than fluency alone. | **Adopt.** |
| Natural-language explanation needs explicit checking for faithfulness or self-consistency rather than trust in stylistic coherence. | Recent evaluation work treats natural-language explanation as a review problem with explicit faithfulness or self-consistency checks, not just readability. | Parcalabescu & Frank (2024), *On Measuring Faithfulness or Self-consistency of Natural Language Explanations* | `E.17.EFP` adapts this into admissibility review, class downgrade, and reopen duties when source anchoring, evidence relation, or face assumptions weaken. | **Adapt.** |

**Architecture-description governance tradition.** `E.17.EFP` adopts the rule that reader-helpful renderings stay subordinate to already governed publication material rather than replacing it. Explanation therefore remains on existing faces and is judged against source-bearing claims, pins, and provenance anchors.

**Explainability and reliability traditions.** `E.17.EFP` adopts the distinction between source-bound explanation and merely plausible explanation prose. It rejects the still-popular shortcut in which fluent or pedagogically useful language is treated as sufficient evidence of explanation faithfulness.

**Local stance.** Best-known current practice supports a narrow rule: explanation renderings are lawful only when their class, source anchoring, evidence relation, admissible faces, and forbidden downstream uses remain visible enough that reader help does not become a second semantic rule track.

### E.17.EFP:12 - Relations

- **Builds on:** `E.17.0`, `E.17`, `A.7`, `E.10.D2`, `A.6.B`, `F.9`, `F.18`
- **Coordinates with:** `ConservativeRetextualization`, `RepresentationTransduction`, `E.17.ID.CR ComparativeReading`, `A.6.4`, `A.15`, `A.20`, `A.21`
- **Impact radius:** primary touch `E.17.0 / E.17`; secondary review surfaces `F.9`, `A.6.4`, `A.15`, `A.20`, `A.21`; any move toward new semantics or gate-bearing use exits the profile
- **Boundary notes:** comparative-interpretation cases exit to `E.17.ID.CR ComparativeReading`; retargeting exits to `A.6.4`; world/gate-bearing consequences exit to `A.15`, `A.20`, or `A.21`.

### E.17.EFP:End


