## A.6.3.CR - ConservativeRetextualization — same-described-entity textual re-expression

**Placement.** Specialization under `A.6.3 U.EpistemicViewing` for same-described-entity textual re-expression.  
**Builds on.** `A.6.3 U.EpistemicViewing`; `A.6.2 U.EffectFreeEpistemicMorphing`; `A.7`; `E.10.D2`; `E.17.0`; `E.17`; `F.9`; `F.18`; `E.10`.  
**Coordinates with.** `ExplanationFaithfulnessProfile`; `RepresentationTransduction`; `E.17.ID.CR ComparativeReading`; `A.6.4 U.EpistemicRetargeting`; `B.5.2`; `A.15`.

**One-line summary.** `ConservativeRetextualization` is a same-described-entity textual re-expression of an episteme that stays inside `A.6.3 U.EpistemicViewing`: it may shorten, reorder, filter, translate, or restate claims, but it does **not** silently change `describedEntityRef`, add new claims about that entity, or hide bridge work.

### A.6.3.CR:1 - Problem frame

Teams constantly need a second textual form of the same episteme:
- an internal technical statement rewritten as an engineer-manager-readable report;
- a longer source note rewritten as a shorter working summary;
- a source-language statement rewritten into another natural language;
- a dense claim set rewritten as a filtered report that keeps only one declared slice.

These transforms are often treated as harmless editing. In practice they can quietly drift into hidden reinterpretation, hidden bridge work, hidden explanation, or even hidden retargeting. FPF already has `A.6.3` for same-described-entity conservative viewing. What is still needed is a focused named pattern that states when a textual rewrite remains only a conservative viewing case under `A.6.3`.

### A.6.3.CR:2 - Problem

Without a dedicated pattern for conservative textual re-expression:
1. report, summary, translation, and filtered rewrite cases are handled ad hoc;
2. authors treat textual simplification as if it were automatically conservative;
3. the boundary to explanation-facing surfaces stays blurry;
4. correspondence-mediated rewrites are not distinguished from direct rewrites;
5. later reviewers cannot tell whether the result is still a view of the same described entity or a new interpretive artefact.

### A.6.3.CR:3 - Forces

- **Same entity, different wording.** Readers need different textual forms without reopening the described entity.
- **Compression vs loss visibility.** Shorter or plainer forms are often useful, but omission and attenuation must stay explicit.
- **Direct vs correspondence-mediated rewrites.** Some rewrites read from one source episteme; others depend on a declared `CorrespondenceModel`.
- **Textual focus vs family creep.** The pattern should cover same-entity textual re-expression, not explanation, not representation-wide shifts, and not retargeting.
- **Publication discipline.** Admissible faces and surfaces still matter even when the transform looks like "just a rewrite."

### A.6.3.CR:4 - Solution — same-described-entity textual re-expression under `A.6.3`

#### A.6.3.CR:4.1 - Informal definition

> `ConservativeRetextualization` is a named pattern specialized under `A.6.3 U.EpistemicViewing` for textual re-expression of the same described entity.
>
> It preserves `describedEntityRef`, keeps the transform effect-free, and allows only claim-preserving or explicitly loss-declared rewriting of already available content.
>
> It may change register, ordering, textual density, language, emphasis, or local wording. It may not silently introduce new claims, new bridge licences, new downstream authority, or a changed object-of-talk.

#### A.6.3.CR:4.1.a - Pattern, case, and publication distinction

`ConservativeRetextualization` is an **intensional pattern** and a named specialization under `A.6.3`. Concrete same-described-entity rewrites are passive episteme-level cases or publication texts reviewed under this pattern; the pattern itself does not act, decide, or publish.

This distinction matters because the pattern governs **how** a rewrite is recognised, justified, and checked. It does **not** require every short report paragraph, summary line, or translation sentence to carry a giant standalone record.

#### A.6.3.CR:4.1.b - Local working vocabulary

