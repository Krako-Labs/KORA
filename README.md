# KORA

Make AI workloads controllable.

KORA is an AI Workload Control Layer. It helps developers inspect work before sending it to a model, identify deterministic paths, preserve provider/model fallback for ambiguous work, and report what happened.

Many AI systems treat every task as a model problem. Many tasks are actually classification, validation, routing, policy, cache reuse, workflow control, or deterministic processing. KORA helps decide what should reach a model, what does not need a model, and how work should move through an AI system.

Current examples are offline and synthetic. They demonstrate KORA's routing/control surfaces, not production readiness, production cost reduction, benchmark superiority, or model replacement.

## Current Availability

Use the current GitHub repository for the latest examples and CLI commands.

Do not use plain `python3 -m pip install kora` for this project. A packaging check on June 18, 2026 found that `kora` on PyPI is already occupied by an unrelated Colab utility package (`kora 0.9.20`). That package is not `Krako-Labs/KORA` and should not be used to test the KORA Doctor CLI.

Planned distribution strategy:

- Public brand: KORA.
- GitHub repository: `Krako-Labs/KORA`.
- Future PyPI distribution package: `getkora`.
- CLI command: `kora`.
- Python import package: `kora`.

`getkora` is the planned future distribution name; this README does not claim it is published. Until a package is published, install from the current repository:

```bash
git clone https://github.com/Krako-Labs/KORA.git
cd KORA

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .

python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora doctor --all examples/kora_doctor/
```

Use `python3 -m pip install -e ".[dev]"` when you also need test dependencies.

## What KORA Is

KORA sits between an AI request and provider/model execution.

It turns implicit work into explicit tasks and routes:

```text
request -> workload/task -> route decision -> deterministic handler or provider-needed fallback -> report
```

KORA does not try to make models smarter. It controls when, why, and how they are used.

## Why KORA Exists

Model-first systems often send too much work directly to inference. That makes it harder to see which parts of a workflow are:

- bounded classification.
- validation.
- routing.
- policy checks.
- cache reuse.
- static transforms.
- workflow control.
- open-ended generation or semantic judgment.

KORA makes these boundaries visible so developers can separate deterministic work from provider/model-needed work before building deeper integrations.

## AI Workload Control Layer

An AI Workload Control Layer is the part of an AI system that asks:

- What kind of work is this?
- Can it be handled deterministically?
- Should it use cache reuse or a static transform?
- Does it require provider/model fallback?
- What route was selected, and why?
- What evidence can be reported without overclaiming?

KORA currently demonstrates this with offline examples, deterministic handlers, KORA `TaskGraph` execution, route rationale, and bounded evidence reports.

Read more:

- [KORA Workload Control Layer vision](docs/vision/kora_workload_control_layer.md)
- [KORA Review Hub](REVIEW_HUB.md)
- [Open This First](OPEN_THIS_FIRST.md)
- [getkora distribution strategy](docs/packaging/getkora_distribution_strategy.md)

## What KORA Can Do Today

Current implemented surfaces in this GitHub repository include:

- List runnable examples: `python3 -m kora examples list`
- Run offline examples through the KORA example runner: `python3 -m kora run <example>`
- Run KORA Doctor sample workload inspection from the first-class CLI: `python3 -m kora doctor examples/kora_doctor/customer_support_workload.json`
- Run the reusable offline OpenAI-style proxy demo from the first-class CLI: `python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json`
- Run the offline agent workflow optimization example.
- Run the offline RAG routing example.
- Run the deterministic classification expansion pack.
- Run the offline OpenAI-compatible proxy example.
- Run first-value CLI paths: `kora inspect`, `kora compare`, `kora run`, `kora doctor`, `kora proxy-demo`, and `kora report`
- Execute deterministic sample tasks through KORA `TaskGraph` paths.
- Produce local JSON and Markdown/text reports from bundled examples.

These are first-value developer examples and bounded evidence paths. They are not production validation.

## Examples

After installing from the current repository, start here:

```bash
python3 -m kora examples list
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
python3 -m kora doctor --all examples/kora_doctor/
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
python3 examples/agent_workflow_optimization/run.py
python3 examples/rag_routing/run.py
python3 examples/openai_compatible_proxy/run.py
python3 examples/kora_doctor/run.py
python3 examples/kora_doctor/run.py --all
python3 examples/deterministic_classification/run.py
```

