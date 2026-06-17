# KRK Route-Selectivity Metrics Implementation Plan v0

## Purpose

This plan defines how to implement KRK route-selectivity metrics for the committed KRK matrix fixtures.

This is an implementation plan, not an implementation. It does not add a runner, does not run GPU tests, does not call providers, and does not create release artifacts.

## Why Route-Selectivity Metrics Matter For July 1

KRK is the KORA Routing Kernel: a deterministic-first routing kernel inside KORA Core.

The July 1 evidence package needs to show more than deterministic-heavy avoided simulated model invocations. It needs a public-safe way to evaluate whether KRK chooses acceptable execution paths across:

- deterministic.
- cache.
- CPU.
- provider.
- GPU.
- fallback.

Route-selectivity metrics are the bridge between methodology and evidence. They convert the KRK matrix fixtures into measurable results without requiring GPU access or provider calls.

## Current Gap

Current public package:

- defines KRK route-selectivity methodology.
- includes four matrix fixtures.
- defines route metrics.
- marks route-selectivity fields as not measured yet.

Missing:

- a dry-run evaluator that consumes the fixtures.
- a route policy interface for matrix dry runs.
- metrics computation.
- JSON output.
- Markdown summary output.
- tests proving oracle labels are not passed into route selection.

## Inputs

Initial input files:

- `examples/workloads/krk-mixed-routing-matrix-alpha.json`
- `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-adversarial-routing-matrix-alpha.json`

Each item contains:

- `request_id`.
- `workload_profile`.
- `workload_class`.
- `router_visible_metadata`.
- `oracle_labels`.

The evaluator must treat `router_visible_metadata` as router input and `oracle_labels` as evaluation-only data.

## Outputs

Required output types:

- metrics JSON.
- Markdown summary.
- route distribution by profile and policy.
- correctness metrics.
- fallback metrics.
- compute-weighted GPU demand when available.
- reproducibility metadata.
- claim level.

Proposed output locations for generated examples, if committed later:

- `examples/reports/krk-route-selectivity-metrics-alpha.json`
- `examples/reports/krk-route-selectivity-summary-alpha.md`

Generated outputs should be committed only if public-safe and deterministic.

## Modules / Files Likely To Change

Goal 045 should inspect the current package layout and choose the smallest matching implementation. Likely candidates:

- `kora/` for reusable route metrics utilities.
- `examples/` for an example runner or dry-run entrypoint.
- `tests/` for evaluator, schema, and oracle isolation tests.
- `docs/evidence/krk-performance-table-v0.md` for measured metric updates after generation.
- `docs/evidence/krk-capability-matrix-v0.md` for status updates after implementation.

Avoid broad refactors. The first implementation should be boring, deterministic, and easy to test.

## Validation Plan

Minimum validation for Goal 045:

```bash
python3 -m pytest
git diff --check
jq empty examples/workloads/krk-mixed-routing-matrix-alpha.json
jq empty examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json
jq empty examples/workloads/krk-cache-heavy-routing-matrix-alpha.json
jq empty examples/workloads/krk-adversarial-routing-matrix-alpha.json
```

New tests should cover:

- fixture loading.
- required field validation.
- oracle labels are excluded from router input.
- exact route accuracy.
- acceptable route rate.
- unsafe misroute rate.
- GPU false positive and false negative counts.
- cache-hit correctness.
- fallback classification.
- compute-weighted GPU demand if implemented.
- JSON output shape.
- Markdown summary output.

## Public/Private Boundary

The route-selectivity evaluator must be public-safe:

- no GPU required.
- no provider call required.
- no credentials required.
- no raw private artifacts.
- no local-only paths in generated outputs.
- no server, user, IP, SSH, or private resource details.

## Claim Boundary

Allowed after implementation, if tests pass:

- KRK route-selectivity metrics are computed for committed dry-run fixtures.
- Metrics evaluate selected routes against independent oracle labels.
- The evaluator requires no GPU or provider calls.

Not allowed:

- production cost reduction.
- real API cost reduction.
- customer savings.
- infrastructure savings.
- broad workload superiority.
- H100 superiority.
- production readiness.

## Implementation Phases

### Phase 1: Fixture Loader

- Load the four matrix files.
- Validate top-level `schema_version`, `profile_id`, and `items`.
- Validate each item has `request_id`, `router_visible_metadata`, and `oracle_labels`.

### Phase 2: Router Input Boundary

- Build a route request object from `router_visible_metadata` only.
- Prohibit passing `oracle_labels` to the route policy.
- Add tests that fail if oracle fields are visible to the router.

### Phase 3: Baseline Policies

Implement simple dry-run policies:

- `all_gpu`.
- `static_heuristic`.
- `provider_first_with_gpu_fallback`.
- `KRK` policy adapter or initial deterministic policy under test.

If the real KRK policy is not directly callable yet, implement the evaluator so the policy adapter can be swapped later, and clearly label the first policy version.

### Phase 4: Metrics Computation

Compute:

- route counts.
- exact route accuracy.
- acceptable route rate.
- unsafe misroute rate.
- GPU false positive count.
- GPU false negative count.
- cache-hit correctness rate.
- fallback rates.
- error count and error percentage.
- compute-weighted GPU demand if supported by input weights.

### Phase 5: Output Generation

- Emit stable JSON.
- Emit Markdown summary.
- Include reproducibility metadata.
- Include claim boundary.

### Phase 6: Evidence Docs Update

After the runner exists and metrics are generated:

- update the KRK performance table.
- update the capability matrix.
- keep missing values marked as missing if not implemented.
