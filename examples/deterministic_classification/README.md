# Deterministic Classification Example Pack

This example pack shows KORA routing synthetic classification tasks to deterministic handlers before provider/model fallback is needed. Every item runs through a KORA `TaskGraph` and the deterministic `classify_by_rules` handler.

Scenarios:

- support ticket routing
- issue triage
- incident severity routing
- document type routing
- log/event classification

## Quick Run

Run the full pack:

```bash
python3 examples/deterministic_classification/run.py
```

Write structured output and a Markdown evidence report:

```bash
python3 examples/deterministic_classification/run.py \
  --json-out /tmp/kora_goal081a_deterministic_classification_pack.json \
  --report-md /tmp/kora_goal081a_deterministic_classification_pack.md
```

Run through the KORA example runner:

```bash
python3 -m kora run deterministic_classification -- \
  --json-out /tmp/kora_goal081a_deterministic_classification_pack.json \
  --report-md /tmp/kora_goal081a_deterministic_classification_pack.md
```

Run one scenario:

```bash
python3 examples/deterministic_classification/run.py --scenario issue_triage
```

The original support-ticket scenario remains available:

```bash
python3 examples/deterministic_classification/run.py --scenario support_ticket_routing
```

## Aggregate Expected Counters

- total tasks: `32`
- deterministic routes: `21`
- provider-needed routes: `11`
- avoided provider invocations: `21`
- provider calls actually made: `0`

Expected counter files are in [expected_outputs](expected_outputs/).

## Narrow Claim

In this example pack, KORA routes `21` of `32` sample classification tasks to deterministic handlers, avoiding simulated provider/model invocation for those sample tasks.

This is a synthetic local example pack. It does not claim production cost reduction, real API-cost proof, benchmark superiority, broad workload superiority, or production validation.