This pattern repeatedly uses a small working vocabulary.
- **Source slice** = the already available pinned or otherwise reviewable textual material being restated.
- **Published slice** = the resulting textual rendering that remains under same-described-entity discipline.
- **Ordinary case** = a reviewable same-entity rewrite where source tether, omission notes, and reroute conditions stay readable without a heavyweight review record.
- **Load-bearing case** = a case where dispute, policy, assurance, correspondence burden, or cross-context reliance makes a fuller record worth publishing.

These terms are only local reading aids. They do not create new owners, new publication faces, or a second semantic layer.

#### A.6.3.CR:4.2 - Scope and exclusions

**In scope**
- same-described-entity report rewrite;
- same-described-entity summary;
- same-described-entity translation between natural-language surfaces;
- declared filtering or foregrounding of already-present claims in textual form.

**Out of scope**
- any change of `describedEntityRef` or hidden change of object-of-talk (`A.6.4`);
- explanation surfaces whose main purpose is explanatory rendering rather than same-entity rewrite (`ExplanationFaithfulnessProfile`);
- representation-regime changes such as text→table, text→diagram, or text→latent form (`RepresentationTransduction`);
- abductive, bridge-mediated, or route-bearing work that introduces new claims rather than restating available ones.


#### A.6.3.CR:4.2.a - Reader guidance

Use this pattern when the object-of-talk stays fixed and the published result still remains textual.
- If the main change is explanatory, move to `ExplanationFaithfulnessProfile`.
- If the main change is a representation-scheme shift, move to `RepresentationTransduction`.
- If the described entity changes, move to `A.6.4`.

#### A.6.3.CR:4.2.b - What a reviewer checks first

A reviewer usually does not begin by filling every field name. The first useful questions are simpler:
1. Is the published result still about the same described entity?
2. Is the result still textual, or has it become explanation or representation change?
3. Can the reader see what was omitted, softened, or foregrounded?
4. If correspondence is doing work, is that burden visible rather than hidden in fluent prose?
5. If any answer is doubtful, is the reroute path explicit?

Only after these questions are answered does a fuller load-bearing review record usually become worth writing.

#### A.6.3.CR:4.3 - Working-model first; explicit review record only when the case is load-bearing

Most same-described-entity textual rewrites should stay human-usable. This pattern therefore follows **E.14’s working-model-first discipline**: ordinary report, summary, or translation cases do not need a giant inline metadata block. What they do need is enough explicitness that a reviewer can still tell what stayed the same, what was omitted, and where the case would have to reroute.

**Ordinary case (default).** For everyday same-described-entity rewrites, it is usually enough that the text or its surrounding publication keeps explicit:
- which source material is being re-expressed;
- that `describedEntityRef` remains preserved;
- whether the case is direct or correspondence-mediated when that is not obvious;
- what omissions or attenuation matter for the reader;
- where the case exits if it has turned into explanation, representation shift, retargeting, or world/gate-bearing material.

**Explicit review record (only for load-bearing cases).** A fuller record is warranted when the case is assurance-facing, gate-adjacent, cross-context, correspondence-heavy, policy-bearing, or likely to be disputed. The record may inherit host ids and already-pinned metadata instead of restating them inline. When published, that record normally captures:
- transform placement (`landingForm = specialization under A.6.3`, `hostOwner`, `sourceForm`, `targetForm`, `changeLocus`);
- preservation context (`describedEntityPolicy = preserve`, `boundedContextPolicy`, `viewpointPolicy`, `referenceSchemePolicy`, `representationSchemePolicy`, `groundingPolicy`, `referencePlanePolicy`);
- claim and publication discipline (`claimPolicy`, `claimScopePolicy`, `publicationScopePolicy`, `reliabilityTransportPolicy`, `pinningPolicy`, `provenancePolicy`, `lossProfile`);
- continuity and bridge discipline (`claimContinuityClass`, `microtheoryContinuityClass`, `onticContinuityClass`, `bridgeRequirement`, `conservativityWitness`);
- downstream and admissibility discipline (`worldContactPolicy`, `evidencePolicy`, `gatePolicy`, `workCrossing`, `upstreamOwner`, `downstreamOwner`, `admissibleFaces`, `admissibleSurfaces`, `compositionLaw`, `reopenCondition`);
- naming and presentation discipline (`publicNamePolicy`).

