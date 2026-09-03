from __future__ import annotations

import json
from pathlib import Path

import pytest

from kora.cli import main
from kora.solution import (
    SolutionAuthoringError,
    integrity_file_digests,
    package_digest,
    package_file_digests,
    run_solution_conformance,
    scaffold_solution,
    validate_solution_package,
)


def _tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_scaffold_is_deterministic_valid_and_conforming(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"

    first_report = scaffold_solution("example.scaffold", first)
    second_report = scaffold_solution("example.scaffold", second)

    assert _tree_bytes(first) == _tree_bytes(second)
    assert first_report["package_digest"] == second_report["package_digest"]
    assert first_report["activity"] == {
        "execution_performed": False,
        "network_accessed": False,
        "model_inference_performed": False,
        "gpu_execution_performed": False,
    }
    validation = validate_solution_package(first)
    assert validation["solution_id"] == "example.scaffold"
    conformance = run_solution_conformance(first)
    assert conformance["package"]["digest"] == first_report["package_digest"]
    assert conformance["status"] == "passed"
    assert conformance["summary"] == {"total": 1, "passed": 1, "failed": 0}


@pytest.mark.parametrize("solution_id", ["Bad Id", "ab", "../escape", "example/escape"])
def test_scaffold_rejects_invalid_solution_id(tmp_path: Path, solution_id: str) -> None:
    with pytest.raises(SolutionAuthoringError) as captured:
        scaffold_solution(solution_id, tmp_path / "package")

    assert captured.value.code == "invalid_solution_id"
    assert not (tmp_path / "package").exists()


def test_checked_in_generated_fixture_is_exact_scaffold_output(tmp_path: Path) -> None:
    generated = tmp_path / "generated"
    scaffold_solution("example.generated-echo", generated)

    checked_in = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "solutions"
        / "generated-echo-fixture"
    )
    assert _tree_bytes(generated) == _tree_bytes(checked_in)


def test_scaffold_never_overwrites_existing_output(tmp_path: Path) -> None:
    target = tmp_path / "existing"
    target.mkdir()
    marker = target / "owned.txt"
    marker.write_text("preserve", encoding="utf-8")

    with pytest.raises(SolutionAuthoringError) as captured:
        scaffold_solution("example.safe", target)

    assert captured.value.code == "output_exists"
    assert marker.read_text(encoding="utf-8") == "preserve"


@pytest.mark.parametrize("relative", ["", "../outside.txt", "/absolute.txt", "solution.json"])
def test_integrity_helper_rejects_unsafe_or_self_referential_paths(
    tmp_path: Path,
    relative: str,
) -> None:
    package = tmp_path / "package"
    scaffold_solution("example.integrity", package)

    with pytest.raises(SolutionAuthoringError) as captured:
        integrity_file_digests(package, [relative])

    assert captured.value.code == "invalid_integrity_path"


def test_integrity_helper_hashes_explicit_files(tmp_path: Path) -> None:
    package = tmp_path / "package"
    scaffold_solution("example.integrity", package)

    digests = integrity_file_digests(package, ["graph/workflow.json"])

    assert list(digests) == ["graph/workflow.json"]
    assert len(digests["graph/workflow.json"]) == 64


def test_package_digest_rejects_symlinked_files(tmp_path: Path) -> None:
    package = tmp_path / "package"
    package.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    (package / "linked.txt").symlink_to(outside)

    with pytest.raises(SolutionAuthoringError) as captured:
        package_file_digests(package)

    assert captured.value.code == "invalid_package"


def test_package_digest_changes_with_package_content(tmp_path: Path) -> None:
    package = tmp_path / "package"
    scaffold_solution("example.digest", package)
    before = package_digest(package)
    (package / "README.md").write_text("changed\n", encoding="utf-8")

    assert package_digest(package) != before


def test_scaffold_and_conform_cli_json(tmp_path: Path, capsys) -> None:
    package = tmp_path / "cli-package"

    assert main(
        [
            "solution",
            "scaffold",
            "example.cli-scaffold",
            "--output",
            str(package),
            "--json",
        ]
    ) == 0
    scaffold_report = json.loads(capsys.readouterr().out)
    assert scaffold_report["status"] == "created"

    assert main(["solution", "conform", str(package), "--json"]) == 0
    conformance = json.loads(capsys.readouterr().out)
    assert conformance["status"] == "passed"
    assert conformance["activity"]["network_accessed"] is False


def test_scaffold_cli_failure_is_machine_readable(tmp_path: Path, capsys) -> None:
    target = tmp_path / "existing"
    target.mkdir()

    assert main(
        [
            "solution",
            "scaffold",
            "example.existing",
            "--output",
            str(target),
            "--json",
        ]
    ) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert json.loads(captured.err)["error"]["code"] == "output_exists"
