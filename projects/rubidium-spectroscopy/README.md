# Doppler-Free Rubidium Spectroscopy

**Lab 6 · York University · Siddharth Prajapati**

A reproducible analysis of a selected saturated-absorption feature: load oscilloscope exports, remove a fitted background, compare Gaussian and Lorentzian models, and inspect the residuals.

**Status:** original notebook, report, and all 20 supplied instrument exports are included. The portable analysis has been run on the original signal/background files. Time-domain fit results are reproduced; frequency calibration remains under review.

![Gaussian and Lorentzian fits with residuals](results/reproduced/fit-comparison.png)

## What the project demonstrates

- Importing instrument data and interpreting its time and voltage units.
- Interpolating a separate background trace and estimating its scale and offset.
- Fitting two nonlinear models to the same selected feature.
- Checking residuals, parameter uncertainty, and whether the measurement window covers the fitted width.
- Producing figures, machine-readable results, and reproducible run instructions.

The original report explicitly credits ChatGPT 5.1 Extended Thinking with generating the notebook code. This portfolio documents **AI-assisted experimental analysis**. The portable refactor and tests were also prepared with AI assistance; see [provenance](PROVENANCE.md).

## Reproduced results

The selected interval is **146.0–147.5 ms**, within a **130–160 ms** trace window. The background regression excludes **145–150 ms**.

| Model | Centre (ms) | Fitted FWHM (ms) | Residual sum of squares (V²) |
| --- | ---: | ---: | ---: |
| Gaussian | 147.3439 | 0.845233 | 0.0000610512 |
| Lorentzian | 147.3200 | 0.860503 | 0.0000367821 |

The background scale is **1.036030**, with an offset of **0.093431 V**. The results agree with the saved notebook at its reported precision.

The Lorentzian has lower RSS for this window. That comparison alone does not establish the physical line shape. Both fitted half-maximum intervals extend beyond the right edge of the data window, so their widths depend partly on extrapolation. See [the analysis review](ANALYSIS_REVIEW.md).

**The historical 28,407–28,921 MHz linewidths are not accepted as calibrated results.** The new run reports widths in milliseconds until the frequency-to-voltage calibration is supported by its source.

## Browse the work

| Item | Contents |
| --- | --- |
| [Portable analysis](src/analyze.py) | Functions and command-line entry point |
| [Archived notebook](notebooks/lab6-archived.ipynb) | Original numerical code and cached outputs, with path edits and explanatory notes |
| [Original report](reports/lab6-original-report.pdf) | Unmodified uploaded PDF, including its original conclusions |
| [Measurements](data/measurements/) | Five captures: high-resolution CSV, trace CSV, settings, and screenshot for each |
| [Input guide](data/README.md) | Capture roles, format, units, and source hashes |
| [Run configuration](config/analysis.json) | File paths, windows, channel, and optional calibration |
| [Reproduced outputs](results/reproduced/) | Background correction, fit/residual plot, CSV, and complete fit metadata |
| [Numerical checks](tests/test_analysis.py) | Ten tests using labelled synthetic inputs |
| [Calibration review](results/calibration-review.json) | Ramp slope calculations and a conditional dimensional check |

## Run

From the repository root, install the project's tested dependency versions in a virtual environment, then run:

```bash
python -m pip install -r projects/rubidium-spectroscopy/requirements.txt
python projects/rubidium-spectroscopy/src/analyze.py --output-dir runs/lab6
```

On Windows, use `py` in place of `python` if appropriate. [Environment setup](../../docs/ENVIRONMENT.md) explains virtual environments.

Outputs are `summary.json`, `background-subtracted.csv`, `background.png`, and `fit-comparison.png`. Running again into the same output folder replaces those generated files. The checked-in comparison figures remain in `results/reproduced/`.

The default configuration reads the two full high-resolution measurements included in this repository. It does not require downloading external data. For different inputs, edit the configuration or supply `--config path/to/config.json`; relative input paths are resolved from this project folder.

## Validation

```bash
python -m unittest discover -s projects/rubidium-spectroscopy/tests -v
```

Validated on Python 3.12.14 with NumPy 2.3.5, SciPy 1.17.0, and Matplotlib 3.10.8. Ten tests passed, covering model widths, positive and negative features, interpolation, input validation, missing data, calibration handling, and file outputs. The experimental rerun additionally reproduced the archived fit values.

## Next improvements

Resolve the original etalon calibration, assess a fit window covering both sides of the feature without blending adjacent peaks, test the background exclusion region, and propagate calibration and background uncertainty. The remaining captures are archived for future analysis; they have not been assigned new spectral-transition identities.
