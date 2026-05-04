---
name: ubiquitous-language
description: |
  Maintain a project thesaurus (domain glossary) following DDD ubiquitous language
  principles. Use PROACTIVELY when naming anything: variables, functions, classes,
  modules, database fields, API endpoints, events, files, or directories. Also use
  when the user asks to "create thesaurus", "update glossary", "add term", "rename
  to match domain", "check naming consistency", "what should I call this", "domain
  language", "ubiquitous language", or "naming conventions". Ensures all names in
  the codebase are consistent, descriptive, and aligned with the shared domain
  vocabulary. Not for general code style or linting — only for domain term
  consistency.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - AskUserQuestion
---

# Ubiquitous Language: Project Thesaurus Manager

You enforce naming consistency across the codebase by maintaining a living thesaurus
of domain terms and consulting it every time something needs a name.

**Three modes:**
- **Naming consultation** (frequent) — everything in this file
- **Thesaurus generation** (rare) — read [references/generating-thesaurus.md](references/generating-thesaurus.md)
- **Naming audit** (periodic) — read [references/naming-audit.md](references/naming-audit.md)

## Foundations

This skill combines two bodies of knowledge:

- **Domain-Driven Design (DDD)** by Eric Evans — ubiquitous language, bounded contexts, aggregate naming
- **[First Principles Framework (FPF)](https://github.com/ailev/FPF/blob/main/FPF-Spec.md)** — a transdisciplinary "operating system for thought" that provides formal tools for semantic precision: bounded contexts as declared semantic frames, polysemy unpacking, lexical firewalls, cross-context bridges with loss notes, term continuity relations, and anti-explosion naming control. References like "FPF F.5" or "FPF A.1.1" point to specific sections of the FPF specification.

## Core Principle

> "A project should use a single, shared vocabulary. Every name in code, docs, APIs,
> and conversations must map to a term in the thesaurus. If a concept isn't in the
> thesaurus — add it before naming anything."
>
> — Domain-Driven Design, Eric Evans

**The codebase is primary evidence, not automatic authority.** Use code to discover
which terms are currently in circulation. Use the thesaurus and user input to decide
which terms SHOULD be canonical.

- For **what exists today** — derive from code (classes, DB schemas, API routes, events)
- For **what should become the standard** — ask the user/domain expert
- If code contradicts the approved thesaurus — the thesaurus wins for new code
- If the user says "fix legacy naming" — the user's directive overrides the codebase;
  map existing code names to `## Legacy Terms` and use the user's terms as canonical

**Tacit knowledge**: For areas not yet implemented, the most important domain knowledge
exists only in experts' heads, not in any artifact.

## Thesaurus File

**Locating the thesaurus:**
1. If the user specified a path — use it
2. If `THESAURUS.md` already exists somewhere in the repo — use that location
3. Default: `docs/THESAURUS.md`

Single source of truth for domain vocabulary.

### Entry Format

```markdown
### [Term]
- **Definition**: What this concept means in the business domain
- **NOT**: What this term does NOT mean (prevents confusion with similar concepts)
- **Synonyms to AVOID**: Terms that mean the same thing but must NOT be used
- **Related terms**: Other thesaurus terms this concept connects to
```

### Minimal Viable Entry

```markdown
### [Term]
- **Definition**: [one sentence]
- **Synonyms to AVOID**: [list]
```

**Why no "Use in code" field**: The thesaurus defines concepts and canonical names,
not how they appear in code. Code casing follows project conventions automatically.

**The thesaurus captures concepts, not behavior.** It's strong at nouns (entity names,
roles, process names) but won't replace behavioral specs for business rules. Don't try
to turn the thesaurus into a specification — keep entries short. If a concept has a
critical invariant, note it briefly in the definition, not as a separate section.

**Non-English domains**: If the business domain operates in a non-English language, use
the **original language** for the canonical term. The thesaurus should reflect how domain
experts actually speak. Add an English translation only if the codebase uses English
identifiers: `Счёт-фактура (Invoice in code)`.

## When to Consult the Thesaurus

