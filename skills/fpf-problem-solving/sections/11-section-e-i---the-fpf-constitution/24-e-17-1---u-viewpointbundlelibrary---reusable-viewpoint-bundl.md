## E.17.1 - `U.ViewpointBundleLibrary` - Reusable Viewpoint Bundles

> **Type:** Architectural (A)
> **Status:** Stable
> **Normativity:** Normative unless marked informative

**Plain-name.** Viewpoint bundle library.

**Builds on.**
`A.6.2-A.6.4` (episteme morphism classes), `A.6.5 U.RelationSlotDiscipline`, `A.7`, `E.7`, `E.10`, `E.10.D1`, `E.10.D2`, `E.17.0 U.MultiViewDescribing`.

**Used by.**
`E.17.2` (TEVB engineering viewpoint bundles), `E.18:5.12`, and domain-specific viewpoint families for architecture, governance, safety, research, or assurance.

### E.17.1:1 - Problem frame

`U.MultiViewDescribing` lets a description family state that one entity-of-interest is rendered through several viewpoints with declared correspondences. In practice many such viewpoint families recur across projects and schools: engineering teams reuse functional / procedural / structural / interface viewpoints; governance teams reuse risk / control / compliance / operations viewpoints; research teams reuse theory / experiment / inference / limitation viewpoints.

FPF therefore needs one explicit owner for reusable viewpoint families so that authors can import them, name them stably, review them once, and keep intensional viewpoint identity separate from document labels and publication surfaces.

### E.17.1:2 - Problem

Without a viewpoint-bundle library pattern:

1. **Each domain invents local viewpoint families.**
   Similar families reappear under slightly different labels, but no stable owner records whether the underlying viewpoints are actually the same.
2. **Viewpoint identity drifts.**
   A family called `functional`, `capability`, or `operational` may differ only lexically, or may differ semantically, but there is no disciplined place to tell which is which.
3. **`U.MultiViewDescribing` cannot reuse a family cleanly.**
   Every instance must restate its finite viewpoint family locally instead of importing an existing bundle.
4. **ISO 42010-style viewpoint libraries remain external.**
   FPF lacks a native place where reusable viewpoint libraries can be expressed as first-class, reviewable objects.
5. **Surface labels leak into semantics.**
   Authors reuse the same name for viewpoints, views, publication faces, or folders, and the intensional object boundary becomes unclear.

### E.17.1:3 - Forces

| Force | Tension |
|---|---|
| **Reuse vs local fit** | Authors want reusable viewpoint families, but a local project may still need a subset or a context-specific extension. |
| **Stable identity vs evolution** | Bundles must stay stable enough for long-term reuse while still admitting editioned change. |
| **Intensional clarity vs surface convenience** | Viewpoint bundles are intensional catalogue objects, yet teams often prefer one surface label for many layers. |
| **Engineering vs publication discipline** | Engineering viewpoints and publication viewpoints both matter, but they must not collapse into one id namespace. |
| **Rich libraries vs cognitive economy** | A library should be rich enough for real reuse without becoming so large that authors cannot choose from it coherently. |

### E.17.1:4 - Solution - `U.ViewpointBundleLibrary`

`E.17.1` introduces `U.ViewpointBundleLibrary` as the architectural home for reusable viewpoint families. The library is a catalogue object: it packages named bundles of `U.Viewpoint` values and related metadata, but it does not define new kernel episteme kinds, new surfaces, or new publication carriers.

#### E.17.1:4.1 - Core role

A conforming viewpoint-bundle library makes three things explicit:

- **which family is being named,** via `ViewFamilyId`;
- **which `U.Viewpoint` values belong to that family;**
- **under what entity-of-interest class and edition discipline** the family is valid.

This lets `U.MultiViewDescribing` import a finite viewpoint family from a stable owner instead of restating it ad hoc in every local description family.

#### E.17.1:4.2 - `U.ViewpointBundleLibrary` (library object)

A `U.ViewpointBundleLibrary` is a catalogue of viewpoint bundles with at least:

- `libraryId : LibraryId`
- `editionId : EditionId`
- `bundles : FinSet(U.ViewpointBundle)`
- optional governance metadata such as owner, change-control note, or scope tags

Normative constraints:

1. Within one library edition, each `ViewFamilyId` **SHALL** be unique.
2. Libraries **SHALL NOT** define new kernel episteme kinds or surface kinds.
3. Libraries **MAY** be specialized as core FPF libraries or organization-local extensions that preserve the same bundle discipline.

