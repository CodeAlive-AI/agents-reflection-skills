## B.1.6 - Γ\_work — Work as Spent Resource

> **► decided‑by: A.14 Advanced Mereology**
**A.14 compliance —** Only **Work** carries resource deltas; quantitative splits/consumption use **PortionOf** against pre‑consumption stocks; run histories use **PhaseOf** on Work; `MemberOf` MUST NOT be used for resource mereology; SCR/RSCR stay outside (use EPV‑DAG anchors).
 
### B.1.6:1 - Problem frame

FPF distinguishes **what is done** from **what it costs** to do it.

* **Method / MethodDescription / Process (design‑time):**
  A **Method** is the abstract **way‑of‑doing** inside a bounded context (A.15). A **MethodDescription** is a design‑time `U.Episteme` that describes a Method (SOP, algorithm, proof, simulator configuration, etc.).
  A **Process** is a *view* that represents a MethodDescription as an ordered/partially‑ordered composition (steps, branches, synchronization). In Cluster B, that ordering/coordination is handled by **Γ\_method** (B.1.5). **Not every MethodDescription admits a step decomposition**; Γ\_method applies only when a step/process view is chosen.

* **Work (run‑time; this pattern focuses on the resource facet):**
  **Work** is the dated run‑time **occurrence** of enacting a MethodDescription by a performer under a `U.RoleAssignment` (A.15). In this pattern we treat Work under its **spent‑resource facet**: the typed delta we can account for across a declared boundary and time window. Γ\_work defines how those deltas compose across parts and phases.

This separation makes models auditable and prevents category errors: **Γ\_method** composes *design‑time coordination* (a process view); **Γ\_work** composes *run‑time Work ledgers* (and never smuggles order semantics).
### B.1.6:2 - Problem

Without a dedicated algebra for spent resources, models drift into four errors:

1. **Process–Work conflation:** Time‑ordered steps and resource spending are mixed, producing ambiguous or double‑counted totals.
2. **Conservation violations:** Totals appear that exceed inputs or create “free” resource, contradicting physical and informational conservation.
3. **Boundary blindness:** Spending is reported without specifying the boundary across which it is measured, making numbers non‑comparable.
4. **Category errors in mereology:** Collection membership (MemberOf) is misused as if it were parthood for resource stocks, polluting Γ proofs (B.1).


### B.1.6:3 - Forces

| Force                                               | Tension                                                                                                                        |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Conservation vs. Abstraction**                    | Totals must obey material/energy/information conservation ↔ models must stay simple and readable.                              |
| **Run‑time measurability vs. Design‑time planning** | We need measurable deltas at run‑time ↔ we also need ex‑ante yields from MethodDescription to plan.                                   |
| **Heterogeneous units vs. Unified sums**            | Resources come in different units (joules, kg, bits) ↔ we still need composite statements (vectors, typed sums).               |
| **Safety vs. Synergy**                              | Weakest‑link bounds must cap availability ↔ redundancy or substitution can improve feasibility but belongs to emergence (B.2). |


### B.1.6:4 - Terminology guard‑rails (A.15 — Strict Distinction)

> These rules are normative in this pattern; they exist to prevent the recurring confusion noted in prior drafts.

* **Method (U.Method)** — design‑time, abstract **way‑of‑doing** inside a bounded context; **not** an execution; it may be described by multiple MethodDescriptions and may or may not admit any step decomposition.
* **MethodDescription (U.MethodDescription)** — a design‑time `U.Episteme` that describes a Method (SOP/algorithm/proof/simulator/solver configuration, control law, or other viewpoint). A step/workflow graph is only one possible representation.
* **Process (view)** — a chosen representation of a MethodDescription as an ordered/partially‑ordered structure (steps, branches, synchronization); composed by **Γ\_method**.
* **Work (U.Work)** — a run‑time **occurrence**: dated enactment of a MethodDescription by a performer under a `U.RoleAssignment`. In this pattern, **Work** is treated under its *spent‑resource ledger* facet; composed by **Γ\_work**.
* **Transformer (T)** — a `U.System` playing the executing and/or auditing role for Work’s accounting (A.12); transformer identity belongs in the **Boundary Ledger**.
* **Mereology for resources (A.14):** use `PortionOf` for **quantitative splits** and `PhaseOf` for **time‑slices**; **do not** use `MemberOf` for resource stocks.
### B.1.6:5 - Solution — The Γ\_work Operator

**Intent.** Provide a universal, conservative way to compose resource spending across parts and steps, without talking about control‑flow (that is Γ\_method’s job).

#### B.1.6:5.1 - Operator signature

