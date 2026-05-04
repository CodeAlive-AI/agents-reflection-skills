## B.5.2 - Abductive Loop

> **Type:** Architectural (A)
> **Status:** Stable
> **Normativity:** Normative unless marked informative

**Plain-name.** Abductive loop.

**Builds on.**
`B.5 Canonical Reasoning Cycle`, `B.5.1 Exploration`, `B.5.2.0 U.AbductivePrompt`, `A.10`, `B.3.3`.

**Coordinates with.**
`B.4.1 Observe-Notice-Stabilize-Route` for pre-abductive routing, `A.16` for lawful language-state moves, `A.6.P` for lexical repair before hypothesis publication, and `A.6.Q` / `A.6.A` when the initiating surface is evaluative or action-inviting rather than explanatory.

### B.5.2:1 - Problem frame

The Canonical Reasoning Cycle begins with abduction: the disciplined proposal of a candidate explanation, model, or conjecture that could account for a declared prompt. In practice this phase is often treated either as opaque inspiration or as unstructured ideation. Both framings are too weak for FPF. The framework needs an entry discipline that is broad enough to admit real inquiry starts and narrow enough to keep the resulting hypothesis auditable.

### B.5.2:2 - Problem

Without an explicit abductive pattern:

1. **Inquiry stalls at surprise.**
   A team encounters an anomaly, opportunity, or probe pressure but has no lawful next move for producing a candidate hypothesis.
2. **Origin is lost.**
   Once a conjecture appears, the initiating prompt, rival candidates, and early plausibility grounds disappear from the record.
3. **Candidate space collapses too early.**
   The first plausible-seeming explanation is treated as the explanation, even though alternatives were never exposed.
4. **Selection becomes opaque.**
   A chosen conjecture moves downstream without a visible record of why it outranked alternatives.
5. **Untestable hypotheses survive too long.**
   A candidate that cannot guide deduction, probe design, or evidence gathering is still treated as if it had earned progression.

### B.5.2:3 - Forces

| Force | Tension |
|---|---|
| **Generativity vs discipline** | The loop must admit non-deductive candidate generation without making arbitrary guesses look lawful. |
| **Breadth vs typed entry** | Abduction should begin from more than anomaly alone, but not from any untyped prose fragment. |
| **Rival diversity vs decision pressure** | Several candidates should remain visible long enough to compare them, while still allowing one prime hypothesis to progress. |
| **Speed vs traceability** | The loop must be light enough for repeated use but explicit enough to preserve provenance and later review. |
| **Plausibility vs evidence** | A candidate may be worth pursuing before evidence is strong, but it still needs explicit plausibility grounds. |

### B.5.2:4 - Solution - Structured abductive micro-cycle

`B.5.2` defines abduction as a typed, iterative micro-cycle that begins from a lawful `U.AbductivePrompt`, expands a candidate set, filters that set by explicit plausibility criteria, and publishes one selected conjecture as a new `U.Episteme` with `AssuranceLevel:L0`.

#### B.5.2:4.1 - Nature of abduction in FPF

In FPF, abduction is **inference to a presently most plausible candidate explanation or solution** under a declared prompt. It is neither arbitrary guessing nor hidden inspiration. The output is not yet an established result; it is a disciplined conjecture prepared for downstream deduction, testing, or refinement.

#### B.5.2:4.2 - Four-step micro-cycle

| Step | Core activity | Required publication outcome |
|---|---|---|
| **1. Frame the prompt** | State the initiating `U.AbductivePrompt` precisely enough that the unexplained contrast, opportunity, or probe pressure is explicit. | A prompt record with open question, scope notes, and provenance. |
| **2. Generate candidate hypotheses** | Produce multiple candidate conjectures that could resolve the prompt. | A visible candidate set, even if lightweight. |
| **3. Apply plausibility filters** | Compare candidates against explicit plausibility criteria. | A short rationale that records why some candidates remain live and others are rejected. |
| **4. Select and publish the prime hypothesis** | Choose one candidate for downstream work and instantiate it as a hypothesis-bearing episteme. | A new `U.Episteme` at `AssuranceLevel:L0`, linked back to the prompt and selection rationale. |

