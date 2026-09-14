"""Explicitly approved owned-GPU execution with bounded resources and evidence.

No import starts a runtime. The worker runs on the owned GPU host, with loopback
HTTP there and an explicitly labelled private-network orchestration boundary.
"""

from __future__ import annotations

import importlib.metadata
import json
import os
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from urllib import request

from pydantic import Field, field_validator

from kora.hero_contracts import (
    AcceleratorProfile,
    HardwareProfile,
    HeroEvent,
    MemoryDomain,
    ModelResourceProfile,
    RuntimeCapability,
    StrictContract,
    WorkloadRequirements,
)
from kora.hero_event_log import HeroEventLog
from kora.hero_feasibility import build_execution_plan
from kora.hero_live_execution import (
    LiveDraft,
    LiveExecutionError,
    LiveServiceRequest,
    _digest,
    _schema_for_service,
    _sha256_file,
    _validate_draft,
)

SCHEMA = "hero.remote-execution-evidence.v1"


class FileIdentity(StrictContract):
    name: str
    sha256: str
    size: int = Field(gt=0, strict=True)

    @field_validator("name")
    @classmethod
    def safe_name(cls, value: str) -> str:
        if not value or Path(value).name != value or value in {".", ".."}:
            raise ValueError("identity requires a basename")
        return value

    @field_validator("sha256")
    @classmethod
    def sha(cls, value: str) -> str:
        if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError("invalid SHA-256")
        return value


