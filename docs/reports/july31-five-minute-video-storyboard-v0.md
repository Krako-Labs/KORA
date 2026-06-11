# July 31 Five-Minute Video Storyboard v0

Status: planning storyboard. This is not a recorded video, final script, or submission artifact.

## Purpose

The five-minute video should explain KORA's public-safe July 31 story:

- KORA makes AI workloads routable.
- KRK is the deterministic-first routing kernel.
- bounded evidence exists for the current alpha.
- KORA Core expands KRK into an execution layer.
- next work is concrete and measurable.

Tone:

- technical.
- calm.
- evidence-backed.
- no overclaiming.

## 0:00-0:30 Problem

Visual:

- simple diagram of fragmented AI execution paths.
- deterministic, cache, CPU, provider, GPU, and fallback paths shown as separate choices.

Narration points:

- AI execution is no longer one path.
- Developers need to know when a model call, local execution, provider execution, GPU-class compute, or fallback is appropriate.
- KORA's north star is to make AI workloads routable.

Avoid:

- saying KORA solves all AI infrastructure problems.
- saying KORA replaces existing providers or serving systems.

## 0:30-1:30 KRK

Visual:

- KRK routing flow.
- workload input -> routing decision -> selected path -> evidence.

Narration points:

- KRK means KORA Routing Kernel.
- KRK is deterministic-first.
- KRK routes tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.
- KRK is the first technical wedge inside KORA Core.

Suggested line:

> KRK asks which execution path is justified before treating model execution as the default.

Avoid:

- claiming every KRK primitive is a stable top-level CLI command unless that command is implemented and tested.

## 1:30-2:30 Evidence

Visual:

- deterministic-heavy benchmark table.
- evidence package index.
- claim boundary table.

Narration points:

- Current evidence is bounded and reproducible.
- In the deterministic-heavy 100-task benchmark, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.
- The package also includes methodology for route accuracy, GPU-routed subset measurement, reproducibility, and claim boundaries.
- Missing metrics are marked as not measured yet.

Suggested line:

> This is alpha evidence. It is useful because it is bounded, reproducible, and explicit about what it does not prove.

Avoid:

- production savings.
- customer-level savings.
- broad workload superiority.
- final validation language.

## 2:30-3:30 KORA Core Expansion

Visual:

- hierarchy: KORA -> KORA Core -> KRK.
- workflow: inspect -> compare -> run -> report.

Narration points:

- KRK is not the whole destination.
- KORA Core is the planned open-source AI workload execution layer.
- KORA Core expands the routing kernel into developer workflows:
  - inspect workloads.
  - compare routes and targets.
  - run selected workload paths.
  - report bounded evidence.
- Current docs define the alpha surface while clearly separating implemented behavior from roadmap.

Avoid:

- presenting inspect, compare, run, and report as complete if they are still roadmap or partial.

## 3:30-4:30 Demo Path

Visual:

- terminal or slide-based demo path.
- show docs and existing public commands rather than relying on unimplemented future commands.

Demo sequence:

1. show KORA docs index.
2. show KRK evidence summary.
3. show KRK performance table.
4. show KORA Core alpha surface docs.
5. show an existing reproducible command path, such as tests or an offline example.

Possible command references:

```bash
python3 -m pytest
python3 -m kora --help
python3 -m kora run runtime_integrated_benchmark -- --offline
```

Use only commands verified on the current repo before recording.

Narration points:

- The current demo should prioritize reproducibility.
- Show where evidence and limitations are documented.
- Explain which surfaces are current alpha and which are next steps.

Avoid:

- live external calls.
- private environment details.
- raw GPU logs.
- unverified command claims.

## 4:30-5:00 Next Plan

Visual:

- roadmap checklist.
- next experiments.
- developer preview path.

Narration points:

- Next work connects the KRK matrix fixtures to a dry-run evaluator.
- KORA Core implements first inspect and compare paths.
- Workload Spec, Target Registry, and Evidence Report become public developer artifacts.
- Community examples and sanitized workload proposals help expand coverage.

Closing line:

> KORA's next step is to turn deterministic-first routing evidence into a practical open-source execution layer for routable AI workloads.

## Video Claim Boundary

Allowed:

- KRK frames deterministic-first execution routing.
- KORA Core expands KRK toward inspect, compare, run, and report.
- bounded deterministic-heavy benchmark evidence exists.
- the July 31 package is a readiness and planning package.

Do not claim:

- production readiness.
- production savings.
- 10x savings.
- customer-level savings.
- infrastructure savings.
- broad workload superiority.
- H100 superiority.
- final competition results.
- formal validation.
- replacement of model providers, API routers, or serving systems.
