# Altair composition, export, and testing

## Composition

Layer shares one coordinate space. Place common data/encoding on a base chart
and derive marks from it. Facet/repeat creates small multiples and should define
panel order and scale resolution. Concatenation places independent views next
to each other; use explicit parameter/selection scope when linking them.

Independent scales improve local detail but prevent direct magnitude comparison.
Shared scales preserve comparison but can compress a small-range panel. Encode
the choice with the installed resolve API and test it in the spec.

On current Altair, express conditional encodings with
`alt.when(selection).then(...).otherwise(...)`. Older `alt.condition(...)`
examples remain common; inspect the installed version before backporting this
syntax to an older project.

## Export boundary

Return a chart from builders. At the application edge choose JSON/dict for a
spec consumer, HTML for a browser artifact, or image/vector export when the
required renderer and optional dependencies are installed. Do not assume that
successful schema serialization proves browser rendering or image export.

## Semantic tests

Inspect `chart.to_dict()` with validation enabled by the installed API. Assert:

- top-level mark/composition node;
- field names, semantic types, aggregates, sort, scales, and titles;
- transform sequence and parameter names;
- shared/independent resolve policy;
- data location (inline/named/URL), without snapshotting all row values;
- no sensitive fields embedded in the spec.

Avoid whole-spec snapshots: defaults and schema versions drift. Add a real-host
render smoke test for clipping, overlapping labels, responsive width,
accessibility, and interaction behavior when those are release requirements.
