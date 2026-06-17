# KORA Core Alpha Surface v0

Status: public alpha surface definition. This is not a complete implementation contract.

## Purpose

KORA Core is the planned open-source AI workload execution layer for routable AI workloads.

The current implementation is KRK-oriented. KRK means KORA Routing Kernel: the deterministic-first execution routing kernel inside KORA Core.

This document defines the first public-facing KORA Core alpha surface without claiming that every future command or module is implemented.

## North Star

Make AI workloads routable.

KORA Core should help developers understand, compare, execute, and review AI workload routes before treating model execution as the default first step.

## Current Alpha

Current public implementation focus:

- KRK routing concepts.
- deterministic-first execution control examples.
- bounded benchmark evidence.
- telemetry and evidence reports for current examples.
- public-safe docs for workload, target, route, and evidence concepts.

Verified top-level CLI commands on the current base:

- `examples`.
- `run`.
- `studio`.
- `telemetry`.

KRK alpha primitives documented in the public docs:

- route.
- explain.
- benchmark.
- report.

Those primitive names are not all exposed as top-level CLI commands on the current base.

## Future KORA Core Workflow

KORA Core should grow around four developer-facing workflow verbs:

- inspect.
- compare.
- run.
- report.

These verbs describe the intended KORA Core product model. They should be presented as alpha surface definitions until implementation, tests, and stable docs exist.

## Surface Map

| Workflow | Purpose | Current Status |
| --- | --- | --- |
| inspect | Understand workload shape, route metadata, target options, and evidence readiness. | Definition only. |
| compare | Compare route policies, targets, baselines, and expected evidence. | Definition only; current benchmark docs provide groundwork. |
| run | Execute a selected workload path under explicit policy and target constraints. | Current CLI has example-oriented `run`; full KORA Core `run` is roadmap. |
| report | Produce bounded evidence for route decisions, benchmark outputs, and reproducibility. | Partially represented by current telemetry and benchmark reports; first-class KORA Core report is roadmap. |

## KRK Boundary

KRK remains the routing kernel. KORA Core wraps KRK with broader workload-execution surfaces.

KRK answers:

- which execution path should this workload item take?
- why was that path selected?
- which routes were rejected or unavailable?
- what evidence should be recorded?

KORA Core should eventually answer:

- what is this workload?
- what routes and targets are available?
- how do options compare?
- how should the selected path run?
- what report can reviewers reproduce?

## Public-Safe Claim Boundary

Allowed:

- KORA Core is the planned OSS AI workload execution layer.
- KRK is the current routing-kernel first building block.
- The current alpha focuses on deterministic-first routing and evidence.
- `inspect`, `compare`, `run`, and `report` are the intended KORA Core workflow verbs.

Do not claim:

- KORA Core is production-ready.
- future workflow verbs are fully implemented commands.
- KORA Core proves production savings, broad superiority, infrastructure savings, or provider replacement.

## Next Implementation Direction

The next implementation work should be small and testable:

1. add read-only `inspect` behavior for existing workload fixtures.
2. add dry-run `compare` behavior for route policies and fixtures.
3. separate example-oriented `run` from future workload `run`.
4. generate a structured report from inspected and compared public-safe inputs.
