# Design-matrix ownership

The component that learns encoding owns the fitted column contract. Record output
feature names, order, dtype, reference levels, missing-value treatment, and intercept
policy. Preserve row identifiers separately from the numeric matrix.

If a sklearn transformer feeds statsmodels, fit it on the permitted analysis sample,
materialize a named matrix, add or omit an intercept deliberately, and test that
prediction data produces exactly the same columns. Do not infer semantic terms from
anonymous array positions after fitting.
