# KORA Workload Expansion Plan for v0.2.0-alpha

Date: 2026-05-04

## Current Workload Status

The current deterministic-heavy workload is:

```text
experiments/workloads/deterministic_heavy_v0.json
```

It contains 20 handwritten tasks across six deterministic-first categories:

| Category | Current task count |
|---|---:|
| arithmetic | 4 |
| cache_lookup | 3 |
| json_validation | 3 |
| routing_decision | 4 |
| schema_check | 3 |
| string_normalization | 3 |

Current metadata split:

| Metric | Value |
|---|---:|
| Total tasks | 20 |
| `requires_model: false` | 16 |
| `requires_model: true` | 4 |

The current benchmark runner supports `dry-run`, `direct-baseline`, and `kora-controlled` modes. The current benchmark is simulated and deterministic-heavy. It does not make production cost, real API-cost, or full runtime integration claims.

## Target Workload Size

The expansion should happen in controlled increments.

| Milestone | Target size | Purpose |
|---|---:|---|
| Near-term target | 100 tasks | Large enough to exercise category coverage, correctness checks, and result summaries without creating large maintenance overhead. |
| Technical preview target | 300-500 tasks | Large enough for a v0.2.0-alpha technical preview benchmark while remaining inspectable and reproducible. |

## Workload Expansion Principles

1. Keep the workload deterministic-heavy until the benchmark runner has stronger correctness checks.
2. Prefer clear, inspectable tasks over broad synthetic volume.
3. Preserve explicit `requires_model` metadata so direct-baseline and KORA-controlled modes remain comparable.
4. Avoid ambiguous expected outputs.
5. Keep fallback candidates clearly labeled as fallback/model-invocation candidates, not as failed deterministic tasks.
6. Add categories incrementally so each expansion can be reviewed and validated.
7. Keep public claim wording limited to simulated controlled benchmark evidence until runtime-integrated measurements exist.

## Category Expansion Plan

### Current Categories

The next workload version should expand the current categories first:

| Category | Expansion direction |
|---|---|
| arithmetic | Add integer, decimal, percentage, rounding, and order-of-operations cases with exact expected outputs. |
| string_normalization | Add casing, whitespace, punctuation, Unicode-normalization-safe ASCII cases, and identifier normalization. |
| json_validation | Add valid/invalid JSON shape checks, missing-key cases, type mismatch cases, and nested structure checks. |
| routing_decision | Add deterministic route selection from structured inputs, priority rules, and fallback-on-ambiguity cases. |
| cache_lookup | Add hit, miss, stale, namespace, and key-normalization cases. |
| schema_check | Add required fields, optional fields, enum checks, nested schema checks, and boundary-value cases. |

### Future Candidate Categories

Future workload versions may add:

| Category | Purpose |
|---|---|
| date_normalization | Normalize deterministic dates and date formats where no interpretation is required. |
| unit_conversion | Convert units with exact conversion rules and rounding policy. |
| config_validation | Validate structured configuration objects and report deterministic failures. |
| policy_rule_match | Match inputs against explicit policy/rule tables. |
| template_rendering | Render deterministic templates from structured variables. |
| deterministic_lookup | Resolve values from static lookup tables outside cache-specific cases. |
| retry_recoverable_failure | Model deterministic retry/recovery scenarios without external calls. |
| verifier_reject_case | Exercise cases where verification rejects malformed or incomplete deterministic outputs. |

## Task Schema Policy

The workload schema should preserve the current task fields:

| Field | Policy |
|---|---|
| `id` | Stable, unique, human-readable identifier. Use category prefixes when practical. |
| `category` | One of the documented category names. New categories must be documented before use. |
| `input` | Structured input payload. Prefer objects over encoded strings where possible. |
| `expected_path` | Deterministic path or decision expected from KORA-controlled handling. |
| `expected_output` | Verifiable expected output for deterministic tasks. |
| `requires_model` | Boolean metadata. `false` means expected deterministic resolution; `true` means fallback/model-invocation candidate. |
| `notes` | Short note explaining why the case exists and whether it is deterministic or a fallback candidate. |

Future schema refinements may add fields such as `difficulty`, `source`, `seed`, `expected_error`, or `tags`, but the v0.2.0-alpha expansion should avoid schema churn unless it directly improves validation.

## Expected-Output Policy

Every deterministic task must have a verifiable `expected_output`.

