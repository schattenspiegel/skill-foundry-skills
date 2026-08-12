# Python UDF contracts

Load this reference only after native expressions, nested expressions, folds, windows, joins, and reshaping have failed to express the required operation.

## Select the exact boundary

| Required callback boundary | Current Polars API | Contract |
|---|---|---|
| One expression as a `Series` batch | `Expr.map_batches` | Callback receives one `Series`; declare the expression result dtype and actual scalar-versus-series shape. |
| Several expressions as `Series` batches | `pl.map_batches` | Callback receives a sequence of `Series` and produces one expression result. |
| A whole lazy-plan node as a `DataFrame` | `LazyFrame.map_batches` | Callback accepts and returns a `DataFrame`; declare the exact output schema when it differs from the input. |
| One Python value at a time | `Expr.map_elements` | Callback receives scalar values; reserve this for irreducible scalar logic. |

These APIs are not interchangeable. The expression forms currently accept `return_dtype`; whole-frame `LazyFrame.map_batches` instead has a frame-level `schema` and output-schema validation contract. Inspect the installed signatures before using drift-sensitive flags.

Current syntax anchors:

```python
one = pl.col("value").map_batches(
    transform_series,
    return_dtype=pl.Float64,
)

many = pl.map_batches(
    ["numerator", "denominator"],
    combine_series,
    return_dtype=pl.Float64,
)

whole = lazy_frame.map_batches(
    transform_frame,
    schema={"id": pl.Int64, "score": pl.Float64},
)
```

## Safety rules

- Declare `return_dtype` for expression and scalar UDFs. Set a scalar-result flag only when the callback truly returns one value for its evaluation context.
- For `LazyFrame.map_batches`, return a Polars `DataFrame`. Keep output-schema validation enabled and provide the full output schema when columns or dtypes change.
- Keep whole-frame optimizer pushdown flags disabled unless equivalence tests prove the callback commutes with that projection, predicate, or slice. A performance guess is not proof.
- Mark an expression UDF elementwise only when it returns the same length and applying it to arbitrary slices produces the same concatenated result.
- Mark a whole-frame UDF streamable only when arbitrary input partitioning produces the same ordered result and schema. Global aggregations, sorting, ranking, and state across batches usually fail this contract.
- Do not depend on a particular batch size or number of callback invocations. Keep callbacks pure and deterministic unless the task explicitly defines another contract.
- Decide whether nulls reach the callback. Current `map_elements` can skip null values; test the chosen behavior rather than relying on its default.
- Define exception behavior and test typed empty, all-null, single-row, multiple-batch, and relevant grouped contexts.

Measure representative data before accepting a Python callback in a hot path. Use an existing compiled expression plugin only when project scope authorizes that dependency and its semantics are covered by the same fixtures.
