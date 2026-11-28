# Compare read-only lookup paths

This offline experiment compares a local directory lookup with an observation-only path, an experimental reuse path, and a plain dictionary cache with the same metadata. It measures actual calls to the synthetic directory and checks every returned answer against authored expectations.

It does **not** enable reuse in the KORA execution engine. Do not use the example as an authorization adapter or a production cache.

## Run the comparison

From the repository root, after an editable installation:

```bash
python -m examples.support_tier_activation.run --iterations 100 --output /tmp/support-tier-comparison.json
python -m pytest -q tests/test_support_tier_activation_example.py
```

The JSON report includes per-path operation counts, local elapsed times, first-iteration events and any answer mismatches. Timing depends on the host and does not include a network or model.

## Comparison paths

| Path | Behavior |
| --- | --- |
| Direct fixture | Calls the original directory for every request. |
| Manual router | Uses a fixed operation-to-tool mapping and the same directory. |
| KORA shadow | Uses the existing observation class; still calls the original handler every time. |
| Activation prototype | Checks authoritative metadata before deciding whether a cached response may be returned. |
| Equal-metadata cache | Uses a plain dictionary with the same validation guard and metadata. This control tests whether reuse alone explains the result. |

## Safety assumptions

All reads, grants and record changes are local to the fixture. The source owns a single serialization lock. Each record or grant write creates a new generation, even when a revision label is reused. The reuse path checks the subject, source, grant, expiry, generation and policy/resolver/prompt versions while holding the source lock. On an invalid or unavailable metadata probe it discards the candidate and uses the original handler. This is a deliberately narrow in-process contract. A remote source would need its own atomic authorization and version contract; an ordinary metadata fetch cannot establish that guarantee.

## Interpret the result

Count metadata probes as work. The fixture does not assign a price to them. A reduction in original-handler calls does not imply lower total cost or latency. The plain cache may achieve the same reduction. The direct and manual paths are controls, not measured historical LLM agents. No model is executed. The authored expectations are regression checks, not independent evaluation labels.

The example is a reproducible method for comparing these paths, not evidence of production savings or superiority.
