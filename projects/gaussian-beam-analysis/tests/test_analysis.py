"""Numerical recovery, input integrity and scientific diagnostics for Lab 02."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gaussian_analysis", PROJECT / "src/analyze.py")
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class GaussianAnalysisTests(unittest.TestCase):
    def test_radius_and_fwhm_conventions(self):
        self.assertAlmostEqual(analysis.gaussian(7, 10, 2, 5, 3), 3 + 10 * np.exp(-2))
        half = 5 * np.sqrt(2 * np.log(2)) / 2
        self.assertAlmostEqual(analysis.gaussian(2 + half, 10, 2, 5, 3), 8)

    def test_recovers_noisy_narrow_and_broad_profiles(self):
        rng = np.random.default_rng(2026)
        x = np.arange(1000, dtype=float)
        for radius in (8.0, 120.0):
            with self.subTest(radius=radius):
                y = analysis.gaussian(x, 200, 430, radius, 12) + rng.normal(0, 0.5, len(x))
                result = analysis.fit_profile(x, y)
                self.assertAlmostEqual(result["radius_samples"], radius, delta=radius * 0.01)
                self.assertAlmostEqual(result["center_samples"], 430, delta=0.1)
                self.assertAlmostEqual(result["offset_counts"], 12, delta=0.1)

    def test_fit_respects_position_translation_and_scaling(self):
        x = np.linspace(-20, 20, 401)
        y = analysis.gaussian(x, 80, 1, 5, 2)
        result = analysis.fit_profile(10000 + 3 * x, y)
        self.assertAlmostEqual(result["radius_samples"], 15, places=5)
        self.assertAlmostEqual(result["center_samples"], 10003, places=5)

    def test_fixed_zero_baseline_recovers_zero_offset_signal(self):
        x = np.arange(500, dtype=float)
        result = analysis.fit_profile(x, analysis.gaussian(x, 200, 240, 60, 0), baseline="zero")
        self.assertAlmostEqual(result["radius_samples"], 60, places=4)
        self.assertEqual(result["offset_counts"], 0)

    def test_invalid_profiles_are_rejected(self):
        x = np.arange(10, dtype=float)
        invalid = [(x[:5], x[:5]), (x, np.ones(10)), (x[::-1], x),
                   (np.zeros(10), x), (x, np.full(10, np.nan)), (x, x[:-1])]
        for positions, intensity in invalid:
            with self.subTest(positions=positions):
                with self.assertRaises(ValueError):
                    analysis.fit_profile(positions, intensity)

    def test_missing_file_error_names_the_input(self):
        with self.assertRaisesRegex(FileNotFoundError, "missing.xlsx"):
            analysis.load_profile(PROJECT / "data/missing.xlsx")

    def test_excel_import_keeps_every_row(self):
        x, y = analysis.load_profile(PROJECT / "data/measurements/beforeexpander.xlsx")
        self.assertEqual(len(y), 2038)
        self.assertEqual(x[0], 0)
        self.assertEqual(x[-1], 2037)
        self.assertEqual(y[0], 0)
        self.assertEqual(max(y), 222)

    def test_saturation_and_incomplete_width_are_reported(self):
        x = np.arange(100, dtype=float)
        y = analysis.gaussian(x, 250, 50, 150, 10)
        result = analysis.fit_profile(x, y, saturation_level=255)
        self.assertFalse(result["full_radius_covered"])
        self.assertGreater(result["samples_at_ceiling"], 0)
        self.assertTrue(any("ceiling" in warning for warning in result["warnings"]))

    def test_ratio_and_independent_uncertainty(self):
        before = {"radius_samples": 10, "radius_stderr_samples": 1}
        after = {"radius_samples": 20, "radius_stderr_samples": 2}
        ratio = analysis.radius_ratio(before, after)
        self.assertEqual(ratio["ratio"], 2)
        self.assertAlmostEqual(ratio["conditional_stderr"], np.sqrt(0.08))
        after["radius_stderr_samples"] = None
        self.assertIsNone(analysis.radius_ratio(before, after)["conditional_stderr"])

    def test_end_to_end_real_inputs_and_baseline_sensitivity(self):
        with tempfile.TemporaryDirectory() as directory:
            summary = analysis.run_analysis(PROJECT / "config/analysis.json", directory, make_figures=False)
            saved = json.loads((Path(directory) / "summary.json").read_text())
            self.assertEqual(summary, saved)
            self.assertEqual(len(saved["profiles"]), 4)
            self.assertIsNone(saved["physical_radius_um"])
            fits = {item["id"]: item for item in saved["profiles"]}
            after = fits["after"]
            self.assertEqual(after["free_baseline"]["samples_at_ceiling"], 21)
            self.assertFalse(after["free_baseline"]["full_radius_covered"])
            self.assertGreater(after["free_baseline"]["radius_samples"],
                               after["zero_baseline_sensitivity"]["radius_samples"] * 1.3)
            for item in saved["profiles"]:
                data = np.loadtxt(Path(directory) / f"{item['id']}-profile.csv", delimiter=",", skiprows=1)
                np.testing.assert_allclose(data[:, 1] - data[:, 2], data[:, 3], atol=2e-7)
                self.assertEqual(len(data), item["free_baseline"]["samples"])


if __name__ == "__main__":
    unittest.main()
