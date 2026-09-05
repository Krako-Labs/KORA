"""Offline measurement foundation; never synthesizes inference throughput."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .contracts import canonical_json_bytes, validate_contract_instance
from .host import LocalSolutionHost


def collect_local_runs(
    host: LocalSolutionHost,
    package: Path,
    payload: dict[str, Any],
    expected: dict[str, Any],
    *,
    repetitions: int = 3,
) -> dict[str, Any]:
    """Measure initialized synchronous runs with exact fixture output checks."""
    if (
        isinstance(repetitions, bool)
        or not isinstance(repetitions, int)
        or not 1 <= repetitions <= 100
    ):
        raise ValueError("repetitions must be an integer from 1 through 100")
    receipt = host.install(package)
    samples = []
    for index in range(repetitions):
        start = time.perf_counter_ns()
        result = host.run(
            receipt["solution"]["id"], payload, version=receipt["solution"]["version"]
        )
        elapsed = (time.perf_counter_ns() - start) / 1_000_000
        evidence_path = host.runs_root / result["run_id"] / "node-evidence.json"
        nodes = (
            host.node_evidence(result["run_id"])["nodes"]
            if evidence_path.exists()
            else []
        )
        samples.append(
            {
                "sequence": index,
                "run_id": result["run_id"],
                "status": result["lifecycle_state"],
                "elapsed_ms": elapsed,
                "quality_pass": result["lifecycle_state"] == "succeeded"
                and result["output"] == expected,
                "output_digest": hashlib.sha256(
                    canonical_json_bytes(result["output"])
                ).hexdigest(),
                "deterministic_nodes_completed": sum(
                    n["state"] == "succeeded" for n in nodes
                ),
                "model_calls": 0,
                "exact_reuse_hits": 0,
                "input_tokens": None,
                "generated_tokens": None,
                "ttft_ms": None,
                "error_code": None
                if result["error"] is None
                else result["error"]["code"],
            }
        )
    report = {
        "schema_version": "kora.benchmark.local/v1",
        "measurement_kind": "measured-local-deterministic",
        "system_set": "local-development",
        "timing_scope": "client-host-run-including-validation-and-persistence",
        "cache_condition": "no-result-reuse-page-cache-uncontrolled",
        "package_digest": receipt["package_digest"],
        "input_digest": hashlib.sha256(canonical_json_bytes(payload)).hexdigest(),
        "expected_digest": hashlib.sha256(canonical_json_bytes(expected)).hexdigest(),
        "samples": samples,
    }
    validate_contract_instance("benchmark-local.schema.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--expected", type=Path, required=True)
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--repetitions", type=int, default=3)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text())
    expected = json.loads(args.expected.read_text())
    if not isinstance(payload, dict) or not isinstance(expected, dict):
        parser.error("input and expected fixtures must be objects")
    report = collect_local_runs(
        LocalSolutionHost(args.store),
        args.package,
        payload,
        expected,
        repetitions=args.repetitions,
    )
    print(json.dumps(report, indent=2))
    return 0 if all(item["quality_pass"] for item in report["samples"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
