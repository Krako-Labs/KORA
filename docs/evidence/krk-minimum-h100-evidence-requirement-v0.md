# KRK Minimum H100 Evidence Requirement v0

Status: minimum evidence definition for July 1 decision-making.

## Question

What is the smallest H100 evidence package required to support a KRK July 1 RC?

## Answer

For a narrowed KRK July 1 RC, no new H100 execution is required. The minimum requirement is explicit boundary disclosure:

- H100 bounded measurement is not included.
- GPU-routed subset methodology is defined.
- dry-run route-selectivity evidence exists.
- no live GPU-class performance claim is made.

For an RC that includes measured GPU-class execution evidence, a small bounded H100 subset package is required.

## Minimum Measurement If Path B Is Chosen

If measured H100 evidence is required, the smallest acceptable package should include:

- one public matrix profile or a clearly defined GPU-routed subset.
- selected subset count.
- fixed public commit.
- fixed evaluator policy version.
- sanitized runtime summary.
- sanitized throughput summary.
- sanitized memory summary.
- artifact boundary statement.
- exact claim level.

## Minimum Reporting

A public report should include:

- profile name.
- subset selection rule.
- item count.
- public-safe command or reproduction description.
- result table.
- limitations.
- public/private boundary.
- claim boundary.

## Minimum Reproducibility

Reproducibility should include:

- public repo commit.
- fixture file.
- evaluator policy version.
- metric formula version.
- measurement command or command template.
- statement that raw logs and private resource details are excluded from public output.

## Minimum Public-Safe Summary

Approved summary shape:

> KRK selected a bounded GPU-routed subset from public matrix fixtures and reported sanitized measurement summaries for that subset.

This wording is only allowed after a measured subset package exists.

## Explicitly Not Required For Narrowed RC

The narrowed KRK July 1 RC does not require:

- live H100 execution.
- provider calls.
- raw GPU logs.
- production deployment evidence.
- broad workload coverage.
- infrastructure outcome claims.
- provider or GPU superiority claims.

## Recommendation

Use the narrowed RC without new H100 execution. Keep H100 measured evidence as the next optional evidence layer unless the owner decides the July 1 package must include a measured GPU-class subset.
