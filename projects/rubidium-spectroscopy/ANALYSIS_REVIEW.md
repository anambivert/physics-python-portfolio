# Analysis review

This review distinguishes reproduced numerical output from a fully validated physical measurement.

## Frequency calibration

The archived notebook sets `alpha_MHz_per_ms = 33609`. Multiplying its fitted widths by that value produces approximately **28.4 and 28.9 GHz**. The supplied files do not contain the etalon calibration that would justify treating this number as MHz/ms.

The selected signal and background settings specify a **90 mV peak-to-peak**, **10 Hz**, **50% symmetry** ramp. A half-period is 50 ms, giving a nominal ramp magnitude of:

```text
|dV/dt| = 0.090 V / 50 ms = 0.0018 V/ms
dν/dt = (dν/dV) × (dV/dt)
```

A linear fit to Channel B, identified in the headers as Output 1, over 130–160 ms gives about **−0.00180001 V/ms** for the signal capture. This supports the nominal ramp rate.

**Conditional dimensional check:** if the historical number 33609 actually represents MHz/V, and if that coefficient applies to this drive path and operating point, the corresponding rate would be **60.4962 MHz/ms**. The two widths would then be about **51.13 and 52.06 MHz**. These are conditional calculations, not accepted corrections. The original calibration, its voltage definition, applicability, and uncertainty are still required.

For context, the rubidium-85 D2 natural linewidth in ordinary frequency units is approximately 6.07 MHz; an observed saturated-absorption feature need not equal the natural linewidth. This reference scale motivates checking the conversion, not replacing it by an expected answer. [Steck, Rubidium 85 D Line Data, Table 3](https://steck.us/alkalidata/rubidium85numbers.pdf).

The portable configuration therefore defaults to a null calibration. A supplied slope must be finite, non-zero, expressed in MHz/ms, and accompanied by a source description. A supplied value is recorded as user-provided, not independently verified.

## Fit-window coverage

The original fit spans **146.0–147.5 ms**. The Lorentzian centre is about **147.320 ms**, with a fitted FWHM of **0.8605 ms**. Its right half-maximum position is about **147.750 ms**, outside the selected interval. The Gaussian has the same coverage problem.

The width is a fitted model parameter, not a direct measurement between two observed half-maximum crossings. Expanding the window requires checking adjacent spectral features. The refactor flags this condition automatically and preserves the original selection so the archived result can be reproduced.

## Model comparison and uncertainty

Both models have four fitted parameters and use the same data, so their RSS values can be compared directly. Lower RSS here is not proof of a pure physical line shape; baseline structure, neighbouring features, correlated noise, or a restricted window can influence it.

Approximate standard errors from fit covariance are included in the JSON output. They are conditional on the chosen model and background and do not propagate background-fit uncertainty, calibration uncertainty, systematic errors, or noise correlations. SciPy explains the local-linear and residual-scaling assumptions behind this covariance. [SciPy curve_fit documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html).

The refactor also disables background extrapolation and constrains widths to be positive. These implementation changes are recorded in [provenance](PROVENANCE.md).
