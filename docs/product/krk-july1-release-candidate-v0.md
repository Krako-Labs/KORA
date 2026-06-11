# KRK July 1 Release Candidate Checklist v0

## Purpose

This checklist defines what KRK should contain before a July 1 release-candidate review.

KRK is the KORA Routing Kernel: the deterministic-first routing kernel inside KORA Core.

## Required Docs

- KRK quickstart.
- KRK architecture.
- KRK capability matrix.
- KRK routing benchmark methodology.
- KRK public evidence boundary.
- KRK performance table schema.
- KORA Core expansion plan.
- KORA Workload Spec.
- KORA Target Registry.
- KORA Evidence Report Schema.

## Required Examples

- deterministic hello-world path.
- direct vs KORA controlled path.
- runtime-integrated benchmark path.
- mixed KRK routing matrix fixture.
- GPU-heavy routing matrix fixture.
- cache-heavy routing matrix fixture.
- adversarial routing matrix fixture.

## Required Benchmark Matrix

Profiles:

- mixed-realistic.
- GPU-heavy.
- cache-heavy.
- adversarial.
- service-replay placeholder.

Policies:

- `all_gpu`.
- `static_heuristic`.
- `provider_first_with_gpu_fallback`.
- `KRK`.

## Required Performance Table

The release-candidate package should include:

- route distribution.
- exact route accuracy.
- acceptable route rate.
- unsafe misroute rate.
- GPU false positive and false negative counts.
- cache-hit correctness.
- fallback metrics.
- compute-weighted GPU demand.
- bounded GPU subset measurement table if measurement has been run.

## Required Tests

- full test suite.
- JSON validation for matrix fixtures.
- documentation whitespace check.
- public/private scan.
- claim boundary scan.
- no-secret scan.

## Required Public-Safe Evidence

Evidence must be reproducible and bounded:

- deterministic-heavy benchmark evidence.
- KRK matrix dry-run evidence when implemented.
- bounded GPU-routed subset evidence only after an approved measurement run.

## Claim Boundary

Allowed:

- KRK is a deterministic-first routing kernel.
- KRK can be evaluated with public-safe benchmark methodology.
- KRK prepares GPU-routed subset measurement.

Not allowed:

- production cost reduction.
- 10x savings.
- customer savings.
- infrastructure savings.
- broad workload superiority.
- H100 superiority.
- replacement of vLLM, OpenRouter, LiteLLM, OpenAI, Claude, Gemini, or other systems.

## Release Blocker List

Block release-candidate status if:

- top-level KRK command behavior is documented inaccurately.
- route/explain/benchmark/report are described as implemented when they are roadmap.
- benchmark output overclaims production or savings results.
- private infrastructure details appear in public docs.
- matrix fixtures fail JSON validation.
- full tests fail without documented unrelated cause.
- evidence reports contain raw private artifacts.

## Readiness Checklist

- [ ] CLI command surface documented exactly.
- [ ] Quickstart verified on a clean checkout.
- [ ] Matrix fixtures parse with `jq empty`.
- [ ] Dry-run evaluator exists or is clearly deferred.
- [ ] Performance table package exists.
- [ ] Public evidence boundary reviewed.
- [ ] Claim boundary reviewed.
- [ ] No private resource details in public docs.
- [ ] Full test suite passes.

## Not Included

Not included in the July 1 KRK release candidate unless separately approved:

- full KORA Core inspect / compare / run / report implementation.
- GPU service operation.
- hosted gateway.
- customer benchmark claims.
- private raw artifacts.
- repo rename or release tag.

## Next After July 1

- KRK technical note.
- KRK dry-run matrix evaluator.
- bounded GPU-routed subset measurement package.
- KORA Core alpha expansion.
- developer preview examples.
