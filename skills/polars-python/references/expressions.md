# Expression and shape rules

Load this reference when the bug involves expression contexts, conditionals, windows, selectors, nested columns, concat, or reshape.

## Context invariants

| Context | Shape invariant |
|---|---|
| `select` | Returns only requested outputs; expressions must have compatible lengths or scalars. |
| `with_columns` | Preserves input height and existing columns unless replaced. |
| `filter` | Preserves columns and retains only rows whose predicate is true; null predicates are not true. |
| `group_by().agg()` | Produces one row per group. |
| `.over()` | Maps a group computation back to rows according to its mapping strategy. |

Sibling expressions see the input schema, not aliases created by siblings. Keep independent work in one context; use successive contexts for dependencies.

## High-value traps

- Strings in expression positions are normally column references. Use `pl.lit("value")` for a string value in conditional branches.
- Use `(predicate_a) & (predicate_b)`, `|`, and `~`. Python boolean operators do not compose expressions.
- All `when` branches must be valid independently; conditions select results after branch expressions are evaluated.
- A bare aggregation in `with_columns` broadcasts a global scalar. Add `.over(keys)` for a per-group value aligned to rows.
- `pl.len()` counts rows, including rows whose target value is null. `pl.col("value").count()` counts non-null values. Name the intended metric in code and test a null-containing group.
- A bare column inside `group_by(...).agg(...)` collects the group values into a `List`. Apply `sum`, `first`, `len`, or another explicit reduction when the output must be scalar.
- Scalar derived expressions inherit a root output name. Use `.alias`; use `.name.prefix`, `.name.suffix`, or another name operation for expression expansion.
- A dtype or selector expression may expand to zero, one, or many columns depending on schema. Test the expected output names.

## Canonical dependent transformation

Use successive contexts only where one derived column consumes another. Keep
independent work together, preserve unknown passthrough columns with
`with_columns`, and wrap string values with `pl.lit`:

```python
def enrich(frame: pl.DataFrame) -> pl.DataFrame:
    return (
        frame.with_columns(
            net=pl.col("gross") / 1.2,
            segment=(
                pl.when(pl.col("spend").is_null())
                .then(pl.lit("unknown"))
                .when(pl.col("spend") >= 1_000)
                .then(pl.lit("gold"))
                .otherwise(pl.lit("standard"))
            ),
        )
        .with_columns(tax=pl.col("gross") - pl.col("net"))
    )
```

Putting `tax` beside `net` in the first call is incorrect: sibling expressions
cannot see the new `net` alias. Replacing `with_columns` with `select` is also a
semantic change because it drops unspecified inputs.

## Nested data and shape changes

Use `List` for variable-length values and `Array` for fixed-shape values. Prefer `.list`, `.arr`, `.struct`, and `list.eval(pl.element())` to Python element callbacks. Use a Struct to keep related fields together or to pass several columns through one expression.

```python
normalized = frame.with_columns(
    pl.col("tags")
    .list.eval(pl.element().str.strip_chars().str.to_lowercase())
    .list.drop_nulls()
)
```

The native list expression preserves null lists and empty lists as different
states. Test both before adding `explode`, which would change row grain.

`explode` changes row grain. Its null/empty-container options and defaults are
version-sensitive; set the required policy when available and test null lists,
empty lists, list lengths, and resulting row count. `unnest` changes columns;
test field names, dtypes, and collisions.

## Concat and reshape

| Contract | Operation |
|---|---|
| Append matching schemas | vertical concat |
| Append with intentional common-supertype coercion | relaxed vertical concat |
| Union different schemas with null-filled fields | diagonal concat |
| Align equal-height columns by row position | horizontal concat, only with a positional invariant |
| Null-pad intentionally unequal positional inputs | the installed horizontal-extension mode |
| Align records by a semantic key | join, not horizontal concat |

For pivoting, state index columns, generated-column source, values, duplicate-cell policy, and generated-column order.

| Pivot condition | Action |
|---|---|
| Generated categories are known and the installed lazy API supports them | Keep the plan lazy and pass the categories explicitly. |
| Categories are data-dependent | Perform bounded discovery or cross an explicit eager boundary; do not guess the output schema. |
| More than one value maps to an `(index, generated column)` cell | Choose an explicit aggregation or fail on the uniqueness contract. |

Current lazy APIs may require an explicit category list and may be unstable.
Inspect the installed signature. For unpivoting, state identifier columns and
expected row multiplication.

```python
wide = source.pivot(
    "region",
    on_columns=["north", "south"],
    index="sku",
    values="revenue",
    aggregate_function="sum",
)
```

```python
combined = pl.concat([historical, current], how="diagonal_relaxed")
```

Use this only when the contract is both union-by-name and common-supertype
coercion. Use `diagonal` if exact shared dtypes are required; neither mode is a
substitute for keyed alignment.

## Windows

| Required result | Operation |
|---|---|
| Group aggregate aligned to each input row | Aggregate expression with `.over(keys)`. |
| Cumulative, shift, or diff within groups | `.over(keys, order_by=...)` with a deterministic tie-breaker. |
| Rank within groups | Rank the target expression, choose its tie method and null policy, then use `.over(keys)`. |
| Fixed temporal buckets | `group_by_dynamic` with explicit boundaries. |
| Trailing temporal window at each observation | `rolling` or an installed `rolling_*_by` expression. |
| Fixed row-count window | Ordinary rolling expression with explicit row order. |

Use the default window mapping when outputs align one-to-one; use list or
explode mapping only when repeated lists or reordered rows are the intended
shape. Load `time-series.md` directly from `SKILL.md` for temporal sortedness,
calendar durations, boundaries, and time zones.

```python
running = (
    frame.sort("account_id", "occurred_at", "sequence")
    .with_columns(
        pl.col("amount").cum_sum().over("account_id").alias("running_amount")
    )
)

history = (
    events.group_by("account_id")
    .agg(
        pl.col("value")
        .sort_by(
            ["event_time", "sequence"],
            nulls_last=[True, False],
        )
        .alias("values")
    )
    .sort("account_id")
)
```

The first keeps row grain; the second creates one row per account. Sorting the
group rows does not sort values inside each aggregated list, so encode both
orders separately.
