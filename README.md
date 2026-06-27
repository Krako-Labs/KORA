# KORA

**Control AI workloads before they reach a model.**

KORA is an **AI Workload Control Layer**. It helps route deterministic, reusable, retrieval-needed, tool-needed, and provider-needed work before unnecessary model invocation.

Most AI systems treat every task as a model task. KORA starts one step earlier: it inspects the workload, chooses a route, and makes provider-needed work explicit.

![KORA Workload Control Layer Architecture](docs/assets/kora_workload_control_layer_architecture.svg)

[View the architecture diagram](docs/assets/kora_workload_control_layer_architecture.svg)

## What KORA Does

- Inspect workloads before deployment.
- Route deterministic work without provider calls.
- Reuse repeated work through cache paths.
- Separate retrieval-needed and tool-needed work.
- Mark provider-needed tasks explicitly.

## Quick Start

Current latest-feature use is from source:

```bash
git clone https://github.com/Krako-Labs/KORA.git
cd KORA
python3 -m pip install -e .
```

Run the first-value paths:

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
python3 examples/cache_reuse/run.py
```

## Package Availability

`pip install kora` is **not** this project.

The planned future PyPI package name is `getkora`, with CLI command `kora` and Python import package `kora`.

`getkora` is not published yet. Use the source install path above for the latest KORA features.

## Flagship Examples

| Example | Shows | Run | Details |
| --- | --- | --- | --- |
| KORA Doctor | Workload inspection | `python3 -m kora doctor examples/kora_doctor/customer_support_workload.json` | [README](examples/kora_doctor/README.md) |
| Deterministic Classification | Rule-routed classification | `python3 examples/deterministic_classification/run.py` | [README](examples/deterministic_classification/README.md) |
| OpenAI-Compatible Proxy | OpenAI-style request routing | `python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json` | [README](examples/openai_compatible_proxy/README.md) |
| RAG Routing | Retrieval-aware control | `python3 examples/rag_routing/run.py` | [README](examples/rag_routing/README.md) |
| Agent Workflow Optimization | Multi-step workflow routing | `python3 examples/agent_workflow_optimization/run.py` | [README](examples/agent_workflow_optimization/README.md) |
| Cache Reuse | Repeated-work reuse | `python3 examples/cache_reuse/run.py` | [README](examples/cache_reuse/README.md) |

See the full [example catalog](examples/README.md).

## How It Works

A workload enters KORA before it reaches a model.

KORA evaluates each unit of work and routes it to one of several paths:

- deterministic handling
- cache reuse
- retrieval-needed handling
- tool-needed handling
- provider-needed fallback

The included examples are offline and make zero provider calls.

## Evidence Boundaries

KORA ships offline sample workloads (simulated provider/model invocation avoidance) **and** one real, measured benchmark on a single synthetic domain: deterministic front-door routing across 5 models (Qwen2.5-32B, Claude Sonnet 4.6, Claude Haiku 4.5, Llama 3.3 70B, Llama 3.1 8B), giving an identical **76.7% deflection** (LLM calls 330 → 77). The routing result reproduces with no API key, no GPU, and zero LLM calls. See [experiments/kora_target_workload](experiments/kora_target_workload/README.md).

The repository does **not** claim:

- production cost reduction proof
- real API-cost reduction proof beyond the single-domain benchmark above
- production readiness
- benchmark superiority
- full OpenAI API compatibility
- production RAG, agent, or cache correctness
- model replacement

See the [claim registry](docs/claims/kora-claim-registry.md) and [public language guide](docs/claims/kora-public-language-guide.md).

## Documentation

- [Documentation index](docs/README.md)
- [Vision: AI Workload Control Layer](docs/vision/kora_workload_control_layer.md)
- [Example catalog](examples/README.md)
- [Packaging: getkora strategy](docs/packaging/getkora_distribution_strategy.md)
- [Reports and evidence](docs/reports/)
- [Contributing](CONTRIBUTING.md)

## License

MIT License. See [LICENSE](LICENSE).