The loop is intentionally iterable. A selected prime hypothesis may later be replaced, narrowed, or reopened if deduction, probe work, or evidence reveals a better rival.

#### B.5.2:4.3 - Entry discipline via `U.AbductivePrompt`

`AnomalyStatement` remains a canonical entry surface, but it is not the only one. `B.5.2` also accepts the broader prompt species owned by `B.5.2.0`, such as `ProblemCuePrompt`, `OpportunityCuePrompt`, and `ProbeCuePrompt`. This broadens entry without dissolving type discipline.

#### B.5.2:4.4 - Plausibility filters

The filtering step is local and context-sensitive, but the criteria used **SHALL** be explicit. Typical filters include:

- **Parsimony.** Does the candidate introduce only the additional structure that the prompt requires?
- **Explanatory reach.** How much of the prompt does the candidate actually account for?
- **Consistency with established constraints.** Does the candidate avoid collision with already trusted pillars, mechanisms, or scope declarations?
- **Falsifiability / probeability.** Does the candidate create a path for deduction, testing, contrast, or evidence acquisition?
- **Scope fit.** Is the candidate framed for the declared prompt scope rather than for an inflated or shifted target?

No one filter is universally decisive. The pattern only requires that at least two filters be declared when a prime hypothesis is selected.

### B.5.2:5 - Archetypal Grounding

**Tell.** Abduction is not "a flash of insight." It is the governed passage from a typed prompt to a candidate conjecture through explicit rival generation and plausibility comparison.

**Show (System).** An operations team sees a recurring latency spike that existing method explanations do not cover. They publish an `AnomalyStatement`, generate rival causes, filter them by consistency with current telemetry and mechanism knowledge, and publish one prime conjecture as an `L0` hypothesis for downstream checking.

**Show (Episteme).** A research group notices that two accepted results no longer fit together under one framing. It publishes a `ProbeCuePrompt`, enumerates several rival explanatory reframings, rejects the ones that fail scope fit or would not generate decisive probes, and advances one candidate explanation as the next working hypothesis.

### B.5.2:6 - Bias-Annotation

This pattern biases authors toward visible candidate plurality, explicit plausibility criteria, and persistent prompt provenance. That bias is intentional. `B.5.2` would rather keep early conjectures slightly over-exposed than let their origin and selection grounds disappear.

### B.5.2:7 - Conformance Checklist

- `CC-B.5.2-1` Every abductive run **SHALL** begin from a declared `U.AbductivePrompt`; arbitrary prose fragments are not sufficient entry surfaces.
- `CC-B.5.2-2` A conforming abductive run **SHALL** record at least one rival candidate alongside any selected prime hypothesis, unless the author explicitly justifies why no rival candidate was available.
- `CC-B.5.2-3` Selection of a prime hypothesis **SHALL** cite at least two explicit plausibility filters.
- `CC-B.5.2-4` The selected prime hypothesis **SHALL** be published as a new `U.Episteme` with `AssuranceLevel:L0`.
- `CC-B.5.2-5` The prime hypothesis record **SHALL** preserve a link to the initiating prompt and to the filtering rationale that justified selection.
- `CC-B.5.2-6` A hypothesis that cannot support any downstream deduction, probe design, or evidence path **SHALL NOT** be presented as a conforming abductive result.

### B.5.2:8 - Common Anti-Patterns and How to Avoid Them

