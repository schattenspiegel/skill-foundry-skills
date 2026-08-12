# Great Tables formatting and styling

Choose one formatter family per semantic column: number, integer, scientific,
percent, currency, bytes, duration, date/time, or markdown/plain text. Specify
locale, decimals/significant figures, separators, sign, scale, and missing-value
policy only when supported by the installed version and required by the output.
For `fmt_percent`, decide whether inputs are proportions or already-scaled
percentage points. Current Great Tables multiplies proportional inputs by 100
when `scale_values=True` (the default); use `scale_values=False` only for values
that already contain percentage points, and protect the choice with examples.

Apply formatting to selectors/columns and optional row predicates. Keep
conditional business categories as explicit derived columns rather than
recomputing them inside several style calls.

Use `tab_style` with `style.*` and `loc.*` for a small number of meaningful
emphases. Target by stable column names and data conditions. Hard-coded row
numbers are valid only for a truly fixed publication layout and must have a
protecting order test.

Color must not be the sole signal; include text, symbols, or labels and retain
readable contrast. Verify negative values, zero, null, large magnitudes, long
labels, and narrow output. Raw `html()` bypasses escaping and is allowed only
for trusted author-owned markup.
