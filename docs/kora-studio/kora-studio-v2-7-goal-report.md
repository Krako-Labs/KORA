# KORA Studio v2.7 Goal Report

## Goal Status

Goal 526G is complete.

KORA Studio v2.7 reviews negative CSP/resource guard coverage and adds only dependency-light cases that materially reduce regression risk for the current server-rendered Studio HTML model.

## Starting State

- Starting public HEAD: `f17076456d2ca54840e93305279c746f01fb3e82`
- Public truth: `origin/main`

## Completed Work

- Reviewed current CSP/resource guard helpers and fixture matrix
- Added normalization for whitespace-padded and mixed-case resource URL values
- Added `javascript:` pseudo URL detection
- Added `srcset` URL candidate parsing
- Added `meta refresh` URL candidate parsing
- Added inline event handler detection
- Added inline `<style>` block detection
- Added targeted table-driven negative fixtures
- Documented added and declined cases

## Files Changed

- `tests/test_kora_studio_server.py`
- `docs/kora-studio/README.md`
- `docs/kora-studio/kora-studio-implementation-breakdown.md`
- `docs/kora-studio/kora-studio-v2-7-csp-negative-coverage-review.md`
- `docs/kora-studio/kora-studio-v2-7-goal-report.md`

## Added Cases and Rationale

Added:

- mixed-case external schemes, because URL schemes are case-insensitive
- whitespace-padded URLs, because raw attribute values can include incidental whitespace
- `javascript:` pseudo URLs, because they are executable link targets
- `srcset` external candidates, because they are image resource URLs
- `meta refresh` URL targets, because they can navigate away from the local preview
- external form `action` targets, because forms are blocked by current CSP
- inline event handlers, because they are inline executable behavior
- inline `<style>` blocks, because current CSP allows only self-hosted stylesheet assets

Declined:

- workers, frames, media, and font-specific negative cases, because Studio does not currently use those resource classes
- browser-only assertions, because browser CSP validation remains optional and explicitly gated
- broader static asset fixtures, because the existing allowlist and traversal tests already cover asset route behavior

## Preserved Fixture Coverage

Existing HTML, CSP, and CSS fixture coverage remains intact:

- inline style attributes
- inline executable scripts
- external scripts and stylesheets
- `data:`, `blob:`, and protocol-relative URLs
- unapproved `/studio-assets/...`
- wildcard CSP sources
- `unsafe-inline`
- `unsafe-eval`
- external CSP hosts
- new image/font CSP directives
- CSS `@import`
- CSS `url(...)`

## Validation Results

Final validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Optional smoke checks:

- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed
- `python3 scripts/check_kora_studio_preview.py`: passed

## Claim Boundaries Preserved

- KORA Studio remains local preview/demo readiness only.
- This is CSP guard negative coverage review only.
- Browser CSP validation remains smoke validation only.
- KORA Studio is not production-ready.
- KORA Studio does not claim production security readiness.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution was added.
- No model execution was added.
- No provider calls were added.
- No downloads were added.
- No cloud sync was added.
- No private model directory scanning was added.
- No runtime model list commands were added.
- No report export or file writing was added.
- No external assets or CDN dependencies were added.
- No production telemetry or production cost evidence claim was added.
- No production cost reduction claim was added.
- No energy outcome claim was added.
- No unsupported larger-model execution claim was added.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Known Limitations

- The review is representative regression coverage, not a production security assessment.
- Future legitimate resource classes should update positive guards, negative fixtures, CSP policy, and docs in a separate reviewed goal.

## Next Recommended Goal

Goal 527G - KORA Studio CSP Guard Documentation Sync.

The next goal should review older KORA Studio static asset and CSP docs for concise cross-links to the v2.4-v2.7 guard reports while preserving runtime behavior, endpoint behavior, smoke markers, and claim safety.
