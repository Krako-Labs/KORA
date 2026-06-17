# KORA

Make AI workloads controllable.

KORA is an AI Workload Control Layer. It helps developers inspect work before sending it to a model, identify deterministic paths, preserve provider/model fallback for ambiguous work, and report what happened.

Many AI systems treat every task as a model problem. Many tasks are actually classification, validation, routing, policy, cache reuse, workflow control, or deterministic processing. KORA helps decide what should reach a model, what does not need a model, and how work should move through an AI system.

Current examples are offline and synthetic. They demonstrate KORA's routing/control surfaces, not production readiness, production cost reduction, benchmark superiority, or model replacement.

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

## What KORA Can Do Today

Current implemented surfaces include:

- List runnable examples: `python3 -m kora examples list`
- Run offline examples through the KORA example runner: `python3 -m kora run <example>`
- Run KORA Doctor sample workload inspection.
- Run the deterministic classification expansion pack.
- Run first-value CLI paths: `kora inspect`, `kora compare`, `kora run`, and `kora report`
- Execute deterministic sample tasks through KORA `TaskGraph` paths.
- Produce local JSON and Markdown/text reports from bundled examples.

These are first-value developer examples and bounded evidence paths. They are not production validation.

## Examples

Start here:

```bash
python3 -m kora examples list
python3 examples/kora_doctor/run.py
python3 examples/kora_doctor/run.py --all
python3 examples/deterministic_classification/run.py
```

The examples require no provider credentials and make no provider calls.

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

Run the Doctor report pack across bundled sample workloads:

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
