# KRK Routing Benchmark Methodology v0

## Purpose

This methodology defines how to evaluate KRK route selection without turning benchmark design into unsupported infrastructure or savings claims.

The core question is:

> Did KRK select an acceptable execution path for the workload?

## Independent Oracle Labels

Each benchmark item should include independent oracle labels:

- expected route.
- acceptable routes.
- disallowed routes.
- oracle reason.

Oracle labels are used for evaluation only. They must not be passed to the router.

## Router-Visible Metadata Versus Oracle-Only Labels

Router-visible metadata may include:

- input size.
- batch size.
- request modality.
- cache key availability.
- latency sensitivity.
- privacy preference.
- estimated complexity.

Oracle-only labels include:

- expected route.
- acceptable routes.
- disallowed routes.
- oracle reason.

The benchmark harness should preserve this separation so KRK cannot overfit by reading answer labels.

## Baseline Policies

### `all_gpu`

Routes every item to GPU.

Purpose:

- establish a maximal GPU-demand baseline.
- expose GPU false positives.

### `static_heuristic`

Routes using a simple fixed rule set based on visible metadata.

Purpose:

- compare KRK against a transparent non-learning policy.

### `provider_first_with_gpu_fallback`

Routes to provider first and uses GPU as a fallback for selected high-complexity cases.

Purpose:

- compare KRK against a provider-oriented policy.

### `KRK`

Routes using the KORA Routing Kernel policy under test.

Purpose:

- evaluate deterministic-first, evidence-producing route selection.

## Metrics

### `exact_route_accuracy`

Fraction of items where selected route equals the oracle expected route.

### `acceptable_route_rate`

Fraction of items where selected route is in oracle acceptable routes.

### `unsafe_misroute_rate`

Fraction of items where selected route is in oracle disallowed routes.

### `gpu_false_positive_count`

Count of items routed to GPU when GPU is not acceptable.

### `gpu_false_negative_count`

Count of items not routed to GPU when GPU is the expected route.

### `cache_hit_correctness_rate`

Fraction of cache-routed items where cache was available and acceptable.

### `safety_fallback_rate`

Fraction of items routed to fallback because of privacy, safety, malformed input, or disallowed route conflicts.

### `failure_fallback_rate`

Fraction of items routed to fallback because a preferred route failed or was unavailable.

### `compute_weighted_gpu_demand`

Estimated GPU demand after applying per-item compute weights.

Formula version `cwgd_v0`:

```text
compute_weighted_gpu_demand =
  sum(compute_weight for items routed to GPU) /
  sum(compute_weight for all items)
```

Compute weight is a benchmark metadata value, not a measured production cost.

## Fallback Classification

Fallback should be classified as:

- `safety_fallback`: route avoided because requested execution would violate policy.
- `failure_fallback`: route used after an unavailable or failed target.
- `validation_fallback`: route used after output validation failed.
- `unknown_fallback`: route used without enough detail; should be minimized.

## Quality Validation Placeholder

Future methodology may include quality checks for provider or GPU outputs. Until that exists, quality validation should be labeled as a placeholder and not used for broad superiority claims.

## Provider Validation Placeholder

Future methodology may include provider-backed validation. Until explicit provider evidence exists, provider validation should be labeled as a placeholder and not used to claim real API cost reduction or production performance.

## Compute Weight Formula Versioning

Every benchmark report should record:

- formula name.
- formula version.
- compute weight source.
- route policy version.
- benchmark profile.

Formula changes must create a new version rather than silently changing historical comparisons.
