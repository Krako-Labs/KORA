# Cache Reuse Example

This offline example shows KORA identifying repeated or reusable work. It routes first-time deterministic sample requests through KORA `TaskGraph` execution, repeated exact or semantically equivalent sample requests to cache hits, and ambiguous/open-ended sample requests to provider-needed fallback.

It does not call external APIs and does not require provider credentials.

Current availability: run this example from a current `Krako-Labs/KORA` checkout installed from source. Plain `python3 -m pip install kora` installs a different PyPI project and should not be used for these examples. Future package distribution is planned as `getkora`, but this README does not claim that package is published.

## Quick Run

```bash
python3 examples/cache_reuse/run.py
```

Write structured JSON and a report:

```bash
python3 examples/cache_reuse/run.py \
  --json-out /tmp/kora_goal088_cache_reuse.json \
  --report-md /tmp/kora_goal088_cache_reuse.md
```

Run through the KORA example runner:

```bash
python3 -m kora run cache_reuse
```

## Expected Output

```text
KORA Cache Reuse Example

Total requests: 7
First-time deterministic handled: 3
Cache hits: 2
Provider-needed: 2
Avoided simulated provider/model invocations: 5
Provider calls actually made: 0
```

## Expected Counters

- total requests: `7`
- first-time deterministic handled: `3`
- cache hits: `2`
- provider-needed: `2`
- avoided simulated provider/model invocations: `5`
- provider calls actually made: `0`

Expected counters are in [expected_counters.json](expected_counters.json). Request fixtures are in [requests.json](requests.json).

## Claim Boundary

In this offline cache-reuse example, KORA routes repeated sample requests to cache hits without making provider calls and marks ambiguous/open-ended requests as provider-needed.

This example does not claim production cache correctness, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.
