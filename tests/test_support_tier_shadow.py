from dataclasses import replace

import pytest

from kora.support_tier_shadow import (
    OriginRead, ReadBasis, RouteVersions, Subject, SupportTierShadow, TierReply,
)


SUBJECT = Subject(tenant="Cedar", account="acct-1", principal="operator-1")
VERSIONS = RouteVersions(policy="policy-1", resolver="resolver-1", prompt="prompt-1")
BASIS = ReadBasis(
    subject=SUBJECT, source="support-directory", fact="support_tier",
    revision="v1", grant_revision="g1", can_read=True, valid_until="2026-09-06",
)
REPLY = TierReply(status="ok", tier="gold")
TODAY = "2026-09-05"


def test_revoked_access_never_reuses_allowed_candidate_and_always_serves_origin():
    shadow = SupportTierShadow("support-directory")
    reads = []
    current = OriginRead(REPLY, BASIS)

    def lookup(subject):
        reads.append(subject)
        return current

    def observe():
        return shadow.observe(SUBJECT, TODAY, lookup, versions=VERSIONS)

    assert observe().decision == "record"
    hit = observe()
    assert hit.decision == "would_reuse"
    assert hit.original is REPLY
    denied = TierReply("denied")
    current = OriginRead(denied, replace(BASIS, can_read=False, revision="v2", grant_revision="g2"))
    revoked = observe()
    assert revoked.original is denied
    assert (revoked.decision, revoked.reason, revoked.cached_tier) == ("defer", "read_not_granted", None)
    current = OriginRead(REPLY, BASIS)
    assert observe().decision == "record"
    assert reads == [SUBJECT] * 4


@pytest.mark.parametrize(("change", "reason"), [
    ({"subject": replace(SUBJECT, tenant="Juniper")}, "scope_mismatch"),
    ({"subject": replace(SUBJECT, account="acct-2")}, "scope_mismatch"),
    ({"subject": replace(SUBJECT, principal="operator-2")}, "scope_mismatch"),
    ({"source": "untrusted"}, "scope_mismatch"),
    ({"fact": "billing_address"}, "scope_mismatch"),
    ({"revision": ""}, "unknown_version"),
    ({"grant_revision": None}, "unknown_version"),
    ({"can_read": 1}, "read_not_granted"),
    ({"valid_until": "2026-09-04"}, "invalid_or_expired"),
    ({"valid_until": "2026-09-31"}, "invalid_or_expired"),
])
def test_failed_binding_clears_warm_candidate(change, reason):
    shadow = SupportTierShadow("support-directory")

    def observe(basis):
        return shadow.observe(SUBJECT, TODAY, lambda _: OriginRead(REPLY, basis), versions=VERSIONS)

    observe(BASIS)
    result = observe(replace(BASIS, **change))
    assert (result.decision, result.reason, result.cached_tier) == ("defer", reason, None)
    assert result.original is REPLY
    assert observe(BASIS).decision == "record"


def test_revisions_are_per_subject_and_rollback_requires_new_observation():
    shadow = SupportTierShadow("support-directory")

    def observe(subject=SUBJECT, versions=VERSIONS, **changes):
        basis = replace(BASIS, subject=subject, **changes)
        return shadow.observe(subject, TODAY, lambda _: OriginRead(REPLY, basis), versions=versions)

    other = replace(SUBJECT, tenant="Juniper")
    assert observe().decision == observe(other).decision == "record"
    assert observe(revision="v2").decision == "record"
    assert observe(other).decision == "would_reuse"
    assert observe().decision == "record"
    assert observe(grant_revision="g2").decision == "record"
    changed = replace(VERSIONS, resolver="resolver-2")
    assert observe(versions=changed, grant_revision="g2").decision == "record"
    assert observe(versions=changed, grant_revision="g2").decision == "would_reuse"
    assert observe(versions=replace(changed, prompt="new"), grant_revision="g2").decision == "record"
    assert observe(versions=replace(changed, policy="policy-2")).decision == "record"


