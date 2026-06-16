# KRK July 1 Readiness Refresh v0

Status: readiness refresh after multi-profile route-selectivity evidence.

## What Changed Since the Prior Planning State

KRK route-selectivity moved from planned/missing evidence to implemented dry-run matrix evidence. The repository now includes generated JSON and Markdown metrics for four public profiles:

- mixed-realistic.
- GPU-heavy.
- cache-heavy.
- adversarial.

The active branch did not contain the earlier release-candidate plan, required-evidence doc, or owner-review packet, so this refresh recreates the required public-safe readiness docs using the current evidence package.

## Goal 046 Evidence Summary

| Profile | Requests | Exact route accuracy | Acceptable route rate | Unsafe misroute rate | Compute-weighted GPU demand |
| --- | ---: | ---: | ---: | ---: | ---: |
| mixed-realistic | 6 | 1.0000 | 1.0000 | 0.0000 | 0.5217 |
| GPU-heavy | 4 | 1.0000 | 1.0000 | 0.0000 | 0.7059 |
| cache-heavy | 4 | 1.0000 | 1.0000 | 0.0000 | 0.5556 |
| adversarial | 4 | 0.7500 | 1.0000 | 0.0000 | 0.0000 |

The evaluator uses only router-visible metadata for route selection and compares the selected route to oracle labels after routing. No provider calls, GPU execution, or live runtime measurement are included.

## Readiness Delta

Improved:

- route-selectivity metrics are implemented for the public matrix path.
- generated evidence outputs are available in JSON and Markdown.
- reproducibility is stronger for the matrix path because the evaluator commands are documented.
- evidence completeness improved but remains PARTIAL.

Unchanged:

- CLI path remains PARTIAL.
- paper draft remains PARTIAL.
- community preview remains PARTIAL.

Still open:

- H100 bounded public evidence.
- provider validation.
- runtime-integrated route-selectivity workflow.
- broader workload representativeness.

## Remaining Blockers

There are no blockers for a narrowed KRK July 1 RC package.

There are blockers for any broader claim that requires live provider validation, bounded GPU-routed subset measurement, or broad workload representativeness.

## Recommendation

Proceed with a narrowed KRK July 1 RC:

- position KRK as deterministic-first execution routing.
- include deterministic-heavy evidence.
- include four-profile dry-run route-selectivity evidence.
- preserve explicit limitations.
- keep KORA Core expansion as roadmap unless implemented.

Do not present this package as live production validation or broad infrastructure proof.
