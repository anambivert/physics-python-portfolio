# Provenance and authorship

Siddharth Prajapati supplied the Lab 02 notebook, report, four Excel workbooks and 14 PNG images for this portfolio. Their original hashes and repository paths are recorded in [data/manifest.json](data/manifest.json).

## Original material

- **Workbooks, PNG images and report:** preserved byte for byte. The report remains a historical document, including its original numerical conclusions and layout.
- **Archived notebook:** original numerical code, execution counts and cached numerical outputs are retained. Windows-specific input/output paths were replaced with relative paths, and an opening note explains that the original TXT inputs are missing. This is an adapted archive, not a newly executed notebook.
- **Historical summary:** the cached console results are transcribed into [results/archived](results/archived/README.md). The propagation figure was extracted without replotting from `word/media/image9.png` in the original report.
- **Original code authorship:** the supplied Lab 02 files do not state who wrote the code or whether AI assistance was used. No independent-authorship claim is made.

## Portfolio additions

The command-line refactor, runnable notebook, tests, data manifest, review and documentation were prepared with AI assistance. The new script reads the four XLSX profiles, fits positive-width Gaussians, compares free and zero backgrounds, records residuals and source hashes, and flags possible clipping and incomplete radius coverage.

Fresh output lives under `results/reproduced/`. Despite the folder name, it reproduces the **new XLSX workflow**, not the original notebook's unavailable TXT-based results. No numeric data were fabricated or extracted from the screenshots. The Python tests use explicitly synthetic profiles only to test numerical recovery.

## Validation

The four-profile analysis was executed on Python 3.12.14 with the dependencies pinned in `requirements.txt`. Ten tests cover model conventions, noisy narrow/broad recovery, coordinate scaling, zero-baseline fitting, invalid input rejection, missing files, exact Excel row counts, clipping/coverage diagnostics, ratio uncertainty and the full workflow on the uploaded data. Figures and the original report were visually reviewed.

The new notebook wraps the tested command-line functions. Its cells passed Python syntax checks; a Jupyter kernel run was not performed because Jupyter/IPython were not installed in the preparation environment. Install JupyterLab as described in the README to run it.