#### E.17.1:4.3 - `U.ViewpointBundle` and `ViewFamilyId`

A `U.ViewpointBundle` is a finite, non-empty family of compatible `U.Viewpoint` values packaged for reuse.

Minimal structure:

- `viewFamilyId : ViewFamilyId`
- `EoIClassSpec <: U.Entity`
- `viewpoints : FinSet(U.Viewpoint)`
- optional `ArchetypalCards : FinSet(U.ArchetypalGroundingRef)`
- optional `AlignmentNotes` for ISO 42010 or domain-standard correspondences
- optional typed annex references for lexical, bridge, routing, example, or SoTA support material

`ViewFamilyId` names the bundle. It does **not** name a `U.View`, a publication face, or a file-system surface.

#### E.17.1:4.4 - Import discipline into `U.MultiViewDescribing`

When a `U.MultiViewDescribing[EoIClass]` family declares a `ViewFamilyId`:

- its finite viewpoint family `Sigma` **SHALL** be a subset of the referenced bundle's `viewpoints`;
- every D/S episteme in the family **SHALL** use `viewpointRef` values drawn from that imported family;
- every associated `U.View` **SHALL** preserve viewpoint attribution rather than silently retyping or relabeling the imported viewpoints.

If more than one bundle is used, the family shall make the partition explicit rather than relying on unnamed mixture.

#### E.17.1:4.5 - Guard and naming discipline

- A viewpoint bundle is a family of **viewpoints**, not a bundle of views or documents.
- `ViewFamilyId` is a lexical family id, not a surface kind.
- Engineering viewpoint ids and publication viewpoint ids may coexist, but they **SHALL** remain disambiguated.
- Bundle semantics come from the owned `U.Viewpoint` definitions, not from the spelling pattern of the family id.

### E.17.1:5 - Archetypal Grounding

**Tell.** A viewpoint bundle library lets FPF say "use this already-defined viewpoint family" without confusing that family with the concrete views or publication faces that later realize it.

**Show (System).** A TEVB engineering bundle can define a reusable family such as `VP.Functional`, `VP.Procedural`, `VP.RoleEnactor`, and `VP.ModuleInterface` for holon descriptions. Later `U.MultiViewDescribing` families import that bundle rather than redefining the same engineering viewpoints each time.

**Show (Episteme).** A governance-oriented bundle can package `VP.Risk`, `VP.Control`, `VP.Compliance`, and `VP.Operations` as one reusable family for service or program descriptions. Publication surfaces may later expose that family, but the bundle itself remains an intensional catalogue object, not the report surface.

### E.17.1:6 - Bias-Annotation

The pattern biases FPF toward bundle-first reuse and against ad hoc local re-invention of recurring viewpoint families. That bias is intentional. The small cost of maintaining libraries and editions is lower than the long-term cost of unstable viewpoint identity.

### E.17.1:7 - Conformance Checklist

- `CC-VBL-0` Within one library edition, each `ViewFamilyId` **SHALL** identify exactly one `U.ViewpointBundle`.
- `CC-VBL-1` Every viewpoint in a bundle **SHALL** have `EoIClassSpec` compatible with the bundle's declared `EoIClassSpec`.
- `CC-VBL-2` A `U.MultiViewDescribing` family that declares a `ViewFamilyId` **SHALL** import only viewpoints from the referenced bundle.
- `CC-VBL-3` `ViewFamilyId` **MUST NOT** be used as a `SurfaceKind`, publication-face kind, or carrier kind.
- `CC-VBL-4` Bundles intended for non-expert reuse **SHOULD** provide archetypal grounding coverage for their viewpoints.
- `CC-VBL-5` Changes to bundle membership or meaning **SHALL** be editioned rather than silently mutating an existing family id.
- `CC-VBL-6` If a family combines several bundles, the contributing `ViewFamilyId` values **SHALL** remain explicit.

### E.17.1:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What it looks like | How FPF prevents it |
|---|---|---|
| **Surface hijack** | A `ViewFamilyId` is reused as a publication-face name or document type. | `CC-VBL-3` keeps family ids lexical and bundle-local. |
| **Bundle equals view collection** | A folder or report pack is called a viewpoint bundle even though no `U.Viewpoint` family is declared. | `E.17.1` defines the bundle as an intensional family of viewpoints, not a file grouping. |
| **Silent local drift** | A local project keeps the old family id but swaps in different viewpoints. | `CC-VBL-5` requires editioning for semantic or membership change. |
| **Namespace collapse** | Engineering viewpoint ids and publication viewpoint ids are mixed as if they were one namespace. | The solution keeps id spaces distinct and requires explicit attribution. |

