"""Lab 05: reproduce four Gaussian fits in time units and audit assumptions.

AI-assisted refactor; see ../PROVENANCE.md. Difference features are not accepted
as calibrated atomic linewidths. Original instrument files are never modified.
"""
from __future__ import annotations

import argparse
import copy
import csv
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
PARAMETERS = ("amplitude_V", "center_ms", "fwhm_ms", "offset_V")


def check_xy(x, y, minimum=2):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or x.size < minimum:
        raise ValueError(f"Expected at least {minimum} paired one-dimensional samples.")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("Samples must be finite.")
    if not np.all(np.diff(x) > 0):
        raise ValueError("Times must be strictly increasing, with no duplicates.")
    return x, y


def check_window(window):
    w = np.asarray(window, dtype=float)
    if w.shape != (2,) or not np.all(np.isfinite(w)) or w[0] >= w[1]:
        raise ValueError("A window must contain two increasing finite bounds.")
    return w


def load_moku_csv(path):
    """Read all three columns, skipping percent comments; seconds become ms."""
    data = np.loadtxt(path, delimiter=",", comments="%", ndmin=2)
    if data.shape[1] != 3 or not np.all(np.isfinite(data)):
        raise ValueError("Expected three finite columns: time_s, channel_A_V, channel_B_V.")
    data[:, 0] *= 1000
    check_xy(data[:, 0], data[:, 1])
    return data


def interpolate_background(time_ms, background_time_ms, background_V):
    """Interpolate only within measured coverage; endpoint extrapolation is rejected."""
    t, _ = check_xy(time_ms, np.zeros_like(time_ms, dtype=float))
    bt, by = check_xy(background_time_ms, background_V)
    if t[0] < bt[0] or t[-1] > bt[-1]:
        raise ValueError("Background does not cover the requested times; extrapolation is disabled.")
    return np.interp(t, bt, by)


def select_dips(time_ms, signal_V, count=4):
    """Historical heuristic: deepest point in each equal sample-count segment.

    This does not identify atomic transitions. A minimum at a segment boundary
    is rejected because the selected feature would be ambiguous.
    """
    t, y = check_xy(time_ms, signal_V, minimum=10 * count)
    edges = np.linspace(0, len(t), count + 1, dtype=int)
    indices = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        k = lo + int(np.argmin(y[lo:hi]))
        if k in (lo, hi - 1):
            raise ValueError("A segment minimum is on its boundary; review the selection window.")
        indices.append(k)
    return indices


def gaussian(t, amplitude, center, fwhm, offset):
    return offset + amplitude * np.exp(-4 * np.log(2) * ((t - center) / fwhm) ** 2)


def fit_dip(time_ms, signal_V, guess_ms, halfwidth_ms):
    """Fit a negative Gaussian with a positive width and report residual diagnostics."""
    t, y = check_xy(time_ms, signal_V, minimum=10)
    if not np.isfinite(halfwidth_ms) or halfwidth_ms <= 0:
        raise ValueError("Fit half-width must be finite and positive.")
    if not np.isfinite(guess_ms):
        raise ValueError("The initial center must be finite.")
    if guess_ms - halfwidth_ms < t[0] or guess_ms + halfwidth_ms > t[-1]:
        raise ValueError("The complete fit window must be covered by the selected data.")
    mask = np.abs(t - guess_ms) <= halfwidth_ms
    tx, yy = check_xy(t[mask], y[mask], minimum=10)
    scale = float(np.ptp(yy))
    if scale <= 0:
        raise ValueError("A constant signal has no identifiable dip.")
    # Milliseconds and normalized voltage keep the optimizer well scaled.
    x, yn = tx - guess_ms, yy / scale
    offset = float(np.median(yn))
    p0 = [float(np.min(yn) - offset), 0, 2.354820045 * halfwidth_ms / 3, offset]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", OptimizeWarning)
        popt, covariance = curve_fit(
            gaussian, x, yn, p0=p0,
            bounds=([-np.inf, x[0], np.finfo(float).eps, -np.inf],
                    [0, x[-1], np.inf, np.inf]),
            maxfev=20000, ftol=1e-11, xtol=1e-11, gtol=1e-11,
        )
    transform = np.array([scale, 1, 1, scale])
    parameters = popt * transform
    parameters[1] += guess_ms
    errors = np.sqrt(np.maximum(np.diag(covariance), 0)) * transform
    model = gaussian(tx, *parameters)
    residual = yy - model
    center, width = parameters[1:3]
    covered = bool(tx[0] <= center - width / 2 and center + width / 2 <= tx[-1])
    notes = [str(item.message) for item in caught]
    if not covered:
        notes.append("Both fitted half-maximum positions are not covered by this window.")
    if not np.all(np.isfinite(covariance)):
        notes.append("The fitted covariance is not finite.")
    # A boundary solution can look successful while failing to identify a dip.
    if min(center - tx[0], tx[-1] - center) < 0.01 * np.ptp(tx):
        notes.append("The fitted center is close to a window boundary.")
    return {
        **dict(zip(PARAMETERS, map(float, parameters))),
        "conditional_standard_errors": dict(zip(PARAMETERS, [float(v) if np.isfinite(v) else None for v in errors])),
        "dip_guess_ms": float(guess_ms), "fit_interval_ms": [float(tx[0]), float(tx[-1])],
        "samples": int(len(tx)), "rmse_V": float(np.sqrt(np.mean(residual ** 2))),
        "rss_V2": float(np.dot(residual, residual)), "full_fwhm_covered": covered,
        "frequency_fwhm_MHz": None, "warnings": notes,
    }, (tx, yy, model, residual)


