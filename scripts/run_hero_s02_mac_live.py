#!/usr/bin/env python3
"""Run the explicitly approved Task038 Mac-only live slice."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from kora.adapters.openai_compatible_local import OpenAICompatibleLocalAdapter
from kora.hero_contracts import WorkloadRequirements
from kora.hero_live_execution import (
    ExistingLlamaCppServerController,
    LiveExecutionConfig,
    LiveServiceRequest,
    LlamaCppServerController,
    run_live_execution,
    write_live_evidence,
)
from kora.hero_planner import build_hero_planning_bundle
from kora.hero_profilers import collect_hardware_profile, profile_model_artifact


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bounded local Qwen/llama.cpp Hero execution; no remote fallback."
    )
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--runtime-path", required=True)
    parser.add_argument("--model-sha256", required=True)
    parser.add_argument("--runtime-sha256", required=True)
    parser.add_argument("--runtime-version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--runtime-log", required=True)
    parser.add_argument("--port", type=int, default=8796)
    parser.add_argument("--model-name", default="Qwen3-30B-A3B")
    parser.add_argument("--api-key-file")
    parser.add_argument("--reuse-existing", action="store_true")
    parser.add_argument("--timeout-s", type=float, default=300)
    return parser


def _service() -> LiveServiceRequest:
    return LiveServiceRequest(
        request_id="hero-s02-task038-private-ai-brief-v1",
        facts=(
            "The service runs on user-owned hardware.",
            "The model endpoint is available only on loopback.",
            "The execution records configuration, calls, timing, memory sampling, and cleanup.",
            "The validation checks only supplied values and structural requirements.",
        ),
        approved_fragment="Private by default. Evidence before claims.",
        allowed_headlines=("Private AI, visible evidence",),
        allowed_audiences=("Teams operating AI on owned hardware",),
        allowed_promises=("Run one bounded local draft with traceable evidence.",),
        approved_proof_points=(
            "Runs on user-owned hardware.",
            "Uses a loopback-only model endpoint.",
            "Records configuration, calls, timing, memory sampling, and cleanup.",
        ),
        required_caveats=(
            "Semantic quality was not measured.",
            "Production behavior was not measured.",
        ),
        prohibited_claims=(
            "2x",
            "3x",
            "production proven",
            "quality proven",
            "larger than vram",
        ),
    )


def main() -> int:
    args = _parser().parse_args()
    if not 1024 <= args.port <= 65535:
        raise SystemExit("--port must be between 1024 and 65535")

    model_path = Path(args.model_path).expanduser().absolute()
    runtime_path = Path(args.runtime_path).expanduser().absolute()
    output_path = Path(args.output).expanduser().absolute()
    log_path = Path(args.runtime_log).expanduser().absolute()

    def which(command: str) -> str | None:
        if command == "llama-server":
            return str(runtime_path)
        return shutil.which(command)

    captured_at = datetime.now(timezone.utc)
    hardware = collect_hardware_profile(
        profile_id="hero-s02-msm2-1-observed",
        captured_at=captured_at,
        which=which,
    )
    model, inventory = profile_model_artifact(
        model_path,
        profile_id="hero-s02-qwen3-30b-a3b-q4-k-m",
        model_id="Qwen3-30B-A3B-Q4_K_M",
        source_revision="local-gguf-verified",
        quantization="Q4_K_M",
        artifact_format="gguf",
    )
    if model.sha256 != args.model_sha256:
        raise SystemExit("model SHA-256 differs from the approved identity")

    workload = WorkloadRequirements(
        workload_class="source_bounded_launch_brief",
        context_tokens=4096,
        max_output_tokens=256,
        concurrency=1,
        estimated_kv_bytes=1024**3,
        runtime_reserve_bytes=4 * 1024**3,
        minimum_free_system_bytes=8 * 1024**3,
        allow_network=False,
    )
    run_stamp = captured_at.strftime("%Y%m%dT%H%M%SZ")
    bundle = build_hero_planning_bundle(
        run_id=f"hero-s02-task038-{run_stamp}",
        plan_id="hero-s02-task038-mac-llama-v1",
        occurred_at=captured_at,
        hardware=hardware,
        model=model,
        workload=workload,
    )
    if bundle.plan.selected_adapter_id != "llama.cpp":
        raise SystemExit(
            "the observed planner did not select llama.cpp; live execution stopped"
        )

    runtime_id = (
        f"llama.cpp:{args.runtime_sha256[:12]}:"
        f"{args.model_sha256[:12]}:{args.runtime_version}"
    )
    config = LiveExecutionConfig(
        endpoint=f"http://127.0.0.1:{args.port}",
        model_name=args.model_name,
        runtime_id=runtime_id,
        runtime_version=args.runtime_version,
        runtime_binary_sha256=args.runtime_sha256,
        model_artifact_sha256=args.model_sha256,
        max_output_tokens=256,
        max_model_calls=2,
        timeout_s=args.timeout_s,
        live_window_s=1200,
    )
    controller_type = (
        ExistingLlamaCppServerController
        if args.reuse_existing
        else LlamaCppServerController
    )
    if args.reuse_existing and not args.api_key_file:
        raise SystemExit("--reuse-existing requires --api-key-file")
    controller = controller_type(
        binary_path=runtime_path,
        model_path=model_path,
        config=config,
        log_path=log_path,
        context_tokens=workload.context_tokens,
    )
    adapter_environment = {
        "KORA_LOCAL_OPENAI_ENDPOINT": config.endpoint,
        "KORA_LOCAL_OPENAI_MODEL": config.model_name,
        "KORA_LOCAL_OPENAI_RUNTIME_ID": config.runtime_id,
        "KORA_LOCAL_OPENAI_TIMEOUT_S": str(config.timeout_s),
        "KORA_LOCAL_OPENAI_DISABLE_THINKING": "true",
    }
    if args.api_key_file:
        adapter_environment["KORA_LOCAL_OPENAI_API_KEY_FILE"] = str(
            Path(args.api_key_file).expanduser().absolute()
        )
    evidence = run_live_execution(
        bundle=bundle,
        hardware=hardware,
        model=model,
        workload=workload,
        service=_service(),
        config=config,
        controller=controller,
        adapter_factory=lambda: OpenAICompatibleLocalAdapter(
            environ=adapter_environment
        ),
    )
    evidence["profile_inventory_digest"] = hashlib.sha256(
        json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    write_live_evidence(output_path, evidence)

    summary = {
        "schema_version": evidence["schema_version"],
        "run_id": evidence["run_id"],
        "accepted_outcome": evidence["verification"]["accepted_outcome"],
        "failure_code": evidence["verification"]["failure_code"],
        "model_calls": evidence["actual_execution"]["model_calls"],
        "provider_calls": evidence["actual_execution"]["provider_calls"],
        "runtime_starts": evidence["actual_execution"]["runtime_starts"],
        "live_window_ms": evidence["actual_execution"]["live_window_ms"],
        "cleanup_success": evidence["cleanup"].get("cleanup_success"),
        "output_digest": evidence["output_digest"],
        "evidence_path": str(output_path),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if evidence["verification"]["accepted_outcome"] else 2


if __name__ == "__main__":
    sys.exit(main())
