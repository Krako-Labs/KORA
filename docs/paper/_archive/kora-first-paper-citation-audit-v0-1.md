# KORA First Paper Citation Audit v0.1

## Purpose

This audit checks reference consistency, citation safety, and claim boundaries for manuscript v0.2 and the selected manuscript v0.3 integration of [R11], [R12], and [R13]. It is a bibliography-readiness document, not a final bibliography and not a submission-readiness claim.

## Scope

This audit covers:

- manuscript v0.2
- manuscript v0.3 selected reference integration
- references [R01] through [R24]
- preliminary references section
- related work framing
- claim boundary language

It does not add BibTeX, final citation style, manuscript-integrated citations beyond the current manuscript, or new evidence claims.

The working citation style strategy is recorded in [KORA First Paper Citation Style Decision](kora-first-paper-citation-style-decision.md). Stable `[Rxx]` labels remain the working style until metadata audit, bibliography normalization, and any later venue-specific conversion are complete.

Reference metadata readiness is recorded in [KORA First Paper Reference Metadata Audit v0.1](kora-first-paper-reference-metadata-audit-v0-1.md). That audit does not generate BibTeX and does not change manuscript claim support.

Normalized bibliography planning is recorded in [KORA First Paper Normalized Bibliography v0.1](kora-first-paper-normalized-bibliography-v0-1.md). That table does not generate BibTeX and does not change manuscript claim support.

Metadata gap resolution is recorded in [KORA First Paper Metadata Gap Resolution v0.1](kora-first-paper-metadata-gap-resolution-v0-1.md). That document classifies high-risk metadata blockers before BibTeX and does not change manuscript claim support.

## Citation Inventory

| ID | Reference topic | Appears in manuscript | Appears in References section | Tracker status | Action |
|---|---|---|---|---|---|
| [R01] | vLLM / PagedAttention | Yes | Yes | verified | normalize later |
| [R02] | MLPerf Inference | Yes | Yes | verified | normalize later |
| [R03] | ONNX Runtime docs | Yes | Yes | verified | needs citation style decision |
| [R04] | LangGraph Graph API docs | Yes | Yes | verified | needs citation style decision |
| [R05] | DSPy | Yes | Yes | verified | normalize later |
| [R06] | Retrieval-Augmented Generation | Yes | Yes | verified | normalize later |
| [R07] | Apache Airflow DAG docs | Yes | Yes | verified | needs citation style decision |
| [R08] | Snakemake | Yes | Yes | verified | normalize later |
| [R09] | llama.cpp | Yes | Yes | verified | needs citation style decision |
| [R10] | ACM Artifact Review and Badging | Yes | Yes | verified | needs citation style decision |
| [R11] | ReAct | Yes, in manuscript v0.3 | Yes, in manuscript v0.3 | verified | normalize later |
| [R12] | Toolformer | Yes, in manuscript v0.3 | Yes, in manuscript v0.3 | verified | normalize later |
| [R13] | PAL | Yes, in manuscript v0.3 | Yes, in manuscript v0.3 | verified | normalize later |
| [R14] | GPTCache | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R15] | Ollama docs/repository | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R16] | NeurIPS reproducibility program report | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R17] | USENIX NSDI artifact guidance | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R18] | MLSys artifact evaluation guidance | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R19] | BIG-bench | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R20] | HELM | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R21] | SWE-bench | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R22] | AgentBench | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R23] | Dynabench | No, future integration | No, future integration | verified | needs manuscript integration decision |
| [R24] | CheckList | No, future integration | No, future integration | verified | needs manuscript integration decision |

## Reference Normalization Status

### [R01] vLLM / PagedAttention

- Preliminary reference usability: usable as a preliminary paper reference.
- Metadata still missing: final venue/citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R02] MLPerf Inference

- Preliminary reference usability: usable as a preliminary benchmark-methodology reference.
- Metadata still missing: final citation-format normalization and full author handling.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R03] ONNX Runtime docs

- Preliminary reference usability: usable as official documentation context.
- Metadata still missing: final documentation citation style and exact access-date formatting.
- BibTeX ready: no.
- Source traceability: traceable to official documentation URL recorded in the tracker.

### [R04] LangGraph Graph API docs

- Preliminary reference usability: usable as official documentation context.
- Metadata still missing: final documentation citation style and exact access-date formatting.
- BibTeX ready: no.
- Source traceability: traceable to official documentation URL recorded in the tracker.

### [R05] DSPy

- Preliminary reference usability: usable as a preliminary programmatic-LM-workflow reference.
- Metadata still missing: final venue/citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL recorded in the tracker.

### [R06] Retrieval-Augmented Generation

- Preliminary reference usability: usable as a preliminary RAG background reference.
- Metadata still missing: final citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R07] Apache Airflow DAG docs

- Preliminary reference usability: usable as official DAG/workflow documentation context.
- Metadata still missing: final documentation citation style and exact access-date formatting.
- BibTeX ready: no.
- Source traceability: traceable to official Apache Airflow documentation URL recorded in the tracker.

