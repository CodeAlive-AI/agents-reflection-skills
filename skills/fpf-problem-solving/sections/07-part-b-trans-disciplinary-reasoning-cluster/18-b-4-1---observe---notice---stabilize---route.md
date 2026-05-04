## B.4.1 - Observe -> Notice -> Stabilize -> Route

> **Type:** Architectural (A)
> **Status:** Draft
> **Normativity:** Normative unless marked informative

**Plain-name.** Observe-to-route seam.

### B.4.1:1 - Problem frame
Observation rarely yields a ready anomaly, action invitation, or hypothesis in one step. Between weak cue preservation and later endpoint ownership, the cluster needs one explicit route-bearing seam that can publish route plurality or route selection without pretending that the cue already belongs to a later owner.

That seam begins **after** `U.PreArticulationCuePack`. Cue preservation may exist before routing. `B.4.1` begins only when route publication itself becomes worth making explicit.

### B.4.1:2 - Problem
Without a pre-abductive seam, early cue publications are either lost, prematurely forced into late forms such as `AnomalyStatement`, `Characteristic`, `ActionOption`, or requirement language, or they smuggle route selection into cue-pack prose with no explicit route owner.

### B.4.1:3 - Forces
| Force | Tension |
|---|---|
| **Early capture vs endpoint discipline** | Preserve weak cues without collapsing route discipline. |
| **Plural route set vs explicit selection** | Permit multiple candidate routes while still requiring an explicit selection record when selection occurs. |
| **Seam clarity vs new-type inflation** | Add a real seam without creating an uncontrolled zoo of new publication kinds. |
| **Form vs face precision** | Keep route-bearing publication form distinct from the MVPK face on which it is rendered. |

### B.4.1:4 - Solution
Insert a pre-abductive route-bearing seam inside the language-state cluster, between observation/cue preservation and later endpoint-entry patterns:

`Observe -> Notice -> Stabilize -> Route`

The seam yields a `RoutedCueSet`, normally downstream of `U.PreArticulationCuePack`.

#### B.4.1:4.1 - `RoutedCueSet` shape
A conforming routed cue set may publish:

- `sourceCuePackRef`
- `candidateRouteSet`
- `routeDecision?`
- `selectedRoute?`
- `routeRationale?`
- `routeAuthorityState?`
- `multiRoutePolicy?`
- `publicationFaceRefs?`
- `articulationThresholdStatus?`
- `closureStatus?`
- `scope?`
- `GammaTime?`

`RoutedCueSet` is not itself the late endpoint. `articulationThresholdStatus` and `closureStatus` report guard state only; their ownership remains with `C.2.4` and `C.2.5`, and route discrimination may additionally cite `C.2.6` or `C.2.7` when anchoring or representation-factor differences are load-bearing.

`candidateRouteSet` and `routeDecision` are the load-bearing core here. `selectedRoute`, `routeRationale`, and `routeAuthorityState` belong here when route selection is explicit. They do **not** belong in `U.PreArticulationCuePack`.

`publicationFaceRefs` names MVPK faces only when face typing matters for publication or review. Faces are renderings of the routed cue set or of later typed projection publications; they are not the route-bearing form itself.

A multi-route `RoutedCueSet` is still one governed member. A lineage fork appears only after distinct successor publications are issued.

#### B.4.1:4.2 - Starter route family
The candidate route set may contain, among others:

- `EvaluativeRoute`
- `ActionInvitationRoute`
- `ProblemAbductionRoute`
- `MethodWorkRoute`
- `RequirementCommitmentRoute`

Contexts may refine the route family locally, but they shall keep the distinction between early route publication and endpoint ownership.

#### B.4.1:4.3 - Projection discipline
Here `projection` names route-bounded partialization, not a rival owner and not a face kind. The resulting publication must be a **typed publication form** rendered, when needed, on an existing MVPK face.

A routed cue set may therefore lead to:

- `U.AbductivePrompt` under `B.5.2.0`,
- a later typed endpoint-entry publication under `A.6.P`, `A.6.A`, or `A.6.Q`,
- or another explicitly typed upstream projection publication.

If no typed downstream publication form can yet be named honestly, stay in `RoutedCueSet` rather than hiding a pseudo-form behind face language.

### B.4.1:5 - Archetypal Grounding
**Tell.** Observation alone is not yet routing. A route requires at least a stabilized cue plus a declared candidate route set.

