# KRK Route Metrics Schema v0

## Purpose

This document defines the route-selectivity metrics schema for KRK matrix dry-run evaluation.

The schema is JSON-like and public-safe. It is intended for generated dry-run evidence, not production telemetry.

## Top-Level Fields

```json
{
  "schema_version": "krk_route_metrics_v0",
  "profile_id": "mixed-realistic",
  "policy_id": "KRK",
  "policy_version": "krk_policy_v0",
  "total_requests": 0,
  "route_counts": {},
  "metrics": {},
  "fallback_counts": {},
  "errors": [],
  "claim_level": "dry_run_route_selectivity",
  "reproducibility": {}
}
```

## Required Metric Fields

### `total_requests`

Total number of evaluated items.

Type:

- integer.

### `route_counts`

Count by selected route.

Example:

```json
{
  "deterministic": 1,
  "cache": 1,
  "CPU": 1,
  "provider": 1,
  "GPU": 1,
  "fallback": 1
}
```

### `exact_route_accuracy`

Fraction of items where selected route equals `oracle_labels.expected_route`.

Formula:

```text
exact_matches / total_requests
```

### `acceptable_route_rate`

Fraction of items where selected route appears in `oracle_labels.acceptable_routes`.

Formula:

```text
acceptable_matches / total_requests
```

### `unsafe_misroute_rate`

Fraction of items where selected route appears in `oracle_labels.disallowed_routes`.

Formula:

```text
unsafe_misroutes / total_requests
```

### `gpu_false_positive_count`

Count of items where selected route is `GPU` and `GPU` is not acceptable.

### `gpu_false_negative_count`

Count of items where expected route is `GPU` and selected route is not `GPU`.

### `cache_hit_correctness_rate`

Fraction of cache-selected items where:

- selected route is `cache`.
- cache key is visible as available.
- `cache` appears in acceptable routes.

If no items are routed to cache, represent this as `null`, not `0`, to avoid implying failed cache correctness.

### `safety_fallback_rate`

Fraction of items routed to fallback for safety, privacy, malformed input, or route-policy conflict reasons.

### `failure_fallback_rate`

Fraction of items routed to fallback because a preferred route failed or was unavailable.

In the first dry-run implementation, this may be `0` unless failure simulation exists.

### `fallback_counts`

Count by fallback class:

```json
{
  "safety_fallback": 0,
  "failure_fallback": 0,
  "validation_fallback": 0,
  "unknown_fallback": 0
}
```

### `error_count`

Count of item-level evaluation errors.

### `error_percentage`

Item-level errors divided by `total_requests`.

## Compute-Weighted GPU Demand

### `compute_weighted_gpu_demand`

Fraction of compute weight routed to GPU.

Formula version:

- `cwgd_v0`.

Formula:

```text
sum(compute_weight for items routed to GPU) /
sum(compute_weight for all items)
```

If compute weights are missing, report:

```json
{
  "compute_weighted_gpu_demand": null,
  "compute_weight_formula_version": "cwgd_v0",
  "compute_weight_status": "not_computed_missing_weights"
}
```

For Goal 045, compute-weighted GPU demand can be staged:

- Stage A: implement route counts and correctness metrics.
- Stage B: implement `cwgd_v0` using existing `compute_weight` fields.

Because current matrix fixtures already include `compute_weight`, Stage B is recommended if implementation remains small.

## Claim Level

Allowed `claim_level` values:

- `dry_run_route_selectivity`.
- `methodology_only`.
- `bounded_gpu_subset_measured`.

Goal 045 should use:

- `dry_run_route_selectivity` when metrics are generated from committed fixtures.
- `methodology_only` if implementation is incomplete.

Do not use `bounded_gpu_subset_measured` unless a future bounded measurement task actually runs and publishes sanitized subset results.

## Reproducibility Metadata

Recommended fields:

```json
{
  "repo_commit": "",
  "profile_file": "",
  "policy_id": "",
  "policy_version": "",
  "formula_version": "cwgd_v0",
  "command": ""
}
```

Do not include:

- local-only paths.
- private hostnames.
- user names.
- credentials.
- raw logs.
- private resource identifiers.

## Markdown Summary Sections

The generated Markdown summary should include:

- title.
- profile and policy.
- route distribution table.
- correctness metrics table.
- fallback metrics table.
- compute-weighted GPU demand table.
- errors table.
- claim boundary.
- reproducibility metadata.