### [R08] Snakemake

- Preliminary reference usability: usable as a preliminary workflow-engine reference.
- Metadata still missing: final citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to DOI recorded in the tracker.

### [R09] llama.cpp

- Preliminary reference usability: usable as official repository context for future local runtime work.
- Metadata still missing: final software/repository citation style and exact access-date formatting.
- BibTeX ready: no.
- Source traceability: traceable to official GitHub repository URL recorded in the tracker.

### [R10] ACM Artifact Review and Badging

- Preliminary reference usability: usable as official artifact-practice guidance context.
- Metadata still missing: final policy/documentation citation style.
- BibTeX ready: no.
- Source traceability: traceable to official ACM policy URL recorded in the tracker.

### [R11] ReAct

- Preliminary reference usability: usable as agent/tool-use background after manuscript integration.
- Metadata still missing: final citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R12] Toolformer

- Preliminary reference usability: usable as model-centered tool-use background after manuscript integration.
- Metadata still missing: final citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R13] PAL

- Preliminary reference usability: usable as program-aided workflow background after manuscript integration.
- Metadata still missing: final citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R14] GPTCache

- Preliminary reference usability: usable as semantic-cache background after manuscript integration.
- Metadata still missing: final citation-format normalization and final decision on how to cite the cost-related title without implying KORA cost evidence.
- BibTeX ready: no.
- Source traceability: traceable to ACL Anthology URL and DOI recorded in the tracker.

### [R15] Ollama

- Preliminary reference usability: usable as official local-runtime context after manuscript integration.
- Metadata still missing: final software/documentation citation style and exact access-date formatting.
- BibTeX ready: no.
- Source traceability: traceable to official documentation URL and official GitHub repository URL recorded in the tracker.

### [R16] NeurIPS Reproducibility Program Report

- Preliminary reference usability: usable as reproducibility-program background after manuscript integration.
- Metadata still missing: final citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R17] USENIX NSDI Artifact Guidance

- Preliminary reference usability: usable as venue-specific artifact-evaluation guidance after manuscript integration.
- Metadata still missing: final documentation citation style and exact access-date formatting.
- BibTeX ready: no.
- Source traceability: traceable to official USENIX URL recorded in the tracker.

### [R18] MLSys Artifact Evaluation Guidance

- Preliminary reference usability: usable as ML/systems artifact-evaluation guidance after manuscript integration.
- Metadata still missing: final documentation citation style and exact access-date formatting.
- BibTeX ready: no.
- Source traceability: traceable to official MLSys URL recorded in the tracker.

### [R19] BIG-bench

- Preliminary reference usability: usable as benchmark-construction and broad task-suite background after manuscript integration.
- Metadata still missing: final citation-format normalization and final author-list handling.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R20] HELM

- Preliminary reference usability: usable as holistic evaluation and multi-metric benchmark-methodology background after manuscript integration.
- Metadata still missing: final citation-format normalization and final author-list handling.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R21] SWE-bench

- Preliminary reference usability: usable as a software-engineering benchmark-construction example after manuscript integration.
- Metadata still missing: final citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R22] AgentBench

- Preliminary reference usability: usable as agent-benchmark background after manuscript integration.
- Metadata still missing: final citation-format normalization and final author-list handling.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R23] Dynabench

- Preliminary reference usability: usable as dynamic benchmark-methodology background after manuscript integration.
- Metadata still missing: final citation-format normalization and final author-list handling.
- BibTeX ready: no.
- Source traceability: traceable to arXiv URL and DOI recorded in the tracker.

### [R24] CheckList

- Preliminary reference usability: usable as behavior-oriented evaluation design background after manuscript integration.
- Metadata still missing: final citation-format normalization.
- BibTeX ready: no.
- Source traceability: traceable to ACL Anthology URL and DOI recorded in the tracker.

## Claim-Support Mapping

