# Polars lazy, reshape, and temporal solution recipes

These patterns preserve deferred execution until an explicit consumer and make
shape-changing semantics observable.

## Recipe `polars.lazy-file-boundary`

**Use when:** A filtered aggregation over files feeds a bounded in-memory consumer.
**Inspect first:** Confirm projected columns, consumer representation, and whether streaming execution is supported by the installed plan.
**Invariants:** Scan, filter, and aggregation remain lazy; collection happens once at the consumer.

```python
from pathlib import Path

import polars as pl


def active_totals(path: Path) -> pl.DataFrame:
    query = (
        pl.scan_parquet(path)
        .filter(pl.col("active"))
        .group_by("account_id")
        .agg(pl.col("amount").sum().alias("total_amount"))
        .sort("account_id")
    )
    plan = query.explain()
    if "Parquet" not in plan:
        raise AssertionError("expected a Parquet scan plan")
    return query.collect()
```

**Do not use when:** The result is unbounded or the consumer accepts a file sink; write or stream at that boundary instead.
**Verify:** Inspect the plan for scan-side projection/filtering and instrument the path to prove one materialization.

## Recipe `polars.streaming-cardinality-check`

**Use when:** A lazy many-to-one join must preserve fact cardinality without collecting both full inputs.
**Inspect first:** Confirm the installed join validation and streaming support, plus the acceptable cost of scalar checks.
**Invariants:** Dimension keys are unique and joined row count equals fact row count.

```python
import polars as pl


def checked_lazy_join(facts: pl.LazyFrame, dimension: pl.LazyFrame) -> pl.LazyFrame:
    duplicate_count = (
        dimension.group_by("key").len().filter(pl.col("len") > 1).select(pl.len()).collect().item()
    )
    if duplicate_count:
        raise ValueError("dimension key is not unique")
    result = facts.join(dimension, on="key", how="left", validate="m:1")
    before = facts.select(pl.len()).collect().item()
    after = result.select(pl.len()).collect().item()
    if after != before:
        raise AssertionError("join changed fact cardinality")
    return result
```

**Do not use when:** Even scalar validation scans violate the latency budget; enforce uniqueness upstream with persisted evidence.
**Verify:** Run duplicate, unmatched, and null-key fixtures and record whether installed streaming execution remains available.

## Recipe `polars.known-category-pivot`

**Use when:** A lazy pivot has a closed, ordered category domain known before execution.
**Inspect first:** Inspect the installed `LazyFrame.pivot` signature; pivot behavior is version-sensitive and unstable in the grounded version.
**Invariants:** Generated columns follow the declared category order and duplicate cells use an explicit aggregate.

```python
import polars as pl


def quarterly_sales(frame: pl.LazyFrame) -> pl.LazyFrame:
    return (
        frame.pivot(
            on="quarter",
            on_columns=["q1", "q2", "q3", "q4"],
            index="account_id",
            values="amount",
            aggregate_function="sum",
        )
        .sort("account_id")
    )
```

**Do not use when:** Categories are open-ended or the installed lazy API lacks the required capability; use an eager boundary deliberately.
**Verify:** Test missing categories, duplicate cells, category order, schema, and the installed signature.

## Recipe `polars.dst-aware-daily-window`

**Use when:** Timestamped events must aggregate by local Berlin calendar day across daylight-saving transitions.
**Inspect first:** Confirm input timezone, desired ambiguous/nonexistent-time policy, and whether day means calendar or fixed-duration day.
**Invariants:** UTC instants are converted to the business timezone before calendar grouping and output ordering is explicit.

```python
import polars as pl


def berlin_daily(events: pl.DataFrame) -> pl.DataFrame:
    return (
        events.with_columns(
            local_time=pl.col("event_time").dt.convert_time_zone("Europe/Berlin")
        )
        .sort("local_time")
        .group_by_dynamic("local_time", every="1d", period="1d", closed="left")
        .agg(pl.col("amount").sum().alias("amount"), pl.len().alias("events"))
        .sort("local_time")
    )
```

**Do not use when:** The requirement is fixed 24-hour windows or input timestamps are naive without an established localization policy.
**Verify:** Test spring-forward and fall-back fixtures, exact UTC instants, calendar labels, row counts, and explicit order.
