# Gaussian Beam Analysis

**Status:** lab-work summary; original source, profiles, and result figures pending import.

## Physics question

How does a laser beam's transverse intensity profile change with focusing, propagation distance, and a beam expander?

## Work to showcase

My lab workflow used Gaussian fits to intensity profiles to extract beam widths, compare profiles at different propagation distances, and evaluate the change in width before and after a beam expander.

The portfolio version will connect the fitted profiles to the physical beam parameters, with explicit units and any pixel-to-distance calibration.

## Python methods

- NumPy arrays for profile data.
- SciPy nonlinear curve fitting.
- Matplotlib comparisons of measurements and fitted profiles.
- Parameter extraction and calculations for beam width and expansion ratio.

## Original inputs

Locate the original scripts and profile exports, including `Before.txt`, `After.txt`, and the profiles measured at different lens settings and propagation distances.

Put the original scripts in `src/` or `notebooks/`. Document the input format and profile-position units in [data/sample/README.md](data/sample/README.md).

## Planned portfolio outputs

| Output | What it should explain |
| --- | --- |
| Measured profile and fitted curve | How well the Gaussian model describes the data |
| Residual plot | Systematic deviations from the fit |
| Beam-width table | Width convention, units, and fit uncertainty |
| Before/after comparison | Expansion ratio and its interpretation |

## Reproduction and results

No analysis program or measurement result is included yet. After importing the original files, add the exact run instructions, dependencies, representative figure, and measured result here.

## Authorship

The summary reflects Siddharth Prajapati's lab workflow. This documentation was prepared with AI assistance. Record the provenance of original scripts, data, and any collaborators during import.
