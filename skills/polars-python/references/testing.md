# Testing Polars behavior

Load this reference when writing or reviewing tests for a Polars transformation.

## Assert the contract

Use `polars.testing.assert_frame_equal` or `assert_series_equal`. Prefer an expected object with an explicit schema over dictionaries, printed tables, row tuples, or string snapshots.

```python
import polars as pl
from polars.testing import assert_frame_equal

expected = pl.DataFrame(
    {"customer_id": [1], "total_cents": [375]},
    schema={"customer_id": pl.Int64, "total_cents": pl.Int64},
)
assert_frame_equal(actual, expected)
```

Assert separately when the risk deserves a clearer failure:

- exact schema and column order;
- row count or one-row-per-entity grain;
- null count versus `NaN` count;
- key uniqueness before or after a join;
- contractual row/list order;
- returned `DataFrame` versus `LazyFrame` type;
- no execution during lazy-plan construction.

Disable row-order checking only when order is explicitly non-contractual. Use installed tolerance keyword names for approximate floats; do not weaken dtype or exact-value checks to hide an unintended coercion.

## Minimal adversarial matrix

Select the rows that can falsify the rule:

- null and `NaN` separately;
- duplicate and unmatched join keys;
- empty input with an explicit schema;
- a dirty value after the inference sample;
- minimum/maximum safe cast values;
- equal sort keys plus a tie-breaker;
- unsorted input for order-sensitive work;
- empty and null nested values before `explode` or `unnest`;
- stale, future, and exact matches for an as-of join.

For a lazy function, assert that constructing it does not call `collect` or an eager reader, then collect the returned plan in the test. For a performance regression, prove result equivalence before checking the plan or timing.
