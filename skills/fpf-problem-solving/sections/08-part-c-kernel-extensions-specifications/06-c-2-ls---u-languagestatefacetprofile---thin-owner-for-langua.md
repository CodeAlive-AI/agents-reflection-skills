## C.2.LS - U.LanguageStateFacetProfile - Thin owner for language-state facets

> **Type:** Definitional (D)
> **Status:** Draft
> **Normativity:** Normative unless marked informative

**Plain-name.** Language-state facet profile.


### C.2.LS:1 - Problem frame
Once position claims in the declared language-state chart over `U.CharacteristicSpace` must be published and compared, teams need one thin owner that keeps the relevant facets visible as one explicit facet profile without turning that profile into a second characteristic calculus or a surrogate maturity ladder.

### C.2.LS:2 - Problem
Without a dedicated profile owner, authors blur articulation, closure, anchoring, and representation into one vague maturity story, or they silently reuse `F` as a surrogate. That blocks lawful threshold publication, weakens `A.16` move guards, and makes school-to-school bridge work harder than it needs to be.

### C.2.LS:3 - Forces
| Force | Tension |
|---|---|
| **Thin owner vs practical coordination** | Keep the owner small, but still give one stable place where the language-state facets are named together. |
| **Reuse vs duplication** | Reuse `A.18/A.19` characteristic machinery and `E.18` path publication rather than building a rival calculus. |
| **Local thresholds vs cross-context comparability** | Contexts need local thresholds, but the facet names must stay stable enough for bridge work and viewpoint bundles. |

### C.2.LS:4 - Solution
`U.LanguageStateFacetProfile` is a typed profile bundle that names the facets by which position claims in the declared language-state chart over `U.CharacteristicSpace` are published and interpreted:

- `formalityRef` -> `U.Formality` from `C.2.3`
- `articulationExplicitnessRef` -> `U.ArticulationExplicitness` from `C.2.4`
- `languageStateClosureDegreeRef` -> `U.LanguageStateClosureDegree` from `C.2.5`
- `languageStateAnchoringModeRef` -> `U.LanguageStateAnchoringMode` from `C.2.6`
- `languageStateRepresentationFactorBundleRef` -> `U.LanguageStateRepresentationFactorBundle` from `C.2.7`
- `thresholdRefs?` -> context-local threshold declarations over the owned facets
- `routeNotes?` -> informative notes that help interpret routing or reopening decisions

`C.2.LS` is therefore a **profile owner**, not a characteristic owner and not a trajectory owner. Characteristic semantics remain with `A.18/A.19`; lawful moves remain with `A.16`; explicit path publication remains with `E.18`.

#### C.2.LS:4.1 - Owner boundary
`C.2.LS` owns only the profile composition and the rule that the language-state facets must remain explicit and non-collapsed. It does **not**:

- redefine `F`;
- invent a second formality ladder;
- own the scale semantics of `AE`, `CD`, `LanguageStateAnchoringMode`, or `U.LanguageStateRepresentationFactorBundle`;
- own reopen/backoff moves;
- own endpoint routing or bridge kinds.

#### C.2.LS:4.2 - Threshold publication discipline
Any threshold used for routing, lawful move guards, or entry into `A.6.P` shall be published on explicit named facets within the profile. Contexts shall not speak of hidden sub-levels of `F` when what matters is really articulation, closure, anchoring, or the representation-factor bundle.

#### C.2.LS:4.2.a - Local profile-reading witness
For this pattern, a published facet profile is reviewable when:

- the facet refs are explicit or explicitly inherited from already pinned upstream material;
- any threshold-bearing use names the facet whose threshold is being invoked;
- route notes or local overlays remain informative and visibly docked to the explicit facet bundle;
- and the profile does not smuggle move law, bridge law, gate state, or downstream-owner semantics into the bundle record.

A polished label, one strong facet, or one memorable route note does not by itself yield a lawful profile reading. The profile remains conformant only when the named facets stay explicit and decomposable.

#### C.2.LS:4.3 - Composite readings
A language-state judgement may be composite, but the composite shall be decomposable. For example, a cue may be:

- low `AE`,
- medium `CD`,
- strongly `AM.TraceAnchored`,
- and representation-wise mixed rather than purely symbolic.

A conforming profile makes this decomposition visible rather than hiding it under one poetic label such as "early" or "raw".

