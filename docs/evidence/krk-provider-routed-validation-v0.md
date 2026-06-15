# KRK Provider-Routed Validation v0

Status: bounded provider-path measurement.

This document summarizes a small public-safe commercial LLM API validation for KRK-selected provider-path items from the public matrix fixtures.

## Purpose

KRK routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths. The route-selectivity evaluator identified a small provider-selected subset in the public matrix fixtures. This validation checks that the provider-routed path can complete bounded calls and emit sanitized aggregate measurement metadata.

This is not a production cost claim, provider benchmark, provider superiority claim, or replacement claim.

## Provider-Routed Path In KRK

The provider path is selected only when visible metadata and policy allow a commercial LLM API route. It is separate from deterministic, cache, CPU, GPU, and fallback paths.

The validation used only synthetic public fixture-derived prompts and retained only aggregate metadata:

- provider family.
- model family.
- sample count.
- success/failure counts.
- latency summary.
- input/output token or unit totals.
- claim and public-boundary flags.

## Bounded Validation Design

The bounded sample size was three provider-selected matrix items. The validation did not publish raw prompts, raw provider responses, credentials, request IDs, account IDs, billing details, private endpoints, or operational notes.

## Live Calls

Live bounded provider calls were run.

| Metric | Value |
| --- | ---: |
| Sample count | 3 |
| Success count | 3 |
| Failure count | 0 |
| Latency min, ms | 1581.517 |
| Latency median, ms | 1583.670 |
| Latency max, ms | 3635.988 |
| Input units/tokens total | 176 |
| Output units/tokens total | 156 |

Generated summaries:

- [Generated provider-routed validation JSON summary](generated/krk-provider-routed-validation-summary-v0.json)
- [Generated provider-routed validation Markdown summary](generated/krk-provider-routed-validation-summary-v0.md)

## Expanded Validation

The provider-routed path now also has an expanded bounded validation with 12 live commercial LLM API calls, 12 successes, 0 failures, sanitized latency metadata, and token/unit totals.

Reference:

- [KRK expanded provider-routed validation v0](krk-expanded-provider-routed-validation-v0.md)
- [Generated expanded provider-routed validation JSON summary](generated/krk-expanded-provider-routed-validation-summary-v0.json)
- [Generated expanded provider-routed validation Markdown summary](generated/krk-expanded-provider-routed-validation-summary-v0.md)

## What This Proves

This supports a bounded statement that KRK-selected provider-path items from the public matrix fixtures completed a small commercial LLM API validation and produced sanitized latency and token/unit metadata.

## What This Does Not Prove

This does not prove:

- production cost reduction.
- provider cost reduction.
- customer savings.
- provider superiority.
- broad provider benchmark performance.
- replacement of commercial LLM APIs.
- production readiness.

## Public Boundary

The committed summary intentionally excludes raw prompts, raw provider responses, credentials, request IDs, account IDs, billing details, private endpoints, server details, local paths, and operational notes.

## Claim Level

`bounded_provider_path_measured`
