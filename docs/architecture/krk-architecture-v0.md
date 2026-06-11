# KRK Architecture v0

## Position Inside KORA Core

KRK is the KORA Routing Kernel inside KORA Core.

KORA Core is the planned open-source AI workload execution layer. KRK is its first technical wedge: deterministic-first execution-path routing with evidence output.

## Routing Input

A KRK routing input should describe:

- workload identity.
- input size.
- batch size.
- request modality.
- cache availability.
- latency sensitivity.
- privacy preference.
- estimated complexity.
- target constraints.
- policy constraints.

Oracle labels used for benchmark evaluation must stay separate from router-visible metadata.

## Route Decision

A route decision selects one execution path:

- deterministic.
- cache.
- CPU.
- provider.
- GPU.
- fallback.

The decision should include a reason, policy context, and evidence fields that can be reported safely.

## Execution Path Classes

### Deterministic

Known logic, templates, rules, validation checks, or structured computation can resolve the request without model execution.

### Cache

Valid prior output can be reused under the workload policy.

### CPU

Local CPU execution is adequate for the workload shape.

### Provider

External or provider-compatible model execution is appropriate and allowed by policy.

### GPU

GPU-class compute is justified by workload shape, batch size, modality, or complexity.

### Fallback

Fallback is selected when policy, target availability, validation failure, malformed input, or safety constraints prevent a preferred route.

## Route Explanation

Every route decision should be explainable:

- selected route.
- visible metadata used.
- policy constraints.
- rejected routes.
- fallback classification if relevant.
- evidence boundary.

## Benchmark And Evidence Path

KRK benchmark evidence should compare routing policies across public-safe workload matrices:

- `all_gpu`.
- `static_heuristic`.
- `provider_first_with_gpu_fallback`.
- `KRK`.

Metrics include route accuracy, acceptable route rate, unsafe misroute rate, GPU false positives and negatives, cache correctness, fallback rate, and compute-weighted GPU demand.

## Evidence Report Output

A KRK evidence report should include:

- run identifier.
- workload profile.
- routing policy.
- route distribution.
- correctness metrics.
- fallback metrics.
- compute-weight formula version.
- reproducibility metadata.
- claim boundary.

Reports must exclude private paths, credentials, raw logs, server details, and raw private artifacts.

## Boundary With KORA Core Roadmap

KRK is not the full KORA Core surface.

KORA Core roadmap surfaces include:

- inspect.
- compare.
- run.
- report.
- doctor.
- Workload Spec.
- Target Registry.
- Evidence Report.
- adapters.
- developer preview.

Until implemented, these should be described as roadmap and not as working CLI commands.