The point of this record is not bureaucratic completion for every paragraph. It is to make **load-bearing** cases reviewable without hiding meaning in style, topic familiarity, or editor intuition.

#### A.6.3.CR:4.3.a - Ordinary admissibility defaults

Default admissibility for ordinary same-described-entity textual cases:
- primary admissible faces are `Plain` and `Tech`;
- bounded report-only use is lawful when source pins, provenance, loss notes, and same-described-entity conservativity remain visible;
- `Interop` use is lawful only when the host explicitly permits source-pinned, text-preserving export without added semantics;
- `Assurance` or gate-bearing use is not default and requires host-explicit policy plus source-pinned conservativity without hidden strengthening.

#### A.6.3.CR:4.4 - Direct and correspondence-mediated profiles

**Direct ConservativeRetextualization**
- source and target are textual re-expressions of one source episteme;
- no `CorrespondenceModelRef` is needed;
- the main burden is explicit loss/provenance discipline.

**CorrespondenceConservativeRetextualization**
- the target text is derived from a declared correspondence between epistemes or views of the same described entity;
- `CorrespondenceModelRef` is required;
- the result remains under `A.6.3` only if the correspondence supports same-described-entity conservativity and no new claims are imported beyond the declared witness set.

Cross-language translation is not automatically direct. If the translation depends on declared correspondence, reference-scheme mediation, or bounded equivalence notes, it must be treated as correspondence-mediated rather than disguised direct rewriting.

#### A.6.3.CR:4.4.a - Recurring same-entity textual moves

The pattern covers a small family of recurring textual moves as long as the same described entity remains explicit:
- **Register shift** — a technical statement is rewritten into plainer engineer-manager prose without changing what is being said about the same entity.
- **Summary or filtered restatement** — a source note is shortened or focused on one declared slice, with omissions stated rather than hidden.
- **Cross-language restatement** — the same source claim is restated in another natural language while the same source tether and same-entity line remain explicit.
- **Correspondence-supported textual synthesis** — one textual rendering is produced from declared same-entity correspondences without importing extra bridge or substitution burden.

These are recurring move shapes, not separate owners. The host relation remains the same: same-described-entity textual re-expression under `A.6.3`.

#### A.6.3.CR:4.5 - Shared conservative retextualization law packet

##### A.6.3.CR:4.5.a. Preservation law
A case under `ConservativeRetextualization` preserves the same described-entity line, the declared bounded context, and the already available claim-bearing source while changing wording, register, language, ordering, or density. It states what remains preserved about claim scope, publication scope, pins, provenance, grounding, and ontic scaffold, and it says whether the case is `Direct` or `Correspondence`.

##### A.6.3.CR:4.5.b. Loss and reliability law
A reviewed case makes explicit what is omitted, shortened, foregrounded, or attenuated by the rewrite. Reliability transport may remain source-bounded or be explicitly downgraded, but it must never be silently strengthened by cleaner prose, stronger rhetoric, or management-facing polish.

##### A.6.3.CR:4.5.c. Authority and handoff law
A case reviewed under this pattern stays same-entity and episteme-level. It does not own explanation governance, bridge stance, retargeting, gate authority, or work enactment. If the rewrite becomes explanatory, bridge-bearing, gate-bearing, or world-facing, the case must hand off to the appropriate downstream owner and say so explicitly.

##### A.6.3.CR:4.5.d. Composition and reopen law
Repeated direct rewrite over the same source line may be idempotent, but heterogeneous rewrites and correspondence-mediated rewrites are generally order-sensitive. A reviewed case must reopen whenever correspondence support, source pins, provenance, admissible-face assumptions, or same-described-entity conservativity stop being explicit.

##### A.6.3.CR:4.5.e. Non-collapse note for correspondence
Correspondence-mediated retextualization does **not** by itself grant bridge licence, substitution licence, or comparative-reading licence. If the case needs those burdens, they must be declared separately rather than being smuggled in through correspondence language.

