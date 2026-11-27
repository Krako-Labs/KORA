"""Run a synthetic support directory alongside a read-only KORA observation stream."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from kora.executor import routing_freshness_failure
from kora.support_tier_shadow import (
    OriginRead, ReadBasis, RouteVersions, Subject, SupportTierShadow, TierReply,
)


@dataclass(frozen=True)
class TierRecord:
    revision: str
    valid_until: str
    tier: str


class FixtureDirectory:
    """Local stand-in for a host-owned source that checks grants and reads its fact."""

    def __init__(self) -> None:
        self.grants: dict[Subject, tuple[str, bool]] = {}
        self.records: dict[tuple[str, str], TierRecord] = {}
        self.origin_calls = 0
        self.fact_reads = 0

    def lookup(self, subject: Subject, as_of: str) -> OriginRead:
        self.origin_calls += 1
        grant_revision, granted = self.grants.get(subject, ("", False))
        if not granted:
            basis = ReadBasis(subject, "fixture-directory", "support_tier", "", grant_revision, False, "")
            return OriginRead(TierReply("denied"), basis)

        self.fact_reads += 1
        record = self.records.get((subject.tenant, subject.account))
        if record is None:
            return OriginRead(TierReply("not_found"), None)

        basis = ReadBasis(
            subject, "fixture-directory", "support_tier", record.revision,
            grant_revision, True, record.valid_until,
        )
        if routing_freshness_failure({"as_of": as_of, "valid_until": record.valid_until}):
            return OriginRead(TierReply("refresh_required"), basis)
        return OriginRead(TierReply("ok", record.tier), basis)


def replay() -> dict:
    subject = Subject("Cedar", "account-1", "operator-1")
    versions = RouteVersions("policy-1", "resolver-1", "no-prompt-v1")
    directory = FixtureDirectory()
    shadow = SupportTierShadow("fixture-directory")
    rows = []
    as_of = "2026-09-05"
    account = (subject.tenant, subject.account)
    directory.grants[subject] = ("g1", True)
    original = TierRecord("v1", "2026-09-06", "gold")
    directory.records[account] = original

    def record(label):
        def origin(request_subject):
            read = directory.lookup(request_subject, as_of)
            receipt["source_basis"] = asdict(read.basis) if read.basis else None
            return read

        receipt = {"case": label, "as_of": as_of, "versions": asdict(versions)}
        observed = shadow.observe(subject, as_of, origin, versions=versions)
        rows.append({**receipt, **asdict(observed)})

    record("r329_valid")
    record("warm_repeat")
    directory.grants[subject] = ("g2", False)
    record("revoked_before_expiry")
    directory.grants[subject] = ("g3", True)
    record("regranted")
    directory.records[account] = TierRecord("v2", "2026-09-06", "platinum")
    record("source_change")
    directory.records[account] = original
    record("rollback")
    directory.records[account] = TierRecord("v3", "2026-09-04", "gold")
    record("r591_expired")
    return {
        "mode": "synthetic_shadow", "origin_calls": directory.origin_calls,
        "fact_reads": directory.fact_reads, "would_reuse": sum(
            row["decision"] == "would_reuse" for row in rows
        ),
        "actual_origin_calls_skipped": 0, "provider_calls": 0, "results": rows,
    }


if __name__ == "__main__":
    print(json.dumps(replay(), indent=2, sort_keys=True))
