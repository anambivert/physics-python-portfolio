# Provenance and changes

## Supplied material

Siddharth Prajapati supplied `Code for Lab 5 (1).ipynb`, `Lab 5- Rubidium Atom.docx` and `lab 5-20251201T203601Z-1-001.zip`. The ZIP contains 25 instrument files from 29 October 2025. Every member is included unchanged under `data/measurements/`; the ZIP container is not duplicated. `data/manifest.json` records its digest and each member's SHA-256 hash.

The report explicitly credits ChatGPT 5.1 Extended Thinking with generating the original code. This portfolio presents AI-assisted experimental analysis and does not claim the supplied implementation was independently written. The original Word report is byte-identical. `provenance.json` records notebook and report hashes.

## Archived notebook

The two Windows input paths were changed to paths relative to the notebook folder, and a markdown introduction explains the archive and review. Numerical logic, cached text, three cached PNGs, execution counts and original environment metadata were retained. `figures/archived/` contains the exact cached PNG bytes.

The two original nonempty code cells were executed sequentially under Python with local input paths and a headless plotting backend. Their rounded printed results reproduce the uploaded outputs, including the historical transmission shift. The new stdout files and numerical record are under `results/archived/`; cached notebook outputs were not overwritten. No Jupyter kernel execution is claimed.

## Portable refactor

The AI-assisted portfolio additions were prepared in September 2026. They preserve the original channel selection, background scale, four-segment feature selection and equivalent fit windows while adding:

- A configuration file, relative paths and a command-line interface.
- Finite-data, monotonic-time, column-count, fit-window and interpolation-coverage validation.
- Negative-amplitude and positive-width constraints, normalized voltage and tighter optimization tolerances.
- Fits in milliseconds, residual plots, conditional covariance errors and half-maximum coverage checks.
- A narrower-window sensitivity calculation on the same measured difference trace.
- An explicit audit of the frequency mapping and invalid transmission ratio.
- Input hashes, environment versions and machine-readable outputs.

The refactor does not apply the historical voltage repair or adopt its physical outputs. Original figures and fresh results remain distinguishable.

## Validation

Ten numerical tests passed under Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and Matplotlib 3.10.8. Synthetic test data are generated only within the tests. The full workflow was also run on the original CSV pair; the time widths differ by less than 0.01% from the original calculation because of the optimizer changes. All three new figures and all five rendered pages of the original report were visually reviewed. The report remains an unmodified archival artifact.

The new analysis notebook's code cells were executed sequentially as ordinary Python, including loading the resulting PNGs. This validates its code path and dependencies without claiming a Jupyter kernel or browser rendering test. Its display cells use Pillow, which is installed with Matplotlib.

No measurements were fabricated or reconstructed from screenshots. The other supplied captures and workbook remain available for future analysis; they were not silently substituted into the selected workflow.
