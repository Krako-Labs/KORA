from __future__ import annotations

import hashlib
import json
import os
import struct
import subprocess
import sys

import pytest

from kora import gguf_inventory as module
from kora.gguf_inventory import GGUFInspectionError, inspect_gguf, write_inventory


def string(value: str) -> bytes:
    data = value.encode()
    return struct.pack("<Q", len(data)) + data


def fixture(tensors=None, metadata=None, alignment=32, version=3, trailing=0):
    """A tiny GGUF wire writer, independent of the production layout table."""
    if tensors is None:
        tensors = [("embedding", [3, 2], 0, 0, 24), ("output", [256], 12, 64, 144)]
    if metadata is None:
        metadata = [("general.alignment", 4, struct.pack("<I", alignment))]
    raw = b"GGUF" + struct.pack("<IQQ", version, len(tensors), len(metadata))
    for key, kind, value in metadata:
        raw += string(key) + struct.pack("<I", kind) + value
    for name, dims, kind, offset, _size in tensors:
        raw += string(name) + struct.pack("<I", len(dims))
        raw += b"".join(struct.pack("<Q", d) for d in dims)
        raw += struct.pack("<IQ", kind, offset)
    data_start = (len(raw) + alignment - 1) // alignment * alignment
    raw += bytes(data_start - len(raw))
    size = max((offset + size for _, _, _, offset, size in tensors), default=0)
    return raw + bytes(size + trailing), data_start


def save(tmp_path, raw):
    path = tmp_path / "fixture.gguf"
    path.write_bytes(raw)
    return path


@pytest.mark.parametrize("version", [2, 3])
def test_payload_excludes_metadata_padding_gaps_and_trailer(tmp_path, version):
    raw, start = fixture(version=version, trailing=37)
    result = inspect_gguf(save(tmp_path, raw))
    assert result["serialized_tensor_payload_bytes"] == 168
    assert result["artifact_bytes"] == len(raw)
    assert result["non_tensor_bytes"] == len(raw) - 168
    assert result["data_start"] == start
    assert [t["file_offset"] for t in result["tensors"]] == [start, start + 64]
    assert result["artifact_sha256"] == hashlib.sha256(raw).hexdigest()
    assert result["text_model_weight_bytes"] is None
    assert result["text_tensor_selection_reviewed"] is False
    assert str(tmp_path) not in json.dumps(result)


@pytest.mark.parametrize("kind,width,block_bytes", [
    (0, 1, 4), (1, 1, 2), (2, 32, 18), (3, 32, 20),
    (6, 32, 22), (7, 32, 24), (8, 32, 34), (9, 32, 40),
    (10, 256, 84), (11, 256, 110), (12, 256, 144),
    (13, 256, 176), (14, 256, 210), (15, 256, 292), (30, 1, 2),
])
def test_supported_layout_bytes_for_multiple_rows(tmp_path, kind, width, block_bytes):
    raw, _ = fixture([("weights", [width * 2, 3], kind, 0, block_bytes * 6)])
    result = inspect_gguf(save(tmp_path, raw))
    assert result["serialized_tensor_payload_bytes"] == block_bytes * 6


def test_metadata_scalar_string_array_and_nested_array_are_skipped(tmp_path):
    metadata = [
        ("tokenizer.tokens", 9, struct.pack("<IQ", 8, 2) + string("x") + string("y")),
        ("example.nested", 9, struct.pack("<IQIQI", 9, 1, 4, 1, 123)),
        ("example.name", 8, string("metadata with UTF-8: \uac00")),
    ]
    for kind, fmt in [(0, "B"), (1, "b"), (2, "H"), (3, "h"), (4, "I"),
                      (5, "i"), (6, "f"), (7, "B"), (10, "Q"), (11, "q"), (12, "d")]:
        metadata.append((f"example.scalar_{kind}", kind, struct.pack("<" + fmt, 1)))
    raw, _ = fixture(metadata=metadata)
    result = inspect_gguf(save(tmp_path, raw))
    assert result["serialized_tensor_payload_bytes"] == 168
    assert "tokenizer" not in json.dumps(result)


@pytest.mark.parametrize("alignment", [1, 16, 64])
def test_alignment_from_metadata(tmp_path, alignment):
    raw, start = fixture([("weight", [2], 1, alignment, 4)], alignment=alignment)
    result = inspect_gguf(save(tmp_path, raw))
    assert result["data_start"] == start
    assert result["tensors"][0]["file_offset"] == start + alignment


@pytest.mark.parametrize("tensors", [
    [("w", [1], 999, 0, 4)],
    [("w", [0], 0, 0, 4)],
    [("w", [], 0, 0, 4)],
    [("w", [1, 1, 1, 1, 1], 0, 0, 4)],
    [("w", [16, 2], 2, 0, 18)],
    [("w", [1], 0, 1, 4)],
    [("w", [2**63, 2**63], 0, 0, 4)],
    [("", [1], 0, 0, 4)],
    [("x" * 65, [1], 0, 0, 4)],
    [("x\0", [1], 0, 0, 4)],
    [("w", [1], 0, 0, 4), ("w", [1], 0, 32, 4)],
    [("a", [16], 0, 0, 64), ("b", [1], 0, 32, 4)],
])
def test_invalid_tensor_descriptors_fail_closed(tmp_path, tensors):
    raw, _ = fixture(tensors)
    with pytest.raises(GGUFInspectionError):
        inspect_gguf(save(tmp_path, raw))


