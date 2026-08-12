# Altair declarative grammar

## Field definitions

An encoding field definition combines field, semantic type, optional aggregate
or bin/time unit, scale, axis/legend, sort, and title. Use explicit channel
objects when configuring these properties. Shorthand is suitable only when the
field name cannot be confused by punctuation and the inferred defaults match
the contract.

Semantic type changes behavior:

- quantitative: continuous numeric magnitude;
- temporal: dates/instants or derived time units;
- nominal: unordered categories/identifiers, even when stored as numbers;
- ordinal: ordered categories with discrete steps;
- geographic: geometry/geospatial shape data.

Never encode an identifier as quantitative merely because its dtype is integer.

## Mark and grain

A mark instance corresponds to the post-transform data grain. Encoding an
aggregate changes that grain. For grouped aggregates, every non-aggregated
encoded field participates in grouping. Write the intended grouping explicitly
when a hidden color/detail/tooltip field would split marks unexpectedly.

Use `detail` to group lines without adding a legend. Use `order` when the mark's
draw/connection order is contractual. Use `tooltip` for inspection, not as the
only place a necessary comparison can be made.

## Missing and invalid values

Decide whether null/invalid data should be filtered, imputed, shown as a gap, or
represented as an explicit category. A line crossing missing time points can
imply continuity; encode or transform gaps according to the domain. Test empty
data and a missing-value row in the serialized spec/render host.
