from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class RequiredDoc:
    path: str
    phrases: tuple[str, ...]


REQUIRED_DOCS: tuple[RequiredDoc, ...] = (
    RequiredDoc(
        "AGENTS.md",
        (
            "AI Workload Control Layer",
            "origin/main",
            "fresh clean worktree",
            "Codex pass is not merge-ready pass",
            "merge-ready",
            "needs-r1",
            "needs-cto-review",
            "blocked",
            "output-quality proof",
        ),
    ),
    RequiredDoc(
        "docs/context/CODEX_INNER_LOOP_QUEUE.md",
        (
            "CIL-001",
            "CIL-002",
            "CIL-003",
            "CIL-004",
            "CIL-005",
            "CIL-006",
            "claim boundaries",
        ),
    ),
    RequiredDoc(
        "docs/context/CODEX_SELF_REVIEW_PROTOCOL.md",
        (
            "changed files vs allowed scope",
            "local-only ChatGPT context untouched",
            "merge-ready",
            "needs-r1",
            "needs-cto-review",
            "blocked",
            "output-quality proof",
        ),
    ),
    RequiredDoc(
        "docs/context/CODEX_RISK_CLASSIFICATION.md",
        (
            "Low Risk",
            "Medium Risk",
            "High Risk",
            "Codex pass is not merge-ready pass",
            "output-quality proof",
        ),
    ),
    RequiredDoc(
        "docs/context/CODEX_ESCALATION_GATES.md",
        (
            "merge",
            "release",
            "PyPI publication",
            "provider calls",
            "H100/GPU/CUDA/server/remote execution",
            "local-only ChatGPT context changes",
            "output-quality proof",
        ),
    ),
    RequiredDoc(
        "docs/context/CODEX_APPROVAL_PACKET.md",
        (
            "decision needed",
            "risk level",
            "final status classification",
            "Albert action options: Merge / Request R1 / Stop / CTO Review",
            "output-quality proof",
        ),
    ),
    RequiredDoc(
        "docs/context/CODEX_MULTI_AGENT_OPERATING_MODEL.md",
        (
            "One writer per branch",
            "Reviewer/checker agents are read-only by default",
            "separate worktrees",
            "No auto-merge",
            "output-quality proof",
        ),
    ),
    RequiredDoc(
        "docs/reports/codex_inner_loop_run_template.md",
        (
            "loop count",
            "repair attempts",
            "Validation Results",
            "final status classification",
            "Approval Packet",
            "output-quality proof",
        ),
    ),
)

BIDI_CODEPOINTS = {
    0x061C,
    0x200E,
    0x200F,
    0x202A,
    0x202B,
    0x202C,
    0x202D,
    0x202E,
    0x2066,
    0x2067,
    0x2068,
    0x2069,
}


def _bad_control_offsets(data: bytes) -> list[tuple[int, int]]:
    allowed = {0x09, 0x0A, 0x0D} | set(range(0x20, 0x7F))
    return [(offset, byte) for offset, byte in enumerate(data) if byte not in allowed]


def _bad_bidi_offsets(text: str) -> list[tuple[int, str]]:
    return [(index, char) for index, char in enumerate(text) if ord(char) in BIDI_CODEPOINTS]


def validate(root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []

    for required in REQUIRED_DOCS:
        path = root / required.path
        if not path.exists():
            errors.append(f"missing required doc: {required.path}")
            continue

        data = path.read_bytes()
        bad_controls = _bad_control_offsets(data)
        if bad_controls:
            offset, byte = bad_controls[0]
            errors.append(f"{required.path}: hidden/control byte at offset {offset}: 0x{byte:02x}")
            continue

        text = data.decode("utf-8")
        bad_bidi = _bad_bidi_offsets(text)
        if bad_bidi:
            index, char = bad_bidi[0]
            errors.append(f"{required.path}: bidi/control code point at char {index}: U+{ord(char):04X}")

        lower_text = text.lower()
        for phrase in required.phrases:
            if phrase.lower() not in lower_text:
                errors.append(f"{required.path}: missing required phrase: {phrase}")

    queue_path = root / "docs/context/CODEX_INNER_LOOP_QUEUE.md"
    if queue_path.exists():
        queue_text = queue_path.read_text(encoding="utf-8")
        task_ids = sorted(set(re.findall(r"\bCIL-\d{3}\b", queue_text)))
        if len(task_ids) < 6:
            errors.append("docs/context/CODEX_INNER_LOOP_QUEUE.md: expected at least 6 task ids")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Codex inner-loop docs validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Codex inner-loop docs validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
