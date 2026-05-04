## B.1.2 - System‑specific Aggregation Γ\_sys

**► decided‑by: A.14 Advanced Mereology**
**A.14 compliance —** Treat **PortionOf** as Σ‑additive stocks; **ComponentOf** must respect boundary integration (BIC); **PhaseOf** is *not* aggregated here (handled by Γ\_time); mapping/representations are *not* parthood.

#### B.1.2:1 - Purpose

`Γ\_sys` is the **default flavour of the universal aggregation operator** for everything that engineers can touch, weigh or wire‑up: bridges, battery packs, data‑centre racks, container clusters.
It translates the abstract Invariant Quintet into three **physically meaningful fold rules**—*additive, limiting, boolean*—and a **Boundary‑Inheritance Standard** (BIC) that keeps external interfaces tidy. Together they guarantee that holons built with `Γ\_sys` obey conservation laws, expose a clean API surface and pass safety audits without manual patching.


#### B.1.2:2 - Context

Kernel § 6 defines `U.System` and states that only a **Calculus** may own an aggregation operator. *Sys‑CAL* (Part C.1) exports `Γ\_sys` as its single builder; other CALs (KD‑CAL, Method‑CAL …) reuse the same quintet but swap in domain rules.
Draft 20 Jul 25 already lists default fold policies (Σ, min, ∨/∧) and a cut‑stable axiom; this pattern turns those snippets into a teachable Standard for day‑to‑day system design.


#### B.1.2:3 - Problem (seen on real projects)

| Field failure                                                           | Algebraic root cause                                                 |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **“Phantom megawatts”** — energy sums higher than fuel input            | Temperatures averaged, masses summed; operator ignored conservation. |
| **Interface Medusa** — hundreds of dangling ports after integration     | No rule for boundary promotion vs encapsulation.                     |
| **Safety inversion** — upgraded actuator lowered SIL rating of the skid | Intensive property (safety) aggregated by average, not min.          |
| **Audit hairball** — inspector cannot trace which crane load went where | Boundary cuts not stable; provenance leaks.                          |

All four break Pillars *Cross‑Scale Consistency* and *State Explicitness*.


#### B.1.2:4 - Forces

| Force                     | Pull                          | Push                                                         |
| ------------------------- | ----------------------------- | ------------------------------------------------------------ |
| **Physical plausibility** | Sum masses, conserve energy   | **Abstraction** — keep rules domain‑agnostic                 |
| **Interface clarity**     | Present one clean API         | **Fidelity** — expose every critical port                    |
| **Safety conservatism**   | Take worst‑case rating        | **Performance** — allow redundancy gains (via MHT later)     |
| **Parallel build**        | Shard assembly, cache results | **Boundary realism** — stress must still balance across cuts |


#### B.1.2:5 - Solution (conceptual core)

##### B.1.2:5.1 - Operator signature

```
Γ\_sys : (D : DependencyGraph\[U.System\], T : U.TransformerRole (plays `AssemblerRole`)) → E\_eff : U.System
```

* **D** – finite acyclic graph whose nodes share one temporal scope and obey the four DG rules (Pattern B .1.1).
* **T** – physically real external system playing `TransformerRole` (e.g., crane, welding rig).

##### B.1.2:5.2 - Three attribute classes

| Class                    | Fold rule                                  | Typical examples                        | Invariants touched       |
| ------------------------ | ------------------------------------------ | --------------------------------------- | ------------------------ |
| **Extensive**            | **Σ** (sum)                                | Mass, energy, cost                      | IDEM - COMM - LOC - MONO |
| **Intensive / Risk**     | **min** (weakest‑link)                     | Temperature limit, SIL, encryption bits | WLNK - MONO              |
| **Boolean / Capability** | **∨ / ∧** (OR for vuln, AND for must‑hold) | CVE exposure, “Has EmergencyStop”       | WLNK                     |

*Rule of thumb for managers:* *If it adds up in your spreadsheet → Σ; if it caps the system → min; if it is yes/no → logic gate*. Defaults match kernel table “Additive flow / Capacity / Boolean capability” .

##### B.1.2:5.3 - Boundary‑Inheritance Standard (BIC)

For **every external interaction** of every part, `Γ\_sys` forces a deliberate choice:

1. **Promote** — port becomes part of the new system boundary.
2. **Forward** — port remains on the child but is namespaced by the parent.
3. **Encapsulate** — port becomes internal and disappears from public view.

BIC is the antidote to *Interface Medusa*: it prevents silent loss of obligations or explosion of unmanaged endpoints.

##### B.1.2:5.4 - Cut‑Stable Boundary Axiom (reminder)

> Given any declared boundary 𝔅, `Γ\_sys(D,C)` **MUST** leave every across‑𝔅 interaction either identical or transformed by a rule that still satisfies the Quintet.

#### B.1.2:6 - Step‑by‑Step Aggregation Recipe

> **Audience:** lead engineer planning a multi‑team build; QA manager preparing an audit; analyst running a quick what‑if.
> **Goal:** fold a ready Dependency Graph into one coherent system in **five repeatable moves**.