#### C.2.LS:4.4 - Corridor map note
`C.2.LS` participates in the current `Language-State & Semantic Routing Corridor`, but only as the thin owner of the facet-profile bundle. Readers who need one map of the full language-state owner set should read the corridor note in `C.2.2a`.

That map does not change the owner boundary here: `C.2.LS` still does not own cue preservation, route-bearing publication, prompt entry, or downstream endpoint handoff.

### C.2.LS:5 - Archetypal Grounding
**Tell.** A team may say a draft is "still forming" for different reasons. `U.LanguageStateFacetProfile` forces the team to say whether the issue is low articulation, weak candidate-space closure, an anchoring mismatch, or an unresolved representation-factor bundle.

**Show (System).** An operator alert note can be strongly operator-loop anchored and low-closure without being low-formality in every respect.

**Show (Episteme).** An inquiry note can be low articulation yet already tightly anchored to exemplars and traces.

### C.2.LS:6 - Bias-Annotation
The pattern biases authors toward explicit facet ownership and away from master-scale stories. That cost is intentional: the goal is to prevent surrogate ladders from entering the Core.

### C.2.LS:7 - Conformance Checklist
- `CC-C.2.LS-1` A language-state facet profile **SHALL** reference explicit facet owners rather than invent local unnamed axes.
- `CC-C.2.LS-2` `C.2.LS` **MUST NOT** redefine `F` or create a second formality ladder.
- `CC-C.2.LS-3` Thresholds that matter for routing, reopening, or lexical repair **SHALL** be published on explicit facets.
- `CC-C.2.LS-4` Trajectory accounts that rely on facet profiles **SHOULD** reuse `A.16` move kinds and `E.18` path publication rules.
- `CC-C.2.LS-5` Composite labels such as `early`, `settled`, or `ready` **SHALL NOT** stand in for the explicit facet bundle when those states matter operationally.
- `CC-C.2.LS-6` Composite readings, overlays, and route notes **SHALL** remain decomposable into named facets and **MUST NOT** behave as hidden master axes.
- `CC-C.2.LS-7` A profile bundle **MUST NOT** smuggle move law, bridge law, gate state, or downstream-owner semantics into what should remain a thin facet-profile record.

### C.2.LS:8 - Common Anti-Patterns and How to Avoid Them
- **Shadow ladder.** Treating `early/late` as a master scale. Split the judgement into the named facets.
- **Formality capture.** Letting `F` stand in for closure or articulation. Publish those facets explicitly.
- **Bundle inflation.** Turning `U.LanguageStateFacetProfile` into a second `A.19`. Keep it thin and referential.
- **Opaque readiness.** Using words such as `ready` or `mature` without naming which facet justifies the claim.
- **Route-note capture.** Letting an informative route note behave like move law, gate state, or endpoint ownership. Keep route notes informative and push operative authority back to `A.16`, downstream owners, or gate/work owners.

### C.2.LS:9 - Consequences
The benefit is owner clarity: early cue work, bridge annotations, and reopen moves can all talk about one explicit facet profile. The trade-off is more explicit profile authoring and threshold publication.

### C.2.LS:10 - Rationale
The pattern gives the declared language-state chart over `U.CharacteristicSpace` one stable facet-profile record through which its facet bundle can be published together, while respecting the rest of FPF's owner boundaries.

### C.2.LS:11 - SoTA-Echoing

**SoTA note.** This section does not mint a second rule layer. It is a load-bearing alignment surface: the Solution, Conformance Checklist, and boundary discipline of this pattern must match the stance stated here or explicitly justify divergence.

**Traditions covered.** This pattern binds itself to architecture-description governance, model-based systems engineering, and governance/profile discipline.

