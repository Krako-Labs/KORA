# Goal 082A KORA Doctor Report Pack

Status: implemented.

## Base Condition

At implementation time, `origin/main` was still `b49617ce0402c3a73504ad3490dd668f0797891f` and did not contain the Goal 081A or Goal 082 files. This work used the completed local `goal082_kora_doctor_example` worktree/branch material as the confirmed-available base, then created a fresh scoped Goal 082A worktree.

## Scope

Goal 082A expands `examples/kora_doctor/` from a single offline workload into a Doctor Report Pack with multiple bundled workloads and aggregate report mode.

## Artifacts

- README: `examples/kora_doctor/README.md`
- runner: `examples/kora_doctor/run.py`
- default workload: `examples/kora_doctor/workload.json`
- additional workloads:
  - `examples/kora_doctor/workloads/customer_support_workload.json`
  - `examples/kora_doctor/workloads/developer_workflow_workload.json`
  - `examples/kora_doctor/workloads/document_intake_workload.json`
- expected counters:
  - `examples/kora_doctor/expected_counters.json`
  - `examples/kora_doctor/expected_counters_all.json`
- tests: `tests/test_kora_doctor_report_pack.py`

## Implementation Summary

The report pack keeps the Goal 082 execution path:

- every workload task is wrapped in a KORA `TaskGraph`.
- every graph runs through `run_graph()`.
- KORA Doctor uses the deterministic `doctor_inspect_task` executor handler.
- provider-needed candidates are identified, but provider/model calls are not performed.

`run.py` now supports:

- single-workload mode: `python3 examples/kora_doctor/run.py`
- custom workload mode: `python3 examples/kora_doctor/run.py --workload <path>`
- aggregate mode: `python3 examples/kora_doctor/run.py --all`
- JSON output via `--json-out`.
- markdown/text report output via `--report-md`.

## Evidence Counters

In these offline sample workloads, KORA Doctor identifies deterministic candidates and provider-needed candidates without making provider calls.

Aggregate report pack counters:

| Metric | Value |
| --- | ---: |
| Workload count | `4` |
| Total tasks | `25` |
| Deterministic candidates | `16` |
| Provider-needed candidates | `9` |
| Avoided simulated provider/model invocations | `16` |
| Provider calls actually made | `0` |

Per-workload counters:

| Workload | Total | Deterministic | Provider-needed | Provider calls |
| --- | ---: | ---: | ---: | ---: |
| `kora_doctor_sample_workload_v0` | `7` | `4` | `3` | `0` |
| `kora_doctor_customer_support_workload_v0` | `6` | `4` | `2` | `0` |
| `kora_doctor_developer_workflow_workload_v0` | `6` | `4` | `2` | `0` |
| `kora_doctor_document_intake_workload_v0` | `6` | `4` | `2` | `0` |

Suggested deterministic handlers across the pack:

- `cache_reuse`
- `classify_by_rules`
- `static_transform`

Provider/model fallback reasons across the pack:

- ambiguous semantic judgment
- open-ended generation
- ambiguous doctor signal: open-ended generation

## Validation Results

```bash
python3 examples/kora_doctor/run.py
```

Result: passed. The command exited `0` and printed the single-workload Doctor report with `7` total tasks, `4` deterministic candidates, `3` provider-needed candidates, and `0` provider calls actually made.

```bash
python3 examples/kora_doctor/run.py --all --json-out /tmp/kora_doctor_report_pack.json --report-md /tmp/kora_doctor_report_pack.md
```

Result: passed. The command exited `0`, wrote JSON and report outputs, and printed the aggregate report pack with `25` total tasks, `16` deterministic candidates, `9` provider-needed candidates, and `0` provider calls actually made.

```bash
python3 examples/kora_doctor/run.py --workload examples/kora_doctor/workloads/customer_support_workload.json
```

Result: passed. The command exited `0` and printed `6` total tasks, `4` deterministic candidates, `2` provider-needed candidates, and `0` provider calls actually made.

```bash
python3 examples/kora_doctor/run.py --workload examples/kora_doctor/workloads/developer_workflow_workload.json
```

Result: passed. The command exited `0` and printed `6` total tasks, `4` deterministic candidates, `2` provider-needed candidates, and `0` provider calls actually made.

```bash
python3 examples/kora_doctor/run.py --workload examples/kora_doctor/workloads/document_intake_workload.json
```

Result: passed. The command exited `0` and printed `6` total tasks, `4` deterministic candidates, `2` provider-needed candidates, and `0` provider calls actually made.

```bash
python3 -m pytest tests/test_kora_doctor_example.py tests/test_kora_doctor_report_pack.py
```

Result: passed, `13 passed`.

```bash
python3 -m pytest tests/test_first_value_cli.py tests/test_executor.py tests/test_deterministic_classification_expansion_pack.py tests/test_kora_doctor_example.py tests/test_kora_doctor_report_pack.py
```

Result: passed, `51 passed`.

```bash
python3 -m kora examples list
```

Result: passed. The output includes `kora_doctor: offline doctor-style workload inspection example`.

## Limitations

- The workloads are synthetic and small.
- The Doctor rules are deterministic examples, not production diagnostics.
- The report pack does not inspect arbitrary repositories.
- The report pack does not execute provider/model fallback.
- The report pack does not establish production proxy readiness.

## Claim Boundaries

This report pack does not claim production diagnostic accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, broad workload superiority, or production proxy readiness.

Supported narrow wording:

> In these offline sample workloads, KORA Doctor identifies deterministic candidates and provider-needed candidates without making provider calls.
