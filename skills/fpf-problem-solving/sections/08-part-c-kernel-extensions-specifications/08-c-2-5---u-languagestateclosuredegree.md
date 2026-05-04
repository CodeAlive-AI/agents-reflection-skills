## C.2.5 - `U.LanguageStateClosureDegree`

> **Type:** Definitional (D)
> **Status:** Draft
> **Normativity:** Normative unless marked informative

**Plain-name.** Language-state closure degree.


### C.2.5:1 - Problem frame
A governed `U.Episteme` may already be explicit enough for publication while its declared position claim remains intentionally open to rival routes or frames. The declared language-state chart over `U.CharacteristicSpace` therefore needs a separate basis-slot owner for how fixed or closed the current candidate space has become.

### C.2.5:2 - Problem
Closure is often hidden inside vague words such as "ready", "settled", or "open". When closure is not explicit, teams cannot reason cleanly about reopen, sketch-backoff, or the admissibility of endpoint docking.

### C.2.5:3 - Forces
| Force | Tension |
|---|---|
| **Commitment vs exploration** | Preserve open search without losing auditability. |
| **Stability vs reversibility** | Allow closure increases, but also lawful reopening and reframing. |
| **Authority vs explicit retreat** | Let strong closure matter, but keep visible the moves that relax it. |

### C.2.5:4 - Solution
`U.LanguageStateClosureDegree` is an ordinal characteristic over how fixed the current candidate set, framing, and admissible next moves are in a published position claim in the declared language-state chart over `U.CharacteristicSpace`.

#### C.2.5:4.1 - Characteristic contract
- **Kind:** CHR characteristic.
- **Scale discipline:** ordinal.
- **What rises:** the local state becomes more fixed or more binding.
- **What does not follow automatically:** truth, trust, formality, or quality.

#### C.2.5:4.2 - Starter anchor set
| Anchor | Reading | Typical governance effect |
|---|---|---|
| `CD0` | exploratory-open | broad rival space remains live |
| `CD1` | weakly stabilized | some contrasts are present, but rival routes remain normal |
| `CD2` | narrowed candidate space | explicit rivals remain, but the field is meaningfully reduced |
| `CD3` | selected route or framing | one route is chosen, though reopening remains routine |
| `CD4` | publication- or operation-fixed under guard | changes require named justification |
| `CD5` | strongly fixed | relaxation requires an explicit `A.16.2` move and governance note |

#### C.2.5:4.3 - Non-collapse rules
`LanguageStateClosureDegree` is not:

- `F`;
- articulation explicitness;
- gate decision;
- evaluator confidence;
- warrant strength.

A text may be highly explicit but weakly closed, or weakly explicit but already strongly closed by policy. Those states shall not be collapsed.

#### C.2.5:4.4 - Change discipline
Increasing `CD` requires narrowing candidate space, route space, or frame space explicitly. Lowering `CD` is lawful only through a named move such as `reopen`, `sketchBackoff`, or `respecify`, with a retained-witness and discarded-assumption note.

### C.2.5:5 - Archetypal Grounding
**Tell.** Two notes may look equally explicit, but one is still intentionally open while the other is already committed to a single route.

**Show (System).** An incident cue can be routed to rollback while remaining reopenable if new evidence arrives.

**Show (Episteme).** A hypothesis sketch can be highly articulated but still low closure because rival explanations remain live.

### C.2.5:6 - Bias-Annotation
The pattern makes closure explicit, which resists hidden overconfidence but may feel heavy to authors who prefer implicit consensus.

### C.2.5:7 - Conformance Checklist
- `CC-C.2.5-1` Closure **SHALL** be declared independently from `F` and `AE` when it matters for routing, docking, or reopening.
- `CC-C.2.5-2` Reopen/backoff moves **SHALL** cite the prior closure state they are relaxing.
- `CC-C.2.5-3` Strong-closure states **SHOULD** name the guard or owner that makes the closure binding.
- `CC-C.2.5-4` Endpoint authority **SHALL NOT** survive a closure drop silently when the supporting route or publication form no longer holds.

### C.2.5:8 - Common Anti-Patterns and How to Avoid Them
- **Closure by mood.** A sentence sounds decisive, so teams assume high closure. Publish `CD` explicitly.
- **Irreversible drift.** Closure rises informally but no reopen path exists. Use `A.16.2`.
- **Authority smuggling.** High closure is treated as if it were automatically a gate or obligation. Route those consequences through the proper owners.

### C.2.5:9 - Consequences
The benefit is lawful handling of stabilization, commitment, and reopening. The trade-off is more explicit state declaration and more explicit retreat records.

### C.2.5:10 - Rationale
Closure is the route-governance basis slot that complements articulation within the declared language-state chart over `U.CharacteristicSpace`. `A.16.0` and its seam species need both.

### C.2.5:11 - SoTA-Echoing
The facet aligns with iterative design, open-world reasoning, and exploratory search practices where closure is a governance choice rather than a hidden by-product.

