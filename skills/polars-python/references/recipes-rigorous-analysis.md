# Rigorous Polars analytical practice and recipes

Use this checklist for consequential transformations, joins, aggregations, and
analytical pipelines. It is a rigorous-computation standard, not a description
of any mathematician's private workflow.

## Frame semantics before expressions

1. **Define the population.** State which records are eligible and which
   filters/exclusions implement that definition.
2. **Name the row grain.** Write “one row per …” for every input, intermediate,
   and output whose grain can change.
3. **Identify keys and multiplicity.** Distinguish record identifiers from
   grouping dimensions and test uniqueness where claimed.
4. **Define each metric.** Record numerator, denominator, units, currency,
   inclusions, exclusions, and zero-denominator behavior.
5. **Keep missing distinct.** Null, `NaN`, zero, absent entity, unavailable, and
   not-applicable states need separate policies.
6. **Define time semantics.** Establish event versus snapshot time, timezone,
   period completeness, interval closure, and required ordering.
7. **Define survivor semantics.** Deduplication requires keys, winner/tie-break
   rule, and final order—not merely `unique`.
8. **Preserve units and domains.** Do not add currencies, durations, or counts
   from incompatible domains without an explicit conversion.

## Design the transformation

9. **Choose the Polars object deliberately.** Separate materialized
   `DataFrame`/`Series`, symbolic `Expr`, and deferred `LazyFrame` contracts.
10. **Classify every shape change.** Mark operations as row preserving,
    filtering, expanding, collapsing, or combining before choosing context.
11. **Make schema a contract.** Pin identifiers, temporal/nested fields, empty
    inputs, and dirty boundaries where inference can change meaning.
12. **Build a dependency graph.** Put dependent aliases in later expression
    stages; do not rely on textual order inside one context.
13. **Aggregate components before ratios.** Usually compute
    `sum(numerator) / sum(denominator)`, not an unweighted mean of row/group
    rates.
14. **Choose joins from grain.** State left/right grain, key domains,
    uniqueness, expected cardinality, null matching, unmatched policy, and
    contractual order before joining.
15. **Keep native expressions until a proven boundary.** A Python callback or
    row conversion needs an explicit schema, purity, null, batch, and scale
    contract.
16. **Place materialization at the consumer.** A streaming collect may reduce
    intermediate memory but still materializes its final `DataFrame`.
17. **Estimate scale before shape expansion.** Bound join fan-out, explode
    multiplicity, pivot width, and cross products before execution.
18. **Define output order explicitly.** If a consumer cares, encode sort keys
    and tie-breakers rather than preserving observed engine order.

## Validate with independent pressure

19. **Check structural invariants.** Assert output object, columns, dtypes,
    grain, key uniqueness, row count, and order.
20. **Reconcile arithmetic.** Compare components with totals, subgroup sums with
    overall values, and pre/post conserved measures.
21. **Audit joins after execution.** Measure null fact keys, unmatched non-null
    fact rows, unused dimension keys, result rows, and measure multiplication.
22. **Test typed empties.** Empty input must preserve the promised output schema
    or fail under an explicit nonempty precondition.
23. **Test dirty and boundary values.** Include null, `NaN`, zero denominator,
    duplicate keys, invalid casts, and temporal boundaries.
24. **Permute arrival order.** If the result should be order independent,
    shuffle/reverse input and compare after the contractual final sort.
25. **Partition row-local work.** Apply it whole and by batches, concatenate,
    and compare; disagreement exposes hidden global or batch dependence.
26. **Compare execution forms.** Where semantics should agree, compare eager
    and lazy results or the production query with a direct small reference.
27. **Inspect only relevant plan properties.** Use `collect_schema` and an
    optimized plan to prove schema/pushdown claims, not to snapshot unstable
    plan spelling.
28. **Use typed expected frames.** Assert schema and semantics separately from
    presentation; choose tolerances from metric units and consequences.

## Communicate the evidence boundary

29. **Separate generated, executed, and validated.** Code or a lazy plan that
    was produced but not run is not execution evidence.
30. **Stop at unresolved semantics.** If grain, metric definition, join domain,
    or reconciliation cannot be established, return the missing evidence or
    fail explicitly instead of presenting a plausible table as trustworthy.

## Recipe `polars.reconciled-weighted-rate`

