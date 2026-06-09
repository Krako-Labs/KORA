from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from kora.cli import main as cli_main


def test_telemetry_missing_input() -> None:
    """Telemetry command exits non-zero and shows a clear error when --input is absent."""
    result = subprocess.run(
        [sys.executable, "-m", "kora", "telemetry"],
        capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "--input" in result.stderr
    assert "required" in result.stderr.lower()


def test_telemetry_input_file_not_found() -> None:
    """Telemetry command exits non-zero with a helpful message when the input file doesn't exist."""
    result = subprocess.run(
        [sys.executable, "-m", "kora", "telemetry", "--input", "/tmp/no_such_file.json"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    # No raw Python traceback should leak to the user
    assert "Traceback" not in result.stderr
    assert "FileNotFoundError" not in result.stderr
    # The path and context should be visible in the error
    assert "no_such_file.json" in result.stderr
    assert "run JSON" in result.stderr


def test_telemetry_input_not_a_file() -> None:
    """Telemetry command fails cleanly when --input points to a directory."""
    result = subprocess.run(
        [sys.executable, "-m", "kora", "telemetry", "--input", "/tmp"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "KORA run" in result.stderr


def test_telemetry_load_json_missing_file_error_message(tmp_path: Path) -> None:
    """load_json raises FileNotFoundError with a helpful message when the file does not exist."""
    from kora.telemetry import load_json

    missing = tmp_path / "does_not_exist.json"
    try:
        load_json(missing)
        assert False, "should have raised FileNotFoundError"
    except FileNotFoundError as e:
        msg = str(e)
        assert str(missing) in msg
        assert "run JSON" in msg
        assert "Provide the path to a KORA run" in msg


def test_telemetry_load_json_directory_error_message(tmp_path: Path) -> None:
    """load_json raises IsADirectoryError with a helpful message when the path is a directory."""
    from kora.telemetry import load_json

    try:
        load_json(tmp_path)
        assert False, "should have raised IsADirectoryError"
    except IsADirectoryError as e:
        msg = str(e)
        assert str(tmp_path) in msg
        assert "directory" in msg
        assert "Provide the path to a KORA run" in msg