### E.17.1:9 - Consequences

| Benefit | Trade-off / Mitigation |
|---|---|
| **Reusable viewpoint families.** Stable bundle ids let many projects reuse the same family without restating it. | Libraries need governance and edition discipline. |
| **Cleaner `U.MultiViewDescribing`.** A family can import a reviewed bundle instead of spelling out every viewpoint locally. | Local exceptions must be made explicit rather than hidden in prose. |
| **Better architectural alignment.** ISO 42010-style viewpoint-library practice gains a native FPF owner. | Initial bundle authoring requires care in naming and grounding. |
| **Lexical hygiene.** Bundle ids, viewpoint ids, views, and publication surfaces stop collapsing into one label. | Authors must learn the separation once and then keep it. |

### E.17.1:10 - Rationale

`U.MultiViewDescribing` already assumes that viewpoint plurality exists. `E.17.1` supplies the reusable owner for that plurality, including cases where viewpoints are used to re-express positions in `U.LanguageStateSpace` or trajectories in `U.LanguageStateTransductionTrajectory`. Without it, every domain can only improvise locally, and long-term correspondence between viewpoint families remains fragile.

### E.17.1:11 - SoTA-Echoing

The pattern aligns with post-2015 multi-view practice: ISO 42010 viewpoint libraries, model-based systems engineering viewpoint catalogues, assurance-oriented viewpoint families, and reusable concern bundles in architecture and governance work. FPF adopts the reusable-library idea, but keeps the ontology stricter by separating bundle ids, viewpoint ids, views, and publication surfaces.

### E.17.1:12 - Relations
- **Builds on:** `C.2.1` slot discipline through `ViewpointSlot` / `ViewSlot`, `A.6.2-A.6.4`, `A.7`, `E.7`, and `E.10`.
- **Constrains:** `E.17.0 U.MultiViewDescribing` whenever it imports viewpoint families from reusable bundles.
- **Coordinates with:** `C.2.2a`, `A.16.0`, `E.17`, `E.17.2`, `E.18:5.12`, `F.9`, `F.9.1`, and any domain-specific viewpoint family that needs stable reuse.
- **Protects:** lexical and ontological separation between viewpoint families, concrete views, and publication surfaces.
#### E.17.1:12.1 - Typed annex manifests for thin bundles

`VF.*` and other reusable viewpoint bundles may reference typed `AnnexManifestRef` assets with roles such as `lexical`, `bridge`, `routing`, `examples`, optional `sota`, and optional `pilotTrace`. This keeps the bundle itself thin while allowing routing notes, lexical baggage, and bridge annexes to remain explicit and typed rather than folded into the bundle core.


### E.17.1:13 - Bundle Anatomy and Member Discipline

A viewpoint-bundle library becomes thin and reusable only when the bundle itself stays stable while the member viewpoints remain explicit enough to review independently. The bundle therefore has two simultaneous obligations: coherence at the family level and clarity at the member level.

#### E.17.1:13.1 - What a viewpoint member should make explicit

Each member `U.Viewpoint` inside a reusable bundle should make explicit at least:

- the **concern family** it brings into focus,
- the **stakeholder families** for whom that concern matters,
- the **entity-of-interest class** for which it is admissible,
- the **allowed description/specification kinds** that usually realize it,
- and any **bundle-specific conformance or correspondence notes** that later view families should preserve.

`E.17.1` does not redefine the internals of `U.Viewpoint`. It states what must remain visible if a viewpoint is to be reused as part of a bundle rather than as an undocumented local label.

#### E.17.1:13.2 - Bundle-level coherence

A bundle is not just a bag of viewpoints with one shared prefix. A coherent bundle should answer a recognizable family-level question, such as:

- *which engineering concerns are standard for holon description?*
- *which governance perspectives are required for a service review?*
- *which research-method viewpoints recur across inquiry reports?*

If the member viewpoints do not share that family-level purpose, the result is not one bundle but an uncurated catalogue fragment.

#### E.17.1:13.3 - Thin bundles, rich annexes

