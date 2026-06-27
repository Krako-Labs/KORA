# Missing Evidence Checklist

## Needed Before First Draft

- Confirm latest benchmark command and output.
- Capture deterministic-heavy benchmark result in a reviewer-safe summary.
- Capture customer-support local validation result.
- Confirm all commands pass on a clean checkout.
- Identify exact tables to include.

## Nice To Have Before Draft

- Expanded 100-request customer-support workload.
- Local model runtime validation, for example Ollama.
- p50/p95 latency for deterministic vs model-required routes.
- Repeated runs.
- Qualitative examples of deterministic route classes.

## Draft v0 Next Evidence Priorities

- Clean command transcript.
- Latency p50/p95.
- Expanded 100-request customer-support workload.
- Local model runtime validation.
- Repeated runs.

## Priority after manuscript v0.1

- Clean command transcript.
- Latency p50/p95.
- Expanded 100-request customer-support workload.
- Local model runtime validation.
- Repeated runs.
- Figure generation.
- Bibliography/references.
- Manuscript v0.2 reference-integration review.
- Citation audit v0.1 review.
- Final verified bibliography.

## References and figures needed

- Additional verified related work references.
- Final citation format and bibliography normalization.
- Final citation audit review.
- Verified BibTeX entries if a BibTeX workflow is selected.
- Figure 1 architecture.
- Figure 2 execution-control layer.
- Figure 3 benchmark result.
- Figure 4 customer-support routing.
- Table finalization.

## Not Needed For First Paper

- OpenAI/Claude API cost validation.
- Production traffic.
- Energy measurement.
- Hosted KORA Studio.
- Real customer data.

## References and bibliography status

First verified reference pass:

- 10 references partially collected across the target related-work categories.
- Verified references recorded in the reference tracker.
- Manuscript v0.2 created with verified references integrated as preliminary citation labels.
- Citation audit v0.1 created.
- Final citation format, final bibliography, and BibTeX still pending.

Additional reference verification pass 2:

- 8 additional references verified and recorded as `[R11]` through `[R18]`.
- Agent/tool-use, semantic caching, local-runtime, reproducibility-program, and venue artifact-guidance coverage improved.
- Manuscript integration for `[R11]` through `[R13]` is complete in manuscript v0.3.
- `[R14]` through `[R18]` remain optional/deferred or tracker/audit-only.
- Final citation style, final bibliography, and BibTeX still pending.

Additional reference categories still pending:

- Benchmark-construction references are partially collected as `[R19]` through `[R24]`, with manuscript integration pending.
- More direct deterministic-heavy synthetic workload construction references may still be needed.
- Optional additional semantic caching references if the manuscript discusses caching in more detail.
- Target-venue-specific citation and artifact guidance after venue selection.
- Final citation style and BibTeX.

Benchmark-construction verification pass:

- 6 additional references verified for benchmark-suite construction, holistic and multi-metric evaluation methodology, software-engineering task benchmarks, agent benchmarks, dynamic benchmarking, and behavior-oriented test design.
- These references are tracker/audit entries only for now.
- They do not provide production benchmark evidence for KORA.
- Final citation style, final bibliography normalization, and BibTeX remain pending.

Citation style decision:

- Working citation style selected: stable `[Rxx]` labels.
- Metadata audit v0.1 for `[R01]` through `[R24]` has been created.
- Normalized bibliography table v0.1 has been created.
- High-risk metadata gap resolution v0.1 has been created at the planning/classification level.
- Preliminary BibTeX v0.1 exists only for ready records `[R01]`, `[R06]`, `[R08]`, `[R11]`, `[R14]`, `[R21]`, `[R24]`.
- Preliminary BibTeX key normalization is complete for the ready subset.
- Ready-subset BibTeX has been audited in final ready-subset BibTeX audit v0.1.
- Docs/repo metadata/style classification has been created for `[R03]`, `[R04]`, `[R07]`, `[R09]`, and `[R15]`.
- BibTeX for docs/repo entries is still pending.
- Artifact guidance metadata/style classification has been created for `[R10]`, `[R17]`, and `[R18]`.
- BibTeX for artifact guidance entries is still pending.
- Paper/preprint metadata-style classification has been created for `[R02]`, `[R05]`, `[R12]`, `[R13]`, `[R16]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]`.
- BibTeX for paper/preprint blocked records is still pending.
- Final blocked metadata review v0.1 has been created across the remaining blocked records.
- Expanded BibTeX candidate audit v0.1 has been created for `[R03]`, `[R04]`, `[R05]`, `[R07]`, `[R09]`, `[R10]`, `[R12]`, `[R13]`, and `[R16]`.
- Deferred records `[R17]` and `[R18]` and still-not-eligible records `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, and `[R23]` remain excluded from BibTeX.
- Final bibliography and claim audit v0.1 has been created.
- Expanded BibTeX remains preliminary, and full BibTeX is still incomplete until deferred and still-not-eligible records are resolved.
- Submission readiness gate v0.1 has been created to separate required blockers from optional improvements.
- Manuscript v0.4 submission-candidate draft has been created with current preliminary BibTeX citation synchronization.
- Manuscript bibliography sync v0.1, manuscript claim-to-evidence audit v0.1, and submission-candidate status v0.1 have been created.
- Submission package readiness v0.1, final human review packet v0.1, reproduction transcript checklist v0.1, and artifact package inventory v0.1 have been created.
- arXiv metadata checklist v0.1, arXiv bibliography scope v0.1, arXiv-style package readiness v0.1, and future venue scan placeholder v0.1 have been created.
- arXiv endorsement is already obtained and is not a current blocker.
- arXiv category compatibility, arXiv license, export package, final transcript, final artifact package review, and final human approval remain pending.
- Figure/table/algorithm plan v0.1 and draft assets v0.1 have been created.
- Manuscript v0.5 has been created with figure/table/algorithm assets inserted.
- Final figure/table/algorithm numbering, layout, rendering, and export treatment remain pending human review.
- v0.5 render/export readiness report and text-only export manifest have been created.
- No dedicated paper export pipeline has been found; final PDF/source-package generation remains pending.
- arXiv export route dry-run report and recommendation have been created.
- Pandoc-to-LaTeX is feasible as a starting route, but LaTeX/PDF tooling, Mermaid conversion, table layout, final bibliography formatting, and human approval remain pending.
- Local export tooling setup guide, dry-build command plan, and source-package hygiene checklist have been created.
- No tools were installed automatically and no full dry build was attempted because required export tools remain missing locally.
- Installed-tools arXiv dry-build result has been created.
- A `/tmp` PDF dry build now passes with Mermaid CLI and Tectonic, but layout warnings, bibliography integration, source-package hygiene review, and final human approval remain pending.
- Dry-build output review and source-package hygiene review have been created for the current `/tmp` outputs.
- Generated PDF visual review, layout cleanup, final bibliography integration, and final source-package hygiene review remain pending.
- Word draft review and figure redesign notes have been created.
- Word-first human review is now active, and PDF/arXiv source-package work is paused until the Word draft and redesigned figures are reviewed.
- Word placeholder review note has been created after human review found broken arrows in the inserted figure images.
- Figure finalization is deferred until after manuscript-body review.
- Clean reproduction transcript capture, final artifact package review, final venue/export decision, and final human review remain pending.
- Paper is still not submission-ready.

## Follow-Up Papers / Technical Reports

- OpenAI/Claude API cost reduction technical report.
- Energy/sustainability paper.
- Production-like application workload report.
