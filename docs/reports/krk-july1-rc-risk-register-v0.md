# KRK July 1 RC Risk Register v0

Status: July 1 RC risk register.

| Risk | Severity | Impact | Mitigation | Blocks July 1 RC? |
| --- | --- | --- | --- | --- |
| Runtime-integrated workflow remains dry-run | Medium | Current runtime-integrated route-selectivity proof creates dry-run evidence records but does not execute production traffic, provider paths, GPU paths, or output-quality validation | Keep RC language dry-run and fixture-scoped; add live workflow and quality validation later | No, if disclosed |
| Broader workload representativeness | High | Small alpha fixtures cannot support broad workload claims | Keep claims limited to four public profiles; add larger synthetic and service-replay profiles later | No, if disclosed |
| Output quality validation | Medium | Route selection is measured, but selected-route output quality is not validated | Add quality rubric and sample validation in a later evidence goal | No, if disclosed |
| Provider sample remains bounded | Medium | Twelve expanded provider calls strengthen provider-path evidence but still do not support provider benchmarking or superiority claims | Keep provider claim to bounded completion and aggregate metadata only; expand workload diversity later | No, if disclosed |
| H100 subset small | Medium | Four GPU-selected items are enough for bounded subset evidence but not broad GPU claims | Keep H100 claim subset-bounded; expand workloads later | No, if disclosed |
| Top-level CLI mismatch | Medium | Planned KRK top-level commands are not fully aligned with current available command surfaces | Document exact current commands and add aliases or wrappers in a future scoped task | No, if disclosed |
| Future KORA Core implementation gap | High | Inspect, compare, run, and report remain roadmap direction rather than complete workflow implementation | Keep KORA Core language roadmap-scoped; implement workflow surfaces after RC | No, if disclosed |

## RC Risk Posture

The July 1 RC can proceed with caveats because the major gaps are claim-boundary and scope risks rather than blockers to publishing the current bounded evidence package.

The RC should not proceed if the intended public message requires production readiness, production savings, customer savings, broad workload superiority, H100 superiority, provider superiority, or replacement claims.