| Step                             | What you do                                                                                                                  | Why it matters                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **1 - Verify the graph**         | Run Pattern B .1.1 checklist (acyclic, typed edges, same scope, boundary tags).                                              | Avoid paradoxes before they snowball.                                             |
| **2 - Label attributes**         | For every property in every node, mark it **Extensive**, **Intensive**, or **Boolean**. Defaults are in Sys‑CAL cheat‑sheet. | The fold rule depends on this label.                                              |
| **3 - Decide the BIC**           | For each external port, pick **Promote / Forward / Encapsulate**. Record choice in the interface table.                      | Keeps APIs intentional and auditable.                                             |
| **4 - Execute Γ\_sys** | *Extensive* → parallel Σ; *Intensive* → propagate min; *Boolean* → ∧/∨ logic.                                                | Implements the Invariant Quintet.                                                 |
| **5 - Run Cut‑Stable test**      | For each declared boundary 𝔅, compare across‑𝔅 interactions before & after fold.                                           | Confirms that sharding or outsourced work didn’t shift loads or responsibilities. |

If the min rule is exceeded by design (e.g., triple redundancy boosts SIL beyond any part), stop here and initiate **Meta‑Holon Transition** (Pattern B .2) to formalise emergence.


#### B.1.2:7 - Worked Example — Battery‑Electric Bus Pack (2025 model year)

| Step                | Snapshot                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Graph**           | 16 modules → 4 strings → pack. Edges `ComponentOf`. All nodes `scope=design`.                                                  |
| **Attribute label** | *Extensive*: energy (kWh), cost; *Intensive*: cell voltage limit, fire rating (SIL 2); *Boolean*: “Has self‑heating”.          |
| **BIC decisions**   | Main DC output ‑ Promote; per‑string fuse access ‑ Forward; cell balancing ports ‑ Encapsulate.                                |
| **Fold**            | Σ energy = 628 kWh; min voltage limit = 4.25 V; ∧ self‑heating = true.                                                         |
| **Cut‑Stable**      | Across‑string current same pre/post fold. Pass.                                                                                |
| **Outcome**         | Pack spec delivered to vehicle OEM; audit shows WLNK bound 4.25 V, MONO intact; financial model reads energy Σ for range calc. |


#### B.1.2:8 - Conformance Checklist (author‑facing)

| ID           | Question                                          | Pass if…                           |
| ------------ | ------------------------------------------------- | ---------------------------------- |
| **CHK‑GC‑1** | All properties classified?                        | No “unknown” label remains.        |
| **CHK‑GC‑2** | Any property violate its fold rule?               | None; else declare MHT.            |
| **CHK‑GC‑3** | BIC table complete?                               | Every external port accounted for. |
| **CHK‑GC‑4** | Cut‑Stable test green on all declared boundaries? | Yes.                               |
| **CHK‑GC‑5** | Provenance hash stamped?                          | `E_eff.meta.provenance` populated. |

Failing a line means the operator must **refactor the graph or escalate to Meta‑Holon** before reuse.


#### B.1.2:9 - Consequences

| Benefit for project leadership                                                                 | Secondary effect                                      |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Plausible mass‑energy books** — no “phantom capacity” during tender negotiations.            | Vendor bids align faster; fewer change orders.        |
| **Single‑page interface sheet** — the BIC doubles as hand‑over Standard to next tier supplier. | Interface churn caught early; legal exposure shrinks. |
| **Safety‑first roll‑up** — weakest‑link bound surfaces brittle parts immediately.              | QA budget aimed at right module; no gold‑plating.     |
| **Seamless parallel builds** — COMM + LOC proven once, reused by every subStandardor.          | Integration rehearsals shortened by weeks.            |


#### B.1.2:10 - Rationale (link to modern practice)

* **Model‑Based Systems Engineering (MBSE 2023‑2025):** Tools like Cameo Systems Modeler automated Σ/min logic via “Property Kind” stereotypes—Γ\_sys formalises the same trick.
* **Safety audits:** ISO 26262‑2 Ed 3 explicitly adopts “minimum of ASIL ratings” rule; our min fold embeds it by design.
* **Interface control:** Aerospace ICDs (NASA‑7120.5E updates 2024) require a promotion/forward/encapsulate decision tree identical to BIC.
* **Cloud operations:** Kubernetes 1.30 resource quotas implement additive CPU/memory and min PodDisruptionBudget—industrial proof that the schema scales.

Real‑world convergence across steel, silicon and software shows the rules are not theory nice‑to‑haves; they are what successful projects already do—Γ\_sys just makes it explicit, automatic and auditable.


#### B.1.2:11 - Relations

* **Builds on:** Dependency Graph (B .1.1); Transformer Principle (A.3).
* **Enables:** Meta‑Holon Transition (B .2); Calculus of Trust (B .3).
* **Refined by:** Γ<sub>epist</sub> (B .1.3) for knowledge artefacts; Γ<sub>time</sub> / Γ<sub>ctx</sub> (B .1.4) for temporal or context‑sensitive domains.
* **Exemplifies:** Pillars P‑8 Cross‑Scale Consistency, P‑9 State Explicitness.

> **Take‑away for engineering managers:** *“Classify, Standard, fold—then sleep easy knowing the numbers and the interfaces will still match tomorrow.”*

### B.1.2:End

