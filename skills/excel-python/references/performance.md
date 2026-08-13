# Performance and Excel limits

Fail before a worksheet exceeds 1,048,576 rows or 16,384 columns. Do not split a
giant analytical dataset across sheets by default; keep detail in
Parquet/DuckDB/Polars and deliver a bounded Excel summary or extract contract.

Choose the mode from required features:

- Polars/Calamine is the default fast path for rectangular data extraction when
  installed; it does not replace OOXML inspection.
- openpyxl normal mode supports object inspection but can use many times the
  file size in memory. Read-only mode is for bounded value streaming and omits
  normal charts/images/object APIs. Write-only mode has a restricted creation
  API and is not an existing-workbook editor.
- XlsxWriter `constant_memory` requires sequential row writes. `add_table()` and
  `merge_range()` do not work in that mode. Choose Table/presentation features
  before enabling it.

For large workbooks, bound value sampling and emitted JSON details while still
computing complete counts/digests where practical. Do not claim a performance
improvement without measuring representative inputs and the actual installed
versions.
