# Add KRK route-selectivity evidence, first-value CLI, and review packet

## Summary

This PR packages the KRK evidence and first-value work on `goal044_krk_route_selectivity_metrics_plan` for public review.

It adds route-selectivity evaluation, bounded provider/H100 evidence, output-fidelity evaluation, an official first-value CLI surface, install validation, and a durable project breadcrumb/review layer.

## What Changed

- Added KRK route-selectivity metrics evaluator and four public profile summaries.
- Added runtime-integrated dry-run route evaluation.
- Added bounded provider-routed validation summaries.
- Added bounded H100 evidence, a repo-owned H100 harness, and expanded H100 representativeness summaries.
- Added baseline equivalence/output-fidelity evaluator and generated summary.
- Added official first-value CLI commands:
  - `kora inspect`
  - `kora compare`
  - `kora run`
  - `kora report`
- Added five-minute first-value quickstart and editable-install validation.
- Added Project Operating System breadcrumb/review layer:
  - `OPEN_THIS_FIRST.md`
  - `REVIEW_HUB.md`
  - ADR, runbook, templates, prompts, and validation reports.
- Updated evidence package, performance table, docs index, and July 1 RC decision materials.

## Validation

- `python3 -m pytest`: passed, `346 passed`
- `git diff --check`: passed
- generated evidence JSON validation: passed for `15` changed JSON files
- Markdown link/path sanity: passed for `78` changed Markdown files
- public/private scan: passed with expected boundary-language hits
- claim-boundary scan: passed with expected prohibited-claim boundary hits

## Evidence Generated

Primary evidence areas:

- route-selectivity metrics over four public matrix profiles.
- runtime-integrated dry-run route evaluation.
- bounded provider-routed validation.
- bounded H100 routed-subset measurement.
- repo-owned H100 harness bounded execution.
- expanded bounded H100 representativeness over public fixture-derived GPU-routed operations.
- baseline equivalence and output-fidelity evaluation over public fixtures.
- first-value CLI and editable-install validation.

Primary entrypoints:

- [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [REVIEW_HUB.md](../../REVIEW_HUB.md)
- [KRK evidence package v0](../evidence/krk-evidence-package-v0.md)
- [KRK performance table v0](../evidence/krk-performance-table-v0.md)
- [KORA five-minute first-value quickstart](../quickstart-five-minute-first-value.md)
- [Goal 074 PR readiness packet](krk-goal074-pr-readiness-merge-packet-v0.md)

## Claim Boundaries

This PR supports bounded, public-safe statements about:

- route-selectivity evidence over public fixtures.
- runtime-integrated dry-run routing evidence.
- bounded provider-path validation.
- bounded H100 fixture execution.
- fixture-derived output-fidelity evaluation.
- local first-value CLI install path.
- project breadcrumb/review-hub operation.

This PR does not claim:

- production readiness.
- production cost reduction.
- real API/GPU cost reduction.
- customer savings.
- energy reduction.
- broad workload superiority.
- H100 superiority.
- provider superiority.
- replacement of model serving, provider routing, or GPU serving systems.

## Known Limitations

- Evidence is bounded and fixture-derived.
- Provider evidence is bounded and aggregate-only.
- H100 evidence is bounded and not a raw H100 benchmark.
- Output fidelity uses deterministic rule-based public fixture comparison, not live semantic judging.
- Native Windows, WSL-specific install validation, wheel validation, source distribution validation, and published package validation remain deferred.

## Reviewer Checklist

- [ ] Review [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md).
- [ ] Review [REVIEW_HUB.md](../../REVIEW_HUB.md).
- [ ] Review the evidence package and performance table.
- [ ] Confirm generated JSON evidence parses.
- [ ] Confirm tests pass.
- [ ] Confirm claim boundaries remain negative for unsupported production, savings, superiority, adoption, and replacement claims.
- [ ] Confirm public/private boundaries remain intact.
- [ ] Confirm the first-value CLI path works locally if doing hands-on review.
