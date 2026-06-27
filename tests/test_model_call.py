import os

import pytest

from kora.model_call import (
    BLOCKED_ADAPTER,
    BlockedLocalRuntimeModelCallAdapter,
    BlockedModelCallAdapter,
    DeterministicStubModelCallAdapter,
    DeterministicLocalRuntimeModelCallAdapter,
    LOCAL_RUNTIME_ADAPTER,
    LOCAL_RUNTIME_PLACEHOLDER_ADAPTER,
    LOCAL_VALIDATION_ADAPTER,
    LocalRuntimeAdapterConfig,
    ModelCallRequest,
    ModelCallSummary,
    available_model_call_adapters,
    select_model_call_adapter,
)


def test_stub_adapter_returns_deterministic_response() -> None:
    adapter = DeterministicStubModelCallAdapter()
    request = ModelCallRequest(request_id="req-1", prompt="Classify this request")

    first = adapter.call(request)
    second = adapter.call(request)

    assert first.output == second.output
    assert first.request_id == "req-1"
    assert first.output == "stub:req-1:Classify this request"


def test_stub_adapter_records_one_model_call_per_call() -> None:
    adapter = DeterministicStubModelCallAdapter()

    response = adapter.call(ModelCallRequest(request_id="req-2", prompt="Hello"))

    assert response.model_calls == 1
    assert response.latency_ms is not None
    assert response.latency_ms >= 0


def test_stub_adapter_token_estimates_are_stable() -> None:
    adapter = DeterministicStubModelCallAdapter()
    request = ModelCallRequest(request_id="req-3", prompt="one two three")

    response = adapter.call(request)

    assert response.input_tokens == 3
    assert response.output_tokens == 3


def test_stub_adapter_provider_model_and_metadata_are_local_safe() -> None:
    adapter = DeterministicStubModelCallAdapter()
    request = ModelCallRequest(
        request_id="req-4",
        prompt="safe synthetic prompt",
        privacy_class="synthetic",
    )

    response = adapter.call(request)

    assert response.provider == "local_validation"
    assert response.model == "deterministic-local"
    assert response.metadata["privacy_class"] == "synthetic"
    assert response.metadata["network"] == "none"
    assert response.metadata["deterministic"] is True


def test_stub_adapter_requires_no_secrets_or_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    response = DeterministicStubModelCallAdapter().call(
        ModelCallRequest(request_id="req-5", prompt="local only")
    )

    assert response.model_calls == 1
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ


def test_local_runtime_adapter_returns_deterministic_response() -> None:
    adapter = DeterministicLocalRuntimeModelCallAdapter()
    request = ModelCallRequest(request_id="req-local-1", prompt="Classify this request")

    first = adapter.call(request)
    second = adapter.call(request)

    assert first.output == second.output
    assert first.output == "local_runtime:req-local-1:Classify this request"
    assert first.model_calls == 1
    assert first.provider == LOCAL_RUNTIME_ADAPTER
    assert first.model == "deterministic-local-runtime"
    assert first.metadata["network"] == "none"
    assert first.metadata["runtime"] == "in_process_stub"
    assert first.metadata["deterministic"] is True


def test_local_runtime_adapter_requires_no_secrets_or_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_RUNTIME", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_ENDPOINT", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_NAME", raising=False)

    response = DeterministicLocalRuntimeModelCallAdapter().call(
        ModelCallRequest(request_id="req-local-2", prompt="local runtime only")
    )

    assert response.model_calls == 1
    assert response.provider == LOCAL_RUNTIME_ADAPTER
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ
    assert "KORA_LOCAL_MODEL_RUNTIME" not in os.environ
    assert "KORA_LOCAL_MODEL_ENDPOINT" not in os.environ
    assert "KORA_LOCAL_MODEL_NAME" not in os.environ


