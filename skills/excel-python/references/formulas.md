# Formula discipline

Compare formulas by relative pattern rather than raw text when searching copied
ranges. Flag hard-coded values inside a formula run, shifted ranges, missing
new rows, external references, and Excel error literals. A Python library can
write formula text and sometimes a cached value, but only a spreadsheet engine
can establish recalculation. Record `FORMULA_TEXT_CHECKED`, `CACHE_INSPECTED`,
and `RECALCULATED` separately.
