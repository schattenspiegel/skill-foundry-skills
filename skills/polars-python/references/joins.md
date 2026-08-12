# Join rules

Load this reference before changing a non-trivial equi, as-of, non-equi, or cross join.

## Join contract

Write down:

- which left and right rows must survive;
- left and right key domains and dtypes;
- expected uniqueness on each side;
- whether null keys may match;
- expected output key columns and suffixes;
- whether output order is contractual.

## Choose from row semantics

| Need | Strategy |
|---|---|
| Only matching rows | inner |
| Every left row plus right matches | left |
| Every row from either side | full |
| Filter left rows by right-side existence | semi |
| Keep left rows absent on the right | anti |
| Nearest ordered key, usually temporal | as-of |
| Predicate rather than equal keys | non-equi, after bounding multiplicity |
| Every pairing | cross, only for an intentional bounded product |

Use semi/anti joins for existence checks; they do not import right-side columns or multiply left rows because of duplicate right keys.

Treat an installed `join_where` as version-sensitive and potentially
experimental. Either side may match several rows and output order is not
preserved. Bound the multiplicity, test duplicate matches, and restore order
explicitly only when the contract requires it.

## Key dtype decision

| Condition | Action |
|---|---|
| Dtypes and semantic domains match | Join directly. |
| Domains match and one lossless canonical conversion exists | Normalize once at the input boundary and test boundary values. |
| Conversion may lose precision, strip leading zeros, change time zones, or merge distinct values | Fail with a descriptive mismatch. |
| Semantic equivalence is unknown | Inspect upstream schema or ask; do not cast both sides to a convenient type. |

## Cardinality guard

| Contract | Required uniqueness |
|---|---|
| one-to-one | both sides |
| one-to-many | left side |
| many-to-one | right side |
| many-to-many | neither, but multiplication must be intentional |

Use the installed validation parameter when it supports the contract. If it does not, assert uniqueness on the constrained side before the join. Always test duplicate keys and output row count. Never deduplicate silently to make a failing contract pass.

Cardinality validation and streaming support are separate capabilities. If the
installed streaming join cannot enforce the declared cardinality, choose one:

| Constraint | Action |
|---|---|
| Cardinality proof is required and an in-memory result fits | Use the validated engine. |
| Streaming is required | Run an explicit uniqueness preflight on the constrained side, report the extra scan, then test join row counts. |
| Neither an extra scan nor in-memory execution is acceptable | Report the contract conflict; do not silently drop validation. |

For a current API whose contract is left-preserving and many-to-one:

```python
result = orders.join(
    customers,
    on="customer_id",
    how="left",
    validate="m:1",
    nulls_equal=False,
    maintain_order="left",
)
```

This syntax is an anchor, not a timeless signature. Confirm drift-sensitive
keywords against the installed version. Align key dtypes before the join only
after proving a lossless, same-domain conversion.

## Nulls, keys, and order

Null keys do not match by default. Enable null equality only when the domain explicitly defines two missing keys as the same entity. Choose key coalescing and suffix behavior from the required output schema; do not accept defaults blindly for full joins or expression keys.

Do not rely on observed join order. Request order preservation only when it is part of the contract because it can restrict optimization. Otherwise compare results after a test-only sort.

## As-of join checklist

Before `join_asof`, establish:

1. both sides use compatible ordered-key dtypes;
2. data is sorted by the required key within grouping keys;
3. `backward`, `forward`, or `nearest` matches the temporal rule;
4. tolerance prevents stale matches;
5. exact-match behavior is explicit;
6. original output order is restored when required.

Include a no-match row, an equal-time row, a stale row outside tolerance, multiple groups, and unsorted input in tests. Inspect the installed signature rather than guessing keyword names.

When the caller requires original event order, preserve it explicitly around
the ordered match:

```python
result = (
    events.with_row_index("__input_order")
    .sort("symbol", "event_time")
    .join_asof(
        quotes.sort("symbol", "quote_time"),
        left_on="event_time",
        right_on="quote_time",
        by="symbol",
        strategy="backward",
        tolerance="5m",
    )
    .sort("__input_order")
    .drop("__input_order")
)
```

Use temporary names that cannot collide with project columns, or fail on a
collision. Sorting is part of correctness here, not a performance suggestion.
