# KRK Expanded Provider-Routed Validation v0

Status: expanded bounded provider-path measurement.

## Purpose

This document summarizes an expanded commercial LLM API routed validation for KRK-selected provider-path work. It strengthens the initial bounded provider-path evidence while preserving public/private and claim boundaries.

This is not a production benchmark, provider cost reduction claim, provider superiority claim, broad commercial LLM benchmark, or replacement claim.

## Sample Size

The expanded validation used the three provider-selected public matrix items as the source set and expanded them into a bounded synthetic validation set.

| Field | Value |
| --- | ---: |
| Source provider-selected items | 3 |
| Expanded variants per source item | 4 |
| Target live calls | 12 |
| Maximum allowed live calls for this goal | 20 |

## Live Calls

Live bounded provider calls were run.

The validation retained only aggregate metadata:

- sample count.
- success/failure counts.
- latency summary.
- input/output token or unit totals.
- error count.
- claim and public-boundary flags.

It did not commit raw prompts, raw provider responses, credentials, request IDs, account IDs, billing details, private endpoints, or operational notes.

## Sanitized Metrics

| Metric | Value |
| --- | ---: |
| Sample count | 12 |
| Success count | 12 |
| Failure count | 0 |
| Latency min, ms | 1418.283 |
| Latency median, ms | 2601.086 |
| Latency p95, ms | 5888.007 |
| Latency max, ms | 5888.007 |
| Input units/tokens total | 1102 |
| Output units/tokens total | 745 |
| Error count | 0 |

Generated summaries:

- [Generated expanded provider-routed validation JSON summary](generated/krk-expanded-provider-routed-validation-summary-v0.json)
- [Generated expanded provider-routed validation Markdown summary](generated/krk-expanded-provider-routed-validation-summary-v0.md)

## Comparison To Initial 3-Call Validation

| Evidence package | Sample count | Success count | Failure count | Latency median, ms | Input units/tokens total | Output units/tokens total | Claim level |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Initial bounded provider validation | 3 | 3 | 0 | 1583.670 | 176 | 156 | `bounded_provider_path_measured` |
| Expanded bounded provider validation | 12 | 12 | 0 | 2601.086 | 1102 | 745 | `expanded_bounded_provider_path_measured` |

The expanded validation increases the bounded sample size from 3 to 12 calls. It remains a public-safe provider-path validation, not a provider benchmark or production claim.

## Limitations

- The sample is still bounded and synthetic.
- The sample is derived from public provider-selected matrix items.
- Output quality validation is not included.
- The result should not be generalized to broad provider performance.
- The result should not be used for production, savings, provider superiority, or replacement claims.

## Claim Boundary

Allowed:

- KRK provider-routed path has expanded bounded provider validation evidence.
- Sanitized latency and token/unit metadata was collected for a bounded sample.

Not allowed:

- production cost reduction.
- provider cost reduction.
- 10x savings.
- customer savings.
- provider superiority.
- broad provider benchmark claims.
- replacement of commercial LLM APIs.

## Public/Private Boundary

The committed summary intentionally excludes credentials, tokens, account IDs, request IDs, private endpoints, raw prompts, raw provider responses, billing information, server details, local paths, and operational notes.

## Claim Level

`expanded_bounded_provider_path_measured`
