# KORA First Paper arXiv-Style Package Readiness v0.1

Status date: 2026-05-13

## Purpose

This artifact records readiness for a venue-neutral arXiv-style preprint package draft around manuscript v0.5. It does not submit to arXiv and does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-4.md`
- `docs/paper/kora-first-paper-manuscript-v0-5.md`
- `docs/paper/kora-first-paper-arxiv-metadata-checklist-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-bibliography-scope-v0-1.md`
- `docs/paper/kora-first-paper-submission-package-readiness-v0-1.md`
- `docs/paper/kora-first-paper-reproduction-transcript-checklist-v0-1.md`
- `docs/paper/kora-first-paper-artifact-package-inventory-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-claim-to-evidence-audit-v0-1.md`

## Package Status

- Package type: arXiv-style technical report / preprint draft.
- Paper type: original reproducible systems/evaluation technical report.
- Status: draft, not submission-ready.
- arXiv submission action: not performed.
- Conference, workshop, or journal selection: not performed.

## arXiv-Specific Checks

| Check | Current status | Remaining action |
|---|---|---|
| Author metadata | Albert Heekwan Kim, Krako Labs, Inc., a.kim@krako.xyz | Confirm exact display before export |
| arXiv endorsement | Already obtained / not blocking | No action unless category compatibility requires review |
| Category compatibility | Pending because endorsed category is not recorded here | Confirm category before submission |
| Candidate categories | `cs.AI`, `cs.LG`, `cs.DC`, `cs.SE` | Candidates only; no category selected here |
| Title / abstract | v0.5 title and abstract exist | Final human approval pending |
| License | Pending arXiv distribution-license decision | User decision required |
| Export format | Markdown draft exists; render/export readiness, export-route dry run, and local tooling plan completed | PDF/LaTeX/Markdown export package pending |
| Source package | Text-only export manifest, route recommendation, command plan, and hygiene checklist exist | Prepare final package only after user approvals |
| Figures/tables/algorithm assets | Inserted in manuscript v0.5 as Markdown/Mermaid/text assets | Render/conversion, numbering, and export treatment pending |
| Review/survey/position framing | Avoided | Preserve original systems/evaluation framing |
| Final human review | Pending | Required before any submission action |

## Manuscript Status

Manuscript v0.5 exists and is the current submission-candidate draft with inserted figure/table/algorithm assets. It remains a draft and should not be described as final or submission-ready.

## Bibliography Subset Status

The first arXiv-style package uses the conservative manuscript-cited bibliography subset:

- Manuscript v0.5 cited records: `[R01]`, `[R03]`, `[R04]`, `[R05]`, `[R06]`, `[R07]`, `[R08]`, `[R09]`, `[R10]`, `[R11]`, `[R12]`, `[R13]`.
- Preliminary BibTeX entries count: 16.
- `[R17]` and `[R18]` remain excluded.
- `[R19]` through `[R24]` remain tracker/audit-only for now.
- Full BibTeX remains incomplete.

## Claim and Evidence Status

The bounded claim remains:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

The package remains limited to reproducible deterministic-heavy benchmark evidence and synthetic local/no-network validation evidence. It does not claim production cost reduction, real API-cost reduction, production benchmark proof, full runtime-integrated real-provider benchmark evidence, broad workload superiority, energy reduction evidence, formal artifact approval, or paper submission readiness.

## Reproduction Transcript Status

The reproduction transcript checklist exists, but a final clean transcript has not been captured for the exact submission package commit.

## Artifact Inventory Status

The artifact package inventory exists. Final artifact availability wording, selected artifact bundle, and export package remain pending.

## Figure, Table, and Algorithm Status

The figure/table/algorithm plan and draft docs exist. They provide text-based Mermaid diagrams, benchmark and evidence-boundary tables, deterministic-first routing pseudocode, and an appendix artifact inventory table. Manuscript v0.5 now inserts those assets. Human review is still needed before final rendering and inclusion in the arXiv-style export package.

## Render and Export Readiness Status

The v0.5 render/export readiness report and text-only export package manifest now exist:

- `docs/paper/kora-first-paper-v0-5-render-export-readiness-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-export-package-manifest-v0-1.md`

No repository paper export pipeline was found, no PDF was generated, and no binary output was committed. Mermaid diagrams remain suitable for repository review but need rendering or conversion before an arXiv-compatible package.

## Export Route Dry-Run Status

The export-route dry run and recommendation now exist:

- `docs/paper/kora-first-paper-arxiv-export-route-dry-run-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-export-route-recommendation-v0-1.md`

Pandoc is available and successfully generated LaTeX and HTML dry-run outputs under `/tmp/kora-paper-export-dry-run`. Direct PDF generation is blocked locally because no LaTeX engine is installed. Mermaid conversion is blocked locally because no Mermaid CLI is installed. The recommended route is Pandoc-to-LaTeX as a starting point, followed by manual source-package cleanup for diagrams, wide tables, and bibliography formatting.

## Local Export Tooling Plan Status

The local export tooling plan, dry-build command plan, and source-package hygiene checklist now exist:

- `docs/paper/kora-first-paper-local-export-tooling-setup-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-dry-build-command-plan-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-source-package-hygiene-v0-1.md`

No tools were installed automatically. The next practical step is user-approved installation or selection of a LaTeX/PDF engine and Mermaid handling path, followed by a `/tmp` dry build.

## Installed-Tools Dry Build Status

The installed-tools dry-build result now exists:

- `docs/paper/kora-first-paper-arxiv-dry-build-result-v0-1.md`

With Tectonic and Mermaid CLI installed, a `/tmp` dry build generated rendered figure PDFs, LaTeX source, and a PDF after configuring Mermaid CLI to use the locally installed browser. No generated output was committed. The dry build still reports layout warnings, preliminary bibliography handling, and remaining source-package hygiene work, so the package remains not submission-ready.

## Dry Build Output Review Status

The dry-build output review now exists:

- `docs/paper/kora-first-paper-arxiv-dry-build-output-review-v0-1.md`

The review confirms the `/tmp` output inventory and cleaned source-package folder. It records remaining layout, bibliography, link, and final human-review blockers. No generated PDFs, rendered figures, source packages, or binary outputs were committed.

## Word-First Pause

PDF and arXiv source-package work are paused while the Word review path is active. The Word draft review and figure redesign notes now exist:

- `docs/paper/kora-first-paper-word-draft-review-v0-1.md`
- `docs/paper/kora-first-paper-figure-redesign-note-v0-1.md`

Final arXiv export remains pending until the Word draft, redesigned figures, bibliography formatting, and final human review are resolved.

## Word Placeholder Review Update

The image-inserted Word draft is superseded by a placeholder Word review draft because the inserted figure arrows did not render correctly:

- `docs/paper/kora-first-paper-word-placeholder-review-v0-1.md`

PDF/arXiv source-package work remains paused. Final publication-quality figures are deferred until after manuscript-body review.

## Missing User Approvals

- Final title and abstract approval.
- Final author/email display approval.
- arXiv category and category compatibility approval.
- arXiv license selection.
- Final bibliography/citation formatting approval.
- Final figures, tables, algorithm placement, reproduction transcript, and artifact package approval.
- Final submission-ready decision.

## Conclusion

The arXiv-style preprint package draft is organized but not submission-ready. Endorsement is already obtained and not blocking. Category compatibility, license, export package, final transcript, final bibliography formatting, and final human approval remain pending.
