# ArviZ diagnostics and comparison

## Sampling diagnostics

Inspect rank-normalized/folded R-hat, bulk and tail ESS, MCSE, traces/ranks,
autocorrelation, and sampler-specific statistics such as divergences, energy,
acceptance, and tree depth. Report the affected variable plus coordinate. One
healthy scalar cannot clear another problematic dimension.

For one chain, state that between-chain convergence is untested. ESS and trace
behavior quantify sampling efficiency but cannot establish exploration of all
modes. More draws reduce Monte Carlo error only after geometry/mixing problems
are resolved.

## Predictive diagnosis

Select discrepancies before looking at replicated results where possible:
location, spread, tails, zeros, maximum, group variation, temporal dependence,
calibration, or held-out predictive loss. Keep posterior predictive and
out-of-sample prediction groups distinct.

## Comparison

PSIS-LOO operates on pointwise log likelihood. Candidate models must use the
same observation identity and predictive target. Inspect Pareto-k by observation
and uncertainty in differences. If importance sampling is unreliable, use a
more robust refit/cross-validation procedure. Weights summarize a candidate set;
they are not posterior probabilities that a model is true.