| Anti-pattern | What it looks like | How FPF prevents it |
|---|---|---|
| **Authority candidate** | One favored conjecture is advanced immediately, with no rival set and no explicit filtering. | `CC-B.5.2-2` and `CC-B.5.2-3` require candidate plurality and visible plausibility grounds. |
| **Untestable grand conjecture** | The candidate sounds deep or comprehensive, but it creates no lawful next step for checking, probing, or deduction. | `CC-B.5.2-6` rejects prime hypotheses that cannot open a downstream path. |
| **Prompt amnesia** | A later reader can see the conjecture but not the initiating anomaly, opportunity, or probe pressure. | `CC-B.5.2-1` and `CC-B.5.2-5` keep prompt provenance attached. |
| **Symptom patching** | The selected candidate only redescribes a visible symptom and leaves the actual prompt unresolved. | The explicit plausibility filter for explanatory reach forces the candidate to be compared against the whole prompt. |

### B.5.2:9 - Consequences

| Benefit | Trade-off / Mitigation |
|---|---|
| **Disciplined generativity.** Abduction stays inventive without collapsing into formless conjecturing. | Requires explicit prompt and filter publication; mitigation: the required record can remain lightweight. |
| **Traceable hypothesis origin.** Later review can reconstruct why a conjecture entered the reasoning cycle. | Adds a small provenance burden; mitigation: reuse prompt and candidate-set notes from adjacent patterns. |
| **Cleaner downstream handoff.** Deduction and evidence work begin from an `L0` artifact with explicit scope and rationale. | Some early conjectures will be rejected sooner; that is a feature, not a defect. |
| **Lawful reopening.** Rival candidates can be revisited when later work weakens the selected prime hypothesis. | Demands editorial discipline so that abandoned rivals remain legible rather than silently vanishing. |

### B.5.2:10 - Rationale

The Canonical Reasoning Cycle needs a disciplined beginning that is neither over-formalized nor mystical. `B.5.2` supplies that beginning. It keeps hypothesis generation explicit, connects it to typed entry surfaces, and prepares the output for later assurance work without pretending that early plausibility is already evidence.

### B.5.2:11 - SoTA-Echoing

Contemporary inquiry practice in science, engineering, design, and diagnosis treats candidate generation as iterative and contrast-driven rather than singular and opaque. The pattern aligns with that practice, but keeps the representation lightweight: explicit prompts, visible rival candidates, and local plausibility grounds instead of heavyweight ideation machinery.

### B.5.2:12 - Relations

- **Is the first reasoning phase within:** `B.5 Canonical Reasoning Cycle`.
- **Typically operates during:** `B.5.1 Exploration`.
- **Consumes:** `U.AbductivePrompt` surfaces from `B.5.2.0`, often reached through `B.4.1` and `A.16`.
- **Produces:** hypothesis-bearing `U.Episteme` artifacts at `AssuranceLevel:L0`.
- **Feeds:** downstream deduction, probe design, and evidence acquisition in the later reasoning cycle.

#### B.5.2:12.1 - Entry-surface broadening via `U.AbductivePrompt`

Older wording that makes `AnomalyStatement` the exclusive entry surface is superseded. `B.5.2` accepts `U.AbductivePrompt`, where `AnomalyStatement` remains one canonical species alongside cue-derived prompt species such as `ProblemCuePrompt`, `OpportunityCuePrompt`, and `ProbeCuePrompt`.


### B.5.2:13 - Prompt, Candidate, and Hypothesis Package Discipline

The abductive loop stays auditable only if the three main publication forms remain distinct: the **prompt**, the **candidate set**, and the **selected prime hypothesis**. Collapsing them into one paragraph is one of the main reasons later review cannot reconstruct what actually happened.

#### B.5.2:13.1 - Prompt package

A conforming prompt package should make explicit:

- the **prompt species** (`AnomalyStatement`, `ProblemCuePrompt`, `OpportunityCuePrompt`, or `ProbeCuePrompt`),
- the **open question** that makes abduction necessary,
- the **declared scope** under which the question is being posed,
- the **witnesses or provenance cues** that made the prompt worth preserving,
- and the **reason the current model is insufficient**.

If the initiating publication is still primarily evaluative, action-inviting, or lexically overloaded, it should first be repaired by the relevant A.6 family before it is treated as a stable abductive prompt. `B.5.2` assumes typed entry, not raw lexical ambiguity.

