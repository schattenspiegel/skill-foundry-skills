# Great Tables render and testing

Choose the terminal artifact deliberately:

- notebook/browser preview: return/display the `GT` object;
- embeddable HTML: `as_raw_html` fragment, with inline CSS when the host/email
  requires it;
- standalone HTML: request a full page or write the raw HTML intentionally;
- LaTeX: verify escaping, packages, and the document compiler;
- image/PDF: use the installed save API and verify headless browser, fonts,
  viewport, scale, and file output.

Test the input dataframe values, row order, and derived flags independently.
For the table specification, assert selected formatters, labels, spanners, and
locations using supported inspection/HTML evidence for the pinned version.
Render an HTML artifact and inspect text/order/escaping; add visual smoke or
snapshot checks only for stable publication layout. Do not treat an HTML string
as proof that PNG/PDF export dependencies work.

Inspect long labels, empty data, nulls, extreme values, and HTML-like input.
Verify that external text is escaped and that every emphasized cell still
matches after input rows are permuted.
