# Performance

PowerPoint is not a high-volume tabular format. Resolve and cache content before
rendering; preprocess images to sensible dimensions; avoid huge rasters,
reparsing the same deck, shape-by-shape business calculations, and uncontrolled
XPath traversal in tight loops.

Deduplicate repeated image content only when package behavior and downstream
editing permit it. Bound inspection details while retaining counts and stable
digests. For batch generation, optimize at the `DeckSpec -> renderer` boundary
and profile only when scale is material; do not compromise slide semantics or
preservation to reduce milliseconds.
