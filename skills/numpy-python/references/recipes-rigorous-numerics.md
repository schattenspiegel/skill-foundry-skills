# Rigorous numerical practice and recipes

Use this checklist when NumPy supports scientific, statistical, optimization,
simulation, or high-consequence numerical work. It is a rigorous-computation
standard, not a description of any mathematician's private workflow.

## Formulate before computing

1. **Define the quantity first.** State the mathematical object, population or
   domain, units, semantic axes, and desired conclusion before selecting APIs.
2. **Write invariants before implementation.** Examples include conservation,
   symmetry, positivity, monotonicity, normalization, bounds, and dimensional
   consistency.
3. **Separate error sources.** Distinguish model/input, discretization,
   sampling, conditioning, and floating-point errors; each needs a different
   remedy.
4. **Choose scale deliberately.** Nondimensionalize or rescale variables whose
   magnitudes would otherwise damage conditioning or make tolerances opaque.
5. **Make the array contract explicit.** Name every axis, dtype, units,
   ownership, mutation policy, and nonfinite policy.
6. **Estimate cost before allocation.** Derive output and temporary shapes,
   element counts, bytes, and asymptotic cost before broadcasting or factoring.

## Choose a stable computation

7. **Prefer stable algebra.** Use `log1p`, `expm1`, `hypot`, log-domain sums,
   centered formulas, or factored expressions when naïve algebra loses digits
   or overflows.
8. **Use the algorithm that matches the problem.** Solve systems rather than
   forming inverses; use least squares for overdetermined models; preserve
   structure such as symmetry when the chosen routine supports it.
9. **Inspect conditioning.** A correct backward-stable algorithm cannot recover
   information the problem itself makes insensitive to the inputs.
10. **Control dtype at every reduction.** Specify accumulation and result
    dtypes where overflow, cancellation, or precision loss is material.
11. **Localize floating-point policy.** Use `np.errstate` around the operation,
    then inspect results. Do not globally silence divide, overflow, or invalid
    warnings.
12. **Treat nonfinite values semantically.** Decide separately whether `NaN`,
    `+inf`, `-inf`, masked, or absent values are valid, propagated, rejected, or
    summarized.
13. **Control expression temporaries.** Stage operations or use `out=` only
    after proving casting and aliasing safety; vectorized code can still exhaust
    memory.
14. **Preserve ownership boundaries.** Do not let a performance optimization
    silently change whether a caller's array is mutated or retained.

## Verify rather than admire output

15. **Check invariants after execution.** Verify shape, dtype, finiteness,
    conservation, normalization, symmetry, bounds, and ownership as applicable.
16. **Use residuals with scale.** Report a dimensionless or unit-aware residual;
    an absolute residual without a reference scale is rarely informative.
17. **Separate backward from forward error.** A small residual can coexist with
    a poor solution when conditioning is bad.
18. **Perform refinement studies.** Vary grid, step, rank, sample count, or
    iteration tolerance and check whether the result converges at a plausible
    rate.
19. **Detect the roundoff floor.** If refinement stops improving or reverses,
    do not extrapolate as if truncation error still dominated.
20. **Triangulate independently.** Compare with a special case, alternate
    formulation, higher-precision reference, direct small problem, or known
    conservation law.
21. **Probe adversarial regimes.** Test empty and singleton axes, near-singular
    systems, cancellation, overflow/underflow, extreme scales, repeated values,
    noncontiguous views, and invalid inputs.
22. **Choose tolerances from the problem.** Derive `rtol` and `atol` from units,
    reference scale, conditioning, method error, and consequence. NumPy's
    defaults are not a universal accuracy contract.
23. **Assert shape and dtype separately.** Numerical closeness can broadcast or
    ignore a dtype mismatch. Use strict testing when those are contractual.
24. **Check the original problem.** Validate the untransformed equation or
    invariant, not only an equivalent implementation intermediate.

## Reproduce and communicate

25. **Own random streams explicitly.** Inject `Generator`; spawn independent
    streams for parallel work rather than sharing global state.
26. **Quantify sampling uncertainty.** Record sample count, standard error or
    interval, dependence assumptions, and convergence diagnostics.
27. **Benchmark representative workloads.** Warm up when relevant, repeat
    measurements, include allocation cost, and test realistic shapes/layouts.
28. **Record the numerical environment.** Capture NumPy version, dtype,
    platform-sensitive backend/thread settings when material, and seed/stream
    construction.
29. **Label the evidence honestly.** Use validated against stated tolerances,
    numerically supported, sampled only, exploratory, or unresolved.
30. **Stop at the evidence boundary.** If conditioning, convergence, or
    uncertainty is unacceptable, return diagnostics or fail explicitly instead
    of presenting a plausible array as a trustworthy result.

## Recipe `numpy.solve-with-diagnostics`

**Use when:** `A` is a finite square matrix, `b` is one finite right-hand-side
vector, and the caller supplies acceptance thresholds.

**Inspect first:** matrix/rhs shapes, dtype and finiteness, expected
conditioning, units/scales, and justified condition/backward-error limits.

**Invariants:** Solve the original system without mutation or explicit inverse;
return condition and normwise scaled backward-error diagnostics.

