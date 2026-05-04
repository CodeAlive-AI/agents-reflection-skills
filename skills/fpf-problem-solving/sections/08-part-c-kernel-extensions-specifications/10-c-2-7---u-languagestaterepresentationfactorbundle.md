## C.2.7 - `U.LanguageStateRepresentationFactorBundle`

> **Type:** Definitional (D)
> **Status:** Draft
> **Normativity:** Normative unless marked informative

**Plain-name.** Language-state representation-factor bundle.


### C.2.7:1 - Problem frame
Published position claims in the declared language-state chart over `U.CharacteristicSpace` must distinguish representation factors such as locality, sparsity, and symbolicity without pretending they form one master axis.

### C.2.7:2 - Problem
Terms such as `EncodingBasis` collapse several independent choices. That makes comparison brittle and encourages one-dimensional stories such as distributed = informal or local = precise.

### C.2.7:3 - Forces
| Force | Tension |
|---|---|
| **Comparability vs reductionism** | Allow comparison without compressing several factors into one slogan. |
| **Compact core vs extensibility** | Keep a minimal starter bundle while leaving room for domain-specific refinements. |
| **Representation vs anchoring** | Describe how the current episteme is represented without hiding what it is anchored to. |

### C.2.7:4 - Solution
`U.LanguageStateRepresentationFactorBundle` is a factor bundle, not one scalar characteristic. The minimal core starter set is:

- `U.LocalityDistribution`
- `U.Sparsity`
- `U.Symbolicity`

A Context may publish a local alias such as `EncodingBasis`, but it shall dock back to the underlying factor bundle instead of replacing it.

#### C.2.7:4.1 - Minimal factor readings
| Factor | Question it answers | Typical values |
|---|---|---|
| `LocalityDistribution` | Is the representation concentrated in local units or distributed across many units? | local / mixed / distributed |
| `Sparsity` | How concentrated is activation or descriptive support? | sparse / mixed / dense |
| `Symbolicity` | How explicit are the symbolic structures and tokens? | symbolic / mixed / subsymbolic |

#### C.2.7:4.2 - Non-collapse rules
`LanguageStateRepresentationFactorBundle` is not:

- `LanguageStateAnchoringMode`;
- `Formality`;
- `ArticulationExplicitness`;
- `LanguageStateClosureDegree`.

A representation may be distributed yet strongly trace-anchored; symbolic yet weakly articulated; sparse yet low-closure. Those combinations shall remain visible.

#### C.2.7:4.3 - Extension rule
Contexts may add extra representation factors only if the extension is published as a factor addition rather than as a new master axis that erases the core factor bundle.

### C.2.7:5 - Archetypal Grounding
**Tell.** A model-state cue can be highly distributed but still strongly trace-anchored; a symbolic note can be low articulation if its semantics are still vague.

**Show (System).** An operator decision aid may mix sparse alert codes and symbolic procedure text.

**Show (Episteme).** A research probe can move from distributed activation patterns to sparse symbolic hypotheses without any one-step formality story.

### C.2.7:6 - Bias-Annotation
The pattern resists folk theories that try to line up one representation axis with one stage or progression story.

### C.2.7:7 - Conformance Checklist
- `CC-C.2.7-1` `LanguageStateRepresentationFactorBundle` **SHALL** be published as a factor bundle, not as a hidden scalar.
- `CC-C.2.7-2` Local aliases such as `EncodingBasis` **MAY** exist only with an explicit docking to the owned factors.
- `CC-C.2.7-3` Representation factors **MUST NOT** silently replace `LanguageStateAnchoringMode` or `LanguageStateClosureDegree`.
- `CC-C.2.7-4` New local factors **SHALL** preserve the factor-bundle discipline.

### C.2.7:8 - Common Anti-Patterns and How to Avoid Them
- **One-axis myth.** Treating distributed/local or symbolic/subsymbolic as the whole story.
- **Progression collapse.** Equating representation shifts with formalization or closure.
- **Alias capture.** Letting `EncodingBasis` or a similar local alias erase the factor bundle.

### C.2.7:9 - Consequences
The benefit is cleaner comparison across schools, substrates, and publication forms. The trade-off is that representation talk becomes more explicit and less slogan-friendly.

### C.2.7:10 - Rationale
The factor-bundle design keeps the representation basis-slot family in the declared language-state chart over `U.CharacteristicSpace` orthogonal to articulation, closure, and anchoring.

### C.2.7:11 - SoTA-Echoing
This factorization fits current work on sparse distributed representations, symbolic/neuro-symbolic stacks, and interpretability practice.

### C.2.7:12 - Relations
- Builds on: `A.18`, `C.2.2a`, `C.2.LS`.
- Coordinates with: `C.2.6`, `A.16.0`, `A.16`, `A.16.1`, `B.4.1`, `B.5.2.0`, `F.9.1`.
- Constrains: language-state position publication and bridge loss notes around representation shifts.
### C.2.7:13 - Worked Examples and Factor Interaction Notes

