## A.16.0 - `U.LanguageStateTransductionTrajectory` - Optional trajectory-account normal form over the language-state `U.CharacteristicSpace`

> **Type:** Architectural (A)
> **Status:** Draft
> **Normativity:** Normative unless marked informative

**Plain-name.** Language-state transduction trajectory.

**Builds on.**
`C.2.2a`, `A.16`, `A.19`, `E.17`, `E.18`, `E.10`, `F.18`.

**Used by.**
`A.16.1`, `A.16.2`, `B.4.1`, `B.5.2.0`, `A.6.P`, `A.6.Q`, `A.6.A`, `F.9.1`, `E.17.1`.

### A.16.0:1 - Problem frame
In engineering, inquiry, operator, and management practice, teams sometimes need more than a local move note. When branch structure, supersession, retirement, handoff, bridge-sensitive loss, or multi-step owner change matters, readers need one place where the history of successive governed `U.Episteme` publications is made explicit.

Cue packs, routed cue sets, abductive prompts, typed route-bounded projection publications, partial normal forms, and later endpoint-bound records are publication forms that may appear in that history. They are not the raw disturbances, telemetry traces, model outputs, bodily tensions, or carrier documents that ground it.

What must remain intelligible is therefore not a myth that one unchanged object literally `moves`. What must remain intelligible is a lineage of successive governed `U.Episteme` publications, together with the load-bearing links among them, when that history itself has governance value.

### A.16.0:2 - Problem
Without an explicit trajectory-account pattern for those heavier cases:

1. history is mistaken for generic workflow rather than for governed transduction over a declared language-state `U.CharacteristicSpace`;
2. early seam publications are confused with endpoint-owned forms;
3. forks, merges, route retirement, supersession, and route-sensitive loss become implicit and unverifiable;
4. every local move is either over-wrapped in ad hoc history prose or under-wrapped in a way that hides handoff and authority change;
5. bridge and viewpoint docking inherit under-described upstream history.

### A.16.0:3 - Forces
| Force | Tension |
| --- | --- |
| **History value vs wrapper inflation** | Publish lineage only when it matters, without making trajectory accounts mandatory around every lawful move. |
| **Lineage fidelity vs readable publication** | Trajectory history must stay branch-aware without becoming unreadable bookkeeping. |
| **Seam usefulness vs endpoint discipline** | Upstream publications must be useful while remaining visibly upstream of endpoint ownership. |
| **Account clarity vs owner boundaries** | The trajectory pattern must explain heavy-history cases without taking over `A.19`, `A.16`, `E.17`, `E.18`, or endpoint semantics. |
| **Local transduction vs bridge entry** | The same trajectory may later cross viewpoint or context boundaries, but that crossing does not redefine the local trajectory owner. |

### A.16.0:4 - Solution
`U.LanguageStateTransductionTrajectory` is the **optional** trajectory-account normal form that records how successive governed `U.Episteme` publications are linked across position claims in the declared language-state `U.CharacteristicSpace` chart named in `C.2.2a`.

It does **not** define position semantics, move legality, or publication-face ontology by itself. Those remain with `C.2.2a` / `A.19`, `A.16`, and `E.17` / `E.18` respectively.

It answers the question: `when history itself matters, which governed publication is current, which members precede or branch from it, which lawful moves relate them, which publication forms carry them, what was lost, and who now owns the next responsibility?`

#### A.16.0:4.1 - Ontological subject and role lanes
In this cluster, keep six roles distinct:

- **current governed member** - the current `U.Episteme` publication under language-state governance;
- **lineage links** - explicit `derivedFrom`, `supersedes`, `forkedFrom`, `mergedFrom`, and retirement / no-successor links among governed members;
- **grounds / witnesses** - service disturbances, model-vs-observation discrepancies, traces, model outputs, bodily tensions, contrasts, or exemplars that justify the history;
- **publication forms** - cue packs, routed cue sets, prompt forms, typed route-bounded projection publications, partial normal forms, and endpoint-owned records through which lineage members are published;
- **publication faces** - the existing MVPK faces on which those publication forms are rendered when face typing matters;
- **carriers** - documents, console notes, cards, trace files, or model artefacts that hold or render those publications.

A multi-route state inside one current governed member is **not** yet a lineage fork. It becomes a fork only when distinct successor members are published and given their own authority, losses, or handoff semantics.

A trajectory step may add a new lineage member, revise the current member, or relate several members through fork, merge, supersession, or retirement. It does **not** mean that the source phenomenon itself has moved through the language-state chart.

