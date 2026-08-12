# DataFrame operation map

Load this reference for construction, inspection, ordinary table transforms,
row or column selection, deduplication, reshaping, or export. Start from intent
and required return shape; do not scan the API alphabetically for a familiar
name.

## Route intent to an operation family

| Intent | Primary API | Expected return | Decision that must be explicit |
|---|---|---|---|
| Construct in-memory data | `pl.DataFrame`, `pl.Series`, `pl.from_*` | Eager object | Schema, orientation, and strictness. |
| Read now | Ordinary readers such as `pl.read_csv` / `pl.read_parquet` | `DataFrame` | Data is intentionally materialized; inspect specialized `read_*` return contracts. |
| Defer file work | `pl.scan_*` | `LazyFrame` | Schema/inference and execution boundary. |
| Inspect table contract | Eager `shape` / `columns` / `schema` / `head` / `glimpse` / `null_count`; lazy `collect_schema` / bounded-output `head(...).collect()` / `explain` | Tuple, list, Schema, frame, display/`None`, or plan text depending on API | Whether inspection executes data or source metadata. |
| Keep/compute columns | `select` | Frame containing only requested outputs | Output names and expression lengths. |
| Add/replace columns | `with_columns` | Frame containing original plus requested outputs | Same-name replacement and dependent stages. |
| Keep rows by values | `filter` | Same columns, subset of rows | Null predicate behavior. |
| Keep rows by position | `slice`, `head`, `tail`, `gather` | Same columns, selected positions | Position is truly the contract. |
| Order rows | `sort`, expression `sort_by` | Reordered frame or values | Keys, direction, null placement, and tie-breaker. |
| Collapse duplicate records | `unique` | At most one row per key | Surviving row and output order. |
| Summarize groups | `group_by(...).agg(...)` | One row per group | Scalar versus list aggregation and group order. |
| Add group metrics to rows | expression `.over(...)` | Original row grain | Partition keys and ordering. |
| Combine keyed tables | `join`, `join_asof`, `join_where` | Match-dependent frame | Key domain, multiplicity, nulls, and order. |
| Stack records | `pl.concat`, `vstack` | Combined frame | Schema compatibility/coercion/union policy. |
| Reshape | `unpivot`, `pivot`, `explode`, `unnest` | New row or column grain | Generated names, multiplicity, and ordering. |
| Hand data to a consumer | `write_*`, `sink_*`, `to_arrow`, `to_numpy`, `to_dicts`, `to_pandas` | External artifact/object | Columnar versus Python boundary and precision. |

## Construct a deliberate frame

Dictionary input is naturally column-oriented. For sequences representing row
records, state `orient="row"`; for column sequences, state `orient="col"` or
use a mapping. Use an ordered schema whenever identifiers, temporal fields,
empty input, nested values, or downstream consumers make inference unsafe.

```python
import polars as pl


orders = pl.DataFrame(
    [
        ("0007", 10, "2026-08-12T09:15:00Z", 2, 12.50),
        ("0011", 10, "2026-08-12T10:00:00Z", 1, None),
    ],
    schema={
        "order_id": pl.String,
        "customer_id": pl.Int64,
        "occurred_at": pl.String,
        "quantity": pl.Int64,
        "unit_price": pl.Float64,
    },
    orient="row",
).with_columns(
    pl.col("occurred_at").str.to_datetime(time_zone="UTC", strict=True)
)
```

Keep `strict=True` unless invalid input becoming null is the declared policy.
Do not cast an identifier such as `"0007"` to an integer just because its
characters are numeric.

## Inspect without changing semantics

For an eager frame, `shape`, `columns`, `schema`, `head`, `glimpse`, and
`null_count` answer different questions. `glimpse()` displays a preview and
returns `None` by default; do not use printed output as a schema or test contract.

For a lazy plan:

```python
query = pl.scan_parquet("orders/*.parquet")
schema = query.collect_schema()
preview = query.head(5).collect()
plan = query.explain()
```

`collect_schema()` does not materialize all rows, but resolving file or remote
metadata may still perform work. `head(...).collect()` returns at most the
requested output rows, but upstream sorting, joining, or aggregation can still
require substantial or complete execution. `explain()` describes a plan; use it
only when plan behavior matters.

## Select columns, derive columns, and filter rows

```python
result = (
    orders.with_columns(
        gross=pl.col("quantity") * pl.col("unit_price"),
        day=pl.col("occurred_at").dt.date(),
    )
    .filter(pl.col("gross").is_not_null() & (pl.col("gross") >= 20))
    .select("order_id", "day", "gross")
)
```

Use `select` when only requested outputs should remain. Use `with_columns` when
unknown passthrough columns must remain. Both return new frames; replacing a
same-named column is explicit transformation, not pandas-style mutation.

