# statsmodels Python decision guide

        ## Ordered decisions

        1. State estimand, response distribution, link, design formula, intercept, weights, and dependence assumptions before fitting.
2. Choose classical, heteroskedasticity-robust, cluster-robust, or HAC covariance from the sampling process.
3. Inspect dropped rows, rank, convergence, residuals, influence, and model-specific diagnostics before interpreting p-values.
4. Preserve categorical levels and formula transformations when constructing prediction data.
5. Distinguish confidence intervals for the conditional mean from prediction intervals for new observations.
6. Treat association and conditional estimates as causal only when the identification design independently supports that claim.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