@pytest.mark.parametrize("metadata", [
    [("general.alignment", 4, struct.pack("<I", 0))],
    [("general.alignment", 4, struct.pack("<I", 3))],
    [("general.alignment", 4, struct.pack("<I", 131072))],
    [("general.alignment", 8, string("32"))],
    [("same", 0, b"\0"), ("same", 0, b"\0")],
    [("", 0, b"\0")],
    [("\uac00", 0, b"\0")],
    [("flag", 7, b"\x02")],
    [("unknown", 13, b"")],
    [("bad_array", 9, struct.pack("<IQ", 88, 0))],
    [("many", 9, struct.pack("<IQ", 0, 2**63))],
    [("split.count", 2, struct.pack("<H", 2))],
    [("long", 8, struct.pack("<Q", 2**63))],
    [("unicode", 8, struct.pack("<Q", 1) + b"\xff")],
])
def test_invalid_or_unsupported_metadata_fail_closed(tmp_path, metadata):
    raw, _ = fixture(metadata=metadata)
    with pytest.raises(GGUFInspectionError):
        inspect_gguf(save(tmp_path, raw))


def test_truncation_at_every_required_byte_rejected(tmp_path):
    raw, _ = fixture()
    path = tmp_path / "truncated.gguf"
    for count in range(len(raw)):
        path.write_bytes(raw[:count])
        with pytest.raises(GGUFInspectionError):
            inspect_gguf(path)


@pytest.mark.parametrize("header", [
    b"GGML" + struct.pack("<IQQ", 3, 1, 0),
    b"GGUF" + struct.pack(">IQQ", 3, 1, 0),
    b"GGUF" + struct.pack("<IQQ", 1, 1, 0),
    b"GGUF" + struct.pack("<IQQ", 3, 0, 0),
    b"GGUF" + struct.pack("<IQQ", 3, 2**63, 0),
    b"GGUF" + struct.pack("<IQQ", 3, 1, 2**63),
])
def test_invalid_headers_rejected(tmp_path, header):
    with pytest.raises(GGUFInspectionError):
        inspect_gguf(save(tmp_path, header))


def test_nested_metadata_budget_and_header_limit(tmp_path, monkeypatch):
    nested = struct.pack("<IQ", 0, 1) + b"\0"
    for _ in range(10):
        nested = struct.pack("<IQ", 9, 1) + nested
    raw, _ = fixture(metadata=[("deep", 9, nested)])
    with pytest.raises(GGUFInspectionError, match="nesting"):
        inspect_gguf(save(tmp_path, raw))
    raw, _ = fixture()
    monkeypatch.setattr(module, "_MAX_HEADER", 30)
    with pytest.raises(GGUFInspectionError, match="header"):
        inspect_gguf(save(tmp_path, raw))


def test_nonregular_and_symlink_inputs_rejected(tmp_path):
    raw, _ = fixture()
    path = save(tmp_path, raw)
    link = tmp_path / "link.gguf"
    link.symlink_to(path)
    for item in (link, tmp_path, tmp_path / "absent"):
        with pytest.raises(GGUFInspectionError):
            inspect_gguf(item)
    if hasattr(os, "mkfifo"):
        fifo = tmp_path / "fifo"
        os.mkfifo(fifo)
        with pytest.raises(GGUFInspectionError):
            inspect_gguf(fifo)


def test_input_mutation_is_rejected(tmp_path, monkeypatch):
    raw, _ = fixture()
    path = save(tmp_path, raw)
    original = module._parse

    def mutate(stream, size):
        result = original(stream, size)
        with path.open("ab") as target:
            target.write(b"x")
        return result

    monkeypatch.setattr(module, "_parse", mutate)
    with pytest.raises(GGUFInspectionError, match="changed"):
        inspect_gguf(path)


def test_inventory_is_stable_and_output_is_exclusive(tmp_path):
    raw, _ = fixture()
    path = save(tmp_path, raw)
    result = inspect_gguf(path)
    assert result == inspect_gguf(path)
    output = tmp_path / "inventory.json"
    write_inventory(output, result)
    before = output.read_bytes()
    with pytest.raises(FileExistsError):
        write_inventory(output, result)
    assert output.read_bytes() == before
    link = tmp_path / "receipt-link"
    link.symlink_to(output)
    with pytest.raises(FileExistsError):
        write_inventory(link, result)
    assert output.read_bytes() == before
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "fixture.gguf", "inventory.json", "receipt-link",
    ]


def test_cli_success_and_rejection_leave_original_receipt_unchanged(tmp_path):
    raw, _ = fixture()
    artifact = save(tmp_path, raw)
    output = tmp_path / "inventory.json"
    cmd = [sys.executable, "-m", "kora.gguf_inventory", str(artifact),
           "--output", str(output)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert json.loads(result.stdout)["text_model_weight_bytes"] is None
    before = output.read_bytes()
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "rejected"
    assert output.read_bytes() == before


def test_invalid_cli_artifact_writes_no_receipt(tmp_path):
    artifact = save(tmp_path, b"broken")
    output = tmp_path / "inventory.json"
    result = subprocess.run(
        [sys.executable, "-m", "kora.gguf_inventory", str(artifact),
         "--output", str(output)], capture_output=True, text=True, check=False,
    )
    assert result.returncode == 1
    assert not output.exists()
