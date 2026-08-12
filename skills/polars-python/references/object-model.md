# Polars object and shape model

Load this reference when the task depends on what a Polars object represents,
what an operation returns, or whether code should manipulate data, a column, an
expression, or a query plan.

## Six nouns

| Object | What it is | Has values now? | Normal role |
|---|---|---:|---|
| `DataFrame` | An eager, materialized two-dimensional table of uniquely named, equal-length columns. Different columns may have different dtypes. | Yes | In-memory work, an eager public contract, or a collected result whose final table fits memory. |
| `Series` | One eager, materialized, named, one-dimensional column whose values share a dtype. | Yes | A one-column input/output boundary or direct one-column operation. |
| `Expr` | A declarative recipe for producing values from columns, literals, or other expressions. It is not a column of data. | No | Reusable transformation inside `select`, `with_columns`, `filter`, `agg`, or a window. |
| `LazyFrame` | A logical query plan that will produce a table when executed. Transformations extend the plan. | No | File-backed, multi-stage, large, or optimization-sensitive work. |
| `Schema` | The ordered mapping from every column name to its dtype. | No rows | The interface contract: use eager `DataFrame.schema` or lazy `LazyFrame.collect_schema()`. |
| Selector | A schema-aware expression expander such as `cs.numeric()` or `cs.matches(...)`. | No | Apply one expression to a set of columns without hard-coding the set. |

`DataFrame` columns are `Series`. Use frame methods to change table shape and
`Expr` objects to define column computations or predicates inside those methods.
`DataFrame` and `LazyFrame` share most of the expression DSL: eager contexts
execute now, while lazy contexts add nodes to a plan. `GroupBy` and
`LazyGroupBy` are intermediate builders, not result tables; finish them with a
terminal group operation, normally `.agg(...)`.

Polars has no pandas-style semantic row index. If labels identify records or
control alignment, keep them as ordinary typed columns and use them in filters,
joins, groups, and sorts.

## Decide from the required return object

| Required result | Use | Do not accidentally return |
|---|---|---|
| A table already computed in memory | `DataFrame` | `LazyFrame` merely because lazy is often faster for files. |
| A deferred table computation | `LazyFrame` | A collected `DataFrame` hidden behind `.lazy()`. |
| One materialized column | `Series` via `get_column` or a declared Series operation | A one-column `DataFrame` if the caller requires `Series`. |
| A reusable column computation | `Expr` helper | A function that accepts a `Series` and forces eager execution. |
| One-column table | `select("name")` | A `Series` from `get_column("name")`. |
| One scalar after execution | Eager `df.select(...).item()` or lazy `lf.select(...).collect().item()` at the consumer | An unevaluated `Expr` or one-row frame. |

Do not infer the return type from the number of columns. A one-column
`DataFrame` is still a table and preserves table composition; a `Series` is a
materialized column.

## Think in shape effects

Before selecting an API, classify its effect on row grain:

| Shape effect | Typical operation | Result rule |
|---|---|---|
| One output value per input row | arithmetic, cast, string/datetime/list expression | Same height in `with_columns`; compatible expression height in `select`. |
| One Boolean per input row | predicate in `filter` | Retain only rows whose result is `True`; null is not true. |
| One value per frame or group | `sum`, `mean`, `first`, `len` | Length-one expression globally or one result per group; the surrounding context remains a frame until explicit extraction. |
| One list per group | bare column expression inside `.agg` | One group row containing a `List`. |
| Group result repeated at input grain | aggregate expression with `.over(keys)` | Same row count unless an explicit window mapping changes it. |
| Nested values expanded to rows | `explode` | Row grain follows nested lengths plus the installed null/empty-container policy; set and test that policy. |
| One row per distinct key | `group_by(...).agg(...)` | Output height equals the number of groups. |
| Match-dependent rows | `join` | Cardinality follows key multiplicity and join type. |

This shape classification is more reliable than choosing a familiar method
name. State the input and output grain before every group, join, explode,
unpivot, pivot, deduplication, or window.

