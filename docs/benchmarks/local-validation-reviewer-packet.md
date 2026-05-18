# Local No-Network Validation Reviewer Packet

## Purpose

This packet helps reviewers reproduce KORA's local/no-network validation path without API keys, external providers, private data, or network calls.

It is intended for technical review of the current validation plumbing: routing decisions, aggregate model-call counters, and Markdown report generation from synthetic workloads.

## What This Packet Shows

- A direct baseline records deterministic local validation adapter events for every request.
- A KORA-controlled path avoids model-call events for deterministic routes.
- The customer-support triage workload demonstrates an application-shaped synthetic workload.
- Markdown reports are generated from aggregate counters.

## What This Packet Does Not Show

This packet is not real provider validation, not real API-cost reduction evidence, not production validation, not production cost-reduction proof, not energy-reduction evidence, and not broad workload superiority proof.

This packet is not:

- real provider validation
- real API-cost reduction evidence
- production validation
- production cost-reduction proof
- energy-reduction evidence
- broad workload superiority proof

## Glossary

### Local no-network validation

Local no-network validation is a KORA validation mode that runs without external providers, API keys, private data, or network calls. It uses deterministic local validation paths to measure model-call routing behavior in synthetic workloads.

This mode is useful for testing KORA's routing, counters, reports, and validation flow before adding local model runtimes or real provider adapters.

## Prerequisites

- A Python environment that can run the KORA test suite and CLI.
- An editable install or local package setup if your environment does not already resolve `python3 -m kora`.
- No API keys required.
- No provider credentials required.
- No network access required for these validation examples.

## Quick Start Commands

```bash
python3 -m kora --help
python3 -m kora examples list

python3 -m kora run real_model_call_validation_fake -- --offline
python3 -m kora run customer_support_triage_fake_validation -- --offline
```

## No-Network Baseline Checklist

Run these commands from a fresh checkout of `origin/main` to reproduce the current local/no-network baseline pass:

```bash
python3 -m pytest
python3 -m kora --help
python3 -m kora examples list

python3 -m kora run direct_vs_kora -- --offline
python3 -m kora run runtime_integrated_benchmark -- --offline

python3 -m kora run real_model_call_validation_fake -- --offline --adapter local_validation
python3 -m kora run customer_support_triage_fake_validation -- --offline --adapter local_validation
python3 -m kora run real_model_call_validation_fake -- --offline --adapter local_runtime
python3 -m kora run customer_support_triage_fake_validation -- --offline --adapter local_runtime

python3 -m kora run customer_support_triage_fake_validation -- --offline --report-md /tmp/kora_customer_support_validation.md
```

Observed local/no-network baseline examples from the current reviewer pass:

| Command | Expected reviewer result |
|---|---:|
| `direct_vs_kora --offline` | direct calls `2`, KORA calls `1` |
| `runtime_integrated_benchmark --offline` | avoided simulated invocations `80/100` |
| `real_model_call_validation_fake --offline --adapter local_validation` | baseline `10`, KORA `4`, avoided `6` |
| `customer_support_triage_fake_validation --offline --adapter local_validation` | baseline `12`, KORA `4`, avoided `8` |

## Generate Reviewer Reports

```bash
python3 -m kora run real_model_call_validation_fake -- --offline --report-md /tmp/kora_local_validation.md

python3 -m kora run customer_support_triage_fake_validation -- --offline --report-md /tmp/kora_customer_support_validation.md

python3 -m kora run customer_support_triage_fake_validation -- --offline --adapter local_runtime --report-md /tmp/kora_customer_support_local_runtime.md
```

Reports are written only when `--report-md` is provided. Use `/tmp` or another local output path for generated artifacts unless a report is intentionally selected for review.

Generated reports are not committed by default. They contain aggregate counters and boundary language. They do not contain raw prompts, raw provider responses, secrets, or private data.

Generated local/no-network reports are organized to separate:

