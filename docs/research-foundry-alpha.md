# Research Foundry Alpha

Research Foundry Alpha turns text-layer PDFs into a deterministic, Local Only lexical index and returns retrieved evidence cards. It does not generate a synthesis or call a model.

## Installation

Install KORA from source with the optional PDF dependency:

```bash
python3 -m pip install -e '.[research]'
```

The extra adds `pypdf`. SQLite and FTS5 are provided by the Python runtime and must be available in that runtime.

## Ingest and query

Use PDFs that you own or are permitted to process. No private or example paper corpus is shipped.

```bash
python3 -m kora research ingest ./papers --state-dir ./.kora-research --json
python3 -m kora research query ./.kora-research "reflection tokens" --top-k 3 --markdown
```

`ingest` recursively discovers `.pdf` files under the supplied folder. `query` searches the selected state directory. Use `--json` for canonical evidence-card JSON, `--markdown` for Markdown, `--output PATH` to save the card, and `--run-json-out PATH` to save deterministic query events and counters.

## State and reuse

KORA creates `research-foundry.sqlite3` only below the explicit `--state-dir`. The source PDF tree is not modified. PDF bytes are hashed with SHA-256; exact duplicate content is indexed once, and unchanged content is reused on later ingestion. Document, chunk, and evidence identifiers are content-derived and stable for unchanged input.

Extracted text remains page-aware. Normalized page text is divided into deterministic chunks and indexed in SQLite FTS5 using lexical retrieval. Source paths are stored only as paths relative to the selected input folder and are not included in evidence cards.

## Evidence cards

JSON and Markdown cards use the `kora.research_evidence_card.v1` contract. A retrieved item contains:

- source title
- content-derived document ID
- one-based PDF page number
- stable chunk ID and evidence ID
- retrieval rank
- verbatim retrieved excerpt

Cards also report `evidence_found` or `insufficient_evidence`, structural validation status, the `Local Only` privacy state, and zero model-call, remote-provider-call, and upload counters. An evidence card is retrieved evidence with provenance; it is not a generated claim, citation judgment, or model-produced synthesis.

## Local Only boundary

The Research Foundry code performs no network request, upload, cloud fallback, provider call, or model inference. The caller controls both the PDF folder and state directory. Treat those inputs and the resulting SQLite database according to your own data-handling requirements.

## Limitations and non-goals

- Text-layer PDFs only; OCR is not supported.
- Lexical SQLite FTS5 retrieval only; there is no vector database or semantic search.
- No semantic synthesis, factuality proof, output-quality proof, or citation-quality judgment.
- No cloud fallback or remote provider integration.
- Exact-byte SHA-256 deduplication does not detect near-duplicates.
- Extracted text quality depends on the PDF text layer and `pypdf` behavior.
- This Alpha surface is not a production-readiness claim.
