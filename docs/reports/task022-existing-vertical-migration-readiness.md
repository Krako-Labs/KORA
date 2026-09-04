# Task 022: Existing Vertical Migration Readiness

Status: bounded reference migration implemented for local validation.

## Decision and claim boundary

Research Foundry remains a non-commercial, offline reference vertical. This work does not select KORA's first commercial Solution, redesign Research Foundry, validate production data, or establish production readiness.

The migration reuses the existing deterministic Research Foundry implementation through the Solution Protocol v0alpha1, the local KORA Host lifecycle, a bounded reference capability runtime, and the package-declared Conformance Kit. It adds no workflow-specific behavior to KORA Core.

## Existing vertical inventory

| Surface | Existing Research Foundry behavior |
| --- | --- |
| Inputs | An explicit PDF folder for ingest; an explicit state directory; a non-empty lexical query; bounded positive `top_k`. |
| PDF handling | Recursive discovery of text-layer `.pdf` files, `pypdf` text extraction, page-aware normalization, and deterministic chunking. |
| Identity and reuse | SHA-256 document identity, exact-byte duplicate suppression, stable document/chunk/evidence identifiers, and unchanged-state reuse. |
| Local state | One SQLite database below the caller-selected state directory, including an FTS5 lexical index. |
| Outputs | Machine-readable ingest events/counters and a deterministic Research Evidence Card for query results. |
| Evidence | Source title, content-derived document id, one-based page, chunk/evidence id, retrieval rank, and verbatim retrieved excerpt. |
| File access | Read PDFs below the caller-selected corpus and write SQLite state below the caller-selected state directory. |
| Permission boundary | The standalone CLI relies on explicit caller paths; it has no Solution manifest approval gate. |
| External activity | No network request, upload, provider call, model inference, GPU, CUDA, OCR, vector retrieval, or semantic judging. |

## Migration gap report

| Gap | Effect on a Solution migration | Task 022 disposition |
| --- | --- | --- |
| No Solution Package | The standalone CLI does not declare schemas, Task Graph, policy, or integrity. | Add one integrity-bound reference package. |
| Separate commands | Ingest and query do not run through `validate`, `install`, `run`, `status`, and `result`. | Map the deterministic ingest-query path to one Host capability. |
| Runtime lacks package context | A runtime could not safely resolve integrity-checked package assets. | Pass the installed package root through the workflow-neutral runtime interface. |
| No PDF capability binding | The base reference runtime cannot invoke the existing Foundry. | Add an optional bounded `document.pdf.lexical-query` runtime. |
| File-write policy is implicit | SQLite creation was not represented as a Solution side effect or approval. | Declare and require `local.file.write`. |
| Arbitrary external corpus access | The current Host has no safe mount/binding contract for caller folders. | Keep the corpus package-local; defer external mounts. |
| Persistent reuse versus run isolation | The Host creates a fresh workspace for every run. | Rebuild a tiny per-run index; defer cross-run state. |
| Ingest output contains a state path | Returning it would expose a Host workspace detail and complicate the output contract. | Return only the existing query/evidence output. |
| No vertical conformance cases | Integrity, approvals, lifecycle, deterministic output, and no-hit behavior were not package-bound. | Add four integrity-bound positive and negative cases. |

## Frozen minimum Protocol slice

Task 022 freezes the following slice:

- one synthetic, text-layer PDF under the package's integrity map;
- one deterministic capability, `document.pdf.lexical-query`;
- the existing `ResearchFoundry.ingest` followed by `ResearchFoundry.query`;
- one fresh SQLite FTS5 state directory inside each isolated run workspace;
- package-relative corpus resolution with absolute-path, parent-traversal, and symlink rejection;
- at most 16 PDFs and 8 MiB of PDF bytes per run;
- `network: denied`;
- declared and explicitly granted `local.file.write`;
- the existing Research Evidence Card output without ingest state paths;
- the same Host `validate`, `install`, `run`, `status`, and `result` interface used by the synthetic reference Solutions.

The capability is exposed only when the optional `pypdf` dependency and SQLite FTS5 are available. The base `kora.reference` runtime remains separate, and one runtime must still satisfy all capabilities required by a package.

