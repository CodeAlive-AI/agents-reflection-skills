## Boundary Statements: Where Language Becomes a System Boundary

Most of the time we can think in fast, compressed speech. Teams say “it’s the same”, “we synced it”, “the service guarantees”, “this is compliant”, and everyone roughly knows what is meant. Nothing explodes—until that sentence crosses a boundary: it lands in an interface, a safety case, an evaluation protocol, a contract, or a dashboard used for a go/no‑go decision.

At the boundary, prose stops being “just communication” and starts behaving like a mechanism. Ambiguity becomes a latent defect: it forks viewpoints, hides obligations, and later gets “patched” by politics rather than evidence.

In post‑2015 engineering practice, boundary text is everywhere:

- API contracts (OpenAPI/Protobuf/gRPC), schema evolution, and data contracts;
- SLO/SLA language in SRE, incident retrospectives, and operational gating;
- ML governance artefacts: evaluation protocols, model cards, dataset sheets, reproducibility checklists;
- regulatory and safety assurance: “what is guaranteed”, “what is admissible”, “what evidence counts”.

FPF treats such boundary sentences as first‑class architectural objects. The **A.6 cluster** (*Signature Stack & Boundary Discipline*) is the place in the spec that deals with the edge‑cases of meaning: the situations where “normal prose” is too lossy, but a full formal spec is not yet available (or not yet worth the cost).

The key idea is simple: do not let one sentence do four jobs. When the same line simultaneously tries to define meaning, declare a runtime gate, assign a duty, and claim evidence, it becomes uncheckable. A.6 gives a lightweight routing discipline—captured as the **Boundary Norm Square** (A.6.B)—that keeps these roles separate:

- **L — laws & definitions** (truth‑conditional content you can inspect or reason over),
- **A — admissibility & gates** (what a mechanism admits at application time),
- **D — deontics & commitments** (who owes what, to whom, and under which scope),
- **E — work‑effects & evidence** (what must be observable on carriers so adjudication is possible).

Once boundary talk is routable, it becomes evolvable: different views can publish the *same* underlying boundary without creating parallel contracts, and changes can be narrated without silently rewriting meaning.

