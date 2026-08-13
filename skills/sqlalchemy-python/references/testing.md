# Query verification

Test with the target dialect when its semantics matter; SQLite is not proof of
PostgreSQL behavior. Cover transaction commit and rollback, constraints,
concurrent ownership, result cardinality, eager/lazy loading, generated SQL and
parameters, pool cleanup, and async cancellation. Count statements to catch
N+1 behavior and inspect execution plans only after correctness.
