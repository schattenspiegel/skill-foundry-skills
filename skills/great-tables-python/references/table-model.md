# Great Tables display-table model

`GT(data)` creates an output-oriented table specification from a dataframe. The
dataframe remains the source of truth for analytical values. The `GT` pipeline
adds presentation parts: heading, stub, row groups, column labels/spanners,
body, summary rows, footnotes, and source notes.

## Structural decisions

- Select and order dataframe columns before presentation unless a table-specific
  column movement is itself part of the design.
- Use a stub when each row needs a human-readable identity. Use row groups when
  sections carry meaning and the ordering is stable.
- Use spanners only for a real header hierarchy. `tab_spanner` may gather
  selected columns together; set/verify `gather` rather than allowing an
  unnoticed column reorder.
- Assign explicit spanner IDs when another operation targets them.
- Keep source notes for provenance and footnotes for localized explanation; do
  not bury critical units or caveats in hover-only behavior.

## Data contract

The table should receive already validated rows, keys, calculations, ordering,
and units. A formatting method changes displayed text, not the underlying
business rule. If a subtotal or percentage must be correct, compute and test it
in the dataframe/domain layer, then display it.