class RemoteConfig(StrictContract):
    approval_id: str = Field(min_length=1)
    lease_id: str = Field(min_length=1)
    project: str = Field(min_length=1)
    unit: str = Field(pattern=r"^[a-zA-Z0-9_-]+\.service$")
    lease_tool: str
    model_dir: str
    model_id: str
    revision: str
    files: tuple[FileIdentity, ...] = Field(min_length=1)
    runtime_files: dict[str, str] = Field(min_length=1)
    runtime_versions: dict[str, str] = Field(min_length=1)
    python_path: str
    port: int = Field(default=8798, ge=1024, le=65535, strict=True)
    max_calls: int = Field(default=2, ge=1, le=2, strict=True)
    max_tokens: int = Field(default=256, ge=1, le=256, strict=True)
    context_tokens: Literal[4096] = 4096
    request_timeout_s: int = Field(default=300, ge=1, le=300, strict=True)
    execution_window_s: int = Field(default=1200, ge=1, le=1200, strict=True)
    restoration_reserve_s: int = Field(default=600, ge=600, le=600, strict=True)

    @field_validator("files")
    @classmethod
    def unique_files(cls, files):
        if len({f.name for f in files}) != len(files):
            raise ValueError("duplicate file identity")
        return files

    @property
    def endpoint(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def launch_environment(self) -> dict[str, str]:
        # Use the installed native sampler: FlashInfer JIT requires an nvcc
        # toolkit that is not a prerequisite of this bounded runtime.
        return {
            "HF_HUB_OFFLINE": "1",
            "TRANSFORMERS_OFFLINE": "1",
            "VLLM_NO_USAGE_STATS": "1",
            "DO_NOT_TRACK": "1",
            "VLLM_USE_FLASHINFER_SAMPLER": "0",
            "VLLM_HOST_IP": "127.0.0.1",
        }

    def command(self) -> list[str]:
        return [
            self.python_path,
            "-m",
            "vllm.entrypoints.openai.api_server",
            "--model",
            self.model_dir,
            "--served-model-name",
            self.model_id,
            "--host",
            "127.0.0.1",
            "--port",
            str(self.port),
            "--dtype",
            "bfloat16",
            "--max-model-len",
            str(self.context_tokens),
            "--max-num-seqs",
            "1",
            "--gpu-memory-utilization",
            "0.90",
            "--enforce-eager",
            "--generation-config",
            "vllm",
        ]


def decoder_schema(service: LiveServiceRequest) -> dict:
    """Adapt decoder syntax; uniqueness remains mandatory in output validation."""
    schema = _schema_for_service(service)
    schema["properties"]["proof_points"].pop("uniqueItems")
    return schema


def validate_lease(
    config: RemoteConfig, status: dict, *, now=None, require_clear=False
) -> dict:
    now = now or datetime.now(timezone.utc)
    try:
        lease = status["lease"]
        sampled = datetime.fromisoformat(status["observed"]["sampled_at"])
        remaining = (
            datetime.fromisoformat(lease["expected_end"]) - now
        ).total_seconds()
        if not 0 <= (now - sampled).total_seconds() <= 30:
            raise ValueError()
        if (
            status["overdue"] is not False
            or lease["lease_id"] != config.lease_id
            or lease["project"] != config.project
            or lease["unit"] != config.unit
            or remaining <= config.restoration_reserve_s
        ):
            raise ValueError()
        processes = status["observed"]["processes"]
        if not isinstance(processes, list):
            raise TypeError()
        if any(p.get("service") != config.unit for p in processes):
            raise ValueError()
        if require_clear and processes:
            raise ValueError()
        return lease
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise LiveExecutionError("lease_not_exclusive_or_expiring") from exc


class _NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise LiveExecutionError("redirect_rejected")


def loopback_json(endpoint: str, path: str, *, payload=None, timeout=10):
    # Callers receive endpoints only from the validated fixed-loopback config.
    if not endpoint.startswith("http://127.0.0.1:") or path not in {
        "/health",
        "/v1/models",
        "/v1/chat/completions",
    }:
        raise LiveExecutionError("endpoint_not_allowed")
    data = None if payload is None else json.dumps(payload, allow_nan=False).encode()
    req = request.Request(
        endpoint + path, data=data, headers={"Content-Type": "application/json"}
    )
    opener = request.build_opener(request.ProxyHandler({}), _NoRedirect())
    with opener.open(req, timeout=timeout) as response:
        raw = response.read(2 * 1024 * 1024 + 1)
    if len(raw) > 2 * 1024 * 1024:
        raise LiveExecutionError("response_too_large")
    return json.loads(raw) if raw else {}


class VllmController:
    """Own one subprocess group inside the externally leased systemd unit."""

    def __init__(self, config: RemoteConfig, log_path: Path):
        self.config = config
        self.log_path = log_path
        self.process = None
        self.log_handle = None
        self.started = time.monotonic()
        self.samples = []
        self.sample_stop = threading.Event()
        self.sampler = None

    def _sample(self):
        while not self.sample_stop.is_set():
            try:
                r = subprocess.run(
                    [
                        "nvidia-smi",
                        "--query-gpu=memory.used,utilization.gpu",
                        "--format=csv,noheader,nounits",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=True,
                )
                memory, utilization = [
                    int(x.strip()) for x in r.stdout.strip().split(",")
                ]
                self.samples.append(
                    {
                        "elapsed_ms": round((time.monotonic() - self.started) * 1000),
                        "gpu_used_bytes": memory * 1024**2,
                        "gpu_utilization_percent": utilization,
                    }
                )
            except (OSError, ValueError, subprocess.SubprocessError):
                pass
            self.sample_stop.wait(1)

    def status(self):
        result = subprocess.run(
            [sys.executable, self.config.lease_tool, "status"],
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )
        return json.loads(result.stdout)

    def guard(self, *, require_clear=False):
        if time.monotonic() - self.started >= self.config.execution_window_s:
            raise LiveExecutionError("execution_window_exhausted")
        validate_lease(self.config, self.status(), require_clear=require_clear)
        cgroup = Path("/proc/self/cgroup").read_text()
        if not any(
            line.endswith("/" + self.config.unit) for line in cgroup.splitlines()
        ):
            raise LiveExecutionError("worker_unit_mismatch")

    def probe(self):
        root = Path(self.config.model_dir)
        if not root.is_dir() or root.is_symlink():
            raise LiveExecutionError("model_directory_invalid")
        for entry in self.config.files:
            path = root / entry.name
            if (
                path.is_symlink()
                or not path.is_file()
                or path.stat().st_size != entry.size
                or _sha256_file(path) != entry.sha256
            ):
                raise LiveExecutionError("model_identity_mismatch")
        for path_string, expected in self.config.runtime_files.items():
            path = Path(path_string)
            if not path.is_file() or _sha256_file(path) != expected:
                raise LiveExecutionError("runtime_identity_mismatch")
        for name, version in self.config.runtime_versions.items():
            if importlib.metadata.version(name) != version:
                raise LiveExecutionError("runtime_version_mismatch")
        gpu = (
            subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=uuid,name,memory.total,driver_version",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=15,
                check=True,
            )
            .stdout.strip()
            .splitlines()
        )
        if len(gpu) != 1:
            raise LiveExecutionError("gpu_topology_mismatch")
        uuid, name, mib, driver = [s.strip() for s in gpu[0].split(",")]
        if "H100" not in name:
            raise LiveExecutionError("gpu_identity_mismatch")
        return {
            "model_manifest_digest": _digest(
                [e.model_dump() for e in self.config.files]
            ),
            "runtime_digest": _digest(self.config.runtime_files),
            "runtime_versions": self.config.runtime_versions,
            "gpu_uuid": uuid,
            "gpu_name": name,
            "gpu_bytes": int(mib) * 1024**2,
            "driver_version": driver,
            "model_endpoint_network": "loopback",
            "orchestration_privacy": "private_network",
            "launch_environment": self.config.launch_environment(),
            "launch_digest": _digest(
                {
                    "command": self.config.command(),
                    "environment": self.config.launch_environment(),
                }
            ),
        }

    def start(self, cancelled: Callable[[], bool]):
        self.guard(require_clear=True)
        import socket

        with socket.socket() as sock:
            sock.bind(("127.0.0.1", self.config.port))
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_handle = self.log_path.open("x")
        env = {**os.environ, **self.config.launch_environment()}
        self.process = subprocess.Popen(
            self.config.command(),
            stdout=self.log_handle,
            stderr=subprocess.STDOUT,
            env=env,
            start_new_session=True,
        )
        self.sampler = threading.Thread(target=self._sample, daemon=True)
        self.sampler.start()
        deadline = min(
            self.started + self.config.execution_window_s, time.monotonic() + 600
        )
        while time.monotonic() < deadline:
            if cancelled():
                raise LiveExecutionError("cancelled")
            if self.process.poll() is not None:
                raise LiveExecutionError("runtime_exited")
            self.guard()
            try:
                models = loopback_json(self.config.endpoint, "/v1/models")
                if [m["id"] for m in models.get("data", [])] != [self.config.model_id]:
                    raise LiveExecutionError("served_model_mismatch")
                return
            except LiveExecutionError:
                raise
            except (OSError, ValueError):
                time.sleep(1)
        raise LiveExecutionError("readiness_timeout")

    def call(self, service: LiveServiceRequest):
        self.guard()
        remaining = self.config.execution_window_s - (time.monotonic() - self.started)
        return loopback_json(
            self.config.endpoint,
            "/v1/chat/completions",
            timeout=min(self.config.request_timeout_s, remaining),
            payload={
                "model": self.config.model_id,
                "temperature": 0,
                "max_tokens": self.config.max_tokens,
                "chat_template_kwargs": {"enable_thinking": False},
                "messages": [
                    {
                        "role": "system",
                        "content": "Return only the required JSON object. Use exactly the supplied allowed values. Use three distinct approved proof points. Preserve caveat order.",
                    },
                    {
                        "role": "user",
                        "content": json.dumps(service.model_dump(mode="json")),
                    },
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "bounded_brief",
                        "strict": True,
                        "schema": decoder_schema(service),
                    },
                },
            },
        )

    def stop(self):
        self.sample_stop.set()
        if self.sampler:
            self.sampler.join(timeout=6)
        started = self.process is not None
        if started:
            try:
                os.killpg(self.process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                self.process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(self.process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                self.process.wait(timeout=10)
        if self.log_handle:
            self.log_handle.close()
        return {
            "gpu_samples": self.samples,
            "gpu_sample_count": len(self.samples),
            "peak_sampled_gpu_used_bytes": max(
                (x["gpu_used_bytes"] for x in self.samples), default=None
            ),
            "memory_method": "1s nvidia-smi device-wide samples under exclusive lease; excludes host RAM; not an exact peak",
            "owned_process_stopped": not started or self.process.poll() is not None,
            "runtime_started": started,
            "borrowed_service_restoration": "pending_supervisor",
        }


def remote_plan(config: RemoteConfig, identity: dict):
    at = datetime.now(timezone.utc)
    hardware = HardwareProfile(
        profile_id="owned-h100-observed",
        captured_at=at,
        platform="Linux",
        architecture="x86_64",
        evidence_level="observed",
        memory_domains=[
            MemoryDomain(
                domain_id="gpu:0",
                kind="dedicated_gpu",
                total_bytes=identity["gpu_bytes"],
                source="nvidia-smi",
                evidence_ref="sha256:" + _digest(identity),
            )
        ],
        accelerators=[
            AcceleratorProfile(
                accelerator_id="gpu:0",
                vendor="NVIDIA",
                product=identity["gpu_name"],
                memory_domain_id="gpu:0",
                device_identifier=identity["gpu_uuid"],
            )
        ],
        runtime_candidates=["vllm-owned"],
    )
    weight_bytes = sum(e.size for e in config.files if e.name.endswith(".safetensors"))
    model = ModelResourceProfile(
        profile_id="qwen-bf16-observed",
        model_id=config.model_id,
        artifact_id="verified-sharded-safetensors",
        artifact_format="safetensors",
        quantization="BF16",
        artifact_bytes=weight_bytes,
        model_weight_bytes=weight_bytes,
        sha256=identity["model_manifest_digest"],
        source_revision=config.revision,
        evidence_level="observed",
        unknown_fields=["exact_tensor_payload_bytes"],
    )
    workload = WorkloadRequirements(
        workload_class="source_bounded_launch_brief",
        context_tokens=config.context_tokens,
        max_output_tokens=config.max_tokens,
        concurrency=1,
        estimated_kv_bytes=1024**3,
        runtime_reserve_bytes=8 * 1024**3,
        allow_network=True,
    )
    capability = RuntimeCapability(
        adapter_id="vllm-owned",
        executor_class="local_ai",
        supported_platforms=["Linux"],
        supported_architectures=["x86_64"],
        supported_artifact_formats=["safetensors"],
        memory_modes=["gpu_resident"],
        detected=True,
        evidence_level="observed",
        evidence_refs=["sha256:" + identity["runtime_digest"]],
    )
    return build_execution_plan(
        plan_id="bounded-owned-h100-v1",
        hardware=hardware,
        model=model,
        workload=workload,
        capabilities=[capability],
        adapter_priority=["vllm-owned"],
    )


class RemoteEvents:
    def __init__(self, run_id, config_digest, level):
        self.log = HeroEventLog(run_id)
        self.config_digest = config_digest
        self.level = level

    def emit(
        self,
        event_type,
        phase,
        status,
        *,
        task=None,
        attempt=1,
        executor="deterministic",
        adapter="deterministic_core",
        payload=None,
    ):
        n = len(self.log.events_after())
        self.log.append(
            HeroEvent(
                run_id=self.log.run_id,
                event_id=f"{self.log.run_id}:{n:04d}",
                sequence=n,
                occurred_at=datetime.now(timezone.utc),
                event_type=event_type,
                phase=phase,
                status=status,
                source="kora.hero_remote_execution",
                evidence_level=self.level,
                task_id=task,
                attempt=attempt if task else None,
                executor_class=executor if task else None,
                adapter_id=adapter if task else None,
                evidence_refs=("sha256:" + self.config_digest,),
                payload=payload or {},
            )
        )

    def begin(
        self,
        task,
        label,
        dependencies=(),
        *,
        executor="deterministic",
        adapter="deterministic_core",
        attempt=1,
        create=True,
    ):
        if create:
            self.emit(
                "task.created",
                "decompose",
                "created",
                task=task,
                payload={
                    "label": label,
                    "purpose": label,
                    "dependencies": list(dependencies),
                },
            )
        for typ, phase, status in [
            ("task.ready", "execute", "ready"),
            ("task.routed", "plan", "ready"),
            ("task.started", "execute", "running"),
        ]:
            self.emit(
                typ,
                phase,
                status,
                task=task,
                executor=executor,
                adapter=adapter,
                attempt=attempt,
            )


def run_remote_execution(
    config: RemoteConfig,
    service: LiveServiceRequest,
    controller,
    *,
    cancelled=lambda: False,
    evidence_level="observed",
):
    events = RemoteEvents(
        "hero-s02-h100-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"),
        _digest(config.model_dump(mode="json")),
        evidence_level,
    )
    events.emit("run.started", "intake", "running")
    started = time.monotonic()
    identity = plan = output = None
    attempts = []
    failure = None
    running = False
    attempt = 1
    cleanup = {"owned_process_stopped": False}
    try:
        if cancelled():
            raise LiveExecutionError("cancelled")
        identity = controller.probe()
        plan = remote_plan(config, identity)
        if plan.selected_adapter_id != "vllm-owned":
            raise LiveExecutionError("resource_plan_rejected")
        events.emit(
            "execution.plan.created",
            "plan",
            "completed",
            payload={
                "plan": plan.model_dump(mode="json"),
                "execution_location": "owned_remote_gpu",
                "orchestration_privacy": "private_network",
            },
        )
        events.begin("facts", "Check supplied facts")
        events.emit(
            "task.completed",
            "execute",
            "completed",
            task="facts",
            payload={"input_digest": _digest(service.model_dump(mode="json"))},
        )
        events.begin(
            "reuse",
            "Reuse approved fragment",
            executor="exact_reuse",
            adapter="exact_reuse_store",
        )
        events.emit(
            "task.completed",
            "execute",
            "completed",
            task="reuse",
            payload={"fragment_digest": _digest(service.approved_fragment)},
        )
        controller.start(cancelled)
        for attempt in range(1, config.max_calls + 1):
            if cancelled():
                raise LiveExecutionError("cancelled")
            events.begin(
                "draft",
                "Owned H100 structured draft",
                ("facts", "reuse"),
                executor="local_ai",
                adapter="vllm-owned",
                attempt=attempt,
                create=attempt == 1,
            )
            running = True
            sample = {
                "attempt": attempt,
                "tokens_in": None,
                "tokens_out": None,
                "time_ms": None,
                "status": "request_started",
            }
            attempts.append(sample)
            call_start = time.monotonic()
            response = controller.call(service)
            sample["time_ms"] = round((time.monotonic() - call_start) * 1000)
            if cancelled():
                raise LiveExecutionError("cancelled")
            if response.get("model") != config.model_id:
                raise LiveExecutionError("response_model_mismatch")
            usage = response.get("usage", {})
            ti, to = usage.get("prompt_tokens"), usage.get("completion_tokens")
            if (
                type(ti) is not int
                or type(to) is not int
                or ti < 0
                or ti + config.max_tokens > config.context_tokens
                or not 0 <= to <= config.max_tokens
            ):
                raise LiveExecutionError("usage_or_token_budget_invalid")
            sample.update(tokens_in=ti, tokens_out=to, status="response_received")
            choice = response["choices"][0]
            retry_code = None
            if choice.get("finish_reason") == "length":
                retry_code = "truncated_output"
            else:
                try:
                    draft = LiveDraft.model_validate_json(choice["message"]["content"])
                except (ValueError, TypeError):
                    retry_code = "malformed_output"
            if retry_code:
                sample["status"] = retry_code
                events.emit(
                    "task.failed",
                    "execute",
                    "failed",
                    task="draft",
                    attempt=attempt,
                    payload={"reason_code": retry_code},
                )
                running = False
                if attempt < config.max_calls:
                    events.emit(
                        "run.replanned",
                        "replan",
                        "replanned",
                        payload={"same_plan": True, "reason_code": retry_code},
                    )
                    continue
                raise LiveExecutionError(retry_code)
            failures = _validate_draft(draft, service)
            if failures:
                raise LiveExecutionError(failures[0])
            output = draft.model_dump(mode="json")
            sample["status"] = "objective_pass"
            events.emit(
                "telemetry.sampled",
                "execute",
                "running",
                task="draft",
                attempt=attempt,
                payload=sample,
            )
            break
        if time.monotonic() - started > config.execution_window_s:
            raise LiveExecutionError("execution_window_exhausted")
    except Exception as exc:  # noqa: BLE001 -- always retain failure and clean owned runtime
        failure = (
            exc.code if isinstance(exc, LiveExecutionError) else type(exc).__name__
        )
    finally:
        try:
            cleanup = controller.stop()
        except Exception:  # noqa: BLE001 -- cleanup failure must be retained
            cleanup = {"owned_process_stopped": False}
    if cleanup.get("owned_process_stopped") is not True:
        failure = "owned_cleanup_failed"
    if failure:
        if running:
            events.emit(
                "task.failed",
                "execute",
                "failed",
                task="draft",
                attempt=attempt,
                payload={"reason_code": failure},
            )
        events.emit(
            "run.escalated",
            "escalate",
            "escalated",
            payload={"reason_code": failure, "automatic_fallback": False},
        )
    else:
        events.emit(
            "task.completed",
            "execute",
            "completed",
            task="draft",
            attempt=attempt,
            payload={"output_digest": _digest(output)},
        )
        events.begin("review", "Independent supplied-value review", ("draft",))
        events.emit(
            "task.completed",
            "execute",
            "completed",
            task="review",
            payload={
                "schema": "pass",
                "supplied_values": "pass",
                "semantic_quality": "not_measured",
            },
        )
        events.emit("merge.started", "merge", "running")
        events.emit("merge.completed", "merge", "completed", payload={"answer": output})
        events.emit("verification.started", "verify", "running")
        events.emit("verification.passed", "verify", "completed")
        events.emit("run.completed", "complete", "completed")
    return {
        "schema_version": SCHEMA,
        "evidence_level": evidence_level,
        "run_id": events.log.run_id,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "request": service.model_dump(mode="json"),
        "decoder_schema_digest": _digest(decoder_schema(service)),
        "input_digest": _digest(service.model_dump(mode="json")),
        "config_digest": _digest(config.model_dump(mode="json")),
        "runtime_identity": identity,
        "plan": plan.model_dump(mode="json") if plan else None,
        "lease_id": config.lease_id,
        "approval_id": config.approval_id,
        "privacy_mode": "private_network",
        "execution_location": "owned_remote_gpu",
        "output": output,
        "output_digest": _digest(output) if output else None,
        "attempts": attempts,
        "cleanup": cleanup,
        "actual_execution": {
            "owned_remote_model_calls": len(attempts),
            "commercial_provider_calls": 0,
            "max_output_tokens": config.max_tokens,
            "execution_window_ms": round((time.monotonic() - started) * 1000),
        },
        "verification": {
            "objective_pass": failure is None,
            "failure_code": failure,
            "semantic_quality": "not_measured",
            "service_restoration": "pending_supervisor",
        },
        "claim_boundary": "Bounded owned-GPU output and structural supplied-value checks. No semantic, production, throughput, larger-than-VRAM or superiority result.",
        "event_log": events.log.snapshot(),
    }
