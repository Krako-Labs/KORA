from pathlib import Path


PACKET_PATH = Path("docs/benchmarks/local-validation-reviewer-packet.md")


def test_local_validation_reviewer_packet_exists_and_has_report_commands() -> None:
    content = PACKET_PATH.read_text(encoding="utf-8")

    assert "# Local No-Network Validation Reviewer Packet" in content
    assert "python3 -m kora run model_call_counter_fixture -- --offline --report-md" in content
    assert (
        "python3 -m kora run customer_support_triage_synthetic -- --offline --report-md"
        in content
    )


def test_local_validation_reviewer_packet_documents_expected_counters() -> None:
    content = PACKET_PATH.read_text(encoding="utf-8")

    assert "| `total_requests` | 10 |" in content
    assert "| `baseline_model_calls` | 10 |" in content
    assert "| `kora_model_calls` | 4 |" in content
    assert "| `avoided_model_calls` | 6 |" in content
    assert "| `total_requests` | 12 |" in content
    assert "| `baseline_model_calls` | 12 |" in content
    assert "| `avoided_model_calls` | 8 |" in content
    assert "`provider`: `local_validation`" in content
    assert "`model`: `deterministic-local`" in content


def test_local_validation_reviewer_packet_preserves_claim_boundaries() -> None:
    content = PACKET_PATH.read_text(encoding="utf-8")

    assert "not real provider validation" in content
    assert "not real API-cost reduction evidence" in content
    assert "not production validation" in content
    assert "not production cost-reduction proof" in content
    assert "not energy-reduction evidence" in content
    assert "KORA has real provider validation from this packet." in content
