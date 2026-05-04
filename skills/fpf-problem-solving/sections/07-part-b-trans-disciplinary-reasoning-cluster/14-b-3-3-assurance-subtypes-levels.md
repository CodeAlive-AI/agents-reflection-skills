## B.3.3 — Assurance Subtypes & Levels

### B.3.3:1 - **Problem Frame**

A complex project may generate hundreds of artifacts: design specifications, simulation models, test suites, and operational logs. While the Trust & Assurance Calculus provides a framework for evaluating these artifacts, teams often face a critical challenge: how to aggregate this diverse evidence into a single, meaningful signal of an artifact's maturity. Simply counting the number of tests or documents can lead to "paper compliance," where an artifact appears well-supported but has critical, unexamined weaknesses in its formal structure or conceptual alignment.

### B.3.3:2 - **Problem**

How do we create an objective, auditable, and balanced Standard for what constitutes "trustworthiness" at each stage of an artifact's development cycle? FPF requires a mechanism that moves beyond simple evidence counting to a qualitative assessment of assurance. This mechanism must prevent common failure modes, such as over-investing in run-time validation (LA) at the expense of design-time verification (VA), or neglecting the critical work of ensuring concepts are correctly mapped and typed (TA).

### B.3.3:3 - **Solution**

FPF establishes a formal Standard that links three distinct **Assurance Subtypes** to three computable **Assurance Levels**. An artifact's level is not assigned manually by an author; it is **derived automatically** by its anchored evidence. This creates a transparent and falsifiable system for tracking an artifact's journey from a speculative idea to a robust, reliable holon.

#### B.3.3:3.1 - Assurance Subtypes: The Three Pillars of Trust

These three subtypes categorize the kind of question an assurance activity answers, ensuring a balanced approach to building confidence.

| Subtype | Code | Core Question | Links to Epistemic Score | Manager's View: What It Prevents |
| :--- | :--- | :--- | :--- | :--- |
| **Typing Assurance** | TA | “Does the artifact faithfully represent its intended concept?” | **CL** (Congruence Level) | **Miscommunication & Integration Failures.** TA ensures that when a requirement says "Sensor," the design model's "Sensor" component is the same conceptual thing. This activity directly improves the Congruence Level (CL) of the integration *edges* between artifacts. |
| **Verification Assurance**| VA | “Is the holon logically correct under its stated assumptions?” | **FV** (Formal Verifiability)| **"It Works on Paper" Errors.** VA catches design flaws, logical inconsistencies, and specification errors before a single line of code is written or a physical part is machined. It ensures the blueprint is sound. |
| **Validation Assurance**| LA | “Does the holon work correctly in the real world?” | **EV** (Empirical Validability)| **"Works in the Lab, Fails in the Field" Surprises.** LA confirms that the holon performs as expected under real or simulated operational conditions, accounting for noise, unexpected inputs, and environmental factors. |

#### B.3.3:3.2 - Computed Assurance Levels: The Ladder of Maturity

An artifact’s level is computed based on the evidence it has accumulated. This creates a clear, step-by-step path for increasing trust.

| Level | Name | How It Is Computed |
| :--- | :--- | :--- |
| **Level 0** | **Unsubstantiated** | No `verifiedBy` or `validatedBy` evidence is present. The artifact is a claim or an idea. |
| **Level 1** | **Substantiated** | At least one `verifiedBy` or `validatedBy` link to an evidence artifact exists, and the artifact is supported by Typing Assurance (TA). |
| **Level 2** | **Axiomatic** | The artifact is `verifiedBy` either a proof **or** a **Compose‑CAL (Γₘ) constructive narrative** that the author has linked from the Working‑Model via `tv:groundedBy` (CT2R‑LOG). Its FormalVerifiabilityScore (FV) meets or exceeds a pre‑defined threshold. Additionally, if the holon is designated as safety‑critical, it **MUST** also be supported by **Validation Assurance (LA)**. For non‑critical holons, LA is strongly recommended (`SHOULD`). |

> **Didactic Note for Managers: What 'Level 1' Really Means**
>
> Think of moving from Level 0 to Level 1 as the first step toward professional seriousness.
>
> *   **Level 0** is an idea on a whiteboard. It has potential, but no receipts.
> *   **Level 1** means you have **at least one receipt**. You have anchored the idea to something concrete: a passing test, a formal sketch, a simulation result. It's no longer just an opinion.
>
> Crucially, Level 1 also demands **Typing Assurance (TA)**. This sounds technical, but its business impact is simple: **it means you've named your terms correctly and consistently**. You've used the Role-Projection Bridge (Pattern B.5) to ensure that the "Sensor" in your requirements document is the same "Sensor" in your architectural diagram. This basic alignment work is what prevents costly integration failures and endless meetings where teams talk past each other. Good typing is the foundation of clear communication, and at Level 1, FPF makes it mandatory.

### B.3.3:4 - **Conformance Checklist**

To ensure the integrity of the assurance calculus, the following rules are normative. A **Target of Assurance (ToA)** is any working-model element designated as a root claim (e.g., a top-level system requirement, safety goal, or core hypothesis).

