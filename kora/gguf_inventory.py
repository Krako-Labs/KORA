"""Bounded, offline GGUF tensor-byte inspection; no model/runtime loading.

Supported layout constants are pinned in docs/gguf-tensor-inventory.md.
This inventories serialized tensors, not a reviewed text-model weight selection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import struct
import tempfile
from pathlib import Path
from typing import BinaryIO

PARSER_VERSION = "kora.gguf-inventory.v1"
# ggml-org/llama.cpp 9e71716247113b47bb831d1e0680cbf5f242f094
# type id -> (name, elements per block, serialized bytes per block).
_LAYOUTS = {
    0: ("F32", 1, 4),
    1: ("F16", 1, 2),
    2: ("Q4_0", 32, 18),
    3: ("Q4_1", 32, 20),
    6: ("Q5_0", 32, 22),
    7: ("Q5_1", 32, 24),
    8: ("Q8_0", 32, 34),
    9: ("Q8_1", 32, 40),
    10: ("Q2_K", 256, 84),
    11: ("Q3_K", 256, 110),
    12: ("Q4_K", 256, 144),
    13: ("Q5_K", 256, 176),
    14: ("Q6_K", 256, 210),
    15: ("Q8_K", 256, 292),
    30: ("BF16", 1, 2),
}
_SCALARS = {0: "B", 1: "b", 2: "H", 3: "h", 4: "I", 5: "i",
            6: "f", 7: "B", 10: "Q", 11: "q", 12: "d"}
_MAX_HEADER = 64 * 1024**2
_MAX_STRING = 16 * 1024**2
_MAX_ITEMS = 1_000_000
_MAX_TENSORS = 100_000


class GGUFInspectionError(ValueError):
    """The artifact cannot support a complete bounded byte inventory."""


class _Reader:
    def __init__(self, stream: BinaryIO, size: int):
        self.stream = stream
        self.size = size
        self.values_left = _MAX_ITEMS

    def read(self, count: int) -> bytes:
        end = self.stream.tell() + count
        if count < 0 or end > self.size or end > _MAX_HEADER:
            raise GGUFInspectionError("truncated file or header byte limit exceeded")
        data = self.stream.read(count)
        if len(data) != count:
            raise GGUFInspectionError("truncated file")
        return data

    def number(self, fmt: str):
        return struct.unpack("<" + fmt, self.read(struct.calcsize("<" + fmt)))[0]

    def string(self, limit: int = _MAX_STRING) -> str:
        length = self.number("Q")
        if length > limit:
            raise GGUFInspectionError("string length limit exceeded")
        try:
            return self.read(length).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise GGUFInspectionError("invalid UTF-8 string") from exc

    def value(self, kind: int, depth: int = 0):
        self.values_left -= 1
        if self.values_left < 0 or depth > 8:
            raise GGUFInspectionError("metadata item or nesting limit exceeded")
        if kind in _SCALARS:
            value = self.number(_SCALARS[kind])
            if kind == 7 and value not in (0, 1):
                raise GGUFInspectionError("invalid boolean metadata")
            return value
        if kind == 8:
            return self.string()
        if kind == 9:
            element_kind, count = self.number("I"), self.number("Q")
            if element_kind not in {*_SCALARS, 8, 9} or count > self.values_left:
                raise GGUFInspectionError("unsupported array type or item limit")
            for _ in range(count):
                self.value(element_kind, depth + 1)
            return None  # Never retain tokenizer arrays or arbitrary metadata.
        raise GGUFInspectionError("unsupported metadata type")


def _parse(stream: BinaryIO, size: int) -> dict:
    reader = _Reader(stream, size)
    if reader.read(4) != b"GGUF":
        raise GGUFInspectionError("invalid GGUF magic")
    version = reader.number("I")
    if version not in (2, 3):
        raise GGUFInspectionError("unsupported GGUF version or byte order")
    tensor_count, metadata_count = reader.number("Q"), reader.number("Q")
    if not 0 < tensor_count <= _MAX_TENSORS or metadata_count > _MAX_ITEMS:
        raise GGUFInspectionError("invalid tensor or metadata count")
    alignment = 32
    metadata_keys: set[str] = set()
    for _ in range(metadata_count):
        key = reader.string(65535)
        if not key or not key.isascii() or key in metadata_keys:
            raise GGUFInspectionError("invalid or duplicate metadata key")
        metadata_keys.add(key)
        kind = reader.number("I")
        value = reader.value(kind)
        if key == "general.alignment":
            if kind != 4 or not 1 <= value <= 65536 or value & (value - 1):
                raise GGUFInspectionError("invalid tensor alignment")
            alignment = value
        if key.startswith("split."):
            raise GGUFInspectionError("split artifacts require a separate shard contract")

    tensors: list[dict] = []
    names: set[str] = set()
    for _ in range(tensor_count):
        name = reader.string(64)
        if not name or "\0" in name or name in names:
            raise GGUFInspectionError("invalid or duplicate tensor name")
        names.add(name)
        rank = reader.number("I")
        if not 1 <= rank <= 4:
            raise GGUFInspectionError("unsupported tensor rank")
        dimensions = [reader.number("Q") for _ in range(rank)]
        kind, offset = reader.number("I"), reader.number("Q")
        if kind not in _LAYOUTS:
            raise GGUFInspectionError("unsupported tensor type")
        label, block_size, block_bytes = _LAYOUTS[kind]
        if any(d == 0 for d in dimensions) or dimensions[0] % block_size:
            raise GGUFInspectionError("invalid tensor dimensions or quantized row")
        payload_bytes = math.prod(dimensions) // block_size * block_bytes
        if payload_bytes > size or offset % alignment:
            raise GGUFInspectionError("tensor size or alignment invalid")
        tensors.append({
            "name": name, "ggml_type": kind, "dtype": label,
            "dimensions_ggml_order": dimensions,
            "data_offset": offset, "payload_bytes": payload_bytes,
        })
    header_end = stream.tell()
    data_start = (header_end + alignment - 1) // alignment * alignment
    end = data_start
    for tensor in sorted(tensors, key=lambda item: item["data_offset"]):
        start = data_start + tensor["data_offset"]
        if start < end:
            raise GGUFInspectionError("overlapping tensor payloads")
        end = start + tensor["payload_bytes"]
        if end > size:
            raise GGUFInspectionError("tensor payload exceeds file size")
        tensor["file_offset"] = start
    total = sum(t["payload_bytes"] for t in tensors)
    return {
        "schema_version": PARSER_VERSION,
        "gguf_version": version, "byte_order": "little",
        "alignment": alignment, "data_start": data_start,
        "artifact_bytes": size, "tensor_count": tensor_count,
        "serialized_tensor_payload_bytes": total,
        "non_tensor_bytes": size - total, "tensors": tensors,
        "tensor_scope": "all_serialized_tensors_in_one_file",
        "text_model_weight_bytes": None,
        "text_tensor_selection_reviewed": False,
        "claim_boundary": (
            "Static single-file byte inventory only. Text-weight membership, "
            "model completeness, provenance/license, runtime compatibility, "
            "physical VRAM, performance and service quality are not established."
        ),
    }


def inspect_gguf(path: str | os.PathLike[str]) -> dict:
    """Inspect one regular little-endian GGUF v2/v3 file without loading tensors.

    Unknown types and split metadata fail closed. The SHA-256 covers the complete
    file, while byte totals exclude metadata, padding and gaps between tensors.
    All tensors remain inventoried; text-only membership requires separate review.
    """
    source = Path(path)
    if source.is_symlink():
        raise GGUFInspectionError("symbolic-link artifacts are not supported")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(source, flags)
        with os.fdopen(fd, "rb") as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise GGUFInspectionError("artifact must be a regular file")
            inventory = _parse(stream, before.st_size)
            stream.seek(0)
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024**2), b""):
                digest.update(chunk)
            after = os.fstat(stream.fileno())
            fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")
            if any(getattr(before, f) != getattr(after, f) for f in fields):
                raise GGUFInspectionError("artifact changed during inspection")
            inventory["artifact_sha256"] = digest.hexdigest()
            inventory["parser_source_sha256"] = hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest()
            inventory["layout_reference_revision"] = (
                "9e71716247113b47bb831d1e0680cbf5f242f094"
            )
            return inventory
    except OSError as exc:
        raise GGUFInspectionError("artifact could not be read safely") from exc


def write_inventory(path: str | os.PathLike[str], inventory: dict) -> None:
    """Publish complete JSON exclusively; never overwrite an earlier receipt."""
    target = Path(path)
    payload = json.dumps(inventory, indent=2, sort_keys=True, allow_nan=False) + "\n"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=target.parent, delete=False,
        ) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        inventory = inspect_gguf(args.artifact)
        write_inventory(args.output, inventory)
    except (GGUFInspectionError, OSError, ValueError):
        print(json.dumps({"status": "rejected", "reason": "artifact_or_output_invalid"}))
        return 1
    print(json.dumps({
        "status": "inventoried",
        "artifact_sha256": inventory["artifact_sha256"],
        "serialized_tensor_payload_bytes": inventory["serialized_tensor_payload_bytes"],
        "text_model_weight_bytes": None,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
