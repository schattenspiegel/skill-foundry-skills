# SciPy solver contracts

Adapt symbolic functions to the exact solver interface:

- scalar root: scalar input and scalar finite residual;
- vector root or least squares: one-dimensional residual vector with stable length;
- minimize: scalar objective plus correctly shaped optional gradient/Hessian;
- integrate: callable argument order required by the integration function.

Scale variables and residuals when magnitudes differ materially. Preserve constraints
explicitly. A solver's `success` indicates its termination criterion, not that the
mathematical model or selected solution is correct.
