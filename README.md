# KORA

Control AI workloads before they reach a model.

KORA is an AI Workload Control Layer. It helps identify deterministic work, reusable work, retrieval-needed work, tool-needed work, and provider-needed work before unnecessary model invocation.

Many AI systems treat every task as a model problem. KORA makes the route explicit: what can run deterministically, what can reuse local context, what needs retrieval or tools, and what should fall back to a provider/model path.

Current examples are offline and synthetic. They demonstrate KORA's routing and control surfaces, not production readiness, production cost reduction, benchmark superiority, or model replacement.

![KORA Workload Control Layer Architecture](docs/assets/kora_workload_control_layer_architecture.svg)

View the architecture diagram: [docs/assets/kora_workload_control_layer_architecture.svg](docs/assets/kora_workload_control_layer_architecture.svg)

## What KORA Does

- Inspects workloads before model/provider execution.
- Routes bounded classification, validation, policy, and transform work to deterministic handlers.
- Reuses cached work where the example workload makes that route explicit.
- Separates retrieval-needed and tool-needed paths from provider-needed fallback.
- Marks ambiguous or open-ended work as provider-needed instead of hiding the fallback.
- Reports route decisions and example outcomes without requiring provider credentials.

## When KORA Helps

KORA is useful when an AI workflow mixes different kinds of work:

- repeatable classification or routing decisions.
- validation, policy checks, or static transforms.
- repeated requests that can be treated as cache candidates.
- document-grounded work that should be separated as retrieval-needed.
- workflow steps that need local tools instead of direct model generation.
- ambiguous or open-ended work that should remain provider/model-needed.

The goal is not to remove models from the system. The goal is to make model use intentional and visible.

## Quick Start From Source

Use the current GitHub repository for the latest examples and CLI commands.

Package note: `python3 -m pip install kora` is not this project. The PyPI name `kora` is occupied by an unrelated package. KORA's planned future PyPI distribution name is `getkora`, but `getkora` is not published yet. Until a package is published, install from source:

```bash
git clone https://github.com/Krako-Labs/KORA.git
cd KORA

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .

python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora examples list
```

The first command produces an offline KORA Doctor report for a bundled sample workload. The second command lists runnable examples available in the repository.

For local development and tests:

```bash
python3 -m pip install -e ".[dev]"
```

## Flagship Examples

All examples below run offline and require no provider credentials.

| Example | What it shows | Command | Read more |
| --- | --- | --- | --- |
| KORA Doctor | Inspects a sample workload and explains deterministic versus provider-needed candidates. | `python3 -m kora doctor examples/kora_doctor/customer_support_workload.json` | [README](examples/kora_doctor/README.md) |
| Deterministic Classification | Routes synthetic classification tasks through deterministic handlers while preserving provider-needed cases. | `python3 examples/deterministic_classification/run.py` | [README](examples/deterministic_classification/README.md) |
| OpenAI-Compatible Proxy Demo | Routes OpenAI-style sample request objects through deterministic handling, cache reuse, or provider-needed fallback. | `python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json` | [README](examples/openai_compatible_proxy/README.md) |
| RAG Routing | Separates deterministic answers, cache reuse, retrieval-needed handling, and provider-needed fallback over an offline corpus. | `python3 examples/rag_routing/run.py` | [README](examples/rag_routing/README.md) |
| Agent Workflow Optimization | Routes workflow steps across deterministic, cache, tool-needed, and provider-needed paths. | `python3 examples/agent_workflow_optimization/run.py` | [README](examples/agent_workflow_optimization/README.md) |
| Cache Reuse | Routes repeated sample requests to cache hits while keeping ambiguous requests provider-needed. | `python3 examples/cache_reuse/run.py` | [README](examples/cache_reuse/README.md) |

Detailed counters and expected outputs live in the example READMEs and reports, not in this landing page.

To see the full runnable example list:

```bash
python3 -m kora examples list
```

## How It Works

KORA sits between workload input and provider/model execution:

```text
request/workload
  -> route decision
  -> deterministic, cache, retrieval-needed, tool-needed, or provider-needed path
  -> report
```

In the current examples:

- deterministic, cache, retrieval-needed, and tool-needed routes run locally where the example defines them.
- provider-needed work is marked explicitly.
- examples make zero provider calls.
- reports keep route decisions visible for review.

That means the examples are safe to run as local demonstrations. They are not a substitute for validating a production workload, integration, or provider configuration.

## What Stays Explicit

KORA examples keep routing decisions visible instead of treating the whole workflow as one opaque model call.

The current public examples preserve these distinctions:

- deterministic: handled by bounded local logic in the example.
- cache: treated as reusable work in the example.
- retrieval-needed: separated for document-grounded handling.
- tool-needed: separated for local action or tool handling.
- provider-needed: marked as fallback for ambiguous or open-ended work.

This is the control-layer boundary KORA is demonstrating today.

## Evidence And Claim Boundaries

Supported narrow statements:

- KORA helps make AI workloads routable and controllable.
- Current examples run over offline sample workloads.
- Current examples can mark deterministic, cache, retrieval-needed, tool-needed, and provider-needed paths.
- Current examples make zero provider calls.
- Example reports may describe simulated provider/model invocation avoidance in those bundled samples.

Not claimed:

- production readiness.
- production cost reduction proof or real API-cost reduction proof.
- benchmark superiority.
- full OpenAI API compatibility.
- production RAG, agent, proxy, diagnostic, or cache correctness.
- model replacement.

See also:

- [Claim registry](docs/claims/kora-claim-registry.md)
- [Public language guide](docs/claims/kora-public-language-guide.md)
- [KRK evidence package](docs/evidence/krk-evidence-package-v0.md)

## Documentation

Start here:

- [Documentation index](docs/README.md)
- [KORA Workload Control Layer vision](docs/vision/kora_workload_control_layer.md)

Use the documentation index for longer installation notes, evidence links, roadmap context, and maintainer-facing material that no longer belongs in the README landing page.

For a first pass, read the vision page, run KORA Doctor, then inspect the example catalog.

Examples:

- `python3 -m kora examples list`
- [KORA Doctor README](examples/kora_doctor/README.md)
- [Deterministic Classification README](examples/deterministic_classification/README.md)
- [OpenAI-Compatible Proxy README](examples/openai_compatible_proxy/README.md)
- [RAG Routing README](examples/rag_routing/README.md)
- [Agent Workflow Optimization README](examples/agent_workflow_optimization/README.md)
- [Cache Reuse README](examples/cache_reuse/README.md)

Project:

- [Packaging strategy](docs/packaging/getkora_distribution_strategy.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Roadmap](ROADMAP.md)
- [Open This First](OPEN_THIS_FIRST.md)
- [Review Hub](REVIEW_HUB.md)

The maintainer-facing files remain linked for continuity, but the README no longer uses them as the primary visitor path.

## License

KORA is released under the [MIT License](LICENSE).

See the license file for full terms.
