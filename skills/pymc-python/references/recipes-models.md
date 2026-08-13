# PyMC model construction recipes

Use these only after the generative assumptions, support, shape, and coordinate
contracts are explicit. A familiar distribution name is not model validation.

## Recipe `pymc.noncentered-hierarchy`

**Use when:** Group effects need partial pooling and a centered hierarchy may form a funnel.
**Inspect first:** Validate observation/group alignment, group index bounds, and scientific prior scales.
**Invariants:** Group and observation axes are named; the raw effect is standard normal and transformed once.

```python
import numpy as np
import pymc as pm


def build_hierarchy(y: np.ndarray, group_idx: np.ndarray, group_names: list[str]) -> pm.Model:
    if y.ndim != 1 or group_idx.shape != y.shape:
        raise ValueError("y and group_idx must be aligned vectors")
    if group_idx.size and (group_idx.min() < 0 or group_idx.max() >= len(group_names)):
        raise ValueError("group index out of bounds")
    coords = {"observation": np.arange(y.size), "group": group_names}
    with pm.Model(coords=coords) as model:
        index = pm.Data("group_idx", group_idx, dims="observation")
        population = pm.Normal("population", 0, 5)
        group_scale = pm.HalfNormal("group_scale", 2)
        group_raw = pm.Normal("group_raw", 0, 1, dims="group")
        group_effect = pm.Deterministic(
            "group_effect", population + group_scale * group_raw, dims="group"
        )
        sigma = pm.HalfNormal("sigma", 2)
        pm.Normal("outcome", group_effect[index], sigma, observed=y, dims="observation")
    return model
```

**Do not use when:** Groups are unrelated fixed categories or pooling has no generative justification.
**Verify:** Test index failures, prior predictive group spread, simulated recovery, and centered-versus-noncentered diagnostics.

## Recipe `pymc.robust-linear-likelihood`

**Use when:** Continuous residuals are plausibly heavy-tailed and a few outliers should not dominate a normal likelihood.
**Inspect first:** Standardize or otherwise justify predictor/outcome scales and decide whether outliers are data errors instead.
**Invariants:** Predictor/observation axes are named and degrees of freedom remain positive.

```python
import numpy as np
import pymc as pm


def build_robust_regression(x: np.ndarray, y: np.ndarray) -> pm.Model:
    if x.ndim != 2 or y.shape != (x.shape[0],):
        raise ValueError("x must be rows by features and y an aligned vector")
    coords = {"observation": np.arange(y.size), "feature": np.arange(x.shape[1])}
    with pm.Model(coords=coords) as model:
        x_data = pm.Data("x", x, dims=("observation", "feature"))
        intercept = pm.Normal("intercept", 0, 2)
        beta = pm.Normal("beta", 0, 1, dims="feature")
        sigma = pm.HalfNormal("sigma", 1)
        nu = pm.Exponential("nu_minus_one", 1 / 29) + 1
        mu = intercept + x_data @ beta
        pm.StudentT("outcome", nu=nu, mu=mu, sigma=sigma, observed=y, dims="observation")
    return model
```

**Do not use when:** The observation process implies censoring, contamination classes, or discrete errors; model that mechanism.
**Verify:** Compare prior predictive tails, simulated recovery, residual predictive checks, divergences, and sensitivity to the `nu` prior.

## Recipe `pymc.zero-inflated-counts`

**Use when:** Nonnegative counts have a separately justified excess-zero process and unequal exposure.
**Inspect first:** Distinguish zero inflation from overdispersion, hurdle behavior, missingness, and exposure errors.
**Invariants:** Counts are integers, exposure is positive, and `psi` means probability of the Poisson component.

```python
import numpy as np
import pymc as pm


def build_zero_inflated(x: np.ndarray, counts: np.ndarray, exposure: np.ndarray) -> pm.Model:
    if counts.ndim != 1 or x.shape != counts.shape or exposure.shape != counts.shape:
        raise ValueError("x, counts, and exposure must be aligned vectors")
    if np.any(counts < 0) or not np.issubdtype(counts.dtype, np.integer):
        raise ValueError("counts must be nonnegative integers")
    if np.any(exposure <= 0):
        raise ValueError("exposure must be positive")
    coords = {"observation": np.arange(counts.size)}
    with pm.Model(coords=coords) as model:
        intercept = pm.Normal("intercept", 0, 1.5)
        beta = pm.Normal("beta", 0, 1)
        psi = pm.Beta("psi", 2, 2)
        mu = pm.math.exp(intercept + beta * x + np.log(exposure))
        pm.ZeroInflatedPoisson("outcome", psi=psi, mu=mu, observed=counts, dims="observation")
    return model
```

**Do not use when:** Extra variance without a distinct zero process is the issue; compare a negative-binomial model first.
**Verify:** Check zero rate and positive-count tails in prior/posterior predictive draws and recover both components from simulations.

## Recipe `pymc.prior-predictive-domain-gate`

**Use when:** Priors must be rejected if they generate domain-impossible outcomes before fitting.
**Inspect first:** Name outcome-scale bounds and discrepancy statistics from subject-matter requirements.
**Invariants:** The gate samples observed nodes from the prior and fails before posterior sampling.

```python
import numpy as np
import pymc as pm


def checked_prior(model: pm.Model, seed: int, absolute_limit: float):
    if absolute_limit <= 0:
        raise ValueError("absolute_limit must be positive")
    with model:
        prior = pm.sample_prior_predictive(draws=500, random_seed=seed)
    values = np.asarray(prior["prior_predictive"]["outcome"].values)
    if not np.isfinite(values).all() or np.max(np.abs(values)) > absolute_limit:
        raise ValueError("prior predictive outcome violates domain bounds")
    return prior
```

**Do not use when:** One absolute bound is not a meaningful adequacy test; encode domain-specific rates, tails, or combinations.
**Verify:** Use a deliberately over-wide prior that fails and a justified prior that passes across repeated seeds.
