from __future__ import annotations

import json

from kora.foundation.device_inventory import (
    DeviceInventory,
    collect_device_inventory,
    detect_runtime_candidates,
    render_device_inventory_text,
)


def _fake_executor(mapping: dict[tuple[str, ...], str]):
    return lambda command: mapping.get(command)


def test_collect_device_inventory_parses_mac_metadata_without_sensitive_identifiers() -> None:
    displays = {
        "SPDisplaysDataType": [
            {
                "_name": "Apple M2 Max",
                "sppci_model": "Apple M2 Max",
                "sppci_cores": "30",
                "spdisplays_ndrvs": [
                    {"_spdisplays_display-serial-number": "SHOULD-NOT-ESCAPE"}
                ],
            }
        ]
    }
    thunderbolt = {
        "SPThunderboltDataType": [
            {
                "domain_uuid_key": "SHOULD-NOT-ESCAPE",
                "receptacle_1_tag": {"current_speed_key": "Up to 40 Gb/s"},
            }
        ]
    }
    network = """
Hardware Port: Ethernet
Device: en0
Ethernet Address: [redacted-test-mac-a]

Hardware Port: Thunderbolt Bridge
Device: bridge0
Ethernet Address: [redacted-test-mac-b]

Hardware Port: Wi-Fi
Device: en1
Ethernet Address: [redacted-test-mac-c]
"""
    mapping = {
        ("sysctl", "-n", "machdep.cpu.brand_string"): "Apple M2 Max",
        ("sysctl", "-n", "hw.memsize"): str(32 * 1024**3),
        ("sysctl", "-n", "hw.physicalcpu"): "12",
        ("sysctl", "-n", "hw.logicalcpu"): "12",
        ("system_profiler", "SPDisplaysDataType", "-json"): json.dumps(displays),
        ("system_profiler", "SPThunderboltDataType", "-json"): json.dumps(thunderbolt),
        ("networksetup", "-listallhardwareports"): network,
    }

    inventory = collect_device_inventory(
        executor=_fake_executor(mapping),
        which=lambda command: "/opt/homebrew/bin/ollama" if command == "ollama" else None,
        node_name="MSM2-test",
        os_name="Darwin",
        os_version="26.0",
        architecture="arm64",
    )
    data = inventory.to_dict()

    assert data["schema_version"] == "kora_foundation_device_inventory_v0"
    assert data["node_name"] == "MSM2-test"
    assert data["chip_model"] == "Apple M2 Max"
    assert data["total_memory_gb"] == 32.0
    assert data["physical_cpu_cores"] == 12
    assert data["logical_cpu_cores"] == 12
    assert data["gpu_models"] == ("Apple M2 Max",)
    assert data["gpu_core_counts"] == (30,)
    assert {item["category"] for item in data["network_interfaces"]} == {
        "ethernet",
        "thunderbolt_bridge",
        "wifi",
    }
    tb = next(item for item in data["transports"] if item["name"] == "thunderbolt_bridge")
    assert tb["detected"] is True
    assert tb["max_link_speed_gbps"] == 40.0
    ollama = next(item for item in data["runtime_candidates"] if item["name"] == "ollama")
    assert ollama["detected"] is True
    assert data["sensitive_identifiers_collected"] is False

    serialized = json.dumps(data).lower()
    assert "redacted-test-mac-a" not in serialized
    assert "redacted-test-mac-b" not in serialized
    assert "should-not-escape" not in serialized


def test_runtime_detection_does_not_start_runtimes() -> None:
    calls: list[str] = []

    def fake_which(command: str) -> str | None:
        calls.append(command)
        return f"/mock/{command}" if command in {"mlx_lm.server", "llama-cli", "vllm"} else None

    candidates = detect_runtime_candidates(fake_which)

    assert next(item for item in candidates if item.name == "mlx-lm").command == "mlx_lm.server"
    assert next(item for item in candidates if item.name == "llama.cpp").command == "llama-cli"
    assert next(item for item in candidates if item.name == "vllm").detected is True
    assert "ollama" in calls


def test_non_darwin_inventory_fails_closed_without_platform_specific_metadata() -> None:
    inventory = collect_device_inventory(
        executor=lambda command: None,
        which=lambda command: None,
        node_name="linux-test",
        os_name="Linux",
        os_version="6.x",
        architecture="x86_64",
    )
    data = inventory.to_dict()

    assert data["os_name"] == "Linux"
    assert data["network_interfaces"] == ()
    assert data["gpu_models"] == ()
    assert data["sensitive_identifiers_collected"] is False
    assert "does not prove runtime compatibility" in data["claim_boundary"]


def test_generic_mac_processor_uses_detected_apple_gpu_chip_label() -> None:
    displays = {"SPDisplaysDataType": [{"sppci_model": "Apple M2 Max", "sppci_cores": "30"}]}
    inventory = collect_device_inventory(
        executor=_fake_executor(
            {("system_profiler", "SPDisplaysDataType", "-json"): json.dumps(displays)}
        ),
        which=lambda command: None,
        node_name="test-node",
        os_name="Darwin",
        os_version="26.0",
        architecture="arm64",
    )
    assert inventory.chip_model == "Apple M2 Max"
    assert inventory.inventory_status == "detected_with_unknowns"


def test_render_device_inventory_text_is_concise_and_claim_safe() -> None:
    inventory = collect_device_inventory(
        executor=lambda command: None,
        which=lambda command: None,
        node_name="test-node",
        os_name="Darwin",
        os_version="26.0",
        architecture="arm64",
    )
    text = render_device_inventory_text(inventory)

    assert "KORA Foundation Device Inventory" in text
    assert "Node: test-node" in text
    assert "Runtime candidates:" in text
    assert "sensitive identifiers collected=False" in text
    assert "performance must be benchmarked" not in text.lower() or "Boundary:" in text
    assert "cost savings" in text


def test_inventory_round_trip_rejects_malformed_or_sensitive_payload() -> None:
    inventory = collect_device_inventory(
        executor=lambda command: None,
        which=lambda command: "/Users/private/bin/ollama" if command == "ollama" else None,
        node_name="safe-label",
        os_name="Darwin",
        os_version="26.0",
        architecture="arm64",
    )
    data = inventory.to_dict()
    assert DeviceInventory.from_dict(data) == inventory
    assert "/Users/private" not in json.dumps(data)

    data["sensitive_identifiers_collected"] = True
    try:
        DeviceInventory.from_dict(data)
    except ValueError as exc:
        assert "sensitive identifiers" in str(exc)
    else:
        raise AssertionError("sensitive inventory payload was accepted")
