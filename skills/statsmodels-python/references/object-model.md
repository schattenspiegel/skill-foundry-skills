# statsmodels Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `model specification`

A likelihood or estimating-equation family plus design. The critical boundary is: Formula coding, intercept, link, and covariance assumptions define estimands.

## `fitted result`

Parameters, covariance, diagnostics, and prediction methods. The critical boundary is: Check convergence and data rows retained before inference.

## `design matrix`

Encoded predictors with column semantics. The critical boundary is: Categorical levels and transformations must match prediction data.

## `covariance estimator`

An uncertainty model such as classical, HC3, cluster, or HAC. The critical boundary is: Choose it from dependence and sampling, not coefficient preference.

## `prediction frame`

Mean and possibly observation uncertainty at new exog. The critical boundary is: Mean confidence and observation intervals answer different questions.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