def transmission_diagnostic(time_ms, cell_V, bg_time_ms, bg_V, window_ms, scale):
    """Audit the historical voltage ratio without shifting or clamping it.

    Even a ratio in (0, 1) would require detector-zero and reference validation.
    Number density and pressure deliberately remain unavailable.
    """
    lo, hi = check_window(window_ms)
    mask = (time_ms >= lo) & (time_ms <= hi)
    t, y = check_xy(time_ms[mask], cell_V[mask], minimum=10)
    bg = interpolate_background(t, bg_time_ms, bg_V)
    k = int(np.argmin(y - scale * bg))
    baseline = float(np.percentile(y, 95))
    ratio = None if baseline == 0 else float(y[k] / baseline)
    valid = bool(ratio is not None and 0 < ratio < 1)
    return {
        "window_ms": [float(lo), float(hi)], "dip_time_ms": float(t[k]),
        "raw_dip_V": float(y[k]), "raw_95th_percentile_V": baseline,
        "raw_voltage_ratio": ratio, "ratio_in_physical_range": valid,
        "accepted_as_optical_transmission": False, "number_density_m3": None,
        "pressure_Pa": None,
        "reason": "Detector zero and an appropriate incident-intensity reference are unverified; no arbitrary voltage shift or ratio clamp is applied.",
    }


