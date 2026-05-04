## C.2.6 - `U.LanguageStateAnchoringMode`

> **Type:** Definitional (D)
> **Status:** Draft
> **Normativity:** Normative unless marked informative

**Plain-name.** Language-state anchoring mode.


### C.2.6:1 - Problem frame
Published position claims in the declared language-state chart over `U.CharacteristicSpace` differ not only by articulation and closure, but by how the governed `U.Episteme` in that claim is anchored to bodies, traces, model states, documents, or operator loops.

### C.2.6:2 - Problem
Without an explicit owner, embodiment and source anchoring are smuggled into informal prose or folded into representation terms. That weakens cue comparison, weakens bridge loss notes, and turns operator-facing language-state work into a special case with no explicit home.

### C.2.6:3 - Forces
| Force | Tension |
|---|---|
| **Embodiment vs abstraction** | Preserve embodied and operator-facing cases without making them mystical exceptions. |
| **Small core vs real diversity** | Keep the core compact while allowing multiple lawful anchoring regimes. |
| **Comparability vs oversimplification** | Compare anchoring regimes without flattening them into text-vs-nontext slogans. |

### C.2.6:4 - Solution
`U.LanguageStateAnchoringMode` is a nominal characteristic that states the primary anchoring regime of the governed `U.Episteme` named by the current position claim: bodily enactment, trace, model state, document, operator loop, or an explicit mixed regime. If source anchoring and current publication-face anchoring differ, both shall be distinguished rather than collapsed.

#### C.2.6:4.1 - Starter family
| Mode | Reading | Typical evidence anchor |
|---|---|---|
| `AM.EmbodiedFelt` | bodily or kinesthetic anchoring matters directly | embodiment note, felt trace, human witness |
| `AM.TraceAnchored` | traces, logs, telemetry traces, or observations anchor the episteme | trace references, measured events, observations |
| `AM.ModelLatent` | latent or internal model state is the key anchor | model-state refs, probe results, latent summaries |
| `AM.DocumentMediated` | document or description is the principal anchoring locus | documents, cards, procedure text |
| `AM.OperatorLoop` | the episteme is directly tied to operator intervention or console control | operator witness, console event, policy hook |
| `AM.Mixed` | more than one anchoring mode matters materially | explicit component list and why the mix matters |

#### C.2.6:4.2 - Owner boundary
`U.LanguageStateAnchoringMode` is not a representation factor bundle, not a closure state, and not a truth status. If embodiment matters, it shall be declared here or immediately beside this characteristic rather than being hidden inside representation talk.

#### C.2.6:4.3 - Mixed-mode rule
`AM.Mixed` is lawful only when the component modes are named explicitly. "Mixed" shall not be a lazy escape from deciding whether the key anchor is bodily, trace-based, model-latent, document-mediated, or operator-loop based.

#### C.2.6:4.4 - Bridge implications
Bridge work over governed `U.Episteme` publications in the declared language-state chart should pay attention to anchoring shifts. A translation from `AM.EmbodiedFelt` to `AM.DocumentMediated`, or from `AM.ModelLatent` to prose, often requires explicit loss notes in `F.9` and often justifies a stance annotation in `F.9.1`.

### C.2.6:5 - Archetypal Grounding
**Tell.** A felt cue, a controller-side probe score, and a textual design note may all be early cues, but they are anchored differently.

**Show (System).** An alert tied to an operator console is `AM.OperatorLoop`, not just "text".

**Show (Episteme).** A model-probe cue grounded in latent state is `AM.ModelLatent` even if it is later paraphrased into prose.

### C.2.6:6 - Bias-Annotation
The pattern pushes authors to declare anchoring rather than hide it in metaphors such as "the system wants" or "the note suggests".

### C.2.6:7 - Conformance Checklist
- `CC-C.2.6-1` Anchoring mode **SHALL NOT** be inferred from publication phrasing alone when it matters for routing, trust, or bridge interpretation.
- `CC-C.2.6-2` Embodiment-sensitive or operator-loop cases **SHOULD** declare the embodiment or operator anchor explicitly.
- `CC-C.2.6-3` `U.LanguageStateAnchoringMode` **MUST NOT** be collapsed into `U.LanguageStateRepresentationFactorBundle`.
- `CC-C.2.6-4` Mixed-mode declarations **SHALL** list their component modes explicitly.

### C.2.6:8 - Common Anti-Patterns and How to Avoid Them
- **Text-only illusion.** Treating every cue as document-mediated because it was written down later.
- **Representation capture.** Using symbolic/distributed labels to hide world-anchoring distinctions.
- **Embodiment mystification.** Treating bodily or operator-loop cues as beyond explicit publication.

### C.2.6:9 - Consequences
The benefit is cleaner reasoning about embodied, operator-facing, trace-based, and model-latent cues. The trade-off is more explicit declaration burden and more explicit bridge loss notes when modes shift.

### C.2.6:10 - Rationale
The declared language-state chart over `U.CharacteristicSpace` needs one explicit anchoring basis slot so that `A.16.0`, `A.16.1`, `B.4.1`, and `F.9.1` can refer to anchoring regime without re-owning it.