- report metadata, including report type, generated timestamp, adapter kind, provider label, model label, offline status, no-network status, and fail-closed status
- aggregate synthetic evidence, including baseline candidate events, KORA-routed model-call events, and avoided model-call events
- adapter-selection result, including the selected local/no-network adapter and labels
- provider fixture dry-run contract status, using aggregate metadata only
- safety boundaries, interpretation, and explicit non-claims

For successful local/no-network validation reports, provider fixture dry-run contract status is expected to show:

- `fixture_contract_status`: `passed`
- `mode`: `dry_run`
- `no_network`: `true`
- `no_provider_call`: `true`
- `contains_real_provider_response`: `false`
- `contains_customer_data`: `false`
- `contains_secret_material`: `false`
- `provider_attempted_events`: `0`

This contract status is a local dry-run report field. It is not a provider request, provider response, credential check, network call, or real-provider validation.

If fixture validation fails, report generation must stop rather than writing a misleading success report.

## Adapter Selection

The local validation examples default to the `local_validation` adapter.

```bash
python3 -m kora run real_model_call_validation_fake -- --offline --adapter local_validation
python3 -m kora run customer_support_triage_fake_validation -- --offline --adapter local_validation
```

The `local_runtime` adapter is an explicit opt-in local/no-network runtime stub. It uses deterministic in-process behavior, records the same aggregate counter shape as `local_validation`, and does not call local HTTP endpoints, subprocess runtimes, remote providers, provider APIs, or external model downloads.

```bash
python3 -m kora run real_model_call_validation_fake -- --offline --adapter local_runtime
python3 -m kora run customer_support_triage_fake_validation -- --offline --adapter local_runtime
```

The `blocked` and `local_runtime_placeholder` adapter kinds are fail-closed safety paths. `blocked` represents an unconfigured model-call path. `local_runtime_placeholder` is design-only, makes no runtime calls, and does not contact local HTTP endpoints, subprocess runtimes, remote providers, or provider APIs.

Fail-closed checks:

```bash
python3 -m kora run real_model_call_validation_fake -- --offline --adapter blocked
python3 -m kora run real_model_call_validation_fake -- --offline --adapter local_runtime_placeholder
python3 -m kora run customer_support_triage_fake_validation -- --offline --adapter blocked
python3 -m kora run customer_support_triage_fake_validation -- --offline --adapter local_runtime_placeholder
```

These commands are expected to exit non-zero. The `local_runtime_placeholder` path reports that no provider call was attempted. Reviewers should treat this as a safety check, not as a validation failure.

## Expected Generic Local Validation Counters

For `real_model_call_validation_fake`, expected counters are:

| Counter | Expected value |
|---|---:|
| `total_requests` | 10 |
| `baseline_model_calls` | 10 |
| `kora_model_calls` | 4 |
| `avoided_model_calls` | 6 |
| `avoided_model_call_rate` | 0.6 |
| `deterministic_routes` | 6 |
| `model_escalations` | 4 |

Expected labels:

- `provider`: `local_validation`
- `model`: `deterministic-local`

With explicit `--adapter local_runtime`, the expected counters are the same and the labels are:

- `provider`: `local_runtime`
- `model`: `deterministic-local-runtime`

## Expected Customer-Support Triage Counters

For `customer_support_triage_fake_validation`, expected counters are:

| Counter | Expected value |
|---|---:|
| `total_requests` | 12 |
| `baseline_model_calls` | 12 |
| `kora_model_calls` | 4 |
| `avoided_model_calls` | 8 |
| `avoided_model_call_rate` | 0.6667 |
| `deterministic_routes` | 8 |
| `model_escalations` | 4 |

Expected labels:

- `provider`: `local_validation`
- `model`: `deterministic-local`

With explicit `--adapter local_runtime`, the expected counters are the same and the labels are:

- `provider`: `local_runtime`
- `model`: `deterministic-local-runtime`

## How To Read The Counters

