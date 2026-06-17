# Goal 082 KORA Doctor Example

Status: implemented.

## Motivation

KORA Doctor is a first-value developer example. It shows what KORA can reveal before a developer integrates deeply: which sample workload tasks look deterministic, which should stay provider/model fallback candidates, and why.

This is not a production diagnostic claim. It is an offline synthetic example that demonstrates inspection shape, route rationale, counters, and next-step recommendations.

## User-Facing Walkthrough

Run from the repository root:

```bash
python3 examples/kora_doctor/run.py
```

Expected report shape:

```text
KORA Doctor Example

Total tasks: 7
Deterministic candidates: 4
Provider-needed candidates: 3
Suggested deterministic handlers:
- cache_reuse
- classify_by_rules
- static_transform

Provider/model fallback recommended for:
- ambiguous semantic judgment
- open-ended generation
- ambiguous doctor signal: open-ended generation

Provider calls actually made: 0
```

Structured output:

```bash
python3 examples/kora_doctor/run.py \
  --json-out /tmp/kora_doctor_example.json \
  --report-md /tmp/kora_doctor_example.md
```

KORA example runner:

```bash
python3 -m kora run kora_doctor
```

## Implementation Summary

Artifacts:

- README: `examples/kora_doctor/README.md`
- runnable example: `examples/kora_doctor/run.py`
- sample workload: `examples/kora_doctor/workload.json`
- expected counters: `examples/kora_doctor/expected_counters.json`
- tests: `tests/test_kora_doctor_example.py`

The example uses KORA runtime execution:

- each sample workload task is wrapped in a KORA `TaskGraph`.
- each graph runs through `run_graph()`.
- the deterministic `doctor_inspect_task` handler in `kora.executor` returns route kind, selected route, rationale, next step, and provider-call count.
- provider-needed candidates are identified without making provider/model calls.

## Evidence Counters

In this offline example, KORA Doctor identifies deterministic candidates and provider-needed candidates in a sample workload without making provider calls.

| Metric | Value |
| --- | ---: |
| Total tasks | `7` |
| Deterministic candidates | `4` |
| Provider-needed candidates | `3` |
| Avoided provider invocations | `4` |
| Provider calls actually made | `0` |

Suggested deterministic handlers:

- `classify_by_rules`
- `cache_reuse`
- `static_transform`

Provider/model fallback recommended for:

- ambiguous semantic judgment
- open-ended generation
- ambiguous doctor signal: open-ended generation

## Validation Results

```bash
python3 examples/kora_doctor/run.py
```

Result: passed. The command exited `0` and printed the KORA Doctor report with `7` total tasks, `4` deterministic candidates, `3` provider-needed candidates, and `0` provider calls actually made.

```bash
python3 examples/kora_doctor/run.py --json-out /tmp/kora_doctor_example.json --report-md /tmp/kora_doctor_example.md
```

Result: passed. The command exited `0` and wrote structured JSON plus report output.

```bash
python3 -m pytest tests/test_kora_doctor_example.py
```

Result: passed, `8 passed`.

```bash
python3 -m pytest tests/test_first_value_cli.py tests/test_executor.py tests/test_deterministic_classification_expansion_pack.py tests/test_kora_doctor_example.py
```

Result: passed, `46 passed`.

```bash
python3 -m kora examples list
```

Result: passed. The output includes `kora_doctor: offline doctor-style workload inspection example`.

## Limitations

- The workload is synthetic and small.
- The doctor rules are deterministic examples, not learned diagnostics.
- The example does not inspect arbitrary repositories.
- Provider-needed candidates are labeled, but no provider/model fallback is executed.
- The example does not measure production behavior, production quality, or production cost.

## Claim Boundaries

This example does not claim production diagnostic accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.

Supported narrow wording:

> In this offline example, KORA Doctor identifies deterministic candidates and provider-needed candidates in a sample workload without making provider calls.

## Recommended Next Examples

- KORA Doctor for a local fixture directory with JSON workload files.
- KORA Doctor report export with machine-readable route recommendations.
- KORA Doctor plus deterministic classification pack walkthrough.
- KORA Doctor comparison between direct provider-candidate workflow and KORA-routed workflow.
