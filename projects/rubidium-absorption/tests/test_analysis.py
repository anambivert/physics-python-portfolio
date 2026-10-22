"""Numerical and failure-mode checks; all generated inputs here are synthetic."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np

spec = importlib.util.spec_from_file_location("lab5_analysis", Path(__file__).parents[1] / "src/analyze.py")
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


class AnalysisTests(unittest.TestCase):
    def test_gaussian_half_maximum(self):
        values = analysis.gaussian(np.array([-1, 0, 1]), -4, 0, 2, 5)
        np.testing.assert_allclose(values, [3, 1, 3], atol=1e-14)

    def test_recover_noisy_negative_gaussian(self):
        t = np.linspace(-5, 5, 1001)
        rng = np.random.default_rng(42)
        y = analysis.gaussian(t, -0.004, 0.35, 1.6, 0.001) + rng.normal(0, 1e-5, len(t))
        fit, _ = analysis.fit_dip(t, y, 0.3, 4)
        self.assertAlmostEqual(fit["center_ms"], 0.35, delta=0.005)
        self.assertAlmostEqual(fit["fwhm_ms"], 1.6, delta=0.01)
        self.assertTrue(fit["full_fwhm_covered"])

    def test_interpolation_and_coverage(self):
        np.testing.assert_allclose(analysis.interpolate_background([1, 1.5, 2], [0, 1, 2], [0, 2, 4]), [2, 3, 4])
        with self.assertRaisesRegex(ValueError, "extrapolation"):
            analysis.interpolate_background([-0.1, 1], [0, 1, 2], [0, 2, 4])

    def test_reject_invalid_numeric_inputs(self):
        for t, y in [([0, 0, 1], [1, 2, 3]), ([0, 2, 1], [1, 2, 3]),
                     ([0, 1, 2], [1, np.nan, 3]), ([0, 1, 2], [1, 2])]:
            with self.subTest(t=t, y=y), self.assertRaises(ValueError):
                analysis.check_xy(t, y)

    def test_csv_comments_units_and_first_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.csv"
            path.write_text("% Instrument\n% Time, A, B\n0.001,1,2\n0.002,3,4\n")
            data = analysis.load_moku_csv(path)
            np.testing.assert_allclose(data, [[1, 1, 2], [2, 3, 4]])
            path.write_text("0,1\n1,2\n")
            with self.assertRaisesRegex(ValueError, "three"):
                analysis.load_moku_csv(path)

    def test_select_four_distinct_dips(self):
        t = np.linspace(0, 40, 4001)
        y = sum(analysis.gaussian(t, -1, center, 0.9, 0) for center in (5, 15, 25, 35))
        np.testing.assert_allclose(t[analysis.select_dips(t, y)], [5, 15, 25, 35])

    def test_reject_segment_boundary_minimum(self):
        with self.assertRaisesRegex(ValueError, "boundary"):
            analysis.select_dips(np.arange(80), np.arange(80))

    def test_reject_constant_or_uncovered_fit(self):
        t = np.linspace(-5, 5, 101)
        with self.assertRaisesRegex(ValueError, "constant"):
            analysis.fit_dip(t, np.ones_like(t), 0, 3)
        with self.assertRaisesRegex(ValueError, "covered"):
            analysis.fit_dip(t, -np.exp(-t**2), 4, 3)

    def test_flag_half_maximum_outside_window(self):
        t = np.linspace(-2, 2, 501)
        fit, _ = analysis.fit_dip(t, analysis.gaussian(t, -0.01, 0, 5, 0.02), 0, 1.5)
        self.assertFalse(fit["full_fwhm_covered"])
        self.assertTrue(fit["warnings"])

    def test_negative_voltage_ratio_is_not_repaired(self):
        t = np.linspace(0, 10, 101)
        y = np.full_like(t, 0.01)
        y[50] = -0.005
        result = analysis.transmission_diagnostic(t, y, t, np.zeros_like(t), [0, 10], 1)
        self.assertEqual(result["raw_voltage_ratio"], -0.5)
        self.assertFalse(result["ratio_in_physical_range"])
        self.assertFalse(result["accepted_as_optical_transmission"])
        self.assertIsNone(result["number_density_m3"])
        self.assertIsNone(result["pressure_Pa"])


if __name__ == "__main__":
    unittest.main()