**ALWAYS** before naming:
- Classes, interfaces, types, enums, aggregates, entities, value objects
- Functions, methods, commands, queries, domain events
- Variables, constants, fields, parameters
- Database tables, columns, collections
- API endpoints, parameters, response fields
- Files, directories, modules, packages
- Feature flags, config keys, environment variables
- Commit messages or PR titles that reference domain concepts

## Workflow

### 1. Read the thesaurus BEFORE inventing any name

**This is the single most important step.** Before proposing ANY name for anything,
find and read the thesaurus (see "Locating the thesaurus" above). Most naming tasks
don't need a new term — the right name is already there.

Check:
- Does a term for this concept already exist? **Use it exactly. Don't invent a new one.**
- Is there a related term that should inform the naming?
- Are there synonyms marked as "AVOID"? Don't use them.
- Which bounded context does this belong to?

If the thesaurus has a term that fits — **stop here**. You're done. Use that term.

### 2. If the concept is new

**Before minting a new term, try four levers** (from FPF F.14 "Name less, express more"):

1. **Reuse** — does an existing term already cover this? Maybe the concept is a variant, not a new thing
2. **Compose** — can you combine existing terms? `OrderLineItem` reuses `Order` + `LineItem`
3. **Qualify** — is this the same concept in a different state/window? Don't create `NightOperator` — use `Operator` with a time qualifier
4. **Ask** — if still unclear: "I need to name [concept]. The thesaurus doesn't have a term for this. What does the domain call it?"
   **If the user doesn't have an answer either** — that's a white spot, not a dead end.
   Building a ubiquitous language is co-creation, not extraction. Add it to `## Unresolved`
   with a `[WHITE-SPOT]` tag. Don't force a name for an undefined concept.

Only after all four fail, mint a new term:
1. **Name what the invariants make true** (FPF F.5) — don't name aspirationally. If the code doesn't enforce "Premium", don't call it `PremiumCustomer`
2. **Use minimal generality** — choose the narrowest name whose rules you actually enforce. Don't upgrade `Task` to `Activity` to sound universal
3. **Keep it to 1-3 words** — no rhetorical adjectives ("robust", "optimal", "advanced")
4. **Add it to THESAURUS.md** with at least: definition + avoided synonyms
5. **Then** use the term in code

### 3. If you find an inconsistency

When existing code uses a term that contradicts the thesaurus:
- Flag it: "Found `fetchPurchases()` but thesaurus says the canonical term is `Order`, not `Purchase`"
- Suggest a rename if scope is small
- For large-scale renames, note as tech debt and ask user how to proceed

## Naming Rules by DDD Construct

### Aggregates & Aggregate Roots
Use the business domain term. Singular. No technical suffixes.

```
GOOD: Order, Invoice, UserAccount, ShoppingCart
BAD:  OrderAggregate, OrderRoot, OrderAggregateImpl, OrderEntity
```

### Entities
Singular noun from the domain. Something with identity.

```
GOOD: OrderLineItem, PaymentTransaction, Customer
BAD:  OrderLineItemEntity, OrderLineItemImpl, OrderLineItemObj
```

### Value Objects
Singular noun describing an immutable concept. Describes **what it is**, not what it does.

```
GOOD: Money, Email, PhoneNumber, Address, DateRange
BAD:  MoneyValue, EmailValidator, PriceInfo, AmountData
```

### Domain Events
**Past tense verb + noun.** Something that happened.

```
GOOD: OrderPlaced, PaymentCaptured, InvoiceSent, InventoryReserved
BAD:  OrderEvent, OnOrderPlaced, CreateOrder (that's a command)
```

### Commands
**Imperative verb + noun.** An action requested.

```
GOOD: CreateOrder, CancelInvoice, ProcessRefund, ReserveInventory
BAD:  OrderCreated (that's an event), NewOrder, OrderCommand
```

### Queries
Question or retrieval. Verb + object or descriptive name.

```
GOOD: GetOrderById, FindInvoicesByCustomer, ListPendingOrders
BAD:  RetrieveOrderData, OrderQuery, GetterForOrder
```

### Domain Services
Named after **business activities** the domain expert recognizes.

