# NumPyro program and shape contract

A model is ordinary Python interpreted by NumPyro primitives and effect
handlers. Each `sample` site has a stable name, distribution, observed or latent
status, and value shape. Posterior dictionaries and guides join to the model by
site name.

## Shape derivation

For every site write:

```text
distribution batch shape + distribution event shape -> sampled value shape
plate axes -> conditionally independent batch dimensions
```

A plate declares independence and may scale a subsampled likelihood. An event
axis is one joint outcome and contributes one log-probability event. Do not use
`.to_event` to silence a plate warning: it changes probability semantics.

## Handler boundary

Use `trace` plus `seed` for structural tests; use `condition`/`substitute` only
when their value and shape contract is known; use `mask`/`scale` for mathematically
defined likelihood changes. Handler nesting order can matter, so keep it local
and covered by a test.

## Stable execution

The set of sites and their shapes should not vary with array data inside a JIT
trace. Express array branching with JAX operations or supported control-flow
primitives. Validate ragged, missing, or categorical input before the model and
represent its policy explicitly.
