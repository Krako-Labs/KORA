# KORA Core

Make AI workloads routable.

Docker made applications portable.
KORA makes AI workloads routable.

KORA Core is an open-source AI workload execution layer.

The current alpha focuses on deterministic-first workload routing and evidence reporting through the KORA Routing Kernel.

![KORA execution control overview](docs/assets/kora-execution-control-overview.png)

## Current Alpha

The current public implementation is a KRK-oriented alpha. KRK means KORA Routing Kernel: a deterministic-first execution routing kernel inside KORA Core.

Current alpha primitives:

- `route`: select a workload route.
- `explain`: explain the routing decision.
- `benchmark`: compare bounded workload behavior.
- `report`: produce evidence for review.

These are KRK alpha primitives, not top-level CLI commands on the current base. The verified local CLI currently exposes `examples`, `run`, `studio`, and `telemetry`.

KRK standalone docs:

- [KRK quickstart](docs/product/krk-quickstart-v0.md)
- [KRK architecture](docs/architecture/krk-architecture-v0.md)
- [KRK capability matrix](docs/evidence/krk-capability-matrix-v0.md)
- [KRK July 1 release-candidate checklist](docs/product/krk-july1-release-candidate-v0.md)

KRK evidence:

- [KRK capability matrix](docs/evidence/krk-capability-matrix-v0.md)
- [KRK performance table](docs/evidence/krk-performance-table-v0.md)
- [KRK evidence package](docs/evidence/krk-evidence-package-v0.md)
- [KRK reproducibility matrix](docs/evidence/krk-reproducibility-matrix-v0.md)
- [KRK claim boundary table](docs/evidence/krk-claim-boundary-table-v0.md)

KORA still starts from the same execution-control idea:

```text
request -> prompt -> model -> output
```

After:

```text
request -> task graph -> deterministic path -> validation -> model escalation -> telemetry
```

Structure first. Inference second.

## Roadmap

KORA Core is planned to expand beyond the current KRK alpha into a broader AI workload execution layer:

- inspect.
- compare.
- run.
- report.
- doctor.
- Workload Spec.
- Target Registry.
- Evidence Report.
- adapters.
- examples.
- developer preview.

These are roadmap surfaces unless a command or module is documented as implemented.

KORA Core alpha surface docs:

- [KORA Core alpha surface](docs/product/kora-core-alpha-surface-v0.md)
- [KORA Core user workflow](docs/product/kora-core-user-workflow-v0.md)
- [Inspect definition](docs/product/kora-core-inspect-definition-v0.md)
- [Compare definition](docs/product/kora-core-compare-definition-v0.md)
- [Run definition](docs/product/kora-core-run-definition-v0.md)
- [Report definition](docs/product/kora-core-report-definition-v0.md)

## Prerequisites

KORA uses `pyproject.toml`-based Python packaging.

- Packaged support: Python 3.11 or newer, as declared in `pyproject.toml`.
- Observed local result: Python 3.9.6 has been confirmed to run the offline `direct_vs_kora` example in one user environment.
- Treat Python 3.9.6 as an observed troubleshooting datapoint, not as the advertised package support floor until clean Python 3.9 compatibility testing is completed.
- Before making Python-version compatibility assumptions, check the active interpreter with `python3 --version`.
- VS Code's selected interpreter may differ from terminal `python3`; make sure both point to the intended environment when debugging setup issues.
- Upgrade `pip`, `setuptools`, and `wheel` before editable install so local tooling understands modern `pyproject.toml` builds.

Check your local tools first:

```bash
python3 --version
python3 -m pip --version
which python3
```

## 3-Minute Local Run

For local development in this repository:

```bash
python3 --version

rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e ".[dev]"
```

If editable install reports that `setup.py`, `setup.cfg`, or install metadata is missing, first verify that your checkout is current:

```bash
git remote -v
git fetch origin
git checkout main
git pull origin main
ls pyproject.toml
```

If `pyproject.toml` is still missing after pulling, re-clone from `https://github.com/Krako-Labs/KORA.git`.

Run the CLI and first offline demo:

```bash
python3 -m kora --help
python3 -m kora examples list
python3 -m kora run hello_kora -- --offline
python3 -m kora run direct_vs_kora -- --offline
```

Inspect the output to see how KORA changes a direct model-first path into a controlled execution path.

## Five-Minute First Value

For the shortest current path from fresh clone to a public-safe KORA result, run:

