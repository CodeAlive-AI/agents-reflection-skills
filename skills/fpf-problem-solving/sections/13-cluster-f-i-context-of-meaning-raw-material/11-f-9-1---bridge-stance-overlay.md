## F.9.1 - Bridge Stance Overlay

> **Type:** Architectural (A)
> **Status:** Draft
> **Normativity:** Normative unless marked informative

**Plain-name.** Bridge-card stance overlay.


### F.9.1:1 - Problem frame
When positions or trajectories in language-state work are compared across schools or contexts, authors often need a disciplined interpretive gloss on top of a formal bridge card. The gloss must help reading without becoming a second bridge taxonomy.

### F.9.1:2 - Problem
Authors often express stance informally ("roughly analogous", "really a projection", "just a rename"), which makes bridge interpretation unstable. A full second taxonomy would be worse: it would compete with the core bridge kinds.

### F.9.1:3 - Forces
| Force | Tension |
|---|---|
| **Expressive stance vs bridge discipline** | Add authoring clarity without introducing a rival bridge-kind system. |
| **Reuse vs inflation** | Make stance annotations reusable across bundles while keeping bridge cards structurally governed by `F.9`. |
| **Interpretive help vs substitution abuse** | Help readers interpret a bridge without silently licensing stronger substitution than `F.9` allows. |

### F.9.1:4 - Solution
A Bridge Stance Overlay is an authoring annotation attached to an existing `F.9` bridge card. It does not change the underlying bridge kind, direction, `CL`, or loss notes.

#### F.9.1:4.1 - Starter overlay vocabulary
| Stance | Intended reading | What it does **not** imply |
|---|---|---|
| `localRename` | the target term is near-renaming within the current context boundary | automatic cross-context identity |
| `operationalizes` | the target gives an operational or procedural realization of the source | type-structure equivalence |
| `partialAnalogy` | some explanatory pattern is shared, but only partially | lawful substitution |
| `projection` | the target is a deliberate reduction or aspectual projection of the source | completeness or reversibility |
| `nonEquivalent` | the apparent similarity is not strong enough for equivalence | any silent substitution |

#### F.9.1:4.2 - Boundary rule
A stance annotation is interpretive help for authors and readers. It is not a second bridge ontology.

#### F.9.1:4.3 - Relation to `CL` and loss
- `CL` still governs substitution licence.
- loss notes still govern what fails to carry.
- stance annotations merely say how the author wants the bridge to be read.

If the stance materially affects interpretation, the bridge card should publish explicit loss notes that match it.

### F.9.1:5 - Archetypal Grounding
**Tell.** A stance annotation says how to read the bridge, not what the bridge kind structurally is.

**Show (System).** An operator alarm label may `operationalizes` a broader control cue without becoming identical to it.

**Show (Episteme).** A TAE felt-sense phrase may be only a `partialAnalogy` to a later formal term.

### F.9.1:6 - Bias-Annotation
The pattern favors disciplined cross-school comparison over sweeping synonym claims.

### F.9.1:7 - Conformance Checklist
- `CC-F.9.1-1` A stance annotation **SHALL NOT** replace the underlying `F.9` bridge kind.
- `CC-F.9.1-2` Stance annotations **SHOULD** be accompanied by explicit loss notes when they materially affect interpretation.
- `CC-F.9.1-3` `nonEquivalent` **SHALL** block silent substitution.
- `CC-F.9.1-4` A stance annotation **SHALL NOT** claim stronger sameness than the bridge card's `CL` and kind allow.

### F.9.1:8 - Common Anti-Patterns and How to Avoid Them
- **Annotation as ontology.** Do not treat stance as the bridge kind itself.
- **Friendly-vague analogy.** If the relation is high-loss, say so explicitly.
- **Stance inflation.** Do not use the annotation to smuggle in substitution rights that `F.9` withholds.

### F.9.1:9 - Consequences
The benefit is reusable authoring clarity for bridge-heavy bundles and school comparisons. The trade-off is one more declared annotation layer on bridge cards.

### F.9.1:10 - Rationale
`U.LanguageStateSpace` and `U.LanguageStateTransductionTrajectory` create many legitimate cross-school comparisons. `F.9.1` gives those comparisons a reusable stance vocabulary without fragmenting the underlying `F.9` bridge discipline.

### F.9.1:11 - SoTA-Echoing
The annotation mirrors common interpretive practice in comparative theory, design translation, and operator documentation, but makes the stance explicit and reusable.

### F.9.1:12 - Relations
- Builds on: `F.9`, `C.2.2a`.
- Coordinates with: `A.16.0`, `E.17.1`, `E.17.ID.CR`, `A.6.P`, `A.6.A`, `A.6.Q`, `C.25`, and `B.4.1`.
- Constrains: authoring annotations for tradition and routing bundles.
### F.9.1:13 - Worked Bridge-Card Examples

#### F.9.1:13.1 - `localRename`
A bridge card may relate two near-coextensive operational labels inside one declared context fragment and mark the stance as `localRename`. The bridge card still publishes its own direction, kind, `CL`, and loss notes. The stance only warns the reader that the author's intended reading is close renaming **within that boundary**; it does not license export of the rename beyond the stated fragment.

#### F.9.1:13.2 - `operationalizes`
A high-level capability cue may be bridged to a more procedural checklist or control ritual. The bridge card may carry the stance `operationalizes` to show that the target gives a lawful enactment surface for the source. The relation can still be high-loss: the procedural target need not preserve the source's broader theoretical framing, and the stance does not claim type-structure sameness.

