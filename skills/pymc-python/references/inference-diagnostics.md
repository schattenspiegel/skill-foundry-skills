# PyMC inference and predictive diagnostics

## Before posterior sampling

Draw from the prior predictive. Plot/check scales, bounds, zero mass, tails,
counts, and domain-impossible combinations. Simulate data from known parameters
and test approximate recovery; this exposes sign, link, indexing, and
identifiability errors.

## After sampling

Use multiple chains. Inspect divergences and where they occur, maximum tree
depth, acceptance/energy behavior, BFMI when available, rank-normalized R-hat,
bulk and tail ESS, MCSE relative to the required precision, and parameter-
specific traces. Thresholds are warning gates, not a certificate. Any divergence
requires investigation; raising `target_accept` is a follow-up after checking
parameterization, not the first and only fix.

## Predictive checks

Compare replicated data to observations using discrepancies tied to the model's
purpose: distribution tails, zeros, rates, group spread, temporal dependence,
calibration, or held-out loss. In-sample posterior predictive checks diagnose
fit; predictions on new covariates assess a different task. Keep their
`InferenceData` groups distinct.

For LOO comparison, retain pointwise log likelihood, inspect Pareto-k warnings,
and compare models fit to the same observations and likelihood target. Model
weight is not proof that the winning model is adequate.
