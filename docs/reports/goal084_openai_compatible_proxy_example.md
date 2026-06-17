# Goal 084 OpenAI-Compatible Proxy Example

## Motivation

Goal 084 adds a concrete offline example showing how KORA can sit in front of OpenAI-style provider requests and route deterministic or cacheable work before a model call would be needed.

The purpose is developer comprehension: show an insertion point for KORA in an OpenAI-style workflow without claiming production proxy readiness or full API compatibility.

## User-Facing Walkthrough

Run:

```bash
python3 examples/openai_compatible_proxy/run.py
```

Write structured output:

```bash
python3 examples/openai_compatible_proxy/run.py \
  --json-out /tmp/kora_goal084_openai_proxy.json \
  --report-md /tmp/kora_goal084_openai_proxy.md
```

Expected report header:

```text
KORA OpenAI-Compatible Proxy Example

Total requests: 6
Deterministic handled: 3
Cache hits: 1
Provider-needed: 2
Avoided simulated provider/model invocations: 4
Provider calls actually made: 0
```

## Implementation Summary

- Added `examples/openai_compatible_proxy/`.
- Added synthetic OpenAI-style chat request fixtures in `requests.json`.
- Added expected counters in `expected_counters.json`.
- Added `run.py` that extracts chat request text, routes through KORA `TaskGraph` execution with `classify_by_rules`, caches repeated deterministic responses, and labels ambiguous/open-ended requests as provider-needed.
- Added focused tests in `tests/test_openai_compatible_proxy_example.py`.
- Updated example listing metadata so `python3 -m kora examples list` includes `openai_compatible_proxy`.
- Updated README, docs index, `OPEN_THIS_FIRST.md`, and `REVIEW_HUB.md`.

The example stays offline and makes no external API calls.

## Request And Route Examples

Example OpenAI-style request:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "Classify support tickets into bounded routing categories."
    },
    {
      "role": "user",
      "content": "Classify this ticket: Customer was charged twice"
    }
  ],
  "temperature": 0
}
```

Route result:

- route: `deterministic`.
- handler: `classify_by_rules`.
- selected route: `proxy.det.support.billing`.
- provider calls: `0`.

Repeated request result:

- route: `cache_hit`.
- handler: `cache_reuse`.
- provider calls: `0`.

Open-ended request result:

- route: `provider_required`.
- handler: `provider_needed_fallback`.
- provider calls actually made: `0`.

## Evidence Counters

- total requests: `6`
- deterministic handled: `3`
- cache hits: `1`
- provider-needed: `2`
- avoided simulated provider/model invocations: `4`
- provider calls actually made: `0`

## Validation Results

```bash
python3 examples/openai_compatible_proxy/run.py
```

Result: passed.

```bash
python3 examples/openai_compatible_proxy/run.py --json-out /tmp/kora_goal084_openai_proxy.json --report-md /tmp/kora_goal084_openai_proxy.md
```

Result: passed. JSON output reported `ok=True`, `6` total requests, `3` deterministic handled, `1` cache hit, `2` provider-needed, and `0` provider calls actually made. Markdown report was written.

```bash
python3 -m kora examples list
```

Result: passed. Output included `openai_compatible_proxy: offline OpenAI-style proxy routing example`.

```bash
python3 -m pytest tests/test_openai_compatible_proxy_example.py tests/test_kora_doctor_cli.py tests/test_first_value_cli.py
```

Result: passed as part of the relevant test set:

```bash
python3 -m pytest tests/test_openai_compatible_proxy_example.py tests/test_kora_doctor_cli.py tests/test_first_value_cli.py tests/test_deterministic_classification_expansion_pack.py
```

The run completed with `31 passed in 6.00s`.

```bash
python3 scripts/check_markdown_links_goal082b.py
git diff --check
```

Result: markdown link validation passed with `Goal 082B markdown links OK`; `git diff --check` passed.

## Limitations

- This is an offline example, not a production proxy.
- It simulates only a narrow OpenAI-style chat request shape.
- It does not claim full OpenAI API compatibility.
- It does not make provider calls.
- Avoided provider/model invocations are simulated counters for this sample workload only.

## Claim Boundaries

Supported wording:

> In this offline OpenAI-style proxy example, KORA routes deterministic or cacheable sample requests without making provider calls and marks ambiguous/open-ended requests as provider-needed.

Not claimed:

- production proxy readiness.
- full OpenAI API compatibility.
- automatic cost reduction.
- real API-cost proof.
- benchmark superiority.
- broad workload superiority.

## Recommended Next Goal

Run a public reviewer walkthrough and example catalog refresh that compares the KORA Doctor, deterministic classification, and OpenAI-compatible proxy examples as first-run onboarding paths.