- `baseline_model_calls`: model-call events recorded by the direct baseline path.
- `kora_model_calls`: model-call events recorded by the KORA-controlled path.
- `avoided_model_calls`: `baseline_model_calls - kora_model_calls`.
- `avoided_model_call_rate`: `avoided_model_calls / baseline_model_calls`.
- `deterministic_routes`: requests handled through deterministic routing.
- `model_escalations`: requests routed to the deterministic local validation adapter.
- `validation_pass_count`: route or response checks that passed.
- `validation_fail_count`: route or response checks that failed.
- `error_count`: runtime errors counted during the example.
- `fallback_count`: requests that fell back because the route was unsupported or unresolved.

## Privacy And Artifact Handling

- Do not include secrets.
- Do not include API keys.
- Do not include private data.
- Do not include raw provider responses.
- Do not use real customer data.
- Do not use proprietary datasets.
- Review generated local reports before sharing them.

## Claim-Safe Language

Allowed:

> KORA's local no-network validation examples show that KORA can measure avoided model-call events in synthetic workloads.

Allowed:

> In the customer-support triage synthetic workload, the local validation path records 8 avoided model-call events out of 12 requests.

Not allowed:

- KORA reduces production AI costs by 66.7%.
- KORA reduces real API costs by 66.7%.
- KORA is production-proven for customer support.
- KORA reduces energy consumption.
- KORA has real provider validation from this packet.

Safe interpretation of this packet:

- The examples use synthetic workloads.
- The examples run local/no-network validation paths.
- The counters are model-call events or simulated invocations, depending on the command.
- The Markdown report path is a local review artifact unless explicitly selected for public review.

## Troubleshooting

- Command not found: confirm you are in the KORA repository and the package is importable with `python3 -m kora --help`.
- Editable install missing: install the project in editable mode if your environment does not resolve local modules.
- Report path not writable: use `/tmp` or another writable local directory.
- Stale checkout: run `git fetch origin` and confirm your local branch is current.
- Expected counters differ: confirm you are running with `--offline` and have not modified the synthetic workload files.

### Example is not listed

If an expected example does not appear when running:

```bash
python3 -m kora examples list
```

confirm that you are on the latest `main` branch and that your local checkout is up to date.

Recommended checks:

```bash
git status --short --branch
git pull
python3 -m kora examples list
```

If the example is still missing, include the command output when opening an issue.

## Next Validation Step

The next step after this packet is real provider adapter design, followed later by any implementation behind explicit opt-in, using the same reporting structure while preserving privacy and claim boundaries.

The reviewer packet commands still use local/no-network validation. The `local_runtime` adapter is an explicit deterministic in-process local/no-network stub. The `local_runtime_placeholder` adapter remains design-only and fail-closed for unsupported runtime paths.

See the [local model adapter design](local-model-adapter-design.md) for the next local runtime pathway after local/no-network validation.

See the [real provider adapter design](real-provider-adapter-design.md) for the future provider boundary. It is design-only and does not implement provider calls, credential handling, network calls, or provider dependencies.


## Validation Counter Glossary

- `baseline_model_calls`: The number of model-call events in the direct baseline path, where every request is sent to the model.
- `kora_model_calls`: The number of model-call events in the KORA-controlled path, after deterministic routes have been handled without escalation.
- `avoided_model_calls`: The difference between baseline model calls and KORA-controlled model calls.
- `avoided_model_call_rate`: The avoided model calls divided by the baseline model calls.
- `deterministic_routes`: Requests handled through deterministic, structured, or policy-driven paths without a model call.
- `model_escalations`: Requests that require model escalation because they cannot be safely resolved through deterministic paths.
- `validation_pass_count`: The number of routed requests that passed their expected validation checks.
- `validation_fail_count`: The number of routed requests that failed their expected validation checks.
- `error_count`: The number of requests that produced execution errors during validation.
- `fallback_count`: The number of requests that required fallback behavior after the primary route could not complete successfully.
