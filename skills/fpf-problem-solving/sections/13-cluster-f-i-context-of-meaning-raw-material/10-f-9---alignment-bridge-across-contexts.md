## F.9 - Alignment & Bridge across Contexts

**“Translate across Contexts; never collapse them.”**
**Type.** Architectural pattern.
**Status.** Stable.
**Normativity.** Normative.
**Builds on:** E.10.D1 (Context discipline: Context = U.BoundedContext); **F.0.1 (senseFamily & StatusModality guard; Bridge-only crossing)**; F.1 (Contexts fixed); F.2/F.3 (Cells exist); F.7 (rows depend on Bridges); F.8 (thresholds and reuse choice).

**Coordinates with:** B.3 **Trust & Assurance Calculus** (uses CL penalties); **A.6.1 U.Mechanism** (Transport clause for cross-context use; penalties route to **R/R_eff** only; **F/G** invariant); Part C patterns (apply Bridges in formal claims); A.6.9 (RPR-XCTX for repairing umbrella “same/equivalent/align/map” prose into explicit Bridge Cards).
**Aliases (informative).** *Context-to-Context translator*; *Sense bridge*.

### F.9:1 - Intent & applicability

**Intent.** Provide a **conceptual discipline** for relating **SenseCells** from **different Contexts (U.BoundedContext)**. A **Bridge** states *what kind* of relationship holds, *how far* it holds (via **CL: Congruence Level**), and *what is lost* during the translation. Bridges **permit carefully scoped reuse** (e.g., a Concept-Set row) while **forbidding silent equivalence**.

**Applicability.** Use **whenever** an author needs to **read across Contexts**—to reuse a familiar label, to connect design-time and run-time notions, to compare two standards’ terms, or to justify a row in the Concept-Set table. This pattern is **not** storage, enactment protocol, or governance; it codifies **thinking moves**.

**Non-goals.** No global meaning; no publication-surface semantics; no editor roles. Bridges are **semantic relations between local senses**, not transport chains, not processes.

### F.9:2 - Problem frame

Cross-context work fails in predictable ways:

1. **String-equals fallacy.** Identical surfaces (“process”, “role”, “accuracy”) taken as identical meaning.
2. **Scope creep.** A naming convenience is stretched to assignment or structural claims.
3. **DesignRunTag jumping.** Design artefacts are substituted for run-time occurrences (or vice-versa).
4. **Direction amnesia.** Narrower/broader relations treated as symmetric.
5. **Loss blindness.** Differences (units, granularity, preconditions) are left unstated, contaminating downstream reasoning.

Bridges cure these by **making relation, direction, loss, and strength explicit**.


### F.9:3 - Forces

| Force                           | Tension to resolve                                                                       |
| ------------------------------- | ---------------------------------------------------------------------------------------- |
| **Locality vs reuse**           | Senses are context-local, yet people need a common label to talk across Contexts.              |
| **Simplicity vs fidelity**      | Few Bridge kinds are teachable; too few will hide real mismatches.                       |
| **Safety vs utility**           | Allow some substitution when safe; forbid it when loss is unbounded.                     |
| **senseFamily purity vs explanation** | Substitution must preserve **senseFamily**; explanation may span **senseFamilies** without implying sameness. |


### F.9:4 - Core idea (didactic)

**A Bridge is a declared translator between two local senses.**
It always names **(a)** the two **SenseCells**, **(b)** a **Bridge kind** (what relation), **(c)** a **direction** (if non-symmetric), **(d)** a **CL** (how strong), and **(e)** **Loss Notes** (what fails to carry). Some Bridges **permit substitution** in limited scopes; others **permit only explanation**.


### F.9:5 - Minimal vocabulary (this pattern only)

* **Context** — shorthand for **U.BoundedContext** (per E.10.D1).
* **SenseCell** - the pair *(Context, Local-Sense)* from F.3.
* **Bridge** — a conceptual relation between two SenseCells with kind, direction, CL, and loss notes.
* **CL (Congruence Level)** — ordinal strength (0…3) of a Bridge (see §7).
* **Scope** — the **licensed use** of a Cross-context reading (as in F.7/F.8):

* **Naming-only** (talk consistently),
* **Role Assignment & Enactment-eligibility** (assignable constraints/roles/status reuse),
* **Type-structure** (safe structural inference).
* **senseFamily** — the semantic category (Role, Status, Measurement, Type-structure, Method, Execution…) per F.0.1 (normative Part F guard).


### F.9:6 - Bridge kinds (senseFamily-aware)

> **Two families** of Bridges: **Substitution Bridges** (senseFamily-preserving; can support Concept-Set rows) and **Interpretation Bridges** (explanatory; **not** for substitution).

#### F.9:6.1 - Substitution Bridges (sense-preserving)

These relate **SenseCells of the same senseFamily** and may license **limited substitution**:

