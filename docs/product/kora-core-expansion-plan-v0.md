# KORA Core Expansion Plan v0

## Definition

KORA Core is the planned open-source AI workload execution layer for routable AI workloads.

The current public alpha is the routing and evidence first building block. It is KRK-oriented rather than a full KORA Core implementation.

## Main Workflow Direction

KORA Core should grow around four developer workflows:

- inspect.
- compare.
- run.
- report.

These are product-direction verbs. They should not be presented as fully implemented commands until the corresponding CLI/API surfaces exist.

## Doctor

`doctor` is a planned troubleshooting helper. It should inspect local setup, target configuration, workload validity, evidence output, and common routing failure modes.

## Current Implementation

Current alpha:

- route.
- explain.
- benchmark.
- report.

These are KRK alpha primitives. They help prove routing behavior and evidence reporting before KORA Core expands to a broader execution layer.

## Future Modules

KORA Core should add:

- Workload Spec: public-safe workload input, target, policy, and hint format.
- Target Registry: metadata for deterministic, local, provider, GPU, and fallback targets.
- Evidence Report: structured execution evidence for route decisions and benchmark results.
- Adapters: execution integrations behind explicit target metadata.
- Examples: reproducible route, explain, benchmark, report, and future inspect/compare/run flows.
- Developer Preview: bounded docs, examples, feedback templates, and limitations.

## Studio/UI Boundary

Studio and UI work should remain deferred relative to backend evidence. The backend routing kernel, workload spec, target registry, evidence schema, and examples should be clear before UI surfaces become the primary public proof path.

## Claim Boundary

KORA Core should be described as a planned open-source execution layer. Public docs should distinguish current alpha behavior from roadmap intent.
