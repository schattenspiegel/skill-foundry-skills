# Polars core solution recipes

Load only the recipe that matches the requested grain and consumer. These are
complete composition patterns, not substitutes for inspecting installed APIs.

## Recipe `polars.typed-csv-scan`

**Use when:** A file-backed pipeline needs stable identifier, amount, and timestamp types.
**Inspect first:** Confirm delimiter, timestamp format, time zone, null markers, and whether malformed rows may be rejected.
**Invariants:** IDs remain strings, timestamps are UTC, casts are strict, and collection occurs once.

```python
from pathlib import Path

import polars as pl


def read_orders(path: Path) -> pl.DataFrame:
    return (
        pl.scan_csv(
            path,
            schema_overrides={"order_id": pl.String, "amount": pl.Float64},
            try_parse_dates=False,
        )
        .with_columns(
            pl.col("created_at").str.to_datetime(
                format="%Y-%m-%dT%H:%M:%S%#z", time_zone="UTC", strict=True
            )
        )
        .select("order_id", "amount", "created_at")
        .collect()
    )
```

**Do not use when:** The caller requires streaming output or the installed parser uses a different verified timestamp contract.
**Verify:** Assert exact schema, rejected dirty timestamps, preserved leading-zero IDs, and one terminal collection.

## Recipe `polars.dependent-expression-stages`

**Use when:** One derived column depends on another derived column from the same transformation.
**Inspect first:** Draw the dependency order and decide null and zero-denominator policy.
**Invariants:** Every expression references columns available at the start of its stage.

```python
import polars as pl


def add_net_ratio(frame: pl.DataFrame) -> pl.DataFrame:
    return frame.with_columns(net=pl.col("gross") - pl.col("discount").fill_null(0)).with_columns(
        net_ratio=pl.when(pl.col("gross") != 0)
        .then(pl.col("net") / pl.col("gross"))
        .otherwise(None)
    )
```

**Do not use when:** Both outputs are independent; keep independent expressions in one stage.
**Verify:** Test zero, null discount, negative values, and output dtypes without using Python row callbacks.

## Recipe `polars.validated-many-to-one-join`

**Use when:** Fact rows must enrich from a dimension whose key should be unique.
**Inspect first:** Confirm key domains, dtypes, null-key policy, expected unmatched rows, and installed validation spelling.
**Invariants:** Left grain and row count remain stable; duplicate dimension keys fail.

```python
import polars as pl


def enrich_orders(orders: pl.DataFrame, customers: pl.DataFrame) -> pl.DataFrame:
    if customers.select(pl.col("customer_id").is_duplicated().any()).item():
        raise ValueError("customer_id must be unique in customers")
    result = orders.join(
        customers.select("customer_id", "segment"),
        on="customer_id",
        how="left",
        validate="m:1",
    )
    if result.height != orders.height:
        raise AssertionError("join changed order grain")
    return result
```

**Do not use when:** The relationship is genuinely many-to-many or unmatched keys must be rejected rather than retained.
**Verify:** Test duplicate dimension keys, null keys, unmatched keys, dtype mismatch, and stable left cardinality.

## Recipe `polars.normalize-nested-list`

**Use when:** Each input row contains a list of structs that must become child rows.
**Inspect first:** Define empty-list and null-list behavior, child schema, and parent key uniqueness.
**Invariants:** Parent identity is retained and child fields are extracted through native namespaces.

```python
import polars as pl


def normalize_items(orders: pl.DataFrame) -> pl.DataFrame:
    return (
        orders.select("order_id", "items")
        .explode("items")
        .filter(pl.col("items").is_not_null())
        .select(
            "order_id",
            sku=pl.col("items").struct.field("sku"),
            quantity=pl.col("items").struct.field("quantity").cast(pl.Int64),
        )
        .sort(["order_id", "sku"])
    )
```

**Do not use when:** Empty and null lists must emit placeholder child rows; encode that policy explicitly first.
**Verify:** Test empty, null, multi-item, and malformed structs plus final grain and order.