#### A.16.0:4.2 - Position-account discipline
The position read by this pattern is the slot-explicit claim defined in `C.2.2a`: a partial coordinate publication in the declared language-state `U.CharacteristicSpace`, where each basis slot publishes a `ValueSet(slot)`, interval, or other admissible set-valued claim.

Early seam publications may leave some slots unknown or wide. That uncertainty is lawful only if it is explicit. A trajectory account therefore records the position claims of the current lineage member and, when needed, of the predecessor or sibling members that justify the move reading.

#### A.16.0:4.3 - Use threshold and core trajectory record
A single local `A.16` move note is sufficient when no load-bearing branch, loss, handoff, or supersession structure needs publication.

Use `U.LanguageStateTransductionTrajectory` when at least one of the following is load-bearing:

- derivation, supersession, fork, merge, or retirement structure;
- multi-step loss notes or reopen conditions that would be hidden by a compressed move note;
- responsibility handoff whose legitimacy depends on upstream history;
- bridge or viewpoint entry that depends on upstream route, loss, or lineage structure.

A conforming trajectory account then keeps at least the following explicit:

- the current governed member;
- predecessor, sibling, or ancestor references when the current reading depends on lineage structure;
- the lineage link kind (`derivedFrom`, `supersedes`, `forkedFrom`, `mergedFrom`, `retiredWithSuccessor`, `retiredWithoutSuccessor`, or another explicitly typed link);
- the current position claim and any load-bearing predecessor position claims;
- the typed move or move sequence that relates them;
- the publication form currently carrying the governed member and, if it matters, the MVPK face carrying that form;
- the next intended owner or handoff state;
- any loss note, reopen condition, branch-specific authority note, or bridge-sensitive note that matters.

#### A.16.0:4.4 - Recorded move-family discipline
`U.LanguageStateTransductionTrajectory` records the governed `A.16` move family: `notice`, `stabilize`, `route`, `projection`, `formalize`, `operationalize`, `reopen`, `sketchBackoff`, `respecify`, and `retire`.

The point is not that every account uses every move. The point is that forward movement, retreat, reframing, and explicit retirement belong to one governed family when that history is worth publishing.

Detailed move guards remain with `A.16`. `A.16.0` records their use; it does not own them.

#### A.16.0:4.5 - Seam publication and face discipline
A trajectory account may refer to seam publications that remain upstream of endpoint ownership. In the current cluster these include:

- `U.PreArticulationCuePack`;
- `RoutedCueSet`;
- `U.AbductivePrompt`;
- partial normal forms already typed elsewhere;
- other explicitly typed upstream publications that preserve non-endpoint status.

These are not a second publication-face ladder. They are typed publication forms rendered, when necessary, on existing MVPK faces under `E.17`.

Untyped placeholders such as "route-bounded publication face" are non-conformant in a trajectory account unless the text also names the actual publication form and, separately, the MVPK face if face typing matters.

#### A.16.0:4.6 - Endpoint docking and responsibility handoff
A trajectory does not need to terminate in order to be useful. What matters is a visible docking milestone or responsibility handoff into an owner that is allowed to take the next contract.

Typical docking owners include:

- `A.6.P` for relation repair forms;
- `A.6.A` for action-invitation forms;
- `A.6.Q` for evaluative repair forms;
- `B.5.2` for later abductive work;
- `A.15` for method / work-facing forms;
- `C.25` for endpoint bundle structures.

A trajectory account should therefore name not only the docking owner but also the owned publication or record that now carries the next contract. Naming only the owner under-publishes the handoff.

After such a handoff, monitoring, maintenance, revisit, or later re-entry may continue through new lineage members or later trajectories. The pattern therefore distinguishes `lineage continuity` from `current owner responsibility`.

#### A.16.0:4.7 - Effect-free moves versus work-requiring crossings
Some `formalize` and `operationalize` steps are effect-free epistemic transformations: rewriting, slot-explicit articulation, route-bounded partialization, view retargeting, or normal-form strengthening over already available grounds.

Other steps require new measurements, experiments, instrumentation, execution, or other `U.Work`. When that happens, the trajectory account shall publish the crossing or handoff explicitly rather than pretending that world-facing work occurred inside the language layer. `A.16.0` records that the crossing was required; the relevant work, gate, or endpoint owner records the world step itself.

