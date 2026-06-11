# KRK Paper Next Experiments v0

Status: future experiment plan for KRK paper evidence. This file defines next work; it does not report completed results.

## Purpose

The next paper iteration needs measured route-selectivity evidence beyond the current deterministic-heavy benchmark. These experiments should preserve oracle-label independence, public-safe artifacts, and bounded claim language.

## 1. 100K Routed Workload Dry-Run

Goal:

- stress the routing/reporting pipeline at larger scale without requiring provider or GPU execution.

Measurements:

- route distribution.
- report generation time.
- artifact size.
- validation failures.
- fallback classification coverage.

Boundary:

- dry-run only unless separately approved and implemented.
- no production behavior claim.

## 2. Multi-Profile Matrix

Profiles:

- mixed-realistic.
- GPU-heavy.
- cache-heavy.
- adversarial.
- service-replay placeholder.

Measurements:

- exact route accuracy.
- acceptable route rate.
- unsafe misroute rate.
- cache correctness.
- fallback rates.
- GPU false positive and false negative counts.

Boundary:

- service-replay profile must use sanitized public-safe inputs only.
- no raw service logs or private records.

## 3. Oracle-Label Independence

Goal:

- verify that oracle labels are used only for evaluation and never passed into router-visible input.

Checks:

- schema separation.
- test fixtures that fail if oracle fields enter router input.
- report fields that record evaluation labels separately from routing metadata.

Boundary:

- this is benchmark integrity work, not route-quality evidence by itself.

## 4. Compute-Weighted GPU Demand

Goal:

- report how much compute-weighted workload mass KRK routes to GPU-class execution under a versioned formula.

Measurements:

- total compute weight.
- GPU-routed compute weight.
- compute-weighted GPU demand.
- formula version.

Boundary:

- compute weight is benchmark metadata, not measured production cost.

## 5. Bounded GPU-Routed Subset Measurement

Goal:

- measure only the subset KRK routes to GPU-class execution after dry-run route validation.

Measurements:

- subset count.
- sanitized runtime summary when safe.
- sanitized throughput summary when safe.
- memory summary when safe.
- artifact boundary.

Boundary:

- do not publish raw logs, private resource identifiers, credentials, local paths, or server details.
- do not claim H100 superiority or broad infrastructure reduction.

## 6. Provider-Routed Sample Validation

Goal:

- validate a small sample where KRK routes selected items to provider execution under explicit configuration.

Measurements:

- selected route.
- provider route reason.
- fallback behavior.
- validation status.
- evidence report completeness.

Boundary:

- no provider replacement claim.
- no billing or savings claim unless a separate reviewed cost methodology exists.

## 7. Adversarial Fallback Evaluation

Goal:

- test fallback behavior on malformed, ambiguous, privacy-sensitive, unsafe, or conflicting workload metadata.

Measurements:

- safety fallback count.
- validation fallback count.
- failure fallback count.
- unsafe misroute rate.
- explanation completeness.

Boundary:

- adversarial examples should be synthetic and public-safe.

## 8. Service-Replay Profile

Goal:

- create a replay-shaped profile that resembles service workload structure without exposing private data.

Measurements:

- route distribution.
- fallback classification.
- report reproducibility.
- claim boundary coverage.

Boundary:

- use sanitized fixtures only.
- do not include raw logs, personal data, private records, server identifiers, or internal operational details.

## Experiment Readiness Gate

Before using any result in the paper:

- workload fixture is committed or reproducible.
- command is documented.
- output schema is documented.
- claim boundary is reviewed.
- `python3 -m pytest` passes.
- public/private scan passes.
- generated raw artifacts are either excluded or intentionally frozen by a reviewed artifact policy.
