## B.5.2.0 - `U.AbductivePrompt`

> **Type:** Definitional (D)
> **Status:** Draft
> **Normativity:** Normative unless marked informative

**Plain-name.** Abductive prompt.


### B.5.2.0:1 - Problem frame
`B.5.2` needs an entry form that can accept lawful language-state trajectories after cue preservation and routing, without pretending that anomaly is the only admissible starting form.

### B.5.2.0:2 - Problem
If anomaly is the only admissible input, pre-anomaly opportunity cues and route-derived prompt forms are excluded or misrepresented. If anything can enter, abduction loses its typed starting discipline.

### B.5.2.0:3 - Forces
| Force | Tension |
|---|---|
| **Breadth vs discipline** | Admit more than anomaly, but keep a bounded family of lawful prompt species. |
| **Reuse vs type inflation** | Introduce a clean entry form without exploding the number of heavy publication kinds. |
| **Prompt vs hypothesis** | Keep the initiating prompt distinct from the later abductive outcome. |

### B.5.2.0:4 - Solution
`U.AbductivePrompt` is a narrow supertype for the prompt forms that may lawfully seed `B.5.2` after lawful cue preservation and routing under `A.16`, `A.16.1`, and `B.4.1`. `A.16.0` is used only when the cue-to-prompt history itself has governance value as an explicit trajectory account. When rendered, a prompt uses ordinary MVPK faces; prompt status is a property of the publication form, not a rival face ontology.

#### B.5.2.0:4.1 - Starter canonical species
- `AnomalyStatement`
- `ProblemCuePrompt`
- `OpportunityCuePrompt`
- `ProbeCuePrompt`

#### B.5.2.0:4.2 - Core shape
A conforming abductive prompt may publish:

- `promptSpecies`
- `motivatingCueRef?`
- `openQuestion`
- `contrastSet?`
- `scope?`
- `witnessRefs?`
- `routeProvenance?`
- `GammaTime?`

A prompt is not yet a hypothesis. Prompt legality usually presupposes articulation high enough to publish a stable open question and closure low enough that rival answers remain live; those thresholds remain owned by `C.2.4` and `C.2.5`, typically reached through cue or route provenance from `A.16.1` and `B.4.1`. It is the initiating publication form that licenses entry into the abductive loop.

#### B.5.2.0:4.3 - Boundary rule
`U.AbductivePrompt` is an entry form, not an excuse to let arbitrary prose count as abductive input. Only declared prompt species may enter `B.5.2` through this form.

### B.5.2.0:5 - Archetypal Grounding
**Tell.** An anomaly is one prompt species, not the only one.

**Show (System).** A control cue may begin probe-design abduction even before it is framed as anomaly.

**Show (Episteme).** A promising mismatch can begin an opportunity-style abductive prompt rather than only a problem statement.

### B.5.2.0:6 - Bias-Annotation
The pattern broadens the entry form to abduction, but still keeps it typed and auditable.

### B.5.2.0:7 - Conformance Checklist
- `CC-B.5.2.0-1` Every `U.AbductivePrompt` **SHALL** declare its prompt species.
- `CC-B.5.2.0-2` A prompt **SHALL NOT** be confused with a finished hypothesis.
- `CC-B.5.2.0-3` Cue-derived prompts **SHOULD** preserve route provenance.
- `CC-B.5.2.0-4` Prompt publication **SHALL** include the open question that makes abduction appropriate.
- `CC-B.5.2.0-5` A publication that already fixes the answer or suppresses plausible rivals **SHALL NOT** remain in prompt status.

### B.5.2.0:8 - Common Anti-Patterns and How to Avoid Them
- **Prompt equals hypothesis.** Keep the prompt distinct from the abductive output.
- **Anything can begin abduction.** No: only declared prompt species can.
- **Route amnesia.** A cue-derived prompt loses the early route provenance that explains why it entered here.

### B.5.2.0:9 - Consequences
The benefit is a cleaner, less brittle entry contract for abduction. The trade-off is one additional explicit prompt supertype and one more declared publication form.

