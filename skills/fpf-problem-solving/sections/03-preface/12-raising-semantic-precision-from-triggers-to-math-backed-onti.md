## Raising Semantic Precision: From Triggers to Math‑Backed Ontics

FPF does not assume people will speak in fully‑typed relational algebra on day one. Early thought is sketchy, and that is healthy. What matters is having a repeatable upgrade path—a way to go from “useful but ambiguous” to “auditable and reusable” when a statement starts carrying load.

That upgrade is often called “formalization” in everyday speech, but in FPF it is a **semantic precision upgrade**: a small workflow that turns compressed language into structure you can reason about. “Formalization” is only one internal step: choosing a stable mathematical substrate so the reasoning cannot collapse back into vibes.

A good precision upgrade tends to follow five moves:

1. **Notice the triggers.** Umbrella verbs (“sync/align/ground/depends”), pronouns (“it/this”), and metonymic endpoints (“the service”, “production”) are not sins; they are alarms that a richer ontic fragment is hiding underneath.
2. **Unpack the ontic fragment.** Make the local mini‑ontology explicit: which kinds, roles, scopes, viewpoints, time selections, and evidence objects are actually in play.
3. **Put a stable mathematical object under it.** Choose a structure with known behaviour—record types with named slots, typed n‑ary relations / hyperedges, partial orders, lattices, graphs, effect signatures—so future edits become well‑posed transformations rather than rewrites of prose.
4. **Refactor the ontology to fit the substrate.** Split bundled notions, make participant positions explicit, declare invariants, and introduce named change classes for “what changed?” (retarget vs revise vs rescope, etc.).
5. **Mint precise lexemes and guardrails.** Give the refined concepts specific names and keep them paired across registers (Tech/Plain twins via **LEX‑BUNDLE**, E.10). Add lexical firewalls so the umbrella words don’t silently re‑enter and collapse distinctions again.

In the spec this precision‑upgrade move is captured as a family recipe (**A.6.P**, Relational Precision Restoration) and then specialised for recurring boundary pain points (slot discipline, basedness declarations, service polysemy, cross‑context “same”, contract unpacking). The point is not to ban natural language; the point is to make natural language *upgradeable*.

A tiny example illustrates the intent:

Before (fast speech): “We synced the model with production.”  
After (precision‑restored): declare *which* relation kind holds between *which* endpoints, under *which* scope/time/viewpoint, with *which* admissible change classes—and publish a Plain gloss that maps back to the Tech token.

Once the relation has a kind, slots, qualifiers, and a change lexicon, you can do what modern SoTA engineering expects: evolve it safely, compare editions, automate checks, and still keep the story readable for humans.

