"""Portable Lab 6 background subtraction and single-feature model comparison.

AI-assisted refactor of the uploaded notebook; see ../PROVENANCE.md.
Time is read in seconds and analysed in milliseconds. No frequency calibration
is assumed. Run with --help for the interface.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import platform
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import OptimizeWarning, curve_fit

PROJECT = Path(__file__).resolve().parents[1]


def gaussian(t, amplitude, center, fwhm, offset):
    """Gaussian with FWHM in the same time units as t."""
    return amplitude * np.exp(-4 * np.log(2) * ((t - center) / fwhm) ** 2) + offset


def lorentzian(t, amplitude, center, fwhm, offset):
    """Lorentzian with FWHM in the same time units as t."""
    return amplitude / (1 + (2 * (t - center) / fwhm) ** 2) + offset


def check_xy(t, y, minimum=2):
    t, y = np.asarray(t, dtype=float), np.asarray(y, dtype=float)
    if t.ndim != 1 or y.shape != t.shape or t.size < minimum:
        raise ValueError(f"Expected at least {minimum} paired one-dimensional samples.")
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(y)):
        raise ValueError("Inputs must contain only finite numeric values.")
    if not np.all(np.diff(t) > 0):
        raise ValueError("Time must be strictly increasing with no duplicates.")
    return t, y


def check_window(window, label):
    values = np.asarray(window, dtype=float)
    if values.shape != (2,) or not np.all(np.isfinite(values)) or values[0] >= values[1]:
        raise ValueError(f"{label} must be [lower, upper] with lower < upper.")
    return values


def load_moku_csv(path, header_rows=10, channel="chA"):
    """Read numeric columns [time_s, chA_V, chB_V] after a fixed header."""
    if channel not in {"chA", "chB"}:
        raise ValueError("channel must be chA or chB.")
    if isinstance(header_rows, bool) or not isinstance(header_rows, int) or header_rows < 0:
        raise ValueError("header_rows must be a non-negative integer.")
    if not Path(path).is_file():
        raise FileNotFoundError(f"Missing measurement file: {path}")
    try:
        data = np.loadtxt(path, delimiter=",", comments="%", skiprows=header_rows, ndmin=2)
    except ValueError as error:
        raise ValueError(f"Cannot read numeric Moku data from {Path(path).name}; check header_rows and columns.") from error
    if data.shape[1] != 3:
        raise ValueError("Expected exactly three CSV columns: time_s, chA_V, chB_V.")
    if not np.all(np.isfinite(data)):
        raise ValueError("CSV contains missing or non-finite values.")
    column = 1 if channel == "chA" else 2
    return check_xy(data[:, 0] * 1000, data[:, column])


def subtract_background(t, signal, bg_t, bg_signal, exclude_ms):
    """Interpolate within measured coverage, then fit signal = a*background + b."""
    t, signal = check_xy(t, signal, minimum=6)
    bg_t, bg_signal = check_xy(bg_t, bg_signal)
    lower, upper = check_window(exclude_ms, "exclude_ms")
    if lower < t[0] or upper > t[-1]:
        raise ValueError("The exclusion window must lie inside the selected signal interval.")
    if t[0] < bg_t[0] or t[-1] > bg_t[-1]:
        raise ValueError("Background does not cover the selected signal times; extrapolation is disabled.")
    background = np.interp(t, bg_t, bg_signal)
    baseline = (t < lower) | (t > upper)
    if baseline.sum() < 3:
        raise ValueError("At least three points outside the feature are needed to fit the background.")
    design = np.column_stack((background[baseline], np.ones(baseline.sum())))
    coefficients, _, rank, _ = np.linalg.lstsq(design, signal[baseline], rcond=None)
    if rank < 2:
        raise ValueError("Background scale and offset are not separately identifiable from a constant background.")
    a, b = map(float, coefficients)
    fitted = a * background + b
    return signal - fitted, fitted, {"scale": a, "offset_V": b, "baseline_points": int(baseline.sum())}


def finite_or_none(value):
    return float(value) if np.isfinite(value) else None


def fit_feature(t, signal, polarity="peak"):
    """Fit two four-parameter models; report conditional covariance and coverage."""
    t, signal = check_xy(t, signal, minimum=8)
    if polarity not in {"peak", "dip"}:
        raise ValueError("polarity must be peak or dip.")
    span, height = float(np.ptp(t)), float(np.ptp(signal))
    if height <= 0:
        raise ValueError("Cannot identify a feature in a constant signal.")
    x = t - t[0]
    positive = polarity == "peak"
    offset = float(signal.min() if positive else signal.max())
    center = float(x[np.argmax(signal) if positive else np.argmin(signal)])
    amplitude = height if positive else -height
    initial = [amplitude, center, span / 4, offset]
    min_width = max(np.finfo(float).eps * span * 100, np.finfo(float).tiny)
    lower = [0 if positive else -np.inf, 0, min_width, -np.inf]
    upper = [np.inf if positive else 0, span, np.inf, np.inf]
    results = {}
    for name, model in (("gaussian", gaussian), ("lorentzian", lorentzian)):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", OptimizeWarning)
            parameters, covariance = curve_fit(
                model, x, signal, p0=initial, bounds=(lower, upper),
                x_scale=[height, span, span, height], maxfev=20000,
            )
        parameters[1] += t[0]
        residual = signal - model(t, *parameters)
        errors = np.sqrt(np.maximum(np.diag(covariance), 0))
        fitted_center, width = float(parameters[1]), float(parameters[2])
        full_fwhm_covered = bool(t[0] <= fitted_center - width / 2 and fitted_center + width / 2 <= t[-1])
        messages = [str(item.message) for item in caught]
        if not full_fwhm_covered:
            messages.append("The selected window does not span both fitted half-maximum positions; width depends on model extrapolation.")
        if not np.all(np.isfinite(covariance)):
            messages.append("Parameter covariance is not finite; standard errors are unavailable.")
        results[name] = {
            "amplitude_V": float(parameters[0]), "center_ms": fitted_center,
            "fwhm_ms": width, "offset_V": float(parameters[3]),
            "rss_V2": float(np.dot(residual, residual)),
            "conditional_standard_errors": dict(zip(
                ["amplitude_V", "center_ms", "fwhm_ms", "offset_V"],
                [finite_or_none(error) for error in errors],
            )),
            "full_fwhm_covered": full_fwhm_covered, "warnings": messages,
        }
    return results


def validate_calibration(calibration):
    slope = calibration.get("mhz_per_ms")
    if slope is None:
        return None
    if isinstance(slope, bool) or not np.isfinite(float(slope)) or float(slope) == 0:
        raise ValueError("Calibration must be a finite, non-zero slope in MHz/ms, or null.")
    if not isinstance(calibration.get("source"), str) or not calibration["source"].strip():
        raise ValueError("A frequency calibration requires its source/derivation.")
    return float(slope)


def parameter_values(result):
    return [result[key] for key in ("amplitude_V", "center_ms", "fwhm_ms", "offset_V")]


def analyse(config, project_root=PROJECT):
    """Analyse supplied measurements; return data and metadata without writing files."""
    window = check_window(config["window_ms"], "window_ms")
    fit_window = check_window(config["fit_window_ms"], "fit_window_ms")
    if fit_window[0] < window[0] or fit_window[1] > window[1]:
        raise ValueError("fit_window_ms must be inside window_ms.")
    slope = validate_calibration(config.get("calibration", {}))
    options = {"header_rows": config.get("header_rows", 10), "channel": config.get("channel", "chA")}
    paths = [Path(project_root) / config[key] for key in ("signal_file", "background_file")]
    t, signal = load_moku_csv(paths[0], **options)
    bg_t, bg_signal = load_moku_csv(paths[1], **options)
    mask = (t >= window[0]) & (t <= window[1])
    t, signal = t[mask], signal[mask]
    corrected, background, background_parameters = subtract_background(t, signal, bg_t, bg_signal, config["exclude_ms"])
    selection = (t >= fit_window[0]) & (t <= fit_window[1])
    fits = fit_feature(t[selection], corrected[selection], config.get("polarity", "peak"))
    for result in fits.values():
        result["fwhm_MHz"] = None if slope is None else abs(slope) * result["fwhm_ms"]
    summary = {
        "source": "Reanalysis of the explicitly supplied CSV files; inspect their provenance.",
        "inputs": [{"name": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
        "config": copy.deepcopy(config), "background": background_parameters, "fits": fits,
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
        "lower_rss_model": min(fits, key=lambda name: fits[name]["rss_V2"]),
        "calibration_status": "not supplied; widths in ms only" if slope is None else "user-supplied; not independently verified",
        "uncertainty_note": "Standard errors are conditional residual-scaled curve-fit covariance estimates. Background, calibration, correlated noise and model uncertainty are not propagated.",
        "comparison_note": "Lower RSS compares these models on the same points; it does not establish the physical line shape.",
    }
    return {"time_ms": t, "signal_V": signal, "background_V": background,
            "corrected_V": corrected, "selection": selection, "summary": summary}


def write_outputs(result, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    t, signal = result["time_ms"], result["corrected_V"]
    np.savetxt(destination / "background-subtracted.csv", np.column_stack((t, signal)),
               delimiter=",", header="time_ms,signal_V", comments="")
    (destination / "summary.json").write_text(json.dumps(result["summary"], indent=2, allow_nan=False) + "\n")

    figure, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True, constrained_layout=True)
    axes[0].plot(t, result["signal_V"], label="Signal")
    axes[0].plot(t, result["background_V"], label="Scaled background")
    axes[0].set(ylabel="Signal (V)", title="Background correction")
    axes[0].legend()
    axes[1].plot(t, signal)
    axes[1].set(xlabel="Time (ms)", ylabel="Corrected signal (V)")
    figure.savefig(destination / "background.png", dpi=160)
    plt.close(figure)

    selected = result["selection"]
    tx, yx = t[selected], signal[selected]
    dense = np.linspace(tx[0], tx[-1], 500)
    figure, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True, constrained_layout=True)
    axes[0].scatter(tx, yx, s=10, label="Data", color="black")
    for name, model in (("gaussian", gaussian), ("lorentzian", lorentzian)):
        parameters = parameter_values(result["summary"]["fits"][name])
        axes[0].plot(dense, model(dense, *parameters), label=name.title())
        axes[1].plot(tx, yx - model(tx, *parameters), label=name.title())
    axes[0].set(ylabel="Corrected signal (V)", title="Selected feature: model comparison")
    axes[0].legend()
    axes[1].axhline(0, color="black", linewidth=0.7)
    axes[1].set(xlabel="Time (ms)", ylabel="Residual (V)")
    axes[1].legend()
    figure.savefig(destination / "fit-comparison.png", dpi=160)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=PROJECT / "config/analysis.json")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for newly computed outputs.")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text())
        result = analyse(config)
        write_outputs(result, args.output_dir)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        parser.exit(1, f"Analysis could not complete: {error}\n")
    print(f"Saved analysis to {args.output_dir}")
    print(result["summary"]["calibration_status"])
    for name, model in result["summary"]["fits"].items():
        print(f"{name}: FWHM={model['fwhm_ms']:.6g} ms, RSS={model['rss_V2']:.6g} V^2")
        for message in model["warnings"]:
            print(f"  Review: {message}")


if __name__ == "__main__":
    main()
