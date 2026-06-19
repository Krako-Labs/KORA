# Goal 089 Repository Hygiene And Architecture Diagram

Status: implemented.

Base: `origin/main` at `2fdc260fb0b4b174ad15e41e081df3703dd209c7`.

Branch: `goal089_repository_hygiene_architecture_diagram`.

## Summary

Goal 089 replaced the public workload-control architecture diagram with Albert's clean SVG asset and ran a repository hygiene audit for accidental exposure of local paths, private operating context, cross-project wording, and tool-specific continuation wording.

The new official public diagram is:

- `docs/assets/kora_workload_control_layer_architecture.svg`

The SVG was copied from the provided local asset without editing. SHA-256 matched before and after copy:

- `26d8124fbe828874388cd0ec780c942b32594bbea7705482b6920bda67d07a2f`

## Diagram References Updated

- `docs/README.md` now renders `assets/kora_workload_control_layer_architecture.svg`.
- `docs/community/KORA_SOCIAL_MEDIA_ANNOUNCEMENT_GUIDE.md` now points to `docs/assets/kora_workload_control_layer_architecture.svg`.
- `docs/paper/kora-first-paper-figure-table-algorithm-plan-v0-1.md` now points to `docs/assets/kora_workload_control_layer_architecture.svg`.

The older diagram asset was left in place for historical compatibility, but live references to the control-layer architecture were moved to the new official SVG.

## Hygiene Audit

The audit searched for the requested internal/private term set, including assistant/tooling terms, local filesystem paths, cross-project names, private-operations phrases, legacy benchmark labels, worktree path patterns, and hardware/evidence terms.

Findings:

- Public exposure found and fixed: hardcoded local filesystem paths in helper scripts and historical reports.
- Public exposure found and fixed: private internals path and private remote wording in an old review/cleanup report.
- Public exposure found and fixed: tool-specific resume headings in the review hub and documentation standard.
- Public exposure found and fixed: third-party chat-product wording in Studio text and one old Studio design SVG caption.
- Public exposure found and fixed: cross-project adoption wording that named a different project unnecessarily.
- Public exposure found and fixed: old benchmark-track labels in content where neutral provider-routing wording was sufficient.
- Residual expected hits remain for bounded public evidence and local-preview safety terminology. These are legitimate public KORA claim-boundary or implementation terms, not accidental private/local operating context.

## Files Updated For Hygiene

Hygiene updates covered:

- root breadcrumb and review hub continuation wording.
- documentation operating-standard and ADR wording.
- Project Operating System public/private boundary wording.
- historical report local-path redaction.
- Studio text and one old Studio design caption.
- legacy benchmark planning copy.
- provider-routing experiment copy.
- helper-script local environment loading.

## Claim Boundary

This task did not add product, benchmark, production-readiness, package-publication, cost-reduction, or model-quality claims. It only replaced a diagram asset, updated references, and removed accidental private/local presentation risk from public-facing files.

## Validation

Validation run:

- `git diff --check`
- markdown link validation
- changed public-doc markdown link sanity check
- requested repository hygiene scan
- `python3 -m kora examples list`

Result: passed after the hygiene rewrites and diagram reference updates.