##### A.6.3.CR:4.5.f. Local conservativity witness for borderline textual cases
For borderline textual rewrites, a reviewer treats the case as no longer conservative under this pattern unless each point below remains visibly preserved or is explicitly loss-declared with the reroute path stated.
- **Modality and force.** A rewrite may not silently turn possibility, uncertainty, bounded scope, or hypothesis language into stronger commitment.
- **Caveats and qualifications.** A rewrite may not quietly remove conditions, exception notes, uncertainty markers, or temporal qualifiers that still matter for reading the same source.
- **Reliability posture.** Cleaner prose, better ordering, or manager-facing polish may not silently raise confidence, warrant strength, or readiness for action.
- **Bridge and substitution burden.** Same-entity textual fluency may not import cross-context equivalence, substitution, or comparative-reading licence unless that burden is declared elsewhere.
- **Alternative preservation.** A rewrite may not collapse open alternatives, rival hypotheses, or declared plurality into one apparently settled reading unless the loss is stated and still lawful under this pattern.

This witness is local to `ConservativeRetextualization`. It does not replace the broader conservativity laws of `A.6.3`; it makes them inspectable for textual rewrites where fluent prose can otherwise hide strengthening.

### A.6.3.CR:5 - Archetypal Grounding

#### A.6.3.CR:5.1 - Same-described-entity report rewrite
**Source note slice.** `Service S exceeded the latency threshold in the evening batch window. Trace T-44 and dashboard pin D-17 show the spike. Two low-confidence hypotheses remain open.`

**Published report slice.** `Evening-batch latency for Service S exceeded the threshold. Source pins: Trace T-44, Dashboard D-17. Low-confidence hypotheses are omitted here and remain in the pinned source note.`

This is a lawful direct `ConservativeRetextualization` because the described entity stays fixed, the report remains textual, and the omission is stated rather than hidden. In ordinary internal use, this often needs only source pins plus visible omission notes rather than a full explicit review record.

#### A.6.3.CR:5.1.a - Ordinary inherited-pin summary
**Pinned source cluster.** `Incident note N-14, trace T-44, and dashboard card D-17 are already published together under one incident review bundle.`

**Published stand-up slice.** `Evening-batch latency again exceeded the threshold for Service S. See N-14 / T-44 / D-17 for the pinned source cluster.`

This is still a lawful ordinary case even though the short stand-up slice does not restate every pin and qualifier inline. The didactic point is that lightweight use may inherit already-published pins and provenance when the tether stays visible to the reader.

#### A.6.3.CR:5.2 - Same-described-entity rewrite via declared correspondence
**Source design slice.** `Cooling loop CL-2 preserves safe temperature margins during standard load.`

**Source safety slice.** `Cooling loop CL-2 maintains the temperature condition required for hazard-control claim HC-7 during standard load.`

**Published joint-review slice.** `For standard load, Cooling loop CL-2 is described in both the design and safety views as maintaining the required temperature condition. This summary relies on CorrespondenceModel CM-12 and does not add claims beyond that declared overlap.`

The synthesis may stay in this pattern only if the source relation remains explicit and the text does not silently strengthen claims beyond the declared correspondence-supported overlap. Because correspondence support is load-bearing here, a fuller explicit review record is usually warranted.

#### A.6.3.CR:5.2.b - Cross-language re-expression without hidden bridge work
**Source slice.** `The backup controller stays in passive watch mode until the primary loop fails two consecutive heartbeat checks.`

**Published slice.** `Резервный контроллер остаётся в режиме пассивного наблюдения, пока основной контур не пропустит две последовательные проверки heartbeat.`

This remains in `ConservativeRetextualization` only if the translation is still tethered to the same source claim, preserves the same described entity, and does not quietly add cross-tradition bridge claims such as "equivalent architecture role" or "same operational guarantee" beyond what the source actually states.

