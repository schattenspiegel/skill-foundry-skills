# PyMC inference, prediction, and comparison recipes

Sampling success is not model success. Keep prior checks, posterior diagnostics,
predictive checks, and comparison as separate gates.

## Recipe `pymc.prior-posterior-predictive-flow`

**Use when:** A fitted model needs explicit prior, posterior, and in-sample replicated-data stages.
**Inspect first:** Set project draw/tune/chains policy, seeds, required InferenceData groups, and diagnostic thresholds.
**Invariants:** Prior predictive happens before fitting and posterior predictive extends the fitted artifact.

```python
import pymc as pm


def fit_with_predictions(model: pm.Model, seed: int):
    with model:
        prior = pm.sample_prior_predictive(random_seed=seed)
        idata = pm.sample(chains=4, random_seed=seed)
        pm.sample_posterior_predictive(
            idata,
            random_seed=seed,
            extend_inferencedata=True,
        )
    return prior, idata
```

**Do not use when:** Out-of-sample prediction is required; update data/coordinates and use a distinct predictions group.
**Verify:** Assert prior, posterior, sample-stat, observed-data, and posterior-predictive groups plus chain/draw/observation dimensions.

## Recipe `pymc.diagnostic-gate`

**Use when:** Sampling output must fail a quality gate instead of silently suppressing warnings.
**Inspect first:** Define parameter-specific thresholds and required sample-stat fields for the selected sampler/backend.
**Invariants:** Missing diagnostics remain unknown/failing and divergent draws are never discarded.

```python
import arviz as az


def diagnostic_report(idata) -> dict[str, object]:
    stats = idata["sample_stats"] if "sample_stats" in idata.children else None
    divergences = (
        int(stats["diverging"].sum())
        if stats is not None and "diverging" in stats
        else None
    )
    summary = az.summary(idata, kind="diagnostics", round_to="none")
    required = ("r_hat", "ess_bulk", "ess_tail", "mcse_mean")
    missing = [name for name in required if name not in summary]
    return {"divergences": divergences, "summary": summary, "missing": missing}
```

**Do not use when:** A generic threshold would replace substantive parameter-specific precision requirements.
**Verify:** Test missing stats, a deliberately bad fit, and a known-good simulation; any divergence remains an investigation gate.

## Recipe `pymc.out-of-sample-prediction`

**Use when:** A fitted mutable-data model predicts new rows with preserved feature semantics.
**Inspect first:** Reuse training transforms, feature order, category coding, and coordinate labels; inspect installed prediction arguments.
**Invariants:** Data and observation coordinates update together and predictions remain separate from in-sample posterior predictive draws.

```python
import numpy as np
import pymc as pm


def predict_new(
    model: pm.Model, idata, x_new: np.ndarray, labels: list[str], seed: int
):
    if x_new.ndim != 2 or x_new.shape[0] != len(labels):
        raise ValueError("new rows and observation labels must align")
    with model:
        pm.set_data({"x": x_new}, coords={"observation": labels})
        pm.sample_posterior_predictive(
            idata,
            var_names=["outcome"],
            predictions=True,
            extend_inferencedata=True,
            random_seed=seed,
        )
    return idata
```

**Do not use when:** The model was built with immutable inputs or new categories/features lack a defined training transformation.
**Verify:** Test changed row count, permuted features, unknown categories, prediction coordinates, and absence of overwritten training observations.

## Recipe `pymc.pointwise-log-likelihood`

**Use when:** A fitted model must expose observation-wise log likelihood for a later ArviZ comparison.
**Inspect first:** Confirm the observed variable, compatible observations, and installed `compute_log_likelihood` API.
**Invariants:** Log likelihood is pointwise, attached to the fitted artifact, and comparison adequacy remains an ArviZ responsibility.

```python
import pymc as pm


def add_log_likelihood(model: pm.Model, idata):
    with model:
        pm.compute_log_likelihood(
            idata,
            var_names=["outcome"],
            extend_inferencedata=True,
        )
    if "log_likelihood" not in idata.children:
        raise RuntimeError("pointwise log likelihood was not attached")
    return idata
```

**Do not use when:** Models target different observations or likelihoods; information-criterion comparison is then not directly valid.
**Verify:** Assert observation coordinates/length, finite pointwise values, and downstream Pareto-k diagnostics before interpreting ranks.
