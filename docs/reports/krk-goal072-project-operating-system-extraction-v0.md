# KRK Goal 072 Project Operating System Extraction v0

Status: public-safe reusable documentation package created.

Final classification: `PROJECT_OPERATING_SYSTEM_EXTRACTED`

## Motivation

Goal 071 established KORA's project breadcrumb and review-hub standard. Goal 072 extracts that pattern into a reusable Project Operating System package so the same structure can be applied to other public/private/local project contexts.

This is a documentation/template extraction task. It does not add benchmark evidence, runtime evidence, product functionality, release approval, or public claims beyond the documentation operating package.

## How Goal 071 Was Generalized

Goal 071 created KORA-specific files:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- `docs/runbooks/project-documentation-operating-standard.md`
- `docs/adr/ADR-001-project-breadcrumb-and-review-hub-standard.md`

Goal 072 generalizes that structure by:

- replacing KORA-specific language with neutral template fields.
- using neutral roles: planning agent, execution agent, reviewer, and project owner.
- adding explicit public GitHub repo, private GitHub repo, and local-only project context sections.
- separating evidence, report, claim registry, ADR, and bootstrap checklist templates.
- adding prompts for initialization, gap analysis, and documentation refresh.

## Files Created

- [Project Operating System README](../project-operating-system/README.md)
- [Project Operating Standard v0](../project-operating-system/project-operating-standard-v0.md)
- [OPEN_THIS_FIRST template](../project-operating-system/templates/OPEN_THIS_FIRST.template.md)
- [REVIEW_HUB template](../project-operating-system/templates/REVIEW_HUB.template.md)
- [ADR-001 template](../project-operating-system/templates/ADR-001-project-breadcrumb-standard.template.md)
- [Report template](../project-operating-system/templates/REPORT.template.md)
- [Evidence template](../project-operating-system/templates/EVIDENCE.template.md)
- [Claim registry template](../project-operating-system/templates/CLAIM_REGISTRY.template.md)
- [Project bootstrap checklist template](../project-operating-system/templates/PROJECT_BOOTSTRAP_CHECKLIST.template.md)
- [Project initialization prompt](../project-operating-system/prompts/project-initialization-prompt.md)
- [Project gap analysis prompt](../project-operating-system/prompts/project-gap-analysis-prompt.md)
- [Project documentation refresh prompt](../project-operating-system/prompts/project-doc-refresh-prompt.md)

## Files Updated

- [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [REVIEW_HUB.md](../../REVIEW_HUB.md)
- [Documentation index](../README.md)

## Extracted Template Set

| Template | Purpose |
| --- | --- |
| `OPEN_THIS_FIRST.template.md` | Fast-start project breadcrumb. |
| `REVIEW_HUB.template.md` | Current-state review hub. |
| `ADR-001-project-breadcrumb-standard.template.md` | Decision record for adopting the breadcrumb/review-hub standard. |
| `REPORT.template.md` | Task completion report. |
| `EVIDENCE.template.md` | Evidence summary. |
| `CLAIM_REGISTRY.template.md` | Supported and unsupported claim registry. |
| `PROJECT_BOOTSTRAP_CHECKLIST.template.md` | New-project setup checklist. |

## How Future Projects Should Adopt The Structure

Recommended adoption path:

1. Read [Project Operating System README](../project-operating-system/README.md).
2. Copy the templates into the target project.
3. Fill in public GitHub repo, private GitHub repo, and local-only project context sections.
4. Create `OPEN_THIS_FIRST.md` and `REVIEW_HUB.md`.
5. Create an ADR accepting the breadcrumb and review-hub standard.
6. Create or update claim registry and evidence index if the project has public claims.
7. Require every completed task to update the breadcrumb and review hub unless explicitly exempted.

## How Another Project Can Use It Next

Another project, including Permea, can use the extracted templates without inheriting KORA-specific evidence or language.

Recommended next use:

- initialize project-specific `OPEN_THIS_FIRST.md`.
- initialize project-specific `REVIEW_HUB.md`.
- identify public repo, private repo, and local-only context boundaries.
- fill the claim registry with only that project's supported claims.
- avoid copying private operational details into public files.

This report intentionally does not include private operational details for any other project.

## Limitations

- The package is documentation-only.
- It has not yet been applied to a second project in this Goal.
- Templates still require project-specific review before use.
- The templates do not replace evidence generation, tests, or human owner approval.
- The package does not create release, PR, or production-readiness status.

## Claim Boundary

Supported:

- KORA now contains a reusable Project Operating System package.
- The package includes templates, prompts, and a project operating standard.
- The package can guide future project breadcrumb/review-hub adoption.

Not supported:

- production readiness.
- production cost reduction.
- customer savings.
- energy reduction.
- broad workload superiority.
- real API/GPU cost reduction.
- provider superiority.
- H100 superiority.
- release, tag, or PR readiness by itself.
