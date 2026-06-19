# KORA Example Catalog

This directory contains runnable examples for KORA as an **AI Workload Control Layer**.

Start with the flagship examples below. They are offline, reproducible, and make zero provider calls.

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

Some directories in `examples/` are older validation, benchmark, or first-run examples. They remain available for reproducibility and project history, but the flagship examples above are the recommended starting point for new readers.

## Evidence Boundaries

These examples demonstrate offline sample workloads. They do not claim production readiness, real API-cost reduction, production cache correctness, production RAG correctness, autonomous agent reliability, or broad benchmark superiority.