### C.2.6:11 - SoTA-Echoing
The facet is motivated by embodied cognition, operator-facing interaction practice, active inference, and modern model-probing practice, all of which distinguish cue content from anchoring regime.

### C.2.6:12 - Relations
- Builds on: `A.18`, `C.2.2a`, `C.2.LS`.
- Coordinates with: `A.7`, `A.16.0`, `A.16`, `A.16.1`, `B.4.1`, `B.5.2.0`, `C.2.7`, `F.9.1`.
- Constrains: cue publication and bridge loss notes.
### C.2.6:13 - Worked Examples and Bridge-Loss Cases

#### C.2.6:13.1 - Embodied-to-document shift
A bodily felt cue later published as prose usually changes from `AM.EmbodiedFelt` toward `AM.DocumentMediated`. That shift is not harmless; it often introduces bridge loss and should be treated as such when cross-context equivalence is claimed.

#### C.2.6:13.2 - Model-latent to operator-loop case
A latent probe score may first be `AM.ModelLatent`, then later feed an operator-facing alert face where the working publication becomes `AM.OperatorLoop`. A conforming account should keep both anchoring modes visible rather than pretending the later publication wording fully captures the model-side cue.

#### C.2.6:13.3 - Mixed-mode publication
A routed alert note may lawfully be `AM.Mixed` when it combines operator-loop anchoring, trace anchoring, and document mediation. But the mix must be named explicitly rather than used as a catch-all escape.

### C.2.6:14 - Authoring and Review Guidance

#### C.2.6:14.1 - Author prompt
When declaring anchoring mode, ask:

- what is the primary anchoring locus?
- does bodily or operator participation matter directly?
- is the key anchor trace-based, model-internal, or document-based?
- if multiple modes matter, which ones and why?

#### C.2.6:14.2 - Review prompt
A reviewer should watch for the common mistake where later prose formatting tricks authors into forgetting the original anchoring mode.

#### C.2.6:14.3 - Bridge note
If anchoring changes across publication or translation, `F.9` and `F.9.1` should often carry explicit loss or stance notes rather than silent equivalence language.

### C.2.6:15 - Extension and Migration Notes

#### C.2.6:15.1 - Local extension rule
Contexts may add local anchoring modes, but they should do so by extension of the starter family rather than by collapsing the family into a text-vs-world binary.

#### C.2.6:15.2 - Migration from metaphorical prose
Statements like "the system wants", "the note suggests", or "the operator-facing publication says" should be repaired by naming the actual anchoring mode and the actual detector/enactor or witness structure.

#### C.2.6:15.3 - Boundary reminder
`U.LanguageStateAnchoringMode` does not decide representation, articulation, closure, or trust by itself. It only names how the episteme is anchored.
### C.2.6:16 - Anchoring Publication Package Discipline

#### C.2.6:16.1 - Minimal anchoring package
A publishable `U.LanguageStateAnchoringMode` claim should normally identify:

- the primary anchoring locus;
- any directly relevant embodiment, operator, trace, model, or document witness;
- the transformation chain if the current note is not at the original anchoring site;
- any secondary modes that remain load-bearing.

This is especially important when the final wording is prose, because prose often hides the anchoring regime.

#### C.2.6:16.2 - Source-versus-face rule
Distinguish the anchoring mode of the source cue from the anchoring mode of the current publication face. A bodily cue later written into a document may still require `AM.EmbodiedFelt` as source mode and `AM.DocumentMediated` as publication face.

#### C.2.6:16.3 - Mixed-mode decomposition rule
`AM.Mixed` is lawful only when its component modes are named and the reason for the mixture is operationally real. It must not become a convenience label for an episteme that has not yet been analyzed.

### C.2.6:17 - Anchoring Shift and Transport Law

#### C.2.6:17.1 - Shift declaration rule
When an episteme crosses from one anchoring mode to another, state whether the shift is merely publication-level or whether it changes what can be preserved, compared, or trusted. A move from operator-loop enactment to report prose, for example, often drops timing, bodily load, and enactment friction.

#### C.2.6:17.2 - Bridge-loss handoff
If an anchoring shift matters across contexts, `F.9` or `F.9.1` should own the loss or stance note. `C.2.6` only requires the shift to be noticed and not misrepresented as lossless.

#### C.2.6:17.3 - Same-content illusion test
Two cues may be paraphrased into the same sentence while remaining differently anchored. If the anchoring regime differs, the cues are not automatically substitutable.

### C.2.6:18 - Review Matrix and Extension Tests

#### C.2.6:18.1 - Review matrix
A reviewer should ask:

- what the original anchoring regime was;
- what the current publication regime is;
- whether the transformation chain is explicit;
- whether any bridge loss or stance note is missing;
- whether a declared mixed mode is genuinely decomposed.

#### C.2.6:18.2 - Local extension test
A new local anchoring mode is justified only when it answers a distinct anchoring question that the starter family cannot express without distortion.

#### C.2.6:18.3 - Cross-facet reminder
Anchoring mode often correlates with representation and articulation changes, but it does not own them. Reject prose that uses `AM.ModelLatent`, `AM.EmbodiedFelt`, or `AM.OperatorLoop` as shorthand for being vague, early, trustworthy, or closed.

### C.2.6:End