```
GOOD: InvoiceCalculator, OrderFulfillment, NotificationSender
BAD:  OrderManager, GenericService, HelperService
```

### Repositories
Repository suffix is acceptable — it's an infrastructure pattern.

```
GOOD: OrderRepository, InvoiceRepository, CustomerRepository
BAD:  OrderStorage, OrderPersistence, OrderFinder, OrderDao
```

### Methods on Aggregates

**Commands (change state):** Imperative verb, no "Get" prefix.
```
GOOD: order.Cancel(), order.AddLineItem(product, quantity), order.Recalculate()
BAD:  order.CancelOrderMethod(), order.GetCancelled(), order.DoCancelOrder()
```

**Queries (read-only):** Start with Get, Is, Has, Can, or a domain verb.
```
GOOD: order.GetTotal(), order.IsExpired(), order.CanBeShipped()
BAD:  order.FetchInfo(), order.CheckData()
```

## Naming Anti-Patterns to Detect and Flag

### Lexical Firewall: Forbidden Terms in Domain Layer

The domain layer must be protected from transient jargon, vague terms, and
implementation details. Maintain a **Forbidden Lexicon** in the thesaurus: terms that
MUST NOT appear in domain code and must always be replaced with a specific domain term.

### Weasel Words (never use in domain layer)

| Weasel Word | Problem | Fix |
|-------------|---------|-----|
| `Info` | Meaningless suffix | Remove it: `UserInfo` -> `User` |
| `Data` | Says nothing about the concept | Use domain term: `OrderData` -> `Order` |
| `Manager` | Vague, hides responsibility | Split by actual responsibility |
| `Handler` | Generic, unclear intent | Name after what it handles |
| `Service` | Overused catch-all | Use specific domain activity name |
| `Base` | Technical distraction | Remove, use composition |
| `Item` | Too generic | Use domain term: `Item` -> `OrderLineItem`, `Product` |
| `Util` / `Helper` | Indicates bad design | Move logic to domain objects |
| `Object` / `Obj` | Never appropriate | Remove suffix |
| `Record` / `Model` | Database concept leaking into domain | Use domain term |

### Technical Jargon in Domain Layer

Domain code must be free of implementation details:

```
BAD:  MongoOrder, SqlUserRepository, HttpOrderService, OrderDto, OrderEntity
GOOD: Order, OrderRepository (interface), PaymentGateway, Order (just Order)
```

Technical prefixes/suffixes belong ONLY in the infrastructure layer:
```
INFRASTRUCTURE LAYER (OK): MongoOrderRepository, RedisSessionCache, HttpPaymentClient
DOMAIN LAYER (NEVER):      MongoOrder, RedisSession, HttpPayment
```

**Framework caveat**: In frameworks that intentionally blend domain and persistence
(Active Record pattern, ORM-centric frameworks), the model IS the domain entity.
Keep the **domain noun clean** and let framework coupling live in inheritance,
annotations, or metadata — not in the class name. Flag technical jargon only when
it becomes part of the business-facing name or leaks outside its boundary.

### Synonym Drift

Same concept called different things in different parts of code:

```
PROBLEM: "Customer" in auth, "User" in API, "Account" in billing — all mean the same thing
FIX:     Pick ONE canonical term per bounded context. Add others to "Avoid" list.
```

### Abbreviation Boundary

Ban abbreviations in **durable, domain-bearing names**: types, exported functions,
modules, API fields, DB columns, events, config keys.

Allow **conventional short-lived local identifiers** when meaning is obvious in scope:
`i`, `j`, `ctx`, `req`, `res`, `err`, `tx`, `db`, `e` for events.

Allow **industry-standard acronyms** when they are the dominant term: `SKU`, `VAT`,
`URL`, `ID`, `OAuth`. Do NOT force unnatural expansions if experts use the acronym.

```
PROBLEM: usr, user, account, acct — competing abbreviations for the same durable concept
FIX:     Pick ONE canonical form for domain-bearing names. Short-lived locals are exempt.
```

### Generic Names Hiding Domain Concepts

