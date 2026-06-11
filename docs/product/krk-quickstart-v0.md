# KRK Quickstart v0

## What KRK Is

KRK means KORA Routing Kernel.

KRK is the deterministic-first execution routing kernel inside KORA Core. It routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

North star:

> Make AI workloads routable.

## What KRK Is Not

KRK is not a hosted gateway, cloud marketplace, production GPU service, provider replacement, or proof of production savings.

KRK is the first technical wedge for KORA Core. The current public alpha demonstrates local execution-control and benchmark evidence through existing KORA examples. It does not yet expose `route`, `explain`, `benchmark`, or `report` as top-level CLI commands.

## Deterministic-First Routing Principle

KRK starts from the question:

> Can this workload be resolved before default model execution?

Route preference should consider:

- deterministic work before inference.
- cache when reuse is valid.
- CPU when local execution is adequate.
- provider when model execution is appropriate.
- GPU when workload shape justifies GPU-class compute.
- fallback when policy, validation, or target availability requires it.

## Current Alpha Command Surface

Verified in this repo:

```bash
python3 -m kora --help
python3 -m kora examples list
python3 -m kora run hello_kora -- --offline
python3 -m kora run direct_vs_kora -- --offline
python3 -m kora run runtime_integrated_benchmark -- --offline
```

Current top-level commands:

- `examples`.
- `run`.
- `studio`.
- `telemetry`.

Roadmap KRK command surface:

- `route`.
- `explain`.
- `benchmark`.
- `report`.

These roadmap names describe the intended standalone KRK surface. They are not top-level commands on the current base.

## Expected Outputs

`python3 -m kora examples list` prints available runnable examples.

`python3 -m kora run hello_kora -- --offline` returns a simple deterministic JSON response.

`python3 -m kora run direct_vs_kora -- --offline` compares a direct model-first path with a KORA-controlled path using offline/mock behavior.

`python3 -m kora run runtime_integrated_benchmark -- --offline` emits bounded benchmark evidence for the deterministic-heavy workload.

## First 5-Minute Path

1. Check local Python:

```bash
python3 --version
```

2. Install the package in editable mode:

```bash
python3 -m pip install -e ".[dev]"
```

3. Inspect the CLI:

```bash
python3 -m kora --help
python3 -m kora examples list
```

4. Run the smallest deterministic example:

```bash
python3 -m kora run hello_kora -- --offline
```

5. Run the current benchmark evidence example:

```bash
python3 -m kora run runtime_integrated_benchmark -- --offline
```

## Limitations

- Top-level KRK commands are roadmap, not current CLI commands.
- H100 and GPU-class measurement is a bounded evidence path, not a service operation.
- Current examples use local/offline and mock paths unless explicitly configured otherwise.
- Benchmark outputs support bounded evidence only.

## Claim Boundary

Allowed:

- KRK is a deterministic-first routing kernel.
- KRK is the first technical wedge toward KORA Core.
- Current examples demonstrate local execution-control and bounded benchmark evidence.

Do not claim:

- production cost reduction.
- 10x savings.
- customer savings.
- infrastructure savings.
- broad workload superiority.
- H100 superiority.
- replacement of vLLM, OpenRouter, LiteLLM, OpenAI, Claude, Gemini, or other systems.

## Next Steps Toward KRK July 1 RC

- finalize the standalone KRK command vocabulary.
- decide whether to add top-level aliases for `route`, `explain`, `benchmark`, and `report`.
- connect the KRK extended matrix fixtures to a dry-run evaluator.
- generate the KRK performance table package.
- prepare public-safe release notes and claim boundaries.
