# KRK Goal 045 Task Breakdown v0

## Goal

Implement KRK route-selectivity metrics for the committed matrix fixtures.

Goal 045 should turn the current route-selectivity methodology into a deterministic dry-run evaluator with JSON and Markdown outputs.

## Scope

Goal 045 should implement:

- matrix evaluator CLI or script.
- route metrics computation.
- JSON output.
- Markdown report output.
- tests.
- example generated outputs if public-safe and deterministic.

Goal 045 must not:

- run GPU tests.
- call providers.
- create a release.
- create a tag.
- upload release assets.
- claim production savings.
- expose private details.

## Inputs

Use the existing fixtures:

- `examples/workloads/krk-mixed-routing-matrix-alpha.json`
- `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-adversarial-routing-matrix-alpha.json`

## Implementation Steps

### 1. Inspect Current CLI And Example Patterns

Review:

- `python3 -m kora --help`.
- existing `examples/` runner patterns.
- existing report generation patterns.
- current tests for examples and benchmark output.

Decide whether the first implementation should be:

- a `python3 -m kora run ... -- --offline` example, or
- a small script under `examples/`, or
- a module utility with tests and a documented command.

Prefer the repo's existing example-runner pattern unless it creates unnecessary complexity.

### 2. Add Fixture Loader

Implement loader that:

- reads a matrix JSON file.
- validates required fields.
- returns normalized item records.
- keeps original order stable.

### 3. Add Oracle Isolation

Implement route request construction that includes only:

- request ID.
- workload profile.
- workload class.
- router-visible metadata.

Add tests proving route policies do not receive `oracle_labels`.

### 4. Add Baseline Policy Or Policy Adapter

Implement enough policy behavior to evaluate fixtures.

Preferred first set:

- `all_gpu`.
- `static_heuristic`.
- `provider_first_with_gpu_fallback`.
- `KRK` adapter if current policy can be called safely.

If KRK policy is not callable yet, implement a policy interface and document the missing adapter rather than faking a measured KRK result.

### 5. Add Metrics Computation

Compute:

- `total_requests`.
- `route_counts`.
- `exact_route_accuracy`.
- `acceptable_route_rate`.
- `unsafe_misroute_rate`.
- `gpu_false_positive_count`.
- `gpu_false_negative_count`.
- `cache_hit_correctness_rate`.
- `safety_fallback_rate`.
- `failure_fallback_rate`.
- `fallback_counts`.
- `error_count`.
- `error_percentage`.
- `compute_weighted_gpu_demand`, if small and safe.
- `claim_level`.

### 6. Add Output Writers

Emit:

- stable JSON.
- Markdown summary.

Recommended generated example paths, if committed:

- `examples/reports/krk-route-selectivity-metrics-alpha.json`
- `examples/reports/krk-route-selectivity-summary-alpha.md`

If generated outputs are not committed, document the output path and command.

### 7. Add Tests

Tests should cover:

- valid fixture parsing.
- invalid fixture failure.
- route input excludes oracle labels.
- exact-route metric.
- acceptable-route metric.
- unsafe misroute metric.
- GPU false positives.
- GPU false negatives.
- cache correctness.
- fallback counts.
- compute-weighted GPU demand if implemented.
- JSON output shape.
- Markdown output contains claim boundary.

### 8. Update Evidence Docs

After implementation and generated metrics:

- update `docs/evidence/krk-performance-table-v0.md`.
- update `docs/evidence/krk-capability-matrix-v0.md`.
- optionally update July 1 readiness docs if present on the active branch.

Do not mark missing metrics as measured unless generated output exists and tests pass.

## Validation Commands

Run:

```bash
python3 -m pytest
git diff --check
jq empty examples/workloads/krk-mixed-routing-matrix-alpha.json
jq empty examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json
jq empty examples/workloads/krk-cache-heavy-routing-matrix-alpha.json
jq empty examples/workloads/krk-adversarial-routing-matrix-alpha.json
```

Run public/private and claim scans before commit.

## Acceptance Criteria

Goal 045 is complete when:

- evaluator runs on all four fixtures.
- generated JSON is valid.
- generated Markdown is public-safe.
- tests pass.
- no GPU or provider calls are required.
- metrics are bounded as dry-run route-selectivity evidence.
- unsupported claims are not introduced.

## Recommended Commit Message

```text
feat: add KRK route-selectivity metrics evaluator
```
