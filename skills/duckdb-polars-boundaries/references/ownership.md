# Ownership and lifetime

DuckDB Connection owns registered names and relation execution context. Polars
LazyFrame owns a deferred plan; DataFrame owns materialized columns. Keep
replacement-scan objects reachable until execution. Do not return cursor-backed
or connection-bound results after closing their owner unless fully materialized.
