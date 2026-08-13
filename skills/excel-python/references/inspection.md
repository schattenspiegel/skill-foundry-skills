# Inspection and preservation

Load formula and cached-value views separately. Map workbook structure before
extracting data or editing. Treat hidden sheets, names, tables, formula runs,
external links, and unexpected constants within formula regions as semantic
evidence. `read_only=True` reduces memory but omits features needed for a full
map. For `.xlsm`, use `keep_vba=True`, preserve the extension, and verify the
VBA archive remains present without executing it.
