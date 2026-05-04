# Naming & Ubiquitous Language Audit

Read this when the user asks to audit, review, or check naming consistency in the codebase.
This is a systematic protocol — run it top to bottom, report findings at the end.

## When to Run

- User asks: "audit naming", "check naming consistency", "review ubiquitous language"
- Before a major refactoring or architecture change
- When onboarding to a new codebase
- Periodically (quarterly) to catch drift

## Prerequisites

- `THESAURUS.md` must exist. If it doesn't, run thesaurus generation first
  (see [generating-thesaurus.md](generating-thesaurus.md))
- Read `THESAURUS.md` before starting

## Audit Protocol

Run all 8 checks. Collect findings without stopping. Present the full report at the end.

### Check 1: Synonym Violations

For each term in the thesaurus, grep the codebase for its "Synonyms to AVOID":

```
For "Order" with AVOID: [Purchase, Transaction, Buy]
→ grep -rn "purchase\|transaction\|buy" src/ --include="*.{ts,cs,py,java,go,rb}"
→ filter: only class names, method names, variable names, DB columns (not comments/strings)
```

**Severity: HIGH** — direct contradiction of the thesaurus.

### Check 2: Weasel Words in Domain Layer

Scan domain-layer code for forbidden terms from the Forbidden Lexicon:

```
Scan for: Manager, Handler, Service (bare), Info, Data, Base, Util, Helper, Object, Obj, Record, Model
In: domain layer classes, interfaces, method names (NOT infrastructure layer)
```

**Severity: MEDIUM** — vague naming that hides domain concepts.

### Check 3: Technical Jargon Leak

Scan domain-layer code for implementation-specific prefixes/suffixes:

```
Scan for: Mongo*, Sql*, Http*, Redis*, Kafka*, Elastic*, *Dto, *Entity, *Model, *Record
In: domain layer only (NOT infrastructure/persistence/API layers)
```

**Severity: HIGH** — infrastructure leaking into domain.

### Check 4: Synonym Drift (same concept, multiple names)

Look for groups of identifiers that likely refer to the same domain concept:

- Same-shaped classes in different modules (similar fields, different names)
- API endpoints that use different terms for the same resource
- Database tables/columns with overlapping semantics
- Tests that use different names than the code they test

**Detection heuristics (grep-friendly, no pairwise comparison):**
- Same role suffix with different noun stems: `UserController` vs `CustomerController`,
  `UserRepository` vs `CustomerRepository` — grep for common suffixes, compare stems
- API route vs domain code drift: `/users/...` in routes but `Customer` in domain
- DB column vs code drift: `user_id` in schema but `customerId` in code
- Test vs implementation drift: test descriptions say "user" but code says `Customer`
- Competing stems in the same module: file that imports both `User` and `Customer`

Treat synonym drift as a **local-cluster problem**: same module, same role, different noun.
Do NOT attempt global pairwise class comparison.

**Severity: HIGH** — the ubiquitous language is fractured.

### Check 5: Polysemy (same name, different meanings)

Look for the same identifier used with structurally different meanings:

- Same class name in different packages with different fields/methods
- Same enum name with different values in different modules
- Same method name doing fundamentally different things in different classes
- Same API parameter meaning different things in different endpoints

**The incompatible-verbs test:** If the same word appears as subject of incompatible
verbs in different parts of the code ("Account is charged" vs "Account is logged in"),
it's polysemy.

**Severity: HIGH** — silent bugs waiting to happen.

### Check 6: Translation Chain

Compare terminology across artifact layers:

```
Layer mapping (local artifacts only — do NOT assume access to Jira/Linear/Notion):
  Local docs/ADRs/OpenAPI specs → API controllers → Domain code → DB schema → Test descriptions → Git commit messages

For each major domain concept, trace the name through available local layers.
If external specs are needed, ask the user to paste the relevant text.
```

**Detection method:**
- Pick 3-10 major domain terms from the thesaurus or API surface
- Grep their stems across available local layers
- Check test descriptions (`describe()`/`it()`/`test()` strings) — tests often use
  the domain expert's term while code uses an abbreviation
- Check `git log --oneline -50` — commit messages reveal human intent vs code naming
- Flag any layer where the term changes

**Example finding:**
```
"Campaign" in docs/architecture.md
→ "Promotion" in openapi.yaml
→ `marketing_push` in domain code
→ `promotions` table in DB
→ "advertising effort" in test descriptions
= Translation chain with 4 breaks
```

If some layers are missing locally, report them as `not auditable from local files`.

**Severity: HIGH** — information loss at every translation.

### Check 7: Abbreviation & Naming Inconsistency

Scan for inconsistent forms of the same term:

- Abbreviated vs full: `usr` / `user` / `customer` / `acct` / `account`
- Casing inconsistency: `orderId` in one file, `order_id` in another (within same language)
- Plural inconsistency: `Order` class but `order_items` table vs `orderItem` field

**Severity: LOW** — cosmetic but creates cognitive load.

### Check 8: Orphan Terms

Check for terms in the thesaurus that no longer appear in code:

```
For each thesaurus term → grep codebase
If zero matches → term may be obsolete
```

Also check reverse: domain-relevant class names NOT in the thesaurus.

**Severity: LOW** — thesaurus drift from codebase.

## Report Format

After running all 8 checks, present findings grouped by severity:

```
## Ubiquitous Language Audit Report

**Codebase**: [project name]
**Date**: [date]
**Thesaurus**: [N terms, M legacy, K unresolved]

### Critical (fix now)

1. **Synonym violation**: `fetchPurchases()` in src/api/orders.ts:12
   — Thesaurus says "Order", not "Purchase" — 8 files affected

2. **Polysemy**: `Account` used as financial entity (billing/)
   AND user identity (auth/) — 18 files affected

3. **Translation chain**: "Campaign" → "Promotion" → `marketing_push`
   — 4 translation breaks across 31 files

### Warning (plan to fix)

4. **Weasel word**: `OrderManager` in src/domain/OrderManager.ts
   — "Manager" hides responsibility. What does it actually do?

5. **Technical leak**: `MongoOrder` in src/domain/MongoOrder.ts
   — Infrastructure prefix in domain layer

### Info (track as debt)

6. **Abbreviation**: `usr` in 3 files, `user` in 12, `customer` in 8
   — All refer to the same concept

7. **Orphan term**: "ShippingLabel" in thesaurus, 0 matches in code
   — May be obsolete or not yet implemented

### Stats

| Check | Findings |
|-------|----------|
| Synonym violations | 3 |
| Weasel words | 5 |
| Technical leaks | 2 |
| Synonym drift | 4 clusters |
| Polysemy | 1 |
| Translation chains | 2 |
| Abbreviation issues | 6 |
| Orphan terms | 3 |
| **Total** | **26** |

### Recommended Priority

1. Fix polysemy first (silent bug risk)
2. Fix translation chains (information loss)
3. Fix synonym violations (thesaurus credibility)
4. Clean up weasel words (naming quality)
5. Track the rest as naming debt
```

## After the Audit

- **Critical findings**: suggest immediate fixes or add to `## Unresolved` in thesaurus
- **Warnings**: create tech debt tickets or note in thesaurus
- **Info**: note for next audit cycle
- **Update the thesaurus**: add missing terms, remove orphans, update "Synonyms to AVOID"
  lists based on what you found in the wild
- **If no thesaurus existed**: the audit findings ARE the input for thesaurus generation —
  feed them into the generating-thesaurus.md workflow