**Show (System).** An operator alarm may route toward intervention, rollback, or anomaly investigation without yet becoming work or a requirement.

**Show (Episteme).** An inquiry cue about a model-vs-observation discrepancy may route toward anomaly framing, opportunity framing, or probe design before a hypothesis exists.

### B.4.1:6 - Bias-Annotation
The pattern favors preserving weak cues and publishing route plurality explicitly. The counter-bias is explicit as well: routing must still state why one route is live and why one route was selected if selection occurred.

### B.4.1:7 - Conformance Checklist
- `CC-B.4.1-1` Observe output **SHALL NOT** be forced directly into `AnomalyStatement` when articulation threshold is not yet met.
- `CC-B.4.1-2` A routed cue set **SHALL** name its `candidateRouteSet`.
- `CC-B.4.1-3` When route selection occurs, `routeDecision`, `selectedRoute`, and `routeRationale` **SHALL** be explicit.
- `CC-B.4.1-4` `publicationFaceRefs` **MAY** be named, but route-bearing form and publication face **SHALL NOT** be collapsed.
- `CC-B.4.1-5` `RoutedCueSet` **SHALL NOT** silently masquerade as a late endpoint owner.

### B.4.1:8 - Common Anti-Patterns and How to Avoid Them
- **Anomaly inflation.** Treat every early cue as already an anomaly statement.
- **Cue-pack route smuggling.** Hide route decision or route rationale upstream in `U.PreArticulationCuePack`.
- **False single-route certainty.** Pretend one route is obvious when multiple candidate routes are still live.
- **Projection capture.** Treat a typed downstream projection publication or its MVPK face as if it already owned the endpoint family.

### B.4.1:9 - Consequences
The benefit is a lawful early seam for language-state trajectories and a cleaner bridge from cue preservation to later patterns. The trade-off is one more explicit publication form and one more explicit route declaration.

### B.4.1:10 - Rationale
`B.4.1` provides the route-bearing seam between cue preservation and later endpoint or abductive entry. It keeps route publication explicit without forcing cue packs to become route records.

### B.4.1:11 - SoTA-Echoing
This matches practice in incident triage, exploratory design, model probing, and embodied cue work, where routing follows stabilization rather than appearing fully formed at first observation.

### B.4.1:12 - Relations
- Builds on: `B.4`, `C.2.2a`, `A.16`, `A.16.1`, `C.2.LS`.
- Coordinates with: `A.16.0`, `C.2.4`, `C.2.5`, `C.2.6`, `C.2.7`, `B.5.2.0`, `B.5.2`, `A.6.P`, `A.6.A`, `A.6.Q`, `A.15`, `F.9.1`.
- Constrains: pre-abductive route publication.

### B.4.1:13 - Worked Route Sets

#### B.4.1:13.1 - Multi-route operator case
An operator alert note about a service disturbance may lawfully publish a route set containing:

- `ActionInvitationRoute`,
- `ProblemAbductionRoute`,
- and `RequirementCommitmentRoute`.

At this stage the point is not to collapse the routes into one winner, but to keep the plurality explicit until a selected route is justified.

#### B.4.1:13.2 - Inquiry case
A conceptual mismatch may route simultaneously toward:

- explanatory inquiry,
- probe design,
- and later lexical repair.

This is lawful only if the route rationale makes the plurality explicit rather than hiding it under vague prose.

#### B.4.1:13.3 - Invalid direct jump
It is invalid to treat a routed cue set as if it were already a hypothesis, a gate, or a work plan. It is a route-bearing publication form, not the endpoint owner.

### B.4.1:14 - Authoring and Review Guidance

#### B.4.1:14.1 - Author prompt
A routed cue set should say:

- where the cue came from,
- which routes are live,
- whether route selection has occurred,
- why one route was selected if a selection occurred,
- what typed downstream publication, if any, is now lawful.

#### B.4.1:14.2 - Review prompt
A reviewer should check whether the selected route is justified by the published cue pack and whether suppressed alternative routes were genuinely considered rather than silently erased.

#### B.4.1:14.3 - Threshold reminder
If the articulation threshold is not met, the routed cue set should keep the publication early rather than laundering it into a late endpoint form.

### B.4.1:15 - Migration and Boundary Notes

