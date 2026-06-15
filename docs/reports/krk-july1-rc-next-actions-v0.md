# KRK July 1 RC Next Actions v0

Status: next actions after Goal 056 decision refresh.

## Required Next Goals

| Goal | Action | Expected output |
| --- | --- | --- |
| Goal 057 | KRK July 1 RC Package PR Readiness | Verify refreshed package consistency, scan boundaries, prepare PR-ready summary, and confirm no unsupported claims were introduced |
| Goal 058 | Open PR | Open a scoped PR only after readiness checks pass and owner approval allows it |
| Goal 059 | Merge if approved | Merge only after PR review/approval and final validation gates pass |

## Optional Next Actions

| Action | Purpose |
| --- | --- |
| Optional public note | Publish a narrow evidence-centered note after approval, using the claim package language |
| Optional technical paper cleanup | Refresh paper draft references to include route-selectivity, runtime-integrated dry-run evidence, bounded H100 subset, expanded provider-path evidence, and expanded H100 not-run status |
| Optional H100/provider expansion | Expand subset sizes and workload variety without broadening claims prematurely; rerun expanded H100 only in a safe CUDA/H100-capable environment |
| KORA Core workflow implementation | Implement inspect, compare, run, and report workflow surfaces so future RCs can move beyond planning-level KORA Core language |

## Immediate Recommendation

Proceed to Goal 057: KRK July 1 RC Package PR Readiness.

Goal 057 should verify the refreshed documentation package, claim boundaries, generated JSON validity, tests, public/private scans, and PR summary before any push or PR action.
