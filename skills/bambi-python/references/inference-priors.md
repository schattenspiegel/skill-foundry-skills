# Bambi families, priors, and inference

## Family and link

Choose the likelihood from outcome support and the data-generating process.
Check bounds, trials/exposure, zero mass, overdispersion, tails, and variance
structure. A link maps the linear predictor to a valid likelihood parameter and
changes coefficient interpretation. Custom families require a supported
likelihood, parameter set, links, and predictive/log-likelihood behavior.

## Priors

`Prior` names backend distributions and their parameters; nested priors define
hierarchical scales. Priors map to built term names, not arbitrary dataframe
column names. Inspect automatic scaling and predictor centering, then set
explicit priors where scientific scale matters. Use prior predictive simulation
to validate implied outcomes.

## Fit and predict

`Model.fit()` delegates inference to a backend and returns labeled inference
results. Record backend and sampler settings. Diagnose with the same PyMC/ArviZ
standards as a hand-built model. `predict` may add mean-parameter or response
draws depending on installed arguments; state whether observation noise and
group-specific effects are included and whether results are in-place. Treat new
groups through an explicit supported policy.