1. **Equivalence** - *near-identity of sense*. Symmetric. Rare.
   *Use:* May support **Type-structure** rows when CL=3 and invariants match.
   *Loss Notes:* usually “none” or “profiling differences”.

2. **Narrower-than / Broader-than** - *proper inclusion of sense*. Directional.
  *Use:* Safe to substitute **narrower > broader** in **Naming-only** and sometimes **Role Assignment & Enactment**; **broader > narrower** is unsafe.
   *Loss Notes:* “loses special cases X”.

3. **Partial-overlap** - *non-empty intersection, neither includes the other*.
  *Use:* **Naming-only** at best. **Never** justifies Role Assignment & Enactment / Type-structure.
   *Loss Notes:* “A-only senseFamily”, “B-only senseFamily”.

4. **Disjoint** - *explicit contrast*.
   *Use:* For **didactic warnings**; not a reuse license.
   *Loss Notes:* n/a (it asserts incompatibility).

#### F.9:6.2 - Interpretation Bridges (cross-senseFamily, explanatory)

These **do not allow substitution** but **explain connections** across senseFamilies:

5. **Design-spec -> Run-trace** - a design concept relates to its run-time occurrence.
   *Example:* *BPMN\:Process* -> *PROV\:Activity*.
   *Use:* Explain design-to-execution correspondence. No Concept-Set rows.
   *Loss Notes:* “graph vs event”, “control-flow vs temporal extent”.

6. **Measure-of / Evidence-for (->)** — a measurement SenseCell evidences or quantifies another **senseFamily** (e.g., a Requirement clause).
   *Example:* *SOSA\:Observation* -> *ITIL\:SLO fulfilment*.
   *Use:* Explain evaluation. No substitution.

7. **Policy-implies / Obliges (->)** — a deontic statement constrains another **senseFamily**.
   *Example:* *ODRL\:Duty* -> *Service behaviour*.
   *Use:* Explain constraint propagation.

> **Rule of thumb.** If you want **rows** or **substitution**, you need a **Substitution Bridge** on the **same senseFamily**. If you want to **explain** why artefacts relate without claiming sameness, use **Interpretation Bridges**.


### F.9:7 - CL scale and scope thresholds

CL expresses how safely meaning carries over.

| CL    | Name              | Intuition                                            | Typical loss             | Row scope allowed (thresholds) |
| ----- | ----------------- | ---------------------------------------------------- | -------------------- | -------------------------------- |
| **0** | **Opposed**       | Intentionally contrastive or disjoint                | n/a                  | none                             |
| **1** | **Comparable**    | Talk under a shared label; senses differ materially  | material sense divergence | **Naming-only** (`CL >= 1`) |
| **2** | **Translatable**  | Bounded loss; consistent examples & counter-examples | small, stated losses     | **Role Assignment & Enactment-eligibility** (`CL >= 2`) |
| **3** | **Near-identity** | Invariants match; no material counter-example        | profile-level only       | **Type-structure** (`CL = 3`) |

* **Thresholds (normative):**

  * Publishing a **Naming-only** row requires **CL >= 1** across the row-s Cells.
  * Publishing a **Role Assignment & Enactment-eligible** row requires **CL >= 2**, the **same senseFamily**, and compatible stance.
  * Publishing a **Type-structure** row requires **CL = 3** **and** matched invariants (acyclicity, anti-symmetry, units, etc.).

* **Penalty use (informative):** B.3 may convert **CL** into an assurance penalty when a cross-context claim is made.


### F.9:8 - The Bridge Card (compact sketch)

> A **thought-format** (not a form). Every bullet can be said in a sentence.

* **Cells.** `A@contextA` - `B@contextB`.
* **senseFamily.** *Role / Status / Measurement / Type-structure / Method / Execution …*
* **Kind.** *Equivalence / Narrower-than / Broader-than / Partial-overlap / Disjoint / Design-spec -> Run-trace / Measure-of / Policy-implies*.
* **Direction.** *A -> B* (if non-symmetric) or *A <-> B*.
* **CL.** *0–3* with a short **why**.
* **Loss Notes (bullets).** What fails to carry (units, scope, granularity, preconditions, time stance).
* **Counter-example.** The crispest case where substitution would mislead.
* **Allowed use.** *Naming-only / Role Assignment & Enactment-eligible / Type-structure / Explanation-only*.
* **Didactic hook.** The helpful sentence a careful engineer can remember.

t’t fit on a screen, you’re describing the Contexts, not the Bridge.*

**Registry-reference note (normative).** `BridgeId` and any policy/edition identifiers cited by a Bridge Card are **registry references** (keys into registries), not semantic symbols exported by signatures. Therefore they MUST NOT be demanded via `SignatureManifest.provides` (or -satisfied- via `imports` closure); conformance is checked by validating that the referenced registry entries exist and, where required, are edition-pinned (see F.15).


