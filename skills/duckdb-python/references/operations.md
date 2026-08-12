# DuckDB Python operation map

## Query

- Use `connection.execute(sql, parameters)` for immediate DB-API statements and
  `connection.sql(..., params=...)` or relational methods when returning or
  composing a relation fits the installed API.
- Use `executemany` only for genuinely repeated parameter sets. For bulk
  analytical ingestion, direct Arrow/dataframe scans or file/table operations
  are usually clearer; measure before choosing row-at-a-time insertion.
- Use `EXPLAIN` for a static plan and profiling for executed work. A faster
  syntax is not evidence of a better physical plan.

## Read and expose data

- Query Parquet/CSV/JSON directly so projections and filters stay in DuckDB.
- Register a named Python object for explicit SQL dependency; unregister it if
  the connection survives the task.
- Inspect with `DESCRIBE SELECT ...` or relation types before accepting
  inferred schema from heterogeneous files.

## Return or persist

- Use scalar/row/list fetches only for bounded results.
- Use Arrow batch readers for a large Arrow-capable consumer; use Arrow tables,
  pandas, Polars, or NumPy only when that exact materialized form is required.
- Use `COPY` for file output and reopen the file for verification. Use table or
  view creation according to copy-versus-query semantics.

## Extensions and filesystems

Loading an extension changes executable capability and can involve network
access or native code. Follow project trust policy, prefer signed official
extensions, and make install/load steps explicit and version-grounded.
