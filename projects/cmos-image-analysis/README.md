# CMOS Image Analysis

**Status:** lab-work summary; original image-analysis code, images, and results pending import.

## Physics question

How can pixel values from a CMOS image be used to study intensity profiles and quantify light detected in a selected region?

## Work to showcase

My lab workflow involved loading camera images as numerical arrays, inspecting row and column profiles, selecting regions of interest, and applying background corrections. The wider analysis related image counts to detector response using the relevant calibration information.

## Python methods

- Pillow for image loading.
- NumPy for image arrays, slicing, and regional sums.
- Matplotlib for image and profile visualization.
- Calculations using detector gain, exposure, and quantum efficiency when supported by the measurement setup.

## Original inputs

Locate the original image-analysis script, `cameraTestFile.bmp`, relevant camera images, and `measurements.xlsx`.

Document image dimensions, pixel format or bit depth, ROI coordinates, background selection, and exposure information. Any conversion from counts to physical quantities needs the applicable detector calibration and units.

## Planned portfolio outputs

| Output | What it should explain |
| --- | --- |
| Image with the ROI identified | Which pixels are used in the calculation |
| Row and column profiles | Spatial intensity structure |
| Background-corrected summary | How the background affects the measurement |
| Calibrated result, if supported | Conversion assumptions and uncertainty |

## Reproduction and results

No executable analysis or measured result is included yet. Add the original inputs and code before presenting ROI totals or calibrated physical quantities.

## Authorship

The summary reflects Siddharth Prajapati's lab workflow. This documentation was prepared with AI assistance. Record the sources of the script, images, measurement tables, and any shared lab work during import.