### F.9:9 - Invariants (normative)

1. **Locality first.** A Bridge relates **SenseCells**, never Contexts or strings.
2. **senseFamily discipline.** **Substitution Bridges must be senseFamily-preserving**. **Interpretation Bridges** may cross senseFamilies but **never** license substitution.
3. **Direction clarity.** If the kind is directional, state direction explicitly.
4. **CL honesty.** Assign **CL** only if you can state at least one **counter-example** for `CL <= 2` or explain its absence with invariants for `CL = 3`.
5. **Loss visibility.** Every Bridge carries **Loss Notes** (even “none”).
6. **Row dependence.** A Concept-Set row’s **scope** is **bounded by the weakest CL** among its participating Bridges (F.7/F.8).
7. **No senseFamily jump by stealth.** You **must not** use an Interpretation Bridge to justify a **row** or **substitution**.
8. **Time DesignRunTag honesty.** If a Context fixes **design/run**, the Bridge must respect that distinction or explicitly declare a bridge such as `Design-spec -> Run-trace`.
9. **Kernel restraint.** Bridges **cannot** be used to promote ad-hoc sameness into a new **U.Type**; A.11 applies.
10. **Non-inheritance of Contexts.** Bridges **do not** imply -is-a- between Contexts (E.10.D1).


### F.9:10 - Micro-examples (illustrative, one-liners)

1. **Participant vs Agent (process model vs provenance)**
   *Cells:* `BPMN:Participant` - `PROV:Agent` - *senseFamily:* Role - *Kind:* `Partial-overlap` - *CL:* 2 - *Loss:* participation vs attribution scopes differ - *Use:* **Naming-only** ("actor").

2. **Process (design) vs Activity (run)**
   *Cells:* `BPMN:Process` -> `PROV:Activity` - *senseFamily:* Method / Execution - *Kind:* **Design-spec -> Run-trace** - *CL:* 2 - *Loss:* graph vs event; concurrency vs temporalization - *Use:* **Explanation-only**.

3. **Observation vs SLO check**
   *Cells:* `SOSA:Observation` -> `ITIL:SLO-fulfilment` - *senseFamily:* Measurement / Status - *Kind:* `Measure-of` - *CL:* 2 - *Loss:* sampling window; target definition - *Use:* **Explanation-only**.

4. **Subtype across OWL and curated taxonomy**
   *Cells:* `OWL:SubClassOf` - `TaxonomyX:is-a` - *senseFamily:* Type-structure - *Kind:* `Equivalence` - *CL:* 3 *(only if TaxonomyX is acyclic and anti-symmetric)* - *Loss:* profile differences - *Use:* **Type-structure** rows allowed.

5. **Accuracy (metrology vs data-quality)**
   *Cells:* `ISO80000:accuracy` - `ISO25024:accuracy` - *senseFamily:* Measurement - *Kind:* `Partial-overlap` - *CL:* 2 - *Loss:* instrument vs dataset perspective - *Use:* **Naming-only** row -accuracy-; methods stay context-local.

### F.9:11 - Anti-patterns & remedies

| ID    | Anti-pattern | Symptom | Why it breaks thinking | Remedy (conceptual move) |
| --------- | -------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **AP-1** | **String-equals = sense-equals** | Same surface used across Contexts with silent identity claims. | Violates locality; invites false substitution. | Always state a **Bridge kind**; if unsure, default to **Partial-overlap** with **Naming-only** scope. |
| **AP-2**  | **Stealth substitution**         | “We’ll just treat A like B for now.”                                              | Hidden policy with unknown loss; leaks into Role Assignment & Enactment.    | Publish a **Bridge Card** with **Loss Notes** and **CL**; if CL<2, substitution remains **forbidden**.      |
| **AP-3** | **Stance jump by wording** | -Activity (PROV) is a Process (BPMN).- | Design/run confusion; swaps graphs for events. | Use a **Design-spec -> Run-trace** Interpretation Bridge, not a substitution bridge; keep **Explanation-only** scope. |
| **AP-4** | **Symmetry hallucination** | Treating directional bridges as if they were symmetric. | Narrows broadened, broadens narrowed; unsafe reuse. | Record **direction** explicitly; only **Equivalence** is symmetric. |
| **AP-5** | **Disjoint but reused** | Declare `Disjoint` and still borrow labels or Role Description constraints (RCS/RSG). | Contradiction between declaration and use. | Either retract `Disjoint` or stop reuse; if a thin thread exists, rename it as **contrastive explanation** (no row). |
| **AP-6** | **CL without counter-example** | -These are CL=3- with no invariant check. | Inflates trust; permits structural rows wrongly. | For **CL=3**, cite the **matching invariants**; otherwise, demote to **CL=2** and add a counter-example. |
| **AP-7** | **Bridge inflation** | Dozens of nearly identical Bridges between the same Contexts. | Noise masks the few material alignments. | Prefer **one Bridge per pair of Cells per senseFamily**; fold variants into **Loss Notes**. |
| **AP-8** | **Row outruns Bridge** | A Concept-Set row claims Role Assignment & Enactment-eligibility where some participating Bridges are `CL = 1`. | Row scope exceeds the weakest link. | Apply the **weakest-link rule** (F.7/F.8): row scope <= `min(CL)`; otherwise split the row. |
| **AP-9** | **Bridge as new U.Type** | Using a Bridge to justify minting a new universal Type. | Re-globalises meaning; breaks A.11 parsimony. | Keep Types context-local; where reuse is needed, use **rows** + Bridges, not new primitives. |
| **AP-10** | **Silent unit/scale mismatch** | Transporting measurements without unit/scale notes. | Hidden dimensional error. | Record units/scales in **Loss Notes**; if units cannot be related, use **Disjoint** or **Partial-overlap** with **Naming-only** scope. |


