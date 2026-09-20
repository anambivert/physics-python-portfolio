# Import existing lab work

Start with the files that produced the original analysis. A project is ready to showcase when a reader can identify the question, inspect the code, and understand at least one result.

## Files to locate

Lab 02 and Lab 06 are already included with their uploaded source files. The filenames below identify additional material that would extend or complete the archive; they are search clues, not files already present.

| Project | Useful original material |
| --- | --- |
| Gaussian beam analysis | The 13 TXT inputs referenced by the archived notebook: `25.4mm.txt`, `100mm.txt`, `200mm.txt`; propagation profiles `25.txt` through `200.txt`; `Before.txt` and `After.txt`. Notebook, report, four XLSX profiles and 14 images are already included. |
| Rubidium spectroscopy | Background-subtraction and fitting scripts; `MokuOscilloscopeData_20251029_144859_HighRes.csv`; `back100offset10hz_20251029_150846_HighRes.csv`; any etalon and narrow-feature traces |
| CMOS image analysis | Original image-analysis script; `cameraTestFile.bmp`; `measurements.xlsx`; saved ROI/profile figures |
| Computational physics | Original notebooks or scripts for FFTs, spectra, nonlinear roots, ODEs, or Monte Carlo methods |

## Where files go

| Folder inside a project | Contents |
| --- | --- |
| `src/` | Python scripts and reusable functions |
| `notebooks/` | Jupyter notebooks |
| `data/raw/` | Full instrument files kept locally by default |
| `data/sample/` | Small, documented datasets committed for reproduction |
| `data/measurements/` | Deliberately shared original inputs used by the included labs |
| `figures/` | Selected figures used in the README |
| `results/` | Compact output tables or summaries |

The Git ignore rules keep files inside `data/raw/` out of normal Git commits. For a reproducible public example, deliberately select suitable inputs for `data/sample/` and document how they relate to the original measurements.

## Prepare the first project

1. Import the original script or notebook and identify its author and any collaborators.
2. Replace computer-specific paths with paths relative to the project. For a script directly inside `src/`, `Path(__file__).resolve().parents[1]` locates the project folder.
3. State the input format, columns, units, and any calibration values with their source.
4. Run the analysis using the documented inputs; inspect the fit, residuals, units, and outputs.
5. Save one informative figure and a short explanation of the actual result.
6. Update both the project README and the root project index from “source pending” to an accurate status.

Keep the initial imported version in Git history before refactoring. Describe later changes separately. Include material you authored or have permission to share, and remove personal paths or identifiers from notebook outputs and report pages.

If an input is unavailable, state that limitation. Any synthetic demonstration added later should identify its data as synthetic.
