# Bambi testing and version grounding

Inspect the project lock and installed Bambi/PyMC/formulae versions:

```text
python -c "import bambi,pymc; print(bambi.__version__, pymc.__version__)"
```

Inspect signatures for `Model`, `Model.fit`, `Model.predict`,
`Model.prior_predictive`, `Formula`, and `Prior`. Bambi evolves rapidly; formula
features, backend options, default priors, prediction behavior, and unseen-group
handling can change across minors.

Minimum tests:

1. missing columns/values and exact retained row identity;
2. built common/group terms, intercept, interactions, reference levels, and
   design-matrix shape;
3. family/link and response support violations;
4. explicit prior assignment and prior predictive bounds/tails;
5. simulated coefficient and group-variation recovery;
6. multiple-chain diagnostics and posterior predictive discrepancies;
7. prediction with changed row count, reordered categories, missing/new levels,
   unseen groups, and inclusion/exclusion of observation noise;
8. required `InferenceData` groups, dimensions, coords, and log likelihood.

Use statistical tolerances and repeated seeds for recovery; exact samples are
not portable acceptance criteria.