The examples require no provider credentials and make no provider calls.

### Agent Workflow Optimization

The agent workflow optimization example shows KORA controlling multi-step agent-style workflows. It routes classification, validation, static transform, and policy-check steps to deterministic handlers, repeated steps to cache reuse, explicit local action steps to tool-needed handling, and ambiguous planning or open-ended generation steps to provider-needed fallback.

Run the example:

```bash
python3 examples/agent_workflow_optimization/run.py
```

Expected counters:

- total workflow steps: `12`
- deterministic steps: `4`
- cache hits: `2`
- tool-needed steps: `3`
- provider-needed steps: `3`
- avoided simulated provider/model invocations: `6`
- provider calls actually made: `0`

Docs:

- [Agent workflow optimization example README](examples/agent_workflow_optimization/README.md)
- [Goal 087 agent workflow optimization example](docs/reports/goal087_agent_workflow_optimization_example.md)

### RAG Routing

The RAG routing example shows KORA controlling a retrieval-style workflow. It routes exact FAQ/policy queries to deterministic answers, repeated queries to cache reuse, document-grounded queries to retrieval-needed handling over an offline corpus, and ambiguous or open-ended generation queries to provider-needed fallback.

Run the example:

```bash
python3 examples/rag_routing/run.py
```

Expected counters:

- total queries: `7`
- deterministic answered: `2`
- cache hits: `1`
- retrieval-needed: `2`
- provider-needed: `2`
- avoided simulated provider/model invocations: `3`
- provider calls actually made: `0`

Docs:

- [RAG routing example README](examples/rag_routing/README.md)
- [Goal 086 RAG routing example](docs/reports/goal086_rag_routing_example.md)

### OpenAI-Compatible Proxy

The OpenAI-compatible proxy example shows KORA sitting in front of OpenAI-style chat request objects. It routes deterministic classification requests through reusable KORA proxy-demo logic and KORA `TaskGraph` execution, reuses a local cache for repeated sample requests, and marks ambiguous or open-ended sample requests as provider-needed.

Run the first-class CLI demo:

```bash
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
```

Run the example wrapper:

```bash
python3 examples/openai_compatible_proxy/run.py
```

Expected counters:

- total requests: `6`
- deterministic handled: `3`
- cache hits: `1`
- provider-needed: `2`
- avoided simulated provider/model invocations: `4`
- provider calls actually made: `0`

Docs:

- [OpenAI-compatible proxy example README](examples/openai_compatible_proxy/README.md)
- [Goal 084 OpenAI-compatible proxy example](docs/reports/goal084_openai_compatible_proxy_example.md)
- [Goal 085 OpenAI proxy reusable module and CLI](docs/reports/goal085_openai_proxy_reusable_module_cli.md)

### KORA Doctor

KORA Doctor inspects sample workloads and explains:

- deterministic candidates.
- provider-needed candidates.
- suggested deterministic handlers.
- provider/model fallback reasons.
- route rationale.
- next-step recommendations.
- provider calls actually made.

Run the default Doctor workload:

```bash
python3 examples/kora_doctor/run.py
```

Run a workload through the first-class CLI:

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
```

Run the Doctor report pack across bundled sample workloads:

```bash
python3 -m kora doctor --all examples/kora_doctor/
```

The example script remains available:

```bash
python3 examples/kora_doctor/run.py --all \
  --json-out /tmp/kora_doctor_report_pack.json \
  --report-md /tmp/kora_doctor_report_pack.md
