# Data inventory

The upload contains four numeric XLSX profiles and 14 PNG visual records. Each workbook has one worksheet, one numeric column, no header, no formulas, and one intensity value per row. Row one is a real sample. The analysis assigns positions 0 through N−1 and uses every row.

| File | Rows | Use |
| --- | ---: | --- |
| `measurements/beforeexpander.xlsx` | 2,038 | Before-expander profile |
| `measurements/expander.xlsx` | 2,037 | Expanded profile, with possible clipping |
| `measurements/focallength10.xlsx` | 1,021 | Lens profile identified by filename |
| `measurements/focallength20.xlsx` | 2,035 | Lens profile identified by filename |

[Browse all 14 images](GALLERY.md). The images are presentation screenshots, with line overlays or graph axes; they are not substitutes for unannotated camera frames or numerical exports. The propagation-distance mapping was not supplied.

The [manifest](manifest.json) lists all 20 source attachments, original SHA-256 hashes, repository paths, and any changes. The four workbooks, 14 PNGs and report are byte-identical copies. The notebook has documented path sanitization and an added archive note.

## Missing inputs referenced by the notebook

- `25.txt`, `50.txt`, `75.txt`, `100.txt`, `125.txt`, `150.txt`, `175.txt`, `200.txt`
- `25.4mm.txt`, `100mm.txt`, `200mm.txt`
- `Before.txt`, `After.txt`

These files are not reconstructed from screenshots. Cached results from them are recorded under [results/archived](../results/archived/README.md). The reproducible new calculations use the XLSX files above.
