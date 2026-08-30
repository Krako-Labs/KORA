from __future__ import annotations

import json

import pytest

from kora.cli import main


def test_system_inventory_cli_prints_json(capsys) -> None:
    rc = main(["system", "inventory", "--json"])
    captured = capsys.readouterr()

    assert rc == 0
    data = json.loads(captured.out)
    assert data["schema_version"] == "kora_foundation_device_inventory_v0"
    assert data["collection_scope"] == "local_metadata_only"
    assert data["sensitive_identifiers_collected"] is False
    assert "runtime_candidates" in data
    assert "transports" in data


def test_system_inventory_cli_writes_json_file(tmp_path, capsys) -> None:
    output = tmp_path / "inventory.json"

    rc = main(["system", "inventory", "--json-out", str(output)])
    captured = capsys.readouterr()

    assert rc == 0
    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["schema_version"] == "kora_foundation_device_inventory_v0"
    assert "Saved JSON:" in captured.out
    assert "KORA Foundation Device Inventory" in captured.out


def test_system_fleet_cli_combines_inventory_files_deterministically(tmp_path, capsys) -> None:
    paths = []
    for label in ("z-node", "a-node"):
        path = tmp_path / f"{label}.json"
        assert main(["system", "inventory", "--json-out", str(path)]) == 0
        data = json.loads(path.read_text(encoding="utf-8"))
        data["node_name"] = label
        path.write_text(json.dumps(data), encoding="utf-8")
        paths.append(path)
        capsys.readouterr()

    rc = main(["system", "fleet", str(paths[0]), str(paths[1]), "--json"])
    data = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert data["node_count"] == 2
    assert [node["node_label"] for node in data["nodes"]] == ["a-node", "z-node"]
    assert data["evidence_state"] == "DETECTED"


def test_system_fleet_cli_rejects_duplicate_and_malformed_inputs(tmp_path, capsys) -> None:
    inventory_path = tmp_path / "node.json"
    assert main(["system", "inventory", "--json-out", str(inventory_path)]) == 0
    capsys.readouterr()

    with pytest.raises(SystemExit, match="2"):
        main(["system", "fleet", str(inventory_path), str(inventory_path)])
    assert "duplicate node labels" in capsys.readouterr().err

    malformed_path = tmp_path / "malformed.json"
    malformed_path.write_text("not-json", encoding="utf-8")
    with pytest.raises(SystemExit, match="2"):
        main(["system", "fleet", str(malformed_path)])
    assert "cannot load inventory" in capsys.readouterr().err
