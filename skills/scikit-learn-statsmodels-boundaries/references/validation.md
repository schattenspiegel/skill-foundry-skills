# Purpose-specific validation

For predictive work, compare against a simple baseline on untouched data and inspect
discrimination/error, calibration, subgroup behavior, and stability over the deployment
boundary.

For inference, inspect the sampling/design assumptions, functional form, residual or
influence diagnostics where relevant, covariance estimator, multiplicity, sensitivity,
and practical magnitude. Use pre-specified models or independent data for confirmatory
claims after exploratory model selection.

When both outputs are required, publish two validation sections. Do not let one
library's successful fit stand in for the other objective's evidence.
