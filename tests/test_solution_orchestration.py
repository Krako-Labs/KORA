from kora.solution import CapabilityTier, TaskContract, recommend_capability_tier


def test_objective_deterministic_work_routes_l0():
    result = recommend_capability_tier(TaskContract(objective_verification=True))
    assert result.tier is CapabilityTier.L0_DETERMINISTIC
    assert result.reason_code == "objective_deterministic"


def test_bounded_routine_routes_l1():
    result = recommend_capability_tier(TaskContract(repetitive_or_inspection=True))
    assert result.tier is CapabilityTier.L1_LOCAL_BOUNDED
    assert result.reason_code == "bounded_routine"


def test_verified_bounded_implementation_routes_l2():
    result = recommend_capability_tier(
        TaskContract(bounded_implementation=True, objective_verification=True)
    )
    assert result.tier is CapabilityTier.L2_LOCAL_STRONG
    assert result.reason_code == "bounded_implementation_verified"


def test_unverified_bounded_implementation_escalates_l3():
    result = recommend_capability_tier(TaskContract(bounded_implementation=True))
    assert result.tier is CapabilityTier.L3_FRONTIER
    assert result.reason_code == "bounded_implementation_unverified"


def test_complex_cross_component_routes_l3():
    result = recommend_capability_tier(TaskContract(complex_cross_component=True))
    assert result.tier is CapabilityTier.L3_FRONTIER
    assert result.reason_code == "complex_cross_component"


def test_architecture_routes_l4():
    result = recommend_capability_tier(TaskContract(architecture_or_ambiguous=True))
    assert result.tier is CapabilityTier.L4_HIGHEST_REASONING
    assert result.reason_code == "architecture_or_ambiguous"


def test_high_risk_prevents_unsafe_downrouting():
    result = recommend_capability_tier(
        TaskContract(
            high_risk=True,
            repetitive_or_inspection=True,
            bounded_implementation=True,
            objective_verification=True,
        )
    )
    assert result.tier is CapabilityTier.L4_HIGHEST_REASONING
    assert result.reason_code == "high_risk"


def test_same_contract_is_stable():
    contract = TaskContract(bounded_implementation=True, objective_verification=True)
    assert recommend_capability_tier(contract) == recommend_capability_tier(contract)


def test_unknown_unverified_work_fails_upward():
    result = recommend_capability_tier(TaskContract())
    assert result.tier is CapabilityTier.L3_FRONTIER
    assert result.reason_code == "unverified_default"
