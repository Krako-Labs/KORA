"""Independent assertions for the local synthetic activation prototype."""
from dataclasses import replace
from threading import Event, Thread
import unittest
from examples.support_tier_activation.run import (
    A, B, C, DAY, EXPIRY, VERSION, Activation, ConventionalCache,
    Directory, TierReply, RouteVersions, run,
)

class ActivationTests(unittest.TestCase):
    def setUp(self):
        self.d = Directory()
        self.d.set_grant(A, "g1", True)
        self.d.set_record(A, "v1", EXPIRY, "gold")
        self.a = Activation(self.d)

    def lookup(self, subject=A, date=DAY, versions=VERSION):
        return self.a.run(subject, date, versions)

    def test_repeat_is_real_skip(self):
        self.assertEqual(self.lookup(), TierReply("ok", "gold"))
        self.assertEqual(self.lookup(), TierReply("ok", "gold"))
        self.assertEqual(self.d.counts["origin_calls"], 1)
        self.assertEqual(self.d.counts["metadata_probes"], 2)
        self.assertEqual(self.d.counts["skipped_origin"], 1)

    def test_revocation_and_same_label_regrant(self):
        self.lookup()
        self.d.set_grant(A,"g1",False)
        self.assertEqual(self.lookup(), TierReply("denied"))
        self.d.set_grant(A,"g1",True)
        self.assertEqual(self.lookup(), TierReply("ok","gold"))
        self.assertEqual(self.d.counts["skipped_origin"], 0)

    def test_same_revision_new_value_and_rollback(self):
        self.lookup()
        self.d.set_record(A,"v1",EXPIRY,"silver")
        self.assertEqual(self.lookup(),TierReply("ok","silver"))
        self.d.set_record(A,"v1",EXPIRY,"gold")
        self.assertEqual(self.lookup(),TierReply("ok","gold"))
        self.assertEqual(self.d.counts["origin_calls"],3)

    def test_other_principal_and_tenant(self):
        self.lookup()
        self.assertEqual(self.lookup(B),TierReply("denied"))
        self.assertEqual(self.lookup(C),TierReply("denied"))
        self.assertEqual(self.d.counts["skipped_origin"],0)

    def test_unrelated_mutation(self):
        self.lookup()
        self.d.set_record(C,"v1",EXPIRY,"platinum")
        self.assertEqual(self.lookup(),TierReply("ok","gold"))
        self.assertEqual(self.d.counts["skipped_origin"],1)

    def test_versions_and_missing_version(self):
        self.lookup()
        for v in (RouteVersions("p2","r1","prompt1"),
                  RouteVersions("p2","r2","prompt1"),
                  RouteVersions("p2","r2","prompt2"),
                  RouteVersions("","r2","prompt2"),
                  RouteVersions("","r2","prompt2")):
            self.assertEqual(self.lookup(versions=v),TierReply("ok","gold"))
        self.assertEqual(self.d.counts["skipped_origin"],0)

    def test_inclusive_expiry_and_invalid_date(self):
        self.lookup()
        self.assertEqual(self.lookup(date=EXPIRY),TierReply("ok","gold"))
        self.assertEqual(self.lookup(date="2026-09-07"),TierReply("refresh_required"))
        self.assertEqual(self.lookup(date="invalid"),TierReply("refresh_required"))
        self.assertEqual(self.lookup(),TierReply("ok","gold"))
        self.assertEqual(self.d.counts["skipped_origin"],1)

    def test_missing_metadata_falls_back(self):
        self.lookup()
        original = self.d.probe
        self.d.probe = lambda s: None
        self.assertEqual(self.lookup(),TierReply("ok","gold"))
        self.d.probe = original
        self.assertEqual(self.lookup(),TierReply("ok","gold"))
        self.assertEqual(self.d.counts["origin_calls"],3)

    def test_probe_error_clears_entry(self):
        self.lookup()
        original = self.d.probe
        def fail(s):
            raise OSError("synthetic metadata error")
        self.d.probe = fail
        self.assertEqual(self.lookup(),TierReply("ok","gold"))
        self.d.probe = original
        self.assertEqual(self.lookup(),TierReply("ok","gold"))
        self.assertEqual(self.d.counts["origin_calls"],3)

    def test_scope_mismatch_from_probe(self):
        self.lookup()
        original = self.d.probe
        def wrong_subject(s):
            meta = original(s)
            return replace(meta, basis=replace(meta.basis, subject=B))
        self.d.probe = wrong_subject
        self.assertEqual(self.lookup(),TierReply("ok","gold"))
        self.assertEqual(self.d.counts["origin_calls"],2)

    def test_missing_record(self):
        self.d.set_grant(C,"g1",True)
        self.assertEqual(self.lookup(C),TierReply("not_found"))
        self.assertEqual(self.lookup(C),TierReply("not_found"))
        self.assertEqual(self.d.counts["fact_reads"],0)

    def test_revocation_serializes_with_lookup(self):
        self.lookup()
        revoked=Event()
        writer_started=Event()
        original=self.d.probe
        inside=Event()
        release=Event()
        replies=[]
        errors=[]
        def paused_probe(s):
            result=original(s)
            inside.set()
            if not release.wait(3):
                raise RuntimeError("test synchronization failed")
            return result
        self.d.probe=paused_probe
        def read():
            try:
                replies.append(self.lookup())
            except Exception as e:
                errors.append(e)
        def revoke():
            writer_started.set()
            self.d.set_grant(A,"g2",False)
            revoked.set()
        reader=Thread(target=read)
        reader.start()
        try:
            self.assertTrue(inside.wait(3))
            writer=Thread(target=revoke)
            writer.start()
            self.assertTrue(writer_started.wait(3))
            # The writer cannot acquire the same lock while validation is in flight.
            self.assertFalse(revoked.wait(0.02))
        finally:
            release.set()
            reader.join(3)
        writer.join(3)
        self.assertFalse(errors)
        self.assertTrue(revoked.is_set())
        self.assertEqual(replies,[TierReply("ok","gold")])
        self.d.probe=original
        self.assertEqual(self.lookup(),TierReply("denied"))

    def test_benchmark_counts_and_oracle(self):
        b=run(3)
        self.assertEqual(b["mismatches"],[])
        arms=b["arms"]
        for arm in arms.values():
            self.assertEqual(arm["requests"],96)
            self.assertEqual(arm["new_model_calls"],0)
        for name in ("activation_prototype","equal_metadata_cache"):
            self.assertEqual(arms[name]["origin_calls"],48)
            self.assertEqual(arms[name]["skipped_origin"],48)
            self.assertEqual(arms[name]["metadata_probes"],96)
        self.assertEqual(arms["kora_shadow"]["origin_calls"],96)
        self.assertEqual(arms["kora_shadow"]["skipped_origin"],0)

if __name__ == "__main__":
    unittest.main()
