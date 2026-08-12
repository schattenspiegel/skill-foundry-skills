# Bambi formula and model contract

The first formula maps a response to predictors. An intercept is controlled by
formula syntax. Main effects, interactions, transforms, and categorical coding
produce concrete design-matrix terms whose names become prior/result interfaces.

## Group-specific terms

`(1 | group)` is a varying intercept. `(1 + x | group)` includes varying
intercept and slope. These coefficients come from population distributions and
share information across groups. Check group counts, observations per group,
the group identifier dtype, and whether a correlated/independent parameterization
is actually supported by the installed version.

## Distributional formulas

A `Formula` can include additional formulas for non-parent likelihood parameters
when the family supports them. Each adds an estimand and prior surface; use only
when varying that parameter is scientifically justified.

## Built model

`Model.build()` produces the PyMC backend graph. Inspect the formula summary,
observations retained, family/link, term names, priors, design matrices, and
backend variables before fitting. Model inputs remain pandas columns; prediction
data must satisfy the same formula namespace, category coding, and transforms.