**Use when:** integer numerator/denominator counts must be summarized by a
non-null grouping key and reconciled to an overall rate.

**Inspect first:** population, group grain, count-column domains, zero-
denominator policy, output order, and whether numerator must be bounded by the
denominator.

**Invariants:** Counts are non-null, nonnegative integers with numerator no
larger than denominator; grouped components equal overall components; rate is
the ratio of summed components and is null when its denominator is zero.

```python
import polars as pl


def summarize_rate(
    frame: pl.DataFrame,
    *,
    group_col: str,
    numerator_col: str,
    denominator_col: str,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    required = (group_col, numerator_col, denominator_col)
    if len(set(required)) != 3 or any(name not in frame.columns for name in required):
        raise ValueError("group, numerator, and denominator columns must be distinct and present")
    invalid = frame.select(
        (
            pl.col(group_col).is_null()
            | pl.col(numerator_col).is_null()
            | pl.col(denominator_col).is_null()
            | (pl.col(numerator_col) < 0)
            | (pl.col(denominator_col) < 0)
            | (pl.col(numerator_col) > pl.col(denominator_col))
        ).any()
    ).item()
    if invalid:
        raise ValueError("invalid grouping key or count relationship")
    schema = frame.schema
    if not schema[numerator_col].is_integer() or not schema[denominator_col].is_integer():
        raise TypeError("numerator and denominator must use integer count dtypes")

    components = (
        frame.group_by(group_col)
        .agg(
            pl.col(numerator_col).sum().alias("numerator_total"),
            pl.col(denominator_col).sum().alias("denominator_total"),
        )
        .sort(group_col)
    )
    grouped = components.with_columns(
        rate=pl.when(pl.col("denominator_total") != 0)
        .then(pl.col("numerator_total") / pl.col("denominator_total"))
        .otherwise(None)
    )
    overall = frame.select(
        pl.col(numerator_col).sum().alias("numerator_total"),
        pl.col(denominator_col).sum().alias("denominator_total"),
    ).with_columns(
        rate=pl.when(pl.col("denominator_total") != 0)
        .then(pl.col("numerator_total") / pl.col("denominator_total"))
        .otherwise(None)
    )
    if components.select("numerator_total", "denominator_total").sum().row(0) != overall.row(0)[:2]:
        raise AssertionError("grouped components do not reconcile to overall components")
    return grouped, overall
```

**Do not use when:** inputs are continuous weights, groups overlap, the overall
population differs from the grouped population, or numerator can legitimately
exceed denominator.

**Verify:** Test unequal group sizes, zero denominators, typed empty input,
invalid/null counts, input-order permutation, and exact component reconciliation.

## Recipe `polars.audited-m1-enrichment`

**Use when:** fact-grain rows are enriched from unique dimension keys and the
caller needs explicit coverage diagnostics.

**Inspect first:** fact/dimension grains, key dtype/domain, enrichment columns,
null policy, expected unmatched/unused keys, and required fact order.

**Invariants:** Dimension keys are unique and non-null, key dtypes agree,
enrichment cannot overwrite fact columns, left row count/order remain stable,
and the audit separates null fact keys from unmatched non-null rows.