```bash
python3 scripts/kora_five_minute_demo.py \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

This one-command workflow shows inspect, compare, run, and report steps over committed public KRK fixtures. It requires no provider credentials, no GPU, and no network access.

Guide:

- [KORA five-minute first-value quickstart](docs/quickstart-five-minute-first-value.md)

## Local Setup Troubleshooting

If first-run setup fails after a system restart, Python upgrade, VS Code interpreter change, or virtual environment change, start by collecting the active environment:

```bash
python3 --version
python3 -m pip --version
python3 -m pip show pydantic
which python3
```

### `TypeError: unsupported operand type(s) for |: 'ModelMetaclass' and 'ModelMetaclass'`

This usually indicates a local Python, virtual environment, `pip`, `setuptools`, or dependency compatibility problem. Python 3.9.6 has been observed to run the offline `direct_vs_kora` example in one user environment, but packaged support is currently Python 3.11 or newer. First rebuild the local environment with current build tooling:

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e ".[dev]"
python3 -m kora run hello_kora -- --offline
python3 -m kora run direct_vs_kora -- --offline
```

Do not assume this error means a newer Python version is unsupported. Test Python 3.9, 3.10, 3.11, or 3.12 in clean environments before changing the package support floor.

### Editable install says `setup.py` or `setup.cfg` is missing

KORA uses `pyproject.toml`-based packaging, so a missing `setup.py` or `setup.cfg` message usually means the local `pip`/build tooling is too old or the virtual environment is stale. Confirm `pyproject.toml` exists, upgrade build tooling, then reinstall:

```bash
ls pyproject.toml
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e ".[dev]"
```

### VS Code interpreter differs from terminal `python3`

If KORA works in Terminal but fails in VS Code, compare the selected VS Code interpreter against terminal `python3`:

```bash
which python3
python3 --version
python3 -m pip --version
```

Select the repository `.venv` interpreter in VS Code, then reopen the terminal or restart the Python language server before rerunning the examples.

## What KORA Does

KORA sits between an AI request and a model call.

It helps developers:

- turn requests into explicit task graphs
- run deterministic work before inference
- validate outputs before escalation
- make model calls conditional instead of default
- record telemetry around each execution path
- compare direct model-first execution against controlled execution

KORA does not try to make models smarter. It controls when, why, and how they are used.

## Current Alpha Evidence

In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

![KORA benchmark evidence card](docs/assets/kora-benchmark-evidence-card.png)

This result is based on the current deterministic-heavy alpha benchmark and should not be interpreted as a universal production cost-reduction claim.

For methodology, counters, artifact policy, and reproduction commands, see:

- [Runtime evidence reviewer guide](docs/reports/v0.3.0-alpha-runtime-evidence-reviewer-guide.md)
- [Benchmark artifact policy](docs/reports/benchmark_artifact_policy.md)
- [Benchmark result summary](docs/benchmarks/kora_benchmark_result_v1_100.md)
- [KRK performance table](docs/evidence/krk-performance-table-v0.md)
- [KRK July 1 evidence summary](docs/reports/krk-july1-evidence-summary-v0.md)
- [Claim registry](docs/claims/kora-claim-registry.md)
- [Validation roadmap](docs/benchmarks/validation-roadmap.md)

## What We Are Testing Next

1. Runtime-integrated benchmark paths with real model calls
2. [Customer-support triage workloads](docs/workloads/customer-support-triage.md)
3. RAG answer-routing workloads
4. Agent budget-guard workloads

We are looking for early developers and AI app teams who want to test KORA against real workloads.

![KORA validation roadmap](docs/assets/kora-validation-roadmap.png)

KORA validation roadmap.

See the [KORA validation roadmap](docs/benchmarks/validation-roadmap.md) for the measurement plan.

See the [real model-call validation design](docs/benchmarks/real-model-call-validation-design.md) for the next measurement path.

KORA includes a local no-network validation path that measures model-call routing without requiring API keys or external providers.

Customer-support triage local validation is available as a no-network example.

Local no-network validation examples can generate Markdown reports with `--report-md`.

Local no-network validation examples support `--adapter local_validation` by default and explicit `--adapter local_runtime` for the deterministic in-process local runtime stub.

Reviewer packet: [local no-network validation](docs/benchmarks/local-validation-reviewer-packet.md).

The reviewer packet includes the no-network baseline checklist, adapter-selection commands, fail-closed safety checks, and local Markdown report generation examples.

