# Goal 089A README Architecture Diagram Placement

Status: implemented.

Base: `origin/main` at `5157832af5dcdf6df8baf8ff9f3ab6df35c8ffbb`.

Branch: `goal089a_readme_architecture_diagram_placement`.

## Summary

Goal 089A makes the clean KORA Workload Control Layer architecture diagram visible from the public README. Goal 089 had copied the clean SVG into `docs/assets/`, but README did not embed that asset, so the GitHub repository landing page still appeared text-only near the top.

## Changes

- Verified the clean SVG exists at `docs/assets/kora_workload_control_layer_architecture.svg`.
- Embedded the SVG near the top of `README.md` after the opening KORA positioning section.
- Added a direct fallback link under the README image.
- Confirmed `docs/README.md` already referenced the same SVG path.
- Added the same diagram reference and fallback link to `docs/vision/kora_workload_control_layer.md`.

## SVG Handling

The SVG file was not modified in this task.

## Validation

Validation run:

- `test -f docs/assets/kora_workload_control_layer_architecture.svg`
- `grep -n "docs/assets/kora_workload_control_layer_architecture.svg" README.md`
- markdown link validation for changed files
- `python3 scripts/check_markdown_links_goal082b.py`
- `git diff --check`

Result: passed.

## Claim Boundary

This task did not add new technical claims, production-readiness claims, release artifacts, tags, GitHub Releases, or package publication claims.
