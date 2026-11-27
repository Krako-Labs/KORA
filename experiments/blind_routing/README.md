# Blinded support routing evaluation

Can a keyword route safely finish a request when one business fact changes? Run this offline evaluation from the repository root with the project dependencies installed. It sends each request through the public task-graph executor and the `classify_by_rules` handler. Deferral records a decision and stops there. The evaluation makes zero model calls.

## Run the development cases

```bash
python -m experiments.blind_routing.run
python -m experiments.blind_routing.run --rules experiments/blind_routing/tenant_rules.json
python -m experiments.blind_routing.run --rules experiments/blind_routing/freshness_rules.json
```

By default each command reports the eight development cases. After freezing a candidate, add `--split holdout` to each command to compare the other sixteen. Use `--split all` for regression testing. The fixtures and answer key are public, so future changes evaluated on these rows are same-set regressions. Add `--timing` to measure local graph decision time in nanoseconds. This excludes model service time.

## What the cases mean

The 24 authored requests form 12 pairs. Each pair stays in one split. Each of four families contributes one development pair and two holdout pairs. They are deliberately chosen challenges. Their frequencies describe this corpus.

| Family | Contract used for scoring |
| --- | --- |
| Tenant-specific status | A pending claim at Cedar goes to review. At Juniper it goes to the transfer queue. A missing or unknown tenant requires deferral. |
| Multiple intents | A single supported request can be fulfilled, including a copy of a payment confirmation as a receipt. A request with two independent actions requires deferral. |
| Ambiguous names | Atlas, Phoenix and Summit can name an account or a device. Direct the request to the relevant desk only when the entity type is known and supported. |
| Data freshness | For stock counts, billing addresses and support tiers, use a value when both dates are available and the requested date is on or before the validity deadline. Defer otherwise. |

`requests.json` contains the business text and context. `gold.json` contains the pair, split, family and expected action. A null action requires deferral. The runner sends the same graph and task IDs for every request. Only the text and structured business context enter the task input. Only the scorer sees the expected action. The baseline and tenant policies are retained for comparison. The hardened policy adds date requirements to three time-sensitive routes and scopes ambiguous entity aliases to the declared account/device context domain.

## Read the results

| Metric | Numerator | Denominator |
| --- | --- | --- |
| False bypass | Answered directly when the contract required deferral | All requests requiring deferral |
| Unnecessary escalation | Deferred when a direct answer was allowed | All requests with a direct answer |
| Wrong direct output | Produced the wrong action for a directly answerable request | Directly answerable requests actually answered directly |

Inspect the per-case expected action, returned output, selected route and fallback reason next to the counts. A correct deferral says nothing about the quality of a future model response. The original [100-task benchmark](../../docs/benchmarks/kora_benchmark_result_v1_100.md) measures a separate workload.

## Scoped keyword rules

A rule can require exact string values in the application's structured context.

```json
{
  "route_id": "review_queue",
  "keywords": ["pending"],
  "required_context": {"tenant": "Cedar"},
  "output": {"action": "review_queue"}
}
```

The caller supplies trusted context in the task input. Source tenant identity from the application's authenticated session if it affects routing. The handler compares strings case-sensitively. Missing context on a potential competitor withholds the decision. A known mismatch rules that competitor out. Multiple eligible rules also cause deferral. Scoped rules require nonempty keywords. Existing unscoped rules retain their keyword behavior.

For a scoped field with a closed set of supported values, `context_domains`
lists that set. A value outside the set is unresolved and causes deferral;
another known value in the set is an ordinary mismatch, allowing its competing
rule to match. Every domain field must exist in `required_context`, and the
required value must belong to its declared domain.

The tenant policy covers the tenant contract. Keyword matching still uses substrings, so a negated phrase or a word containing a configured keyword can match. A separate test is needed for each additional language or business constraint.

## Facts with validity dates

Set `"require_fresh_context": true` on a rule whose answer depends on a dated fact.
The application supplies the effective request date in `context.as_of` and the
fact's inclusive expiry date in `context.valid_until`. Supply both as trusted
calendar dates in `YYYY-MM-DD` form, for example `2028-02-29`. Replay uses
those dates without consulting the machine clock or interpreting request text.
The application is responsible for choosing the correct effective date and
checking that the expiry belongs to the fact being used.

A matching rule with missing, malformed or expired dates defers with a reason.
An overlapping keyword rule cannot return an answer while the applicable fact
is unusable. An exact tenant mismatch rules that candidate out before its dates
are checked. Existing rules without this requirement keep their behavior.