*   **CC-B3.3.1 (L1 Anchor Mandate):** A ToA **SHALL NOT** be considered to have reached `AssuranceLevel:L1` unless it is linked to at least one evidence artifact via `verifiedBy` or `validatedBy`.
*   **CC-B3.3.2 (L1 Typing Mandate):** A ToA at `AssuranceLevel:L1` or higher **MUST** be supported by **Typing Assurance (TA)**. This includes, at a minimum, that its core concepts are mapped via the Role-Projection bridge (Pattern B.5) and it conforms to its declared schema.
*   **CC-B3.3.3 (L2 V&V Mandate):** A ToA at `AssuranceLevel:L2` **MUST** satisfy all L1 criteria. In addition, it **MUST** be supported by **Verification Assurance (VA)** with `FV ≥ threshold_FV`. For holons designated as safety-critical (e.g., `criticality ≥ SIL-2`), the ToA **MUST** also be supported by **Validation Assurance (LA)** with `EV > 0`. For non-critical holons, LA **SHOULD** be present.
    *   *Exemption Note:* Purely formal artifacts (e.g., mathematical axioms) may justify an exemption from the LA requirement, provided this is documented in their rationale.
*   **CC-B3.3.4 (Concept-Bridge Completeness):** For any mechanism used in a model at `AssuranceLevel:L1` or higher, all of its mandatory U.Types **MUST** be mapped to domain concepts via the Role-Projection bridge (Pattern B.5).
*   **CC-B3.3.5 (Scope Separation):** Assurance claims **MUST** maintain a strict separation between `design-time` and `run-time` scopes (Pattern A.4). An assurance tuple for a `MethodDescription` (design-time) SHALL NOT be conflated with one for its corresponding `Work`/`Trace` (run-time). The Evidence Graph Ref (`verifiedBy`, `validatedBy`) must point to artifacts of the appropriate scope.
* **CC-B3.3.6 (CT2R‑LOG Handshake):** If a ToA depends on **structural** claims, those claims **SHALL** be published as **Working‑Model** relations and, when used to justify `L2`, **SHALL** declare `validationMode=axiomatic` and provide **Constructive** grounding with `tv:groundedBy → Γₘ.(sum|set|slice)` (see B.3.5 and C.13).  
* **CC-B3.3.7 (Downward‑Only Dependence):** Assurance artefacts (Mapping/Logical/Constructive/Evidence) **SHALL NOT** impose vocabulary or layout back onto the Working‑Model surface (E.14).
 
### B.3.3:5 - **Common Anti-Patterns and How to Avoid Them**

| Anti-Pattern | Manager's View: What It Looks Like | How FPF Prevents It |
| :--- | :--- | :--- |
| **The "Tested but Untyped" Mess** | "Our code has 100% test coverage, but we still have integration bugs and nobody understands what the code do." | **CC-B3.3.2** makes Typing Assurance (TA) mandatory for L1. You cannot claim your work is "Substantiated" without first ensuring your terms and concepts are clear and consistently mapped. |
| **The "Perfect Blueprint, Flawed Reality"** | "The design was formally proven to be perfect, but the physical product failed catastrophically in the field." | **CC-B3.3.3** mandates Validation Assurance (LA) for safety-critical systems at L2. A perfect blueprint (`FV=4`) is not enough; you must also provide empirical evidence (`EV>0`) that it works in the real world. |
| **The "Paper Compliance" Shell Game** | "We have thousands of documents and links, so we must be at a high assurance level." | The computed `AssuranceLevel` is not based on the *quantity* of evidence but on its *type* and *quality* (via FV/EV scores). You cannot reach L2 without strong formal verification (VA), no matter how much validation (LA) you do. |

### B.3.3:6 - **Consequences**

| Benefits | Trade-offs / Mitigations |
| :--- | :--- |
| **Objective Gatekeeping:** The rules provide a clear, objective, and falsifiable basis for an artifact's assurance status, eliminating subjective judgment and "assurance theater." | **Risk of Over-stringency:** The rules might feel too strict for rapid prototypes. *Mitigation:* The requirements for `L1` are deliberately lightweight, demanding only one piece of evidence and basic typing, making the first step onto the ladder accessible. |
| **Balanced Assurance:** The Standard requires a mix of evidence types for higher levels, preventing teams from over-investing in one area (e.g., testing) while neglecting another (e.g., formal specification). | **Risk of Evidence Inflation:** Teams might add trivial evidence just to meet the criteria. *Mitigation:* The quality of evidence is assessed via the epistemic scores (FV, EV, CL); merely linking to low-quality evidence will not significantly raise the scores needed for L2. |
| **Clear Progress Tracking:** The ladder provides a clear roadmap for maturing an artifact from an idea to a fully assured component, making planning and progress monitoring transparent. | **Overhead for Complex Holons:** A holon with many ToAs may require significant assurance work. *Mitigation:* The framework allows grouping, where a parent claim's evidence can satisfy the coverage requirements for its children if explicitly declared. |

### B.3.3:7 - **Rationale**

This pattern transforms the assurance framework from a descriptive taxonomy into a prescriptive, actionable Standard. By binding the computed `AssuranceLevel` to mandatory, well-defined evidence coverage, it makes the notion of "trustworthiness" in FPF an objective and auditable property. The rules ensure that as an artifact's formality and claimed reliability increase, the rigor and balance of its supporting evidence increase in lockstep, operationalizing the principle of "no blind trust." The separation of `design-time` and `run-time` evidence, mandated by CC-B3.3.5, further ensures that claims made about a blueprint are not confused with claims made about a running system, preserving the integrity of the entire lifecycle.

### B.3.3:8 - **Relations**

*   **Builds on:** `B.3.1 Characteristic & Epistemic Spaces`, `A.10 Evidence Graph Referring`, `A.4 Temporal Duality`.
*   **Constrains:** The computation and interpretation of `AssuranceLevel` for all holons.
*   **Enables:** Objective quality gates in the Canonical Evolution Loop (B.4) and reliable inputs for the Trust-Aware Mediation Calculus (D.4).

### B.3.3:End

