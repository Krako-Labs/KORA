# KRK July 1 RC Risk Register v0

Status: July 1 RC risk register.

| Risk | Severity | Impact | Mitigation | Blocks July 1 RC? |
| --- | --- | --- | --- | --- |
| Runtime-integrated workflow gap | High | Current route-selectivity proof is dry-run and separate from the full runtime path | Keep RC language dry-run and fixture-scoped; add runtime-integrated workflow implementation after RC package review | No, if disclosed |
| Broader workload representativeness | High | Small alpha fixtures cannot support broad workload claims | Keep claims limited to four public profiles; add larger synthetic and service-replay profiles later | No, if disclosed |
| Output quality validation | Medium | Route selection is measured, but selected-route output quality is not validated | Add quality rubric and sample validation in a later evidence goal | No, if disclosed |
| Provider sample size small | Medium | Three provider-selected items are enough for bounded path validation but not provider benchmarking | Keep provider claim to bounded completion and aggregate metadata only; expand sample later | No, if disclosed |
| H100 subset small | Medium | Four GPU-selected items are enough for bounded subset evidence but not broad GPU claims | Keep H100 claim subset-bounded; expand workloads later | No, if disclosed |
| Top-level CLI mismatch | Medium | Planned KRK top-level commands are not fully aligned with current available command surfaces | Document exact current commands and add aliases or wrappers in a future scoped task | No, if disclosed |
| Future KORA Core implementation gap | High | Inspect, compare, run, and report remain roadmap direction rather than complete workflow implementation | Keep KORA Core language roadmap-scoped; implement workflow surfaces after RC | No, if disclosed |

## RC Risk Posture

The July 1 RC can proceed with caveats because the major gaps are claim-boundary and scope risks rather than blockers to publishing the current bounded evidence package.

The RC should not proceed if the intended public message requires production readiness, production savings, customer savings, broad workload superiority, H100 superiority, provider superiority, or replacement claims.