### F.9:12 - Worked examples (didactic)

#### F.9:12.1 - Service acceptance (design) vs executions & observations (run)

* **Cells & Contexts**
  `ITIL4:SLO` *(Status, design)* <- `SOSA:Observation(availability)` *(Measurement, run)*
  `BPMN:Process` *(Method, design)* -> `IEC61131:Task-Execution` *(Execution, run)*
* **Narrative**
  Availability SLOs are **evaluated** by observations of task executions. No substitution follows: an SLO is not an observation, and a process is not an execution occurrence.
* **Bridge Cards (sketch)**
  *ITIL\:SLO <- SOSA\:Observation* - **CL=2** - Loss: sampling window, clock skew.
  *BPMN\:Process -> IEC\:Execution* - **CL=2** - Loss: control-flow vs temporalization, concurrency collapse.
* **Permitted use**
  Explanation-only; Concept-Set rows may be **Naming-only** ("availability") with **CL >= 1** label coherence across Contexts.


#### F.9:12.2 - Behavioural role vs access role

* **Cells & Contexts**
  `BPMN:Participant` *(Role)* - `NIST-RBAC:Role` *(Status)*
* **Narrative**
  Both talk about -who acts-, but one is a **behavioural mask** in a process model, while the other is a **permission grouping**.
* **Bridge**
  **Kind:** `Partial-overlap`, **CL=2**; Loss: assignment moment, enforcement locus, multiplicity.
* **Permitted use**
* **Naming-only** row “actor”; **no Role Assignment & Enactment reuse** across senseFamilies.


#### F.9:12.3 - Equivalence of subtype notions for structural rows

* **Cells & Contexts**
  `OWL2:SubClassOf` *(Type-structure)* - `TaxX:is-a` *(Type-structure curated)*
* **Bridge**
  **Kind:** `Equivalence`, **CL=3** **iff** the curated taxonomy is **acyclic and anti-symmetric** and uses class-level reasoning.
* **Permitted use**
  **Type-structure** rows allowed (`CL = 3`); Loss: OWL profile limitations (RL/EL/QO).


#### F.9:12.4 - Accuracy (metrology) vs accuracy (data-quality)

* **Cells & Contexts**
  `ISO80000:measurement-accuracy` *(Measurement)* - `ISO25024:data-accuracy` *(Measurement)*
* **Bridge**
  **Kind:** overlap, **CL=2**; Loss: “true value” notion differs (instrument vs dataset), scale transformations.
* **Permitted use**
  **Naming-only** row “accuracy” used for reports; no shared methods.


#### F.9:12.5 - Setpoint (control) vs target (service)

* **Cells & Contexts**
  `CTRL:text:setpoint` *(Status/Control)* - `ITIL:target` *(Status/Service)*
* **Bridge**
  **Kind:** `Disjoint` - Rationale: physical reference value vs business objective; different target kinds (control parameters vs requirement clause).
* **Permitted use**
  Didactic contrast only; prevents accidental substitution in SLO calculus.

#### F.9:12.6 - Role substitution & CL gating (RoleAssignment/enactment scope)

> **Use.** A worked, role-focused restatement of Bridge usage for the recurring question:
> “May `Role_B@B` satisfy `Role_A@A` for `requiredRoles` / enactment checks-”

**Rule.** **No cross-context substitution by name.** If a step in **Context A** needs `Role_A`, and the performer only holds `Role_B` in **Context B**, an explicit **Bridge** **MUST** state how `Role_B@B` relates to `Role_A@A`, with direction, **CL**, and Loss Notes.

##### F.9:12.6.1 - Directional substitution (role-oriented shorthand)

A Bridge may assert, *directionally*:

* **`substitutesFor(Role_B@B > Role_A@A)`** with a CL and a list of **kept** and **lost** characteristics (for roles: typical losses are RCS characteristics and/or RSG nuances).
* The reverse direction **does not** follow unless declared (F.9:13.7).

