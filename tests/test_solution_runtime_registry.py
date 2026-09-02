from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from kora.solution import (
    RESULT_ENVELOPE_SCHEMA,
    RUNTIME_STATUS_SCHEMA,
    CapabilityRegistryError,
    LocalCapabilityRegistry,
    LocalSolutionHost,
    ReferenceRuntime,
    SolutionHostError,
    validate_contract_instance,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
HELLO_SOLUTION = REPO_ROOT / "examples" / "solutions" / "hello-solution"
DOCUMENT_SOLUTION = REPO_ROOT / "examples" / "solutions" / "document-transform-fixture"


def _resolve(registry: LocalCapabilityRegistry, capabilities: set[str]):
    return registry.resolve(
        capabilities,
        protocol_version="kora.dev/v0alpha1",
        task_kinds={"det"},
    )


def test_registration_list_and_priority_resolution_are_deterministic(
    tmp_path: Path,
) -> None:
    class LowerPriorityRuntime(ReferenceRuntime):
        runtime_id = "fixture.lower"
        priority = 10

    class HigherPriorityRuntime(ReferenceRuntime):
        runtime_id = "fixture.higher"
        priority = 20

    registry = LocalCapabilityRegistry(tmp_path / "runtimes")
    lower = registry.register(LowerPriorityRuntime())
    higher = registry.register(HigherPriorityRuntime())
    listing = registry.list()
    selected = _resolve(registry, {"det.echo"})

    assert (
        lower["activity"]
        == higher["activity"]
        == {
            "execution_performed": False,
            "network_accessed": False,
            "model_inference_performed": False,
            "gpu_execution_performed": False,
        }
    )
    assert [entry["descriptor"]["runtime"]["id"] for entry in listing["runtimes"]] == [
        "fixture.higher",
        "fixture.lower",
    ]
    assert selected.identity["id"] == "fixture.higher"
    assert len(selected.identity["descriptor_digest"]) == 64


def test_persisted_descriptor_without_trusted_binding_cannot_execute(
    tmp_path: Path,
) -> None:
    root = tmp_path / "runtimes"
    LocalCapabilityRegistry(root).register(ReferenceRuntime())
    reopened = LocalCapabilityRegistry(root)

    listing = reopened.list()
    assert listing["runtimes"][0]["bound"] is False

    with pytest.raises(CapabilityRegistryError) as captured:
        _resolve(reopened, {"det.echo"})

    assert captured.value.code == "runtime_unavailable"


def test_equal_highest_priority_is_rejected_as_ambiguous(tmp_path: Path) -> None:
    class FirstRuntime(ReferenceRuntime):
        runtime_id = "fixture.first"

    class SecondRuntime(ReferenceRuntime):
        runtime_id = "fixture.second"

    registry = LocalCapabilityRegistry(tmp_path / "runtimes")
    registry.register(FirstRuntime())
    registry.register(SecondRuntime())

    with pytest.raises(CapabilityRegistryError) as captured:
        _resolve(registry, {"det.echo"})

    assert captured.value.code == "ambiguous_runtime"


def test_capabilities_are_not_split_across_multiple_runtimes(tmp_path: Path) -> None:
    class EchoRuntime(ReferenceRuntime):
        runtime_id = "fixture.echo"

        @property
        def capabilities(self) -> frozenset[str]:
            return frozenset({"det.echo"})

    class NormalizeRuntime(ReferenceRuntime):
        runtime_id = "fixture.normalize"

        @property
        def capabilities(self) -> frozenset[str]:
            return frozenset({"text.normalize"})

    registry = LocalCapabilityRegistry(tmp_path / "runtimes")
    registry.register(EchoRuntime())
    registry.register(NormalizeRuntime())

    with pytest.raises(CapabilityRegistryError) as captured:
        _resolve(registry, {"det.echo", "text.normalize"})

    assert captured.value.code == "missing_capability_runtime"


def test_runtime_execution_policy_is_enforced_before_selection(tmp_path: Path) -> None:
    class NetworkRuntime(ReferenceRuntime):
        runtime_id = "fixture.network"

        @property
        def descriptor(self) -> dict[str, Any]:
            descriptor = super().descriptor
            descriptor["execution"]["network_access"] = True
            return descriptor

    registry = LocalCapabilityRegistry(tmp_path / "runtimes")
    registry.register(NetworkRuntime())

    with pytest.raises(CapabilityRegistryError) as captured:
        _resolve(registry, {"det.echo"})

    assert captured.value.code == "incompatible_runtime"


def test_descriptor_binding_mismatch_and_registry_tampering_fail_closed(
    tmp_path: Path,
) -> None:
    class MismatchedRuntime(ReferenceRuntime):
        runtime_id = "fixture.mismatch"

        @property
        def descriptor(self) -> dict[str, Any]:
            descriptor = super().descriptor
            descriptor["capabilities"] = ["det.echo"]
            return descriptor

    registry = LocalCapabilityRegistry(tmp_path / "mismatch")
    with pytest.raises(CapabilityRegistryError) as mismatch:
        registry.register(MismatchedRuntime())
    assert mismatch.value.code == "invalid_runtime_binding"

    verified = LocalCapabilityRegistry(tmp_path / "verified")
    verified.register(ReferenceRuntime())
    descriptor_path = (
        tmp_path / "verified" / "kora.reference" / "0.1.0" / "runtime.json"
    )
    payload = json.loads(descriptor_path.read_text(encoding="utf-8"))
    payload["priority"] = 999
    descriptor_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(CapabilityRegistryError) as tampered:
        verified.list()
    assert tampered.value.code == "runtime_integrity_mismatch"


def test_host_records_selected_runtime_for_both_reference_solutions(
    tmp_path: Path,
) -> None:
    host = LocalSolutionHost(tmp_path / "host")
    hello_receipt = host.install(HELLO_SOLUTION)
    document_receipt = host.install(DOCUMENT_SOLUTION)
    hello = host.run("example.hello", {"message": "Hello"})
    document = host.run("example.document-transform", {"text": "  A   B  "})

    expected = hello_receipt["runtime_resolution"]
    assert document_receipt["runtime_resolution"] == expected
    assert hello["runtime"] == document["runtime"] == expected
    assert host.status(hello["run_id"])["runtime"] == expected
    validate_contract_instance(RUNTIME_STATUS_SCHEMA, host.status(document["run_id"]))
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, document)
    assert hello["activity"]["network_accessed"] is False
    assert hello["activity"]["model_inference_performed"] is False
    assert hello["activity"]["gpu_execution_performed"] is False


def test_registry_tampering_after_install_creates_valid_failed_result(
    tmp_path: Path,
) -> None:
    host = LocalSolutionHost(tmp_path / "host")
    host.install(HELLO_SOLUTION)
    descriptor_path = host.runtimes_root / "kora.reference" / "0.1.0" / "runtime.json"
    descriptor_path.write_bytes(descriptor_path.read_bytes() + b"\n")

    result = host.run("example.hello", {"message": "Hello"})

    assert result["lifecycle_state"] == "failed"
    assert result["runtime"] is None
    assert result["error"]["code"] == "runtime_integrity_mismatch"
    assert result["activity"]["execution_performed"] is False
    validate_contract_instance(RESULT_ENVELOPE_SCHEMA, result)


def test_host_rejects_ambiguous_runtime_before_install(tmp_path: Path) -> None:
    class AlternateRuntime(ReferenceRuntime):
        runtime_id = "fixture.alternate"

    host = LocalSolutionHost(
        tmp_path / "host",
        runtimes=(ReferenceRuntime(), AlternateRuntime()),
    )

    with pytest.raises(SolutionHostError) as captured:
        host.install(HELLO_SOLUTION)

    assert captured.value.code == "ambiguous_runtime"
