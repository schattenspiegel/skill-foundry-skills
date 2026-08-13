# Library selection

| Intent | Default | Boundary |
|---|---|---|
| Read an Excel Table or rectangular sheet as data | Polars `read_excel`, Calamine engine | Use when workbook structure is not the subject; inspect installed Polars/fastexcel. |
| Join, aggregate, reshape, type, clean, or lazily compute table data | `polars-python` | That skill owns dataframe semantics even when Excel is the source or destination. |
| Inspect or minimally edit supported content in an existing `.xlsx`/`.xlsm` | openpyxl | It does not calculate and cannot preserve every OOXML feature. |
| Inspect package preservation risk | standard-library ZIP/XML plus openpyxl | Inventory is evidence, not a preservation guarantee. |
| Create a presentation-quality workbook | XlsxWriter | It cannot read or modify an existing workbook. |
| Write an owned Polars DataFrame as a formatted Excel Table | Polars `write_excel` | XlsxWriter-backed; Excel delivery returns to this skill's contract and verification. |
| Recalculate, refresh, run VBA, use unsupported objects, or export natively | installed Excel runtime | Out of scope; require explicit authority and separate verification. |

Do not convert an existing workbook to a DataFrame and recreate it merely to
change a cell. Do not use openpyxl as a general analytics engine. Do not
introduce Polars solely because a small workbook exists when the project has a
simpler established data path.