### B.5.2.0:10 - Rationale
This keeps lawful cue preservation and route publication able to dock into `B.5.2` through a typed prompt form without anomaly inflation and without making `A.16.0` mandatory.

### B.5.2.0:11 - SoTA-Echoing
The pattern reflects real abductive practice, where opportunities, probe prompts, and stabilized cues often begin the loop before a full anomaly formulation exists.

### B.5.2.0:12 - Relations
- Builds on: `C.2.2a`, `A.16`, `A.16.1`, `B.4.1`, `C.2.LS`, `C.2.4`, `C.2.5`.
- Coordinates with: `A.16.0`, `A.16.2`, `C.2.6`, `C.2.7`, `B.5.2`, `A.6.P`, `A.6.Q`, `A.6.A`, `F.9.1`.
- Constrains: lawful prompt entry into abduction.
### B.5.2.0:13 - Worked Prompt Species

#### B.5.2.0:13.1 - Anomaly statement as canonical prompt
An anomaly statement remains a canonical prompt species, especially when the contrast and failure condition are already explicit.

#### B.5.2.0:13.2 - Opportunity-style prompt
A cue may lawfully become an opportunity prompt when the open question concerns a potentially valuable line of probe or intervention rather than a failure description.

#### B.5.2.0:13.3 - Probe-style prompt
A routed cue may become a probe prompt when what matters is not yet explanation but the explicit need to test, contrast, instrument, or perturb.

### B.5.2.0:14 - Authoring and Review Guidance

#### B.5.2.0:14.1 - Author prompt
An abductive prompt should state:

- which prompt species it is,
- what open question it poses,
- what cue or route provenance justifies entry,
- and why the current publication is still a prompt rather than already a hypothesis.

#### B.5.2.0:14.2 - Review prompt
A reviewer should watch for the common mistake where authors silently upgrade a prompt into a hypothesis merely because the prose sounds explanatory.

#### B.5.2.0:14.3 - Provenance reminder
If the prompt came from a routed cue, route provenance should stay visible so that later abductive claims can be audited back to their originating form.

### B.5.2.0:15 - Migration and Invalid Entry Notes

#### B.5.2.0:15.1 - Migration from anomaly monopoly
Older statements such as "abduction begins only with anomaly" should be rewritten into the narrower claim that anomaly is one canonical prompt species among several lawful entry forms.

#### B.5.2.0:15.2 - Invalid entry case
A bare intuition, slogan, or rhetorical question with no prompt species and no cue provenance is not yet a lawful `U.AbductivePrompt`.
### B.5.2.0:16 - Prompt Package Discipline

A prompt becomes reusable in `B.5.2` only when its initiating question is explicit enough to remain stable across later hypothesis work.

#### B.5.2.0:16.1 - Minimal prompt package

A robust abductive prompt should make explicit:

- the **prompt species**,
- the **open question**,
- the **motivating cue or route provenance**,
- the **contrast set**, if one is already visible,
- the **scope** in which the question is being asked,
- and the **witnesses or cue grounds** that justify beginning abduction.

This package lets later conjectures be tested against the same question rather than against a later paraphrase.

#### B.5.2.0:16.2 - Prompts are questions, not claims

A prompt may imply pressure toward one explanation, but it remains a question-bearing entry form. If the text already asserts the answer, it has moved past prompt status and should be treated under `B.5.2` or another later owner.

#### B.5.2.0:16.3 - Prompt provenance remains load-bearing

Route provenance, cue provenance, and witness provenance are part of prompt legality, not optional history.

### B.5.2.0:17 - Species Boundary Tests

#### B.5.2.0:17.1 - `AnomalyStatement`

Use anomaly species when the key form is an explicit failure, contradiction, or surprising departure from what the current model expected.

#### B.5.2.0:17.2 - `ProblemCuePrompt`

Use this species when the current cue-derived publication has become problem-shaped enough to justify abductive entry, but is still better described as a cue-derived problem prompt than as a fully stabilized anomaly statement.

Cue-derived labels such as `ProblemCueProjection`, `OpportunityCueProjection`, and `ProbeCueProjection` should be retired in favor of prompt-headed species names. The prompt kind is load-bearing; the older labels over-signalled the narrowing move and under-signalled the actual owner.