## Mapping

| Solution element | Research Foundry mapping |
| --- | --- |
| Manifest | `example.research-foundry-reference` version `0.1.0` |
| Input schema | Required `query` string and `top_k` integer from 1 through 20 |
| Task Graph | One deterministic retrieval task |
| Capability | `document.pdf.lexical-query` |
| Runtime | `kora.document-pdf-reference` version `0.1.0` |
| Static asset | `assets/corpus/reference.pdf` |
| Side effect | Per-run SQLite state below the Host workspace |
| Approval | Explicit `local.file.write` run grant |
| Output schema | Strict existing query events, counters, and Research Evidence Card |
| Network/model/GPU | Denied and reported false |

## Failure semantics and conformance

Initialized runs preserve the existing fail-closed, machine-readable result envelope.

The package declares these integrity-bound cases:

| Case | Expected path |
| --- | --- |
| `query-success` | Valid input and approval produce one exact evidence record. |
| `no-hit` | Valid input and approval produce `insufficient_evidence` with no evidence records. |
| `invalid-input` | Input validation fails before runtime execution. |
| `missing-approval` | Approval validation fails before runtime execution. |

Additional automated checks cover deterministic repeatability, installed-PDF tampering before execution, package-path escape rejection, optional-runtime absence, persisted status/result schema validation, and a socket-denied conformance run.

## Implemented files

- `kora/solution/reference_runtime.py`: bounded PDF capability and optional runtime availability probe.
- `kora/solution/host.py`: workflow-neutral installed-package context passed to the selected runtime.
- `kora/solution/runtime_registry.py`: corresponding runtime protocol signature.
- `kora/solution/validator.py`: validation knowledge of the frozen capability.
- `kora/solution/__init__.py`: public Solution-runtime exports.
- `examples/solutions/research-foundry-reference/`: manifest, graph, schemas, synthetic PDF, input, README, and four conformance cases.
- `tests/test_research_foundry_solution.py`: migration lifecycle, repeatability, failure, integrity, path, and offline checks.

## Intentionally deferred

The following are next-sprint candidates, not Task 022 implementation:

- a safe Host contract for caller-selected external corpus mounts or bindings;
- cross-run Research Foundry state and unchanged-document reuse through the Host;
- separate ingest and query tasks with typed task-output dataflow;
- stop, resume, checkpoint, and cache behavior;
- OCR, vector retrieval, semantic search, synthesis, and semantic judging;
- provider, API, model, GPU, CUDA, or network execution;
- dynamic or remote runtime discovery and registries;
- multi-Mac operation;
- production data, production access, production validation, and commercial Solution selection;
- release, tag, package publication, Marketplace, or public claim expansion.

## Validation completed

- Focused Research Foundry and Solution checks: 62 passed.
- Full regression: 677 passed, including the 671-test pre-change baseline.
- Package-declared conformance: 4 passed, 0 failed.
- Isolated non-editable source-install readiness: 6 passed, 0 failed.
- Fresh non-editable `.[research]` installed CLI: `validate`, `install`, two `run` calls, `status`, `result`, exact repeatability, and conformance passed from outside the checkout.
- Existing first-run CLI profile: 7 passed, 0 failed.
- Existing release-smoke script: passed; no release, tag, archive publication, or package publication was performed.
- Python compile check, Markdown link check, and `git diff --check`: passed.
- Changed-file security and boundary scan: 26 files inspected with zero private-path, credential-pattern, bidirectional/control-character, package-symlink, integrity, JSON-parse, or active-PDF-action findings.
- Runtime/conformance activity records and socket-denied testing confirmed no network access, model inference, or GPU execution.

## Known limitations

This slice is intentionally small. It accepts only integrity-bound package-local text-layer PDFs, performs a fresh ingest for each run, depends on local `pypdf` and SQLite FTS5 support, and is capped at 16 files and 8 MiB. Extracted text quality still depends on the PDF text layer and `pypdf`. Passing the declared conformance cases demonstrates only this bounded deterministic protocol path; it does not prove output quality, security certification, production readiness, customer savings, or broader workload performance.
