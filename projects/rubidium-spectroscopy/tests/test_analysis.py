"""Synthetic numerical checks; these are not experimental measurements."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

MODULE_PATH = Path(__file__).resolve().parents[1] / "src/analyze.py"
SPEC = importlib.util.spec_from_file_location("lab6_analysis", MODULE_PATH)
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class AnalysisTests(unittest.TestCase):
    def test_width_convention(self):
        for model in (analysis.gaussian, analysis.lorentzian):
            values = model(np.array([9.5, 10, 10.5]), 2, 10, 1, 4)
            np.testing.assert_allclose(values, [5, 6, 5], rtol=1e-12)

    def test_recover_gaussian_and_lorentzian(self):
        rng = np.random.default_rng(4061)
        x = np.linspace(145, 150, 501)
        for name, model in (("gaussian", analysis.gaussian), ("lorentzian", analysis.lorentzian)):
            for sign in (1, -1):
                with self.subTest(name=name, sign=sign):
                    y = model(x, sign * .02, 147.4, .7, .01) + rng.normal(0, .00001, x.size)
                    fitted = analysis.fit_feature(x, y, "peak" if sign == 1 else "dip")[name]
                    self.assertAlmostEqual(fitted["center_ms"], 147.4, delta=.002)
                    self.assertAlmostEqual(fitted["fwhm_ms"], .7, delta=.003)
                    self.assertTrue(fitted["full_fwhm_covered"])

    def test_background_scale_offset_and_interpolation(self):
        t = np.linspace(0, 10, 101)
        bg_t = np.linspace(0, 10, 201)
        bg = 0.1 + .01 * bg_t
        feature = np.where((t >= 4) & (t <= 6), .02, 0)
        signal = 1.3 * (.1 + .01 * t) + .04 + feature
        corrected, _, fit = analysis.subtract_background(t, signal, bg_t, bg, [4, 6])
        np.testing.assert_allclose(corrected, feature, atol=1e-12)
        self.assertAlmostEqual(fit["scale"], 1.3)
        self.assertAlmostEqual(fit["offset_V"], .04)

    def test_refuse_background_extrapolation(self):
        t = np.linspace(0, 10, 101)
        with self.assertRaisesRegex(ValueError, "extrapolation"):
            analysis.subtract_background(t, t, t[1:], t[1:], [4, 6])

    def test_reject_constant_background(self):
        t = np.linspace(0, 10, 101)
        with self.assertRaisesRegex(ValueError, "not separately identifiable"):
            analysis.subtract_background(t, t, t, np.ones(t.size), [4, 6])

    def test_reject_bad_input(self):
        for t, y in (([1, 1], [1, 2]), ([2, 1], [1, 2]), ([1, 2], [1, np.nan])):
            with self.assertRaises(ValueError):
                analysis.check_xy(t, y)
        with self.assertRaises(ValueError):
            analysis.fit_feature([1, 2], [1, 2])
        with self.assertRaises(ValueError):
            analysis.fit_feature(np.arange(10), np.ones(10))

    def test_flag_incomplete_feature_window(self):
        x = np.linspace(146, 147.5, 151)
        y = analysis.lorentzian(x, .015, 147.32, .86, .01)
        fit = analysis.fit_feature(x, y)["lorentzian"]
        self.assertFalse(fit["full_fwhm_covered"])
        self.assertTrue(any("extrapolation" in message for message in fit["warnings"]))

    def test_calibration_requires_source_and_units(self):
        self.assertIsNone(analysis.validate_calibration({"mhz_per_ms": None}))
        self.assertEqual(analysis.validate_calibration({"mhz_per_ms": -20, "source": "synthetic test"}), -20)
        for value in [0, float("nan"), float("inf"), True]:
            with self.assertRaises(ValueError):
                analysis.validate_calibration({"mhz_per_ms": value, "source": "test"})
        with self.assertRaises(ValueError):
            analysis.validate_calibration({"mhz_per_ms": 20, "source": ""})

    def test_complete_csv_to_outputs_without_frequency_scale(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            t = np.linspace(130, 160, 3001)
            bg = .15 + .0008 * (t - 130)
            y = 1.2 * bg + .02 + analysis.gaussian(t, .015, 147, .7, 0)
            header = "\n".join(["Synthetic test metadata"] * 10)
            for name, values in (("signal.csv", y), ("bg.csv", bg)):
                np.savetxt(root / name, np.column_stack((t / 1000, values, values)), delimiter=",", header=header, comments="% ")
            config = {"signal_file": "signal.csv", "background_file": "bg.csv", "window_ms": [130, 160],
                      "fit_window_ms": [145, 149], "exclude_ms": [144, 150], "calibration": {"mhz_per_ms": None}}
            result = analysis.analyse(config, root)
            fit = result["summary"]["fits"]["gaussian"]
            self.assertAlmostEqual(fit["fwhm_ms"], .7, delta=.002)
            self.assertIsNone(fit["fwhm_MHz"])
            config["calibration"] = {"mhz_per_ms": -20, "source": "Synthetic validation only"}
            calibrated = analysis.analyse(config, root)
            self.assertAlmostEqual(calibrated["summary"]["fits"]["gaussian"]["fwhm_MHz"], 14, delta=.04)
            analysis.write_outputs(result, root / "output")
            saved = json.loads((root / "output/summary.json").read_text())
            self.assertEqual(saved["calibration_status"], "not supplied; widths in ms only")
            self.assertIsNone(saved["config"]["calibration"]["mhz_per_ms"])
            for file in ["background-subtracted.csv", "background.png", "fit-comparison.png"]:
                self.assertGreater((root / "output" / file).stat().st_size, 100)

    def test_missing_csv_has_clear_error(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(FileNotFoundError, "Missing measurement file"):
                analysis.load_moku_csv(Path(temp) / "missing.csv")


if __name__ == "__main__":
    unittest.main()
