from __future__ import annotations

import json
from pathlib import Path

from kora.cli import main


REPO_ROOT = Path(__file__).resolve().parents[1]
HELLO_SOLUTION = REPO_ROOT / "examples" / "solutions" / "hello-solution"


def test_solution_validate_cli_json(capsys) -> None:
    exit_code = main(["solution", "validate", str(HELLO_SOLUTION), "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload["status"] == "valid"
    assert payload["solution_id"] == "example.hello"
    assert payload["execution_performed"] is False


def test_solution_validate_cli_reports_missing_capability(capsys) -> None:
    exit_code = main(
        [
            "solution",
            "validate",
            str(HELLO_SOLUTION),
            "--capability",
            "text.normalize",
            "--json",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    payload = json.loads(captured.err)
    assert payload["status"] == "invalid"
    assert payload["issues"][0]["code"] == "missing_capability"
