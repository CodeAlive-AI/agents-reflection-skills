# Generating and Maintaining the Thesaurus

Read this when the user asks to create, generate, update, or audit the project thesaurus.
For naming consultation (the frequent case), the main SKILL.md has everything you need.

## Creating a New Thesaurus

**Derive the thesaurus from the codebase** — not from docs or specs.

### Step 0: Determine the thesaurus path

1. If the user specified a path — use it
2. Search the repo for an existing `THESAURUS.md`: `find . -name "THESAURUS.md" -not -path "*/node_modules/*"`
3. If found — use the existing location
4. Default: `docs/THESAURUS.md` (create `docs/` if it doesn't exist)

Use this resolved path throughout all subsequent steps.

### Step 1: Scan high-signal hubs (do NOT read the whole codebase)

An agent cannot scan an entire repository without exhausting context. Instead, target
**structural files that are dense with domain nouns** — 5-10 tool calls covers 80-90%:

1. **DB schemas and migrations** — ORM model definitions, schema files, migration scripts
2. **API contracts** — OpenAPI/Swagger specs, GraphQL schemas, route/controller definitions
3. **Domain layer** — aggregate/entity/value-object type declarations
4. **Directory structure** — `ls` top-level dirs to map product areas (cheap, zero-read)
5. **Symbol extraction** — grep for type/class/interface/struct declarations across source

**Stop conditions:**
- If the repo has multiple product areas, ask the user which to catalog first
- Stop when new scans mostly return terms already seen (diminishing returns)
- Default to one bounded area at a time, not the entire monorepo

**Do NOT rely on docs** — they're often outdated. If a README says "User" but the code
says "Customer" everywhere, the canonical term is "Customer".

**Scope the thesaurus to the problem.** Don't catalog every noun in the codebase —
catalog only terms that matter for the system's purpose. Include a term if: domain
experts use it, it appears in invariants/commands/events, ambiguity about it has caused
bugs, or multiple synonyms exist. Exclude purely technical infrastructure terms
(LogLevel, RetryPolicy, ConnectionPool). **Target: 15-40 terms per bounded context.**
Past 60 you're likely including infrastructure; fewer than 10 you're missing concepts.

### Step 2: Separate active from legacy/obsolete

Codebases accumulate dead weight. When scanning, classify each term:

- **Active**: Used in current code paths, referenced by live features
- **Legacy**: Still in codebase but deprecated, behind feature flags, or in migration layers. Mark with `[LEGACY]` prefix and note what replaces it
- **Obsolete**: Dead code, unused classes, abandoned tables. Don't add to thesaurus — just note for cleanup

**How to detect legacy/obsolete:**
- Classes/tables with `Legacy`, `Old`, `Deprecated`, `V1`, `V2` prefixes/suffixes
- Code behind `if (featureFlag)` guards or `#if LEGACY` preprocessor directives
- Methods marked `@Deprecated`, `[Obsolete]`, or with deprecation comments
- Database tables with zero recent writes (check with user)
- Modules that nothing imports anymore (check import graph)
- Names that only appear in test fixtures or migration scripts

**Ask the user** when classification is ambiguous: "I found `UserProfile` and `CustomerProfile` — which is the active concept? Is the other legacy?"

### Step 3: Cluster, identify conflicts, collect ambiguities

- Group synonyms and variants (same concept, different names)
- Identify polysemy (same name, different concepts in different places)
- Flag naming inconsistencies between active code and its tests/docs

**Don't stop on each ambiguity** — collect them all into the `## Unresolved` section
of the thesaurus. This lets you scan the entire codebase in one pass and gives the
user a complete picture to prioritize, rather than answering questions one by one.

For each ambiguity, record: what term, where it's found, what the question is,
how many files are affected, and possible resolutions if obvious.

### Step 4: Write the thesaurus

Write `THESAURUS.md` with what you know:
- Active terms go to `## Terms`
- Deprecated terms go to `## Legacy Terms`
- All ambiguities go to `## Unresolved`

**Start with a flat thesaurus** — just a single list of terms without bounded contexts.
Most projects don't need context separation. Only introduce bounded contexts later
if Step 5 reveals genuine polysemy.

### Step 5: Surface unresolved issues

**This step is mandatory** — always runs right after writing the file.

After creating `THESAURUS.md`, explicitly present the `## Unresolved` section to the
user. Frame it as: "The thesaurus is ready, but there are N naming conflicts that
need your input — without resolving them, the thesaurus quality will suffer."

List each issue with its impact. Example output:

```
THESAURUS.md created with 24 terms, 3 legacy terms, and 5 unresolved issues:

1. `Account` — used as financial entity (billing/) AND user identity (auth/) — 18 files affected
2. `User` vs `Customer` — synonym drift between API and domain layers — 31 files
3. `Process` — means workflow in scheduler/, means OS process in runtime/ — 7 files
4. `Status` — enum with 12 values, some overlap with `State` enum — 15 files
5. `Service` — bare word used 40+ times, needs polysemy unpacking

Which would you like to resolve first?
```

As the user resolves each item, promote it from `## Unresolved` to `## Terms`
(or `## Legacy Terms`). Items the user defers stay as documented naming debt.

### Step 6: Update project instructions

**This step is mandatory** — the thesaurus is only useful if the agent knows about it.

After creating the thesaurus, add a reference to it in **all** agent instruction files
found in the project. Check for and update whichever exist:

- `CLAUDE.md` (Claude Code)
- `GEMINI.md` (Gemini CLI)
- `AGENTS.md` (multi-agent)
- `.cursorrules` (Cursor)
- `.github/copilot-instructions.md` (GitHub Copilot)

Propose adding a section like (use the resolved path from Step 0):

```markdown
## Domain Language

This project maintains a domain thesaurus at `docs/THESAURUS.md`.

- **Before naming any new entity** (class, method, variable, DB table, API endpoint),
  read `docs/THESAURUS.md` first. If the concept already has a canonical term — use it.
- **Before introducing a new domain term**, add it to `docs/THESAURUS.md` first.
- Terms in the "Synonyms to AVOID" lists must never appear in new code.
- See the "Forbidden Lexicon" section for terms banned from the domain layer.
```

This ensures every agent session — even without the ubiquitous-language skill installed —
knows the thesaurus exists and should consult it.

### Step 7 (optional): Detect polysemy

**Do NOT pre-assign bounded contexts.** The agent cannot reliably determine context
boundaries — this is an architectural decision that requires deep domain knowledge.

Instead, look for **evidence of polysemy** — the same word meaning different things:
- Same class name in different modules/packages with different fields/methods
- Same DB column name with different semantics in different tables
- Same API term used inconsistently across endpoints
- User/team disagreement about what a term means

**When you find evidence**, don't decide — report it to the user:
"I found `Account` used in two different ways: as a financial entity in `billing/`
and as a user identity in `auth/`. Should these be separate bounded contexts, or is
one of them a legacy naming mistake?"

Only add `## Bounded Context:` sections to the thesaurus after the user confirms
the separation. A wrong context boundary is worse than no boundary.

**The invariant test** (from FPF A.1.1): A bounded context is justified only when you
can name **at least one rule (invariant)** that is true inside the context but not
outside. Example: "An Order in Sales context can be cancelled; an Order in Fulfillment
context cannot be cancelled once shipped." If you can't name such a rule — it's just
a module, not a bounded context.

### Bootstrap Template

```markdown
# Project Thesaurus

> Domain glossary following DDD ubiquitous language. Every name in code, APIs, docs,
> and conversations must use terms from this thesaurus. Update this file BEFORE
> introducing new concepts.
>
> **Rules:**
> 1. One canonical term per concept — no synonyms in code
> 2. New concepts must be added here before being used in code
> 3. "Avoid" terms must never appear in new code
> 4. When renaming, update all references (code, docs, API, DB)

## Forbidden Lexicon

> Terms that MUST NOT appear in the domain layer. These are implementation details,
> weasel words, or ambiguous terms that must always be replaced with a specific
> domain term from this thesaurus.

| Forbidden Term | Why | Use Instead |
|---------------|-----|-------------|
| Manager | Vague, hides responsibility | [specific domain activity] |
| Handler | Generic | [what it handles] |
| Service | Overloaded — see Polysemy section | [specific facet] |
| Info / Data | Meaningless suffix | [the domain term itself] |

## Terms

### [Term]
- **Definition**: [What this means in the business domain]
- **NOT**: [What this does NOT mean — other concepts it could be confused with]
- **Synonyms to AVOID**: [Words that mean the same but must not be used]
- **Related terms**: [Other thesaurus entries this connects to]

## Legacy Terms

> Terms still present in the codebase but deprecated or being phased out.
> New code MUST use the replacement term. Legacy terms are kept here to help
> developers reading old code understand what they mean.

### [Legacy Term] `[LEGACY]`
- **Definition**: [What this meant]
- **Status**: Deprecated since [date/version]. Being replaced by [new term]
- **Still found in**: [modules/files where it persists]
- **Replacement**: [canonical term from active thesaurus]

## Unresolved

> Naming ambiguities, contradictions, and open questions found during thesaurus
> generation. Each entry needs a human decision before the term can be added to
> the active thesaurus. Resolve these top-down by impact.

### `[Term]` — [short description of the problem]
- **Found in**: [where in code this term appears with different meanings/usage]
- **Question**: [what needs to be decided]
- **Impact**: [how many files/modules are affected]
- **Options**: [possible resolutions, if known]

<!-- Add these sections ONLY when confirmed polysemy requires them:

## Bounded Context: [Context Name]

### [Term]
- **Definition**: [What this means in THIS context]
- **NOT**: [What it means in other contexts]
- **Synonyms to AVOID**: [list]

## Cross-Context Bridges

| Term | Context A meaning | Context B meaning | Relationship | Loss Notes |
|------|-------------------|-------------------|-------------|------------|

-->
```

## Polysemy Unpacking

Some terms are "bundle-collapse" words — they silently stand in for multiple distinct
concepts. The word "service" is the canonical example: it can mean a promise, a system,
an endpoint, a commitment, a delivery method, or a work episode — all at once.

**When you encounter an overloaded term**, unpack it into its facets:

1. **Identify the facets** — what distinct things does this word refer to?
2. **Create separate thesaurus entries** for each facet with qualified names
3. **Add the bare word to the Forbidden Lexicon** — it must always be qualified
4. **Document which facet is meant** in each code location

### Example: Unpacking "Service"

The bare word "service" collapses at least these facets:

| Facet | What it means | Qualified name |
|-------|--------------|----------------|
| Promise | What is offered/contracted | ServiceOffering |
| Provider | Who is accountable | ServiceProvider |
| Endpoint | What you can call/address | ServiceEndpoint |
| Delivery System | What performs the work | ServiceSystem |
| Commitment | The binding obligation (SLA) | ServiceCommitment |
| Delivery Work | A fulfillment episode | ServiceRun |

**The "can you X it?" tests:**
- "Can you call/restart it?" → it's an **endpoint**, not a promise
- "Can it guarantee/must it?" → it's a **commitment**, not an endpoint
- "How does it work?" → it's a **system** or **method**, not a promise
- "Is it down/slow?" → it's an **endpoint** or **work episode**, with evidence

### When to Unpack

Flag a term for polysemy unpacking when:
- The same word appears as subject of incompatible verbs ("the X is deployed" AND "the X promises")
- Different team members mean different things by the same word
- Code uses the term in structurally different ways across modules
- You can't answer "what type is this?" with a single answer

## Bounded Contexts and Polysemy

The same word can mean different things in different bounded contexts. This is correct
DDD — don't fight it, document it.

> "Cross-context sameness is never inferred from spelling; cross-context alignment is
> represented only via explicit Bridges." — FPF A.1.1

### When the Same Word Means Different Things

Example: "Account" across three contexts:
- **Payment Context**: Financial account with a balance
- **Customer Context**: User login credentials and profile
- **Accounting Context**: Ledger entry in chart of accounts

**Rules:**
- Each context owns its own definition in the thesaurus
- Organize the thesaurus by bounded context, not alphabetically
- If code has `if` statements checking "which context am I in?" — the boundary is wrong
- Use Anti-Corruption Layers at context boundaries for term translation
- **Never assume sameness from spelling** — "Account" in Payment and "Account" in Customer are different concepts that happen to share a label

### Recognizing Context Boundaries

You've found a boundary when:
- Domain experts disagree on what a term means
- Translation logic between modules keeps growing
- The same class name appears with different structures in different packages
- Teams use different words for the same concept (this is a signal, not a problem)

### Cross-Context Bridges

When terms appear in multiple contexts, document the **bridge** explicitly in the
Cross-Context Bridges table of the thesaurus. Every bridge must state:

- **Which contexts** the term appears in
- **The relationship**: overlap (shared subset), distinct (different concepts), narrower/broader
- **Loss notes**: what breaks if you treat them as the same — this is the most important field
- **Direction**: can you safely substitute A for B? B for A? Neither?

```markdown
## Cross-Context Bridges

| Term | Context A meaning | Context B meaning | Relationship | Loss notes |
|------|-------------------|-------------------|-------------|------------|
| Account | Financial balance (Payment) | Login identity (Customer) | Distinct | Service accounts have no Customer; leads have no Account |
| Order | Customer purchase (Sales) | Kitchen ticket (Fulfillment) | Narrower | Kitchen Order adds prep steps, timing; loses pricing |
```

### Documenting Cross-Context Terms

```markdown
### Account (Payment Context)
- **Definition**: Financial account with balance, used for charging and refunds
- **NOT**: User identity or login credentials (that's Account in Customer Context)
- **Synonyms to AVOID**: Wallet, Purse, Balance

### Account (Customer Context)
- **Definition**: User's login identity — email, password, profile
- **NOT**: Financial balance (that's Account in Payment Context)
- **Synonyms to AVOID**: User, Profile, Login
```

## Term Relationships

Use these relationship types to connect terms (based on ISO 25964 / SKOS):

| Relationship | Meaning | Example |
|-------------|---------|---------|
| **Broader** | More general concept | Repository is broader than GitHubRepository |
| **Narrower** | More specific concept | GitHubRepository is narrower than Repository |
| **Part-of** | Composition | Commit is part-of Repository |
| **Related** | Associated, not hierarchical | Repository is related to Branch |
| **Synonym** | Same concept, different word (pick one, avoid the other) | Codebase = Repository (avoid Codebase) |

In thesaurus entries:
```markdown
### Repository
- **Definition**: A version-controlled code storage location
- **Broader**: VersionControlSystem
- **Narrower**: GitHubRepository, GitLabRepository, Monorepo
- **Part-of**: —
- **Has parts**: Branch, Commit, File
- **Related**: CodeSource, IndexedAnalysis
```

## Consistency Audit

For a full naming audit protocol (8 checks, severity levels, report format), see
[naming-audit.md](naming-audit.md).

## Brownfield Language Adoption

When introducing ubiquitous language to a project that already has an established
(but imprecise) vocabulary:

1. **Don't try to change how people talk overnight.** Language habits are ingrained.
   Correcting colleagues mid-conversation creates friction, not alignment.
2. **Control what you can first:** new code uses thesaurus terms, docs get updated,
   new API endpoints use canonical names, tests use domain language.
3. **Let conversational language follow.** As people read correct terms in code and
   PRs, spoken language shifts gradually. This takes weeks, not days.
4. **Watch for technical terms masquerading as domain language.** Stakeholders using
   DB table names as domain terms ("the users table" instead of "Customer") is a
   common brownfield pattern. Map these in `## Legacy Terms`.
5. **Pick battles by frequency.** Fix terms used 200 times across the codebase before
   terms used in 3 files.

## Legacy Code Migration

When migrating from inconsistent legacy naming:

### Phase 1: Anti-Corruption Layer
Keep legacy code as-is. Create adapter layer with correct naming:
```
Legacy: class UserManager → New: class Customer (domain) + LegacyUserAdapter (boundary)
```

### Phase 2: Gradual Rename
- New code always uses thesaurus terms
- Old classes get "Legacy" prefix only at migration boundaries
- Use interfaces to decouple: `IOrderRepository` stays stable while implementation changes
- Wire command handlers to new implementation first

### Phase 3: Cleanup
- Delete legacy classes once all consumers migrated
- Remove "Legacy" prefixes
- Final audit against thesaurus

**Rules:**
- Never rename across all layers at once
- Use interfaces to decouple
- Config flags to toggle old vs new implementation during migration
