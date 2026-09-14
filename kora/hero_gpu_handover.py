"""Bounded service handover state machine with injected host operations.

The caller supplies reviewed operations for a single declared borrowed service
and one owned worker unit. This module never discovers or stops arbitrary work.
"""

from __future__ import annotations

import time


def run_handover(ops, *, clock=time.monotonic, sleep=time.sleep):
    lease = None
    borrowed_touched = False
    worker_touched = False
    started = clock()
    receipt = {
        "owned_unit_stopped": False,
        "restored_health": False,
        "lease_released": False,
        "foreign_work_preserved": True,
        "restored_model": None,
        "failure": None,
    }
    try:
        ops.preflight()
        before = ops.baseline_identity()
        ops.require_idle()
        lease = ops.acquire()
        receipt["lease_id"] = lease["lease_id"]
        ops.persist_lease(lease)
        ops.require_lease(lease)
        ops.require_idle()
        borrowed_touched = True
        ops.stop_borrowed()
        ops.require_clear()
        worker_touched = True
        ops.start_worker(lease)
        last_heartbeat = clock()
        while not ops.worker_finished():
            if clock() - started >= 1200:
                raise TimeoutError("bounded worker window exhausted")
            if clock() - last_heartbeat >= 30:
                ops.heartbeat(lease)
                last_heartbeat = clock()
            sleep(2)
        ops.require_worker_output()
    except Exception as exc:  # noqa: BLE001 -- restoration must run after any host failure
        receipt["failure"] = type(exc).__name__
    finally:
        if lease is not None:
            try:
                if worker_touched:
                    ops.stop_worker()
                ops.require_owned_stopped()
                receipt["owned_unit_stopped"] = True
                if borrowed_touched:
                    ops.restore_borrowed()
                after = ops.wait_baseline_identity()
                if after != before:
                    raise RuntimeError("restored model identity differs")
                receipt["restored_health"] = True
                receipt["restored_model"] = "openai/gpt-oss-120b"
                ops.release(lease)
                receipt["lease_released"] = True
            except Exception as exc:  # noqa: BLE001 -- retain lease on failed restoration
                receipt["restoration_failure"] = type(exc).__name__
        receipt["elapsed_seconds"] = round(clock() - started, 3)
        ops.persist_receipt(receipt)
    return receipt
