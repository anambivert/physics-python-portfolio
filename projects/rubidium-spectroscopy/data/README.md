# Lab 6 measurement data

All 20 supplied files are preserved byte-for-byte in [measurements/](measurements/). File sizes and SHA-256 digests are recorded in [manifest.json](manifest.json).

| Capture on 2025-11-12 | Role in this project | Output 1 settings |
| --- | --- | --- |
| 15:36:45 | Additional overview capture; not used in the original single-feature fit | 10 Hz, 1.200 Vpp |
| 17:16:38 filename | Signal selected by the original notebook | 10 Hz, 90.0 mVpp |
| 17:21:48 | Background selected by the original notebook | 10 Hz, 90.0 mVpp |
| 17:29:19 | Additional capture; not analysed here | 10 Hz, 53.0 mVpp |
| 17:30:10 | Additional capture; not analysed here | 10 Hz, 53.0 mVpp |

The signal file's acquisition header records 17:16:39, one second later than its filename. The original filename is retained.

Each capture includes a `HighRes.csv`, `Traces.csv`, `Settings.txt`, and `Screenshot.png`.

## High-resolution CSV format

There are ten metadata/comment lines followed by three numeric columns:

| Column | Meaning | Unit |
| --- | --- | --- |
| 1 | Time | seconds |
| 2 | Channel A, Input 1 | volts |
| 3 | Channel B, Output 1 | volts |

Each high-resolution file contains 16,320 samples. [captures.json](captures.json) records time coverage. The signal and background have different sampling intervals, so the background is interpolated to the signal time grid.

The current configuration uses Channel A and converts time from seconds to milliseconds. The raw files are unchanged. Screenshots and settings provide acquisition context; plots for fitting are generated from CSV values, not digitized from screenshots.

For future unpublished working files, `raw/` remains ignored by Git. These deliberately included measurement files use `measurements/` so a fresh checkout can reproduce the project.
