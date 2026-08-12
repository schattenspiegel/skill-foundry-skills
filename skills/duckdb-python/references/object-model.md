# DuckDB Python connection and relation model

## Database and connection

`duckdb.connect()` creates a connection to a new in-memory database unless a
path or special database name says otherwise. The connection owns session
state: transaction, temporary/catalog objects, settings, registrations, and the
current DB-API result. Module-level query functions use a shared default
connection; package code should avoid that hidden dependency.

A helper that receives a connection borrows it. A helper that creates a
connection owns and closes it. Never return a lazy relation or reader after
closing the connection it needs.

## Relation and result

`DuckDBPyRelation` is a connection-bound symbolic relational query. Operations
compose a query; fetching, displaying, writing, or creating a catalog object is
an execution boundary. DB-API `execute` stores the current result on the
connection for `fetch*` conversion. Do not interleave result consumption with a
second statement on the same handle.

## Catalog and external objects

A table stores data in DuckDB. A view stores a query. A registered Python object
is a connection-scoped dependency, not a durable copy. Replacement scans can
discover in-scope Python objects implicitly, which is convenient interactively
but obscures dependency injection in libraries. Prefer explicit registration
and keep the object alive through consumption.

## Concurrency

The module-level default connection is unsafe for concurrent package work. A
created connection is thread-safe in the current DB-API, but it is locked for
each query. `.cursor()` produces a thread-usable handle to that same connection,
so sibling cursors serialize rather than execute queries in parallel. Give each
worker an independent connection when parallel query execution is required.
Thread-local cursors are valid when serialized access to the same database
instance, including an unnamed in-memory instance, is intentional. For a
persistent database, test the intended concurrent read/write pattern rather
than extrapolating from an in-memory unit test.
