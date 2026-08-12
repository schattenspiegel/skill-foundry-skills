# Pandas migration

Load this reference only for an explicitly requested pandas-to-Polars migration.

## Translate semantics

| Pandas concept | Polars decision |
|---|---|
| Index or MultiIndex | Expose every label level as an ordinary column when it affects alignment, selection, grouping, resampling, ordering, or output. Discard it only after proving it is incidental. |
| Label-aligned arithmetic, assignment, or `concat(axis=1)` | Polars has no implicit label alignment. Join on the exposed label columns; use positional operations only when row position is the proven contract. |
| Column assignment chain | Use expression contexts; split only real dependencies. |
| `groupby().agg()` | Use `group_by().agg()` when output grain is one row per group. |
| `groupby().transform()` | Use `.over(...)` when every input row must remain. |
| Null group keys | Preserve the old `dropna` behavior explicitly. Pandas commonly excludes null-key groups by default; Polars `group_by` includes a null group. |
| `apply(axis=1)` | Decompose into expressions, folds, structs, lists, joins, or windows before a UDF. |
| Merge used as an existence filter | Use semi/anti join. |
| Merge with null keys | Current pandas merge can match null keys to each other; Polars equi-joins do not by default. Use the installed `nulls_equal` option only when equivalence requires null matching. |
| Missing values | Specify null and `NaN` behavior independently. |
| Ordered cumulative/rolling work | Sort by semantic keys and tie-breakers before the window. |

Do not transliterate pandas method names. Polars has no implicit row-label contract, uses stricter dtypes, and expresses most transformations through contexts rather than mutation. Treat pandas defaults and Polars join keywords as version-sensitive: inspect the old call, its tests, and the installed signatures before encoding equivalence.

To reproduce a pandas grouping that excludes null keys, filter those keys before the Polars `group_by`; to reproduce one that retains them, keep the null group and test it. Do not let either library's default choose this policy silently.

## Migration procedure

1. Write an equivalence fixture from the old implementation, including permuted and unmatched labels, duplicate labels or keys, null join keys, null group keys, `NaN`, ordering ties, empty input, and relevant dtypes.
2. State the old input and output grain.
3. Trace every use of the pandas index. Preserve the relevant levels as named columns even when the labels are technical rather than business keys.
4. Replace label alignment with an explicit key join. Assert key uniqueness before choosing a one-to-one alignment; do not substitute horizontal concat merely because fixture rows happen to share an order.
5. Decide null-key join and null-group behavior from the old result, then encode that policy explicitly in Polars.
6. Build the Polars version from native expressions and explicit joins/windows.
7. Compare values, schema, cardinality, missing-value behavior, and contractual order.
8. Convert to pandas only at an actual interoperability boundary.

If the old code's behavior is accidental or ambiguous, do not preserve it silently. Surface the decision and encode the chosen contract in tests.