#### A.16.0:4.8 - Relation to `A.16` and `E.18`
`U.LanguageStateTransductionTrajectory` is not an `E.18` path publication object, and `A.16.0` does **not** own the semantics of language-state movement.

- `A.19` plus `C.2.2a` own the declared characteristic-space reading of positions;
- `A.16` owns move kinds and move guards;
- `E.17` / `E.18` own publication-face discipline and graph-level path publication;
- endpoint owners own endpoint-local contracts.

`A.16.0` standardizes only the heavier history package for cases where that package is itself worth publication.

#### A.16.0:4.9 - Bridge and viewpoint entry
A trajectory may later cross a viewpoint or context boundary. When that happens:

- bridge substitution licence remains with `F.9`;
- stance overlays remain with `F.9.1`;
- viewpoint reuse remains with `E.17.1`;
- endpoint-local semantics remain with their endpoint owners.

`A.16.0` only makes those entry points explicit so that later attachments do not float without an upstream history account.

### A.16.0:5 - Archetypal Grounding
**Tell.** A language-state trajectory account is not `we kept refining the note`. It is an optional, lineage-aware account of successive `U.Episteme` publications, with declared position claims, move kinds, publication forms, losses, and next owners.

**Show (System).** A service disturbance is a system-side phenomenon, not the trajectory subject. It grounds an alerting episteme lineage. One stabilized cue pack may first keep two routes live in one `RoutedCueSet`; only later, if two distinct successor publications are actually issued, does the lineage fork.

**Show (Episteme).** A model-vs-observation discrepancy is a witness-level tension, not the occupant itself. Once preserved as a cue pack, the governed lineage may project into a typed prompt publication on one branch and later formalize on another, or it may reopen and retire one branch if the provisional route proves unsupported.

### A.16.0:6 - Bias-Annotation
The pattern biases authors toward lineage-aware history accounts rather than stage stories about one magically maturing object. That bias is intentional when branch, loss, or handoff semantics matter. The counter-bias is equally intentional: do **not** publish a trajectory account when a local move note already suffices.

### A.16.0:7 - Conformance Checklist
- `CC-A.16.0-1` `U.LanguageStateTransductionTrajectory` **SHALL NOT** be treated as mandatory wrapper syntax around every `A.16` move.
- `CC-A.16.0-2` A language-state trajectory account **SHALL** identify the current governed `U.Episteme` publication and **SHALL NOT** collapse grounds, publication forms, publication faces, carriers, and governed members into one unnamed moving thing.
- `CC-A.16.0-3` Position claims used in the trajectory **SHALL** be published as slot-explicit claims in the declared language-state `U.CharacteristicSpace`, not as folk stage labels.
- `CC-A.16.0-4` Fork, merge, supersession, derivation, and retirement **SHALL** be made explicit whenever the account depends on them.
- `CC-A.16.0-5` Publication form and MVPK face **SHALL NOT** be collapsed, and untyped seam placeholders **SHALL NOT** substitute for typed publication forms.
- `CC-A.16.0-6` `projection` **SHALL** be read as route-bounded partialization with visible loss notes and a lawful reopen path.
- `CC-A.16.0-7` Work-requiring `formalize` or `operationalize` steps **SHALL** expose the relevant crossing or handoff rather than pretending that `U.Work` occurred inside the language layer.
- `CC-A.16.0-8` When graph-level path publication is needed, authors **SHOULD** reuse `E.18` rather than inventing a rival path calculus here.

### A.16.0:8 - Common Anti-Patterns and How to Avoid Them
- **Meta-wrapper inflation.** Treat `A.16.0` as obligatory around every move. Repair by publishing a local `A.16` move note unless history itself has governance value.
- **One-object myth.** Treat one frozen episteme as literally moving unchanged. Repair by publishing lineage members and their links.
- **Owner/form collapse.** Treat later owners as if they were publication forms. Repair by naming the owned form and the owner separately.
- **Form/face collapse.** Treat seam publications as if they minted a second MVPK face family. Repair by naming form and face separately.
- **Multi-route/fork collapse.** Treat several live routes in one governed member as if they were already several successor members.
- **Hidden work crossing.** Describe operationalization as purely linguistic when it actually required new world-facing work. Repair by publishing the crossing explicitly.

### A.16.0:9 - Consequences
The benefit is that heavy-history language-state movement becomes lineage-aware, reviewable, and dockable without premature endpoint capture or metonymic collapse. The trade-off is more explicit publication of position claims, lineage links, move kinds, loss notes, and handoffs when history is worth publishing.