```python
def audited_m1_enrichment(
    facts: pl.DataFrame,
    dimension: pl.DataFrame,
    *,
    key: str,
    columns: list[str],
) -> tuple[pl.DataFrame, pl.DataFrame]:
    if key not in facts.columns or key not in dimension.columns:
        raise ValueError("join key must exist on both sides")
    if facts.schema[key] != dimension.schema[key]:
        raise TypeError("join key dtypes must match")
    if not columns or len(columns) != len(set(columns)):
        raise ValueError("enrichment columns must be unique and nonempty")
    if any(name == key or name not in dimension.columns for name in columns):
        raise ValueError("invalid enrichment column")
    if any(name in facts.columns for name in columns):
        raise ValueError("enrichment must not overwrite fact columns")
    if dimension.select(pl.col(key).is_null().any()).item():
        raise ValueError("dimension keys must be non-null")
    projected = dimension.select(key, *columns)
    if projected.select(key).is_duplicated().any():
        raise ValueError("dimension key must be unique")

    null_fact_keys = facts.filter(pl.col(key).is_null()).height
    nonnull_facts = facts.filter(pl.col(key).is_not_null())
    dimension_keys = projected.select(key)
    unmatched_fact_rows = nonnull_facts.join(dimension_keys, on=key, how="anti").height
    used_fact_keys = nonnull_facts.select(key).unique()
    unused_dimension_keys = dimension_keys.join(used_fact_keys, on=key, how="anti").height
    result = facts.join(
        projected,
        on=key,
        how="left",
        validate="m:1",
        nulls_equal=False,
        maintain_order="left",
    )
    if result.height != facts.height:
        raise AssertionError("join changed fact grain")
    audit_columns = (
        "fact_rows",
        "dimension_rows",
        "result_rows",
        "null_fact_keys",
        "unmatched_fact_rows",
        "unused_dimension_keys",
    )
    audit = pl.DataFrame(
        {
            "fact_rows": [facts.height],
            "dimension_rows": [dimension.height],
            "result_rows": [result.height],
            "null_fact_keys": [null_fact_keys],
            "unmatched_fact_rows": [unmatched_fact_rows],
            "unused_dimension_keys": [unused_dimension_keys],
        },
        schema={name: pl.UInt64 for name in audit_columns},
    )
    return result, audit
```

**Do not use when:** the relationship is genuinely many-to-many, null keys
should match, unmatched facts must be rejected, or the enrichment changes grain.

**Verify:** Test duplicate/null dimension keys, dtype mismatch, null and
unmatched fact keys, unused dimension keys, input order, empty inputs, and row
count preservation.

## Recipe `polars.verify-row-local-transform`

**Use when:** a transformation is claimed to operate independently per row and
must behave identically under row permutation and batch partitioning.

**Inspect first:** unique non-null record key, expected output schema, whether
the transformation truly has no global/window/order dependence, and comparison
tolerances.

**Invariants:** Input and output contain the same unique keys and row count;
whole, reversed, partitioned, and typed-empty executions agree after sorting by
the key; the input is not mutated.

```python
import math
from collections.abc import Callable

from polars.testing import assert_frame_equal


def verify_row_local_transform(
    transform: Callable[[pl.DataFrame], pl.DataFrame],
    frame: pl.DataFrame,
    *,
    key: str,
    rel_tol: float = 1e-12,
    abs_tol: float = 1e-15,
) -> pl.DataFrame:
    if not math.isfinite(rel_tol) or not math.isfinite(abs_tol) or rel_tol < 0 or abs_tol < 0:
        raise ValueError("comparison tolerances must be finite and nonnegative")
    if key not in frame.columns or frame.select(pl.col(key).is_null().any()).item():
        raise ValueError("verification key must exist and be non-null")
    if frame.select(key).is_duplicated().any():
        raise ValueError("verification key must be unique")
    before = frame.clone()

    def normalized(source: pl.DataFrame) -> pl.DataFrame:
        result = transform(source)
        if not isinstance(result, pl.DataFrame):
            raise TypeError("transform must return DataFrame")
        if key not in result.columns or result.height != source.height:
            raise AssertionError("transform changed record grain")
        if (
            result.select(pl.col(key).is_null().any()).item()
            or result.select(key).is_duplicated().any()
        ):
            raise AssertionError("transform corrupted record keys")
        return result.sort(key)

    baseline = normalized(frame)
    assert_frame_equal(baseline.select(key), frame.select(key).sort(key), check_exact=True)
    assert_frame_equal(normalized(frame.reverse()), baseline, rel_tol=rel_tol, abs_tol=abs_tol)
    split = max(1, frame.height // 2)
    partitioned = pl.concat(
        [transform(frame.slice(0, split)), transform(frame.slice(split))],
        how="vertical",
    ).sort(key)
    assert_frame_equal(partitioned, baseline, rel_tol=rel_tol, abs_tol=abs_tol)
    assert_frame_equal(
        normalized(frame.head(0)), baseline.head(0), rel_tol=rel_tol, abs_tol=abs_tol
    )
    assert_frame_equal(frame, before, check_exact=True)
    return baseline
```

**Do not use when:** the transform intentionally aggregates, filters, expands,
uses windows/cumulative state, or depends on order or batch-global statistics.

**Verify:** Run a true row-local expression plus known-bad transforms that use
global means, cumulative order, row dropping, duplicate keys, or wrong returns.
