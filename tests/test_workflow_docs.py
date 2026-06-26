from __future__ import annotations

import shutil
from pathlib import Path

from scripts import validate_workflow_docs as validator


def _copy_required_docs(tmp_path: Path) -> Path:
    for required in validator.REQUIRED_DOCS:
        source = validator.REPO_ROOT / required.path
        destination = tmp_path / required.path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    return tmp_path


def test_valid_current_docs_pass() -> None:
    assert validator.validate() == []


def test_missing_required_file_fails(tmp_path: Path) -> None:
    root = _copy_required_docs(tmp_path)
    (root / "AGENTS.md").unlink()

    errors = validator.validate(root)

    assert any("missing required doc: AGENTS.md" in error for error in errors)


def test_missing_queue_task_ids_fails(tmp_path: Path) -> None:
    root = _copy_required_docs(tmp_path)
    queue = root / "docs/context/WORKFLOW_QUEUE.md"
    queue.write_text(
        queue.read_text(encoding="utf-8").replace("CIL-006", "TASK-006").replace("CIL-007", "TASK-007"),
        encoding="utf-8",
    )

    errors = validator.validate(root)

    assert any("expected at least 6 task ids" in error for error in errors)


def test_missing_risk_levels_fails(tmp_path: Path) -> None:
    root = _copy_required_docs(tmp_path)
    risk = root / "docs/context/WORKFLOW_RISK_CLASSIFICATION.md"
    risk.write_text(risk.read_text(encoding="utf-8").replace("High Risk", "Escalated Risk"), encoding="utf-8")

    errors = validator.validate(root)

    assert any("missing required phrase: High Risk" in error for error in errors)


def test_missing_final_classifications_fails(tmp_path: Path) -> None:
    root = _copy_required_docs(tmp_path)
    protocol = root / "docs/context/WORKFLOW_SELF_REVIEW_PROTOCOL.md"
    protocol.write_text(protocol.read_text(encoding="utf-8").replace("needs-r1", "requires patch"), encoding="utf-8")

    errors = validator.validate(root)

    assert any("missing required phrase: needs-r1" in error for error in errors)


def test_missing_approval_gates_fails(tmp_path: Path) -> None:
    root = _copy_required_docs(tmp_path)
    gates = root / "docs/context/WORKFLOW_ESCALATION_GATES.md"
    gates.write_text(gates.read_text(encoding="utf-8").replace("provider calls", "external calls"), encoding="utf-8")

    errors = validator.validate(root)

    assert any("missing required phrase: provider calls" in error for error in errors)


def test_missing_multi_agent_one_writer_or_read_only_language_fails(tmp_path: Path) -> None:
    root = _copy_required_docs(tmp_path)
    model = root / "docs/context/WORKFLOW_MULTI_ACTOR_OPERATING_MODEL.md"
    text = model.read_text(encoding="utf-8")
    text = text.replace("One writer per branch", "Single active editor")
    text = text.replace("Reviewer/checker agents are read-only by default", "Reviewers inspect by default")
    model.write_text(text, encoding="utf-8")

    errors = validator.validate(root)

    assert any("missing required phrase: One writer per branch" in error for error in errors)
    assert any("missing required phrase: Reviewer/checker agents are read-only by default" in error for error in errors)


def test_hidden_control_unicode_detection_fails(tmp_path: Path) -> None:
    root = _copy_required_docs(tmp_path)
    agents = root / "AGENTS.md"
    agents.write_bytes(agents.read_bytes() + b"\x00")

    errors = validator.validate(root)

    assert any("hidden/control byte" in error for error in errors)