def test_model_call_summary_aggregates_counters() -> None:
    adapter = DeterministicStubModelCallAdapter()
    responses = [
        adapter.call(ModelCallRequest(request_id="req-6", prompt="alpha beta")),
        adapter.call(ModelCallRequest(request_id="req-7", prompt="gamma")),
    ]

    summary = ModelCallSummary.from_responses(responses, error_count=1)

    assert summary.total_requests == 3
    assert summary.model_calls == 2
    assert summary.input_tokens_total == 3
    assert summary.output_tokens_total == 3
    assert summary.latency_total_ms is not None
    assert summary.error_count == 1


def test_model_call_summary_preserves_unknown_token_totals() -> None:
    adapter = DeterministicStubModelCallAdapter()
    response = adapter.call(ModelCallRequest(request_id="req-8", prompt="known"))
    response_without_tokens = type(response)(
        request_id=response.request_id,
        output=response.output,
        model_calls=response.model_calls,
        latency_ms=response.latency_ms,
        input_tokens=None,
        output_tokens=response.output_tokens,
        provider=response.provider,
        model=response.model,
        metadata=response.metadata,
    )

    summary = ModelCallSummary.from_responses([response, response_without_tokens])

    assert summary.input_tokens_total is None
    assert summary.output_tokens_total is not None


def test_blocked_adapter_fails_closed() -> None:
    adapter = BlockedModelCallAdapter()

    with pytest.raises(RuntimeError, match="Real model-call adapter is not configured"):
        adapter.call(ModelCallRequest(request_id="req-9", prompt="blocked"))


def test_local_runtime_config_can_be_created_with_defaults() -> None:
    config = LocalRuntimeAdapterConfig()

    assert config.runtime == ""
    assert config.model is None
    assert config.endpoint is None
    assert config.command is None
    assert config.timeout_s is None
    assert config.metadata == {}


def test_local_runtime_config_metadata_default_is_not_shared() -> None:
    first = LocalRuntimeAdapterConfig()
    second = LocalRuntimeAdapterConfig()

    first.metadata["runtime"] = "example"

    assert second.metadata == {}


def test_blocked_local_runtime_adapter_fails_closed_without_prompt_leak() -> None:
    adapter = BlockedLocalRuntimeModelCallAdapter()
    raw_prompt = "do not include this raw synthetic prompt"

    with pytest.raises(RuntimeError) as exc_info:
        adapter.call(ModelCallRequest(request_id="req-local-runtime", prompt=raw_prompt))

    message = str(exc_info.value)
    assert "Local runtime adapters are not implemented yet" in message
    assert "No provider call was attempted" in message
    assert "local_validation" in message
    assert raw_prompt not in message


def test_blocked_local_runtime_adapter_accepts_inert_config() -> None:
    config = LocalRuntimeAdapterConfig(
        runtime="ollama",
        model="example-local-model",
        endpoint="http://127.0.0.1:11434",
        command="example-local-runtime",
        timeout_s=5.0,
        metadata={"purpose": "test-only placeholder"},
    )
    adapter = BlockedLocalRuntimeModelCallAdapter(config=config)

    assert adapter.config == config
    assert adapter.provider == LOCAL_RUNTIME_PLACEHOLDER_ADAPTER
    assert adapter.model == "local-runtime-not-configured"
    with pytest.raises(RuntimeError, match="No provider call was attempted"):
        adapter.call(ModelCallRequest(request_id="req-local-runtime-config", prompt="blocked"))


def test_select_model_call_adapter_defaults_to_local_validation() -> None:
    adapter = select_model_call_adapter()

    assert isinstance(adapter, DeterministicStubModelCallAdapter)


def test_select_model_call_adapter_returns_local_validation_adapter() -> None:
    adapter = select_model_call_adapter(LOCAL_VALIDATION_ADAPTER)

    assert isinstance(adapter, DeterministicStubModelCallAdapter)
    response = adapter.call(ModelCallRequest(request_id="req-10", prompt="local validation"))
    assert response.provider == "local_validation"
    assert response.model == "deterministic-local"


