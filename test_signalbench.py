"""Controls establish synthetic numerical behavior, not physical measurement accuracy."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from signalbench import analyze, demo, read_recording


class NumericalControls(unittest.TestCase):
    def test_known_frequency_and_power_change(self):
        fs = 1_024_000
        x = .2 * np.exp(2j * np.pi * 125_000 * np.arange(16384) / fs)
        a, b = analyze(x, fs), analyze(x / 10, fs)
        self.assertAlmostEqual(a["largest_non_dc_peak_offset_hz"], 125_000)
        self.assertAlmostEqual(b["mean_sample_power_db_re_unit"] - a["mean_sample_power_db_re_unit"], -20)
        self.assertAlmostEqual(a["psd_integral_window_weighted_sample_power"], .04, places=8)

    def test_dc_and_adc_rails(self):
        x = np.exp(2j * np.pi * np.arange(4096) / 32)
        a = analyze(.2 * x + .15, 1_024_000)
        self.assertGreater(a["dc_power_fraction"], .3)
        clipped = np.clip(1.3 * x.real, -1, 1) + 1j * np.clip(1.3 * x.imag, -1, 1)
        self.assertGreater(analyze(clipped, 1_024_000)["component_rail_fraction_at_unit_limit"], .2)

    def test_uint8_interleaving_and_normalization(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "u8.sigmf-meta"
            raw = bytes([0, 255]) * 256
            p.with_suffix(".sigmf-data").write_bytes(raw)
            p.write_text(json.dumps({"global": {"core:datatype": "cu8", "core:sample_rate": 1000,
                                                 "core:sha512": hashlib.sha512(raw).hexdigest()}}))
            x, _, ok = read_recording(p)
            self.assertTrue(ok)
            np.testing.assert_array_equal(x, np.full(256, -1 + 1j))

    def test_integrity_detects_a_changed_byte(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            demo(out)
            data = out / "clean.sigmf-data"
            raw = bytearray(data.read_bytes())
            raw[100] ^= 1
            data.write_bytes(raw)
            self.assertIs(read_recording(out / "clean.sigmf-meta")[2], False)

    def test_invalid_data_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze(np.zeros(100), 1000)
        with self.assertRaises(ValueError):
            analyze(np.zeros(256), 0)
        with self.assertRaises(ValueError):
            analyze(np.full(256, np.nan), 1000)

    def test_sample_rate_error_is_not_hidden(self):
        fs = 1_024_000
        x = .2 * np.exp(2j * np.pi * 125_000 * np.arange(16384) / fs)
        self.assertEqual(analyze(x, fs * 2)["largest_non_dc_peak_offset_hz"], 250_000)


if __name__ == "__main__":
    unittest.main()