##### F.9:12.6.2 - CL > gating policy (didactic default)

| **CL** | Meaning (intuitive)                     | **Permit** | **Guard**                                                                            | **Block** |
| :----: | --------------------------------------- | :--------: | ------------------------------------------------------------------------------------ | :-------: |
|  **3** | Near-isomorphic sense; no material loss | Yes | None beyond ordinary gates (e.g., window + RSG state) | - |
|  **2** | Close but with stated losses            |    Yes     | Require **extra evidence** (e.g., additional checklist item) **or** a named reviewer |     —     |
|  **1** | Distant analogy; risky                  | Exception  | Only by explicit **Waiver SpeechAct** naming the Bridge + loss rationale             |  Default  |
|  **0** | Incompatible                            |     No     | —                                                                                    |    Yes    |

*Notes.* The **substitution licence** is defined in **F.9:13.2-13.3** (Role-Assignment/Enactment-eligible substitution requires **CL >= 2**; Naming-only is **CL >= 1**).
CL penalties route to assurance (R) per **B.3**; safety-critical policies may require **CL >= 2** by default (D.2).

##### F.9:12.6.3 - Typical bridges (worked patterns)

* **BPMN Task - PROV Activity.**  
  `substitutesFor(Task@BPMN > Activity@PROV)` with **CL=2**; **lost:** BPMN control-flow guards; **kept:** “bounded occurrence consuming/producing entities.”  
  *Effect.* A Work logged as `Activity@PROV` may satisfy a step requiring a `Task@BPMN` **iff** an extra guard enforces the BPMN pre-/post-conditions.

* **Essence Alpha-State - RoleStateGraph state.**  
  `substitutesFor(“Alpha.State:Ready”@Essence > “Ready”@RSG)` with **CL=2**; **lost:** Alpha-specific narrative criteria; **kept:** checklist-based readiness.  
  *Effect.* A team may reuse Essence states as labels in RSG, but still maintains local checklists as **StateAssertions**.

* **ITIL Service Owner - RBAC Administrator.**  
  Typically **CL=1** and **directional** (Administrator\@RBAC > ServiceOwner\@ITIL) **rejected** unless a policy Bridge enumerates compensating controls.  
  *Effect.* Prevents “ops admin = service owner” conflations without an explicit waiver.

##### F.9:12.6.4 - Bridge invariants (role-relevant reminders)

* **Local first.** Substitution never overrides in-Context role algebra (its own role relations, guards, and exclusions).
* **Loss honesty.** If a Bridge’s loss notes indicate that a dropped characteristic is required by a step, substitution is invalid (regardless of CL).
* **No silent inversion.** Direction is explicit; substitution does not reverse unless declared (F.9:13.7).

### F.9:13 - Reasoning primitives (judgement schemas)

> **All judgements are conceptual.** They license or forbid specific *thinking moves*-not enactment steps and not process enactment surfaces.

#### F.9:13.1 - Bridge declaration

`Bridge(A@RA, B@RB) : senseFamily, kind, dir, CL, Loss, scope`

*Reading:* There exists a declared Bridge between SenseCells `A` and `B` with stated attributes.


#### F.9:13.2 - Substitution licence (senseFamily-preserving)

`Bridge(A,B): same senseFamily f, kind in {Equivalence, Narrower-than, Broader-than}, dir A->B, CL>=2, Loss L -> A may stand in for B at senseFamily f (Role-Assignment/Enactment-eligible)`

*Reading:* A **Substitution Bridge** on the same senseFamily with **CL >= 2** licenses **Role-Assignment/Enactment-level** substitution **in the stated direction**. (`Type-structure` requires **CL = 3**.)


#### F.9:13.3 - Naming-only licence

`Bridge(A,B): kind in {Equivalence, Narrower-than, Broader-than, Partial-overlap}, CL>=1 -> A and B may share a label (Naming-only)`

*Reading:* A Bridge with **CL >= 1** supports using a shared label in prose or Concept-Set **Naming-only** rows, without structural or Role Assignment & Enactment commitments.


#### F.9:13.4 - Prohibition by kind

`Bridge(A,B): kind=Disjoint -> no substitution and no shared row`

*Reading:* **Disjoint** forbids substitution and rows; only contrastive teaching is allowed.


#### F.9:13.5 - Interpretation embargo

`Bridge(A,B): kind in {Design-spec -> Run-trace, Measure-of, Policy-implies} -> Explanation-only`

*Reading:* **Interpretation Bridges** never license substitution or rows.


#### F.9:13.6 - Weakest-link rule for rows

`row R uses {Bridge_i} -> scope(R) = min_i(scopeAllowed(Bridge_i)) and CL(R) = min_i(CL_i)`