#### B.5.2:13.2 - Candidate-set note

A candidate-set note is the minimal record that preserves rival plurality. It need not be heavy, but it should make visible:

- candidate identifiers or short names,
- the differentiating claim each candidate adds,
- the principal plausibility strengths and liabilities of each candidate,
- whether the candidate remains live, is deferred, or is rejected,
- and what missing evidence or probe would most strongly discriminate among the remaining rivals.

The important point is not bureaucratic completeness. The important point is to prevent retrospective rewriting in which the surviving candidate is made to look as if it had been the only serious option from the beginning.

#### B.5.2:13.3 - Prime-hypothesis record

A selected prime hypothesis should preserve more than the hypothesis sentence itself. A conforming `L0` hypothesis record should name:

- the **selected candidate**,
- the **prompt** it answers,
- the **filters** under which it outranked rivals,
- the **scope** within which it is being advanced,
- the **next lawful downstream move** (deduction, probe design, targeted evidence acquisition, or explicit reopening criteria),
- and any **known fragilities** already visible at selection time.

This is how `B.5.2` stays connected to the rest of the reasoning cycle. The abductive loop does not merely emit an idea; it emits a conjecture with an explicit handoff contract.

### B.5.2:14 - Lawful Transitions, Abort Paths, and Reopening

The abductive loop is iterative, but it is not formless. Several transition cases need explicit handling so that later stages know whether they are receiving a stable `L0` conjecture, a deferred candidate, or a prompt that should be reopened rather than forced forward.

#### B.5.2:14.1 - Relation to `B.4.1` and `A.16`

`B.4.1` and `A.16` often supply the pre-abductive seam. They help preserve, stabilize, and route upstream publications before they are fit for explicit conjecture. `B.5.2` begins only once the current publication is ready to function as an abductive prompt. This boundary matters because it prevents two opposite errors:

- **premature abduction**, where a weak cue is treated as if it had already earned hypothesis form;
- **delayed abduction**, where a now-stable prompt is kept indefinitely in early cue form even though rival conjectures should already be compared.

#### B.5.2:14.2 - Abort, defer, and split cases

Not every abductive run should end in a prime hypothesis. Three non-selection outcomes are lawful:

1. **Abort.** The prompt dissolves because the initiating anomaly or opportunity was misread, duplicated, or already answered elsewhere.
2. **Defer.** Several candidates remain live, but the discriminating evidence or probe is not yet available. The loop pauses without pretending a winner exists.
3. **Split.** The original prompt turns out to contain several distinct questions. The run should fork into several narrower prompts rather than select one over-broad conjecture.

These outcomes are not failures. They are part of keeping abduction honest.

#### B.5.2:14.3 - Reopening and rival reinstatement

A prime hypothesis may later weaken under deduction, probe results, or new evidence. When that happens, `B.5.2` prefers explicit reopening to silent replacement.

A conforming reopening note should identify:

- which prior prime hypothesis is being reopened,
- whether a stored rival is being reinstated or a new candidate is entering,
- what change in evidence, scope, or internal contradiction triggered the reopening,
- and whether the original prompt itself has changed or only the candidate ranking has changed.

This allows the reasoning cycle to keep continuity without pretending that the earlier abductive choice had never been made.

#### B.5.2:14.4 - Scope discipline during iteration

Abductive drift often comes from silent scope expansion. A conjecture first framed for one target slice quietly becomes a universal explanation. `B.5.2` therefore expects scope discipline to remain explicit during iteration. If a candidate requires a broader or narrower scope than the prompt originally declared, that scope move should be stated rather than smuggled in under the rhetoric of a "better explanation."

### B.5.2:15 - Worked Examples

#### B.5.2:15.1 - Service degradation diagnosis

A service team notices recurring latency spikes during one operating window. The prompt species is `AnomalyStatement`: *why does latency spike in the evening batch window despite unchanged nominal load?*

The candidate set includes:

