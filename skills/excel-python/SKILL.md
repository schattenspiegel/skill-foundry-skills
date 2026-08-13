---
name: excel-python
description: >-
  Use for writing, reviewing, debugging, or testing Python code that inspects,
  edits, extracts, validates, or generates Excel .xlsx or .xlsm workbooks with
  openpyxl or XlsxWriter. Trigger on formulas and cached values, tables, named
  ranges, charts, styles, hidden sheets, external links, macro preservation,
  and workbook verification. Do not use for CSV-only work, Excel UI automation,
  macro execution, or dataframe calculations with no workbook boundary.
argument-hint: "[workbook task, preservation requirements, and output contract]"
---

# Excel workbook boundaries

Inspect the installed version of openpyxl and XlsxWriter and the exact APIs before
relying on version-sensitive preservation, chart, table, or formula behavior.

Choose the library from the operation:

| Intent | Use | Critical limit |
|---|---|---|
| Inspect or carefully edit an existing workbook | openpyxl | It does not recalculate formulas and cannot preserve every Excel feature. |
| Create a new presentation-quality workbook | XlsxWriter | It cannot read or modify an existing workbook. |
| Preserve `.xlsm` while editing supported content | openpyxl with `keep_vba=True` | VBA is preserved, not executed or edited. |

## Workflow

1. Preserve the original. Resolve `.xlsx` versus `.xlsm`, required Excel-only
   features, external links, formulas, macros, expected calculation layer, and
   output destination before loading.
2. For inspection, open formula text normally and cached results separately
   with `data_only=True` only when stored values matter. Cached values are the
   last values written by a spreadsheet application; they are not a Python
   recalculation.
3. Inventory visible/hidden sheets, used ranges, tables, names, merged cells,
   formulas, charts, validations, comments when relevant, and external links.
4. When editing, change the smallest supported region. Never overwrite the
   source by default. For macro-enabled files preserve the extension and load
   with `keep_vba=True`.
5. When generating, define sheet roles, table/range contracts, units, formats,
   freeze panes, filters, formulas, charts, methodology, and validation before
   writing. Use Excel Tables where review and filtering benefit.
6. Write to a temporary destination, close successfully, move into place, then
   reopen and verify sheet, table, formula, chart, name, and value inventories.

## Invariants

- Never claim formulas were recalculated unless a real spreadsheet calculation
  engine ran and its saved results were reread.
- Do not execute macros or refresh external connections.
- Saving with openpyxl can lose unsupported features such as shapes. If the
  workbook contains a feature that must survive and preservation is unverified,
  stop or use an Excel-native automation path with explicit authority.
- XlsxWriter `constant_memory` requires sequential row writes and is
  incompatible with features such as tables; choose memory mode after defining
  the required workbook features.
- Formula text and stored result are different evidence. Inspect both when
  detecting overrides, stale caches, or formula deviations.

## Canonical new workbook

```python
import xlsxwriter

with xlsxwriter.Workbook("output.xlsx") as workbook:
    sheet = workbook.add_worksheet("Summary")
    percent = workbook.add_format({"num_format": "0.0%"})
    sheet.write_row("A1", ["Segment", "Rate"])
    sheet.write_row("A2", ["Core", 0.124], percent)
    sheet.add_table(
        "A1:B2",
        {
            "name": "SummaryTable",
            "columns": [
                {"header": "Segment"},
                {"header": "Rate"},
            ],
        },
    )
    sheet.freeze_panes(1, 0)
```

After creation, reopen with openpyxl and assert the expected sheets, table
range, formats, formulas, and chart count. Read [inspection and preservation](references/inspection.md),
[generation and verification](references/generation.md), and [formula discipline](references/formulas.md).
