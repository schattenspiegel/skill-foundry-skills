# ArviZ inference-data contract

ArviZ 1.x uses an xarray `DataTree` as its inference container. Some upstream
integrations and older projects still call or return `InferenceData`; inspect
the installed boundary instead of assuming the 0.x container API. The
container organizes semantically distinct xarray groups. Typical groups include
posterior/prior latent draws, sample statistics, pointwise log likelihood,
posterior/prior predictive replicated observations, out-of-sample predictions,
observed data, and constant inputs.

## Dimension rules

- `chain` identifies independent MCMC runs.
- `draw` identifies iteration within a chain.
- `sample` may represent a stacked sample identity but must not be used before
  chain-aware diagnostics.
- `pred_id` can identify repeated predictive values per posterior sample.
- Domain dimensions such as `feature`, `school`, or `observation` require
  coordinates whose values and lengths match the originating model.

Dimension names carry meaning; order alone does not. Every variable is named,
and groups without sampled quantities (for example observed data) omit sample
dimensions.

## Conversion invariants

Before conversion, identify the backend's raw axis order and warmup content.
For ArviZ 1.x, pass a nested group mapping to `from_dict`, for example
`{"posterior": {"beta": values}}`; do not use the removed 0.x
`posterior=...` keyword form. Supply explicit dims/coords mappings, assert
coordinate uniqueness, and reject ambiguous flattened samples. When merging,
require compatible group schemas and coordinates; never silently overwrite a
group with a different observation set.
