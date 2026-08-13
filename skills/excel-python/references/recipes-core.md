# Evaluated core recipes

## Recipe `excel.safe-text-export`
**Use when:** exporting externally sourced fields that are semantically text.
**Inspect first:** text/formula/hyperlink contract and required literal value.
**Invariants:** no implicit formula or URL conversion; identifiers remain exact.
```python
import xlsxwriter

with xlsxwriter.Workbook(
    "output.xlsx",
    {"strings_to_formulas": False, "strings_to_urls": False},
) as workbook:
    sheet = workbook.add_worksheet("Data")
    sheet.write_string("A1", "customer_input")
    sheet.write_string("A2", "=2+2")
    sheet.write_string("A3", "001234567890123456")
```
**Do not use when:** the field is an explicitly authorized formula or hyperlink.
**Verify:** reopen and assert all target cells have text data type and exact value.

## Recipe `excel.preservation-preflight`
**Use when:** a valuable existing `.xlsx` or `.xlsm` may be edited.
**Inspect first:** required preserved features and output extension.
**Invariants:** source remains unchanged; unknown required parts block save.
```python
import json
import subprocess
import sys

completed = subprocess.run(
    [sys.executable, "scripts/inspect_workbook.py", "input.xlsm"],
    check=True,
    capture_output=True,
    text=True,
)
report = json.loads(completed.stdout)
if report["preservation"]["requires_escalation"]:
    raise RuntimeError("Workbook contains unsupported or unknown preservation risk")
```
**Do not use when:** no existing workbook is being round-tripped.
**Verify:** save to a new path and run the semantic diff before delivery.

## Recipe `excel.copied-formula-audit`
**Use when:** checking a formula-owned row or column for overrides or drift.
**Inspect first:** contract range, intentional exceptions, and formula/cache views.
**Invariants:** compare relative patterns; do not rewrite deviations automatically.
```python
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator

workbook = load_workbook("model.xlsx", data_only=False)
sheet = workbook["Model"]
anchor = sheet["F2"].value
for row in range(3, sheet.max_row + 1):
    expected = Translator(anchor, origin="F2").translate_formula(f"F{row}")
    if sheet[f"F{row}"].value != expected:
        print(f"F{row}: formula deviation")
```
**Do not use when:** the region has no declared copied-formula contract.
**Verify:** inspect each deviation against neighboring formulas and exceptions.

## Recipe `excel.verified-report-generation`
**Use when:** generating a new reviewable tabular workbook.
**Inspect first:** workbook contract, row/column limits, types, and presentation.
**Invariants:** named Table, explicit formats, safe text, close then reopen.
```python
import xlsxwriter
from openpyxl import load_workbook

with xlsxwriter.Workbook("report.xlsx", {"strings_to_formulas": False}) as wb:
    ws = wb.add_worksheet("Summary")
    ws.write_row("A1", ["Segment", "Rate"])
    ws.write_string("A2", "Core")
    ws.write_number("B2", 0.124, wb.add_format({"num_format": "0.0%"}))
    ws.add_table("A1:B2", {"name": "SummaryTable", "columns": [
        {"header": "Segment"}, {"header": "Rate"},
    ]})
    ws.freeze_panes(1, 0)

check = load_workbook("report.xlsx", data_only=False)
assert check["Summary"].tables["SummaryTable"].ref == "A1:B2"
```
**Do not use when:** an existing workbook must be preserved or output exceeds limits.
**Verify:** run contract assertions and visual review when presentation matters.