A length-one expression can broadcast to frame height in a compatible context;
other incompatible expression lengths raise. A window with the default
`mapping_strategy="group_to_rows"` preserves row grain. The `"explode"`
strategy changes row count and needs an explicit grain and order contract.

## Canonical object flow

```python
import polars as pl
import polars.selectors as cs


def normalized_text(column: str) -> pl.Expr:
    return pl.col(column).str.strip_chars().str.to_lowercase()


users = pl.DataFrame(
    [
        (1, " Ada ", [9, 10], 3),
        (2, "LIN", [8], None),
    ],
    schema={
        "user_id": pl.Int64,
        "name": pl.String,
        "scores": pl.List(pl.Int64),
        "visits": pl.Int64,
    },
    orient="row",
)

eager_result = users.with_columns(
    normalized_text("name").alias("name"),
    cs.integer().exclude("user_id").fill_null(0),
)
name: pl.Series = eager_result.get_column("name")

plan: pl.LazyFrame = users.lazy().with_columns(normalized_text("name").alias("name"))
schema: pl.Schema = plan.collect_schema()
```

The helper returns an `Expr`, so the caller decides whether it runs eagerly or
becomes part of a lazy plan. The constructor names dtypes and row orientation
because both are part of the boundary contract. Calling `.lazy()` changes the
execution representation, not the data semantics.

Contrast materialized and symbolic column work:

```python
series = users.get_column("name").str.to_lowercase()  # executes now
expr = pl.col("name").str.to_lowercase()  # recipe for a frame context
```

## Access and selection contracts

- Use `frame.get_column("x")` when the result must be a `Series`.
- Use `frame.select("x")` when the result must remain a one-column frame.
- Use `select` or selectors for column choice and computation.
- Use `filter` for value-based row choice.
- Use `gather` or a row slice only when row positions themselves are the
  contract; Polars positions are not semantic labels.
- A two-axis eager selection such as `frame[rows, columns]` may be concise for
  positional work, but it does not translate to a pandas label-index contract
  or a lazy query. Prefer named expression APIs in reusable transformations.
- Do not use `df["x"] = values` as a pandas-style transformation. Use
  `with_columns`, which returns a frame and replaces a same-named column.

## Dtype-directed operations

Choose an expression namespace from the column dtype:

| Dtype family | Namespace | Examples of intent |
|---|---|---|
| String | `.str` | normalize, parse, search, split |
| Date/Datetime/Time/Duration | `.dt` | extract calendar fields, offset, truncate, convert timezone |
| Variable-length homogeneous nested values | `.list` | evaluate elements, get, aggregate, explode |
| Fixed-shape homogeneous nested values | `.arr` | fixed-position and fixed-shape operations |
| Named heterogeneous fields | `.struct` | select/rename/unnest fields |
| Categorical/Enum | `.cat` | inspect or transform encoded categories |
| Binary | `.bin` | encode, decode, slice, test prefixes |

Do not convert typed columns to Python objects merely to reach a familiar
Python method. If the required operation is not known, inspect the installed
namespace before introducing a callback.

## API lookup routing

Use the narrowest current reference page when syntax is uncertain:

| Need | Official reference |
|---|---|
| Table operations and returns | `https://docs.pola.rs/api/python/stable/reference/dataframe/index.html` |
| Deferred plan operations | `https://docs.pola.rs/api/python/stable/reference/lazyframe/index.html` |
| Materialized column operations | `https://docs.pola.rs/api/python/stable/reference/series/index.html` |
| Computation recipes and namespaces | `https://docs.pola.rs/api/python/stable/reference/expressions/index.html` |
| Schema-driven column sets | `https://docs.pola.rs/api/python/stable/reference/selectors.html` |
| Dtypes and nested type constructors | `https://docs.pola.rs/api/python/stable/reference/datatypes.html` |
| Readers, scanners, and external sources | `https://docs.pola.rs/api/python/stable/reference/io.html` |

The reference taxonomy helps locate an API; it does not prove that a remembered
signature matches the project. Inspect the installed version for a keyword or
capability that may have drifted.
