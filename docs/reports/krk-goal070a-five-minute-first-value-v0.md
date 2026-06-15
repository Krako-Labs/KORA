# KRK Goal 070A Five-Minute First Value v0

Status: public-safe first-value workflow implemented.

Final classification: `FIVE_MINUTE_FIRST_VALUE_PATH_MEASURED`

## Motivation

KRK now has reviewer-facing technical evidence across route selectivity, runtime-integrated routing, provider validation, H100 harness execution, expanded H100 representativeness, and baseline equivalence/output fidelity. That evidence answers whether KRK is technically coherent.

The remaining OSS onboarding question is different:

Can a new user get value from KORA in approximately five minutes?

Goal 070A creates the first public-safe path from fresh clone to first value using existing repo-owned functionality.

## Target User

The target user is a prospective OSS evaluator who wants to understand KORA before configuring providers, GPUs, private workloads, or production systems.

Assumptions:

- the user can run Python from the repository root.
- the user has no provider credentials configured.
- the user has no GPU available.
- the user wants a local, public-safe, reproducible first experience.

## First-Value Definition

First value means the user can see KORA perform a complete local workflow:

1. inspect available execution paths.
2. compare direct and KRK-routed execution paths.
3. run a public-safe fixture workflow.
4. report route and output-fidelity results.

The workflow is intentionally scoped to local public fixtures. It is not a benchmark-strengthening task and does not create production claims.

## Implementation

Goal 070A adds:

- `kora/five_minute_first_value.py`
- `scripts/kora_five_minute_demo.py`
- `tests/test_five_minute_first_value.py`

The wrapper reuses existing public-safe evaluators:

- `kora.runtime_route_evaluator.evaluate_runtime_routes`
- `kora.output_fidelity.evaluate_output_fidelity`

No provider calls, GPU execution, network access, private logs, or private configuration are required.

## Workflow Steps

| Step | User-facing purpose | Repo-owned source |
| --- | --- | --- |
| inspect | Show execution paths, workload profiles, and environment requirements. | public matrix fixtures and route constants |
| compare | Contrast direct model-candidate path with KRK-routed path. | runtime route evaluator counters |
| run | Execute public-safe route-specific dry-run workflow. | runtime route evaluator |
| report | Generate route and output-fidelity summary. | output fidelity evaluator |

## Execution Path

```bash
python3 scripts/kora_five_minute_demo.py \
  --json-out docs/evidence/generated/krk-goal070a-five-minute-first-value-summary-v0.json \
  --md-out docs/evidence/generated/krk-goal070a-five-minute-first-value-summary-v0.md
```

Fresh-clone quickstart users should write to `/tmp` first:

```bash
python3 scripts/kora_five_minute_demo.py \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

## Generated Outputs

- [Generated Goal 070A first-value JSON summary](../evidence/generated/krk-goal070a-five-minute-first-value-summary-v0.json)
- [Generated Goal 070A first-value Markdown summary](../evidence/generated/krk-goal070a-five-minute-first-value-summary-v0.md)
- [Five-minute first-value quickstart](../quickstart-five-minute-first-value.md)

## Measured Onboarding Complexity

| Metric | Value |
| --- | ---: |
| Step count | 4 |
| Commands required | 1 |
| Required user decisions | 0 |
| Estimated time to first value, minutes | 5 |
| Provider credentials required | false |
| GPU required | false |
| Network required | false |
| Generated outputs | 2 |

## First-Value Evidence Summary

| Metric | Value |
| --- | ---: |
| Total fixture items | 18 |
| Dry-run execution success rate | 1.0000 |
| Unsafe misroute rate | 0.0000 |
| Output exact match count | 17 |
| Output structured equivalent count | 1 |
| Output degraded count | 0 |
| Output failed count | 0 |
| Acceptable output rate | 1.0000 |

## Compare Step Result

The compare step reports `11 / 18` local-or-guardrail routing opportunities:

- deterministic: 2
- cache: 3
- CPU: 2
- fallback: 4

These are items routed away from provider/GPU-class paths in the public fixture workflow. This is an execution-path opportunity count, not a production savings claim.

## Limitations

- The workflow uses public fixtures, not customer workloads.
- The workflow is local dry-run evidence, not production execution.
- Provider and GPU paths are represented by public fixture routing and dry-run evidence, not live execution.
- The time-to-first-value estimate is an onboarding complexity estimate, not a timed usability study.
- The wrapper is a first public-safe path; official `kora inspect`, `kora compare`, `kora run`, and `kora report` commands remain future interface work.

## Claim Boundary

Supported:

- KORA has a one-command public-safe first-value workflow.
- The workflow exposes inspect, compare, run, and report steps over committed public fixtures.
- The workflow works without provider credentials, GPU hardware, or network access.
- The workflow produces JSON and Markdown summaries.

Not supported:

- production adoption.
- production readiness.
- production cost reduction.
- customer savings.
- provider superiority.
- H100 superiority.
- broad workload superiority.
- real API/GPU cost reduction.

## Future Inspect/Compare/Run/Report Roadmap

The wrapper should evolve into official CLI commands:

- `kora inspect`: list execution paths, fixture/workload sources, local environment readiness, and claim boundaries.
- `kora compare`: compare direct, deterministic, KRK-routed, provider, GPU, and fallback plans over a selected workload.
- `kora run`: execute the selected public-safe or user-provided workload through the local runtime path.
- `kora report`: render route, output-fidelity, environment, and claim-boundary reports from a run artifact.

Future work should keep the same public/private boundary: no private paths, no raw provider responses, no raw GPU logs, no credentials, and no unsupported production claims.
