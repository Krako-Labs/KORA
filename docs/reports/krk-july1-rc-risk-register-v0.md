# KRK July 1 RC Risk Register v0

Status: July 1 RC risk register.

| Risk | Severity | Impact | Mitigation | Blocks July 1 RC? |
| --- | --- | --- | --- | --- |
| Runtime-integrated workflow remains dry-run | Medium | Current runtime-integrated route-selectivity proof creates dry-run evidence records but does not execute production traffic, provider paths, GPU paths, or output-quality validation | Keep RC language dry-run and fixture-scoped; add live workflow and quality validation later | No, if disclosed |
| Broader workload representativeness | High | Small alpha fixtures cannot support broad workload claims | Keep claims limited to four public profiles; add larger synthetic and service-replay profiles later | No, if disclosed |
| Output quality validation | Medium | Route selection is measured, but selected-route output quality is not validated | Add quality rubric and sample validation in a later evidence goal | No, if disclosed |
| Provider sample remains bounded | Low | Twelve expanded provider calls strengthen provider-path evidence and reduce the initial sample-size concern, but still do not support provider benchmarking or superiority claims | Keep provider claim to bounded completion and aggregate metadata only; expand workload diversity later | No, if disclosed |
| H100 subset small | Medium | Four GPU-selected items and 24 repo-owned bounded harness operations are enough for bounded fixture-derived evidence but not broad GPU or H100 claims | Keep H100 claim subset-bounded; expand workloads later | No, if disclosed |
| Expanded H100 evaluation not measured | Medium | Goal 055 remains a historical prepared-but-not-measured expanded H100 routed-subset slot | Keep Goal 055 historical; use Goal 058C as separate repo-owned bounded harness evidence; expand workload diversity later | No, if disclosed |
| H100 runtime environment readiness | Low | Goal 058C prepared and used a CUDA-capable runtime for bounded harness execution, but local worktree runtime still cannot execute CUDA/H100 workloads | Use the repo-owned harness and controlled CUDA/H100 environment for future measured runs; keep raw logs local-only | No, if disclosed |
| Repo-owned H100 harness availability | Retired | Goal 058C added a reusable public harness that emits structured `not_run` output without CUDA and aggregate-only measured output with CUDA | Continue maintaining harness tests and aggregate-only output boundary | No |
| Top-level CLI mismatch | Medium | Planned KRK top-level commands are not fully aligned with current available command surfaces | Document exact current commands and add aliases or wrappers in a future scoped task | No, if disclosed |
| Future KORA Core implementation gap | High | Inspect, compare, run, and report remain roadmap direction rather than complete workflow implementation | Keep KORA Core language roadmap-scoped; implement workflow surfaces after RC | No, if disclosed |

## RC Risk Posture

The July 1 RC can proceed with caveats because the major gaps are claim-boundary and scope risks rather than blockers to publishing the current bounded evidence package. The provider sample-size risk is lower after the 12-call bounded validation, and the basic repo-owned H100 harness blocker is retired after Goal 058C. Expanded and broader H100 workload representativeness remains open.

The RC should not proceed if the intended public message requires production readiness, production savings, customer savings, broad workload superiority, H100 superiority, provider superiority, or replacement claims.