*Reading:* The **row scope** and **row CL** are bounded by the weakest participating Bridge.


#### F.9:13.7 - Direction guard

`Bridge kind=Narrower-than with dir A->B -> not(B may stand in for A)`

*Reading:* Narrower>Broader does **not** invert; only A may substitute into B under the stated scope.


#### F.9:13.8 - SenseFamily purity

`Bridge scope=Role Assignment & Enactment-eligible -> same senseFamily(A,B) and same stance(A,B)`

*Reading:* Role Assignment & Enactment-level substitution requires **same senseFamily** and same stance (run-time or design time).


#### F.9:13.9 - Loss accumulation

`A->B with Loss L1 and B->C with Loss L2 -> A->C allowed only if the same senseFamily is preserved, CL=min(CL1,CL2), and Loss accumulates as L1 union L2`

*Reading:* Chained substitution is rarer; if used, **accumulate Loss** and respect the **minimum CL**. When in doubt, avoid chaining across Contexts.


### F.9:14 - Relations

**Builds on:** E.10.D1 (Context discipline: Context = U.BoundedContext); **F.0.1 (senseFamily guard; Bridge-only crossing)**; F.1 (Contexts fixed); F.2/F.3 (Cells exist); F.7 (rows depend on Bridges); F.8 (thresholds and reuse choice).

**Coordinates with:** `F.9.1` for stance overlays that remain subordinate to bridge cards; `E.17.1` when viewpoint bundles need explicit cross-family correspondence; `A.6.Q` / `C.25` when evaluative endpoints or bundle-shaped quality families cite bridge cards without absorbing bridge semantics.

**Constrains:**

* **F.7 Concept-Set Table:** each cross-context row must name supporting **Bridges**; row scope <= the weakest supporting Bridge.
* **F.8 Mint or Reuse:** reuse choices reference **CL** and **kind**; no reuse without a Bridge.
* **Part C patterns:** formal claims that span Contexts cite Bridges and respect senseFamily/StatusModality & CL constraints.
* **B.3 Trust & Assurance Calculus:** may interpret **CL** as a penalty factor in Cross-context reasoning.


### F.9:15 - Migration notes (conceptual)

1. **Edition shift in a Context.** Re-read affected **Cells**; if sense moved, split the Bridge or **lower CL**; keep the older Bridge for historical claims.
2. **New evidence of mismatch.** Add a **counter-example**; decrease `CL` or change bridge kind (for example from `Equivalence` to `Partial-overlap` or `Disjoint`).
3. **Convergence over time.** When invariants demonstrably match, and counter-examples evaporate, **raise CL** cautiously; for **CL=3**, cite invariants.
4. **senseFamily refactor.** If a Cell’s senseFamily was mis-typed, fix the senseFamily first in F.3, then revisit Bridges; **Interpretation** is safer than forced substitution.
5. **Row under-protected.** If a row’s scope exceeds the weakest Bridge, either **split the row** by Context or **downgrade scope** to Naming-only.
6. **Bridge sprawl.** Consolidate near-duplicates into one Bridge with richer **Loss Notes**; retire the rest.


### F.9:16 - Acceptance tests (SCR/RSCR — concept-level)

#### F.9:16.1 - Static conformance (SCR)

* **SCR-F9-S01 (Well-typed).** Every Bridge names **two SenseCells**, each bound to a **Context** from F.1, and states **senseFamily**, **kind**, **dir** (if needed), **CL**, **Loss**, and **scope**.
* **SCR-F9-S02 (senseFamily discipline).** Any Bridge that licenses **Role/Enactment-eligible** substitution is **senseFamily-preserving** and has kind in {`Equivalence`, `Narrower-than`, `Broader-than`}.
* **SCR-F9-S03 (Loss visibility).** Every Bridge has **non-empty Loss Notes** (the word "none" is allowed only with **CL=3** and stated invariants).
* **SCR-F9-S04 (Counter-example hygiene).** Bridges with **CL <= 2** carry at least one **counter-example**; Bridges with **CL=3** cite **matching invariants**.
* **SCR-F9-S05 (Row compliance).** Every Concept-Set row shows a **scope** no greater than the **minimum CL** across its supporting Bridges; no row relies on **Interpretation** Bridges.

#### F.9:16.2 - Regression (RSCR)

* **RSCR-F9-E01 (Edition churn).** When a Context-s edition changes, re-validate all Bridges touching it; flag `CL` drift and update rows- scopes if needed.
* **RSCR-F9-E02 (Counter-example drift).** New counter-examples lower **CL**; deletions do not automatically raise **CL**.
* **RSCR-F9-E03 (senseFamily drift).** If a Cell-s `senseFamily` is corrected, all Bridges crossing that Cell are re-typed; any substitution that would now cross senseFamilies is invalidated.
* **RSCR-F9-E04 (Weakest-link enforcement).** Adding a low-CL Bridge to a row reduces the row-s scope; if the row-s published scope would exceed the new minimum, split or downgrade the row.


