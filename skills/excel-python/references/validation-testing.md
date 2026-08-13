# Semantic validation and testing

Validation layers are distinct:

1. Package: ZIP opens; required parts, relationships, content types, VBA, and
   high-risk opaque hashes are present.
2. Structure: sheets/order/visibility, Tables/ranges, names, dimensions,
   validations, panes, charts/drawings, and date/calculation settings match.
3. Formula: locations, exact text where contractual, normalized copied patterns,
   external references, array/spill boundaries, and formula-owned columns match.
4. Values/types: selected identifiers, units, blanks, booleans, dates, errors,
   formats, and reconciliation totals satisfy the workbook contract.
5. Presentation: representative sheets render/read correctly with titles,
   units, widths, panes, charts, and print settings when required.
6. Runtime: recalculation, refresh, VBA, or native rendering is reported only if
   an authorized real engine ran and its saved artifact was reread.

Use `diff_workbooks.py` for a semantic before/after report; do not compare raw
`.xlsx` bytes. Every difference must be required, accepted, or unexpected. Add
small falsifiers for 16+ digit IDs, leading `=`, blank versus empty string,
non-finite numbers, epoch boundaries, formula overrides, hidden sheets, and
package parts that the selected library does not understand.
