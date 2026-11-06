"""Hardware-free tests for the F2 capture orchestrator (no RTL-SDR required)."""
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools import capture_gain_sweep as sweep


class GainSweepControls(unittest.TestCase):
    def test_loss_markers_are_recorded(self):
        log = "Reading samples in async mode...\nlost at least 100 bytes\n"
        self.assertEqual(sweep.loss_lines(log), ["lost at least 100 bytes"])
        self.assertEqual(sweep.loss_lines("Tuned to 100000000 Hz.\n"), [])

    def test_metadata_is_uncalibrated_and_compatible(self):
        meta = sweep.sigmf_metadata("a" * 128, "19.7")
        self.assertEqual(meta["global"]["core:datatype"], "cu8")
        self.assertEqual(meta["global"]["core:sample_rate"], 1024000)
        self.assertEqual(meta["global"]["core:sha512"], "a" * 128)
        self.assertEqual(meta["captures"][0]["core:frequency"], 100000000)
        self.assertNotIn("core:datetime", meta["captures"][0])

    def test_gain_sweep_writes_nine_traceable_sets(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "new_sweep"

            def fake_run(args, stdout, stderr, check, timeout):
                Path(args[-1]).write_bytes(bytes([127, 128]) * 256)
                stderr.write(b"Tuned to 100000000 Hz.\n")
                return SimpleNamespace(returncode=0)

            with patch.object(sweep, "SAMPLE_COUNT", 256), \
                 patch.object(sweep.shutil, "which", return_value="/usr/bin/rtl_sdr"), \
                 patch.object(sweep.subprocess, "run", side_effect=fake_run):
                sweep.run_sweep(out)

            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            results = manifest["results"]
            self.assertEqual(len(results), 9)
            self.assertEqual(
                [(r["repeat"], r["manual_gain_db"]) for r in results],
                [(repeat, gain) for repeat in (1, 2, 3) for gain in (7.7, 19.7, 32.8)],
            )
            self.assertTrue(all(r["file_integrity_preconditions_passed"] for r in results))
            for record in results:
                data = (out / record["data_filename"]).read_bytes()
                meta = json.loads((out / record["metadata_filename"]).read_text(encoding="utf-8"))
                self.assertEqual(len(data), 512)
                self.assertEqual(meta["global"]["core:sha512"], hashlib.sha512(data).hexdigest())
            with patch.object(sweep.shutil, "which", return_value="/usr/bin/rtl_sdr"):
                with self.assertRaises(FileExistsError):
                    sweep.run_sweep(out)

    def test_short_capture_preserved_and_not_marked_valid(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "short"

            def fake_run(args, stdout, stderr, check, timeout):
                Path(args[-1]).write_bytes(b"\\x7f\\x80")
                stderr.write(b"lost at least 100 bytes\n")
                return SimpleNamespace(returncode=0)

            with patch.object(sweep, "SAMPLE_COUNT", 256), \
                 patch.object(sweep.shutil, "which", return_value="/usr/bin/rtl_sdr"), \
                 patch.object(sweep.subprocess, "run", side_effect=fake_run):
                with self.assertRaisesRegex(RuntimeError, "expected 512"):
                    sweep.run_sweep(out)

            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "IN_PROGRESS")
            self.assertEqual(len(manifest["results"]), 1)
            self.assertFalse(manifest["results"][0]["file_integrity_preconditions_passed"])
            self.assertEqual(manifest["results"][0]["sample_loss_log_lines"], ["lost at least 100 bytes"])
            self.assertFalse(list(out.glob("*.sigmf-meta")))


if __name__ == "__main__":
    unittest.main()