#### B.5.2.0:17.3 - `OpportunityCuePrompt`

Use opportunity species when the pressure comes from a promising line of development or advantageous contrast, not primarily from failure or contradiction.

#### B.5.2.0:17.4 - `ProbeCuePrompt`

Use probe species when what matters is the need to instrument, contrast, perturb, or ask a question that could discriminate among several future explanations.

These tests are not lexical ornaments. They keep different prompt pressures from collapsing into one anomaly-shaped template.

### B.5.2.0:18 - Handoff, Deferral, and Invalid Prompt Drift

#### B.5.2.0:18.1 - Handoff to `B.5.2`

A prompt should enter `B.5.2` only when the question is explicit enough that rival hypotheses can now be compared against it. If the question is still too weakly articulated, the lawful continuation is further stabilization or routing, not premature abduction.

#### B.5.2.0:18.2 - Deferred prompt entry

A routed cue may be close to prompt form but still missing one decisive contrast or witness. In such cases the prompt may be deferred explicitly rather than forced into `U.AbductivePrompt` before its initiating question is stable.

#### B.5.2.0:18.3 - Invalid prompt drift

A common failure mode is drift from cue -> prompt -> hypothesis without anyone naming the boundary crossings. `B.5.2.0` blocks that drift by keeping the prompt package distinct from both the earlier cue pack and the later prime hypothesis. The point is to keep the starting question stable and reviewable.

### B.5.2.0:19 - Review Tests for Prompt Readiness

A reviewer can test prompt readiness with three questions:

1. **Is there a real open question?** If the text already asserts the answer, it is no longer a prompt.
2. **Is the prompt species plausible?** If the initiating pressure is opportunity-shaped or probe-shaped, forcing anomaly species is a category error.
3. **Could rival hypotheses now be compared against this prompt?** If not, the prompt candidate probably needs more stabilization before entering `B.5.2`.

These tests keep the prompt layer narrow and help prevent the common drift where every interesting sentence is treated as abductive input.
### B.5.2.0:20 - Prompt Scope and Rival-Set Discipline

#### B.5.2.0:20.1 - Scope must be stated narrowly enough
A prompt should declare the scope in which its question is being asked: the domain fragment, operational horizon, or inquiry slice that makes the question answerable. If scope remains unbounded, rival hypotheses will later become incomparable because they are answering different questions.

#### B.5.2.0:20.2 - Rival-set anticipation
A prompt need not list full hypotheses yet, but it should make visible whether rival answer types are already imaginable. If no rival answer space is even latent, the publication may still be a cue or orientation note rather than a true abductive prompt.

#### B.5.2.0:20.3 - Prompt narrowing without answer smuggling
A prompt may be narrowed to become more discriminating, but the narrowing must not silently smuggle in the answer it is supposedly asking about. Otherwise the prompt ceases to be an initiating question and becomes a disguised conclusion.

### B.5.2.0:21 - Prompt Composition and Comparative Validity

#### B.5.2.0:21.1 - One prompt versus prompt bundle
A note may legitimately contain a bundle of closely related prompts. If so, the bundle members should be distinguishable. Treating several open questions as one prompt is only lawful if the bundle still supports later rival comparison without confusion.

#### B.5.2.0:21.2 - Comparative prompt use
Prompts may be compared across contexts only when their species, scope, and provenance are explicit. A probe-shaped question and an opportunity-shaped question are not the same kind of abductive entry merely because both invite explanation.

#### B.5.2.0:21.3 - Boundary to hypothesis preloading
If a prompt already excludes every serious rival except one preferred explanatory line, the publication may already be preloading a hypothesis. Review should then either weaken the prompt back into a real question or promote the later owner explicitly.

### B.5.2.0:22 - Review Addendum for Prompt Readiness

Add three checks to the base prompt tests:

- **Is the scope tight enough for later comparison?**
- **Is there an imaginable rival-set, even if not yet fully written?**
- **Has narrowing turned the question into a disguised answer?**

These checks keep `U.AbductivePrompt` a genuine entry form for later abductive work rather than a rhetorical preloading device.

### B.5.2.0:End


