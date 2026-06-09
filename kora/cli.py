"""KORA command-line utilities."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from kora.cost_model import compute_savings
from kora.studio_server import (
    DEFAULT_STUDIO_HOST,
    DEFAULT_STUDIO_PORT,
    is_allowed_studio_host,
    run_studio_server,
)
from kora.studio_status import get_studio_status, render_studio_status_text
from kora.telemetry import load_json, render_markdown_report, summarize_run


def _default_json_out(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.telemetry.json")


def _default_md_out(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.telemetry.md")


def _examples_root() -> Path:
    return Path(__file__).resolve().parent.parent / "examples"


def _example_descriptions() -> dict[str, str]:
    return {
        "hello_kora": "basic deterministic hello-world graph",
        "retry_demo": "retry/recovery flow example",
        "customer_support_triage_fake_validation": "customer-support triage local no-network validation example",
        "direct_vs_kora": "direct call vs KORA-controlled path",
        "real_workload_harness": "benchmark/report flow example",
        "real_model_call_validation_fake": "local no-network model-call validation example",
        "runtime_integrated_benchmark": "initial runtime-path benchmark harness",
        "stress_test": "repeated-run stress harness",
    }


def _discover_examples() -> list[dict[str, object]]:
    root = _examples_root()
    if not root.exists():
        return []

    descriptions = _example_descriptions()
    examples: list[dict[str, object]] = []
    for child in sorted(root.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            continue
        run_path = child / "run.py"
        if not run_path.exists():
            continue
        examples.append(
            {
                "name": child.name,
                "run_path": run_path,
                "has_graph": (child / "graph.json").exists(),
                "description": descriptions.get(child.name, "runnable example"),
            }
        )
    return examples


def _print_examples_list() -> None:
    examples = _discover_examples()
    if not examples:
        print("No runnable examples found.")
        return

    print("Runnable examples")
    for example in examples:
        graph_label = "yes" if example["has_graph"] else "no"
        print(f"- {example['name']}: {example['description']} (graph.json: {graph_label})")


def _run_example(example_name: str, extra_args: list[str]) -> int:
    examples = _discover_examples()
    example_map = {str(example["name"]): Path(example["run_path"]) for example in examples}

    if example_name not in example_map:
        available = ", ".join(sorted(example_map)) if example_map else "(none)"
        print(f"Unknown example: {example_name}", file=sys.stderr)
        print(f"Available examples: {available}", file=sys.stderr)
        return 2

    command = [sys.executable, str(example_map[example_name]), *extra_args]
    repo_root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(repo_root)
        if not existing_pythonpath
        else str(repo_root) + os.pathsep + existing_pythonpath
    )
    completed = subprocess.run(command, check=False, env=env)
    return int(completed.returncode)


def _print_summary(summary: dict) -> None:
    print("Telemetry Summary")
    print(f"- ok: {summary['ok']}")
    print(f"- total_time_ms: {summary['total_time_ms']}")
    print(f"- total_llm_calls: {summary['total_llm_calls']}")
    print(f"- tokens_in: {summary['tokens_in']}")
    print(f"- tokens_out: {summary['tokens_out']}")
    print(f"- events_ok: {summary['events_ok']}")
    print(f"- events_fail: {summary['events_fail']}")
    print(f"- events_skipped: {summary['events_skipped']}")
    print(f"- budget_breaches: {summary['budget_breaches']}")
    print(f"- escalation_required: {summary['escalation_required']}")
    if "estimated_cost_usd" in summary:
        print(f"- model: {summary.get('model', '')}")
        print(f"- estimated_cost_usd: {summary['estimated_cost_usd']}")
    print("- stage_counts:")
    if summary["stage_counts"]:
        for stage, count in sorted(summary["stage_counts"].items()):
            print(f"  - {stage}: {count}")
    else:
        print("  - (none)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kora.cli", description="KORA CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    examples_parser = subparsers.add_parser("examples", help="list available runnable examples")
    examples_subparsers = examples_parser.add_subparsers(dest="examples_command", required=True)
    examples_subparsers.add_parser("list", help="list runnable examples")

    run_parser = subparsers.add_parser(
        "run",
        help="run an example",
        description="Run an example. Use -- to pass arguments through to the example.\nExample: kora run direct_vs_kora -- --offline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    run_parser.add_argument("example", help="example name under examples/")
    run_parser.add_argument("example_args", nargs=argparse.REMAINDER, help="arguments passed to the example")

    studio_parser = subparsers.add_parser(
        "studio",
        help="launch KORA Studio local browser UI",
        description="Launch the localhost-only KORA Studio preview server and open the local browser UI by default. Use --status to print planning/preview status only.",
    )
    studio_parser.add_argument("--status", action="store_true", help="show planning/preview status")
    studio_parser.add_argument("--no-browser", action="store_true", help="start the local server without opening a browser")
    studio_parser.add_argument("--open-browser", action="store_true", help="open the default browser; this is already the default")
    studio_parser.add_argument("--serve", action="store_true", help="start the local-only Studio server; preserved for compatibility")
    studio_parser.add_argument("--host", default=DEFAULT_STUDIO_HOST, help="local host for Studio server (default: 127.0.0.1)")
    studio_parser.add_argument("--port", default=DEFAULT_STUDIO_PORT, type=int, help="local port for Studio server (default: 8765)")

    telemetry_parser = subparsers.add_parser("telemetry", help="summarize a run JSON file")
    telemetry_parser.add_argument("--input", required=True, help="path to run/report JSON")
    telemetry_parser.add_argument("--json-out", help="output path for telemetry JSON")
    telemetry_parser.add_argument("--md-out", help="output path for telemetry markdown report")
    telemetry_parser.add_argument("--price-input", type=float, help="override input price per 1k tokens")
    telemetry_parser.add_argument("--price-output", type=float, help="override output price per 1k tokens")
    telemetry_parser.add_argument("--compare", help="optional second run/report JSON to compute savings delta")

    args = parser.parse_args(argv)

    if args.command == "examples" and args.examples_command == "list":
        _print_examples_list()
        return 0

    if args.command == "run":
        extra_args = list(args.example_args)
        if extra_args and extra_args[0] == "--":
            extra_args = extra_args[1:]
        return _run_example(args.example, extra_args)

    if args.command == "studio":
        if args.status:
            status = get_studio_status()
            print(render_studio_status_text(status), end="")
            return 0
        if not is_allowed_studio_host(args.host):
            print(
                "KORA Studio server is local-only; use --host 127.0.0.1 or --host localhost.",
                file=sys.stderr,
            )
            return 2
        run_studio_server(host=args.host, port=args.port, open_browser=not args.no_browser)
        return 0

    if args.command == "telemetry":
        input_path = Path(args.input)
        try:
            obj = load_json(input_path)
        except (FileNotFoundError, IsADirectoryError) as e:
            print(e, file=sys.stderr)
            return 1
        summary = summarize_run(obj, price_input=args.price_input, price_output=args.price_output)
        json_out = Path(args.json_out) if args.json_out else _default_json_out(input_path)
        md_out = Path(args.md_out) if args.md_out else _default_md_out(input_path)

        savings: dict | None = None
        compare_path: Path | None = None
        if args.compare:
            compare_path = Path(args.compare)
            compare_obj = load_json(compare_path)
            compare_summary = summarize_run(
                compare_obj,
                price_input=args.price_input,
                price_output=args.price_output,
            )
            input_mode = str(obj.get("mode", "")).lower()
            compare_mode = str(compare_obj.get("mode", "")).lower()

            input_cost = float(summary.get("estimated_cost_usd", 0.0))
            compare_cost = float(compare_summary.get("estimated_cost_usd", 0.0))
            if input_mode == "kora" and compare_mode == "direct":
                savings = compute_savings(compare_cost, input_cost)
            elif input_mode == "direct" and compare_mode == "kora":
                savings = compute_savings(input_cost, compare_cost)
            else:
                savings = compute_savings(compare_cost, input_cost)
            summary["savings"] = savings

        json_out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        md_report = render_markdown_report(
            summary,
            source_path=str(input_path),
            compare_path=str(compare_path) if compare_path else None,
            savings=savings,
        )
        md_out.write_text(md_report, encoding="utf-8")
        _print_summary(summary)
        if savings is not None:
            print("Savings Summary")
            print(f"- direct_cost_usd: {savings['direct_cost_usd']}")
            print(f"- kora_cost_usd: {savings['kora_cost_usd']}")
            print(f"- savings_usd: {savings['savings_usd']}")
            print(f"- savings_percent: {savings['savings_percent']}")
        print(f"Saved telemetry JSON: {json_out}")
        print(f"Saved telemetry Markdown: {md_out}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
