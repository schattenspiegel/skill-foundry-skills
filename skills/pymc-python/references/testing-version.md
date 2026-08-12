# PyMC testing and version grounding

Inspect the project lock and installed versions before writing APIs:

```text
python -c "import inspect,pymc as pm; print(pm.__version__); print(inspect.signature(pm.sample)); print(inspect.signature(pm.sample_posterior_predictive))"
```

PyMC major versions can change data mutability, dims support, sampling backends,
and predictive controls. The `pymc.dims` module is experimental in current
official documentation; use it only when the target project already adopts and
pins it.

Minimum tests:

1. graph construction and initial log probability are finite;
2. prior predictive shapes/groups and domain bounds;
3. sampled-data recovery for a small seeded fixture;
4. posterior dimensions, chain count, and required sample-stat fields;
5. an intentionally bad parameterization triggers the diagnostic test;
6. in-sample posterior predictive group and out-of-sample predictions group;
7. changed row count, feature ordering, category levels, and coordinates;
8. serialization/reload of the durable `InferenceData` if persistence matters.

Use small tests to prove wiring, not to set production draw counts. Statistical
assertions need tolerances justified by Monte Carlo error and repeated seeds.
