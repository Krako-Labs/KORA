"""Bounded, opt-in Hero execution against a user-owned loopback model server.

This module has no ambient live mode. Callers must supply exact runtime/model
identities and an explicit controller. Remote endpoints and provider fallbacks
are rejected. Semantic quality remains outside the machine acceptance contract.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import socket
import subprocess
import threading
import time
from collections.abc import Callable
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
from urllib import error, parse, request

from pydantic import (
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
)

from kora.adapters.openai_compatible_local import (
    LocalOpenAICompatibleError,
    OpenAICompatibleLocalAdapter,
)
from kora.hero_contracts import (
    HardwareProfile,
    HeroEvent,
    ModelResourceProfile,
    StrictContract,
    WorkloadRequirements,
)
from kora.hero_event_log import HeroEventLog
from kora.hero_planner import HeroPlanningBundle, build_hero_planning_bundle


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
        ensure_ascii=False,
    )
    return hashlib.sha256(encoded.encode()).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _loopback_endpoint(value: str) -> str:
    endpoint = value.strip().rstrip("/")
    parsed = parse.urlparse(endpoint)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("endpoint must be loopback HTTP without credentials")
    if parsed.port is None:
        raise ValueError("endpoint must include an explicit port")
    return endpoint


class LiveExecutionError(RuntimeError):
    """Stable fail-closed error for the bounded live path."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class LiveServiceRequest(StrictContract):
    """Supplied values that make objective output grounding deterministic."""

    request_id: str = Field(min_length=1)
    facts: tuple[str, ...] = Field(min_length=3)
    approved_fragment: str = Field(min_length=1)
    allowed_headlines: tuple[str, ...] = Field(min_length=1)
    allowed_audiences: tuple[str, ...] = Field(min_length=1)
    allowed_promises: tuple[str, ...] = Field(min_length=1)
    approved_proof_points: tuple[str, ...] = Field(min_length=3)
    required_caveats: tuple[str, str]
    prohibited_claims: tuple[str, ...] = ()

    @field_validator(
        "facts",
        "allowed_headlines",
        "allowed_audiences",
        "allowed_promises",
        "approved_proof_points",
        "required_caveats",
        "prohibited_claims",
    )
    @classmethod
    def _strings_are_non_empty_and_unique(
        cls, values: tuple[str, ...]
    ) -> tuple[str, ...]:
        if any(not value.strip() for value in values):
            raise ValueError("request values must be non-empty")
        if len(values) != len(set(values)):
            raise ValueError("request values must be unique")
        return values