def test_missing_evidence_origin_failure_or_drift_never_serves_a_shadow_reply():
    shadow = SupportTierShadow("support-directory")

    def observe(read, as_of=TODAY, versions=VERSIONS):
        return shadow.observe(SUBJECT, as_of, lambda _: read, versions=versions)

    assert observe(OriginRead(REPLY, None)).reason == "missing_basis"
    assert observe(OriginRead(REPLY, BASIS), versions=replace(VERSIONS, policy=" ")).reason == "unknown_version"
    assert observe(OriginRead(REPLY, BASIS), "2026-09-06").decision == "record"
    assert observe(OriginRead(REPLY, BASIS), "2026-09-07").decision == "defer"
    assert observe(OriginRead(REPLY, BASIS), "09/05/2026").decision == "defer"
    assert observe(OriginRead(REPLY, BASIS)).decision == "record"
    different = TierReply("ok", "platinum")
    drift = observe(OriginRead(different, BASIS))
    assert drift.original is different
    assert (drift.decision, drift.reason, drift.cached_tier) == ("defer", "origin_disagrees", None)
    unavailable = TierReply("unavailable")
    assert observe(OriginRead(unavailable, BASIS)).original is unavailable
    assert observe(OriginRead(unavailable, BASIS)).reason == "origin_unavailable"
    assert observe(OriginRead(REPLY, BASIS)).decision == "record"


def test_older_read_cannot_rewarm_candidate_after_overlapping_revocation():
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    shadow = SupportTierShadow("support-directory")
    sampled, resume = Event(), Event()

    def observe(origin):
        return shadow.observe(SUBJECT, TODAY, origin, versions=VERSIONS)

    def old_lookup(_):
        value = OriginRead(REPLY, BASIS)
        sampled.set()
        assert resume.wait(5)
        return value

    with ThreadPoolExecutor() as pool:
        old = pool.submit(observe, old_lookup)
        try:
            assert sampled.wait(5)
            denied = TierReply("denied")
            revoked = observe(lambda _: OriginRead(denied, replace(BASIS, can_read=False)))
            assert revoked.original is denied
            assert revoked.reason == "read_not_granted"
        finally:
            resume.set()
        superseded = old.result(timeout=5)
        assert superseded.original is REPLY
        assert superseded.reason == "superseded_read"
    assert observe(lambda _: OriginRead(REPLY, BASIS)).decision == "record"


def test_origin_exception_keeps_its_identity_and_discards_warm_candidate():
    shadow = SupportTierShadow("support-directory")

    def observe(origin):
        return shadow.observe(SUBJECT, TODAY, origin, versions=VERSIONS)

    error = RuntimeError("source unavailable")

    def unavailable(_):
        raise error

    assert observe(lambda _: OriginRead(REPLY, BASIS)).decision == "record"
    with pytest.raises(RuntimeError) as raised:
        observe(unavailable)
    assert raised.value is error
    assert observe(lambda _: OriginRead(REPLY, BASIS)).decision == "record"


def test_offline_example_keeps_dated_controls_and_never_skips_original_lookup():
    import json
    from pathlib import Path
    from examples.support_tier_shadow.run import replay

    fixture = Path(__file__).resolve().parents[1] / "experiments/blind_routing/requests.json"
    requests = {row["id"]: row for row in json.loads(fixture.read_text())}
    run = replay()
    cases = {row["case"]: row for row in run["results"]}
    assert run["origin_calls"] == len(cases) == 7
    assert run["fact_reads"] == 6
    assert run["actual_origin_calls_skipped"] == run["provider_calls"] == 0
    assert run["would_reuse"] == 1
    for label, case in (("r329_valid", "r329"), ("r591_expired", "r591")):
        assert cases[label]["as_of"] == requests[case]["context"]["as_of"]
        assert cases[label]["source_basis"]["valid_until"] == requests[case]["context"]["valid_until"]
    assert cases["revoked_before_expiry"]["original"]["status"] == "denied"
    assert cases["revoked_before_expiry"]["cached_tier"] is None
    assert cases["rollback"]["decision"] == "record"
