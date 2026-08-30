"""One-Mac, local-only PDF ingestion and lexical retrieval."""

from __future__ import annotations

import hashlib
import re
import sqlite3
from pathlib import Path
from typing import Any

from .evidence_card import ZERO_COUNTERS, build_evidence_card

DB_NAME = "research-foundry.sqlite3"


class ResearchFoundryError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _normalize(text: str) -> str:
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.replace("\x00", "").splitlines()]
    return "\n".join(line for line in lines if line).strip()


def _chunks(text: str, target_chars: int = 1100) -> list[str]:
    result: list[str] = []
    current = ""
    for paragraph in (line for line in text.split("\n") if line):
        if current and len(current) + len(paragraph) + 1 > target_chars:
            result.append(current)
            current = ""
        if len(paragraph) > target_chars:
            if current:
                result.append(current)
                current = ""
            result.extend(paragraph[start:start + target_chars] for start in range(0, len(paragraph), target_chars))
        else:
            current = f"{current}\n{paragraph}".strip()
    if current:
        result.append(current)
    return result


class ResearchFoundry:
    def __init__(self, state_dir: str | Path):
        self.state_dir = Path(state_dir).expanduser()
        self.db_path = self.state_dir / DB_NAME

    @staticmethod
    def _connect(path: Path) -> sqlite3.Connection:
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        connection.executescript("""
            PRAGMA foreign_keys=ON;
            CREATE TABLE IF NOT EXISTS documents (
              doc_id TEXT PRIMARY KEY, sha256 TEXT NOT NULL UNIQUE, title TEXT NOT NULL,
              bytes INTEGER NOT NULL, pages INTEGER NOT NULL, chunks INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS files (
              relative_path TEXT PRIMARY KEY, sha256 TEXT NOT NULL, doc_id TEXT NOT NULL,
              status TEXT NOT NULL, FOREIGN KEY(doc_id) REFERENCES documents(doc_id)
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
              evidence_id UNINDEXED, doc_id UNINDEXED, title UNINDEXED, page UNINDEXED, text,
              tokenize='unicode61'
            );
        """)
        return connection

    def ingest(self, folder: str | Path) -> dict[str, Any]:
        source = Path(folder).expanduser()
        if not source.is_dir():
            raise ResearchFoundryError(f"PDF folder not found: {source}")
        pdfs = sorted((path for path in source.rglob("*") if path.is_file() and path.suffix.lower() == ".pdf"),
                      key=lambda path: path.relative_to(source).as_posix())
        if not pdfs:
            raise ResearchFoundryError("no PDF files found")
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ResearchFoundryError("PDF support requires the 'research' extra: pip install 'kora[research]'") from exc
        self.state_dir.mkdir(parents=True, exist_ok=True)
        counts = {"pdfs_discovered": len(pdfs), "documents_parsed": 0, "documents_reused": 0,
                  "duplicates_skipped": 0, "pages_parsed": 0, "chunks_indexed": 0,
                  "pages_reused": 0, "chunks_reused": 0, **ZERO_COUNTERS}
        records = []
        with self._connect(self.db_path) as conn:
            known = {row["sha256"]: row for row in conn.execute("SELECT * FROM documents")}
            for path in pdfs:
                relative = path.relative_to(source).as_posix()
                digest = _sha256(path)
                if digest in known:
                    row = known[digest]
                    prior = conn.execute("SELECT relative_path FROM files WHERE sha256=? ORDER BY relative_path LIMIT 1", (digest,)).fetchone()
                    status = "unchanged" if prior and prior["relative_path"] == relative else "exact_duplicate"
                    counts["documents_reused" if status == "unchanged" else "duplicates_skipped"] += 1
                    counts["pages_reused"] += row["pages"]
                    counts["chunks_reused"] += row["chunks"]
                    conn.execute("INSERT OR REPLACE INTO files VALUES (?,?,?,?)", (relative, digest, row["doc_id"], status))
                    records.append({"file": relative, "document_id": row["doc_id"], "status": status})
                    continue
                try:
                    reader = PdfReader(path)
                    title = _normalize(str((reader.metadata or {}).get("/Title") or path.stem))
                    page_texts = [_normalize(page.extract_text() or "") for page in reader.pages]
                except Exception as exc:
                    raise ResearchFoundryError(f"unreadable PDF '{relative}': {exc}") from exc
                if not page_texts or not any(page_texts):
                    raise ResearchFoundryError(f"PDF has no extractable text (OCR is not supported): {relative}")
                slug = re.sub(r"[^A-Za-z0-9.-]+", "-", path.stem).strip("-.") or "document"
                doc_id = f"doc-{slug}-{digest[:12]}"
                inserted = 0
                for page_number, text in enumerate(page_texts, 1):
                    for chunk_number, chunk in enumerate(_chunks(text), 1):
                        evidence_id = f"{doc_id}:p{page_number:03d}:c{chunk_number:03d}"
                        conn.execute("INSERT INTO chunks_fts VALUES (?,?,?,?,?)", (evidence_id, doc_id, title, page_number, chunk))
                        inserted += 1
                conn.execute("INSERT INTO documents VALUES (?,?,?,?,?,?)", (doc_id, digest, title, path.stat().st_size, len(page_texts), inserted))
                conn.execute("INSERT INTO files VALUES (?,?,?,?)", (relative, digest, doc_id, "parsed"))
                known[digest] = conn.execute("SELECT * FROM documents WHERE doc_id=?", (doc_id,)).fetchone()
                counts["documents_parsed"] += 1
                counts["pages_parsed"] += len(page_texts)
                counts["chunks_indexed"] += inserted
                records.append({"file": relative, "document_id": doc_id, "status": "parsed"})
        return {"operation": "research_ingest", "privacy_state": "Local Only", "state_dir": str(self.state_dir),
                "counters": counts, "events": records}

    def query(self, query: str, top_k: int = 5) -> dict[str, Any]:
        if not query.strip():
            raise ResearchFoundryError("query must not be empty")
        if top_k < 1:
            raise ResearchFoundryError("top_k must be at least 1")
        if not self.db_path.is_file():
            raise ResearchFoundryError(f"research state not found: {self.state_dir}")
        terms = re.findall(r"[\w]+", query, flags=re.UNICODE)
        records: list[dict[str, Any]] = []
        if terms:
            match = " OR ".join(f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms)
            with self._connect(self.db_path) as conn:
                rows = conn.execute("SELECT evidence_id,doc_id,title,page,text FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY bm25(chunks_fts), evidence_id LIMIT ?", (match, top_k)).fetchall()
            records = [{"title": row["title"], "doc_id": row["doc_id"], "page": int(row["page"]),
                        "evidence_id": row["evidence_id"], "text": row["text"]} for row in rows]
        allowed = {record["evidence_id"]: record for record in records}
        card = build_evidence_card(query, records, allowed_records=allowed)
        return {"operation": "research_query", "privacy_state": "Local Only",
                "events": [{"event": "lexical_retrieval", "deterministic": True, "retrieval_only": True,
                            "hits": len(records), **ZERO_COUNTERS}],
                "counters": {"queries": 1, "retrieval_hits": len(records), **ZERO_COUNTERS}, "card": card}
