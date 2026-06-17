# KRK H100 Evidence Refresh v0

Status: public evidence readiness review. No H100 workload was run for this refresh.

## Purpose

This document inventories public KRK H100 and GPU-class evidence readiness for a narrowed July 1 KRK release-candidate package.

The review distinguishes:

- methodology that is already public.
- dry-run route-selectivity evidence that is already generated.
- bounded GPU-class measurement that is not yet included.

## Evidence Inventory

| Item | Exists? | Public? | Reproducible? | Sufficient for July 1? | Notes |
| --- | --- | --- | --- | --- | --- |
| KRK extended H100 test matrix methodology | Yes | Yes | Methodology only | Yes for methodology, no for measurement | Defines dry-run, bounded GPU-routed subset, and public reporting phases |
| KRK public evidence boundary | Yes | Yes | N/A | Yes | Defines public-safe fields, private-only fields, raw artifact handling, and prohibited claims |
| KRK performance table H100 section | Yes | Yes | N/A | Yes for explicit gap disclosure | States H100 bounded measurement values are not included in the current public package |
| KRK evidence package bounded GPU measurement section | Yes | Yes | N/A | Yes for explicit gap disclosure | States bounded GPU measurement is not included |
| KRK multi-profile route-selectivity results | Yes | Yes | Yes | Yes for narrowed RC | Evaluates route choice without provider calls or GPU execution |
| Bounded GPU-routed subset measurement result | No | No | No | Not required for narrowed RC | Required only if the RC wants to include measured GPU-class execution evidence |
| Public task count/runtime/throughput/memory table for KRK H100 subset | No | No | No | Not required for narrowed RC | Required only for a GPU-measurement claim level |

## Existing Public-Safe H100 Evidence

Current public-safe H100 material is methodology and boundary material, not measured KRK H100 execution evidence.

Existing public-safe support:

- the matrix defines when a bounded GPU-routed subset should be selected.
- the evidence boundary defines what public summaries may include.
- the performance table explicitly states that H100 bounded measurement is not included.
- the route-selectivity evaluator shows which fixture items KRK routes to GPU in dry-run mode.

## Bounded Measurement Evidence

No public KRK H100 bounded measurement table is included in the current package.

Missing measured fields:

- measured subset count.
- runtime summary.
- throughput summary.
- memory summary.
- sanitized measurement environment summary.
- reproducibility metadata for the measurement run.

## GPU-Routed Subset Methodology

The methodology is sufficient to define a future measurement:

1. run the public matrix evaluator.
2. select only requests routed to GPU by KRK.
3. execute a bounded measurement on that subset.
4. publish sanitized summaries only.
5. keep raw artifacts private unless separately reviewed and sanitized.

## Measurement Limitations

The current package cannot support statements about live GPU performance, H100 superiority, provider superiority, production readiness, broad workload behavior, or infrastructure outcomes.

## Public Summaries

The current public summary should say:

> KRK has public dry-run route-selectivity metrics and a defined bounded GPU-routed subset methodology. KRK H100 bounded measurement is not included in the current public package.

## July 1 Sufficiency

For a narrowed KRK July 1 RC, current evidence is sufficient if the RC scope is limited to:

- deterministic-heavy evidence.
- dry-run route-selectivity over four public matrix profiles.
- bounded H100 methodology and explicit gap disclosure.

For any RC that claims measured GPU-class execution evidence, current evidence is not sufficient.
