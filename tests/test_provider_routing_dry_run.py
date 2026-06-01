import json
from pathlib import Path

import pytest

from experiments.provider_routing.run_dry_run import (
    EXPECTED_PROVIDER_KINDS,
    ProviderRoutingConfigError,
    load_config,
    main,
    simulate_routing,
    validate_provider_config,
)


CONFIG_PATH = Path("experiments/provider_routing/config.example.yaml")


def test_provider_routing_config_validation_accepts_example() -> None:
    config = load_config(CONFIG_PATH)

    validation = validate_provider_config(config)

    assert validation["provider_count"] == 9
    assert set(validation["provider_kinds"]) == EXPECTED_PROVIDER_KINDS
    assert validation["synthetic_task_count"] == 9


def test_provider_routing_dry_run_routes_all_provider_kinds() -> None:
    summary = simulate_routing(load_config(CONFIG_PATH))

    assert summary["mode"] == "dry-run"
    assert summary["synthetic_results_only"] is True
    assert summary["real_network_calls_attempted"] is False
    assert summary["real_gpu_calls_attempted"] is False
    assert summary["summary"]["synthetic_tasks"] == 9
    assert summary["summary"]["blocked_real_execution_routes"] == 7
    assert {task["provider_kind"] for task in summary["routed_tasks"]} == EXPECTED_PROVIDER_KINDS
    assert all(task["real_call_attempted"] is False for task in summary["routed_tasks"])


def test_provider_routing_rejects_active_endpoint() -> None:
    config = load_config(CONFIG_PATH)
    config["providers"][0]["endpoint"] = "https://example.invalid/provider"

    with pytest.raises(ProviderRoutingConfigError, match="must not define an active endpoint"):
        validate_provider_config(config)


def test_provider_routing_example_contains_placeholders_only() -> None:
    text = CONFIG_PATH.read_text(encoding="utf-8")

    forbidden_fragments = [
        "sk-",
        "A" + "KIA",
        "BEGIN " + "PRIVATE KEY",
        "aws_secret" + "_access_key",
        "api_key",
        "https://" + "api.",
        "http://",
        ".".join(["121", "160", "51", "114"]),
    ]
    for fragment in forbidden_fragments:
        assert fragment not in text

    config = json.loads(text)
    assert all(provider["endpoint"] is None for provider in config["providers"])
    assert {provider["credential_ref"] for provider in config["providers"]} == {"PLACEHOLDER_ONLY"}


def test_provider_routing_cli_writes_dry_run_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output_path = tmp_path / "provider-routing-summary.json"

    exit_code = main(["--config", str(CONFIG_PATH), "--output", str(output_path)])

    captured = capsys.readouterr()
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    printed = json.loads(captured.out)
    assert exit_code == 0
    assert saved == printed
    assert saved["claim_boundary"].startswith("Synthetic dry-run routing only")
