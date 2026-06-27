"""Provider-neutral model-call measurement primitives."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Protocol

LOCAL_VALIDATION_ADAPTER = "local_validation"
LOCAL_RUNTIME_ADAPTER = "local_runtime"
BLOCKED_ADAPTER = "blocked"
LOCAL_RUNTIME_PLACEHOLDER_ADAPTER = "local_runtime_placeholder"
LOCAL_RUNTIME_NOT_CONFIGURED_MODEL = "local-runtime-not-configured"

SUPPORTED_MODEL_CALL_ADAPTERS = (
    LOCAL_VALIDATION_ADAPTER,
    LOCAL_RUNTIME_ADAPTER,
    BLOCKED_ADAPTER,
    LOCAL_RUNTIME_PLACEHOLDER_ADAPTER,
)


def _estimate_tokens(text: str) -> int:
    """Return a stable, conservative token estimate for local validation."""
    return len(text.split()) if text.strip() else 0


@dataclass(frozen=True)
class ModelCallRequest:
    """Provider-neutral model-call request for validation harnesses."""

    request_id: str
    prompt: str
    metadata: dict[str, Any] = field(default_factory=dict)
    privacy_class: str = "synthetic"


@dataclass(frozen=True)
class ModelCallResponse:
    """Provider-neutral model-call response with measurement counters."""

    request_id: str
    output: str
    model_calls: int
    latency_ms: float | None
    input_tokens: int | None
    output_tokens: int | None
    provider: str | None
    model: str | None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LocalRuntimeAdapterConfig:
    """Inert future local runtime configuration for fail-closed adapters."""

    runtime: str = ""
    model: str | None = None
    endpoint: str | None = None
    command: str | None = None
    timeout_s: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelCallAdapter(Protocol):
    """Protocol implemented by model-call adapters used in validation."""

    def call(self, request: ModelCallRequest) -> ModelCallResponse:
        """Execute one model-call request and return measured counters."""


class DeterministicStubModelCallAdapter:
    """Local no-network adapter for deterministic validation tests."""

    provider = LOCAL_VALIDATION_ADAPTER
    model = "deterministic-local"

    def call(self, request: ModelCallRequest) -> ModelCallResponse:
        start = time.perf_counter()
        output = f"stub:{request.request_id}:{request.prompt.strip()[:80]}"
        latency_ms = (time.perf_counter() - start) * 1000.0
        return ModelCallResponse(
            request_id=request.request_id,
            output=output,
            model_calls=1,
            latency_ms=latency_ms,
            input_tokens=_estimate_tokens(request.prompt),
            output_tokens=_estimate_tokens(output),
            provider=self.provider,
            model=self.model,
            metadata={
                "privacy_class": request.privacy_class,
                "adapter": self.provider,
                "network": "none",
                "deterministic": True,
            },
        )


class DeterministicLocalRuntimeModelCallAdapter:
    """Explicit opt-in local runtime stub with deterministic in-process behavior."""

    provider = LOCAL_RUNTIME_ADAPTER
    model = "deterministic-local-runtime"

    def call(self, request: ModelCallRequest) -> ModelCallResponse:
        start = time.perf_counter()
        output = f"local_runtime:{request.request_id}:{request.prompt.strip()[:80]}"
        latency_ms = (time.perf_counter() - start) * 1000.0
        return ModelCallResponse(
            request_id=request.request_id,
            output=output,
            model_calls=1,
            latency_ms=latency_ms,
            input_tokens=_estimate_tokens(request.prompt),
            output_tokens=_estimate_tokens(output),
            provider=self.provider,
            model=self.model,
            metadata={
                "privacy_class": request.privacy_class,
                "adapter": self.provider,
                "network": "none",
                "runtime": "in_process_stub",
                "deterministic": True,
            },
        )


class BlockedModelCallAdapter:
    """Adapter that fails closed when real provider use is not configured."""

    def __init__(self, message: str | None = None) -> None:
        self.message = message or (
            "Real model-call adapter is not configured. Use an explicit local "
            "or remote adapter in a validation harness."
        )

    def call(self, request: ModelCallRequest) -> ModelCallResponse:
        del request
        raise RuntimeError(self.message)


class BlockedLocalRuntimeModelCallAdapter:
    """Fail-closed skeleton for future local runtime adapters."""

    provider = LOCAL_RUNTIME_PLACEHOLDER_ADAPTER
    model = LOCAL_RUNTIME_NOT_CONFIGURED_MODEL

    def __init__(
        self,
        config: LocalRuntimeAdapterConfig | None = None,
        message: str | None = None,
    ) -> None:
        self.config = config or LocalRuntimeAdapterConfig()
        self.message = message or (
            "Local runtime adapters are not implemented yet. No provider call "
            "was attempted. Use local_validation for local/no-network validation."
        )

    def call(self, request: ModelCallRequest) -> ModelCallResponse:
        del request
        raise RuntimeError(self.message)


def available_model_call_adapters() -> list[str]:
    """Return adapter kind labels supported by the selector."""

    return list(SUPPORTED_MODEL_CALL_ADAPTERS)


def select_model_call_adapter(kind: str | None = None) -> ModelCallAdapter:
    """Select a provider-neutral model-call adapter by kind.

    The default path is local no-network validation. The concrete local runtime
    path is an explicit opt-in deterministic in-process adapter.
    """

    selected_kind = kind or LOCAL_VALIDATION_ADAPTER
    if selected_kind == LOCAL_VALIDATION_ADAPTER:
        return DeterministicStubModelCallAdapter()
    if selected_kind == LOCAL_RUNTIME_ADAPTER:
        return DeterministicLocalRuntimeModelCallAdapter()
    if selected_kind == BLOCKED_ADAPTER:
        return BlockedModelCallAdapter()
    if selected_kind == LOCAL_RUNTIME_PLACEHOLDER_ADAPTER:
        return BlockedLocalRuntimeModelCallAdapter()

    supported = ", ".join(SUPPORTED_MODEL_CALL_ADAPTERS)
    raise ValueError(f"Unsupported model-call adapter kind {selected_kind!r}. Supported: {supported}")


@dataclass(frozen=True)
class ModelCallSummary:
    """Aggregate model-call counters for validation reports."""

    total_requests: int
    model_calls: int
    input_tokens_total: int | None
    output_tokens_total: int | None
    latency_total_ms: float | None
    error_count: int

    @classmethod
    def from_responses(
        cls,
        responses: list[ModelCallResponse],
        *,
        error_count: int = 0,
    ) -> "ModelCallSummary":
        input_tokens = [response.input_tokens for response in responses]
        output_tokens = [response.output_tokens for response in responses]
        latencies = [response.latency_ms for response in responses]
        return cls(
            total_requests=len(responses) + error_count,
            model_calls=sum(response.model_calls for response in responses),
            input_tokens_total=(
                sum(token for token in input_tokens if token is not None)
                if all(token is not None for token in input_tokens)
                else None
            ),
            output_tokens_total=(
                sum(token for token in output_tokens if token is not None)
                if all(token is not None for token in output_tokens)
                else None
            ),
            latency_total_ms=(
                sum(latency for latency in latencies if latency is not None)
                if all(latency is not None for latency in latencies)
                else None
            ),
            error_count=error_count,
        )
