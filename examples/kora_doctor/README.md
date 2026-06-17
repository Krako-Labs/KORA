# KORA Doctor Example

This offline example shows how KORA can inspect small project-like workloads before deeper integration. It identifies deterministic candidates, provider-needed candidates, route rationale, summary counters, and next-step recommendations.

Current availability: run this example from a current `Krako-Labs/KORA` checkout installed from source. Plain `python3 -m pip install kora` installs a different PyPI project and should not be used to test `kora doctor`. Future package distribution is planned as `getkora`, but this README does not claim that package is published.

Recommended setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .
```

Run from the repository root:

```bash
python3 examples/kora_doctor/run.py
```

Run a workload through the first-class CLI:

```bash
python3 -m kora doctor examples/kora_doctor/customer_support_workload.json
```

Write structured JSON and a report:

```bash
python3 -m kora doctor examples/kora_doctor/workloads/customer_support_workload.json \
  --json-out /tmp/kora_doctor_customer_support.json \
  --report-md /tmp/kora_doctor_customer_support.md
```

The example script remains available:

```bash
python3 examples/kora_doctor/run.py \
  --json-out /tmp/kora_doctor_example.json \
  --report-md /tmp/kora_doctor_example.md
```

Run the full Doctor report pack across all bundled sample workloads:

```bash
python3 -m kora doctor --all examples/kora_doctor/
```

The example script remains available for the same report pack:

```bash
python3 examples/kora_doctor/run.py --all \
  --json-out /tmp/kora_doctor_report_pack.json \
  --report-md /tmp/kora_doctor_report_pack.md
```

Run through the KORA example runner:

```bash
python3 -m kora run kora_doctor
```

Expected counters:

- total tasks: `7`
- deterministic candidates: `4`
- provider-needed candidates: `3`
- avoided provider invocations in this example: `4`
- provider calls actually made: `0`

Report pack aggregate counters:

- workload count: `4`
- total tasks: `25`
- deterministic candidates: `16`
- provider-needed candidates: `9`
- avoided provider invocations in these offline samples: `16`
- provider calls actually made: `0`

The default sample workload is [workload.json](workload.json). Additional workloads live in [workloads](workloads/):

- `customer_support_workload.json`
- `developer_workflow_workload.json`
- `document_intake_workload.json`

Expected counters are in [expected_counters.json](expected_counters.json) and [expected_counters_all.json](expected_counters_all.json).

Claim boundary: In this offline CLI example, KORA Doctor identifies deterministic candidates and provider-needed candidates in sample workloads without making provider calls. This is a first-value developer report pack over synthetic data. It does not claim production diagnostic accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, broad workload superiority, or production proxy readiness.