```
BAD:  record, entity, item, data, info, config, settings
GOOD: Use the specific domain term. "Config" → "LoanProduct". "Settings" → "NotificationPreferences"
```

### Naming by Implementation Instead of Domain

```
BAD:  RedisCache, PostgresStore, KafkaProducer, ElasticSearchIndex
GOOD: SessionStore, OrderHistory, EventPublisher, ProductCatalog
```

### Translation Chain ("Telephone Game")

When different artifacts use different terms for the same concept across the
knowledge chain, information is lost at each translation:

```
SMELL: Domain expert says "Campaign" → PM writes "Promotion" in spec →
       Dev codes `marketing_push` → QA tests "advertising effort"
FIX:   Same term everywhere: expert, PM, dev, QA all say and write "Campaign"
```

This is worse than synonym drift because each translation also loses nuance and
business rules. **How to detect:** compare terms in requirements/specs/tickets
against code names. If they don't match, the ubiquitous language has a translation
gap — adopt the domain expert's term everywhere.

## Casing Conventions

When the thesaurus provides a canonical term, apply it using the project's casing:

| Context | Convention | Example (term: "Order") |
|---------|-----------|------------------------|
| Class/Type | PascalCase | `Order`, `OrderService` |
| Function/Method | Project convention | `createOrder` / `create_order` |
| Variable | Project convention | `pendingOrder` / `pending_order` |
| Constant | UPPER_SNAKE | `MAX_ORDER_ITEMS` |
| Database table | Project convention | `orders`, `order_items` |
| API endpoint | kebab-case or convention | `/orders`, `/order-items` |
| Event/Message | PascalCase with past-tense verb | `OrderPlaced`, `OrderCancelled` |
| File/Directory | Project convention | `order.ts`, `order_service.py` |

**Key rules:**
- Use the EXACT canonical term — don't abbreviate (`ord`), don't expand (`orderObject`), don't synonym (`purchase`)
- Compound names combine thesaurus terms: `OrderItem`, not `PurchaseLineItem`
- Technical suffixes for infrastructure roles are fine: `OrderRepository`, `OrderDTO` (in infra layer only)
- Multi-word terms like "Processing Stage" become `ProcessingStage` / `processing_stage` — keep all words
- Variables and parameters use full descriptive names: `totalAmount` not `amt`, `customerEmail` not `cEmail`

## Updating the Thesaurus

When changing terms, use the **least strong** relation that tells the truth (from FPF F.13):

| Operation | When | Effect on thesaurus |
|-----------|------|---------------------|
| **Add** | New concept | Create entry. Minimum: definition + avoided synonyms |
| **Rename** | Wording improved, sense unchanged | Old name becomes legacy alias; grep codebase, suggest renames |
| **Split** | One term covered two senses | Old term deprecated; two new entries; disambiguation note |
| **Merge** | Two terms are really one sense | Pick canonical form; other becomes alias in "Avoid" list |
| **Retire** | Term was misleading, no single successor | Read-warning only ("avoid in new code; see X and Y") |
| **Deprecate** | Concept being phased out | Move to Legacy Terms with replacement pointer |

**Key test**: Can you point to the **same concept** before and after the change?
- Yes, same concept, better wording → **Rename** (keep as alias for reading old code)
- No, the concept actually changed → **Split** or **Merge** (not a rename)

**Alias parsimony**: keep at most 1 legacy alias per term — the one readers will most likely encounter in old code.

## Quick Checklist Before Naming Anything

1. Is this term in `THESAURUS.md`? If not — add it first
2. Would a domain expert recognize this name?
3. Does it contain a weasel word (Manager, Service, Handler, Info, Data, Item, Base, Util)?
4. Is it too generic (could mean multiple things in different contexts)?
5. Does it reveal infrastructure details (Mongo, Sql, Http, Dto, Entity, Model)?
6. Is it consistent with other uses of this term across the codebase?
7. Am I using the EXACT canonical form from the thesaurus, or a synonym?
8. Am I in the right bounded context for this term?
9. If this is a domain event, is it past tense? If a command, imperative?
10. Can I explain what this name represents in one sentence using domain language?

If any answer raises a concern — stop and fix before proceeding.
