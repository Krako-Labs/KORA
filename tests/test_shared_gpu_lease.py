import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "lease", Path(__file__).resolve().parents[1] / "scripts" / "gpu_lease.py"
)
lease = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lease)


class LeaseTests(unittest.TestCase):
    def test_busy_and_exact_service(self):
        sample = {"processes": [{"cgroup": "0::/system.slice/real.service"}]}
        for allowed in ["", "other.service", "real"]:
            with self.assertRaises(RuntimeError):
                lease.check_busy(sample, allowed)
        lease.check_busy(sample, "real.service")

    def test_concurrent_and_stale_ownership(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(
                os.environ,
                KRAKO_GPU_STATE=directory,
                PYTHONPATH=str(Path(__file__).resolve().parents[1] / "scripts"),
            )
            code = "import gpu_lease as m; m.observe=lambda:{'processes':[]}; m.main()"
            prefix = [sys.executable, "-c", code]
            acquire = prefix + [
                "acquire",
                "--project",
                "test",
                "--owner",
                "test",
                "--purpose",
                "test",
                "--minutes",
                "1",
                "--unit",
                "test.service",
            ]
            processes = [
                subprocess.Popen(
                    acquire, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                for _ in range(2)
            ]
            for process in processes:
                process.communicate(timeout=10)
            self.assertEqual(sorted(p.returncode for p in processes), [0, 1])
            path = Path(directory, "active.json")
            data = json.loads(path.read_text())
            data["expected_end_epoch"] = 0
            path.write_text(json.dumps(data))
            self.assertNotEqual(
                subprocess.run(
                    acquire, env=env, capture_output=True, check=False
                ).returncode,
                0,
            )
            bad = prefix + ["release", "--lease-id", "wrong"]
            self.assertNotEqual(
                subprocess.run(
                    bad, env=env, capture_output=True, check=False
                ).returncode,
                0,
            )
            good = prefix + ["release", "--lease-id", data["lease_id"]]
            self.assertEqual(
                subprocess.run(
                    good, env=env, capture_output=True, check=False
                ).returncode,
                0,
            )
            self.assertFalse(path.exists())
            events = [
                json.loads(x)
                for x in Path(directory, "history.jsonl").read_text().splitlines()
            ]
            self.assertEqual([x["event"] for x in events], ["acquire", "release"])
            self.assertGreaterEqual(events[-1]["lease"]["elapsed_seconds"], 0)


if __name__ == "__main__":
    unittest.main()
