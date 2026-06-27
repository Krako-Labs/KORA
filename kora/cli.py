"""KORA command-line utilities."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

from kora.cost_model import compute_savings
from kora.five_minute_first_value import (
    build_five_minute_first_value,
    render_markdown_summary as render_first_value_markdown,
    write_outputs as write_first_value_outputs,
)
from kora.openai_proxy_demo import (
    DEFAULT_EXPECTED_COUNTERS_PATH,
    build_proxy_summary,
    render_report as render_proxy_report,
    write_report as write_proxy_report,
)
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


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _example_descriptions() -> dict[str, str]:
    return {
        "agent_workflow_optimization": "offline agent workflow control example",
        "cache_reuse": "offline cache reuse routing example",
        "hello_kora": "basic deterministic hello-world graph",
        "retry_demo": "retry/recovery flow example",
        "customer_support_triage_synthetic": "customer-support triage local no-network validation example",
        "deterministic_classification": "deterministic classification example pack",
        "direct_vs_kora": "direct call vs KORA-controlled path",
        "kora_doctor": "offline doctor-style workload inspection example",
        "openai_compatible_proxy": "offline OpenAI-style proxy routing example",
        "rag_routing": "offline RAG routing control example",
        "real_workload_harness": "benchmark/report flow example",
        "model_call_counter_fixture": "local no-network model-call validation example",
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


def _load_doctor_module():
    doctor_path = _examples_root() / "kora_doctor" / "run.py"
    spec = importlib.util.spec_from_file_location("kora_doctor_cli_runtime", doctor_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load KORA Doctor module from {doctor_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _resolve_doctor_workload_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.exists():
        return path

    doctor_root = _examples_root() / "kora_doctor"
    workload_candidate = doctor_root / "workloads" / path.name
    if path.parent.name == "kora_doctor" and workload_candidate.exists():
        return workload_candidate

    return path


def _run_doctor_command(
    workload_path: str | None,
    *,
    all_workloads: bool,
    json_out: str | None,
    report_md: str | None,
) -> int:
    doctor = _load_doctor_module()
    try:
        if all_workloads:
            workloads_root = Path(workload_path) if workload_path else _examples_root() / "kora_doctor"
            if not workloads_root.exists() or not workloads_root.is_dir():
                print(f"KORA Doctor workload directory not found: {workloads_root}", file=sys.stderr)
                return 2
            summary = doctor.build_aggregate_summary(
                workloads_root=workloads_root,
                json_out=Path(json_out) if json_out else None,
            )
        else:
            resolved_workload = (
                _resolve_doctor_workload_path(workload_path)
                if workload_path
                else _examples_root() / "kora_doctor" / "workload.json"
            )
            if not resolved_workload.exists() or not resolved_workload.is_file():
                print(f"KORA Doctor workload JSON not found: {resolved_workload}", file=sys.stderr)
                return 2
            summary = doctor.build_doctor_summary(
                resolved_workload,
                json_out=Path(json_out) if json_out else None,
            )
    except (json.JSONDecodeError, KeyError, RuntimeError, ValueError) as e:
        print(f"KORA Doctor failed: {e}", file=sys.stderr)
        return 1

    report = doctor.render_text_report(summary)
    if report_md:
        report_path = Path(report_md)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    print(report, end="")
    return 0 if summary["ok"] else 1


def _run_proxy_demo_command(
    requests_path: str,
    *,
    json_out: str | None,
    report_md: str | None,
) -> int:
    path = Path(requests_path)
    if not path.exists() or not path.is_file():
        print(f"KORA proxy demo request JSON not found: {path}", file=sys.stderr)
        return 2

    try:
        summary = build_proxy_summary(
            requests_path=path,
            expected_counters_path=DEFAULT_EXPECTED_COUNTERS_PATH,
            json_out=Path(json_out) if json_out else None,
            mode="openai_proxy_demo_cli",
        )
    except (json.JSONDecodeError, KeyError, RuntimeError, ValueError) as e:
        print(f"KORA proxy demo failed: {e}", file=sys.stderr)
        return 1

    report = render_proxy_report(summary)
    write_proxy_report(report, Path(report_md) if report_md else None)
    print(report, end="")
    return 0 if summary["ok"] else 1


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
    repo_root = _repo_root()
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


def _write_json_output(data: dict, path: str | None) -> None:
    if not path:
        return
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _print_inspect(step: dict) -> None:
    print("KORA Inspect")
    print("- execution paths:")
    for route in step["available_execution_paths"]:
        print(f"  - {route}")
    print("- workload profiles:")
    for profile in step["routable_workload_profiles"]:
        print(f"  - {profile}")
    env = step["environment_summary"]
    print("- first-value requirements:")
    print(f"  - provider credentials required: {str(env['provider_credentials_required']).lower()}")
    print(f"  - GPU required: {str(env['gpu_required']).lower()}")
    print(f"  - network required: {str(env['network_required']).lower()}")
    print(f"  - execution mode: {env['execution_mode']}")


def _print_compare(step: dict) -> None:
    direct = step["direct_path"]
    krk = step["krk_routed_path"]
    opportunities = step["avoided_execution_opportunities"]
    print("KORA Compare")
    print(f"- direct path candidate invocations: {direct['candidate_invocations']}")
    print("- KRK route counts:")
    for route, count in krk["route_counts"].items():
        print(f"  - {route}: {count}")
    print(f"- provider/GPU route count: {krk['provider_or_gpu_route_count']}")
    print(f"- local-or-guardrail route count: {krk['local_or_guardrail_route_count']}")
    print(f"- avoided execution opportunities: {opportunities['count']} ({opportunities['rate']:.4f})")
    print("- claim boundary: execution-path opportunity count, not a production savings claim")


def _print_run(step: dict) -> None:
    print("KORA Run")
    print(f"- total requests: {step['total_requests']}")
    print("- route counts:")
    for route, count in step["route_counts"].items():
        print(f"  - {route}: {count}")
    print(f"- dry-run execution success rate: {step['dry_run_execution_success_rate']:.4f}")
    print(f"- unsafe misroute rate: {step['unsafe_misroute_rate']:.4f}")
    print(f"- error count: {step['error_count']}")
    print(f"- provider calls performed: {str(step['provider_calls_performed']).lower()}")
    print(f"- GPU execution performed: {str(step['gpu_execution_performed']).lower()}")


def _run_first_value_step(step_id: str, *, json_out: str | None = None) -> int:
    result = build_five_minute_first_value(command=f"kora {step_id}")
    step = next(item for item in result["steps"] if item["step_id"] == step_id)
    output = {
        "schema_version": f"kora_{step_id}_v0",
        "claim_level": result["claim_level"],
        "final_classification": result["final_classification"],
        "step": step,
        "works_without_provider_credentials": result["works_without_provider_credentials"],
        "works_without_gpu": result["works_without_gpu"],
        "network_required": result["network_required"],
        "claim_boundary": result["claim_boundary"],
    }
    if step_id == "inspect":
        _print_inspect(step)
    elif step_id == "compare":
        _print_compare(step)
    elif step_id == "run":
        _print_run(step)
    else:
        raise ValueError(f"unsupported first-value step: {step_id}")
    _write_json_output(output, json_out)
    if json_out:
        print(f"Saved JSON: {json_out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kora", description="KORA CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    examples_parser = subparsers.add_parser("examples", help="list available runnable examples")
    examples_subparsers = examples_parser.add_subparsers(dest="examples_command", required=True)
    examples_subparsers.add_parser("list", help="list runnable examples")

    inspect_parser = subparsers.add_parser(
        "inspect",
        help="inspect public-safe first-value execution paths",
        description="Inspect the public-safe KORA first-value environment and available execution paths.",
    )
    inspect_parser.add_argument("--json-out", help="optional path for structured JSON output")

    compare_parser = subparsers.add_parser(
        "compare",
        help="compare direct and KRK-routed public fixture behavior",
        description="Compare direct model-candidate behavior with KRK-routed public fixture behavior.",
    )
    compare_parser.add_argument("--json-out", help="optional path for structured JSON output")

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="inspect a workload for deterministic and provider-needed candidates",
        description=(
            "Run the offline KORA Doctor workload-control report for a workload JSON file, "
            "or aggregate bundled workloads with --all."
        ),
    )
    doctor_parser.add_argument(
        "workload_path",
        nargs="?",
        help="workload JSON path, or workload directory when used with --all",
    )
    doctor_parser.add_argument("--all", action="store_true", help="run all workloads in a Doctor workload directory")
    doctor_parser.add_argument("--json-out", help="optional path for structured JSON output")
    doctor_parser.add_argument("--report-md", help="optional path for the rendered text report")

    proxy_demo_parser = subparsers.add_parser(
        "proxy-demo",
        help="run the offline OpenAI-style proxy demo",
        description=(
            "Run the offline KORA proxy demo for OpenAI-style sample request JSON. "
            "The demo routes deterministic or cacheable sample requests without provider calls "
            "and marks ambiguous/open-ended requests as provider-needed."
        ),
    )
    proxy_demo_parser.add_argument("requests_path", help="OpenAI-style request fixture JSON")
    proxy_demo_parser.add_argument("--json-out", help="optional path for structured JSON output")
    proxy_demo_parser.add_argument("--report-md", help="optional path for the rendered text report")

    run_parser = subparsers.add_parser(
        "run",
        help="run the public-safe first-value fixture path or a named example",
        description=(
            "Run the public-safe first-value fixture path when no example is provided. "
            "Use an example name plus -- to pass arguments through to an example.\n"
            "Examples:\n"
            "  kora run\n"
            "  kora run --json-out /tmp/kora-run.json\n"
            "  kora run direct_vs_kora -- --offline"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    run_parser.add_argument("example", nargs="?", help="optional example name under examples/")
    run_parser.add_argument("--json-out", help="optional path for structured JSON output when no example is provided")
    run_parser.add_argument("example_args", nargs=argparse.REMAINDER, help="arguments passed to the example")

    report_parser = subparsers.add_parser(
        "report",
        help="generate the public-safe first-value report",
        description="Generate JSON and Markdown reports for the public-safe first-value workflow.",
    )
    report_parser.add_argument("--json-out", required=True, help="output path for JSON report")
    report_parser.add_argument("--md-out", required=True, help="output path for Markdown report")

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

    if args.command == "inspect":
        return _run_first_value_step("inspect", json_out=args.json_out)

    if args.command == "compare":
        return _run_first_value_step("compare", json_out=args.json_out)

    if args.command == "doctor":
        return _run_doctor_command(
            args.workload_path,
            all_workloads=args.all,
            json_out=args.json_out,
            report_md=args.report_md,
        )

    if args.command == "proxy-demo":
        return _run_proxy_demo_command(
            args.requests_path,
            json_out=args.json_out,
            report_md=args.report_md,
        )

    if args.command == "run":
        if args.example is None:
            return _run_first_value_step("run", json_out=args.json_out)
        extra_args = list(args.example_args)
        if extra_args and extra_args[0] == "--":
            extra_args = extra_args[1:]
        return _run_example(args.example, extra_args)

    if args.command == "report":
        command = f"kora report --json-out {args.json_out} --md-out {args.md_out}"
        result = build_five_minute_first_value(command=command)
        write_first_value_outputs(result, json_out=Path(args.json_out), md_out=Path(args.md_out))
        print(render_first_value_markdown(result))
        print(f"Saved JSON: {args.json_out}")
        print(f"Saved Markdown: {args.md_out}")
        return 0

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
