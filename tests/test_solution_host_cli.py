from __future__ import annotations

import json
from pathlib import Path

from kora.cli import main

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_SOLUTION = REPO_ROOT / "examples" / "solutions" / "document-transform-fixture"


def test_solution_host_cli_lifecycle_json(
    tmp_path: Path,
    capsys,
) -> None:
    store = tmp_path / "host"
    input_path = tmp_path / "input.json"
    input_path.write_text(
        json.dumps({"text": "  Alpha   value  "}),
        encoding="utf-8",
    )

    assert main(
        [
            "solution",
            "install",
            str(DOCUMENT_SOLUTION),
            "--store",
            str(store),
            "--json",
        ]
    ) == 0
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["solution"]["id"] == "example.document-transform"

    assert main(
        [
            "solution",
            "run",
            "example.document-transform",
            "--store",
            str(store),
            "--input",
            str(input_path),
            "--json",
        ]
    ) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["output"] == {"text": "Alpha value"}

    assert main(
        [
            "solution",
            "status",
            result["run_id"],
            "--store",
            str(store),
            "--json",
        ]
    ) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["lifecycle_state"] == "succeeded"

    assert main(
        [
            "solution",
            "result",
            result["run_id"],
            "--store",
            str(store),
            "--json",
        ]
    ) == 0
    persisted = json.loads(capsys.readouterr().out)
    assert persisted == result


def test_solution_run_cli_returns_machine_readable_failure(
    tmp_path: Path,
    capsys,
) -> None:
    store = tmp_path / "host"
    input_path = tmp_path / "invalid-input.json"
    input_path.write_text(json.dumps({"wrong": "field"}), encoding="utf-8")
    assert main(
        [
            "solution",
            "install",
            str(DOCUMENT_SOLUTION),
            "--store",
            str(store),
            "--json",
        ]
    ) == 0
    capsys.readouterr()

    assert main(
        [
            "solution",
            "run",
            "example.document-transform",
            "--store",
            str(store),
            "--input",
            str(input_path),
            "--json",
        ]
    ) == 1
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert captured.err == ""
    assert result["lifecycle_state"] == "failed"
    assert result["error"]["code"] == "input_validation_failed"
