"""Offline OpenAI-compatible proxy example using reusable KORA routing logic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from kora.openai_proxy_demo import (
    build_proxy_summary as build_reusable_proxy_summary,
    render_report as render_reusable_report,
    write_report,
)

EXAMPLE_DIR = Path(__file__).resolve().parent
REQUESTS_PATH = EXAMPLE_DIR / "requests.json"
EXPECTED_COUNTERS_PATH = EXAMPLE_DIR / "expected_counters.json"


def build_proxy_summary(
    *,
    requests_path: Path = REQUESTS_PATH,
    json_out: Path | None = None,
) -> dict:
    return build_reusable_proxy_summary(
        requests_path=requests_path,
        expected_counters_path=EXPECTED_COUNTERS_PATH,
        json_out=json_out,
        mode="openai_compatible_proxy_example",
    )


def render_report(summary: dict) -> str:
    return render_reusable_report(summary, title="KORA OpenAI-Compatible Proxy Example")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", default=str(REQUESTS_PATH), help="OpenAI-style request fixture JSON")
    parser.add_argument("--json-out", help="optional path for structured JSON output")
    parser.add_argument("--report-md", help="optional path for rendered report output")
    args = parser.parse_args()

    summary = build_proxy_summary(
        requests_path=Path(args.requests),
        json_out=Path(args.json_out) if args.json_out else None,
    )
    report = render_report(summary)
    write_report(report, Path(args.report_md) if args.report_md else None)
    print(report, end="")
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