| Claim need | SoTA practice (post-2015) | Primary source (post-2015) | Alignment with `C.2.LS` | Adoption status |
|---|---|---|---|---|
| Multi-facet state should be published through explicit profile elements rather than one summary stage label. | Contemporary architecture-description practice keeps the relevant properties, views, and correspondence burden explicit instead of replacing them with one reader-facing maturity word. | ISO/IEC/IEEE 42010:2022 | `C.2.LS` adopts this by requiring explicit facet refs and by rejecting profile-by-vibe labels such as `ready` or `raw` when the bundle matters operationally. | **Adopt.** |
| Complex technical state is better captured through typed properties and decomposable profiles than one lifecycle rail. | Recent MBSE practice favours explicit properties, viewpoints, and cross-view consistency over one implicit staircase of readiness. | OMG SysML v2 (2025) | `C.2.LS` adapts this into a thin facet-profile bundle whose members remain decomposable and whose thresholds stay tied to named facets. | **Adapt.** |
| Governance-facing readiness should stay scoped and profile-based, not collapse into one global adjective. | Current governance frameworks use explicit profiles, scoped conditions, and local thresholds rather than one blanket readiness label. | NIST AI RMF 1.0 (2023) | `C.2.LS` adopts profile-level threshold publication and rejects the popular shortcut where one polished profile label substitutes for explicit facet talk. | **Adopt/Reject-popular-shortcut.** |

**Architecture-description governance.** `C.2.LS` adopts the discipline that useful state publication should keep the relevant profile elements explicit rather than hiding them inside one summary label.

**MBSE and profile discipline.** `C.2.LS` adapts typed multi-property state publication into a thin, decomposable language-state facet bundle rather than one master scale.

**Local stance.** The load-bearing SoTA claim for this pattern is narrow: best-known current practice treats language-state publication as a small explicit facet profile with local thresholds and decomposable readings, not as one maturity adjective or one route-coloured bundle label.

### C.2.LS:12 - Relations
- Builds on: `A.18`, `A.19`, `C.2.2a`, `C.2.3`.
- Coordinates with: `C.2.4`, `C.2.5`, `C.2.6`, `C.2.7`, `A.16.0`, `A.16`, `A.16.1`, `A.16.2`, `B.4.1`, `B.5.2.0`, `E.18`, `F.9.1`.
- Constrains: language-state threshold publication and profile composition.
### C.2.LS:13 - Worked Examples and Composition Notes

#### C.2.LS:13.1 - Operator-facing early alert
A console alert note may be published with a language-state facet profile such as:

- `F = F2/F3` because the note is structurally controlled but still lightweight;
- `AE = AE2` because candidate anchors are visible but not yet fully relation-shaped;
- `CD = CD1` because several routes remain live;
- `LanguageStateAnchoringMode = AM.OperatorLoop` because the note is directly anchored to operator action;
- `RepresentationFactorBundle = {local, sparse, mixed-symbolic}` because alert text and compact codes coexist.

This example shows why no one facet can replace the others. The note is not `simply early`; it is early in a specific, decomposable way.

#### C.2.LS:13.2 - Research cue before lexical repair
A felt or trace-anchored mismatch cue in an inquiry note may be:

- low `AE`,
- very low `CD`,
- strongly `AM.EmbodiedFelt`,
- and representation-wise mixed because the cue is partly verbal, partly kinesthetic, partly exemplar-based.

That profile explains why the cue should remain in `A.16.1` rather than being forced into `A.6.P` or `B.5.2` immediately.

#### C.2.LS:13.3 - Architecture-description case
A viewpoint-bound note about the adequacy of an architecture description may be moderately high in `F`, moderately high in `AE`, still mid-level in `CD`, document-mediated in `AM`, and strongly symbolic in its representation-factor bundle. The profile keeps description-side adequacy distinct from system-side engineering quality.

#### C.2.LS:13.4 - Same `F`, different profile
Two notes may share the same rough `F` band and still differ sharply in articulation, closure, anchoring, and representation factors. One may be operator-loop anchored and low-closure; another may be document-mediated and comparatively closed. The profile bundle keeps that difference visible instead of letting `F` behave like a master axis.

### C.2.LS:14 - Authoring and Review Guidance

#### C.2.LS:14.1 - For authors
When publishing a language-state facet profile:

1. start from the local authoring problem rather than from a memorized ladder;
2. name the facet refs explicitly;
3. add threshold refs only when a threshold changes routing, repair, or governance;
4. avoid global labels such as "mature", "raw", or "ready" unless the profile decomposition is already visible.

#### C.2.LS:14.2 - For reviewers
A reviewer should ask:

- is any facet silently replaced by `F`?
- is a threshold published on an explicit facet rather than on a poetic surrogate?
- do route or reopen claims actually match the published facet bundle?
- are profile notes genuinely informative, or are they smuggling owner semantics that belong elsewhere?

#### C.2.LS:14.3 - For integrators
Integrators should preserve profile references rather than rephrasing them into local slang. A local alias is acceptable only if the underlying facet docking remains explicit and stable.