#### F.9.1:13.3 - `projection`
A rich construct may be mapped into a narrower reporting or measurement surface. The bridge card may declare the stance `projection` when the target intentionally keeps only one aspect. The required loss notes should name the dropped dimensions, because the stance is informative only when the omitted structure is made explicit.

#### F.9.1:13.4 - `partialAnalogy` and `nonEquivalent`
A comparative bundle may need to mention an explanatory resemblance across traditions without claiming substitution. In such cases `partialAnalogy` may guide reading when the shared pattern is local and declared. If review concludes that even this local resemblance is too weak for safe reuse, `nonEquivalent` should be preferred so that apparent similarity does not drift into silent replacement.

### F.9.1:14 - Authoring and Review Guidance
- Publish a stance overlay only on top of a complete bridge card that already declares bridge kind, direction, `CL`, and explicit loss notes where needed.
- Choose the weakest stance that truthfully describes the intended reading; do not strengthen the overlay merely because it sounds more helpful.
- If multiple interpretive notes are needed, prefer one primary stance plus explicit loss notes rather than several competing overlays.
- Use `nonEquivalent` when the main value of the annotation is to warn the reader away from substitution.
- In school bundles and annex manifests, place the overlay near the bridge card it qualifies so readers can inspect structural bridge data before reading the interpretive gloss.

Reviewer guidance is simple: ask whether the overlay merely helps reading or is covertly claiming extra sameness, transport, or substitution rights. If it does the latter, revise the bridge card itself rather than decorating it.

### F.9.1:15 - Migration and Boundary Notes
Legacy comparative notes often contain undeclared stance language such as "roughly the same", "really a projection", or "just an operational version". When such material is normalized, the first repair step is to recover the underlying bridge card in `F.9`; only then may a Bridge Stance Overlay be added as an explicit authoring annotation.

The pattern intentionally does not define a second bridge taxonomy, a new substitution calculus, or a score for bridge quality. Those responsibilities remain with the bridge card, `CL`, and declared loss discipline. Tradition bundles may carry many bridge cards with stance overlays, but the overlays remain local annotations attached to those cards, not free-standing comparative objects.
### F.9.1:16 - Overlay Package Discipline

A stance overlay is useful only when it stays visibly subordinate to the bridge card it qualifies.

#### F.9.1:16.1 - Minimal overlay package
A usable stance overlay should normally publish:

- the qualified `F.9` bridge card,
- the chosen stance term,
- the local reason the stance is helpful,
- and any loss emphasis that becomes especially important under that stance.

Without this package, a stance word becomes a decorative gloss detached from the bridge it is supposed to interpret.

#### F.9.1:16.2 - One primary stance per bridge card
A bridge card should normally carry one primary stance overlay. If several interpretive notes are needed, the extras should usually live in explicit loss notes or surrounding commentary rather than in several competing stance tags.

#### F.9.1:16.3 - Overlay locality
A stance overlay is local to the bridge card and context fragment that publish it. Reusing the same stance label elsewhere is lawful only when the new bridge card independently supports that reading.

### F.9.1:17 - Interaction with `CL`, Direction, and Loss

#### F.9.1:17.1 - `CL` remains prior
If the stance sounds friendlier than the declared `CL`, `CL` wins. An `operationalizes` or `localRename` overlay cannot overrule a high-loss bridge or a low-substitution `CL` declaration.

#### F.9.1:17.2 - Direction-sensitive reading
Some stance labels read differently depending on bridge direction. A construct may project into a report-only surface in one direction while the reverse direction is not lawful at all. Authors should therefore avoid stance prose that sounds symmetric when the bridge card is directional.

#### F.9.1:17.3 - Loss emphasis rule
When a stance is likely to invite over-reading, the loss note should be strengthened rather than softened. The overlay is useful exactly because it helps interpretation; that is also why it can mislead if the losses are understated.

### F.9.1:18 - Bundle Use and Comparative Reading

#### F.9.1:18.1 - Bundle-level reuse
Tradition bundles and viewpoint bundles may reuse the same stance vocabulary across many bridge cards, but the interpretation remains card-local. Bundle reuse is a readability aid, not a warrant that similarly named overlays are structurally equivalent.

#### F.9.1:18.2 - Comparative stance caution
Two bridge cards may both be marked `projection` while dropping very different dimensions. Reviewers should therefore compare the loss notes and source-target structure, not the overlay term alone.

#### F.9.1:18.3 - Boundary to second bridge taxonomy
If authors start grouping bridges primarily by stance label and ignoring bridge kind, direction, `CL`, or loss, they have implicitly created a rival bridge taxonomy. `F.9.1` forbids that drift.

### F.9.1:19 - Review Matrix and Migration Tests

A reviewer can test stance-overlay integrity with five questions:

1. **Is the underlying bridge card complete and still primary?**
2. **Does the overlay stay weaker than the bridge card's structural claims?**
3. **Would the same overlay still be truthful if read in the reverse direction?** If not, the locality or directionality needs to be made clearer.
4. **Do the loss notes carry the interpretive burden that the overlay might otherwise overstate?**
5. **Is the bundle using stance as a readability aid, or as a covert replacement for bridge ontology?**

Legacy prose about things being "really the same", "only a projection", or "just an operational version" should therefore be migrated by recovering bridge kind, direction, `CL`, and loss first, then adding an overlay only if it still adds disciplined interpretive value.
### F.9.1:End


