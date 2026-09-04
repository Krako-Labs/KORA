# KORA Example Catalog

This directory contains runnable examples for KORA as an **AI Workload Control Layer**.

Start with the flagship examples below. They are offline, reproducible, and make zero provider calls.

## Solution Protocol Fixtures

The [reference Solution guide](solutions/README.md) covers the hand-authored `hello-solution` and `document-transform-fixture` packages, the SDK-produced `generated-echo-fixture`, and the bounded `research-foundry-reference` migration. All four validate, install, and run through the same offline Host lifecycle and conformance entry point; the Research Foundry path additionally requires the optional `research` extra and an explicit local-write grant.

## Flagship Examples

| Example | What it demonstrates | Command |
| --- | --- | --- |
| [KORA Doctor](kora_doctor/) | Workload inspection and route-candidate reporting. | `python3 -m kora doctor examples/kora_doctor/customer_support_workload.json` |
| [Deterministic Classification](deterministic_classification/) | Rule-routed classification across practical scenarios. | `python3 examples/deterministic_classification/run.py` |
| [OpenAI-Compatible Proxy](openai_compatible_proxy/) | Offline OpenAI-style request routing through KORA. | `python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json` |
| [RAG Routing](rag_routing/) | Deterministic, cache, retrieval-needed, and provider-needed paths in a RAG-style workflow. | `python3 examples/rag_routing/run.py` |
| [Agent Workflow Optimization](agent_workflow_optimization/) | Multi-step workflow routing across deterministic, cache, tool-needed, and provider-needed paths. | `python3 examples/agent_workflow_optimization/run.py` |
| [Cache Reuse](cache_reuse/) | Repeated request reuse through an offline local cache path. | `python3 examples/cache_reuse/run.py` |

## Suggested Reviewer Path

Run these commands after installing from source:

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
python3 examples/cache_reuse/run.py
```

Then explore the remaining examples:

```bash
python3 examples/deterministic_classification/run.py
python3 examples/rag_routing/run.py
python3 examples/agent_workflow_optimization/run.py
```

## Additional Examples

The root `examples/` directory also contains older basic, validation, benchmark, and fixture examples. They remain in place for continuity and reproducibility. New readers should start with the flagship examples above.

## Workload Representativeness Seed

- [KORA representativeness seed fixture v0](workloads/kora-representativeness-seed-v0.json) broadens public-safe synthetic workload category coverage for future evaluation design.

This seed is fixture-design support only. It does not run providers, run H100 workloads, prove production workload handling, prove output quality, or prove broad workload superiority.

## Directory Map

| Group | Directories | Purpose |
| --- | --- | --- |
| Flagship examples | `kora_doctor`, `deterministic_classification`, `openai_compatible_proxy`, `rag_routing`, `agent_workflow_optimization`, `cache_reuse` | Current public first-value examples. |
| Basic / first-run examples | `hello_kora`, `direct_vs_kora`, `retry_demo` | Smaller examples for minimal graph execution, direct comparison, and retry behavior. |
| Validation / harness examples | `customer_support_triage_fake_validation`, `real_model_call_validation_fake`, `real_workload_harness`, `stress_test`, `workloads` | Validation fixtures, harnesses, representativeness seeds, stress runs, and workload data retained for project history and reproducibility. |
| Benchmark / evidence examples | `runtime_integrated_benchmark` | Benchmark-oriented evidence path retained outside the flagship reviewer path. |

Paths are not being moved in this pass. Future grouping should use link-preserving stubs or redirects so existing documentation, scripts, and external links do not break.

## Evidence Boundaries

These examples demonstrate offline sample workloads. They do not claim production readiness, real API-cost reduction, production cache correctness, production RAG correctness, autonomous agent reliability, or broad benchmark superiority.
