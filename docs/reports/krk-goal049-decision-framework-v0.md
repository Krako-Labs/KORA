# KRK Goal 049 Decision Framework v0

Status: decision framework for the next KRK evidence goal.

## Decision Point

Should Goal 049 proceed to the KRK July 1 RC Decision Package, or should it run a bounded H100 routed subset evaluation first?

## Path A: Current Evidence Sufficient

Decision:

```text
Current evidence sufficient
-> Goal 049
KRK July 1 RC Decision Package
```

Use Path A if the July 1 RC is narrowed to:

- deterministic-heavy evidence.
- four-profile dry-run route-selectivity evidence.
- explicit H100 measurement gap disclosure.
- public-safe methodology for future bounded GPU-routed subset measurement.

Pros:

- avoids running new GPU jobs before the claim boundary is settled.
- keeps July 1 package public-safe and evidence-bounded.
- uses evidence that is already generated and reproducible.
- reduces risk of leaking raw artifacts or private environment details.

Cons:

- no measured H100 execution table is included.
- reviewers may ask for a measured GPU-class subset later.
- performance story remains methodology-first.

Risk:

- low public/private risk.
- medium evidence-perception risk if readers expect measured GPU-class execution.

Claim impact:

- supports dry-run route-selectivity and deterministic-heavy evidence.
- does not support live GPU-class performance claims.

## Path B: Additional H100 Evidence Required

Decision:

```text
Additional H100 evidence required
-> Goal 049
Bounded H100 Routed Subset Evaluation
```

Use Path B if the July 1 RC must include measured GPU-class execution evidence.

Pros:

- creates a measured H100 subset package.
- strengthens performance evidence if sanitized correctly.
- can connect route-selectivity to bounded execution measurement.

Cons:

- requires running new GPU work.
- increases artifact handling and sanitization burden.
- adds schedule and boundary risk.
- requires careful claim wording.

Risk:

- medium-to-high public/private risk if raw artifacts are mishandled.
- medium schedule risk.
- high claim-boundary risk if results are overinterpreted.

Claim impact:

- can support only subset-bounded measured evidence after the measurement package exists.
- still cannot support production, savings, broad superiority, provider superiority, or H100 superiority claims.

## Recommendation

Choose Path A for the next goal.

The current package is sufficient for a narrowed KRK July 1 RC decision package. Choose Path B only if the owner requires measured H100 subset evidence before the RC decision.
