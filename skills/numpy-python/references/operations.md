# Operations, broadcasting, and numerical rules

## Broadcasting

Align shapes from the right. Each aligned pair must be equal or one. Missing
leading dimensions behave as one. Insert semantic axes explicitly:

```python
# observations: (samples, features); weights: (samples,)
weighted = observations * weights[:, None]
```

Use `broadcast_shapes` to validate without allocating. Estimate the result and
temporary sizes; vectorization can be slower when it materializes an enormous
outer difference.

## Indexing and mutation

Combine boolean/integer selection and assignment in one operation. Confirm
boolean mask shape and whether repeated integer indices require accumulation
(`np.add.at`) rather than last-write behavior. Negative indices are valid Python
positions, not missing sentinels.

## Reductions

Always decide `axis`; `axis=None` flattens the semantic tensor. Use `keepdims`
when the result will broadcast back. Define empty behavior via `initial`, domain
rules, or explicit rejection. Distinguish `argmax` position from maximum value
and map positions back through the intended axis.

## Numerics

Use stable specialized functions (`log1p`, `expm1`, `hypot`, `logaddexp`) near
problematic regimes. For comparisons, choose `allclose` tolerances from scale
and algorithm, and also compare shape/dtype/nonfinite positions. Use `errstate`
to make divide/overflow/invalid handling local; never silence warnings globally
without checking results.
