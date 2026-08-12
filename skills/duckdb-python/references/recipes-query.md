# DuckDB query and result recipes

Keep values, SQL structure, connection ownership, and result materialization as
separate decisions. Inspect installed signatures before adopting an online form.

## Recipe `duckdb.parameterized-owned-query`

**Use when:** A package function owns a connection and returns a proven-small ordered result.
**Inspect first:** Confirm database path, read-only policy, result bound, and tie-breaker columns.
**Invariants:** Caller values are bound, connection closes, and exact order is contractual.

```python
from pathlib import Path

import duckdb


def find_orders(
    database: Path, customer_email: str, minimum_amount: float
) -> list[tuple[object, ...]]:
    sql = """
        SELECT order_id, amount, created_at
        FROM orders
        WHERE customer_email = ? AND amount >= ?
        ORDER BY created_at ASC, order_id ASC
    """
    with duckdb.connect(str(database), read_only=True) as connection:
        return connection.execute(sql, [customer_email, minimum_amount]).fetchall()
```

**Do not use when:** The result is not bounded or the helper borrows a caller-owned connection.
**Verify:** Send quote/SQL-looking values, assert catalog is unchanged, exact rows/order, and connection closure.

## Recipe `duckdb.bounded-arrow-reader`

**Use when:** A potentially large result goes to an Arrow-capable streaming consumer.
**Inspect first:** Verify installed Arrow reader API, batch-size support, and connection lifetime.
**Invariants:** Projection/filter stay in DuckDB and the caller keeps the connection open through consumption.

```python
from pathlib import Path

import duckdb


def stream_active(
    connection: duckdb.DuckDBPyConnection, path: Path, batch_size: int = 65_536
):
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    relation = connection.sql(
        "SELECT id, payload FROM read_parquet(?) WHERE active = true",
        params=[str(path)],
    )
    return relation.to_arrow_reader(batch_size=batch_size)
```

**Do not use when:** The helper will close the connection before consumption or the consumer requires a durable file.
**Verify:** Consume multiple batches and instrument against `fetchall`, pandas, Polars, or full Arrow Table materialization.

## Recipe `duckdb.relation-composition`

**Use when:** Several package helpers must compose a relational plan before one consumer executes it.
**Inspect first:** Confirm all relations share the same borrowed connection and define the eventual consumer.
**Invariants:** Helpers return relations without fetching and never close the injected connection.

```python
from pathlib import Path

import duckdb


def active_orders(
    connection: duckdb.DuckDBPyConnection, path: Path
) -> duckdb.DuckDBPyRelation:
    return connection.sql(
        "SELECT customer_id, amount FROM read_parquet(?) WHERE active = true",
        params=[str(path)],
    )


def customer_totals(relation: duckdb.DuckDBPyRelation) -> duckdb.DuckDBPyRelation:
    return relation.aggregate("sum(amount) AS total_amount", "customer_id").order(
        "total_amount DESC, customer_id ASC"
    )
```

**Do not use when:** A helper owns and closes its connection; return a materialized bounded value or durable artifact instead.
**Verify:** Assert no fetch occurs during composition, inspect the final plan, then consume before closing the connection.

## Recipe `duckdb.explain-plan-guard`

**Use when:** A projection/filter pushdown claim must be checked for a file scan.
**Inspect first:** Verify installed EXPLAIN format and choose stable semantic evidence rather than exact plan text.
**Invariants:** The query projects only required fields and binds the external path as data.

```python
from pathlib import Path

import duckdb


def explain_active_scan(
    connection: duckdb.DuckDBPyConnection, path: Path
) -> str:
    relation = connection.sql(
        "SELECT id FROM read_parquet(?) WHERE active = true",
        params=[str(path)],
    )
    plan = relation.explain()
    if "PARQUET" not in plan.upper():
        raise AssertionError("expected a Parquet scan")
    return plan
```

**Do not use when:** Exact physical-plan formatting is the test target; pin the engine and accept maintenance cost explicitly.
**Verify:** Use a disposable Parquet fixture and confirm the expected scan plus result equivalence to a direct query.