`E.17.1` intentionally allows bundles to stay thin. Rich supporting material such as:

- lexical discipline notes,
- bridge overlays,
- routing notes,
- worked examples,
- or SoTA references

may live in typed annex manifests. This preserves a stable bundle core while still letting reuse packages carry enough didactic and review support.

### E.17.1:14 - Import, Subset, and Multi-Bundle Coordination

The value of viewpoint bundles appears most clearly when they are imported, subsetted, and coordinated across several reused families. Those cases need explicit discipline so that a local project does not quietly mutate what it claims to be reusing.

#### E.17.1:14.1 - Subset selection

A `U.MultiViewDescribing` family may legitimately import only a subset of a bundle's viewpoints. When it does so, it should declare:

- which `ViewFamilyId` is the source,
- which viewpoint members are actually in local use,
- and whether the omitted members are simply unused or are intentionally excluded because the local scope does not require them.

The local family must not speak as if it had imported the whole bundle while silently dropping inconvenient viewpoints.

#### E.17.1:14.2 - Local overlays vs new bundles

A local project often wants a small adaptation: one extra concern note, one narrower stakeholder emphasis, one local naming convention. `E.17.1` prefers explicit overlays or new editions over silent mutation.

A practical rule is:

- if the local project is merely selecting a subset or adding local didactic material, keep the original bundle id and declare the overlay clearly;
- if the local project changes viewpoint membership or meaning, publish a new local bundle or a new edition.

This is how bundle reuse remains trustworthy across organizations.

#### E.17.1:14.3 - Multi-bundle coordination

Many real description families need more than one bundle, for example:

- one engineering viewpoint family,
- one safety or assurance family,
- and one governance or publication-oriented family.

In such cases, `E.17.1` expects the family to preserve the provenance of each member viewpoint rather than flattening everything into one unnamed `Sigma`. Cross-family correspondence should then cite both the participating viewpoint ids and their `ViewFamilyId` origins.

#### E.17.1:14.4 - Engineering vs publication families

Some contexts need both engineering viewpoints and publication viewpoints. `E.17.1` permits both, but it does not allow one family id to erase the distinction. A family that imports both kinds must keep the namespaces and bundle origins explicit so that authors do not confuse *how the holon is being understood* with *how a publication surface chooses to expose that understanding*.

### E.17.1:15 - Worked Bundle Families

#### E.17.1:15.1 - TEVB engineering family

A TEVB engineering bundle for holons may include viewpoints such as:

- `VP.Functional`,
- `VP.Procedural`,
- `VP.RoleEnactor`,
- `VP.ModuleInterface`.

The important point is not the vocabulary alone. The bundle states that these viewpoints are intended to recur together for one engineering family of concerns. A later description family then imports that engineering bundle rather than re-inventing a local list of "roughly similar" viewpoints.

#### E.17.1:15.2 - Governance and risk family

A governance bundle may group viewpoints such as:

- `VP.Risk`,
- `VP.Control`,
- `VP.Compliance`,
- `VP.Operations`.

This bundle is valuable precisely because the four viewpoints recur together but are not interchangeable. Keeping them as one family id makes the reuse visible while still preserving the distinct member meanings.

#### E.17.1:15.3 - Research-method family

A research-method bundle may include viewpoints such as:

- `VP.Theory`,
- `VP.Experiment`,
- `VP.Inference`,
- `VP.Limitations`,
- and, where appropriate, `VP.Reproducibility`.

A local inquiry note might import only three of these viewpoints, but the import remains legible because the omitted ones still belong to a reviewed family rather than disappearing into ad hoc prose.

#### E.17.1:15.4 - Cross-family description stack

A serious project may use TEVB engineering viewpoints for the design family, a governance bundle for program oversight, and a publication-oriented family for public surfaces. `E.17.1` makes this stack lawful by preserving which bundle each viewpoint came from and by preventing the final publication surface from masquerading as the viewpoint library itself.

### E.17.1:16 - Authoring and Review Guidance

#### E.17.1:16.1 - For bundle authors

Bundle authors should ask:

- what recurring family is being named,
- which viewpoints truly belong together in that family,
- what local didactic material belongs in annexes instead of the bundle core,
- and whether the bundle is stable enough to deserve a reusable `ViewFamilyId`.

A good bundle is not maximal. It is coherent, reviewable, and reusable.

