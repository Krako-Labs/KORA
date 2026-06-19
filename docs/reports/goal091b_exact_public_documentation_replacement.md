# Goal 091B Exact Public Documentation Replacement

## Purpose

Goal 091B replaces selected public documentation with exact authored files.

The objective is to stop iterative interpretation of README and documentation changes and instead apply reviewed Markdown files verbatim.

## Files to Replace or Create

- `README.md`
- `docs/README.md`
- `examples/README.md`
- `docs/vision/kora_workload_control_layer.md`
- `docs/examples/kora_example_guide.md`

## Files to Update Manually

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

These files should be updated with short Goal 091B breadcrumb entries while preserving existing content.

## Required Validation

- `python3 -m kora examples list`
- `python3 scripts/check_markdown_links_goal082b.py`
- `git diff --check`
- Markdown heading sanity check for `README.md`
- Table sanity check for `README.md`
- High-risk private/internal term scan over changed files

## Claim Boundary Review

The replacement docs do not claim:

- production cost reduction proof
- real API-cost reduction proof
- production readiness
- benchmark superiority
- full OpenAI API compatibility
- production RAG, agent, or cache correctness
- model replacement
- published `getkora` availability

## Expected Outcome

The root README becomes a concise landing page.

Detailed example and evidence material moves to docs and example-specific files.

The repository remains source-install-only for latest features until a future `getkora` distribution is actually published.
