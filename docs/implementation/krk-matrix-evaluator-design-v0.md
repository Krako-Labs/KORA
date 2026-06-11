# KRK Matrix Evaluator Design v0

## Purpose

This document designs a no-GPU, no-provider dry-run evaluator for the existing KRK matrix workloads.

The evaluator answers:

> Did the selected route match the independent oracle labels for this matrix item?

## Workload Files

The evaluator should load:

- `examples/workloads/krk-mixed-routing-matrix-alpha.json`
- `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-adversarial-routing-matrix-alpha.json`

## Top-Level Flow

1. Parse workload file.
2. Validate schema version and required fields.
3. For each item, construct router input from `router_visible_metadata` only.
4. Run the selected route policy.
5. Compare selected route against `oracle_labels`.
6. Accumulate metrics.
7. Emit metrics JSON.
8. Emit Markdown summary.

## Data Boundary

Router-visible input:

- `request_id`.
- `workload_profile`.
- `workload_class`.
- `router_visible_metadata`.

Evaluation-only input:

- `oracle_labels.expected_route`.
- `oracle_labels.acceptable_routes`.
- `oracle_labels.disallowed_routes`.
- `oracle_labels.oracle_reason`.

The route policy must not receive the full item object.

## Route Policy Interface

Proposed policy function:

```python
def select_route(route_request: RouteRequest) -> RouteDecision:
    ...
```

`RouteRequest` should contain only public-safe fields derived from router-visible metadata.

`RouteDecision` should include:

- `selected_route`.
- `policy_id`.
- `policy_version`.
- `decision_reason`.
- `fallback_classification`, optional.
- `error`, optional.

Allowed `selected_route` values:

- `deterministic`.
- `cache`.
- `CPU`.
- `provider`.
- `GPU`.
- `fallback`.

## Baseline Policies

### `all_gpu`

Routes every item to `GPU`.

Purpose:

- expose GPU false positives.
- establish a maximal GPU-demand baseline.

### `static_heuristic`

Routes by simple transparent rules over visible metadata.

Example rule order:

1. restricted privacy or malformed metadata -> `fallback`.
2. cache key available with low or medium complexity -> `cache`.
3. low complexity and local preference -> `deterministic`.
4. high complexity with large batch and permitted local/sanitized policy -> `GPU`.
5. provider allowed and medium complexity -> `provider`.
6. otherwise -> `CPU`.

### `provider_first_with_gpu_fallback`

Routes provider-allowed requests to provider, then high-complexity local/sanitized requests to GPU, then uses fallback for restricted or malformed cases.

Purpose:

- compare KRK against a provider-oriented policy.

### `KRK`

Routes through the KRK policy under test.

If the current KRK policy is not callable as a stable API, Goal 045 should create a small adapter boundary and label the first version explicitly.

## Metrics JSON Output

Proposed output shape:

```json
{
  "schema_version": "krk_route_metrics_v0",
  "profile_id": "mixed-realistic",
  "policy_id": "KRK",
  "policy_version": "krk_policy_v0",
  "metrics": {},
  "route_counts": {},
  "fallback_counts": {},
  "items": [],
  "claim_level": "dry_run_route_selectivity",
  "reproducibility": {}
}
```

Per-item output should include:

- `request_id`.
- `selected_route`.
- `expected_route`.
- `acceptable`.
- `unsafe_misroute`.
- `fallback_classification`.
- `error`.

Do not include private environment details.

## Markdown Summary Output

The Markdown summary should include:

- profile ID.
- policy ID.
- total requests.
- route distribution table.
- correctness metrics table.
- fallback metrics table.
- compute-weighted GPU demand if implemented.
- claim boundary.
- missing or staged metrics.

## Error Handling

The evaluator should:

- fail clearly on invalid JSON.
- fail clearly on missing required fields.
- count route policy exceptions as item-level errors when safe.
- include `error_count` and `error_percentage`.
- avoid partial silent success.

## Determinism

Dry-run metrics should be deterministic:

- stable file order.
- stable item order.
- stable JSON key ordering if emitted by script.
- no network calls.
- no current machine identifiers.
- no wall-clock dependency unless timestamp is explicitly optional and public-safe.

## Goal 045 Acceptance Criteria

The evaluator is acceptable when:

- all four fixtures parse.
- at least one policy can be evaluated end to end.
- oracle labels are not visible to the policy.
- metrics JSON is generated.
- Markdown summary is generated.
- tests cover positive and negative fixture cases.
- no GPU or provider access is required.
