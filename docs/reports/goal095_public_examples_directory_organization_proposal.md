# Goal 095 Public Examples Directory Organization Proposal

Current public HEAD: `b6b323c339bd9e6b567351f95ce17b02d5be389b`

Status: documentation and proposal only. This goal did not move example directories, rename example directories, delete files, change repository settings, create a release, create a tag, create a GitHub Release, create a package publication, or change product claims.

## Purpose

KORA now has a clear public README and strong flagship examples, but the `examples/` directory still lists current first-value examples beside older basic, validation, benchmark, stress, and fixture examples. This goal improves the public examples index and records a future organization proposal without moving paths.

## Full Examples Directory Inventory

- `agent_workflow_optimization`
- `cache_reuse`
- `customer_support_triage_fake_validation`
- `deterministic_classification`
- `direct_vs_kora`
- `hello_kora`
- `kora_doctor`
- `openai_compatible_proxy`
- `rag_routing`
- `real_model_call_validation_fake`
- `real_workload_harness`
- `retry_demo`
- `runtime_integrated_benchmark`
- `stress_test`
- `workloads`

## Classification Table

| Directory | Group | Rationale |
| --- | --- | --- |
| `kora_doctor` | Flagship examples | Current first-value workload inspection and route-candidate reporting path. |
| `deterministic_classification` | Flagship examples | Current rule-routed classification example pack across practical scenarios. |
| `openai_compatible_proxy` | Flagship examples | Current OpenAI-style request routing example with offline provider-needed fallback labels. |
| `rag_routing` | Flagship examples | Current retrieval-needed versus provider-needed routing example. |
| `agent_workflow_optimization` | Flagship examples | Current multi-step workflow routing example across deterministic, cache, tool-needed, and provider-needed paths. |
| `cache_reuse` | Flagship examples | Current repeated-work reuse example using an offline local cache path. |
| `hello_kora` | Basic / first-run examples | Minimal graph example useful for first-run mechanics, but not part of the current flagship reviewer path. |
| `direct_vs_kora` | Basic / first-run examples | Comparison-style example useful for understanding the control layer, but older than the current flagship set. |
| `retry_demo` | Basic / first-run examples | Small runtime behavior example for retry handling. |
| `customer_support_triage_fake_validation` | Validation / harness examples | Validation-oriented customer-support fixture path. |
| `real_model_call_validation_fake` | Validation / harness examples | Local no-network validation example with historical naming that should remain stable until a dedicated rename or grouping plan. |
| `real_workload_harness` | Validation / harness examples | Harness-oriented example for workload validation flows. |
| `stress_test` | Validation / harness examples | Stress-run example retained for reproducibility rather than newcomer onboarding. |
| `workloads` | Validation / harness examples | Workload fixture directory supporting examples and validation paths. |
| `runtime_integrated_benchmark` | Benchmark / evidence examples | Benchmark-oriented runtime evaluation path outside the flagship reviewer path. |

## Proposed Future Grouping

Do not move directories without a dedicated approval gate. If approved later, a future organization could group examples as:

- `examples/flagship/` for `kora_doctor`, `deterministic_classification`, `openai_compatible_proxy`, `rag_routing`, `agent_workflow_optimization`, and `cache_reuse`.
- `examples/basic/` for `hello_kora`, `direct_vs_kora`, and `retry_demo`.
- `examples/validation/` for `customer_support_triage_fake_validation`, `real_model_call_validation_fake`, `real_workload_harness`, `stress_test`, and `workloads`.
- `examples/benchmarks/` for `runtime_integrated_benchmark`.

The current Goal 095 change uses README/index grouping only. It preserves every existing path.

## Risks of Moving Example Paths

- README quick-start commands may break.
- Reports and docs may link to current paths.
- Tests or scripts may refer to example directories directly.
- External links to public example paths may break.
- Historical evidence and validation context may become harder to trace.
- The `workloads` fixture directory may have implicit dependencies from examples or scripts.

## Link-Preserving Strategy for Future Moves

If example paths are moved in a later approved goal:

1. Inventory every internal link and script reference before moving.
2. Move one group at a time in a dedicated PR.
3. Leave a README stub at each old path when feasible.
4. Keep old run commands documented until replacement commands are validated.
5. Run markdown link validation and targeted example smoke checks.
6. Update `README.md`, `examples/README.md`, `docs/examples/kora_example_guide.md`, and relevant reports together.

## Boundary Confirmation

- No example directories were moved.
- No example directories were renamed.
- No files were deleted.
- No repository settings were changed.
- No release was created.
- No tag was created.
- No GitHub Release was created.
- No package publication was performed.
- No production-readiness claim was added.
- No cost-reduction proof claim was added.
- No `getkora` publication claim was added.
- No benchmark-superiority claim was added.

## Validation Results

- `python3 -m kora examples list`: passed.
- `python3 scripts/check_markdown_links_goal082b.py`: passed.
- `git diff --check`: passed.
- `python3 examples/cache_reuse/run.py`: passed.
- `python3 examples/rag_routing/run.py`: passed.
- `python3 examples/agent_workflow_optimization/run.py`: passed.
- High-risk private/internal scan over changed files: passed.

## Recommended Next Goal

Goal 096 - Documentation navigation and archive-bucket proposal, without moving files unless explicitly approved.