### F.9:17 - Didactic distillation (90-second script)

> -A **Bridge** translates between **local senses** from different **Contexts**. It always declares **what relation** holds (`Equivalence`, `Narrower-than`, `Broader-than`, `Partial-overlap`, `Disjoint`, or an interpretation such as `Design-spec -> Run-trace`), **how strong** (`CL 0-3`), **which way** (when direction matters), and **what is lost**. **Substitution** is allowed only on the **same senseFamily** and only with **CL >= 2**; **Type-structure** needs **CL = 3**. **Interpretation Bridges** explain, never substitute. Rows in the Concept-Set table obey the **weakest-link**: their scope cannot exceed the lowest `CL` among their Bridges. When editions change or counter-examples surface, lower `CL` or change bridge kind; if two senses truly converge and invariants match, raise to **CL = 3**-rarely, and with reasons. Translate across Contexts; never collapse them.-

#### F.9:17.1 - Bridge stance overlay compatibility
A bridge card may carry a `F.9.1` Bridge Stance Overlay such as `localRename`, `operationalizes`, `partialAnalogy`, `projection`, or `nonEquivalent`. The overlay is an authoring annotation and **does not replace** the underlying bridge kind, direction, `CL`, or loss notes.

### F.9:18 - Archetypal Grounding

#### F.9:18.1 - Tell

A Bridge is not a synonym claim and not an enactment edge. It is a context-bounded correspondence record that tells a reader what may be reused, what may only be explained, and what is lost when meaning is transported.

#### F.9:18.2 - Show (System lane)

A service team may reuse the word *availability* across monitoring, SLO review, and architecture discussion. F.9 requires the team to publish Bridge Cards that separate observation, status target, and architectural concern rather than treating the shared label as silent sameness. The benefit is that naming convenience survives while substitution rights stay bounded by `senseFamily`, `CL`, and Loss Notes.

#### F.9:18.3 - Show (Episteme lane)

A comparative bundle may say that two traditions both discuss *readiness* or *capability*. Under F.9, that statement is only explanatory until the author publishes the two SenseCells, the Bridge kind, direction, `CL`, and the counter-example that marks where the comparison stops. The Bridge then becomes an auditable correspondence rather than a rhetorical shortcut.

### F.9:19 - Bias-Annotation

Lenses tested: **Gov**, **Arch**, **Onto/Epist**, **Prag**, **Did**. Scope: **Universal** for cross-context correspondence and reuse.

* **Gov bias:** F.9 raises the authoring bar by requiring explicit Bridge Cards.
  *Mitigation:* keep the card compact and teach weakest-link discipline as the default review heuristic.
* **Arch bias:** the pattern prefers typed bridge declarations over friendly synonym prose.
  *Mitigation:* allow Naming-only scope and explanatory Interpretation Bridges so useful comparisons are not blocked.
* **Onto/Epist bias:** F.9 is strongly local-first and resists global meaning claims.
  *Mitigation:* reuse remains possible, but only through explicit correspondence, direction, and Loss Notes.
* **Prag bias:** conservative `CL` assignment may feel slower than informal reuse.
  *Mitigation:* the pattern still licenses bounded substitution when the evidence is good enough; it only blocks silent overreach.
* **Did bias:** the didactic script can make Bridge Cards look simpler than they are.
  *Mitigation:* Conformance, counter-examples, and weakest-link rules keep the teaching surface tied to real constraints.

### F.9:20 - Conformance Checklist (CC-F.9)

A Bridge publication conforms to F.9 iff:

1. **CC-F.9-1 - Well-typed Bridge declaration.**
   Every Bridge names two SenseCells bound to declared Contexts and publishes kind, direction (if needed), `CL`, Loss Notes, and allowed use.
2. **CC-F.9-2 - Substitution discipline.**
   Any substitution or row licence comes only from a Substitution Bridge on the same `senseFamily`; Role Assignment & Enactment-level substitution requires `CL >= 2`, and Type-structure substitution requires `CL = 3` plus matched invariants.
3. **CC-F.9-3 - Interpretation embargo.**
   Interpretation Bridges remain explanation-only and are not used to justify substitution or Concept-Set rows.
4. **CC-F.9-4 - CL honesty and loss visibility.**
   Bridges with `CL <= 2` publish a counter-example or explicit boundary case; Bridges with `CL = 3` publish the invariants that justify the stronger licence; all Bridges publish Loss Notes.
5. **CC-F.9-5 - Weakest-link row discipline.**
   Cross-context rows never claim a scope or row-level `CL` stronger than the weakest participating Bridge.
6. **CC-F.9-6 - Overlay non-collapse.**
   If a `F.9.1` Bridge Stance Overlay is used, it remains an annotation and does not replace bridge kind, direction, `CL`, or Loss Notes.
