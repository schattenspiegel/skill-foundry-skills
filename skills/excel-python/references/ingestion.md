# Tabular ingestion

Use Polars with its installed Calamine/fastexcel engine for `.xlsx`, `.xlsb`, or
`.xls` table extraction when workbook structure is not itself the subject.
Prefer `table_name=` for a named Excel Table; otherwise declare sheet, header,
range/columns, schema overrides, empty-row policy, and row grain.

Do not treat a visually rectangular region as a stable table without checking
merged headers, subtotal rows, repeated headings, footnotes, hidden rows, units,
formula versus cached values, and identifier types. Preserve 16+ digit IDs as
text with a schema override rather than accepting numeric inference.

Once the task needs joins, aggregation, reshaping, dtypes, missing-value rules,
ordering, lazy execution, or analytical validation, load `polars-python` and let
it own those decisions. Return to this skill for the workbook delivery contract.
