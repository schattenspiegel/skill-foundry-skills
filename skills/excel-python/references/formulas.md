# Formula semantics

## Evidence states

Report these independently:

- `FORMULA_TEXT_CHECKED`: formula cells and their stored formula text were read.
- `CACHE_INSPECTED`: the cached values last saved by a spreadsheet application
  were read separately with `data_only=True`.
- `RECALCULATED`: a real spreadsheet engine recalculated, saved, and the saved
  values were reread. openpyxl, XlsxWriter, and package inspection cannot
  establish this state.

A missing, zero, or old cache is not evidence that the formula is wrong. A
plausible cache is not evidence that it is current.

## Audit formula regions

Compare copied formulas by relative pattern, not raw text. Normalize A1
references while preserving absolute (`$A$1`), mixed (`A$1`, `$A1`), range,
sheet, workbook, structured, spill (`#`), and implicit-intersection (`@`)
semantics. Flag:

- constants or blanks embedded in a formula-owned column;
- one formula whose normalized pattern differs from its run;
- shifted or truncated ranges, especially formulas that omit inserted rows;
- formulas referring to unexpected sheets, workbooks, or external links;
- Excel error literals and cached error results;
- unexpected array/shared-formula boundaries or spill anchors.

Do not automatically replace a deviation: it may be an intentional subtotal,
opening balance, exception, or override. Report the cell, neighboring pattern,
and contract conflict.

## Writing formulas

- XlsxWriter formulas use Excel's stored US-English function names, comma
  separators, and documented future-function prefixes or options. Never copy a
  localized display formula unchanged.
- XlsxWriter does not calculate formulas. Its default cached result is zero and
  it marks the workbook for recalculation. Supply an explicit cached value only
  when independently computed from the same declared inputs, and label it as a
  supplied cache rather than Excel evidence.
- Use the library's array/dynamic-array API for array formulas. Do not emulate a
  spill formula by copying ordinary formulas into the expected spill range.
- Preserve structured references when the Table is the stable interface.

## High-risk semantics

Inspect and preserve calculation mode, full-calculation flags, iterative
calculation settings, circular references, volatile functions, external
references, defined-name formulas, and table calculated columns. `LET`,
`LAMBDA`, dynamic-array functions, and newer functions can require versioned
storage syntax; inspect the installed writer and a known-valid workbook before
rewriting them. Do not claim compatibility with an older Excel consumer unless
that consumer is part of the tested contract.