```
Γ_work : (S : Set[U.Work], M_spec : U.MethodDescription?) → W_tot : U.Work
```

* **S — Work set.** A finite set of `U.Work` instances to be rolled up (parts, phases, episodes, or boundary partitions). Each Work MUST carry (or reference) a **Boundary Ledger** (§5.3) and a typed resource ledger on an explicit basis. Where a stock is subdivided, the split uses `PortionOf`; where a run is time‑sliced, the slices use `PhaseOf` (A.14).

  If `S` contains overlaps (shared stocks, shared ports, or overlapping time windows), the fold MUST apply an explicit **overlap / de‑duplication policy** declared in the relevant `U.BoundedContext` (A.15.1:5.3); otherwise the result is undefined (double counting).

* **M_spec — optional.** If present, it provides *ex‑ante* yield/efficiency (η) and declared equivalence maps for **planning** or **basis normalization**. It MUST NOT overwrite measured deltas; planned and measured Work MUST be reported separately (CC‑B1.6.8).

* **Result W_tot — U.Work.** A composite Work whose **resource ledger** is the Γ_work fold of the input ledgers (plus any declared overheads/residuals). It is accompanied by a **Boundary Ledger** (see §5.3) and references its parts for auditability.

> **Do not confuse:** Γ\_work neither schedules nor orders steps; it composes **resource deltas attached to Work**. If you need order, use Γ\_method at design‑time and Work’s run‑time relations (`precedes`, `PhaseOf`, `overlaps`) with Γ\_time for temporal coverage.
#### B.1.6:5.2 - What counts as “Work”

Work is defined **with respect to a declared boundary** of the holon being transformed or assembled:

* **Boundary‑relative delta (conservative form):**
  For any resource type *q* measured on boundary *B* during a run,

  ```
  Work_B(q) = Inflow_B(q) − Outflow_B(q) − ΔStock_inside(q)
  ```

  where **ΔStock\_inside(q)** is the change of internal stock over the run (positive when the stock grows).

* **Embodiment split:**
  Work can be split into **Dissipation** (lost to environment) and **Embodied** (retained in produced holons as state). Both are part of the same Work vector; the split is a reporting choice, not a second algebra.

* **Heterogeneous vectors:**
  Γ\_work treats different resource types as a **typed vector space** (no implicit conversion). Equivalences (e.g., joules↔bits via a declared model) are allowed only if **declared in M\_spec** or in a domain CAL; otherwise vectors remain multi‑dimensional.

#### B.1.6:5.3 - Boundary Ledger (normative output metadata)

Every Γ\_work result **MUST** include a **Boundary Ledger**:

* **(i) Boundary scope:** which `U.Boundary` was used (source holon, ports).
* **(ii) Time window:** start/stop or `PhaseOf` slice identifiers.
* **(iii) Basis:** the ordered list of resource types and units.
* **(iv) Method context & lineage:** reference(s) to the governing `U.MethodDescription`(s) (and, if known, `U.Method`), plus the Work lineage (which Work IDs were folded to produce `W_tot`).
* **(v) Accounting authority:** identity of the system(s) that executed, metered, and/or audited the reported ledgers (often the performer/transformer per Work part, plus the aggregator for a roll‑up).

This ledger is what makes cross‑model Work totals comparable and auditable (A.10).
#### B.1.6:5.4 - The invariant quintet instantiated (overview)

Γ\_work preserves B.1 invariants; the detailed proofs and corner cases are in Part 2.

* **IDEM (idempotence):** Folding a singleton zero‑delta Work (or adding a zero‑delta Work to any fold) does not change totals; the zero‑delta ledger is the identity element.
* **COMM / LOC (local commutativity / locality):** For **independent** boundary/stock partitions, composed Work is additive and independent of local fold order.
* **WLNK (weakest‑link bound):** Effective Work is capped by the scarcest **critical** input on the boundary (no Work can exceed available supply).
* **MONO (monotonicity):** Increasing an available resource cannot decrease Work (for the same boundary and time window); decreasing dissipation or improving η cannot reduce feasibility.
#### B.1.6:5.5 - How Γ\_work relates to Methods (and to Γ\_method)

* **Design‑time:** `M_spec` (a `U.MethodDescription`) may declare an intended yield **η** and admissible equivalences between resource types (e.g., heat→mechanical). These are **assumptions** until validated by run‑time Work.
* **Run‑time:** A `U.Work` instance (enacting a MethodDescription under a `U.RoleAssignment`) produces measured deltas across its declared boundary/time window. Γ\_work composes those deltas; it does not speculate nor retroactively “fix” measurements.
* **Sequencing:** If multiple MethodDescriptions are ordered/branched (process view), use **Γ\_method** to define that coordination at design‑time. At run‑time, model the corresponding segments as Work parts and fold them with Γ\_work (Work adds in serial and parallel), while time coverage is handled by Γ\_time.

