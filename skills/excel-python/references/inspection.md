# Inspection

Start with `python scripts/inspect_workbook.py WORKBOOK`. It combines openpyxl
structure with read-only ZIP/OOXML inventory and reports bounded details plus
complete counts/digests. It does not establish preservation support.

Open formula and cached-value views separately when caches matter. Normal mode
is required for a complete object map; `read_only=True` omits charts, images,
and other APIs. Inspect sheet order and visibility, dimensions, Tables, names,
merged ranges, formulas, validations, panes, comments, charts, external links,
date system, and calculation settings relevant to the contract.

Do not infer that `max_row`/`max_column` is the semantic data range; formatting
and stale dimensions can expand it. Prefer an Excel Table or declared range.
Do not dump sensitive cell values by default. Sample only the contract-relevant
region and state truncation.

For `.xlsm`, load with `keep_vba=True`, preserve the extension, and hash
`xl/vbaProject.bin` before and after without executing it. If package inventory
finds unknown or unsupported parts and preservation matters, stop before save.