class LiveDraft(StrictContract):
    """The only model-produced structure accepted by Task038."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    headline: str = Field(min_length=1, max_length=240)
    audience: str = Field(min_length=1, max_length=240)
    promise: str = Field(min_length=1, max_length=360)
    proof_points: tuple[str, str, str]
    caveats: tuple[str, str]


LIVE_DRAFT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "headline": {"type": "string"},
        "audience": {"type": "string"},
        "promise": {"type": "string"},
        "proof_points": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 3,
        },
        "caveats": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2,
            "maxItems": 2,
        },
    },
    "required": ["headline", "audience", "promise", "proof_points", "caveats"],
    "additionalProperties": False,
}


def _schema_for_service(service: LiveServiceRequest) -> dict[str, Any]:
    schema = deepcopy(LIVE_DRAFT_SCHEMA)
    properties = schema["properties"]
    properties["headline"]["enum"] = list(service.allowed_headlines)
    properties["audience"]["enum"] = list(service.allowed_audiences)
    properties["promise"]["enum"] = list(service.allowed_promises)
    properties["proof_points"]["items"]["enum"] = list(service.approved_proof_points)
    properties["proof_points"]["uniqueItems"] = True
    properties["caveats"]["items"]["enum"] = list(service.required_caveats)
    return schema


class LiveExecutionConfig(StrictContract):
    """Frozen safety and budget bounds for one live session."""

    endpoint: str
    model_name: str = Field(min_length=1)
    runtime_id: str = Field(min_length=1)
    runtime_version: str = Field(min_length=1)
    runtime_binary_sha256: str
    model_artifact_sha256: str
    max_output_tokens: int = Field(default=256, ge=1, le=256)
    max_model_calls: int = Field(default=2, ge=1, le=3)
    timeout_s: float = Field(default=120.0, gt=0, le=600)
    live_window_s: float = Field(default=1200.0, gt=0, le=1200)

    @field_validator("endpoint")
    @classmethod
    def _endpoint_is_loopback(cls, value: str) -> str:
        return _loopback_endpoint(value)

    @field_validator("runtime_binary_sha256", "model_artifact_sha256")
    @classmethod
    def _digests_are_sha256(cls, value: str) -> str:
        normalized = value.lower()
        if len(normalized) != 64 or any(
            character not in "0123456789abcdef" for character in normalized
        ):
            raise ValueError("identity digest must be lowercase SHA-256")
        return normalized


class RuntimeController(Protocol):
    """Owned local runtime lifecycle used by the live orchestrator."""

    def probe(self) -> dict[str, Any]: ...

    def start(self) -> dict[str, Any]: ...

    def stop(self) -> dict[str, Any]: ...


class _RssSampler:
    def __init__(self, pid: int, interval_s: float = 0.05) -> None:
        self.pid = pid
        self.interval_s = interval_s
        self.peak_bytes: int | None = None
        self.sample_count = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def _run(self) -> None:
        while not self._stop.wait(self.interval_s):
            try:
                completed = subprocess.run(
                    ("ps", "-o", "rss=", "-p", str(self.pid)),
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=1,
                )
                kib = int(completed.stdout.strip())
            except (OSError, ValueError, subprocess.TimeoutExpired):
                continue
            self.sample_count += 1
            measured = kib * 1024
            self.peak_bytes = max(self.peak_bytes or 0, measured)


class LlamaCppServerController:
    """Start and stop exactly one owned llama.cpp loopback server."""

    def __init__(
        self,
        *,
        binary_path: str | os.PathLike[str],
        model_path: str | os.PathLike[str],
        config: LiveExecutionConfig,
        log_path: str | os.PathLike[str],
        context_tokens: int,
    ) -> None:
        self.binary_path = Path(binary_path)
        self.model_path = Path(model_path)
        self.config = config
        self.log_path = Path(log_path)
        self.context_tokens = context_tokens
        self._process: subprocess.Popen[bytes] | None = None
        self._log_handle: Any = None
        self._sampler: _RssSampler | None = None
        self._started_at: float | None = None
        self._probe: dict[str, Any] | None = None

    @staticmethod
    def _regular_file(path: Path, code: str) -> None:
        if path.is_symlink() or not path.is_file():
            raise LiveExecutionError(code)

    def probe(self) -> dict[str, Any]:
        self._regular_file(self.binary_path, "runtime_binary_missing_or_unsafe")
        self._regular_file(self.model_path, "model_artifact_missing_or_unsafe")
        if _sha256_file(self.binary_path) != self.config.runtime_binary_sha256:
            raise LiveExecutionError("runtime_identity_mismatch")
        if _sha256_file(self.model_path) != self.config.model_artifact_sha256:
            raise LiveExecutionError("model_identity_mismatch")
        environment = {
            **os.environ,
            "DYLD_LIBRARY_PATH": str(self.binary_path.parent),
            "LC_ALL": "C",
            "LANG": "C",
        }
        try:
            version = subprocess.run(
                (str(self.binary_path), "--version"),
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
                env=environment,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise LiveExecutionError("runtime_version_probe_failed") from exc
        version_text = (version.stdout + version.stderr).strip()
        if version.returncode != 0 or self.config.runtime_version not in version_text:
            raise LiveExecutionError("runtime_version_mismatch")
        self._probe = {
            "runtime_detected": True,
            "runtime_version": self.config.runtime_version,
            "runtime_binary_sha256": self.config.runtime_binary_sha256,
            "model_artifact_sha256": self.config.model_artifact_sha256,
            "model_artifact_bytes": self.model_path.stat().st_size,
            "platform": platform.system(),
            "architecture": platform.machine(),
            "network": "loopback",
        }
        return deepcopy(self._probe)

    def _port_is_available(self) -> bool:
        parsed = parse.urlparse(self.config.endpoint)
        assert parsed.port is not None
        family = socket.AF_INET6 if parsed.hostname == "::1" else socket.AF_INET
        host = "::1" if parsed.hostname == "::1" else "127.0.0.1"
        with socket.socket(family, socket.SOCK_STREAM) as candidate:
            candidate.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                candidate.bind((host, parsed.port))
            except OSError:
                return False
        return True

    def start(self) -> dict[str, Any]:
        if self._process is not None:
            raise LiveExecutionError("runtime_already_started")
        probe = self._probe or self.probe()
        if not self._port_is_available():
            raise LiveExecutionError("loopback_port_unavailable")
        parsed = parse.urlparse(self.config.endpoint)
        assert parsed.port is not None
        host = "::1" if parsed.hostname == "::1" else "127.0.0.1"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log_handle = self.log_path.open("wb")
        environment = {
            **os.environ,
            "DYLD_LIBRARY_PATH": str(self.binary_path.parent),
            "LC_ALL": "C",
            "LANG": "C",
        }
        command = (
            str(self.binary_path),
            "--model",
            str(self.model_path),
            "--host",
            host,
            "--port",
            str(parsed.port),
            "--ctx-size",
            str(self.context_tokens),
            "--n-predict",
            str(self.config.max_output_tokens),
            "--parallel",
            "1",
            "--no-webui",
            "--metrics",
        )
        try:
            self._process = subprocess.Popen(
                command,
                stdin=subprocess.DEVNULL,
                stdout=self._log_handle,
                stderr=subprocess.STDOUT,
                env=environment,
                start_new_session=True,
            )
        except OSError as exc:
            self._log_handle.close()
            self._log_handle = None
            raise LiveExecutionError("runtime_start_failed") from exc
        self._started_at = time.monotonic()
        self._sampler = _RssSampler(self._process.pid)
        self._sampler.start()
        deadline = self._started_at + min(self.config.timeout_s, 180)
        health_url = self.config.endpoint + "/health"
        while time.monotonic() < deadline:
            if self._process.poll() is not None:
                raise LiveExecutionError("runtime_exited_before_ready")
            try:
                with request.urlopen(health_url, timeout=2) as response:
                    payload = json.load(response)
                if response.status == 200 and isinstance(payload, dict):
                    return {
                        **deepcopy(probe),
                        "runtime_started": True,
                        "runtime_starts": 1,
                        "pid_recorded_locally": True,
                    }
            except (OSError, error.URLError, json.JSONDecodeError):
                pass
            time.sleep(0.25)
        raise LiveExecutionError("runtime_readiness_timeout")

    def stop(self) -> dict[str, Any]:
        process = self._process
        if process is None:
            return {
                "cleanup_success": True,
                "runtime_was_started": False,
                "peak_process_rss_bytes": None,
                "rss_sample_count": 0,
            }
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        if self._sampler is not None:
            self._sampler.stop()
        if self._log_handle is not None:
            self._log_handle.close()
        cleanup = {
            "cleanup_success": process.poll() is not None,
            "runtime_was_started": True,
            "exit_code": process.returncode,
            "peak_process_rss_bytes": (
                self._sampler.peak_bytes if self._sampler is not None else None
            ),
            "rss_sample_count": (
                self._sampler.sample_count if self._sampler is not None else 0
            ),
            "rss_method": "ps child-process RSS sampled at 50 ms; not total system peak",
            "live_window_ms": (
                round((time.monotonic() - self._started_at) * 1000)
                if self._started_at is not None
                else None
            ),
        }
        self._process = None
        return cleanup


class ExistingLlamaCppServerController(LlamaCppServerController):
    """Borrow an idle project-local server without stopping or reconfiguring it."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._existing_pid: int | None = None

    def _health(self) -> bool:
        try:
            with request.urlopen(
                self.config.endpoint + "/health", timeout=3
            ) as response:
                payload = json.load(response)
            return response.status == 200 and isinstance(payload, dict)
        except (OSError, error.URLError, json.JSONDecodeError):
            return False

    def _listener_pid(self) -> int:
        parsed = parse.urlparse(self.config.endpoint)
        assert parsed.port is not None
        try:
            found = subprocess.run(
                (
                    "lsof",
                    "-nP",
                    "-t",
                    f"-iTCP:{parsed.port}",
                    "-sTCP:LISTEN",
                ),
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )
            pids = {int(value) for value in found.stdout.split() if value.isdigit()}
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise LiveExecutionError("existing_runtime_listener_probe_failed") from exc
        if found.returncode != 0 or len(pids) != 1:
            raise LiveExecutionError("existing_runtime_listener_not_unique")
        pid = pids.pop()
        try:
            described = subprocess.run(
                ("ps", "-p", str(pid), "-o", "command="),
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise LiveExecutionError("existing_runtime_process_probe_failed") from exc
        command = described.stdout.strip()
        if (
            described.returncode != 0
            or str(self.binary_path) not in command
            or str(self.model_path) not in command
        ):
            raise LiveExecutionError("existing_runtime_process_identity_mismatch")
        return pid

    def start(self) -> dict[str, Any]:
        if self._existing_pid is not None:
            raise LiveExecutionError("runtime_already_started")
        probe = self._probe or self.probe()
        if not self._health():
            raise LiveExecutionError("existing_runtime_not_healthy")
        self._existing_pid = self._listener_pid()
        self._started_at = time.monotonic()
        self._sampler = _RssSampler(self._existing_pid)
        self._sampler.start()
        return {
            **deepcopy(probe),
            "runtime_started": True,
            "runtime_starts": 0,
            "preexisting_runtime": True,
            "listener_identity_verified": True,
        }

    def stop(self) -> dict[str, Any]:
        if self._existing_pid is None:
            return {
                "cleanup_success": True,
                "runtime_was_started": False,
                "preexisting_runtime_preserved": True,
                "peak_process_rss_bytes": None,
                "rss_sample_count": 0,
            }
        if self._sampler is not None:
            self._sampler.stop()
        same_pid = False
        try:
            same_pid = self._listener_pid() == self._existing_pid
        except LiveExecutionError:
            same_pid = False
        healthy = self._health()
        result = {
            "cleanup_success": bool(same_pid and healthy),
            "runtime_was_started": False,
            "preexisting_runtime_preserved": bool(same_pid and healthy),
            "peak_process_rss_bytes": (
                self._sampler.peak_bytes if self._sampler is not None else None
            ),
            "rss_sample_count": (
                self._sampler.sample_count if self._sampler is not None else 0
            ),
            "rss_method": (
                "preexisting llama-server process RSS sampled at 50 ms; "
                "not total system peak"
            ),
            "live_window_ms": (
                round((time.monotonic() - self._started_at) * 1000)
                if self._started_at is not None
                else None
            ),
        }
        self._existing_pid = None
        return result


def _validate_draft(draft: LiveDraft, service: LiveServiceRequest) -> list[str]:
    checks: list[str] = []
    if draft.headline not in service.allowed_headlines:
        checks.append("headline_not_supplied")
    if draft.audience not in service.allowed_audiences:
        checks.append("audience_not_supplied")
    if draft.promise not in service.allowed_promises:
        checks.append("promise_not_supplied")
    if len(set(draft.proof_points)) != 3 or any(
        point not in service.approved_proof_points for point in draft.proof_points
    ):
        checks.append("proof_point_not_supplied")
    if draft.caveats != service.required_caveats:
        checks.append("required_caveats_not_preserved")
    combined = json.dumps(draft.model_dump(mode="json"), ensure_ascii=False).lower()
    if any(claim.lower() in combined for claim in service.prohibited_claims):
        checks.append("prohibited_claim")
    return checks


class _LiveBridge:
    def __init__(
        self,
        *,
        bundle: HeroPlanningBundle,
        hardware: HardwareProfile,
        model: ModelResourceProfile,
        workload: WorkloadRequirements,
        service: LiveServiceRequest,
        config: LiveExecutionConfig,
        controller: RuntimeController,
        adapter_factory: Callable[[], OpenAICompatibleLocalAdapter],
        cancelled: Callable[[], bool],
    ) -> None:
        self.bundle = HeroPlanningBundle.model_validate(bundle.model_dump(mode="json"))
        self.hardware = HardwareProfile.model_validate(hardware.model_dump(mode="json"))
        self.model = ModelResourceProfile.model_validate(model.model_dump(mode="json"))
        self.workload = WorkloadRequirements.model_validate(
            workload.model_dump(mode="json")
        )
        self.service = service
        self.config = config
        self.controller = controller
        self.adapter_factory = adapter_factory
        self.cancelled = cancelled
        self.at = datetime.now(timezone.utc)
        self.log = HeroEventLog(self.bundle.events[0].run_id)
        self.log.extend(deepcopy(self.bundle.events))
        self.call_count = 0
        self.runtime_starts = 0
        self.runtime_identity: dict[str, Any] | None = None
        self.cleanup: dict[str, Any] = {
            "cleanup_success": False,
            "runtime_was_started": False,
        }
        self.draft: LiveDraft | None = None
        self.usage: list[dict[str, Any]] = []
        self.failure_code: str | None = None
        self.started_at = time.monotonic()

    def emit(
        self,
        event_type: str,
        phase: str,
        status: str,
        *,
        task_id: str | None = None,
        attempt: int | None = None,
        executor_class: str | None = None,
        adapter_id: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        projection = self.log.projection
        assert projection is not None
        sequence = projection.last_sequence + 1
        refs = (
            f"sha256:{self.bundle.evidence_digest}",
            f"sha256:{self.config.model_artifact_sha256}",
            f"sha256:{self.config.runtime_binary_sha256}",
        )
        self.log.append(
            HeroEvent(
                event_id=f"{self.log.run_id}:{sequence:04d}",
                run_id=self.log.run_id,
                sequence=sequence,
                occurred_at=self.at,
                event_type=event_type,
                phase=phase,
                status=status,
                source="kora.hero_live_execution",
                evidence_level="observed",
                task_id=task_id,
                attempt=attempt,
                executor_class=executor_class,
                adapter_id=adapter_id,
                evidence_refs=refs,
                payload={
                    "mode": "live_local_bounded",
                    "actual_model_calls": self.call_count,
                    "actual_provider_calls": 0,
                    "runtime_starts": self.runtime_starts,
                    **(payload or {}),
                },
            )
        )

    def task_start(
        self,
        task_id: str,
        label: str,
        purpose: str,
        dependencies: tuple[str, ...],
        executor_class: str,
        adapter_id: str,
        *,
        attempt: int = 1,
        create: bool = False,
    ) -> None:
        if create:
            self.emit(
                "task.created",
                "decompose",
                "created",
                task_id=task_id,
                attempt=attempt,
                payload={
                    "label": label,
                    "purpose": purpose,
                    "dependencies": list(dependencies),
                },
            )
        self.emit("task.ready", "execute", "ready", task_id=task_id, attempt=attempt)
        self.emit(
            "task.routed",
            "plan",
            "ready",
            task_id=task_id,
            attempt=attempt,
            executor_class=executor_class,
            adapter_id=adapter_id,
        )
        self.emit(
            "task.started",
            "execute",
            "running",
            task_id=task_id,
            attempt=attempt,
            executor_class=executor_class,
            adapter_id=adapter_id,
            payload={
                "effective_config": deepcopy(self.bundle.plan.effective_config),
                "effective_config_digest": _digest(self.bundle.plan.effective_config),
            },
        )

    def complete_supplied(
        self,
        task_id: str,
        label: str,
        purpose: str,
        dependencies: tuple[str, ...],
        executor_class: str,
        adapter_id: str,
        result: Any,
    ) -> None:
        self.task_start(
            task_id,
            label,
            purpose,
            dependencies,
            executor_class,
            adapter_id,
            create=True,
        )
        self.emit(
            "task.completed",
            "execute",
            "completed",
            task_id=task_id,
            attempt=1,
            executor_class=executor_class,
            adapter_id=adapter_id,
            payload={"result": result},
        )

    def fail(self, code: str, *, task_running: bool = False, attempt: int = 1) -> None:
        self.failure_code = code
        if task_running:
            self.emit(
                "task.failed",
                "execute",
                "failed",
                task_id="draft",
                attempt=attempt,
                executor_class="local_ai",
                adapter_id="llama.cpp",
                payload={"reason": code, "reason_code": code},
            )
        self.emit(
            "escalation.required",
            "escalate",
            "escalated",
            payload={"reason": code, "reason_code": code, "automatic_fallback": False},
        )
        self.emit(
            "run.escalated",
            "escalate",
            "escalated",
            payload={"reason": code, "reason_code": code, "automatic_fallback": False},
        )

    def _call(self, attempt: int) -> tuple[LiveDraft | None, str | None]:
        if self.cancelled():
            return None, "cancelled"
        if self.call_count >= self.config.max_model_calls:
            return None, "model_call_budget_exhausted"
        adapter = self.adapter_factory()
        identity = adapter.cache_identity()
        if (
            identity["endpoint"] != self.config.endpoint
            or identity["model"] != self.config.model_name
            or identity["runtime_id"] != self.config.runtime_id
        ):
            return None, "adapter_identity_mismatch"
        self.call_count += 1
        self.emit(
            "adapter.started",
            "execute",
            "running",
            task_id="draft",
            attempt=attempt,
            executor_class="local_ai",
            adapter_id="llama.cpp",
            payload={"adapter_identity": identity},
        )
        try:
            result = adapter.run(
                task_id="hero-s02-live-draft",
                input=self.service.model_dump(mode="json"),
                budget={"max_tokens": self.config.max_output_tokens},
                output_schema=_schema_for_service(self.service),
            )
        except LocalOpenAICompatibleError as exc:
            message = str(exc)
            if "truncated output" in message:
                return None, "truncated_output"
            if "invalid JSON output" in message:
                return None, "malformed_output"
            return None, "runtime_request_failed"
        meta = result.get("meta", {})
        if (
            meta.get("network") != "loopback"
            or meta.get("provider") != "local"
            or meta.get("remote_provider_calls") != 0
            or meta.get("model_calls") != 1
        ):
            return None, "telemetry_identity_mismatch"
        usage = result.get("usage")
        if not isinstance(usage, dict):
            return None, "telemetry_usage_invalid"
        tokens_out = usage.get("tokens_out")
        if isinstance(tokens_out, bool) or not isinstance(tokens_out, int):
            return None, "telemetry_usage_invalid"
        if tokens_out < 0:
            return None, "telemetry_usage_invalid"
        if tokens_out > self.config.max_output_tokens:
            return None, "output_token_budget_exceeded"
        try:
            draft = LiveDraft.model_validate(result.get("output"))
        except ValidationError:
            return None, "malformed_output"
        objective_failures = _validate_draft(draft, self.service)
        self.usage.append(deepcopy(usage))
        self.emit(
            "telemetry.sampled",
            "execute",
            "running",
            task_id="draft",
            attempt=attempt,
            executor_class="local_ai",
            adapter_id="llama.cpp",
            payload={
                "usage": deepcopy(usage),
                "output_digest": _digest(draft.model_dump(mode="json")),
            },
        )
        if objective_failures:
            return None, objective_failures[0]
        self.emit(
            "adapter.completed",
            "execute",
            "completed",
            task_id="draft",
            attempt=attempt,
            executor_class="local_ai",
            adapter_id="llama.cpp",
            payload={"output_digest": _digest(draft.model_dump(mode="json"))},
        )
        return draft, None

    def run(self) -> dict[str, Any]:
        selected = self.bundle.plan.selected_adapter_id
        if (
            selected != "llama.cpp"
            or self.bundle.plan.evidence_level == "fixture"
            or self.hardware.evidence_level == "fixture"
            or self.model.evidence_level == "fixture"
            or self.model.sha256 != self.config.model_artifact_sha256
            or self.workload.allow_network
        ):
            self.fail("live_plan_or_identity_mismatch")
            return self.result()
        rebuilt = build_hero_planning_bundle(
            run_id=self.bundle.events[0].run_id,
            plan_id=self.bundle.plan.plan_id,
            occurred_at=self.bundle.events[0].occurred_at,
            hardware=self.hardware,
            model=self.model,
            workload=self.workload,
        )
        if rebuilt != self.bundle:
            self.fail("planning_evidence_mismatch")
            return self.result()

        tasks = (
            (
                "facts",
                "Check supplied facts",
                "Validate bounded supplied values.",
                (),
                "deterministic",
                "deterministic_core",
            ),
            (
                "reuse",
                "Reuse approved fragment",
                "Reuse an exact approved fragment.",
                (),
                "exact_reuse",
                "exact_reuse_store",
            ),
            (
                "draft",
                "Draft bounded service brief",
                "Produce the approved structured local draft.",
                ("facts", "reuse"),
                "local_ai",
                "llama.cpp",
            ),
            (
                "review",
                "Independent deterministic review",
                "Check schema, grounding, claims, and caveats.",
                ("draft",),
                "deterministic",
                "deterministic_review",
            ),
        )
        self.emit(
            "graph.created",
            "decompose",
            "completed",
            payload={"task_ids": [task[0] for task in tasks]},
        )
        self.complete_supplied(
            *tasks[0], result={"facts_digest": _digest(self.service.facts)}
        )
        self.complete_supplied(*tasks[1], result=self.service.approved_fragment)
        self.task_start(*tasks[2], create=True)

        attempt = 1
        task_running = True
        try:
            self.runtime_identity = self.controller.probe()
            self.emit(
                "adapter.probed",
                "execute",
                "completed",
                task_id="draft",
                attempt=attempt,
                executor_class="local_ai",
                adapter_id="llama.cpp",
                payload={"runtime_identity": deepcopy(self.runtime_identity)},
            )
            started = self.controller.start()
            self.runtime_starts = int(started.get("runtime_starts", 1))
            self.runtime_identity = deepcopy(started)
            self.emit(
                "adapter.prepared",
                "execute",
                "ready",
                task_id="draft",
                attempt=attempt,
                executor_class="local_ai",
                adapter_id="llama.cpp",
                payload={"runtime_identity": deepcopy(self.runtime_identity)},
            )
            while True:
                draft, failure = self._call(attempt)
                if draft is not None:
                    self.draft = draft
                    break
                assert failure is not None
                self.emit(
                    "adapter.execute.failed",
                    "execute",
                    "failed",
                    task_id="draft",
                    attempt=attempt,
                    executor_class="local_ai",
                    adapter_id="llama.cpp",
                    payload={"reason": failure, "reason_code": failure},
                )
                self.emit(
                    "task.failed",
                    "execute",
                    "failed",
                    task_id="draft",
                    attempt=attempt,
                    executor_class="local_ai",
                    adapter_id="llama.cpp",
                    payload={"reason": failure, "reason_code": failure},
                )
                task_running = False
                if (
                    failure not in {"malformed_output", "truncated_output"}
                    or attempt >= 2
                ):
                    self.fail(failure, task_running=False, attempt=attempt)
                    break
                self.emit(
                    "run.replanned",
                    "replan",
                    "replanned",
                    payload={
                        "reason": failure,
                        "reason_code": failure,
                        "replan_strategy": "bounded_same_plan_retry",
                    },
                )
                self.emit(
                    "execution.plan.reaffirmed",
                    "replan",
                    "replanned",
                    payload={
                        "plan_id": self.bundle.plan.plan_id,
                        "planning_digest": self.bundle.evidence_digest,
                    },
                )
                attempt += 1
                self.task_start(*tasks[2], attempt=attempt, create=False)
                task_running = True
        except LiveExecutionError as exc:
            self.fail(exc.code, task_running=task_running, attempt=attempt)
        finally:
            try:
                self.cleanup = self.controller.stop()
            except (OSError, RuntimeError, ValueError):
                self.cleanup = {
                    "cleanup_success": False,
                    "runtime_was_started": self.runtime_starts > 0,
                    "reason_code": "cleanup_failed",
                }
            self.emit(
                "adapter.cleaned",
                "execute",
                "completed" if self.cleanup.get("cleanup_success") else "failed",
                task_id="draft",
                attempt=attempt,
                executor_class="local_ai",
                adapter_id="llama.cpp",
                payload={"cleanup": deepcopy(self.cleanup)},
            )

        live_window_ms = self.cleanup.get("live_window_ms")
        if (
            isinstance(live_window_ms, (int, float))
            and live_window_ms > self.config.live_window_s * 1000
            and self.failure_code is None
        ):
            self.fail(
                "live_window_exceeded", task_running=task_running, attempt=attempt
            )
        if self.failure_code is not None:
            if not self.cleanup.get("cleanup_success"):
                self.failure_code = "cleanup_failed"
                self.emit(
                    "cleanup.failed",
                    "fail",
                    "failed",
                    payload={"reason_code": "cleanup_failed"},
                )
            return self.result()
        if not self.cleanup.get("cleanup_success"):
            self.fail("cleanup_failed", task_running=task_running, attempt=attempt)
            return self.result()
        if self.draft is None:
            self.fail("no_completed_output", task_running=task_running, attempt=attempt)
            return self.result()
        self.emit(
            "task.completed",
            "execute",
            "completed",
            task_id="draft",
            attempt=attempt,
            executor_class="local_ai",
            adapter_id="llama.cpp",
            payload={
                "result": self.draft.model_dump(mode="json"),
                "output_digest": _digest(self.draft.model_dump(mode="json")),
            },
        )
        self.complete_supplied(
            *tasks[3],
            result={
                "schema": "pass",
                "grounding": "exact_supplied_values_pass",
                "prohibited_claims": "pass",
                "required_caveats": "pass",
            },
        )
        self.emit("merge.started", "merge", "running")
        self.emit(
            "merge.completed",
            "merge",
            "completed",
            payload={"answer": self.draft.model_dump(mode="json")},
        )
        self.emit("verification.started", "verify", "running")
        self.emit(
            "verification.passed",
            "verify",
            "completed",
            payload={
                "service_acceptance": "objective_pass",
                "structural_acceptance": "pass",
                "semantic_non_regression": "not_measured",
                "checks": [
                    "schema",
                    "exact_supplied_value_grounding",
                    "prohibited_claims",
                    "required_caveats",
                    "cleanup",
                ],
            },
        )
        self.emit("run.completed", "complete", "completed")
        return self.result()

    def result(self) -> dict[str, Any]:
        projection = self.log.projection
        accepted = bool(
            projection
            and projection.accepted_outcome
            and self.draft is not None
            and self.cleanup.get("cleanup_success")
        )
        return {
            "schema_version": "hero.live-execution-evidence.v1",
            "run_id": self.log.run_id,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "evidence_level": "observed",
            "claim_boundary": (
                "One bounded local execution. Objective schema and supplied-value "
                "checks only; semantic quality, preference, production behavior, "
                "larger-than-VRAM behavior, and performance superiority are not measured."
            ),
            "planning_digest": self.bundle.evidence_digest,
            "hardware_digest": _digest(self.hardware.model_dump(mode="json")),
            "model_profile_digest": _digest(self.model.model_dump(mode="json")),
            "runtime_identity": deepcopy(self.runtime_identity),
            "effective_config": deepcopy(self.bundle.plan.effective_config),
            "effective_config_digest": _digest(self.bundle.plan.effective_config),
            "input_digest": _digest(self.service.model_dump(mode="json")),
            "output_digest": (
                _digest(self.draft.model_dump(mode="json")) if self.draft else None
            ),
            "output": self.draft.model_dump(mode="json") if self.draft else None,
            "usage": deepcopy(self.usage),
            "cleanup": deepcopy(self.cleanup),
            "actual_execution": {
                "runtime_starts": self.runtime_starts,
                "model_calls": self.call_count,
                "provider_calls": 0,
                "live_window_ms": round((time.monotonic() - self.started_at) * 1000),
            },
            "verification": {
                "accepted_outcome": accepted,
                "service_acceptance": "objective_pass" if accepted else "failed",
                "semantic_non_regression": "not_measured",
                "failure_code": self.failure_code,
            },
            "A_workload_control": {
                "deterministic_fact_check": "completed" if accepted else "incomplete",
                "exact_reuse": "completed" if accepted else "incomplete",
                "local_model_draft": "completed" if accepted else "incomplete",
                "deterministic_review": "completed" if accepted else "incomplete",
            },
            "B_local_execution": {
                "execution_performed": self.call_count > 0,
                "peak_process_rss_bytes": self.cleanup.get("peak_process_rss_bytes"),
                "rss_sample_count": self.cleanup.get("rss_sample_count", 0),
                "rss_method": self.cleanup.get("rss_method"),
                "semantic_quality_measured": False,
            },
            "event_log": self.log.snapshot(),
        }


def run_live_execution(
    *,
    bundle: HeroPlanningBundle,
    hardware: HardwareProfile,
    model: ModelResourceProfile,
    workload: WorkloadRequirements,
    service: LiveServiceRequest,
    config: LiveExecutionConfig,
    controller: RuntimeController,
    adapter_factory: Callable[[], OpenAICompatibleLocalAdapter] | None = None,
    cancelled: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Run one explicitly configured bounded local session."""

    if adapter_factory is None:
        environment = {
            "KORA_LOCAL_OPENAI_ENDPOINT": config.endpoint,
            "KORA_LOCAL_OPENAI_MODEL": config.model_name,
            "KORA_LOCAL_OPENAI_RUNTIME_ID": config.runtime_id,
            "KORA_LOCAL_OPENAI_TIMEOUT_S": str(config.timeout_s),
            "KORA_LOCAL_OPENAI_DISABLE_THINKING": "true",
        }
        adapter_factory = lambda: OpenAICompatibleLocalAdapter(environ=environment)
    return _LiveBridge(
        bundle=bundle,
        hardware=hardware,
        model=model,
        workload=workload,
        service=service,
        config=config,
        controller=controller,
        adapter_factory=adapter_factory,
        cancelled=cancelled or (lambda: False),
    ).run()


def write_live_evidence(
    output_path: str | os.PathLike[str], evidence: dict[str, Any]
) -> Path:
    """Atomically retain one local-only live evidence record."""

    if evidence.get("schema_version") != "hero.live-execution-evidence.v1":
        raise LiveExecutionError("invalid_live_evidence_schema")
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp")
    temporary.write_text(
        json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, target)
    return target


__all__ = [
    "LIVE_DRAFT_SCHEMA",
    "ExistingLlamaCppServerController",
    "LiveDraft",
    "LiveExecutionConfig",
    "LiveExecutionError",
    "LiveServiceRequest",
    "LlamaCppServerController",
    "RuntimeController",
    "run_live_execution",
    "write_live_evidence",
]