#### A.6.3.CR:5.3 - Boundary to explanation surfaces
A text is rewritten not mainly to restate the same source, but to explain why it matters, simplify reasoning for a learner, or narrate a mechanism. That move should leave `ConservativeRetextualization` and be reviewed under `ExplanationFaithfulnessProfile`.

#### A.6.3.CR:5.4 - Boundary to representation transduction
A prose note is rewritten as a table, matrix, diagram, or latent/distributed representation. Even if the described entity stays fixed, this is not only a textual rewrite; it belongs with `RepresentationTransduction`.

### A.6.3.CR:6 - Bias-Annotation

Lenses tested: **Arch**, **Onto/Epist**, **Prag**, **Did**.
This pattern intentionally biases toward same-entity conservativity and away from explanation or retargeting inflation. The main mitigation is explicit reroute discipline to `ExplanationFaithfulnessProfile`, `RepresentationTransduction`, `A.6.4`, and later downstream owners when the same-entity textual reading stops being honest.

### A.6.3.CR:7 - Conformance Checklist

1. **CC-CR-1 — Same described entity remains explicit.**
   The case preserves `describedEntityRef` without special pleading.
2. **CC-CR-2 — Textual re-expression remains the right family.**
   The result stays a textual re-expression rather than explanation or representation shift.
3. **CC-CR-3 — Loss / provenance / pinning / reliability are explicit or inherited by pinned reference.**
   The case states these explicitly or inherits them through already-pinned host material that remains visible to review.
4. **CC-CR-4 — Direct vs correspondence split is explicit.**
   The `Direct / Correspondence` split is explicit and justified.
5. **CC-CR-5 — Correspondence support is named where needed.**
   If correspondence-mediated, `CorrespondenceModelRef` is declared.
6. **CC-CR-6 — Local conservativity witness remains satisfied.**
   The reviewed case does not silently strengthen modality, remove caveats, raise reliability posture, import bridge or substitution licence, or collapse declared alternatives beyond stated loss notes.
7. **CC-CR-7 — Reroute path is explicit on failure.**
   If the case fails any of the checks above, the reroute path is explicit (`ExplanationFaithfulnessProfile`, `RepresentationTransduction`, `A.6.4`, `B.5.2`, or another owner).
8. **CC-CR-8 — Working-model first remains intact.**
   Ordinary same-entity rewrites stay lightweight; fuller explicit review records are reserved for load-bearing cases.

### A.6.3.CR:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | Why it is wrong | How to avoid it |
|---|---|---|
| Treating every summary as automatically conservative | summary pressure hides omission and claim drift | publish loss/provenance discipline explicitly |
| Hiding correspondence in plain paraphrase | correspondence burden disappears into prose | declare `CorrespondenceModelRef` when needed |
| Letting a rewrite become explanation | explanation work quietly becomes a textual “rewrite” | reroute to explanation governance once didactic/explanatory work dominates |
| Letting object-of-talk drift by topic similarity | same topic is not the same described entity | exit to `A.6.4` if `DescribedEntityRef` changes |

### A.6.3.CR:9 - Consequences

- Textual same-entity rewrites get a lawful place without inventing a new heavy owner.
- Direct and correspondence-mediated variants stay visibly separated.
- Loss, provenance, and reliability transport become explicit instead of implicit editorial judgement.
- Ordinary working-model use stays lightweight, while load-bearing cases get a fuller explicit review record when risk warrants it.
- The pattern remains safely bounded by `A.6.3`, `A.6.4`, explanation-facing work, and representation-shift work.

### A.6.3.CR:10 - Rationale

This pattern is worth splitting out because same-entity textual re-expression is common, useful, and safer than many neighboring transform families when it stays explicitly conservative. Keeping it under `A.6.3` as a named specialization preserves owner integrity while making a recurring authoring move easier to review, while still respecting E.14’s working-model-first discipline for ordinary cases.

### A.6.3.CR:11 - SoTA-Echoing

**SoTA note.** This section does not mint an independent second rule layer. It is a load-bearing alignment surface: the Solution, Conformance Checklist, boundary rules, and Relations of this pattern must match the stance stated here or explicitly justify any divergence.

