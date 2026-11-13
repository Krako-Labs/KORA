from __future__ import annotations

import subprocess

from kora.cli import _discover_examples, _print_examples_list, _run_example
from kora.cli import main as cli_main


UNKNOWN_NAME = "definitely-not-a-real-example"


def _forbidden_run(*args, **kwargs):
    raise AssertionError("unknown example must not spawn a subprocess")


def test_run_unknown_example_returns_2_and_lists_available(capsys, monkeypatch):
    """Unknown example names fail closed: exit 2, name the problem, list options.

    Regression coverage for #207: running an unknown example name must fail
    clearly and suggest listing the available examples, without spawning
    any subprocess for the non-existent example.
    """
    monkeypatch.setattr(subprocess, "run", _forbidden_run)

    exit_code = _run_example(UNKNOWN_NAME, [])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert f"Unknown example: {UNKNOWN_NAME}" in captured.err
    assert "Available examples:" in captured.err
    names = [str(example["name"]) for example in _discover_examples()]
    assert names
    for name in names:
        assert name in captured.err


def test_run_unknown_example_via_cli(capsys, monkeypatch):
    """`kora run <unknown>` exits 2 and points at the available examples."""
    monkeypatch.setattr(subprocess, "run", _forbidden_run)

    exit_code = cli_main(["run", UNKNOWN_NAME])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert f"Unknown example: {UNKNOWN_NAME}" in captured.err
    assert "Available examples:" in captured.err


def test_examples_list_shows_known_examples(capsys):
    """`kora examples list` prints every discovered example.

    This is the listing the unknown-example error message points users at,
    so it must actually contain the runnable examples.
    """
    _print_examples_list()

    captured = capsys.readouterr()
    assert "Runnable examples" in captured.out
    names = [str(example["name"]) for example in _discover_examples()]
    assert names
    for name in names:
        assert name in captured.out
