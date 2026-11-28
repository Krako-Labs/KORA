"""Synthetic read-only activation benchmark; no model or network calls."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from threading import RLock
from time import perf_counter_ns
import statistics

from kora.executor import routing_freshness_failure
from kora.support_tier_shadow import Subject, RouteVersions, ReadBasis, TierReply, OriginRead, SupportTierShadow

SOURCE = "fixture-directory"
VERSION = RouteVersions("p1", "r1", "prompt1")
DAY = "2026-09-05"
EXPIRY = "2026-09-06"
A = Subject("Cedar", "account-1", "operator-1")
B = Subject("Cedar", "account-1", "operator-2")
C = Subject("Other", "account-1", "operator-1")

@dataclass(frozen=True)
class Metadata:
    basis: ReadBasis
    fact_epoch: int
    grant_epoch: int

class Directory:
    """Authoritative metadata and data share one serialization boundary.
    Every write changes the epoch, including rollback or same-label writes.
    Metadata does not read or return the tier. All calls are counted.
    """
    def __init__(self):
        self.lock = RLock()
        self.epoch = 0
        self.grants = {}
        self.meta = {}
        self.tiers = {}
        self.counts = Counter()

    def set_grant(self, subject, revision, granted):
        with self.lock:
            self.epoch += 1
            self.grants[subject] = (revision, granted, self.epoch)

    def set_record(self, subject, revision, expiry, tier):
        with self.lock:
            self.epoch += 1
            key = (subject.tenant, subject.account)
            self.meta[key] = (revision, expiry, self.epoch)
            self.tiers[key] = tier

    def _metadata(self, subject):
        grant, granted, ge = self.grants.get(subject, ("", False, 0))
        rev, expiry, fe = self.meta.get((subject.tenant, subject.account), ("", "", 0))
        return Metadata(ReadBasis(subject, SOURCE, "support_tier", rev, grant, granted, expiry), fe, ge)

    def probe(self, subject):
        with self.lock:
            self.counts["metadata_probes"] += 1
            return self._metadata(subject)

    def lookup(self, subject, day):
        with self.lock:
            self.counts["origin_calls"] += 1
            meta = self._metadata(subject)
            basis = meta.basis
            if basis.can_read is not True:
                return OriginRead(TierReply("denied"), basis)
            self.counts["record_checks"] += 1
            if not meta.fact_epoch:
                return OriginRead(TierReply("not_found"), None)
            if routing_freshness_failure({"as_of": day, "valid_until": basis.valid_until}):
                return OriginRead(TierReply("refresh_required"), basis)
            self.counts["fact_reads"] += 1
            return OriginRead(TierReply("ok", self.tiers[(subject.tenant, subject.account)]), basis)

def known(value):
    return isinstance(value, str) and bool(value.strip())

def reusable(meta, subject, day, versions):
    if not isinstance(meta, Metadata) or not isinstance(meta.basis, ReadBasis) or not isinstance(versions, RouteVersions):
        return False
    b = meta.basis
    return (b.subject == subject and b.source == SOURCE and b.fact == "support_tier"
            and b.can_read is True and meta.fact_epoch > 0 and meta.grant_epoch > 0
            and all(known(v) for v in (subject.tenant, subject.account, subject.principal,
                b.revision, b.grant_revision, versions.policy, versions.resolver, versions.prompt))
            and not routing_freshness_failure({"as_of": day, "valid_until": b.valid_until}))

class Activation:
    """Prototype only. Not the production KORA execution path.
    The adapter owns the lock: no gap between metadata validation and return.
    """
    def __init__(self, directory):
        self.directory = directory
        self.cache = {}

    def run(self, subject, day, versions):
        d = self.directory
        with d.lock:
            try:
                meta = d.probe(subject)
            except Exception:
                self.cache.pop(subject, None)
                return d.lookup(subject, day).reply
            eligible = reusable(meta, subject, day, versions)
            entry = self.cache.get(subject)
            if eligible and entry is not None and entry[:2] == (meta, versions):
                d.counts["skipped_origin"] += 1
                return entry[2]
            self.cache.pop(subject, None)
            result = d.lookup(subject, day)
            if (eligible and result.basis == meta.basis and result.reply.status == "ok"
                    and known(result.reply.tier)):
                self.cache[subject] = (meta, versions, result.reply)
            return result.reply

class ConventionalCache:
    """Equal-metadata control: a plain dictionary keyed by authoritative epoch."""
    def __init__(self, directory):
        self.directory = directory
        self.last = {}

    def run(self, subject, day, versions):
        d = self.directory
        with d.lock:
            try:
                meta = d.probe(subject)
            except Exception:
                self.last.pop(subject, None)
                return d.lookup(subject, day).reply
            valid = reusable(meta, subject, day, versions)
            key = (meta, versions)
            previous = self.last.get(subject)
            if valid and previous and previous[0] == key:
                d.counts["skipped_origin"] += 1
                return previous[1]
            self.last.pop(subject, None)
            result = d.lookup(subject, day)
            if valid and result.basis == meta.basis and result.reply.status == "ok" and known(result.reply.tier):
                self.last[subject] = (key, result.reply)
            return result.reply

def steps():
    # (label, mutation, subject, date, versions, authored expected reply)
    ok = lambda tier: TierReply("ok", tier)
    none = lambda d: None
    v2 = RouteVersions("p2", "r1", "prompt1")
    yield ("cold", lambda d: (d.set_grant(A,"g1",True), d.set_record(A,"v1",EXPIRY,"gold")), A, DAY, VERSION, ok("gold"))
    yield ("repeat", none, A, DAY, VERSION, ok("gold"))
    yield ("revoke", lambda d: d.set_grant(A,"g2",False), A, DAY, VERSION, TierReply("denied"))
    yield ("regrant", lambda d: d.set_grant(A,"g3",True), A, DAY, VERSION, ok("gold"))
    yield ("change", lambda d: d.set_record(A,"v2",EXPIRY,"platinum"), A, DAY, VERSION, ok("platinum"))
    yield ("rollback", lambda d: d.set_record(A,"v1",EXPIRY,"gold"), A, DAY, VERSION, ok("gold"))
    yield ("expired", lambda d: d.set_record(A,"v3","2026-09-04","gold"), A, DAY, VERSION, TierReply("refresh_required"))
    yield ("restore", lambda d: d.set_record(A,"v1",EXPIRY,"gold"), A, DAY, VERSION, ok("gold"))
    for i in range(10):
        yield (f"stable_{i}", none, A, DAY, VERSION, ok("gold"))
    yield ("other_principal", none, B, DAY, VERSION, TierReply("denied"))
    yield ("other_tenant", none, C, DAY, VERSION, TierReply("denied"))
    yield ("policy_change", none, A, DAY, v2, ok("gold"))
    yield ("policy_repeat", none, A, DAY, v2, ok("gold"))
    yield ("unknown_policy", none, A, DAY, RouteVersions("", "r1","prompt1"), ok("gold"))
    yield ("unknown_policy_repeat", none, A, DAY, RouteVersions("", "r1","prompt1"), ok("gold"))
    yield ("same_label_rewrite", lambda d: d.set_record(A,"v1",EXPIRY,"silver"), A, DAY, VERSION, ok("silver"))
    yield ("same_label_repeat", none, A, DAY, VERSION, ok("silver"))
    yield ("unrelated_update", lambda d: d.set_record(C,"v1",EXPIRY,"bronze"), A, DAY, VERSION, ok("silver"))
    yield ("inclusive_expiry", none, A, EXPIRY, VERSION, ok("silver"))
    yield ("date_expired", none, A, "2026-09-07", VERSION, TierReply("refresh_required"))
    yield ("invalid_date", none, A, "not-a-date", VERSION, TierReply("refresh_required"))
    yield ("new_valid_date", none, A, DAY, VERSION, ok("silver"))
    yield ("repeat_final", none, A, DAY, VERSION, ok("silver"))

ARMS = ("direct_fixture", "manual_equal_tool", "kora_shadow", "activation_prototype", "equal_metadata_cache")

def runner(arm, d):
    if arm == "direct_fixture":
        return lambda s, day, v: d.lookup(s, day).reply
    if arm == "manual_equal_tool":
        table = {"support_tier": d.lookup}
        return lambda s, day, v: table["support_tier"](s, day).reply
    if arm == "kora_shadow":
        shadow = SupportTierShadow(SOURCE)
        return lambda s, day, v: shadow.observe(s, day, lambda x: d.lookup(x, day), versions=v).original
    if arm == "activation_prototype":
        return Activation(d).run
    if arm == "equal_metadata_cache":
        return ConventionalCache(d).run
    raise ValueError(arm)

def run(iterations):
    if iterations < 1:
        raise ValueError("iterations must be positive")
    result = {}
    # Rotate order across iterations to reduce fixed-order timing bias.
    times = {arm: [] for arm in ARMS}
    totals = {arm: Counter() for arm in ARMS}
    first = {}
    errors = []
    for i in range(iterations):
        for arm in ARMS[i % len(ARMS):] + ARMS[:i % len(ARMS)]:
            d = Directory()
            execute = runner(arm,d)
            for label, mutation, s, day, versions, expected in steps():
                mutation(d)
                before = d.counts.copy()
                t = perf_counter_ns()
                actual = execute(s, day, versions)
                times[arm].append(perf_counter_ns() - t)
                if actual != expected:
                    errors.append({"arm":arm,"iteration":i,"case":label,"actual":asdict(actual),"expected":asdict(expected)})
                if i == 0:
                    first.setdefault(arm, []).append({"case":label,"reply":asdict(actual),"counts":dict(d.counts-before)})
            totals[arm].update(d.counts)
    for arm in ARMS:
        values = sorted(times[arm])
        count = len(values)
        c = totals[arm]
        result[arm] = {"requests":count, "origin_calls":c["origin_calls"],"fact_reads":c["fact_reads"],
            "record_checks":c["record_checks"], "metadata_probes":c["metadata_probes"],"skipped_origin":c["skipped_origin"],
            "p50_us":statistics.median(values)/1000,"p95_us":values[(95*count+99)//100-1]/1000,
            "new_model_calls":0}
    return {"scope":"authored synthetic in-process fixture; not a real agent or production evidence",
        "iterations":iterations,"arms":result,"first_iteration":first,"mismatches":errors,
        "historical_agent":"not executed; this fixture does not implement a historical agent",
        "model_first":"not executed; no model is part of this benchmark"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations",type=int,default=100)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    result = run(args.iterations)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"arms":result["arms"],"mismatches":len(result["mismatches"])},indent=2))
    raise SystemExit(bool(result["mismatches"]))
