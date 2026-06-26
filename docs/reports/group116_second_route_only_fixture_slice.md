# Group 116 Second Route-Only Fixture Slice

Status: implemented with local validation complete; PR open.

## Objective

Group 116 adds a second public-safe synthetic route-only fixture slice adjacent to, but distinct from, the Goal 102 representativeness seed and Goal 103 route-only evaluator.

This group adds breadth to route-shape evidence only. It does not prove output quality, broader workload representativeness, production readiness, production validation, production cost reduction, customer savings, provider replacement, H100/GPU/CPU superiority, or GPU-serving replacement.

## Approval Packet

Decision needed: review and decide whether to merge Group 116 second route-only fixture slice.

Risk level: low

Final status classification: `merge-ready`

Changed files: second synthetic route-only fixture, narrow validator schema generalization, route-only evaluator, focused tests, Group 116 report, docs index, queue, and breadcrumbs.

Validation summary: focused slice tests, existing Goal 102/103 tests, real route-only evaluator run, markdown links, whitespace diff check, and full pytest passed.

Repair attempts: 1.

Failures encountered: initial focused test expectations used `category_count == 11`, `fallback == 5`, and `tool_needed == 5`; the real fixture/evaluator correctly reported 12 categories, `fallback == 4`, and `tool_needed == 6`. Tests were updated to match the implemented fixture design.

Self-review summary: scope is fixture-only route-shape evidence, validation/evaluation tests, report, and breadcrumbs. `CIL-003` remains deferred. No validation profile registry or command profile registry was changed.

Claim-boundary audit: Group 116 is route-only aggregate evidence over a synthetic public-safe fixture. It does not call providers, run model inference, run H100/GPU/CUDA/server/remote execution, perform semantic judging or human grading, publish packages, claim `getkora` is published, claim install-from-PyPI support, or make production/output-quality/broader-representativeness/cost-reduction/provider-replacement/GPU-serving-replacement claims.

Forbidden-action audit: no `CIL-003` implementation, validation profile registry change, command profile registry change, provider call, model inference, H100/GPU/CUDA/server/remote execution, semantic judging, human grading, release, tag, GitHub Release, release asset, PyPI publication, package publication, issue, project board, repository settings change, collaborator change, file movement, file rename, file archive, file deletion, or local-only project context change was added.

Uncertainty notes: none. The fixture and evaluator are deterministic and route-only.

workflow recommendation: Merge after normal review.

Albert action options: Merge / Request R1 / Stop.

## Base And Branch

- public truth: `origin/main`
- base public HEAD: `49affdfb25bb7551e30255839a4816047971ced9`
- branch: `workflow/group116-route-only-fixture-slice`
- worktree: `/Users/albertkim/02_PROJECTS/05_KORA_Project/worktrees/group116_route_only_fixture_slice`
- PR: https://github.com/Krako-Labs/KORA/pull/268

## Subtasks

- 116-1 Fixture scope and category design: designed a second synthetic route-only slice focused on practical workload-control surfaces that are adjacent to Goal 102 but not a mechanical copy.
- 116-2 Second route-only fixture: added `examples/workloads/kora-representativeness-slice-v1.json` with 40 public-safe fixture-only items.
- 116-3 Shape validator / reuse decision: reused the existing Goal 102 validator with narrow backward-compatible schema-version generalization.
- 116-4 Route-only evaluator: added `scripts/evaluate_representativeness_slice_routes.py`, emitting aggregate counters only.
- 116-5 Focused tests: added `tests/test_representativeness_slice_route_only_evaluator.py`.
- 116-6 Real local route-only run: ran the new evaluator locally and recorded counters below.
- 116-7 Report / breadcrumbs / queue update: added this report and updated `OPEN_THIS_FIRST.md`, `REVIEW_HUB.md`, `docs/README.md`, and `docs/context/NEXT_GOAL_QUEUE.md`.
- 116-8 Validation / PR open: validation completed locally; PR opened after commit and push.

## Fixture Design Summary

The second slice emphasizes practical workload-control surfaces not fully stressed by the Goal 102 seed:

- multi-step app workflow routing.
- document intake and normalization.
- local policy checks.
- schema validation.
- retry and fallback control.
- cache-reuse candidates.
- tool-needed local action candidates.
- retrieval-needed candidates.
- provider-needed ambiguous tasks.
- GPU-candidate batch labels only, with no GPU execution.
- CPU/local deterministic transforms.
- report-generation control tasks.

The fixture remains synthetic, public-safe, and fixture-only. It includes stable IDs, categories, explicit route labels, rationales, public-safety flags, and fixture-only claim scope. It avoids private data, real customer data, live provider examples, raw model outputs, secrets, restricted URLs, and infrastructure details.

It is adjacent to Goal 102 because it uses the same public-safe shape and allowed route labels. It is distinct because it focuses more heavily on local app workflow control, schema/policy/retry surfaces, and operational report-control routing rather than the original support/issue/RAG/agent seed mix.

## Real Route-Only Run Counters

Command:

```bash
python3 scripts/evaluate_representativeness_slice_routes.py
```

Observed result:

- total slice items: `40`
- unsupported / unknown / missing route metadata count: `0`
- route counts:
  - `cache`: `7`
  - `cpu`: `6`
  - `deterministic`: `5`
  - `fallback`: `4`
  - `gpu`: `3`
  - `provider_needed`: `4`
  - `retrieval_needed`: `5`
  - `tool_needed`: `6`
- route group counts:
  - `cache_reuse_candidates`: `7`
  - `deterministic_local_route_candidates`: `22`
  - `fallback_control_candidates`: `4`
  - `provider_model_candidates`: `7`
- workload category count: `12`

This run emitted aggregate counters only. It did not call providers, run model inference, run H100/GPU/CUDA/server/remote execution, inspect output quality, perform semantic judging, or perform human grading.

## Files Added

- `examples/workloads/kora-representativeness-slice-v1.json`
- `scripts/evaluate_representativeness_slice_routes.py`
- `tests/test_representativeness_slice_route_only_evaluator.py`
- `docs/reports/group116_second_route_only_fixture_slice.md`

## Files Updated

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- `docs/README.md`
- `docs/context/NEXT_GOAL_QUEUE.md`
- `scripts/validate_representativeness_seed.py`

## Validation Results

Final validation before PR open:

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_representativeness_slice_route_only_evaluator.py tests/test_representativeness_seed.py tests/test_representativeness_route_only_evaluator.py` | passed, `12 passed` |
| `python3 scripts/evaluate_representativeness_slice_routes.py` | passed; `40` items; unsupported/unknown/missing route metadata `0` |
| `python3 scripts/check_markdown_links_goal082b.py` | passed |
| `git diff --check` | passed |
| `python3 -m pytest` | passed, `501 passed` |

## Loop Count And Repairs

- loop count: 1
- repair attempts: 1
- max loop count: 5
- max repair attempts per failing subtask: 2

## Risk And Final Classification

- risk level: low
- final status classification: `merge-ready`

Rationale: this group adds a deterministic synthetic fixture, a route-only aggregate evaluator, focused tests, and narrow docs. It does not change command registries, validation profile registries, public positioning, package state, or claim boundaries.

## Self-Review

- changed files match the approved second route-only fixture slice scope.
- fixture is synthetic, public-safe, and small enough for review.
- evaluator emits aggregate route/category/group counters only.
- unsupported / unknown / missing route metadata count is `0`.
- `CIL-003` remains deferred and was not implemented.
- no validation profile registry changed.
- no command profile registry changed.
- no provider calls were added or executed.
- no model inference was added or executed.
- no H100/GPU/CUDA/server/remote execution was added or executed.
- no semantic judging or human grading was added.
- no PyPI/package publication/release/tag action was added.
- no `getkora` published or install-from-PyPI support claim was added.
- no production readiness, production validation, output-quality proof, broader workload representativeness proof, cost-reduction proof, customer-savings claim, provider replacement claim, or GPU-serving replacement claim was added.
- no local-only project context changed.

## Next Recommendation

Recommended next action: review and merge Group 116 if the PR passes CI and the merge gate confirms the same boundaries.

`CIL-003` remains deferred until Albert explicitly approves the medium-risk profile-registry checklist.

## Claim Boundary Reminder

Group 116 adds route-only aggregate counters over a synthetic fixture. It does not prove output quality, broader workload representativeness, production workload handling, production readiness, production validation, cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, or GPU-serving replacement.