Fallback candidates may include expected behavior, expected route, or expected fallback reason, but they should not require exact generated model content. For fallback candidates, expected fields should describe the deterministic benchmark expectation, such as "fallback required", "model candidate", or "ambiguous input".

Future correctness checks should compare benchmark runner output against `expected_output` where tasks are deterministic. Correctness scoring should be reported separately from simulated model-invocation counts.

## Fallback Candidate Policy

Fallback candidates should remain a minority of the deterministic-heavy workload.

Recommended ratio for v0.2.0-alpha:

| Workload size | Deterministic tasks | Fallback candidates |
|---|---:|---:|
| 100 tasks | 75-85 | 15-25 |
| 300-500 tasks | 75-85% | 15-25% |

Fallback candidates should be included to test the boundary where deterministic handling should stop. They should not be used to inflate avoided-invocation rates, and they should not imply that a real model call has occurred.

## Generated-vs-Handwritten Task Policy

The workload should combine handwritten seed cases with deterministic generation.

Recommended approach:

1. Use handwritten seed cases for coverage, readability, and reviewability.
2. Use deterministic generator scripts for scale only after the schema and correctness checks are stable.
3. Require generated tasks to be reproducible from a documented seed.
4. Keep generator inputs and seed data reviewable.
5. Do not generate tasks with ambiguous expected outputs.
6. Do not introduce random task variation without checked-in seed configuration.

Generated tasks should still produce stable IDs, stable expected outputs, and stable category counts.

## Validation Policy

The v0.2.0-alpha workload should be validated through:

1. JSON syntax validation with `python3 -m json.tool`.
2. Schema validation for required task fields and value types.
3. Category validation against documented allowed categories.
4. Unique ID validation.
5. Deterministic `expected_output` validation for `requires_model: false` tasks.
6. Benchmark mode validation for `dry-run`, `direct-baseline`, and `kora-controlled`.
7. Release validation through `./scripts/release_smoke.sh`.
8. Full test validation through `python3 -m pytest -q`.
9. CI validation before merge.

## Result Artifact Policy Options

| Option | Pros | Cons |
|---|---|---|
| Commit generated JSON results | Exact outputs are reviewable and archived. | Can create churn, merge noise, and stale artifacts if policy is weak. |
| Generate results on demand only | Keeps the repository clean and avoids artifact churn. | Reviewers must rerun commands to inspect exact outputs. |
| Commit summary markdown but not raw JSON | Keeps public evidence concise and readable while preserving reproducibility commands. | Raw structured outputs are not available in git history. |

Recommended policy for now:

- keep raw generated benchmark outputs uncommitted
- commit markdown summaries and reproducibility commands
- revisit raw result artifact policy at v0.2.0-alpha once output schema and correctness scoring are stable

## v0.2.0-alpha Acceptance Criteria

The v0.2.0-alpha benchmark milestone should require:

1. 100+ deterministic-heavy tasks.
2. Expanded coverage across all current categories.
3. Documented policy for future categories.
4. `direct-baseline` and `kora-controlled` modes pass on the expanded workload.
5. Stronger correctness checks exist for deterministic tasks.
6. Benchmark result summary is generated or manually documented from reproducible commands.
7. Reproducibility commands are documented.
8. CI remains green.
9. No production cost claim is made.
10. No real API-cost reduction claim is made.
11. Limitations and non-claims remain explicit.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Generated tasks become hard to review | Keep handwritten seed cases and require deterministic seed configuration. |
| Expected outputs become ambiguous | Require exact expected outputs for deterministic tasks and reject ambiguous generation rules. |
| Category drift weakens comparability | Document allowed categories and validate category names. |
| Avoided-invocation rate is overinterpreted | Keep safe claim wording and explicit non-claims in benchmark summaries. |
| Raw result artifacts create churn | Keep raw JSON generated-only until v0.2.0-alpha policy is finalized. |
| Fallback candidates are too easy or too broad | Keep fallback candidates clearly scoped and review their ratio per category. |
| Correctness is ignored in favor of invocation counts | Add correctness checks before expanding beyond the near-term 100-task target. |

## Proposed Next Implementation Tasks

1. Add workload schema validation tests for required fields and unique IDs.
2. Add deterministic correctness checks for `requires_model: false` tasks.
3. Draft `deterministic_heavy_v1.json` with 100 tasks.
4. Add category-count expectations for the expanded workload.
5. Add a generated-task policy note if generator scripts are introduced.
6. Add benchmark summary generation once result JSON schema stabilizes.
7. Update `docs/technical_preview_results.md` after the 100-task workload is validated.