> **Didactic tip:** Think of **Γ\_method** as the **coordination story**, and **Γ\_work** as the **receipt of what it cost**, both anchored to the same boundary and time window.
### B.1.6:6 - Fold rules (how Γ\_work composes)

#### B.1.6:6.1 - Boundary partition (across parts of a whole)
Let the system‑level boundary **B** be covered by a finite family of pairwise‑disjoint sub‑boundaries **{Bᵢ}** (ports, surfaces, interfaces) that together exhaust **B**. For any resource type *q* in the basis:

* **Partition additivity (normative):**

  ```
  Work_B(q) = Σ_i Work_Bi(q)
  ```

  Preconditions: (i) `Bi` are disjoint except for measure‑zero interfaces, (ii) meters are aligned (same units, same time window), (iii) internal stock changes ΔStock\_inside(q) are measured for the *same* closed region bounded by B.
  *Why it matters:* this is the cross‑scale rule that lets part‑level Work totals roll up to the whole without double counting.

#### B.1.6:6.2 - Time slicing (serial runs / phases)
Let the run be split by a set of non‑overlapping intervals **{τⱼ}** that cover the window **τ** (use `PhaseOf` to tag the slices). Then:

```
Work_B(q, τ) = Σ_j Work_B(q, τ_j)
```

This is the **temporal additivity** of Work. It is the Γ\_work analogue of Γ\_time’s coverage rule: we never “smear” or reorder; we sum non‑overlapping slices.

#### B.1.6:6.3 - Concurrent branches (parallel activity)
When two independent sub‑boundaries **B₁**, **B₂** are active over overlapping time, total Work still **adds**:

```
Work_B(q) = Work_B1(q) + Work_B2(q)
```

Independence here means: no shared port, no shared stock variable, no hidden transfer between B₁ and B₂ that bypasses the declared meters. If a shared internal stock exists, it must be accounted in ΔStock\_inside(q) for **B** to keep conservation exact.

> **Didactic contrast:** Γ\_method handles **duration** (Σ for serial, max for parallel). Γ\_work handles **resource** (Σ in both serial and parallel), because resource spending composes additively across disjoint boundary parts and disjoint time slices.

#### B.1.6:6.4 - Multi‑resource vectors and declared equivalences
Γ\_work never implicitly converts units. If a planning model needs an exchange (e.g., heat→mechanical, memory→compute), it must be **declared** in `M_spec` (or a domain CAL) as an **equivalence map** `E` applied **before** folding, yielding a new typed basis **E(basis)**. Absent such declaration, vectors remain multi‑dimensional and are added component‑wise.

#### B.1.6:6.5 - Availability gates (weakest‑link discipline)
Many runs require **critical** inputs (a subset **Q\*** of the basis) to be present at or above a threshold. Let `Avail_B(q*)` be the measurable availability for `q* ∈ Q*` on boundary B during τ. Then feasibility is constrained by:

```
Work_B(q*) ≤ Avail_B(q*),  for all q* ∈ Q*
```

If any inequality is violated, the fold **must fail** or the modeller must declare a **Meta‑Holon Transition (B.2)** that introduces redundancy/substitution as a new structural capability (changing Q\* or the equivalence map). This is WLNK in resource form.

### B.1.6:7 - Embodiment and dissipation (reporting scheme)

Every Work vector **MAY** be split into two projections, both defined on the **same basis** and the **same boundary/time window**:

* **Embodied\_B(q)** — the part of Work retained **inside** B as *state change* of produced holons (e.g., latent heat stored, material incorporated, committed data).
* **Dissipated\_B(q)** — the part of Work irreversibly exported beyond B (e.g., heat loss, scrap, discarded packets).

By norm:

```
Work_B(q) = Embodied_B(q) + Dissipated_B(q)
```

This split is **informative**, not a second algebra: Γ\_work always folds the **total** Work; the split is attached in the **Boundary Ledger** for transparency.


### B.1.6:8 - Invariants — edge cases and proof sketches

#### B.1.6:8.1 - IDEM (idempotence)
Let `S = {W}` be a singleton Work set. If the resource ledger carried by `W` satisfies `Work_B(q)=0` for all basis components *q* (i.e., no net delta across the declared boundary over the window), then

```
Γ_work(S) = 0  (the zero vector)
```

