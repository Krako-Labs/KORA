# Roadmap

> Current orientation note:
> KORA is now presented publicly as an AI Workload Control Layer. This root roadmap is retained for continuity and may include earlier roadmap language. For the current public landing page, start with [README.md](README.md). For the current workload-control framing, see [docs/vision/kora_workload_control_layer.md](docs/vision/kora_workload_control_layer.md). For current examples, see [examples/README.md](examples/README.md).

This roadmap defines the practical evolution of KORA.

It is implementation-focused, not speculative.

---

## Current State - v0.1

KORA v0.1 includes:

- Task IR specification
- DAG-based execution
- Deterministic-first processing
- Budget governance
- Schema validation
- Reasoning adapter abstraction
- Telemetry instrumentation
- Break-even modeling
- Benchmark baseline

The architecture is structurally complete.

---

## v0.2 - Structural Refinement

Focus:

- Optimize structural overhead
- Improve deterministic coverage detection
- Improve DAG validation efficiency
- Strengthen telemetry performance
- Harden schema enforcement edge cases

Goals:

- Reduce O in break-even inequality
- Reduce latency variance
- Improve test coverage completeness

---

## v0.3 - Routing Intelligence

Focus:

- Policy-based routing engine
- Multi-model integration
- Cost-aware routing decisions
- Dynamic backend selection
- Escalation refinement

Goals:

- Reduce model-bound work
- Enable lightweight local reasoning
- Preserve compute neutrality

---

## v0.4 - Distributed Execution Prototype

Focus:

- Orchestrator-node protocol
- Node capability advertisement
- Failure isolation testing
- Telemetry aggregation across nodes
- Routing under partial failure

Goals:

- Demonstrate atomic distributed execution
- Validate failure containment
- Preserve invariants under distribution

---

## v0.5 - Structural Performance Validation

Focus:

- Large dataset benchmarking
- Latency distribution modeling
- Retry pattern analysis
- Overhead quantification at scale

Goals:

- Validate performance model predictions
- Refine break-even boundaries
- Publish empirical results

---

## v0.6 - DNFM Experimental Integration

Focus:

- Structured prompt segmentation experiments
- Task-scoped reasoning evaluation
- Budget-aware reasoning tests
- Model boundary isolation experiments

Goals:

- Evaluate feasibility of decomposition-native models
- Measure coherence under segmentation
- Publish experimental findings

---

## Long-Term Direction

If structural claims hold under scale:

- Distributed CPU cloud experimentation
- Edge-device participation
- Task-level compute marketplace
- Decomposition-native model collaboration

If structural claims fail:

- Refine decomposition granularity
- Optimize structural overhead
- Re-evaluate routing assumptions

Architecture must evolve under evidence.

---

## Invariants Across All Versions

The following must remain intact:

- Determinism before inference
- Budget as contract
- Schema validation enforcement
- Task atomicity
- Routing neutrality

Version upgrades must preserve these invariants.

---

## Closing Position

KORA evolves through disciplined iteration.

Each version must:

- Preserve structure
- Improve measurability
- Reduce hidden inference
- Strengthen architectural clarity

Structure is not negotiable.

Scale follows structure.
