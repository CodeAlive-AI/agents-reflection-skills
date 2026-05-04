## The "Bitter Lesson" trajectory — compute, data, and freedom over hand‑tuned rules (FPF stance)
Empirical progress since 2015 supports the “Bitter Lesson” (Sutton, 2019): systems that leverage *more data*, *more compute*, and *more freedom* (less hand‑coded domain procedure) tend to outperform bespoke rule‑engineered solutions. Scaling‑law work (e.g., 2020–2022) shows that broader models benefit from compute/data scaling; instruction‑following and tool‑use methods (2019–2024) let general models adapt across tasks without per‑task re‑engineering (e.g., ReAct‑style tool use, self‑reflection/Reflexion, autonomous open‑world exploration such as Voyager/Auto‑GPT‑class agents).

 FPF separates *goals and constraints* from *procedures*. We prefer **Rule‑of‑Constraints (RoC)** — explicit prohibitions, budgets, and safety envelopes — over **Instruction‑of‑Procedure (IoP)** — detailed step‑by‑step scripts. RoC keeps the **design–run separation** intact: designers declare *what must not happen* and *what budgets apply*; agents have freedom of choose *how* to act within those bounds at run‑time. 

**Implications for architecture (normative hooks inside FPF):**
- **Express behavior as goals, constraints, and budgets.** Prefer RoC to IoP. When you must prescribe a procedure (regulatory/safety), document the exception in the Design‑Rationale Record and pair it with run‑time monitors (see *Observability‑first templates*).
- **Autonomy budgets.** For each agent/holon, declare allowed tools, call‑rates, cost/time ceilings, and risk thresholds. Enforce via policy/telemetry cells; record usage in the **Comparability Governance (CG) frame** so that uplift/regret can be compared over runs.
- **Agentic tool use.** Orchestrate function calls via agentic planning/reflective loops instead of fixed pipelines: the agent can choose order, retry strategies, and escalation paths (cf. ReAct‑style tool use, self‑reflection, autonomous exploration in 2022–2024 SoTA). This keeps logic in prompts/policies, not in brittle DAGs.
- **Compute and data elasticity.** Keep **bench/test packs** versioned; enable periodic model refresh without rewriting logic (Chinchilla‑style scaling insight, 2022). Treat data > code when feasible; ensure refresh does not break **parity/comparability** by pinning to the CG‑frame.
- **Feedback‑in‑the‑loop.** Build preference/critique channels (human‑, AI‑, or environment‑in‑the‑loop), shadow modes, and safe A/B gating. Use these to continuously adjust prompts/policies rather than continuously fine‑tuning bespoke sub‑models.
- **Safety first.** Encode **rules‑as‑prohibitions** (create **Constitution-based framework**) and **risk budgets** as RoC; keep them small, explicit, and testable. Combine with design‑run separation to prevent prompt drift from violating safety envelopes.

A **Rule‑of‑Constraints (RoC)** is a compact, versioned policy bundle: *(a)* scope (holon/agent + tools), *(b)* budgets (cost/time/call‑rate), *(c)* prohibitions (red lines), *(d)* escalation (who/what to consult), *(e)* telemetry (metrics to log into the CG‑frame). RoC is enforced at run‑time but never prescribes the exact procedure.

**Why not just add more rules?** Because micro‑ontologies and brittle flow‑charts do not generalize. FPF uses rules to define *boundaries* and *measurement frames* while giving agents freedom to search within them using general models. The inner loop remains empirical: **measure → reflect → adjust RoC/prompts → run**.

**Expected outcomes.** Faster iteration (minutes‑to‑change via prompt/policy edits), resilience to model refresh, lower authoring cost, and higher autonomy at comparable risk thanks to budgets + telemetry + CG‑framed comparability.