Trivial by definition: no measured boundary‑relative delta implies zero spent‑resource Work.

#### B.1.6:8.2 - COMM/LOC (local commutativity / locality)
Let `S` be partitioned into independent subsets `{Sᵢ}` whose boundary partitions `{Bᵢ}` are disjoint and cover **B** (6.1). Since each subset’s ledger is evaluated with its own meters and time slices (6.2), and vector addition is commutative/associative, any local fold order yields the same `Σ_i Γ_work(Sᵢ)`. Hence Γ\_work inherits commutativity/locality **under independence**.
*Note:* If subsets share a stock variable (or an undeclared transfer), independence fails and the modeller must either (i) refactor boundaries / Work decomposition to restore independence, or (ii) model the shared stock explicitly in ΔStock\_inside(q) for the **parent** B.

#### B.1.6:8.3 - WLNK (weakest‑link)
Let **Q\*** be the critical input set with availability caps `Avail_B(q*)`. Since the delta definition measures **net** consumption across B (inflow–outflow–Δstock), and no external creation is allowed, each `Work_B(q*)` cannot exceed `Avail_B(q*)`. If the plan suggests more, you have either (a) a measurement error, (b) a missing equivalence declaration in `M_spec`, or (c) a true emergent synergy that must be modelled as **MHT** (new redundancy/substitution capability).

#### B.1.6:8.4 - MONO (monotonicity)
Monotonicity is interpreted along three characteristics; in all cases “improvement” never makes the whole **worse** (i.e., never increases required Work nor decreases feasibility):

* **Availability monotonicity:** Increasing `Avail_B(q)` for any non‑critical q leaves `Work_B(q)` unchanged (availability is not auto‑consumed); increasing it for a critical q cannot increase `Work_B(q)` and weakly increases feasibility.
* **Yield monotonicity (η):** For a fixed output target, increasing declared or measured **η** weakly **decreases** the required `Work_B(q)` in the inputs, never increases it.
* **Loss monotonicity:** Decreasing dissipation (better insulation, better compression) weakly **decreases** `Dissipated_B(q)`; total Work cannot go up as a result.

#### B.1.6:8.5 - Compatibility with Γ\_method
Let a process be composed by Γ\_method from steps `{S_k}`, each with its own boundary partition `{B_k}` and time slice `{τ_k}`. If independence holds between steps at the resource boundary level (no hidden cross‑leaks), the summed Work

```
Σ_k Work_Bk(q, τ_k)
```

is invariant to any topological sort consistent with Γ\_method’s order (Γ\_method may change *when* costs are incurred; Γ\_work adds *how much* is spent).

**Manager note.** When reviewing a plan, inspect **Γ\_method** (is the order/capability sound?). When reviewing results, inspect **Γ\_work** (do the boundary‑relative deltas and units make sense?). Use **PhaseOf** to align both views over time.

### B.1.6:9 - Archetypal grounding (System / Episteme)

| Facet                       | **U.System — Assembling a heat‑treated frame**                                                                      | **U.Episteme — Training and publishing a model**                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Boundary**                | The enclosure boundary of the frame workstation; ports for electricity, gas, material in/out.                       | The boundary of the knowledge artefact: data ingress, model artefact egress, compute energy ingress.                                 |
| **Work definition**         | Electricity and fuel inflows minus outflows minus Δstock of materials and thermal content retained in the frame.    | Energy spent (compute) + data‑read deltas; Embodied work includes the stored parameters (as committed bytes) and archived SCRs. |
| **Embodied vs Dissipated**  | Embodied: material incorporated, latent heat retained; Dissipated: heat loss, scrap.                                | Embodied: parameter file written, proof artefacts; Dissipated: energy to heat, discarded intermediate data.                          |
| **Additivity across parts** | Ports on furnace, press, conveyor are `Bᵢ`; total frame‑level Work is Σ over `Bᵢ`.                                  | Data‑read over dataset shards are `Bᵢ`; total training Work adds per‑shard deltas.                                                   |
| **Time slicing**            | Heat → dwell → quench phases are `PhaseOf`; Work adds: Σ over phases.                                               | Epochs are `PhaseOf`; Work adds across epochs.                                                                                       |
| **WLNK**                    | Gas supply cap limits feasible heat cycles (critical input); if redundancy is added (dual supply), model it as MHT. | Storage bandwidth caps data‑read; adding a cache hierarchy is MHT (new structural capability), not “free” efficiency.                |


### B.1.6:10 - Conformance Checklist (complete)

