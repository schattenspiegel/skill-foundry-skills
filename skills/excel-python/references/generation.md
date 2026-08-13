# Generation

Use XlsxWriter for a new workbook whose contract includes formatting, formulas,
Tables, charts, validations, names, or print settings. Use Polars
`DataFrame.write_excel` when a DataFrame is already the semantic owner and the
required output fits its installed XlsxWriter-backed API; pass an open
XlsxWriter workbook when adding several tables or presentation elements.

Before writing, define sheet roles, stable Table/name interfaces, row grain,
keys, units, type/blank policy, formulas, editable cells, chart sources,
presentation requirements, provenance, and output-size limits. Reject invalid
sheet/Table/name collisions before creating the file.

Create into a temporary sibling path. Centralize formats and write rows in
deterministic order. Close the workbook successfully before moving it to the
destination. Never use `constant_memory` when the contract needs Tables or
merged ranges.

Reopen with an independent reader and assert the workbook contract. Inspect the
OOXML package and formula text, not only displayed values. A generated workbook
with formulas has not been recalculated merely because it reopens. Render or
manually inspect representative sheets when visual usability is part of done.