#### E.17.1:16.2 - For reviewers

Reviewers should inspect both levels:

- **member level** - are the included viewpoints individually explicit enough to be reused?
- **bundle level** - do they actually form one coherent family rather than one convenient list?

They should also check whether a local project has silently forked the bundle while still using the inherited family id.

#### E.17.1:16.3 - For integrators and librarians

Integrators should keep libraries small, curated, and editioned. It is usually better to publish:

- one stable core bundle,
- one explicit local extension,
- and one clear subset declaration

than to let one giant family absorb every recurring viewpoint a domain has ever used. Library sprawl destroys the cognitive advantage that reusable bundles are supposed to provide.

### E.17.1:17 - Edition and Migration Notes

#### E.17.1:17.1 - Rename vs semantic change

A lexical rename that leaves viewpoint meaning and membership unchanged may be treated as a naming-layer migration. A change in membership, concern, admissibility, or member semantics is not just a rename; it requires a new edition or a new local bundle.

#### E.17.1:17.2 - Migration from local `Sigma` lists

Legacy `U.MultiViewDescribing` families often publish only one local list of viewpoints. Migration should proceed by:

1. identifying recurring families across several such local lists,
2. publishing those families as explicit bundles,
3. then rewriting the local families to import the new `ViewFamilyId` and declare any subset selection explicitly.

This sequence preserves provenance and avoids pretending that the reusable family had always existed.

#### E.17.1:17.3 - Migration from surface-bound naming

If a legacy practice uses one label interchangeably for a viewpoint family, a report section, and a publication face, migration should separate those roles explicitly. `ViewFamilyId` remains at the bundle layer; `U.Viewpoint` ids remain at the viewpoint layer; publication-face names remain publication-layer vocabulary.

#### E.17.1:17.4 - Boundary to annex growth

Annex manifests are useful, but a bundle should not become a thin shell hiding all of its meaning elsewhere. The core bundle still needs enough explicit member and family structure to stand on its own. Annexes deepen reuse; they do not replace the bundle's primary contract.
### E.17.1:18 - Import Collision and Alias Discipline

#### E.17.1:18.1 - Family id is not a synonym bag
A `ViewFamilyId` does not mean that all member viewpoints are interchangeable labels for one concern. It means that a reviewed family of viewpoints is intended to recur together. Authors should therefore resist the common drift where one convenient bundle name begins to substitute for all of its members.

#### E.17.1:18.2 - Import collision rule
When two imported bundles contribute viewpoints with overlapping lexical names, the publication should preserve the originating viewpoint ids and bundle provenance rather than silently merging the members. Bundle reuse is lawful only if collisions remain inspectable.

#### E.17.1:18.3 - Alias boundary
Local teaching aliases may be added for readability, but the alias must dock to explicit member viewpoints and must not erase bundle provenance. If the alias starts doing bundle-selection work by itself, it has become too strong and should be replaced by explicit member references.

### E.17.1:19 - Bundle Projection and Comparative Use

#### E.17.1:19.1 - Projection to local subsets
A description family may project only a subset of a reusable bundle. This is lawful if the omitted members remain visible as omitted rather than disappearing into an ad hoc local list. Projection keeps bundle provenance intact while acknowledging that local publication rarely uses every member.

#### E.17.1:19.2 - Comparative bundle use
Bundles may be compared across contexts only if the comparison preserves member ids, member meanings, and subset/projection decisions. Comparing two bundle labels alone is not enough, because similarly named families may contain materially different viewpoint sets.

#### E.17.1:19.3 - Boundary to publication-face design
A publication face may choose to surface one composite presentation of several viewpoints, but the face is not the bundle. `E.17.1` therefore requires the underlying member structure to remain recoverable even when a public-facing document flattens it for readability.

### E.17.1:20 - Review Matrix and Library Governance

A reviewer can test a viewpoint bundle library with five questions:

1. **Do the member viewpoints still have explicit standalone meaning?**
2. **Does the bundle name describe one coherent recurring family rather than one convenience list?**
3. **If a subset is imported, is the omitted remainder still visible as omission rather than silent deletion?**
4. **If several bundles interact, is provenance preserved across collisions and local aliases?**
5. **Has a publication face started impersonating the library itself?**

Library governance should therefore prefer small, editioned, provenance-preserving bundles over lexical mega-families that are easy to name but hard to reuse truthfully.
### E.17.1:End