### A.16.0:10 - Rationale
Language-state work needs one explicit trajectory-account normal form for the subset of cases where history itself matters. Without that account, readers have to reconstruct lineage, branch structure, retirement, and handoff semantics from fragments. With it overused, every local move becomes over-wrapped. The pattern exists to hold the middle line.

### A.16.0:11 - SoTA-Echoing
The pattern matches contemporary practice in exploratory inquiry, operator-centered incident work, model probing, and structured design iteration: lawful progress sometimes requires visible intermediate publications, branch-aware history, disciplined retreat, and explicit handoffs rather than hidden jumps from cue to endpoint.

### A.16.0:12 - Relations
- Builds on: `C.2.2a`, `A.16`, `A.19`, `E.17`, `E.18`.
- Coordinates with: `C.2.LS`, `A.16.1`, `A.16.2`, `B.4.1`, `B.5.2.0`, `B.5.2`, `A.6.P`, `A.6.Q`, `A.6.A`, `F.9`, `F.9.1`, `E.17.1`.
- Constrains: trajectory-account publication, branch visibility, seam publication reading, docking visibility, and anti-pipeline language across the cluster.

### A.16.0:13 - Worked trajectories

#### A.16.0:13.1 - Multi-route state before fork
A routed operator cue may first publish one governed member with both intervention and inquiry routes live inside one `RoutedCueSet`. That is still one member in a multi-route state. Only if separate successor publications are later issued for those two continuations does the lineage fork.

#### A.16.0:13.2 - Inquiry trajectory with fork
An inquiry cue pack centered on a felt or trace-anchored discrepancy cue may first publish one governed member, then fork into:

- `notice -> stabilize -> route -> projection -> formalize`, with a cue-derived prompt publication carrying the explanatory branch, and
- `notice -> stabilize -> route -> projection -> operationalize`

if one branch supports explanatory work while another supports immediate probe or control work. The branches remain lawful only if the fork is visible and each branch keeps its own loss notes and handoff conditions.

#### A.16.0:13.3 - Operator trajectory with retirement
An operator alert note about a service disturbance may move:

`notice -> stabilize -> route -> projection -> operationalize`

If one route later proves unsupported, the lawful continuation may include explicit retirement of that branch rather than silent disappearance. The retirement does not erase the prior branch; it withdraws authority and preserves continuity explicitly.

#### A.16.0:13.4 - Bridge-sensitive trajectory
A route-bearing comparative note may move through a seam publication and only later dock to a bridge overlay or viewpoint bundle. The bridge or viewpoint attachment does not replace the trajectory account; it annotates or re-expresses a lineage that already exists.

### A.16.0:14 - Trajectory publication package discipline
A publishable trajectory account should normally identify:

- the current governed `U.Episteme` publication;
- predecessor, sibling, or ancestor references when they are load-bearing;
- the lineage link kind;
- the current position claim and any load-bearing predecessor position claims;
- the move or move sequence being asserted;
- the current publication form and, if relevant, the MVPK face carrying it;
- the grounds or witnesses that make the history necessary;
- the next route, docking owner, or retirement state;
- the losses, open rivals, or reopen conditions that matter for continuation.

If these are missing, the publication is usually only lifecycle prose, not a conforming trajectory account.

### A.16.0:15 - Review guidance
A reviewer should ask:

1. Is the author really describing history over the declared language-state `U.CharacteristicSpace`, or only narrating progress informally?
2. Is the current governed member distinct from the grounds, publication form, publication face, and carrier?
3. Is this history heavy enough to justify `A.16.0`, or would a local `A.16` move note have sufficed?
4. Are multi-route state and lineage fork being kept distinct?
5. Are derivation, supersession, fork, merge, or retirement links visible where the reading depends on them?
6. Is the current publication a seam publication or already an endpoint-owned form?
7. If `formalize` or `operationalize` required world-facing work, is the crossing or handoff explicit?

### A.16.0:16 - Boundary notes
`A.16.0` does not replace `C.2.2a` / `A.19` position semantics, `A.16` move guards, `A.16.1` cue-pack semantics, `A.16.2` retreat / retirement semantics, `B.4.1` seam entry routing, `B.5.2.0` abductive prompt species, `E.17` face typing, `E.18` path publication, or any endpoint-local repair logic.

Its job is narrower and architectural: to make the heavier trajectory account visible only where lineage, branch, loss, retreat, retirement, and handoff need to be published as one intelligible package.
### A.16.0:End

