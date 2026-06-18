# OpenAI-Compatible Proxy Example

This offline example shows KORA sitting in front of OpenAI-style chat request objects. It routes bounded classification requests through reusable KORA proxy-demo logic and KORA deterministic handlers, reuses a local cache for repeated requests, and marks ambiguous or open-ended requests as provider-needed without making external API calls.

Current availability: run this example from a current `Krako-Labs/KORA` checkout installed from source. Plain `python3 -m pip install kora` installs a different PyPI project and should not be used for these examples. Future package distribution is planned as `getkora`, but this README does not claim that package is published.

## Quick Run

Run the first-class CLI demo:

```bash
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
```

Run the example wrapper:

```bash
python3 examples/openai_compatible_proxy/run.py
```

Write structured JSON and a report:

```bash
python3 examples/openai_compatible_proxy/run.py \
  --json-out /tmp/kora_goal085_openai_proxy.json \
  --report-md /tmp/kora_goal085_openai_proxy.md
```

Write structured JSON and a report from the CLI:

```bash
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json \
  --json-out /tmp/kora_goal085_openai_proxy_cli.json \
  --report-md /tmp/kora_goal085_openai_proxy_cli.md
```

Run through the KORA example runner:

```bash
python3 -m kora run openai_compatible_proxy
```

## Expected Output

```text
KORA OpenAI-Compatible Proxy Example

Total requests: 6
Deterministic handled: 3
Cache hits: 1
Provider-needed: 2
Avoided simulated provider/model invocations: 4
Provider calls actually made: 0
```

## Expected Counters

- total requests: `6`
- deterministic handled: `3`
- cache hits: `1`
- provider-needed: `2`
- avoided simulated provider/model invocations: `4`
- provider calls actually made: `0`

Expected counters are in [expected_counters.json](expected_counters.json). OpenAI-style request fixtures are in [requests.json](requests.json).

The reusable proxy demo implementation lives in `kora.openai_proxy_demo`. The example script is a compatibility wrapper around that module.

## Claim Boundary

In this offline proxy demo, KORA routes deterministic or cacheable OpenAI-style sample requests without making provider calls and marks ambiguous/open-ended requests as provider-needed.

This example does not claim production proxy readiness, full OpenAI API compatibility, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.
