# DuckDB resource, transaction, and persistence recipes

Use these patterns where correctness depends on ownership rather than SQL text
alone.

## Recipe `duckdb.thread-private-connections`

**Use when:** Worker threads need actual parallel query execution against one persistent database.
**Inspect first:** Test the deployment's concurrent read/write pattern and decide read-only access per worker.
**Invariants:** Every worker creates and closes its own connection; no default connection or shared cursor is used.

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import duckdb


def _count_one(database: Path, parquet_path: Path) -> int:
    with duckdb.connect(str(database), read_only=True) as connection:
        row = connection.execute(
            "SELECT count(*) FROM read_parquet(?)", [str(parquet_path)]
        ).fetchone()
        return int(row[0])


def count_files(database: Path, paths: list[Path]) -> list[int]:
    with ThreadPoolExecutor() as pool:
        return list(pool.map(lambda path: _count_one(database, path), paths))
```

**Do not use when:** Serialized access to one in-memory database is intentional; thread-local cursors may be the correct branch.
**Verify:** Instrument connection identity per worker and test the real persistent database under concurrent load.

## Recipe `duckdb.atomic-dependent-writes`

**Use when:** Multiple dependent database writes must commit or roll back together.
**Inspect first:** Separate transactional database effects from external file/network effects that cannot roll back.
**Invariants:** Commit occurs only after every statement succeeds and any exception triggers rollback.

```python
import duckdb


def transfer_credit(
    connection: duckdb.DuckDBPyConnection, source: str, target: str, amount: int
) -> None:
    if amount <= 0:
        raise ValueError("amount must be positive")
    connection.begin()
    try:
        connection.execute(
            "UPDATE accounts SET credits = credits - ? WHERE account_id = ?",
            [amount, source],
        )
        connection.execute(
            "UPDATE accounts SET credits = credits + ? WHERE account_id = ?",
            [amount, target],
        )
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
```

**Do not use when:** The operation includes irreversible external effects; use an explicit coordination/outbox design.
**Verify:** Force the second statement to fail and inspect balances from a fresh connection after rollback.

## Recipe `duckdb.registered-object-lifetime`

**Use when:** Reusable SQL consumes a caller-provided Arrow or dataframe object by an explicit name.
**Inspect first:** Confirm accepted object type, connection ownership, result size, and whether a durable copy is required.
**Invariants:** Registration is explicit, the source remains alive through consumption, and cleanup occurs in `finally`.

```python
import duckdb


def summarize_registered(
    connection: duckdb.DuckDBPyConnection, arrow_table: object
) -> list[tuple[object, ...]]:
    connection.register("input_rows", arrow_table)
    try:
        return connection.execute(
            """
            SELECT category, count(*) AS rows
            FROM input_rows
            GROUP BY category
            ORDER BY category
            """
        ).fetchall()
    finally:
        connection.unregister("input_rows")
```

**Do not use when:** Data must survive connection close or process restart; create a table or durable file deliberately.
**Verify:** Assert results before cleanup, failed-query cleanup, missing registration afterward, and no implicit replacement scan.

## Recipe `duckdb.persistent-copy-contract`

**Use when:** External file data must become a durable DuckDB table that survives process boundaries.
**Inspect first:** Define replacement/migration policy, schema, database path, and transaction boundary.
**Invariants:** `CREATE TABLE AS` copies data, validation happens before commit, and reopening proves durability.

```python
from pathlib import Path

import duckdb


def replace_orders(database: Path, parquet_path: Path) -> int:
    with duckdb.connect(str(database)) as connection:
        connection.begin()
        try:
            connection.execute("DROP TABLE IF EXISTS orders")
            connection.execute(
                "CREATE TABLE orders AS SELECT * FROM read_parquet(?)",
                [str(parquet_path)],
            )
            rows = int(connection.execute("SELECT count(*) FROM orders").fetchone()[0])
        except Exception:
            connection.rollback()
            raise
        else:
            connection.commit()
    with duckdb.connect(str(database), read_only=True) as check:
        if int(check.execute("SELECT count(*) FROM orders").fetchone()[0]) != rows:
            raise AssertionError("persisted row count changed")
    return rows
```

**Do not use when:** Consumers need a live view of changing external files; use a view and preserve that dependency explicitly.
**Verify:** Reopen in a fresh connection, assert schema/types/counts, and force a pre-commit failure to prove rollback.