| ID            | Requirement                                                                                                                                     | Purpose                                               |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **CC‑B1.6.1** | Every Γ\_work result SHALL include a **Boundary Ledger**: boundary, time window, basis, method context, transformer identity.                   | Make Work statements comparable and auditable (A.10). |
| **CC‑B1.6.2** | Resource vectors SHALL be **typed**; no implicit unit conversions. Any equivalence MUST be declared in `M_spec` (or a domain-specific mechanisms).      | Prevent silent inflation/deflation.                   |
| **CC‑B1.6.3** | Resource stocks SHALL be structured with `PortionOf` and `PhaseOf`; `MemberOf` MUST NOT be used for resource mereology.                         | Align with A.14 and prevent category errors.          |
| **CC‑B1.6.4** | For partitioned boundaries `{Bᵢ}` the fold MUST satisfy partition additivity and document the partition.                                        | Enable cross‑scale roll‑ups.                          |
| **CC‑B1.6.5** | For time slicing `{τⱼ}` the fold MUST satisfy temporal additivity with non‑overlapping slices (Γ\_time‑compatible).                             | Keep history coherent.                                |
| **CC‑B1.6.6** | Critical inputs **Q\*** and their availability caps MUST be explicit; any violation SHALL cause the fold to fail or require an MHT declaration. | Enforce WLNK conservatism.                            |
| **CC‑B1.6.7** | If a shared internal stock exists between sub‑boundaries, it MUST be modelled in ΔStock\_inside(q) at the **parent** boundary level.            | Preserve conservation and COMM/LOC preconditions.     |
| **CC‑B1.6.8** | When `M_spec` declares a yield η, the report SHALL separate **planned** (ex‑ante) and **measured** (ex‑post) Work.                              | Keep planning distinct from accounting (A.15).        |
| **CC‑B1.6.9** | Γ\_work SHALL provide proofs of the invariant quintet under the independence assumptions used, or explicitly state where MHT is required.       | Maintain B.1 guarantees.                              |


### B.1.6:11 - Consequences

**Benefits**

* **Audit‑ready costing:** A single definition of Work makes multi‑scale totals consistent and comparable.
* **Separation of concerns:** Control‑flow (Γ\_method) never contaminates cost accounting (Γ\_work).
* **Cross‑scale reliability:** Partition/time additivity gives predictable roll‑ups from parts and phases.
* **Safety by design:** WLNK gates reveal feasibility limits early; emergence is explicit via MHT.

**Trade‑offs / mitigations**

* **Boundary modelling effort:** Requires explicit ports and stock deltas. *Mitigation:* use A.14 templates for common boundary patterns.
* **Vector heterogeneity:** Mixed units can be hard to read. *Mitigation:* keep vectors typed; add equivalence maps only when justified in `M_spec`.
* **Independence discipline:** Shared stocks complicate additivity. *Mitigation:* elevate stock accounting to the parent boundary per CC‑B1.6.7.


### B.1.6:12 - Rationale (informative)

Γ\_work is a conservative algebra of **spent resources**. It respects physical conservation (mass/energy), supports information‑centric resources without conflation, and keeps the **design‑time** (MethodDescription) separate from **run‑time** (Work) facts (A.15). Additivity over disjoint boundaries and non‑overlapping phases is the minimal set of rules that yields stable cross‑scale accounting while remaining faithful to the universal invariants of B.1. Emergent efficiency (redundancy, substitution) is not “free”: it is made structural via **Meta‑Holon Transition** (B.2), after which the same algebra applies at the new level.


### B.1.6:13 - Relations

* **Builds on:** A.12 **Transformer Principle**; A.14 **Mereology Extension** (PortionOf, PhaseOf); A.15 **Strict Distinction** (MethodDescription / Method / Work).
* **Coordinates with:** B.1.5 **Γ\_method** (order and concurrency), B.1.4 **Γ\_time** (temporal coverage), B.1.2 **Γ\_sys** (system assembly).
* **Triggers:** B.2 **Meta‑Holon Transition (MHT): Recognizing Emergence and Re‑identifying Wholes** when feasibility constraints (WLNK) are beaten by structural redundancy/substitution.
* **Feeds:** B.3 **Trust & Assurance Calculus (F–G–R with Congruence)** (cost‑aware confidence overlays) — informative only, without altering Γ\_work’s conservation semantics.

> **Summary for practitioners.**
> Use **Γ\_method** to say **what happens and in which order**.
> Use **Γ\_work** to say **what it costs across a boundary**.
> Keep boundaries, time windows, units, yields, and transformers explicit.
> When apparent “free gains” appear, declare the structural change (MHT) and apply the same algebra one level up.

### B.1.6:End

