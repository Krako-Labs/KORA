"""Check local markdown links in Goal 082B public-facing docs."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "OPEN_THIS_FIRST.md",
    ROOT / "REVIEW_HUB.md",
    ROOT / "docs" / "vision" / "kora_workload_control_layer.md",
    ROOT / "docs" / "reports" / "goal082b_narrative_repositioning.md",
]


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def _target_exists(source: Path, href: str) -> bool:
    if href.startswith(("http://", "https://", "mailto:")):
        return True
    target = href.split("#", 1)[0].strip()
    if not target:
        return True
    return (source.parent / target).resolve().exists()


def main() -> int:
    missing: list[str] = []
    for path in DOCS:
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            href = match.group(1)
            if not _target_exists(path, href):
                missing.append(f"{path.relative_to(ROOT)} -> {href}")
    if missing:
        print("Missing markdown links:")
        for item in missing:
            print(f"- {item}")
        return 1
    print("Goal 082B markdown links OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
