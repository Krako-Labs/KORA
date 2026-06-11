# KORA Routing Kernel Definition v0

## Definition

KRK means KORA Routing Kernel.

KRK is the deterministic-first execution routing kernel inside KORA Core. Its job is to select and explain an execution path before a workload turns into a default model call.

## Execution Paths

KRK evaluates execution paths such as:

- deterministic.
- cache.
- CPU.
- provider.
- GPU.
- fallback.

The path list is intentionally implementation-facing. A workload may begin with deterministic checks, reuse safe cached outputs, use CPU-local execution, call an external provider, select a GPU-backed target, or fall back when the preferred path is unavailable or unsafe.

## Current Alpha Mapping

The current public alpha maps existing behavior and examples to KRK primitives:

- `route`: select a route for a workload request.
- `explain`: show why a route was selected.
- `benchmark`: compare bounded workloads and routes.
- `report`: generate reviewable evidence.

These primitives are the first building block for KORA Core. They do not yet imply a complete production execution platform.

On the current base, these primitive names are not exposed as top-level CLI commands. Verified top-level commands are `examples`, `run`, `studio`, and `telemetry`. Standalone KRK aliases or commands remain roadmap until implemented and tested.

## GPU And H100 Benchmark Boundary

KRK benchmarks when GPU or H100-backed execution should be used, not raw GPU usage. The routing question is whether the workload justifies a GPU target compared with deterministic, cache, CPU, provider, or fallback paths.

Public evidence should focus on path selectivity, reproducibility, and methodology. Raw private artifacts and resource details should stay out of public docs.

## Inside KORA Core

KRK is not separate from KORA Core. It is the routing kernel inside KORA Core and should eventually feed higher-level inspect, compare, run, and report workflows.

## Allowed Claims

Allowed:

- KRK is a deterministic-first execution routing kernel.
- KRK evaluates deterministic, cache, CPU, provider, GPU, and fallback paths.
- The current alpha documents route, explain, benchmark, and report as KRK primitives.
- KRK can produce bounded routing and benchmark evidence.

Prohibited:

- production cost reduction proof.
- 10x savings.
- broad workload superiority.
- customer savings.
- infrastructure savings.
- replacement of vLLM, OpenRouter, LiteLLM, OpenAI, Claude, Gemini, or other systems.
- H100 superiority claims.
