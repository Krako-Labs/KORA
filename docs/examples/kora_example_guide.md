# KORA Example Guide

This guide explains the flagship examples in KORA.

For a shorter list, see the root [README](../../README.md) or the [example catalog](../../examples/README.md).

## Recommended Order

1. **KORA Doctor** — inspect a workload and see route candidates.
2. **OpenAI-Compatible Proxy** — see OpenAI-style requests routed through KORA.
3. **Cache Reuse** — see repeated work routed to a cache path.
4. **RAG Routing** — see retrieval-needed work separated from provider-needed work.
5. **Agent Workflow Optimization** — see multi-step workflow routing.
6. **Deterministic Classification** — see rule-routed classification scenarios.

## Commands

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
python3 examples/cache_reuse/run.py
python3 examples/rag_routing/run.py
python3 examples/agent_workflow_optimization/run.py
python3 examples/deterministic_classification/run.py
```

## Interpreting the Examples

The examples use offline fixtures. They may report simulated avoided provider/model invocations, but they do not make provider calls and do not prove production savings.

Use them to understand the KORA routing model:

```text
workload -> route decision -> deterministic/cache/retrieval/tool/provider-needed path
```

## Where to Find Details

Each flagship example has its own README and report:

- [`examples/kora_doctor`](../../examples/kora_doctor/)
- [`examples/openai_compatible_proxy`](../../examples/openai_compatible_proxy/)
- [`examples/cache_reuse`](../../examples/cache_reuse/)
- [`examples/rag_routing`](../../examples/rag_routing/)
- [`examples/agent_workflow_optimization`](../../examples/agent_workflow_optimization/)
- [`examples/deterministic_classification`](../../examples/deterministic_classification/)
- [`docs/reports`](../reports/)

## Additional Example Groups

The public reviewer path should start with the flagship examples above. Other example directories are retained at their existing paths for continuity and reproducibility:

| Group | Directories |
| --- | --- |
| Basic / first-run examples | [`hello_kora`](../../examples/hello_kora/), [`direct_vs_kora`](../../examples/direct_vs_kora/), [`retry_demo`](../../examples/retry_demo/) |
| Validation / harness examples | [`customer_support_triage_fake_validation`](../../examples/customer_support_triage_fake_validation/), [`real_model_call_validation_fake`](../../examples/real_model_call_validation_fake/), [`real_workload_harness`](../../examples/real_workload_harness/), [`stress_test`](../../examples/stress_test/), [`workloads`](../../examples/workloads/) |
| Benchmark / evidence examples | [`runtime_integrated_benchmark`](../../examples/runtime_integrated_benchmark/) |

Paths are not being moved yet because example directories may be referenced by README commands, reports, tests, scripts, or external links. A future grouping pass should use link-preserving stubs or redirects before any directory move.