7. **CC-F.9-7 - Registry-reference discipline.**
   `BridgeId` and cited policy pins are treated as registry references, not as signature-exported semantic symbols.

### F.9:21 - Consequences

**Benefits.**
F.9 lets FPF compare, translate, and partially reuse ideas across Contexts without collapsing them into one vocabulary. It gives downstream rows, claims, and assurance reasoning an explicit correspondence surface instead of relying on prose intuition.

**Trade-offs / mitigations.**
The pattern adds explicit card authoring and may feel heavier than informal comparison. Mitigation: use Naming-only scope when explanation is enough, and reserve stronger licences for Bridges that really earn them.

### F.9:22 - Rationale

The core move of F.9 is simple: cross-context work is unavoidable, but silent sameness is unacceptable. A Bridge therefore does two jobs at once:

* it preserves practical reuse where bounded transport is genuinely available, and
* it keeps non-identity visible through direction, Loss Notes, `CL`, and weakest-link scope.

Without that discipline, every shared label becomes a hidden ontology merger. With it, cross-context comparison stays teachable, auditable, and compatible with the rest of FPF.

### F.9:23 - SoTA-Echoing

This pattern adds no new empirical claim beyond its canonical bridge discipline; the alignment note below explains why that discipline still matches contemporary practice.

Contemporary ontology-alignment, knowledge-integration, and interoperability practice already prefers explicit typed correspondences over raw lexical identity. F.9 **adopts** that explicit-correspondence stance, **adapts** it by making `senseFamily`, `CL`, and Loss Notes normative card fields, and **rejects** string-equals identity as a reuse licence.

Current integration practice also distinguishes explanatory mappings from substitutive equivalence. F.9 **adopts** that distinction, **adapts** it into the explicit split between Substitution Bridges and Interpretation Bridges, and **rejects** any attempt to reuse an explanatory Bridge as if it granted substitution or row scope.

Contemporary architecture-description and systems-integration practice likewise keeps context and viewpoint boundaries explicit rather than fungible. F.9 **adapts** that discipline by binding every Bridge to SenseCells in declared Contexts and by forcing downstream rows to obey the weakest-link rule instead of outrunning the supporting correspondences.

### F.9:24 - Bridge Card Publication Discipline

#### F.9:24.1 - Minimal bridge package
A usable Bridge Card should make visible:

- the two typed SenseCells,
- the bridge kind,
- direction where direction matters,
- declared `senseFamily`,
- `CL`,
- explicit Loss Notes,
- and the licensed use or row consequence.

If any of these fields is absent, later readers are forced back into inference by prose similarity, which is exactly what `F.9` is supposed to block.

#### F.9:24.2 - One-pair default rule
The default authoring discipline is one primary Bridge per cell pair per relevant `senseFamily`, with richer Loss Notes rather than many near-duplicate cards. Local exceptions are lawful only when the cards genuinely differ in bridge kind, direction, or admissible use.

#### F.9:24.3 - Revision over silent drift
If later evidence changes bridge strength, direction, or loss, the Bridge Card should be revised explicitly. It should not be left in place while surrounding prose quietly changes the practical licence.

### F.9:25 - Bundle and Endpoint Interaction Law

#### F.9:25.1 - Viewpoint and bundle interaction
Viewpoint bundles, quality bundles, and other endpoint bundles may cite Bridges, but they do not absorb bridge semantics. `F.9` remains the owner of cross-context alignment, while the citing bundle remains the owner of its own ontology.

#### F.9:25.2 - Quality-family interaction
When a quality family claim crosses contexts, bridge loss and `CL` affect what may be compared or reused, but they do not retype the quality family itself. Any resulting assurance penalty routes to `R` rather than changing the ontology of `F`, `G`, or the Q-Bundle head.

#### F.9:25.3 - Overlay interaction rule
A `F.9.1` stance overlay may help readers interpret a bridge, but the bridge card remains primary. If the overlay sounds stronger than the bridge kind, direction, `CL`, or Loss Notes, the card wins and the overlay should be weakened or removed.

### F.9:26 - Review Matrix and Migration Tests

A reviewer can test bridge integrity with six questions:

1. **Are the two cells and contexts explicit-**
2. **Is the bridge kind the weakest truthful kind rather than the friendliest one-**
3. **Does `CL` match the published counter-example or invariant burden-**
4. **Are Loss Notes specific enough that the licensed use is really bounded-**
5. **If a row or bundle cites the bridge, does it stay within the bridge's licensed use-**
6. **If a stance overlay exists, does it remain strictly weaker than the bridge card itself-**

Migration from legacy "same/equivalent/align/map" prose should therefore recover the Bridge Card first, then any row licence, then any optional stance overlay. Doing it in the opposite order recreates silent equivalence under new vocabulary.
### F.9:End

