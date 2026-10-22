# Lab 05 inputs

All **25** files extracted from the supplied ZIP are included unchanged in [measurements](measurements/): **12 CSVs, 6 settings files, 6 screenshots and 1 workbook**. [manifest.json](manifest.json) records SHA-256 hashes and original ZIP member paths.

## Inputs used by the portable workflow

| Role | File | Selected channel | Instrument source |
| --- | --- | --- | --- |
| Cell capture | `MokuOscilloscopeData_20251029_144859_HighRes.csv` | A | Input 1 |
| Background, as designated by the notebook | `back100offset10hz_20251029_150846_HighRes.csv` | B | Input 1 |
| Ramp check | Same cell capture | B | Output 1 |

Both selected CSVs contain **16,320 rows** after ten percent-prefixed metadata lines. Their numeric columns are time in seconds, Channel A in volts and Channel B in volts. The script skips percent comments and converts time to milliseconds. The header channel mappings matter: the background file's A/B mappings differ from the cell file's.

Both selected captures use a 10 Hz, 1 Vpp ramp with −100 mV offset according to their headers. The capture named as background also contains structured dips. Its no-cell designation and alignment need experimental confirmation; see [the review](../ANALYSIS_REVIEW.md).

The XLSX is archived as supplied. Its first rows include instrument metadata and its numeric table starts at row 11; it is not a second input to the workflow. The remaining 10 Hz and 100 Hz captures preserve changes in drive offset and instrument routing for future study. File labels alone do not establish atomic-transition identities.

## Complete inventory

| Original filename | Bytes |
| --- | ---: |
| `0 offset 100hz data.csv` | 914,405 |
| `0 offset 100hz.csv` | 50,714 |
| `0 offset 100hz.png` | 105,991 |
| `0 offset 100hz.txt` | 665 |
| `0 offset 10hz.csv` | 907,428 |
| `0 offset 10hz.png` | 101,937 |
| `0 offset 10hz.txt` | 664 |
| `210offset100hz_20251029_145836_HighRes.csv` | 917,101 |
| `210offset100hz_20251029_145836_Screenshot.png` | 105,962 |
| `210offset100hz_20251029_145836_Settings.txt` | 665 |
| `210offset100hz_20251029_145836_Traces.csv` | 50,932 |
| `back100offset10hz_20251029_150846_HighRes.csv` | 895,973 |
| `back100offset10hz_20251029_150846_Screenshot.png` | 105,579 |
| `back100offset10hz_20251029_150846_Settings.txt` | 684 |
| `back100offset10hz_20251029_150846_Traces.csv` | 49,802 |
| `back210offset100hz_20251029_150607_HighRes.csv` | 897,903 |
| `back210offset100hz_20251029_150607_Screenshot.png` | 107,153 |
| `back210offset100hz_20251029_150607_Settings.txt` | 685 |
| `back210offset100hz_20251029_150607_Traces.csv` | 49,894 |
| `MokuOscilloscopeData_20251029_144859_HighRes.csv` | 907,870 |
| `MokuOscilloscopeData_20251029_144859_HighRes.xlsx` | 358,720 |
| `MokuOscilloscopeData_20251029_144859_Screenshot.png` | 102,821 |
| `MokuOscilloscopeData_20251029_144859_Settings.txt` | 664 |
| `Rubidium 0 offset.csv` | 50,420 |
| `Rubidium off 100mv.csv` | 50,445 |

The original notebook and Word report are under `../notebooks/` and `../reports/`. All inputs required for the portable analysis are present. The original etalon calibration source, independently measured detector zero and verified optical reference are not supplied.
