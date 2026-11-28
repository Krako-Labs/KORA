from examples.document_policy_reuse.maintenance import run


def test_versioned_policy_maintenance_replay_and_negative_control():
    report = run(rounds=1)
    assert report["model_calls"] == 0
    arms = report["arms"]
    for name, stages in arms.items():
        for stage, result in stages.items():
            assert result["requests"] == 6
            faults = int(name != "direct" and stage == "missing_version_bump")
            assert result["matches"] == 6 - faults
            assert result["expected_faults"] == faults
            assert result["dispatches"] + result["hits"] == 18
        if name != "direct":
            for stage in ("baseline_repeat", "missing_version_bump", "revised_repeat", "rollback_repeat"):
                assert stages[stage]["dispatches"] == 0
            for stage in ("baseline", "version_bump", "rollback"):
                assert stages[stage]["dispatches"] > 0
    for stage in arms["manual"]:
        assert arms["manual"][stage]["dispatches"] == arms["kora"][stage]["dispatches"]