Local model adapter design: [provider-neutral local runtime path](docs/benchmarks/local-model-adapter-design.md).

Real provider adapter design-only packet: [future provider boundary](docs/benchmarks/real-provider-adapter-design.md).

Real provider test harness design-only packet: [dry-run provider validation contract](docs/benchmarks/real-provider-test-harness-design.md).

## Help Test KORA

Good candidate workloads:

- customer-support triage
- repetitive RAG workflows
- agent workflows with budget or escalation rules
- deterministic-heavy backend workflows
- LLM apps with high repeated request patterns

To participate, follow the [contact and discussion routes](docs/community/contact-and-discussion-routes.md).

To contribute code or docs without write access to this repository, use the [fork-based pull request workflow](CONTRIBUTING.md#fork-workflow-for-external-contributors). Direct write access is not required to contribute through pull requests.

![KORA help-test flow](docs/assets/kora-help-test-flow.png)

How to help test KORA with a real workload.

See [Help Test KORA](docs/community/help-test-kora.md) for the workload submission template.

> When proposing workloads for KORA validation, use only synthetic or sanitized examples. Do not include secrets, API keys, private user data, proprietary datasets, raw provider responses, or production logs.

## Documentation

Start with the [KORA Documentation Index](docs/README.md) for the developer path:

- Start
- Understand
- Run
- Inspect evidence
- Help test
- Contribute

Useful entry points:

- [Examples directory](examples/)
- [Telemetry and observability counters](docs/telemetry-and-observability.md)
- [Public language guide](docs/claims/kora-public-language-guide.md)
- [KORA Studio planning docs](docs/kora-studio/README.md)
- [Contact and discussion routes](docs/community/contact-and-discussion-routes.md)
- [Community manager guide](docs/community/KORA_COMMUNITY_MANAGER_GUIDE.md)
- [Contributing guide](CONTRIBUTING.md)

For branch naming, pushing your work, and opening a pull request into `main`, see the [branch and PR workflow](CONTRIBUTING.md#branch-and-pr-workflow).

For support-channel problems or bugs, start with a reproducible report using the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) before attempting a code change.

## Install

Target package install path:

```bash
pip install kora
```

Homebrew install path:

```bash
brew install kora
```

For the current repository alpha, use the editable local install in the [3-Minute Local Run](#3-minute-local-run).

## Current Examples

Current examples available in this repository:

- `examples/hello_kora`
- `examples/direct_vs_kora`
- `examples/retry_demo`
- `examples/real_workload_harness`
- `examples/stress_test`
- `examples/runtime_integrated_benchmark`

Use `--offline` for reproducible first-run paths without OpenAI credentials.

## 📚 Resources

### KORA Guide Series

| Guide    | Topic                                                          |
| -------- | -------------------------------------------------------------- |
| Guide #1 | Introducing KORA: Open-Source AI Orchestration for Task Graphs |
| Guide #2 | Coming Soon                                                    |
| Guide #3 | Coming Soon                                                    |

### Latest Article

👉 Introducing KORA: Open-Source AI Orchestration for Task Graphs

https://dev.to/krakoteam/introducing-kora-open-source-ai-orchestration-for-task-graphs-10o9


## Alpha Scope

Included in the alpha surface:

- execution-layer primitives for structured AI workloads
- task graph and scheduler foundations
- deterministic-first execution and verification components
- telemetry summarization and reporting
- repository examples covering direct-vs-structured execution, retries, stress behavior, and runtime evidence flow
- terminal-first developer workflow

Not included in the alpha surface:

- GUI-first product
- chatbot interface
- desktop AI app
- model hosting or model serving engine
- production cost-reduction proof
- real API-cost reduction proof
- energy reduction evidence

## What KORA Is Not

KORA is not:

- a chatbot
- a desktop AI app (not yet)
- a hosted chat-product alternative
- a model serving engine
- another agent wrapper that only forwards prompts to providers

KORA is a standalone open-source execution-control layer for AI workloads.

## Contribute

Want to contribute? Start with:

- [Contributor pathway](docs/community/contributor-pathway.md)
- [Contact and discussion routes](docs/community/contact-and-discussion-routes.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [Good first issue candidates](docs/good_first_issues.md)
- [SECURITY.md](SECURITY.md)
- [GOVERNANCE.md](GOVERNANCE.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Ecosystem

KORA is part of the broader Krako infrastructure.

Related repository:

- Krako 2.0: TBD

## License

Apache-2.0. See [LICENSE](LICENSE).
