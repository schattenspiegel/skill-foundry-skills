# Presentation and provenance

For generated stakeholder workbooks:

- separate raw machine-readable Tables from summaries and presentation sheets;
- keep merged cells out of data regions and use one header row per Table;
- add filters and useful freeze panes; choose widths deliberately;
- show units in headers, titles, or axes and centralize date/currency/percent/bps
  formats;
- distinguish editable inputs from formulas and outputs using redundant cues,
  not color alone;
- back charts with stable Tables or explicit named ranges; label titles, axes,
  periods, and units; avoid decorative chart types that obscure comparison;
- document every hidden sheet's role; never hide undocumented business logic;
- set print area, orientation, headers, and pagination only when print/PDF is a
  declared output.

When provenance matters, add a configurable `_meta` or About region with
generator/schema version, generated-at timestamp, data as-of date, source IDs
or hashes, material parameters, and code revision. Do not expose secrets,
private paths, credentials, or unnecessary personal data.

Reopen for structural checks, then render or inspect representative sheets at
realistic zoom/page settings. Visual review is required when presentation is an
output contract because an OOXML-valid file can still be unreadable.