```

Current Doctor report pack counters:

- workload count: `4`
- total tasks: `25`
- deterministic candidates: `16`
- provider-needed candidates: `9`
- avoided simulated provider/model invocations in these offline samples: `16`
- provider calls actually made: `0`

Docs:

- [KORA Doctor README](examples/kora_doctor/README.md)
- [Goal 082 KORA Doctor example](docs/reports/goal082_kora_doctor_example.md)
- [Goal 082A KORA Doctor report pack](docs/reports/goal082a_kora_doctor_report_pack.md)
- [Goal 083 KORA Doctor CLI](docs/reports/goal083_kora_doctor_cli.md)

### Deterministic Classification

The deterministic classification example pack shows KORA routing synthetic classification tasks through deterministic handlers while preserving provider-needed fallback cases.

Run the pack:

```bash
python3 examples/deterministic_classification/run.py
```

Run through the KORA example runner:

```bash
python3 -m kora run deterministic_classification
```

Current deterministic classification pack counters:

- total tasks: `32`
- deterministic routes: `21`
- provider-needed routes: `11`
- avoided simulated provider/model invocations in this example pack: `21`
- provider calls actually made: `0`

Scenarios:

- support ticket routing.
- issue triage.
- incident severity routing.
- document type routing.
- log/event classification.

Docs:

- [Deterministic classification example pack README](examples/deterministic_classification/README.md)
- [Goal 081A deterministic classification expansion pack](docs/reports/goal081a_deterministic_classification_expansion_pack.md)

## Evidence And Validation

KORA still includes KRK-oriented evidence and first-value reports. Current evidence is bounded and public-safe.

Key evidence and reports:

- [KORA five-minute first-value quickstart](docs/quickstart-five-minute-first-value.md)
- [getkora distribution strategy](docs/packaging/getkora_distribution_strategy.md)
- [KRK evidence package](docs/evidence/krk-evidence-package-v0.md)
- [KRK performance table](docs/evidence/krk-performance-table-v0.md)
- [KRK route-selectivity results](docs/evidence/krk-route-selectivity-results-v0.md)
- [KRK runtime-integrated route evaluation](docs/evidence/krk-runtime-integrated-route-evaluation-v0.md)
- [Goal 082A README refresh proposal](docs/reports/goal082a_readme_refresh_proposal.md)
- [Goal 082B narrative repositioning report](docs/reports/goal082b_narrative_repositioning.md)

## Safe Claim Boundaries

Supported narrow statements:

- KORA helps make AI workloads routable and controllable.
- KORA examples can identify deterministic candidates and provider-needed candidates in bundled offline sample workloads.
- KORA examples can execute deterministic sample tasks through KORA `TaskGraph` paths.
- KORA examples can preserve explicit provider-needed fallback cases while making zero provider calls.
- KORA Doctor and deterministic classification examples produce local reports over synthetic sample workloads.

Not claimed:

- production cost reduction proof.
- broad workload superiority.
- production readiness.
- benchmark superiority.
- automatic savings.
- model replacement.
- production diagnostic accuracy.
- real API-cost proof.
- production proxy readiness.

## Installation

KORA uses `pyproject.toml`-based Python packaging.

Packaged support is Python 3.11 or newer, as declared in `pyproject.toml`.

Installation paths:

- PyPI `kora`: do not use for this project; it is an unrelated package.
- Current latest features: clone `Krako-Labs/KORA` and install from the source checkout with `python3 -m pip install -e .`.
- Local development and tests: use `python3 -m pip install -e ".[dev]"`.
- Future package distribution: planned as `getkora`, with CLI command `kora`; do not use `python3 -m pip install getkora` unless a future release explicitly announces publication.

```bash
git clone https://github.com/Krako-Labs/KORA.git
cd KORA

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e ".[dev]"
```

Check the CLI:

```bash
python3 -m kora --help
python3 -m kora examples list
```

## First-Value CLI

The first-value CLI path runs over committed public fixtures and requires no provider credentials, no GPU, and no network access after dependencies are installed:

```bash
kora inspect
kora compare
kora run
kora report \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

Module form:

```bash
python3 -m kora inspect
python3 -m kora compare
python3 -m kora run
python3 -m kora report \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

Guide:

- [KORA five-minute first-value quickstart](docs/quickstart-five-minute-first-value.md)

## Roadmap

Near-term roadmap direction:

- continue improving examples as first-value onboarding.
- add reviewer walkthroughs for KORA Doctor and deterministic classification.
- keep public claims tied to checked fixtures and reports.
- expand workload-control docs without presenting future work as implemented.
- preserve explicit provider/model fallback boundaries.

Longer-term surfaces remain roadmap unless a command, example, or module is documented as implemented:

- richer doctor inspection.
- broader workload specs.
- target registries.
- adapter integrations.
- project-level reports.
- developer preview workflows.

## Documentation

- [Documentation index](docs/README.md)
- [KORA Workload Control Layer vision](docs/vision/kora_workload_control_layer.md)
- [Open This First](OPEN_THIS_FIRST.md)
- [Review Hub](REVIEW_HUB.md)
- [Claim registry](docs/claims/kora-claim-registry.md)
- [Public language guide](docs/claims/kora-public-language-guide.md)
