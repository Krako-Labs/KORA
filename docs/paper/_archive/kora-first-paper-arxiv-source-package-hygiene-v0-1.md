# KORA First Paper arXiv Source Package Hygiene v0.1

Status date: 2026-05-13

## Purpose

This checklist defines source-package hygiene expectations for a future arXiv-style package. It does not create a package, does not upload to arXiv, and does not mark the paper as submission-ready.

## Include Only Build-Needed Files

The package should include only files needed to build or review the final paper package:

- final paper source,
- final bibliography source,
- approved figure files or approved source equivalents,
- required style files,
- required appendix or artifact-description source.

## Exclude

Exclude:

- private or local paths,
- raw benchmark artifacts,
- temporary build outputs,
- generated logs unless explicitly needed,
- `/tmp` outputs,
- hidden comments and unrelated planning notes,
- provider responses,
- API keys and credentials,
- private user data,
- production traffic,
- release assets,
- large unused files.

## Secret and Path Checks

Before any upload, inspect source files for:

```text
sk-
ghp_
password=
secret=
api_key=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

Also inspect manually for absolute local home paths, private local context paths, and internal workflow markers.

Any match must be removed or explicitly justified before packaging.

## Claim Boundary Checks

Before any upload, inspect source files for unsupported claims:

```text
production cost reduction
real API-cost reduction
production benchmark proof
full runtime-integrated real-provider benchmark evidence
broad workload superiority
energy reduction
formal government validation
guaranteed adoption
formal artifact approval
formally approved
```

Boundary or limitation wording may be appropriate in planning docs, but the final source package should only include claim language intentionally meant for the paper.

## Residual File Warning

arXiv source files may become downloadable after submission. Avoid unnecessary residual files, local-only notes, debug comments, temporary outputs, or unrelated planning artifacts in the source package.

## Metadata Checks

Before upload, confirm:

- final arXiv category and category compatibility,
- license choice,
- title and abstract,
- author display,
- affiliation and email display,
- comments field if used,
- final bibliography formatting,
- final figure/table rendering.

## Status

The dry-build source-package hygiene review is recorded in `docs/paper/kora-first-paper-arxiv-dry-build-output-review-v0-1.md`. The reviewed `/tmp` folder contains only generated LaTeX, rendered figure PDFs, and the preliminary bibliography draft. Final package hygiene review remains pending for the exact final source package. No upload was performed, and the paper remains not submission-ready.
