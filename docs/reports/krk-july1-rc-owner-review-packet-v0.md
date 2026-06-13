# KRK July 1 RC Owner Review Packet v0

Status: owner review packet refreshed after route-selectivity evidence generation.

## Executive Recommendation

Recommendation: proceed with a narrowed KRK July 1 RC.

The package is not ready to be framed as a broad KORA Core release, live infrastructure proof, or measured H100 execution package. It is ready to be framed as a bounded KRK alpha/release-candidate package focused on deterministic-first routing, deterministic-heavy evidence, dry-run route-selectivity metrics over four public matrix profiles, and explicit H100 measurement gap disclosure.

## Decision Options

### A. Proceed with KRK July 1 RC

Use only if the RC is explicitly scoped to KRK route-selectivity and deterministic-heavy evidence. This is acceptable if the public wording stays narrow.

### B. Proceed with narrowed KRK July 1 RC

Recommended.

Rationale:

- route-selectivity metrics now exist for four public dry-run matrix profiles.
- generated JSON and Markdown evidence outputs are committed.
- deterministic-heavy evidence remains available and bounded.
- H100 methodology and public evidence boundaries exist.
- public KRK H100 measured evidence is not included and is not required for a narrowed RC.
- remaining gaps are explicit rather than hidden.

### C. Delay KRK July 1 RC

Choose this if the desired RC must include live provider validation, bounded GPU-routed subset measurement, or broader workload representativeness. Those evidence layers are not complete in the current package.

## What Is Ready

- KRK product definition.
- KRK quickstart and architecture docs.
- deterministic-heavy benchmark evidence.
- four public KRK matrix fixtures.
- dry-run route-selectivity metrics for mixed-realistic, GPU-heavy, cache-heavy, and adversarial profiles.
- JSON and Markdown generated evidence outputs.
- public/private and claim-boundary docs.

## What Is Not Ready

- live provider validation.
- H100 bounded public evidence.
- runtime-integrated route-selectivity workflow.
- broad workload representativeness.
- final technical paper polish.
- contributor-facing preview issue set.

## Must Fix Before July 1

- Keep README and evidence docs aligned with the narrowed RC scope.
- Ensure all generated JSON files parse.
- Keep route-selectivity wording explicitly dry-run and fixture-scoped.
- Re-run full tests and boundary scans before any PR or public announcement.

## Should Fix Before July 1

- Add a one-command regeneration wrapper for matrix outputs.
- Add a contributor-friendly issue list for the next evidence gaps.
- Refresh the technical paper draft with the route-selectivity results.
- Decide whether H100 measured evidence is required before July 1 or can remain post-RC.

## Can Wait Until After July 1

- live provider validation.
- bounded GPU-routed subset measurement.
- broader service-replay profile.
- KORA Core inspect/compare/run/report implementation.

## Claim Boundary

The owner decision should not imply production readiness, savings, infrastructure reduction, provider superiority, GPU superiority, or broad workload superiority.