#### B.4.1:15.1 - Migration from anomaly-first prose
Older anomaly-first language should be migrated into route publication when the publication is not yet strong enough for anomaly ownership.

#### B.4.1:15.2 - Boundary reminder
`B.4.1` owns route publication, not abductive reasoning, lexical repair, deontic commitment, or work execution. Those belong to later owners.

### B.4.1:16 - Route-Set Package Discipline

A routed cue set is strongest when it makes route plurality, route grounds, and current authority explicit.

#### B.4.1:16.1 - Minimal route package
A robust route package should identify:

- the **originating cue pack**,
- the **candidate route set**,
- the **route decision state**,
- the **selected route**, if any,
- the **grounds for each live route**,
- the **conditions that would change route ranking**,
- and any **typed downstream publication** already published.

This is enough to keep later handoff reviewable without collapsing the seam into an endpoint owner.

#### B.4.1:16.2 - Selected route is not endpoint ownership
Even when one route is selected, the routed cue set remains a seam publication form until a later owner is entered explicitly.

#### B.4.1:16.3 - Deferred selection
Deferral is lawful when route plurality and missing discriminators are published. It is not lawful when one route is silently assumed while the publication still speaks as if the question were open.

### B.4.1:17 - Route Selection and Branch Law

#### B.4.1:17.1 - Selecting one route
Route selection should be driven by published cue grounds, not by convenience. A selected route should therefore cite the stabilizing anchors, route rationale, and any threshold conditions that make later handoff lawful.

#### B.4.1:17.2 - Keeping several routes live
Some cues are genuinely multi-routable. In those cases, the point of `B.4.1` is not to force premature convergence but to keep the route set legible until later owners can discriminate more sharply.

#### B.4.1:17.3 - Multi-route state versus lineage fork
One routed cue set may keep several candidate routes live without yet forking lineage. A fork occurs only when distinct successor publications are actually issued and acquire their own authority, losses, or handoff semantics.

#### B.4.1:17.4 - Route splitting
One cue cluster may split into several routed cue sets if different sub-cues support different destinations. The split should be published explicitly so that later readers do not assume that one route exhausted the whole original cue complex.

### B.4.1:18 - Worked Seam Cases and Review Tests

#### B.4.1:18.1 - Intervention vs inquiry split
An operator-facing disturbance may legitimately support both:

- an immediate intervention-oriented route,
- and a slower explanatory route.

`B.4.1` preserves both without forcing one to swallow the other.

#### B.4.1:18.2 - Requirement-route overreach
A route set that includes `RequirementCommitmentRoute` should not be read as if the requirement already exists. Reviewers should ask whether a requirement owner has actually been entered or whether the route is merely one lawful continuation among others.

#### B.4.1:18.3 - Review test for false single-route certainty
A reviewer should ask: if the selected route were denied, would the publication still contain enough information to explain the other live routes? If not, the route set is likely under-published and has collapsed too early into one favored continuation.

### B.4.1:19 - Boundary to Later Owners

The routed cue set exists to make later owner entry cleaner, not to delay it indefinitely.

Typical next-owner conditions are:

- explicit evaluative family selection for `A.6.Q`,
- explicit action-oriented family selection for `A.6.A`,
- explicit prompt question for `B.5.2.0`,
- explicit requirement or commitment head for requirement-facing owners,
- or explicit method/work hook for `A.15`-side use.

If none of those next-owner conditions can yet be stated, the governed publication likely still belongs in the seam. If they can already be stated, `B.4.1` should not remain a holding form for a publication that has already crossed the threshold.

### B.4.1:20 - Route Evidence and Discrimination Package

#### B.4.1:20.1 - Evidence-per-route rule
Each live route in a routed cue set should cite the cue grounds that actually support it. If a route has no published grounds, it is not a live route; it is only a private guess.

#### B.4.1:20.2 - Discriminator publication
When a route set remains plural, authors should name the discriminator they are waiting for: a missing anchor, contrast, measurement, witness, articulation threshold, closure condition, or other explicit facet transition. Doing so makes deferred selection informative instead of merely indecisive.

#### B.4.1:20.3 - Projection restraint
A typed downstream projection publication or prompt may be shown as one lawful continuation, but it shall not dominate the routed cue set so strongly that the other routes become unreadable. Projection is guidance, not covert owner replacement.
### B.4.1:End


