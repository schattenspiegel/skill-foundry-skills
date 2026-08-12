# NumPyro testing and version grounding

This skill targets the official `pyro-ppl/numpyro` package, not a package named
`numpypro`. Inspect the lock plus JAX/JAXLIB/NumPyro versions and devices:

```text
python -c "import jax,numpyro; print(numpyro.__version__, jax.__version__); print(jax.devices())"
```

Inspect signatures for `MCMC`, `MCMC.run`, `Predictive`, key creation, and any
handler or reparameterizer used. JAX and NumPyro compatibility, device setup,
chain execution, and PRNG APIs drift.

Minimum tests:

1. seeded trace contains the exact site names, observed flags, and value shapes;
2. duplicate sites, wrong plate sizes, and wrong event shapes fail;
3. same key reproduces a test draw while split keys produce independent draws;
4. prior predictive respects support and shape;
5. small simulated-data MCMC recovery and diagnostics;
6. SVI multiple-start stability and comparison to MCMC where SVI is supported;
7. posterior prediction uses `obs=None`, a fresh key, and expected site shapes;
8. representative batch sizes show intended JIT compilation behavior.

Use tolerant statistical properties, not exact stochastic arrays across
platforms, except for narrow same-environment PRNG plumbing tests.