A filter retains only rows whose predicate evaluates to `True`; both `False`
and null predicates are discarded. If rows with unknown status must remain,
encode that policy, for example
`pl.col("status").eq("open") | pl.col("status").is_null()`.

Use selectors when the operation follows dtype or name rather than a fixed
column list:

```python
import polars.selectors as cs


numeric_ready = orders.with_columns(
    cs.numeric().exclude("customer_id").fill_null(0).cast(pl.Float64)
)
```

Selectors expand against the input schema and can match zero, one, or many
columns. Test the expanded output names when the schema is not fixed.

## Get a column or positional subset

```python
amounts: pl.Series = result.get_column("gross")
one_column: pl.DataFrame = result.select("gross")
first_two_rows: pl.DataFrame = result.head(2)
selected_rows: pl.DataFrame = orders.gather([1, 0, 1])
```

Use a `Series` boundary only when the consumer wants one materialized column.
Keep a one-column `DataFrame` when later work remains table-shaped. Use named
expressions for semantic selection; use row positions only when positions are
part of the request. Polars positions do not align records by label.

## Aggregate or annotate groups

```python
summary = (
    orders.group_by("customer_id")
    .agg(
        order_rows=pl.len(),
        priced_rows=pl.col("unit_price").count(),
        revenue=(pl.col("quantity") * pl.col("unit_price")).sum(),
        order_ids=pl.col("order_id").sort_by("occurred_at"),
    )
    .sort("customer_id")
)

annotated = orders.with_columns(
    customer_revenue=(pl.col("quantity") * pl.col("unit_price"))
    .sum()
    .over("customer_id")
)
```

The first produces one row per customer. The second preserves every order row.
`pl.len()` counts rows; expression `.count()` counts non-null values. A bare
column in `.agg` collects a `List`, so apply an explicit reduction when the
output must be scalar. Sort explicitly if row, group, or list order is part of
the contract.

## Sort and deduplicate from a survivor rule

“Remove duplicates” is incomplete. Define the subset that identifies a
duplicate, the surviving row, and final order.

```python
events = pl.DataFrame(
    {
        "event_id": ["a", "a", "b"],
        "event_time": [3, 3, 1],
        "ingest_id": [10, 11, 12],
        "value": ["old", "new", "only"],
    }
)

latest = (
    events.sort(
        ["event_time", "ingest_id"],
        descending=[True, True],
        nulls_last=[True, True],
    )
    .unique(subset="event_id", keep="first")
    .sort("event_id")
)
```

Here “first” means first after the explicit timestamp and ingestion tie-breaker
sort. The final sort defines output order. Set `maintain_order=True` only when
the intermediate unique output itself must preserve input order; it has an
execution cost and can block streaming.

## Reshape from input and output grain

```python
quarterly = pl.DataFrame(
    {
        "customer_id": [10, 20],
        "q1": [100, 80],
        "q2": [120, 90],
        "q3": [110, 95],
        "q4": [140, 105],
    }
)

long = quarterly.unpivot(
    ["q1", "q2", "q3", "q4"],
    index="customer_id",
    variable_name="quarter",
    value_name="revenue",
).sort("customer_id", "quarter")

wide = long.pivot(
    on="quarter",
    on_columns=["q1", "q2", "q3", "q4"],
    index="customer_id",
    values="revenue",
    aggregate_function="sum",
)
```

`unpivot` turns columns into rows and does not promise output row order, so sort
when order matters. `pivot` turns values into columns. Before a
pivot, decide how duplicate `(index, generated-column)` cells resolve; do not
use `first` merely to suppress an error. Generated categories determine the
output schema; an explicit ordered `on_columns` set determines generated
columns. Pivot is unstable in Polars `1.43.2`, so inspect the installed
signature. A lazy pivot is appropriate only when the installed API supports it
and the full category set is known; otherwise discover the categories or cross
an explicit eager boundary.

`explode` turns nested elements into rows and changes grain. The emitted rows
for null or empty containers depend on the installed `empty_as_null` and
`keep_nulls` behavior, whose defaults are version-sensitive; set the required
policy when available and test both states. `unnest` expands Struct fields into
columns. Test name collisions and the new row count.

## Export only at the consumer boundary

Keep the pipeline columnar until a real consumer requires another form:

```python
result.write_parquet("result.parquet")
payload = result.to_dicts()  # only for a consumer requiring Python row dicts
```

Prefer a lazy `sink_*` for a large file result that need not become one
in-memory `DataFrame`. `to_dicts()` and `iter_rows()` create Python objects and
truncate `Datetime("ns")` values to Python's microsecond precision; use
Parquet, Arrow, or a suitable NumPy boundary when nanoseconds must survive.
`to_numpy()` may copy or coerce: numeric columns can choose a common supertype,
integer nulls can become floating `NaN`, and mixed frames can become object
arrays. Arrow and pandas conversion can require optional dependencies. Choose
the boundary from the consumer contract, then test dtypes and missing values.