### C.2.5:12 - Relations
- Builds on: `A.18`, `C.2.2a`, `C.2.LS`.
- Coordinates with: `C.2.4`, `A.16.0`, `A.16`, `A.16.1`, `A.16.2`, `B.4.1`, `B.5.2.0`.
- Constrains: reopen, backoff, and endpoint docking guards.
### C.2.5:13 - Worked Examples and Retreat Cases

#### C.2.5:13.1 - Explicit but still open
A note may sit at `AE4` yet only `CD1` because rival explanatory frames are still live. The important lesson is that explicit publication does not imply settled closure.

#### C.2.5:13.2 - Strong closure under policy guard
An operator rule may be only moderate in `AE` but high in `CD` because policy already fixes the next step under the current horizon. This shows why closure is governance-facing, not merely stylistic.

#### C.2.5:13.3 - Reopen case
A route may move from `CD4` back to `CD2` when counter-evidence appears. A conforming publication does not hide this as embarrassment; it records the retreat as a lawful `A.16.2` move.

### C.2.5:14 - Authoring and Review Guidance

#### C.2.5:14.1 - Author prompt
To assign `CD`, ask:

- how many rivals remain live?
- is one route merely preferred, or actually fixed?
- what guard or owner makes the closure binding?
- what would count as a lawful reopen trigger?

#### C.2.5:14.2 - Review prompt
A reviewer should ask whether closure is being inferred from tone, from hierarchy, or from social pressure rather than from an explicit narrowing of route or frame space.

#### C.2.5:14.3 - Governance note
Whenever `CD` materially affects gates, commitments, or late endpoint authority, the supporting guard or owner should be visible.

### C.2.5:15 - Extension and Migration Notes

#### C.2.5:15.1 - Local anchor refinement
Contexts may refine the starter closure anchors, but shall keep the ordinal progression and the explicit link to reopen/backoff discipline.

#### C.2.5:15.2 - Migration from readiness language
Words such as "settled", "closed", "final", or "open" should be treated as migration prompts into explicit `CD` claims and, where needed, into named `A.16.2` moves.

#### C.2.5:15.3 - Boundary reminder
`CD` is not warrant strength and not a gate decision. It speaks only about the local fixity of the current episteme/publication path and its candidate space.
### C.2.5:16 - Closure Publication Package Discipline

#### C.2.5:16.1 - Minimal closure package
A publishable `CD` claim should name what has narrowed:

- the rival routes or frames that remain live;
- the route, frame, or interpretation that is currently privileged or fixed;
- the guard, owner, or policy that makes the narrowing binding;
- the condition under which a lawful reopen or backoff would occur.

A bare claim such as "now settled" is insufficient when closure affects routing or authority.

#### C.2.5:16.2 - Narrowing-source rule
Closure may rise because evidence eliminates rivals, governance temporarily binds a route, or protocol requires fixation under time pressure. State the source of narrowing because different sources imply different reopen expectations.

#### C.2.5:16.3 - Partial-closure rule
Closure may be local rather than global. A note can be closed enough for one route while remaining open about broader explanation or classification; a prompt may be fixed enough to hold one question steady while still open enough that rival answers remain live. Publish that locality explicitly.

### C.2.5:17 - Retained and Withdrawn Authority Handling

#### C.2.5:17.1 - Authority retention rule
If higher `CD` carried endpoint expectations, guard pressure, or route commitments, a later closure drop must say which consequences remain and which are withdrawn.

#### C.2.5:17.2 - Lawful retreat record
A lawful retreat through `reopen`, `sketchBackoff`, or `respecify` should retain:

- the prior closure state;
- the reason the prior fixation no longer holds;
- the assumption or route being relaxed;
- the still-binding remainder, if any.

This prevents false continuity after retreat.

#### C.2.5:17.3 - Closure versus obligation boundary
High `CD` may coexist with obligations, but `CD` is not itself an obligation owner. When prose treats "closed" as "must now be done", reroute the claim through the actual owner.

### C.2.5:18 - Review Matrix and Reopen Tests

#### C.2.5:18.1 - Review matrix
A reviewer should ask:

- what was narrowed;
- by what owner or guard it was narrowed;
- what would reopen it;
- whether any downstream authority survives the claimed closure level;
- whether the publication distinguishes local closure from whole-context finality.

#### C.2.5:18.2 - False-finality test
Words such as "final", "settled", or "decided" should be challenged unless the route/guard package is explicit. Final-sounding rhetoric often overstates actual closure.

#### C.2.5:18.3 - Cross-facet reminder
Low `CD` does not imply low articulation, weak anchoring, or poor representation. Reviewers should not treat openness as low seriousness.

#### C.2.5:18.4 - Split-closure review case
A publication may be closed enough for immediate local action while remaining open about broader explanation, long-horizon consequences, or alternative classification. Allow the split when locality is explicit; reject prose that advertises whole-case finality when only one route segment is fixed.

### C.2.5:End