def test_select_model_call_adapter_returns_local_runtime_adapter() -> None:
    adapter = select_model_call_adapter(LOCAL_RUNTIME_ADAPTER)

    assert isinstance(adapter, DeterministicLocalRuntimeModelCallAdapter)
    response = adapter.call(ModelCallRequest(request_id="req-local-3", prompt="local runtime"))
    assert response.provider == LOCAL_RUNTIME_ADAPTER
    assert response.model == "deterministic-local-runtime"


def test_select_model_call_adapter_returns_blocked_adapter() -> None:
    adapter = select_model_call_adapter(BLOCKED_ADAPTER)

    assert isinstance(adapter, BlockedModelCallAdapter)
    with pytest.raises(RuntimeError, match="Real model-call adapter is not configured"):
        adapter.call(ModelCallRequest(request_id="req-11", prompt="blocked"))


def test_select_model_call_adapter_local_runtime_placeholder_fails_closed() -> None:
    adapter = select_model_call_adapter(LOCAL_RUNTIME_PLACEHOLDER_ADAPTER)

    assert isinstance(adapter, BlockedLocalRuntimeModelCallAdapter)
    with pytest.raises(RuntimeError, match="Local runtime adapters are not implemented yet"):
        adapter.call(ModelCallRequest(request_id="req-12", prompt="placeholder"))


def test_select_model_call_adapter_unknown_kind_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Unsupported model-call adapter kind"):
        select_model_call_adapter("remote_provider")


def test_available_model_call_adapters_lists_safe_kinds() -> None:
    adapters = available_model_call_adapters()

    assert LOCAL_VALIDATION_ADAPTER in adapters
    assert LOCAL_RUNTIME_ADAPTER in adapters
    assert BLOCKED_ADAPTER in adapters
    assert LOCAL_RUNTIME_PLACEHOLDER_ADAPTER in adapters


def test_select_model_call_adapter_requires_no_secrets_or_local_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_RUNTIME", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_ENDPOINT", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_NAME", raising=False)

    adapter = select_model_call_adapter(LOCAL_VALIDATION_ADAPTER)
    response = adapter.call(ModelCallRequest(request_id="req-13", prompt="no runtime"))

    assert response.model_calls == 1
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ
    assert "KORA_LOCAL_MODEL_RUNTIME" not in os.environ
    assert "KORA_LOCAL_MODEL_ENDPOINT" not in os.environ
    assert "KORA_LOCAL_MODEL_NAME" not in os.environ


def test_local_runtime_adapter_requires_no_secrets_or_local_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_RUNTIME", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_ENDPOINT", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_NAME", raising=False)

    adapter = select_model_call_adapter(LOCAL_RUNTIME_ADAPTER)
    response = adapter.call(ModelCallRequest(request_id="req-local-4", prompt="no runtime"))

    assert response.model_calls == 1
    assert response.metadata["runtime"] == "in_process_stub"
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ
    assert "KORA_LOCAL_MODEL_RUNTIME" not in os.environ
    assert "KORA_LOCAL_MODEL_ENDPOINT" not in os.environ
    assert "KORA_LOCAL_MODEL_NAME" not in os.environ


def test_local_runtime_placeholder_requires_no_secrets_or_local_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_RUNTIME", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_ENDPOINT", raising=False)
    monkeypatch.delenv("KORA_LOCAL_MODEL_NAME", raising=False)

    adapter = select_model_call_adapter(LOCAL_RUNTIME_PLACEHOLDER_ADAPTER)

    assert isinstance(adapter, BlockedLocalRuntimeModelCallAdapter)
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ
    assert "KORA_LOCAL_MODEL_RUNTIME" not in os.environ
    assert "KORA_LOCAL_MODEL_ENDPOINT" not in os.environ
    assert "KORA_LOCAL_MODEL_NAME" not in os.environ
