"""Strict deterministic renderer for ``kora.research_evidence_card.v1``."""

from __future__ import annotations

import json
import re
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = "kora.research_evidence_card.v1"
VALIDATOR_VERSION = "kora.evidence_card_validator.v1"
ZERO_COUNTERS = {"model_calls": 0, "remote_provider_calls": 0, "uploads": 0}
ID_PATTERN = re.compile(r"^doc-[A-Za-z0-9.-]+-[0-9a-f]{12}:p[0-9]{3}:c[0-9]{3}$")


class FailClosed(ValueError):
    """Raised when an evidence record cannot be rendered safely."""


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def build_evidence_card(
    query: str,
    records: Sequence[Mapping[str, Any]],
    *,
    allowed_records: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    if not isinstance(query, str) or not query.strip():
        raise FailClosed("invalid_query")
    evidence: list[dict[str, Any]] = []
    required = {"title", "doc_id", "page", "evidence_id", "text"}
    for rank, record in enumerate(records, 1):
        if set(record) != required:
            raise FailClosed("evidence_record_schema_mismatch")
        evidence_id = record.get("evidence_id")
        if not isinstance(evidence_id, str) or not ID_PATTERN.fullmatch(evidence_id):
            raise FailClosed("malformed_evidence_id")
        frozen = allowed_records.get(evidence_id)
        if frozen is None:
            raise FailClosed("unknown_evidence_id")
        if dict(record) != dict(frozen):
            raise FailClosed("provenance_or_excerpt_mismatch")
        page = record["page"]
        if not isinstance(page, int) or page < 1 or not record["title"] or not record["text"]:
            raise FailClosed("invalid_evidence_record")
        if evidence_id != f"{record['doc_id']}:p{page:03d}:c{int(evidence_id.rsplit(':c', 1)[1]):03d}":
            raise FailClosed("provenance_or_excerpt_mismatch")
        evidence.append({
            "source_title": record["title"], "document_id": record["doc_id"], "page": page,
            "chunk_id": evidence_id, "evidence_id": evidence_id,
            "verbatim_retrieved_excerpt": record["text"], "retrieval_rank": rank,
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "query": query,
        "result_status": "evidence_found" if evidence else "insufficient_evidence",
        "evidence": evidence,
        "privacy_state": "Local Only",
        "counters": dict(ZERO_COUNTERS),
        "structural_validation": {"result": "passed", "validator_version": VALIDATOR_VERSION},
    }


def render_evidence_card_markdown(card: Mapping[str, Any]) -> bytes:
    # Rebuild from the card's evidence so arbitrary or mutated card objects fail closed.
    expected_keys = {"schema_version", "query", "result_status", "evidence", "privacy_state", "counters", "structural_validation"}
    if set(card) != expected_keys or card.get("schema_version") != SCHEMA_VERSION:
        raise FailClosed("schema_mismatch")
    raw = []
    allowed = {}
    for item in card.get("evidence", []):
        if not isinstance(item, Mapping):
            raise FailClosed("invalid_evidence")
        record = {"title": item.get("source_title"), "doc_id": item.get("document_id"), "page": item.get("page"),
                  "evidence_id": item.get("evidence_id"), "text": item.get("verbatim_retrieved_excerpt")}
        if item.get("chunk_id") != item.get("evidence_id") or item.get("retrieval_rank") != len(raw) + 1:
            raise FailClosed("provenance_or_excerpt_mismatch")
        raw.append(record)
        allowed[str(record["evidence_id"])] = record
    rebuilt = build_evidence_card(str(card.get("query", "")), raw, allowed_records=allowed)
    if dict(card) != rebuilt:
        raise FailClosed("card_validation_failed")
    lines = ["# Research Evidence Card", "", f"Schema: `{SCHEMA_VERSION}`  ", f"Query: {card['query']}  ",
             f"Result status: `{card['result_status']}`  ", "Privacy state: `Local Only`  ",
             f"Structural validation: `passed` (`{VALIDATOR_VERSION}`)", "", "## Retrieved evidence", ""]
    if not raw:
        lines.extend(["No retrieved evidence. No claim or citation generated.", ""])
    for rank, record in enumerate(raw, 1):
        lines.extend([f"### Rank {rank}", "", f"- Source title: {record['title']}",
                      f"- Document ID: `{record['doc_id']}`", f"- Page: {record['page']}",
                      f"- Chunk ID: `{record['evidence_id']}`", f"- Evidence ID: `{record['evidence_id']}`", "",
                      "```text", str(record["text"]), "```", ""])
    lines.extend(["## Execution counters", "", "- Model calls: 0", "- Remote/provider calls: 0", "- Uploads: 0", ""])
    return "\n".join(lines).encode("utf-8")
