import pytest

from kora.hero_gpu_handover import run_handover


class Ops:
    def __init__(self, fail=None):
        self.fail = fail
        self.calls = []
        self.receipt = None

    def action(self, name):
        self.calls.append(name)
        if self.fail == name:
            raise RuntimeError(name)

    def preflight(self):
        self.action("preflight")

    def baseline_identity(self):
        self.action("identity")
        return "baseline"

    def require_idle(self):
        self.action("idle")

    def acquire(self):
        self.action("acquire")
        return {"lease_id": "test"}

    def persist_lease(self, l):
        self.action("persist_lease")

    def require_lease(self, l):
        self.action("require_lease")

    def stop_borrowed(self):
        self.action("stop_borrowed")

    def require_clear(self):
        self.action("clear")

    def start_worker(self, l):
        self.action("start_worker")

    def worker_finished(self):
        self.action("finished")
        return True

    def require_worker_output(self):
        self.action("output")

    def heartbeat(self, l):
        self.action("heartbeat")

    def stop_worker(self):
        self.action("stop_worker")

    def require_owned_stopped(self):
        self.action("owned_stopped")

    def restore_borrowed(self):
        self.action("restore")

    def wait_baseline_identity(self):
        self.action("restored_identity")
        return "baseline"

    def release(self, l):
        self.action("release")

    def persist_receipt(self, r):
        self.receipt = r


def test_handover_orders_exclusive_lease_before_service_mutation_and_restore_before_release():
    o = Ops()
    r = run_handover(o)
    assert r["lease_released"] and r["restored_health"]
    assert (
        o.calls.index("acquire")
        < o.calls.index("stop_borrowed")
        < o.calls.index("start_worker")
    )
    assert (
        o.calls.index("stop_worker")
        < o.calls.index("restore")
        < o.calls.index("release")
    )


@pytest.mark.parametrize("failure", ["clear", "start_worker", "finished", "output"])
def test_worker_failure_restores_and_releases(failure):
    o = Ops(failure)
    r = run_handover(o)
    assert r["failure"] == "RuntimeError"
    assert r["restored_health"] and r["lease_released"]


@pytest.mark.parametrize(
    "failure",
    ["stop_worker", "owned_stopped", "restore", "restored_identity", "release"],
)
def test_restoration_failure_retains_lease(failure):
    o = Ops(failure)
    r = run_handover(o)
    assert not r["lease_released"]
    assert "restoration_failure" in r


def test_foreign_resource_preflight_never_mutates_services():
    o = Ops("preflight")
    r = run_handover(o)
    assert o.calls == ["preflight"] and not r["lease_released"]


def test_timeout_stops_owned_work_and_restores():
    o = Ops()
    o.worker_finished = lambda: False
    ticks = iter([0, 0, 1201, 1202])
    r = run_handover(o, clock=lambda: next(ticks), sleep=lambda _: None)
    assert r["failure"] == "TimeoutError"
    assert r["restored_health"] and r["lease_released"]
