# Testing DuckDB integrations

1. Use a temporary database path for persistence tests and a new connection per
   concurrency participant.
2. Assert columns, DuckDB types, nulls, cardinality, and explicit ordering. Test
   duplicate keys and tied sort values when relevant.
3. Send hostile quotes and SQL-looking strings through value parameters; assert
   data behavior and unchanged schema/catalog.
4. Force the middle statement of a transaction to fail and verify rollback on a
   fresh connection.
5. Test registered-object cleanup and lifetime, including consumption before
   close/unregister.
6. For large-result APIs, consume multiple batches and assert the implementation
   does not first call a full-table/dataframe fetch.
7. Reopen database or file output and verify the persisted artifact.
8. Use `EXPLAIN`/profiling for projection, filter, join, or scan-performance
   claims; do not assert exact unstable plan formatting unless version-pinned.
