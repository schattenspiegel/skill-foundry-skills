# Text and typography

Text hierarchy is `TextFrame -> Paragraph -> Run`. Mutate at the narrowest level
that preserves meaningful formatting. Setting `shape.text` reconstructs text
content and can discard paragraph/run formatting; use it only when that loss is
explicitly harmless.

Inherit theme and placeholder fonts. Define minimum sizes by delivery context
and treat overflow as a failed content/layout contract. Shorten, split, or move
content before applying `fit_text()`. Font fitting depends on metrics and is not
visual proof.

Make paragraph spacing, bullet levels, indentation, and soft versus paragraph
breaks deliberate. Track font references, local availability, embedding policy,
and PowerPoint substitution checks separately. Do not distribute font files.