#### C.2.7:13.1 - Distributed but explicit
A model-side summary may be representation-wise distributed and still highly explicit once published into a stable symbolic wrapper. This case matters because it blocks the folk myth that distributed implies vague.

#### C.2.7:13.2 - Symbolic but still weakly articulated
A glossary-like note may be fully symbolic while still low in `AE` because the semantic anchors are not yet stabilized. This blocks the opposite myth: symbolic therefore explicit.

#### C.2.7:13.3 - Mixed-stack publication
An operator-facing publication face may combine sparse alert codes, symbolic procedure text, and distributed back-end model summaries. The representation-factor bundle should make that mixture visible instead of compressing it into one label.

### C.2.7:14 - Authoring and Review Guidance

#### C.2.7:14.1 - Author prompt
To publish a representation-factor bundle, ask separately:

- how local or distributed is the representation?
- how sparse or dense is it?
- how symbolic or subsymbolic is it?
- which additional factor, if any, genuinely matters enough to publish?

#### C.2.7:14.2 - Review prompt
A reviewer should reject any attempt to use one factor as if it summarized the rest. The factor bundle exists precisely to block that reduction.

#### C.2.7:14.3 - Cross-facet reminder
Reviewers should also watch for silent replacement of `LanguageStateAnchoringMode`, `AE`, or `CD` by representation talk.

### C.2.7:15 - Extension and Migration Notes

#### C.2.7:15.1 - Local extension rule
Contexts may add extra factors, but each added factor should answer a distinct question rather than duplicating locality, sparsity, or symbolicity under another label.

#### C.2.7:15.2 - Migration from alias-heavy prose
Aliases such as `EncodingBasis` or similar should be unfolded into explicit factor dockings before they are relied upon for routing, comparison, or bridge claims.

#### C.2.7:15.3 - Boundary reminder
`U.LanguageStateRepresentationFactorBundle` describes representational organization only. It does not determine route authority, closure, or anchoring by itself.
### C.2.7:16 - Factor-Bundle Publication Discipline

#### C.2.7:16.1 - Minimal representation package
A publishable `U.LanguageStateRepresentationFactorBundle` should normally show the current factor settings for locality/distribution, sparsity/density, and symbolicity/subsymbolicity, together with any declared extra factor. If a factor is intentionally omitted, say so rather than hiding the omission under a compact alias.

#### C.2.7:16.2 - No hidden scalar rule
Compact overlays such as "sparse-symbolic" are lawful only when they dock to the underlying factor bundle. No compact label may behave as a hidden master score for routing, bridge comparison, or stage/progression talk.

#### C.2.7:16.3 - Alias docking rule
Local aliases such as `EncodingBasis` are lawful only when their docking to the owned factors is explicit and stable. If an alias compresses several factors, the compression should remain visible.

### C.2.7:17 - Factor Interaction and Cross-Facet Reading Law

#### C.2.7:17.1 - Interaction law
Representation factors may correlate, but they do not determine one another. Highly distributed cues can still be sparse; symbolic publications can still be locally dense; mixed symbolicity can coexist with either strong or weak articulation. Publish the actual factor bundle rather than narrating one factor as if it predicted the rest.

#### C.2.7:17.2 - Cross-facet non-substitution
Representation talk must not silently replace `AE`, `CD`, or `LanguageStateAnchoringMode`. A shift from distributed to symbolic publication may change readability while leaving articulation low, closure open, or anchoring heavily operator-bound.

#### C.2.7:17.3 - Bridge reminder
If a representation shift matters in transport across contexts, note that the shift may alter what is preserved or salient. The bridge itself remains owned by `F.9` and `F.9.1`.

### C.2.7:18 - Review Matrix and Extension Tests

#### C.2.7:18.1 - Review matrix
A reviewer should ask:

- are all claimed factors visible in the publication or cited source;
- does any alias hide the factor bundle;
- is one factor being used as if it summarized the whole representation state;
- has representation talk started to replace articulation, closure, or anchoring claims.

#### C.2.7:18.2 - Local extension test
An additional factor is justified only if it captures a distinct representational question that cannot be reduced to locality, sparsity, or symbolicity. The extra factor should extend the bundle, not become a rival master axis.

#### C.2.7:18.3 - Migration test for legacy terminology
Legacy vocabularies often use "symbolic", "distributed", or "encoding basis" as if one term solved the whole classification problem. A conforming migration unpacks the term into explicit factor dockings and then checks whether any cross-facet claims were smuggled into the old label.

#### C.2.7:18.4 - Bundle-comparison reminder
Representation bundles may be compared across contexts only after the compared factors are explicit. If one context uses a compact local alias and another publishes the full factor bundle, require explicit docking before treating the two descriptions as commensurable.

### C.2.7:End