**Traditions covered.** This pattern binds itself to architecture-description governance, summarization factuality, translation-quality governance, and plain-language rewrite practice.

| Claim need | SoTA practice (post-2015) | Primary source (post-2015) | Alignment with `A.6.3.CR` | Adoption status |
|---|---|---|---|---|
| Conservative rewrite must stay visibly tied to the same described content rather than drifting through presentation fluency. | Architecture-description practice separates source artefact, view, viewpoint, and correspondence burden instead of letting rendered prose silently change the object being described. | ISO/IEC/IEEE 42010:2022 | `A.6.3.CR` keeps same-described-entity textual restatement under `A.6.3`, requires explicit reroute when object-of-talk changes, and keeps bridge burden out of fluent rewrite. | **Adopt.** |
| Summary-like rewriting is not automatically harmless; factuality and faithfulness need source-sensitive checking. | Modern summarization work treats unsupported compression, strengthening, and hallucinated linkage as core failure modes rather than editorial noise. | Maynez et al. (2020), *On Faithfulness and Factuality in Abstractive Summarization* | `A.6.3.CR` adopts that stance and adapts it to FPF by making omission, reliability posture, and same-entity bounds explicit review concerns. | **Adopt/Adapt.** |
| Translation quality is governed through declared dimensions such as accuracy, omission, and addition rather than by fluency alone. | Translation-quality governance separates adequacy from surface smoothness and requires explicit treatment of omission/addition error classes. | Lommel et al. (2018), *MQM: A Framework for Declaring Translation Quality Metrics* | `A.6.3.CR` adapts this by treating correspondence-mediated and cross-language rewrites as lawful only when loss, provenance, and same-entity bounds stay explicit. | **Adapt.** |
| Plain-language rewrite may improve readability, but it must not silently change obligations, scope, or force. | Plain-language standards favour reader-oriented rewriting while preserving the original commitments and conditions that matter for use. | ISO 24495-1:2023 | `A.6.3.CR` adopts reader-oriented simplification for ordinary cases and rejects the popular shortcut that “plainer text” alone proves conservativity. | **Adopt/Reject-popular-shortcut.** |

**Architecture-description governance.** `A.6.3.CR` adopts the discipline that rendered text must stay visibly tied to a declared source/view line. It therefore rejects same-topic textual polish as sufficient evidence of same-described-entity conservativity.

**Summarization factuality.** `A.6.3.CR` adapts modern factuality concerns into a local conservativity witness: unsupported strengthening, hidden omission, and rhetorical uplift are treated as load-bearing failures, not as style noise.

**Translation and plain-language traditions.** `A.6.3.CR` adopts the reader-oriented value of translation and plain rewrite, but rejects the still-popular habit of treating cross-language or plain-language textual fluency as automatic proof that no new claim has been introduced.

**Local stance.** Best-known current practice supports a narrow rule: same-described-entity textual restatement is lawful only when source tether, loss, provenance, and same-entity bounds remain explicit enough that the reader can still tell what was preserved, what was omitted, and when the case must exit to another owner.

### A.6.3.CR:12 - Relations

- **Builds on:** `A.6.3`, `A.6.2`, `A.7`, `E.10.D2`, `E.17.0`, `E.17`, `F.9`, `F.18`, `E.10`
- **Coordinates with:** `ExplanationFaithfulnessProfile`, `RepresentationTransduction`, `E.17.ID.CR ComparativeReading`, `A.6.4`, `B.5.2`, `A.15`
- **Impact radius:** primary touch `A.6.3`; secondary review surfaces `E.17.0`, `E.17`, `F.9`; failed conservativity exits to `A.6.4`, `B.5.2`, or `A.15`
- **Boundary notes:** explanation-facing cases exit to `ExplanationFaithfulnessProfile`; representation-regime shifts exit to `RepresentationTransduction`; bounded comparative review surfaces exit to `E.17.ID.CR ComparativeReading`; described-entity changes exit to `A.6.4`.

### A.6.3.CR:End