### C.2.LS:15 - Extension and Migration Notes

#### C.2.LS:15.1 - Local extension rule
Contexts may extend the profile with local threshold refs, route notes, or additional descriptive aids, but they shall not add a new master facet that collapses the owned set into one summary axis.

#### C.2.LS:15.2 - Migration from surrogate prose
Older prose often says:

- "the episteme is still early",
- "the issue is not mature enough",
- "the note is ready",
- "the cue is still raw".

A conforming migration rewrites such statements into explicit facet talk: which facet is low, which is high, which threshold is or is not met, and which move that fact justifies.

#### C.2.LS:15.3 - Boundary reminder
`U.LanguageStateFacetProfile` is a coordination record. If authors find themselves putting move laws, bridge laws, scale laws, or bundle semantics into the profile itself, they are writing in the wrong owner.
### C.2.LS:16 - Profile Publication Package Discipline

#### C.2.LS:16.1 - Minimal publishable profile package
A publishable `U.LanguageStateFacetProfile` should normally carry:

- the declared facet refs for `AE`, `CD`, `LanguageStateAnchoringMode`, and `LanguageStateRepresentationFactorBundle`;
- any threshold refs that materially affect routing, repair, bridge interpretation, or review burden;
- the local relation to `F` when readers might otherwise treat `F` as a surrogate;
- any omission note when a facet is intentionally unpublished, unknown, or locally irrelevant.

One-line publication is lawful only if facet ownership remains legible.

#### C.2.LS:16.2 - Partial-profile rule
A partial profile is lawful only when omission is explicit. Publishing `AE` and `CD` while deferring `LanguageStateAnchoringMode` is acceptable; silently omitting it and then speaking in scalar prose such as "early" or "ready" is not.

If only one facet is published, either explain why the others are not owned in the current note or point to the note where they are already published.

#### C.2.LS:16.3 - Overlay discipline
Local overlays such as "explicit-but-open", "trace-heavy", or "operator-tight" are lawful only when they dock to explicit facet refs. Overlays remain secondary to the owned profile and must not replace the facet bundle.

### C.2.LS:17 - Cross-Facet Reading Law

#### C.2.LS:17.1 - No master-facet reading
Do not infer the whole language-state profile from one facet. High `AE` does not entail high `CD`; strong `AM.OperatorLoop` does not fix `AE` or `CD`; symbolic representation does not entail high `F`; low `CD` does not imply low operational consequence.

#### C.2.LS:17.2 - Threshold interaction rule
When a threshold is expressed over one facet, say whether the other facets are merely informative or also constraining. A Context may allow entry into `B.5.2.0` once `AE` suffices for an explicit open question while still capping `CD` so rival answers remain live; it may allow entry into `A.6.P` at `AE3+` while still capping `CD` so the move remains exploratory rather than endpoint-binding.

#### C.2.LS:17.3 - Transition reading rule
Read profile transitions facetwise. A note may become more explicit without becoming more closed, more document-mediated without changing closure, or more symbolic without becoming more formal. `A.16`, `A.16.1`, `A.16.2`, `B.4.1`, and `B.5.2.0` should therefore cite the facet transition that actually justifies the move.

### C.2.LS:18 - Review Matrix and Migration Tests

#### C.2.LS:18.1 - Review matrix
A reviewer should ask:

- is each published facet owned by its proper pattern rather than by surrogate prose;
- does any overlay smuggle a hidden scalar or gate decision;
- are threshold claims tied to the facet that really bears them;
- do cited moves in `A.16`, `A.16.1`, `A.16.2`, `B.4.1`, or `B.5.2.0` actually match the facet bundle;
- if the profile crosses a bridge or viewpoint boundary, are stance and loss notes kept in `F.9` or `F.9.1` rather than imported as fake facets.

#### C.2.LS:18.2 - Migration test for old prose
Legacy phrases such as "still immature", "not ready yet", or "already stable enough" should be unpacked into: which facet is claimed, which anchor or bundle member justifies it, which threshold or route consequence follows, and which owner carries that consequence.

#### C.2.LS:18.3 - Comparative profile use
Compare profiles facetwise unless a Context has published an explicit local aggregation for reporting. Such an aggregation remains secondary and must not replace the profile in norms, thresholds, or bridge claims.

### C.2.LS:End

