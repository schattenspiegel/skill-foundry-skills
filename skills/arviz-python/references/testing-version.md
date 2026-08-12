# ArviZ testing and version grounding

Inspect the lock and installed API before copying an older example:

```text
python -c "import arviz as az; print(az.__version__); print(az.__file__)"
```

ArviZ 1.x reorganizes functionality across its ecosystem and uses xarray
`DataTree` as the inference container. Inspect signatures for conversion,
stats, plotting, persistence, and comparison functions. In particular,
`from_dict` takes a nested group mapping and `compare` performs PSIS-LOO without
the removed 0.x `ic="loo"` argument. Do not assume a 0.x import path, group
access pattern, keyword, or return type remains current.

Minimum tests:

1. required groups and exact variable names;
2. chain, draw, and domain dimensions plus coordinate values;
3. reject swapped, flattened, unequal-chain, or ambiguous sample axes;
4. synthetic well-mixed and deliberately stuck chains for diagnostics;
5. missing sampler-stat and log-likelihood groups produce explicit unknown/error;
6. posterior predictive versus predictions group selection;
7. model comparison rejects different observation coordinates;
8. persisted inference artifact reloads with equivalent groups, dims, coords,
   dtypes, and attributes required for provenance.

Avoid exact stochastic thresholds in tiny tests. Assert direction and warning
behavior on strong synthetic counterexamples.