| Claim or statement type | References used | Supported use | Boundary |
|---|---|---|---|
| LLM serving systems context | [R01], [R02], [R03] | Background on model serving, inference benchmarking, and runtime context | Does not support KORA outperforming serving systems. |
| Workflow/DAG orchestration context | [R07], [R08] | Background on explicit workflows, DAGs, and reproducible pipelines | Does not support KORA replacing workflow systems. |
| Agent/programmatic AI context | [R04], [R05] | Background on graph-based agent execution and programmatic LM workflows | Does not support KORA replacing agent frameworks. |
| RAG context | [R06] | Background for retrieval-grounded generation and contrast with KORA routing | Does not support KORA replacing RAG. |
| Local runtime context | [R03], [R09] | Future-work context for local model/runtime systems | Does not support current local runtime validation evidence. |
| Benchmarking/reproducibility context | [R02] | Benchmark-methodology background | Does not support KORA production benchmark proof. |
| Artifact evaluation context | [R10] | Artifact-practice and transparency background | Does not indicate formal artifact evaluation approval. |
| Additional agent/tool-use context | [R11], [R12], [R13] | Manuscript v0.3 background on reasoning/action, API/tool-use, and program-aided execution | Does not support KORA outperforming agent or tool-use systems. |
| Semantic caching context | [R14] | Future manuscript background on cache reuse for LLM applications | Does not support KORA production cost or real API-cost claims. |
| Additional local runtime context | [R15] | Future manuscript background for local runtime systems | Does not support current KORA Ollama integration evidence. |
| Additional reproducibility context | [R16] | Future manuscript background on reproducibility programs and checklists | Does not make KORA submission-ready or formally reproducible by venue standards. |
| Venue-specific artifact guidance | [R17], [R18] | Future manuscript/readiness background on artifact-evaluation expectations | Does not indicate artifact approval or formal artifact evaluation. |
| Benchmark-construction and evaluation methodology context | [R19], [R20], [R21], [R22], [R23], [R24] | Future methodology/background context for benchmark breadth, metric coverage, task benchmark construction, agent evaluation, dynamic benchmarking, and behavior-oriented tests | Does not support KORA production benchmark proof, production/API-cost/energy claims, or broad workload superiority. |
| KORA 80/100 result | KORA benchmark docs and reproducible deterministic-heavy benchmark evidence | Supports the approved deterministic-heavy benchmark claim | External references do not imply production savings, real API-cost reduction, energy reduction, or broad superiority. |

## Forbidden Citation Uses

- Do not cite external systems as proof KORA is superior.
- Do not cite references as production cost reduction proof.
- Do not cite references as real API-cost reduction proof.
- Do not cite references as energy reduction evidence.
- Do not cite references as production benchmark evidence.
- Do not cite references as formal artifact evaluation approval.

## Bibliography Gaps

- Final citation style selection pending.
- BibTeX pending.
- Exact venue/metadata audit pending where needed.
- Additional references for agent/tool-use partially expanded in pass 2.
- Semantic caching reference partially added in pass 2.
- Synthetic workload and benchmark-construction references partially added in the benchmark-construction pass.
- Local runtime references partially expanded in pass 2.
- Venue-specific artifact guidance partially expanded in pass 2.

## Additional Reference Verification Pass 2

Pass date: 2026-05-11.

Additional verified references: 8.

Categories covered:

- agent/tool-use and agentic workflows
- program-aided language-model workflows
- semantic caching
- local model runtime systems
- reproducibility programs and checklists
- venue-specific artifact evaluation guidance

Categories still missing:

- more synthetic workload and benchmark-construction references
- target-venue-specific citation style and artifact guidance once a target venue is selected
- optional additional semantic-cache references if the manuscript discusses caching in more detail

Manuscript integration status:

- References [R11] through [R18] were verified tracker entries only in this pass.
- References [R11], [R12], and [R13] were later integrated into manuscript v0.3 text and its preliminary References section.
- References [R14] through [R18] remain tracker/audit-only, optional, or deferred according to the v0.3 integration plan.
- This does not complete final citation style, BibTeX, or final bibliography normalization.

## Manuscript v0.3 Integration Status

Manuscript v0.3 integrates selected pass-2 references.

Status:

- [R11] ReAct appears in manuscript v0.3 related work and the preliminary References section.
- [R12] Toolformer appears in manuscript v0.3 related work and the preliminary References section.
- [R13] PAL appears in manuscript v0.3 related work and the preliminary References section.
- [R14] through [R18] remain tracker/audit-only, optional, or deferred.
- Final citation audit is not complete.
- BibTeX remains pending.
- Final citation style remains pending.

## Benchmark-Construction Reference Verification Pass

Pass date: 2026-05-11.

Additional verified references: 6.

New verified labels: `[R19]` through `[R24]`.

Categories covered:

- broad benchmark-suite construction for language-model capabilities
- holistic and multi-metric evaluation methodology
- software-engineering task benchmark construction
- agent benchmark construction
- dynamic benchmark methodology
- behavior-oriented evaluation and test design

Categories still missing:

- references that specifically discuss deterministic-heavy synthetic workload construction for model-call routing systems
- final target-venue guidance after venue selection
- final decisions about which benchmark-methodology references belong in manuscript text

Manuscript integration status:

- References `[R19]` through `[R24]` are tracker/audit entries only in this pass.
- They are intended to support future benchmark-methodology background, not current manuscript claims.
- KORA's 80/100 result remains supported by KORA's own reproducible deterministic-heavy benchmark evidence, not by external references.
- These references do not prove production cost reduction, real API-cost reduction, energy reduction, production benchmark evidence, or broad workload superiority.
- This pass does not complete final citation style, BibTeX, final bibliography normalization, or final citation audit.

## Next Step

- Decide whether selected `[R19]` through `[R24]` references should be integrated into a future benchmark-methodology section.
- Use metadata gap resolution v0.1 to prepare preliminary BibTeX only for ready records and defer blocked records until metadata/style gaps are resolved.
- Manuscript v0.3 still requires final bibliography and claim-audit review before any submission-readiness claim.
