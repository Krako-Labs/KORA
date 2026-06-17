# Goal 085 OpenAI Proxy Reusable Module and CLI

## Motivation

Goal 084 showed that KORA can sit in front of OpenAI-style sample requests and route deterministic or cacheable work without making provider calls. Goal 085 promotes that example-local logic into a reusable KORA-owned module and adds a first-class CLI command.

The purpose is reuse for later offline examples such as RAG routing, agent workflow control, cache reuse, and provider-needed fallback demonstrations. This remains an offline demo path, not a production proxy claim.

## User-Facing Walkthrough

Run the reusable CLI demo from a current source checkout:

```bash
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
```

Expected high-level output:

```text
KORA OpenAI Proxy Demo

Total requests: 6
Deterministic handled: 3
Cache hits: 1
Provider-needed: 2
Avoided simulated provider/model invocations: 4
Provider calls actually made: 0
```

The original example wrapper still works:

```bash
python3 examples/openai_compatible_proxy/run.py
```

Structured outputs are available from either path:

```bash
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json \
  --json-out /tmp/kora_goal085_openai_proxy_cli.json \
  --report-md /tmp/kora_goal085_openai_proxy_cli.md
```

## Implementation Summary

- Added `kora.openai_proxy_demo` as the reusable offline proxy demo module.
- Moved request loading, OpenAI-style message extraction, stable request cache keys, KORA `TaskGraph` construction, route execution, OpenAI-style response envelope generation, counter aggregation, JSON writing, and report rendering into the module.
- Kept `examples/openai_compatible_proxy/run.py` as a compatibility wrapper over the reusable module.
- Added `python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json`.
- Added tests for the reusable module and the CLI command.
- Updated README/docs and continuation breadcrumbs.

The reusable path still routes every non-cache request through KORA `TaskGraph` execution and the deterministic `classify_by_rules` handler. Cache hits reuse prior deterministic output without provider calls. Ambiguous/open-ended requests are marked provider-needed without external API calls.

## Command Examples

```bash
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json \
  --json-out /tmp/kora_goal085_openai_proxy_cli.json \
  --report-md /tmp/kora_goal085_openai_proxy_cli.md
python3 examples/openai_compatible_proxy/run.py
python3 -m kora run openai_compatible_proxy
```

## Evidence Counters

Using `examples/openai_compatible_proxy/requests.json`:

- total requests: `6`
- deterministic handled: `3`
- cache hits: `1`
- provider-needed: `2`
- avoided simulated provider/model invocations: `4`
- provider calls actually made: `0`

The counters are sample-fixture counters only.

## Validation Results

Final validation was run from the Goal 085 worktree:

```bash
python3 examples/openai_compatible_proxy/run.py
```

Result: passed. The command reported `Total requests: 6`, `Deterministic handled: 3`, `Cache hits: 1`, `Provider-needed: 2`, and `Provider calls actually made: 0`.

```bash
python3 -m kora proxy-demo examples/openai_compatible_proxy/requests.json
```

Result: passed. The command reported `KORA OpenAI Proxy Demo` with the same counters and `Provider calls actually made: 0`.

```bash
python3 -m kora examples list
```

Result: passed. The output includes `openai_compatible_proxy: offline OpenAI-style proxy routing example`.

```bash
python3 -m pytest tests/test_openai_proxy_demo_cli.py tests/test_openai_compatible_proxy_example.py tests/test_kora_doctor_cli.py tests/test_first_value_cli.py tests/test_deterministic_classification_expansion_pack.py
```

Result: passed with `36 passed in 15.43s`.

```bash
python3 scripts/check_markdown_links_goal082b.py
```

Result: passed with `Goal 082B markdown links OK`.

```bash
git diff --check
```

Result: passed with no output.

## Limitations

- The proxy demo accepts a small repository-owned OpenAI-style fixture format; it is not a full OpenAI API implementation.
- It does not start an HTTP server.
- It does not call OpenAI or any other external provider.
- Cache reuse is local to a single demo run.
- Route rules are synthetic and bounded to the sample requests.
- Provider-needed means "would require provider/model handling in a real system"; no provider invocation is made here.

## Claim Boundaries

Supported narrow wording:

> In this offline proxy demo, KORA routes deterministic or cacheable OpenAI-style sample requests without making provider calls and marks ambiguous/open-ended requests as provider-needed.

Not claimed:

- production proxy readiness.
- full OpenAI API compatibility.
- automatic cost reduction.
- real API-cost proof.
- benchmark superiority.
- broad workload superiority.
- production validation.
- model replacement.

## Recommended Next Goal

Goal 086 should refresh the public reviewer path around the example catalog and make the fastest first-run route explicit now that KORA has first-class `doctor` and `proxy-demo` CLI surfaces.