def analyze(config, project_root=PROJECT):
    paths = [Path(project_root) / config[k] for k in ("signal_file", "background_file")]
    cell, bg = [load_moku_csv(p) for p in paths]
    channels = {"A": 1, "B": 2}
    try:
        sc = channels[config["signal_channel"]]
        bc = channels[config["background_channel"]]
    except KeyError as error:
        raise ValueError("Channels must be A or B.") from error
    scale = float(config["background_scale"])
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError("Background scale must be finite and positive.")
    lo, hi = check_window(config["selection_window_ms"])
    mask = (cell[:, 0] >= lo) & (cell[:, 0] <= hi)
    t, raw = check_xy(cell[mask, 0], cell[mask, sc], minimum=40)
    interpolated = interpolate_background(t, bg[:, 0], bg[:, bc])
    difference = raw - scale * interpolated
    dips = select_dips(t, difference)
    fits, arrays, sensitivity = [], [], []
    for i, index in enumerate(dips, 1):
        fit, data = fit_dip(t, difference, t[index], config["fit_halfwidth_ms"])
        narrow, _ = fit_dip(t, difference, t[index], config["sensitivity_halfwidth_ms"])
        fit["feature"] = i
        fits.append(fit)
        arrays.append(data)
        sensitivity.append({"feature": i, "main_fwhm_ms": fit["fwhm_ms"],
                            "narrow_fwhm_ms": narrow["fwhm_ms"],
                            "change_percent": 100 * (narrow["fwhm_ms"] / fit["fwhm_ms"] - 1),
                            "narrow_fit": narrow})
    historic = config["historical_frequency_mapping"]
    duration = float(np.ptp(cell[:, 0]))
    legacy_scale = float(historic["frequency_span_GHz"]) * 1000 / duration
    ramp_lo, ramp_hi = check_window(config["ramp_check_window_ms"])
    ramp_mask = (cell[:, 0] >= ramp_lo) & (cell[:, 0] <= ramp_hi)
    rt, rv = check_xy(cell[ramp_mask, 0], cell[ramp_mask, 2], minimum=10)
    ramp_slope, ramp_intercept = np.polyfit(rt - rt[0], rv, 1)
    ramp_residual = rv - (ramp_slope * (rt - rt[0]) + ramp_intercept)
    summary = {
        "source": "Reanalysis of supplied Lab 05 measurements; not calibrated spectroscopy results.",
        "inputs": [{"name": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
        "config": copy.deepcopy(config), "fits": fits, "window_sensitivity": sensitivity,
        "transmission_review": transmission_diagnostic(cell[:, 0], cell[:, sc], bg[:, 0], bg[:, bc], config["transmission_window_ms"], scale),
        "calibration_review": {
            "accepted_MHz_per_ms": None, "recording_duration_ms": duration,
            "historical_MHz_per_ms": legacy_scale,
            "historical_mapping_fwhm_MHz": [f["fwhm_ms"] * legacy_scale for f in fits],
            "measured_ramp_V_per_ms": float(ramp_slope),
            "ramp_linear_fit_rmse_V": float(np.sqrt(np.mean(ramp_residual ** 2))),
            "background_coverage_ms": [float(bg[0, 0]), float(bg[-1, 0])],
            "historical_full_trace_points_outside_background": int(np.sum((cell[:, 0] < bg[0, 0]) | (cell[:, 0] > bg[-1, 0]))),
            "note": "The historical mapping stretches one assumed frequency span over a recording containing multiple triangular sweeps. Its MHz values are retained only for numerical comparison. The original tuning-curve source is missing.",
        },
        "uncertainty_note": "Fit errors are residual-scaled covariance estimates conditional on the chosen model and background. Correlated noise, background alignment, model mismatch and calibration uncertainty are not propagated.",
        "interpretation_note": "The background capture also contains structured dips. Fits describe the difference trace; the no-cell background designation and scan alignment need experimental confirmation before assigning atomic widths.",
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "matplotlib": matplotlib.__version__},
    }
    return {"summary": summary, "time_ms": t, "raw_V": raw, "background_V": scale * interpolated,
            "difference_V": difference, "fit_arrays": arrays, "full_cell": cell, "full_background": bg}


def write_outputs(result, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    summary = result["summary"]
    (destination / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    np.savetxt(destination / "selected-trace.csv", np.column_stack([result[k] for k in ("time_ms", "raw_V", "background_V", "difference_V")]),
               delimiter=",", header="time_ms,cell_V,scaled_background_V,difference_V", comments="", fmt="%.12g")
    with (destination / "fit-summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["feature", "center_ms", "fwhm_ms", "conditional_fwhm_stderr_ms", "rmse_V", "full_fwhm_covered"])
        for fit in summary["fits"]:
            writer.writerow([fit["feature"], fit["center_ms"], fit["fwhm_ms"], fit["conditional_standard_errors"]["fwhm_ms"], fit["rmse_V"], fit["full_fwhm_covered"]])
    for i, arrays in enumerate(result["fit_arrays"], 1):
        np.savetxt(destination / f"feature-{i}.csv", np.column_stack(arrays), delimiter=",",
                   header="time_ms,difference_V,fit_V,residual_V", comments="", fmt="%.12g")

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    colors = ["#1768AC", "#B35C1E", "#22836F", "#8256A8"]
    fig, axes = plt.subplots(4, 2, figsize=(12, 10), constrained_layout=True,
                             gridspec_kw={"height_ratios": [2, 1, 2, 1]})
    for i, (fit, arrays) in enumerate(zip(summary["fits"], result["fit_arrays"])):
        row, col = 2 * (i // 2), i % 2
        ax, res = axes[row, col], axes[row + 1, col]
        t, y, model, residual = arrays
        ax.plot(t, 1000 * y, color="#999999", linewidth=0.9, label="Difference trace")
        ax.plot(t, 1000 * model, color=colors[i], linewidth=2, label="Gaussian fit")
        ax.set(title=f"Feature {i+1}  |  FWHM {fit['fwhm_ms']:.3f} ms", ylabel="Difference (mV)")
        ax.legend(fontsize=8, loc="lower right")
        res.plot(t, 1000 * residual, color=colors[i], linewidth=0.8)
        res.axhline(0, color="#444444", linewidth=0.7)
        res.set(xlabel="Time (ms)", ylabel="Residual (mV)")
        ax.set_xlim(t[0], t[-1]); res.set_xlim(t[0], t[-1])
    fig.suptitle("Lab 05 · Four time-domain fits\nResidual structure limits the physical interpretation", fontsize=15)
    fig.savefig(destination / "four-feature-fits.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(3, 1, figsize=(11, 9), constrained_layout=True)
    cell, bg = result["full_cell"], result["full_background"]
    sc = 1 if summary["config"]["signal_channel"] == "A" else 2
    bc = 1 if summary["config"]["background_channel"] == "A" else 2
    axes[0].plot(cell[:, 0], cell[:, sc] * 1000, linewidth=0.7, label="Cell capture, Input 1")
    axes[0].plot(bg[:, 0], bg[:, bc] * summary["config"]["background_scale"] * 1000, linewidth=0.7, alpha=0.8, label="Background capture, Input 1")
    axes[0].axvspan(*summary["config"]["selection_window_ms"], color="#22836F", alpha=0.12, label="Selected sweep")
    axes[0].set(title="Original captures on their measured time ranges", ylabel="Voltage (mV)", xlabel="Time (ms)")
    axes[0].legend(fontsize=8, loc="lower right")
    axes[1].plot(result["time_ms"], result["difference_V"] * 1000, color="#34465B", linewidth=0.8)
    for i, fit in enumerate(summary["fits"]):
        axes[1].axvline(fit["dip_guess_ms"], color=colors[i], linestyle="--", alpha=0.8, label=f"Feature {i+1}")
    axes[1].set(title="Selected difference trace · background scale 1", xlabel="Time (ms)", ylabel="Difference (mV)")
    axes[1].legend(ncol=4, fontsize=8, loc="lower right")
    axes[2].plot(cell[:, 0], cell[:, 2], color="#1768AC", linewidth=1)
    axes[2].axvspan(*summary["config"]["selection_window_ms"], color="#22836F", alpha=0.12)
    axes[2].set(title="Cell capture Channel B is the repeated 10 Hz drive ramp", xlabel="Time (ms)", ylabel="Output 1 (V)")
    fig.savefig(destination / "trace-overview.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
    x = np.arange(1, 5)
    ax.plot(x, [s["main_fwhm_ms"] for s in summary["window_sensitivity"]], "o-", label=f"Original-equivalent ±{summary['config']['fit_halfwidth_ms']:.3f} ms")
    ax.plot(x, [s["narrow_fwhm_ms"] for s in summary["window_sensitivity"]], "s--", label=f"Sensitivity ±{summary['config']['sensitivity_halfwidth_ms']:.1f} ms")
    ax.set(xticks=x, xlabel="Feature number", ylabel="Fitted FWHM (ms)", title="Fit-window sensitivity · same data and Gaussian model")
    ax.legend()
    fig.savefig(destination / "window-sensitivity.png", dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=PROJECT / "config/analysis.json")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = analyze(json.loads(args.config.read_text(encoding="utf-8")))
        write_outputs(result, args.output_dir)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        parser.exit(1, f"Analysis could not complete: {error}\n")
    print(f"Saved Lab 05 analysis to {args.output_dir}")
    for fit in result["summary"]["fits"]:
        print(f"Feature {fit['feature']}: FWHM {fit['fwhm_ms']:.6f} ms")
    print("Frequency calibration, optical transmission, number density and pressure remain unverified.")


if __name__ == "__main__":
    main()
