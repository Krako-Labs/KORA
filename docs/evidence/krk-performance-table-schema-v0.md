# KRK Performance Table Schema v0

## Purpose

KRK performance tables should make route selectivity reviewable without overstating benchmark results.

This schema is public-safe and designed for dry-run matrix evidence plus later bounded GPU-routed subset measurement.

## Route Distribution Table

| Field | Type | Description |
| --- | --- | --- |
| `profile_id` | string | Matrix profile name. |
| `policy_id` | string | Routing policy under test. |
| `route` | string | deterministic, cache, CPU, provider, GPU, or fallback. |
| `count` | integer | Number of items routed to this path. |
| `percent` | number | Percent of profile items routed to this path. |

## Correctness Metrics Table

| Field | Type | Description |
| --- | --- | --- |
| `profile_id` | string | Matrix profile name. |
| `policy_id` | string | Routing policy under test. |
| `exact_route_accuracy` | number | Selected route equals oracle expected route. |
| `acceptable_route_rate` | number | Selected route is acceptable. |
| `unsafe_misroute_rate` | number | Selected route is disallowed. |
| `gpu_false_positive_count` | integer | GPU selected when not acceptable. |
| `gpu_false_negative_count` | integer | GPU not selected when expected. |
| `cache_hit_correctness_rate` | number | Cache routes with valid cache condition. |

## Fallback Metrics Table

| Field | Type | Description |
| --- | --- | --- |
| `profile_id` | string | Matrix profile name. |
| `policy_id` | string | Routing policy under test. |
| `safety_fallback_count` | integer | Fallbacks caused by safety or policy constraints. |
| `failure_fallback_count` | integer | Fallbacks caused by target failure or unavailability. |
| `validation_fallback_count` | integer | Fallbacks caused by validation failure. |
| `unknown_fallback_count` | integer | Fallbacks without sufficient classification. |

## Compute-Weighted GPU Demand Table

| Field | Type | Description |
| --- | --- | --- |
| `profile_id` | string | Matrix profile name. |
| `policy_id` | string | Routing policy under test. |
| `formula_version` | string | Example: `cwgd_v0`. |
| `total_compute_weight` | number | Sum of item compute weights. |
| `gpu_routed_compute_weight` | number | Sum of compute weights routed to GPU. |
| `compute_weighted_gpu_demand` | number | GPU-routed weight divided by total weight. |

## Bounded GPU Measurement Table

| Field | Type | Description |
| --- | --- | --- |
| `measurement_id` | string | Stable measurement identifier. |
| `profile_id` | string | Matrix profile name. |
| `selected_subset_rule` | string | Rule used to select GPU-routed subset. |
| `items_measured` | integer | Count of measured subset items. |
| `latency_summary` | object | Sanitized latency summary when safe. |
| `throughput_summary` | object | Sanitized throughput summary when safe. |
| `artifact_boundary` | string | Public-safe, private-only, or local-only. |

This table is for bounded subset measurement only. It does not imply production performance.

## Public-Safe Claim Level

| Field | Type | Description |
| --- | --- | --- |
| `claim_level` | string | Example: `dry_run_route_selectivity`, `bounded_gpu_subset_measured`. |
| `approved_language` | string | Exact bounded language allowed for public summaries. |
| `prohibited_interpretations` | array | Claims this result does not support. |

## Reproducibility Metadata

| Field | Type | Description |
| --- | --- | --- |
| `repo_commit` | string | Public repo commit used for the run. |
| `profile_file` | string | Workload matrix file. |
| `policy_version` | string | Routing policy version. |
| `formula_version` | string | Compute-weight formula version. |
| `command` | string | Public-safe command or dry-run invocation. |
| `generated_at` | string | Timestamp if included. |

Reproducibility metadata must not include private paths, credentials, server details, raw logs, or private resource identifiers.