```python
import numpy as np
import numpy.typing as npt


def solve_with_diagnostics(
    a: npt.ArrayLike,
    b: npt.ArrayLike,
    *,
    max_condition: float,
    max_backward_error: float,
) -> tuple[np.ndarray, float, float]:
    matrix = np.asarray(a, dtype=np.float64)
    rhs = np.asarray(b, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or not matrix.shape[0]:
        raise ValueError("a must be a nonempty square matrix")
    if rhs.ndim != 1 or rhs.shape[0] != matrix.shape[0]:
        raise ValueError("b must be one compatible vector")
    if not np.all(np.isfinite(matrix)) or not np.all(np.isfinite(rhs)):
        raise ValueError("a and b must be finite")
    if not np.isfinite(max_condition) or max_condition <= 0:
        raise ValueError("max_condition must be finite and positive")
    if not np.isfinite(max_backward_error) or max_backward_error < 0:
        raise ValueError("max_backward_error must be finite and nonnegative")

    condition = float(np.linalg.cond(matrix))
    if not np.isfinite(condition) or condition > max_condition:
        raise np.linalg.LinAlgError("condition threshold exceeded")
    solution = np.linalg.solve(matrix, rhs)
    residual_norm = float(np.linalg.norm(matrix @ solution - rhs, ord=np.inf))
    denominator = np.longdouble(np.linalg.norm(matrix, ord=np.inf)) * np.longdouble(
        np.linalg.norm(solution, ord=np.inf)
    ) + np.longdouble(np.linalg.norm(rhs, ord=np.inf))
    backward_error = float(residual_norm / denominator) if denominator else residual_norm
    if not np.isfinite(backward_error) or backward_error > max_backward_error:
        raise ArithmeticError("backward-error threshold exceeded")
    return solution, condition, backward_error
```

**Do not use when:** The problem is least squares, rank deficient, sparse, or
requires a structured solver.

**Verify:** Exercise ordinary, rescaled, near-singular, invalid, and deliberately
bad-residual systems against caller-owned thresholds.

## Recipe `numpy.stable-softmax`

**Use when:** logits are real float data and each slice contains at least one
finite value.

**Inspect first:** semantic normalization axis, nonfinite policy, expected
output shape/dtype, and justified normalization tolerances.

**Invariants:** Preserve shape, avoid overflow, permit `-inf` only beside a
finite logit, and return probabilities whose selected-axis sums satisfy the
explicit tolerance.

```python
def stable_softmax(
    logits: npt.ArrayLike,
    *,
    axis: int = -1,
    rtol: float = 1e-12,
    atol: float = 1e-15,
) -> np.ndarray:
    values = np.asarray(logits, dtype=np.float64)
    if values.ndim == 0 or not -values.ndim <= axis < values.ndim:
        raise ValueError("axis must select an existing non-scalar dimension")
    if not np.isfinite(rtol) or not np.isfinite(atol) or rtol < 0 or atol < 0:
        raise ValueError("rtol and atol must be finite and nonnegative")
    axis %= values.ndim
    if values.shape[axis] == 0:
        raise ValueError("softmax axis must be nonempty")
    if np.any(np.isnan(values)) or np.any(np.isposinf(values)):
        raise ValueError("NaN and positive infinity are not valid logits")
    maximum = np.max(values, axis=axis, keepdims=True)
    if not np.all(np.isfinite(maximum)):
        raise ValueError("each softmax slice needs a finite value")
    with np.errstate(under="ignore"):
        weights = np.exp(values - maximum)
    probabilities = weights / weights.sum(axis=axis, keepdims=True)
    if not np.allclose(probabilities.sum(axis=axis), 1.0, rtol=rtol, atol=atol):
        raise ArithmeticError("softmax normalization check failed")
    return probabilities
```

**Do not use when:** infinities have a different domain meaning or the consumer
requires complex, masked, or specialized log-domain outputs.

**Verify:** Check shift invariance, extreme magnitudes, axis shape, finite
outputs, `-inf` behavior, invalid slices, and sums of one under explicit
tolerances.

## Recipe `numpy.monte-carlo-mean`

**Use when:** estimating a scalar finite-valued mean whose sampler accepts an
injected `Generator` and a requested batch size.

**Inspect first:** estimator definition, dependence assumptions, stream
ownership, sample count, memory budget, and required uncertainty measure.

**Invariants:** Request no more than `batch_size` draws at once, consume exactly
`sample_count`, keep only online moments, and return sample standard error and
count with the mean.

```python
from collections.abc import Callable


def monte_carlo_mean(
    sampler: Callable[[np.random.Generator, int], npt.ArrayLike],
    rng: np.random.Generator,
    *,
    sample_count: int,
    batch_size: int = 65_536,
) -> tuple[float, float, int]:
    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng must be an injected numpy Generator")
    if sample_count < 2 or batch_size < 1:
        raise ValueError("need at least two samples and a positive batch size")
    count = 0
    mean = 0.0
    sum_squared_deviations = 0.0
    while count < sample_count:
        size = min(batch_size, sample_count - count)
        values = np.asarray(sampler(rng, size), dtype=np.float64)
        if values.shape != (size,) or not np.all(np.isfinite(values)):
            raise ValueError("sampler must return one finite scalar per draw")
        batch_mean = float(values.mean(dtype=np.float64))
        batch_m2 = float(np.sum((values - batch_mean) ** 2, dtype=np.float64))
        total = count + size
        delta = batch_mean - mean
        sum_squared_deviations += batch_m2 + delta**2 * count * size / total
        mean += delta * size / total
        count = total
    variance = sum_squared_deviations / (count - 1)
    standard_error = float(np.sqrt(variance / count))
    return mean, standard_error, count
```

**Do not use when:** draws are dependent without an adjusted uncertainty method,
the estimand is vector-valued, or bias/model error dominates sampling error.

**Verify:** Check batch-size bounds, equivalent-stream reproducibility, constant
and variable samplers, invalid outputs, and agreement with a direct small
reference. Do not interpret the standard error as model or bias error.
