# Lazy execution and performance

Load this reference for file-backed pipelines, memory pressure, repeated execution, or an optimization claim.

## Memory and execution decision

| Need | Action |
|---|---|
| Optimizable file-backed plan | Use `scan_*`, build a `LazyFrame`, execute at the consumer. |
| Small already-materialized one-step work | Eager execution may be clearer and sufficient. |
| Final `DataFrame` fits memory but intermediates are large | Keep the plan lazy and test the installed streaming engine at the terminal collect. |
| Final `DataFrame` may not fit memory | Do not collect. Change the consumer contract to a file or batch boundary. |
| File is the final consumer | Prefer a supported `sink_*` whose installed execution semantics are verified. |
| Incremental processing is the final consumer | Use an installed batch collection or sink API only after testing its stability, ordering, and memory behavior. |
| Several outputs share a base plan | Use the installed multi-query execution API when it actually shares work. |

Streaming is an execution strategy, not an output container. In current Polars, a streaming collect still returns a materialized `DataFrame`, and an operation unsupported by the streaming engine can fall back to in-memory execution. Verify the installed engine and terminal API rather than treating `streaming` as proof of bounded memory.

A reused `LazyFrame` is not a promise of caching. Separate executions may recompute its plan. Do not insert `cache()` by intuition; inspect the optimized plan and measure.

## Plan inspection

Use `collect_schema()` for schema validation and `explain()` for plan diagnosis. Compare optimized and non-optimized plans when a regression concerns:

- projection pushdown: only required source columns are read;
- predicate pushdown: source predicates reach the scan;
- slice pushdown: small terminal slices avoid full materialization;
- repeated source scans or subplans;
- joins, sorts, order preservation, or UDF nodes that block optimization.

Do not assert durable behavior from exact plan text across an unpinned version range. In a pinned regression fixture, assert only the relevant plan property.

```python
query = (
    pl.scan_parquet(path)
    .filter(pl.col("status") == "paid")
    .select(
        "customer_id",
        (pl.col("amount_cents") / 100).alias("amount"),
    )
)

print(query.explain(optimized=True))
```

The relevant evidence is that source filtering and column projection reach the
scan. A visually shorter plan is not itself a performance proof.

For streaming-sensitive work, inspect the physical plan when the installed API supports it. Current Polars exposes a physical streaming graph through the equivalent of:

```python
query.show_graph(plan_stage="physical", engine="streaming")
```

Confirm the exact installed signature, then look for in-memory fallbacks and blocking operators. A logical `explain()` alone does not prove streaming execution.

## Performance procedure

1. Lock semantic equivalence with frame and schema assertions.
2. Reproduce the slow boundary with representative data scale and shape.
3. Remove accidental collects, Python-object conversion, and row callbacks.
4. Check whether source predicates and projections reach the scan.
5. Estimate final-result size separately from intermediate pressure. If the final `DataFrame` cannot fit, change the consumer contract.
6. Test streaming, sink, or batch execution only after verifying installed signatures, supported operators, ordering, and output equivalence.
7. Measure the same boundary before and after; report data size, version, engine, and statistic.

`maintain_order`, stable sorts, rechunking, Python UDFs, and conversions to pandas/NumPy can carry real costs. Use each only for an explicit semantic or interoperability requirement.