- queue saturation in one downstream dependency,
- a time-window interaction with backup traffic,
- and a recent mechanism regression in cache invalidation.

The prime hypothesis is not selected because it sounds most familiar. It is selected because it best fits the observed window, remains consistent with known mechanism declarations, and generates a concrete next probe: isolate backup traffic and compare the latency shape against prior windows. The resulting conjecture becomes an `L0` hypothesis with one explicit evidence path.

#### B.5.2:15.2 - Opportunity-driven materials inquiry

A research group sees an opportunity rather than a failure: a new fabrication method appears to create a micro-structure with useful thermal behavior. The prompt species is `OpportunityCuePrompt` rather than anomaly.

Candidate hypotheses include:

- the effect is caused by surface geometry,
- it is caused by composition gradients,
- or it is an artefact of one measurement regime.

The selected prime hypothesis is the geometry explanation because it has stronger explanatory reach across the initial observations and yields a cleaner discriminating experiment. The loop shows why opportunity-driven abduction still needs rival tracking; without it, attractive novelty language would substitute for hypothesis discipline.

#### B.5.2:15.3 - Probe-driven theory repair

A theory-maintenance group identifies a probe-worthy mismatch between two accepted claims. The prompt species is `ProbeCuePrompt`: *what changed assumption would allow these two claims to coexist without contradiction?*

The candidate set includes:

- hidden scope restriction on the first claim,
- mistaken invariance assumption in the second,
- and a more general missing mediating construct.

The selected prime hypothesis is the mediating construct, but the scope-restriction candidate remains stored as a live rival because it could still outperform if later deductions fail. This example illustrates why `B.5.2` tracks the rival set rather than only the currently favored conjecture.

### B.5.2:16 - Authoring and Review Guidance

#### B.5.2:16.1 - For authors

Authors should treat the abductive loop as a **selection discipline**, not as a prose genre. The minimal questions are:

- what is the prompt,
- what rival candidates were seriously considered,
- why is one candidate currently the best live conjecture,
- and what downstream move could expose that selection as right or wrong?

If those answers cannot be given, the publication is probably not yet at `B.5.2` and should return to prompt-shaping or lexical repair.

#### B.5.2:16.2 - For reviewers

Reviewers should not ask only whether the chosen hypothesis looks plausible. They should also ask:

- whether the prompt was typed lawfully,
- whether at least one real rival was preserved,
- whether the filters named at selection time actually discriminate among candidates,
- whether the selected hypothesis has a credible downstream path,
- and whether any scope inflation occurred during selection.

A polished hypothesis with no visible rivals is usually less trustworthy than a rougher hypothesis whose rival space is explicit.

#### B.5.2:16.3 - For integrators and assurance leads

Integrators should remember that `L0` is still early assurance. `B.5.2` supplies disciplined conjectures, not corroborated claims. Its value is that it exposes where deduction, method design, and evidence acquisition should now concentrate. Assurance leads therefore should preserve the prompt link and the filter rationale rather than flattening the conjecture into a decontextualized work item.

### B.5.2:17 - Migration and Boundary Notes

#### B.5.2:17.1 - Migration from anomaly monopoly

Older wording that says abduction begins only from anomaly should be rewritten into the broader but still typed claim: abduction begins from a lawful `U.AbductivePrompt`, of which anomaly is one canonical species.

#### B.5.2:17.2 - Migration from inspiration rhetoric

Legacy prose that describes abduction as a flash, leap, or raw creative moment may remain as didactic metaphor, but it should not be used as the operational description of the pattern. The operational core is typed prompt -> rival set -> plausibility filtering -> prime hypothesis publication.

#### B.5.2:17.3 - Boundary to deduction and evidence

`B.5.2` ends when one conjecture is published as a prime `L0` hypothesis or when the run is explicitly aborted, deferred, or split. Deduction, evidence acquisition, and later assurance do not belong to the abductive loop itself, even though the loop must prepare a clean handoff to them.
### B.5.2:End

