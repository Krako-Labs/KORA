# Goal 083 KORA Doctor CLI

## Motivation

Goal 083 promotes the offline KORA Doctor example into a first-class CLI command. The example already showed how KORA can inspect sample workloads and identify deterministic candidates and provider-needed candidates through KORA `TaskGraph` execution. The CLI makes that developer experience available directly as `kora doctor`.

## User-Facing Walkthrough

Run a single workload-control report:

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
```

Run the aggregate report pack across bundled Doctor workloads:

```bash
python3 -m kora doctor --all examples/kora_doctor/
```

Write structured output:

```bash
python3 -m kora doctor examples/kora_doctor/workloads/customer_support_workload.json \
  --json-out /tmp/kora_doctor_customer_support.json \
  --report-md /tmp/kora_doctor_customer_support.md
```

The CLI output includes:

- workload name.
- total tasks.
- deterministic candidates.
- provider-needed candidates.
- suggested deterministic handlers.
- provider/model fallback reasons.
- avoided simulated provider/model invocations.
- provider calls actually made: `0`.

## Implementation Summary

- Added a first-class `doctor` subcommand to `kora/cli.py`.
- Reused the existing KORA Doctor implementation from `examples/kora_doctor/run.py`.
- Preserved the example script path for compatibility.
- Added aggregate-directory support to the Doctor summary builder.
- Added report output lines for workload identity and avoided simulated provider/model invocations.
- Added focused CLI tests in `tests/test_kora_doctor_cli.py`.
- Updated README, docs index, KORA Doctor README, `OPEN_THIS_FIRST.md`, and `REVIEW_HUB.md`.

The command stays offline and does not call external APIs.

## Command Examples

Single workload:

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
```

Aggregate workloads:

```bash
python3 -m kora doctor --all examples/kora_doctor/
```

Example catalog:

```bash
python3 -m kora examples list
```

## Validation Results

Validation was run from the Goal 083 worktree:

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
```

Result: passed. Output reported `kora_doctor_customer_support_workload_v0`, `6` total tasks, `4` deterministic candidates, `2` provider-needed candidates, `4` avoided simulated provider/model invocations, and `0` provider calls actually made.

```bash
python3 -m kora doctor --all examples/kora_doctor/
```

Result: passed. Output reported `4` workloads, `25` total tasks, `16` deterministic candidates, `9` provider-needed candidates, `16` avoided simulated provider/model invocations, and `0` provider calls actually made.

```bash
python3 -m kora examples list
```

Result: passed. Output included `kora_doctor: offline doctor-style workload inspection example`.

```bash
python3 -m pytest tests/test_kora_doctor_cli.py tests/test_first_value_cli.py tests/test_executor.py tests/test_kora_doctor_example.py tests/test_kora_doctor_report_pack.py
```

Result: passed, `43 passed in 6.55s`.

## Limitations

- The CLI currently operates over the bundled offline Doctor workload format.
- The workload examples are synthetic.
- Provider-needed routes are reported as recommendations; no provider calls are made.
- The CLI is not a production diagnostic system.

## Claim Boundaries

Supported narrow wording:

> In this offline CLI example, KORA Doctor identifies deterministic candidates and provider-needed candidates in sample workloads without making provider calls.

Not claimed:

- production diagnostic accuracy.
- automatic cost reduction.
- real API-cost proof.
- benchmark superiority.
- broad workload superiority.
- model replacement.

## Recommended Next Goal

Add `kora doctor --json-out` usage to a lightweight onboarding quickstart and define the minimal external workload schema expected by third-party users.
