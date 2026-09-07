# S3 acceptance packet

Status: conditionally closed by maintainer decision on 2026-09-07 KST.
Merged implementation: PR #295, squash commit `e0e85aff366adedccd454cda6d11955417421dd3`.
Regression before merge: 749 passed; CI passed.

## Verified evidence

| Check | Outcome | Limit |
|---|---|---|
| Changed calculation and order cleaning, independent fixed oracle | MP 4/4, cluster 4/4, native-client 4/4 | Native D is controller CPU, not GPU |
| Bounded template replies | MP 30/30, cluster 30/30, native 30/30 | Exact templates, no open-ended quality proof |
| Native mixed order workload | 5/5, five model calls | Separate authorized window |
| Model process first request / resident repeats | 3/3 and 15/15 | MP only; OS/file cache not cleared |
| Same-device direct / worker, single request | 6/6 each | Small resident-model adapter comparison |
| Same-device direct / worker, two overlapping requests | 12/12 versus 6/12 | Worker admission is one job; failed requests retained |
| Exact reuse and changed input | Prior first/repeat/changed evidence plus fault injection | Earlier self-referential oracle corrected before merge |
| Native handover | Existing service restored, lease released | Historical verification; no new window needed for acceptance |

Raw evidence was inspected, not inferred from test totals. Initial six cluster
transport failures remain in historical results and are not included as successes
in the separate final twelve-row changed-input batch. API checks are not visual QA.

## Mandatory S4 readiness gates

1. Visual QA: inspect the rendered comparison controls, changed-input preview,
   result cards, failure and recorded labels, saved-run selection and JSON export
   through an authorized reachable browser.
2. Older hardware: identify and connect representative older devices, measure
   supported configurations and label inaccessible or incompatible cases accurately.

Neither gate is passed merely by merging S3. Both must have evidence before final
exhibition readiness. The current sprint scope and dates remain unchanged.

## Decision boundary

S3 acceptance is bounded to the implementation and evidence above. It does not
establish broad model quality, production performance, hardware superiority,
energy savings or general workload representativeness. S4 adds validation,
reproducibility and rehearsal evidence; it does not expand these claims.
