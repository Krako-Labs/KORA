# Goal 103 Representativeness Route-Only Evaluator

Status: route-only evaluator added for the Goal 102 representativeness seed; no provider calls, H100 execution, model inference, or output-quality proof added.

## Objective

Goal 103 adds a narrow evaluator for the public-safe synthetic representativeness seed fixture introduced in Goal 102.

The evaluator reads the fixture, reuses the shape-only validator, and reports aggregate route/counter evidence only. It does not inspect or publish raw benchmark outputs beyond the already public fixture content.

## Input Fixture

- [KORA representativeness seed fixture v0](../../examples/workloads/kora-representativeness-seed-v0.json)
- schema: `kora_representativeness_seed_v0`
- claim scope: `fixture_only`
- public safe: `true`

## Evaluator Command

```bash
python3 scripts/evaluate_representativeness_seed_routes.py
```

The evaluator emits deterministic JSON to stdout. It does not create raw benchmark artifacts.

## Aggregate Counters Produced

Total seed items: `40`

Route counts:

| Route | Count |
| --- | ---: |
| `cache` | 6 |
| `cpu` | 5 |
| `deterministic` | 7 |
| `fallback` | 5 |
| `gpu` | 3 |
| `provider_needed` | 8 |
| `retrieval_needed` | 1 |
| `tool_needed` | 5 |

Route group counts:

| Group | Count |
| --- | ---: |
| `cache_reuse_candidates` | 6 |
| `deterministic_local_route_candidates` | 18 |
| `fallback_control_candidates` | 5 |
| `provider_model_candidates` | 11 |

Unsupported, unknown, or missing route metadata count: `0`

Workload category counts:

| Category | Count |
| --- | ---: |
| `agent_workflow_steps` | 3 |
| `cache_reuse_repeated_work` | 2 |
| `document_intake` | 3 |
| `gpu_candidate_batch` | 3 |
| `incident_alert_routing` | 3 |
| `issue_triage` | 3 |
| `mixed_operational_workflow` | 3 |
| `output_quality_methodology_seed` | 2 |
| `policy_safety_fallback` | 2 |
| `provider_needed_ambiguous_tasks` | 2 |
| `rag_query_routing` | 3 |
| `report_generation_control` | 3 |
| `support_ticket_classification` | 3 |
| `tool_needed_local_actions` | 2 |
| `validation_schema_check` | 3 |

## Validation Performed

The evaluator calls [the Goal 102 shape-only validator](../../scripts/validate_representativeness_seed.py) before computing route counters.

Validation covers:

- supported schema version.
- fixture-level `public_safe: true`.
- fixture-level `claim_scope: fixture_only`.
- item count range.
- required item fields.
- duplicate ids.
- allowed route-label vocabulary.
- item-level `public_safe: true`.
- item-level `claim_scope: fixture_only`.

## Relationship To Goal 102

Goal 102 added the seed fixture and shape-only validation. Goal 103 is the next narrow step: it turns that same fixture into aggregate route/counter evidence for planning and reviewer inspection.

This remains shape-validated seed analysis. It is not a benchmark, not an output-quality evaluator, and not production workload evidence.

## Explicit Non-Claims

Goal 103 does not:

- call OpenAI, Anthropic, Gemini, local model servers, or any external inference provider.
- execute H100, GPU, CUDA, server, or remote workloads.
- run model inference.
- evaluate output quality.
- prove broader workload representativeness.
- prove production readiness.
- prove production workload handling.
- prove production benchmark results.
- prove production cost reduction, real API-cost reduction, or real GPU-cost reduction.
- prove H100, GPU, CPU, or multi-GPU superiority.
- prove customer savings.
- replace providers, model serving, or GPU serving.
- publish `getkora`.

## Recommended Next Goal

Recommended next goal:

- Goal 104 - Design a public-safe output-quality methodology for the representativeness seed without semantic judging or live provider calls.

Alternative next goal:

- Goal 104 - Add a second route-only fixture slice after explicit approval for the category expansion boundary.
