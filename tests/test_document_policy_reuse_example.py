from examples.document_policy_reuse.run import run

def test_document_policy_reuse_matches_oracle_and_manual_cache():
    report = run(rounds=1)
    assert report["cases_per_round"] == 55
    assert report["phases"] == 11
    arms = report["arms"]
    for arm in arms.values():
        assert arm["matches"] == 55
        assert arm["boundary_checks"] == 11
        assert arm["model_calls"] == 0
        assert arm["total_calls"] + arm["hits"] == 165
    assert arms["no_reuse"]["total_calls"] == 165
    assert arms["whole_request_cache"]["total_calls"] == 132
    assert arms["manual_node_cache"]["total_calls"] == 104
    assert arms["kora_node_cache"]["total_calls"] == 104
    assert arms["kora_node_cache"]["counter_checks"] == 55
