# Goal 081A Deterministic Classification Expansion Pack

Status: implemented.

## Scope

Goal 081A expands the Goal 080 deterministic classification example into a reusable OSS example pack under `examples/deterministic_classification/`.

Base note: at implementation time, fetched `origin/main` was `b49617ce0402c3a73504ad3490dd668f0797891f` and did not yet contain the Goal 080 files. The completed local Goal 080 worktree was confirmed available, and the Goal 081A fresh worktree was created from `origin/main` with the Goal 080 support-ticket scenario preserved inside the new pack.

## KORA Execution Path

The pack uses KORA runtime execution for every sample item:

- each sample is wrapped in a `TaskGraph`.
- each graph executes through `run_graph()`.
- deterministic route selection is performed by the `classify_by_rules` deterministic handler registered in `kora.executor`.
- provider-needed cases are labeled for comparison but do not execute a provider/model call.

This avoids a disconnected standalone keyword demo while keeping the example local and public-safe.

## Scenarios

| Scenario | Dataset | Total | Deterministic | Provider-needed | Provider calls |
| --- | --- | ---: | ---: | ---: | ---: |
| support ticket routing | `examples/deterministic_classification/datasets/support_ticket_routing.json` | `8` | `5` | `3` | `0` |
| issue triage | `examples/deterministic_classification/datasets/issue_triage.json` | `6` | `4` | `2` | `0` |
| incident severity routing | `examples/deterministic_classification/datasets/incident_severity_routing.json` | `6` | `4` | `2` | `0` |
| document type routing | `examples/deterministic_classification/datasets/document_type_routing.json` | `6` | `4` | `2` | `0` |
| log/event classification | `examples/deterministic_classification/datasets/log_event_classification.json` | `6` | `4` | `2` | `0` |

## Aggregate Evidence Summary

In this example pack, KORA routes `21` of `32` sample classification tasks to deterministic handlers, avoiding simulated provider/model invocation for those sample tasks.

| Metric | Value |
| --- | ---: |
| Total tasks | `32` |
| Deterministic routes | `21` |
| Provider-needed routes | `11` |
| Avoided provider invocations | `21` |
| Provider calls actually made | `0` |

Expected counters are checked in under `examples/deterministic_classification/expected_outputs/`.

## Comparison Surface

The runnable output includes an aggregate `comparison` list across all scenarios. Each row includes:

- scenario id.
- input subject.
- selected route.
- route kind.
- classification category for deterministic cases.
- provider-call status.
- provider-needed reason for fallback cases.

## Claim Boundary

This example pack supports only narrow statements about the synthetic sample records in this repository. It does not claim production cost reduction, real API-cost proof, benchmark superiority, broad workload superiority, or production validation.

## Validation

```bash
python3 examples/deterministic_classification/run.py --json-out /tmp/kora_goal081a_deterministic_classification_pack.json --report-md /tmp/kora_goal081a_deterministic_classification_pack.md
```

Result: passed. The command exited `0`, wrote JSON and Markdown outputs, and reported `32` total tasks, `21` deterministic routes, `11` provider-needed routes, `21` avoided provider invocations, and `0` provider calls actually made.

```bash
python3 -m pytest tests/test_deterministic_classification_expansion_pack.py
```

Result: passed, `12 passed`.

```bash
python3 -m pytest tests/test_first_value_cli.py tests/test_executor.py tests/test_customer_support_triage_fake_validation.py tests/test_deterministic_classification_expansion_pack.py
```

Result: passed, `54 passed`.

```bash
python3 -m kora examples list
```

Result: passed. The output includes `deterministic_classification: deterministic classification example pack`.
