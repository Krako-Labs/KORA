from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from kora.research import FailClosed, ResearchFoundry, ResearchFoundryError, canonical_json, render_evidence_card_markdown
from kora.research.evidence_card import build_evidence_card


def _pdf(path: Path, title: str, pages: list[str]) -> None:
    """Create a tiny deterministic text-layer PDF without a fixture dependency."""
    objects: list[bytes] = []
    page_ids = []
    # 1 catalog, 2 pages, 3 font, then page/content pairs, final metadata.
    for index, text in enumerate(pages):
        page_id = 4 + index * 2
        content_id = page_id + 1
        page_ids.append(page_id)
        escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream = f"BT /F1 11 Tf 72 720 Td ({escaped}) Tj ET".encode("latin-1")
        objects.extend([
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R >>".encode(),
            b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        ])
    metadata_id = 4 + len(pages) * 2
    prefix = [b"<< /Type /Catalog /Pages 2 0 R >>",
              f"<< /Type /Pages /Kids [{' '.join(f'{item} 0 R' for item in page_ids)}] /Count {len(page_ids)} >>".encode(),
              b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    safe_title = title.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    all_objects = prefix + objects + [f"<< /Title ({safe_title}) >>".encode("latin-1")]
    data = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, body in enumerate(all_objects, 1):
        offsets.append(len(data))
        data.extend(f"{number} 0 obj\n".encode() + body + b"\nendobj\n")
    xref = len(data)
    data.extend(f"xref\n0 {len(all_objects)+1}\n0000000000 65535 f \n".encode())
    data.extend(b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:]))
    data.extend(f"trailer\n<< /Size {len(all_objects)+1} /Root 1 0 R /Info {metadata_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    path.write_bytes(data)


def test_ingest_query_provenance_dedup_reuse_and_isolation(tmp_path: Path):
    corpus = tmp_path / "corpus"
    state = tmp_path / "state"
    corpus.mkdir()
    _pdf(corpus / "alpha.pdf", "Alpha Paper", ["alpha routing evidence page one", "stable provenance page two"])
    shutil.copyfile(corpus / "alpha.pdf", corpus / "duplicate.pdf")
    foundry = ResearchFoundry(state)
    first = foundry.ingest(corpus)
    assert first["counters"]["documents_parsed"] == 1
    assert first["counters"]["duplicates_skipped"] == 1
    assert first["counters"]["pages_parsed"] == 2
    assert first["counters"]["model_calls"] == first["counters"]["remote_provider_calls"] == first["counters"]["uploads"] == 0
    second = foundry.ingest(corpus)
    assert second["counters"]["documents_parsed"] == 0
    assert second["counters"]["documents_reused"] == 1
    assert second["counters"]["duplicates_skipped"] == 1
    result = foundry.query("stable provenance", top_k=3)
    item = result["card"]["evidence"][0]
    digest = hashlib.sha256((corpus / "alpha.pdf").read_bytes()).hexdigest()
    assert item["document_id"] == f"doc-alpha-{digest[:12]}"
    assert item["page"] == 2
    assert item["evidence_id"].endswith(":p002:c001")
    assert result["counters"] == {"queries": 1, "retrieval_hits": 1, "model_calls": 0, "remote_provider_calls": 0, "uploads": 0}
    assert list(state.iterdir()) == [state / "research-foundry.sqlite3"]
    assert not list(corpus.glob("*.sqlite3"))


def test_multi_source_no_hit_and_byte_stability(tmp_path: Path):
    corpus = tmp_path / "corpus"; corpus.mkdir()
    _pdf(corpus / "one.pdf", "One", ["sharedterm first source"])
    _pdf(corpus / "two.pdf", "Two", ["sharedterm second source"])
    foundry = ResearchFoundry(tmp_path / "state")
    foundry.ingest(corpus)
    card = foundry.query("sharedterm", top_k=2)["card"]
    assert len(card["evidence"]) == 2
    assert len({item["document_id"] for item in card["evidence"]}) == 2
    assert canonical_json(card) == canonical_json(foundry.query("sharedterm", top_k=2)["card"])
    assert render_evidence_card_markdown(card) == render_evidence_card_markdown(card)
    empty = foundry.query("wordnotpresentanywhere")["card"]
    assert empty["result_status"] == "insufficient_evidence" and empty["evidence"] == []
    assert b"No retrieved evidence. No claim or citation generated." in render_evidence_card_markdown(empty)


def test_evidence_records_fail_closed():
    record = {"title": "Title", "doc_id": "doc-alpha-0123456789ab", "page": 1,
              "evidence_id": "doc-alpha-0123456789ab:p001:c001", "text": "verbatim"}
    with pytest.raises(FailClosed, match="unknown_evidence_id"):
        build_evidence_card("query", [record], allowed_records={})
    malformed = dict(record, evidence_id="bad")
    with pytest.raises(FailClosed, match="malformed_evidence_id"):
        build_evidence_card("query", [malformed], allowed_records={"bad": malformed})
    changed = dict(record, text="changed")
    with pytest.raises(FailClosed, match="provenance_or_excerpt_mismatch"):
        build_evidence_card("query", [changed], allowed_records={record["evidence_id"]: record})


def test_clear_errors_for_missing_no_pdf_and_no_text(tmp_path: Path):
    with pytest.raises(ResearchFoundryError, match="folder not found"):
        ResearchFoundry(tmp_path / "state").ingest(tmp_path / "missing")
    empty = tmp_path / "empty"; empty.mkdir()
    with pytest.raises(ResearchFoundryError, match="no PDF"):
        ResearchFoundry(tmp_path / "state").ingest(empty)
    _pdf(empty / "blank.pdf", "Blank", [""])
    with pytest.raises(ResearchFoundryError, match="OCR is not supported"):
        ResearchFoundry(tmp_path / "state").ingest(empty)


def test_cli_success_and_error_paths(tmp_path: Path):
    corpus = tmp_path / "corpus"; corpus.mkdir()
    _pdf(corpus / "paper.pdf", "CLI Paper", ["cli searchable token"])
    state = tmp_path / "state"
    ingest = subprocess.run([sys.executable, "-m", "kora", "research", "ingest", str(corpus), "--state-dir", str(state), "--json"], capture_output=True, text=True)
    assert ingest.returncode == 0, ingest.stderr
    assert json.loads(ingest.stdout)["counters"]["documents_parsed"] == 1
    query = subprocess.run([sys.executable, "-m", "kora", "research", "query", str(state), "searchable", "--json"], capture_output=True, text=True)
    assert query.returncode == 0, query.stderr
    assert json.loads(query.stdout)["schema_version"] == "kora.research_evidence_card.v1"
    markdown = subprocess.run([sys.executable, "-m", "kora", "research", "query", str(state), "missing", "--markdown"], capture_output=True, text=True)
    assert markdown.returncode == 0 and "insufficient_evidence" in markdown.stdout
    error = subprocess.run([sys.executable, "-m", "kora", "research", "query", str(tmp_path / "missing"), "x", "--json"], capture_output=True, text=True)
    assert error.returncode == 1 and "research state not found" in error.stderr
