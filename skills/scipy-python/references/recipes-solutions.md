# Evaluated solution recipes

## Recipe `scipy.minimize-with-residual-guard`
**Use when:** solve and independently verify a bounded smooth optimum.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
from scipy.optimize import minimize


def solve_quadratic(target):
    target = np.asarray(target, dtype=float)
    if not np.isfinite(target).all() or ((target < 0) | (target > 10)).any():
        raise ValueError("target must be finite and inside bounds")
    objective = lambda x: float(np.sum((x - target) ** 2))
    gradient = lambda x: 2 * (x - target)
    result = minimize(
        objective, np.full_like(target, 5.0), jac=gradient, bounds=[(0, 10)] * target.size
    )
    if (
        not result.success
        or not np.isfinite(result.fun)
        or np.max(np.abs(gradient(result.x)), initial=0.0) > 1e-7
    ):
        raise RuntimeError(f"optimization failed: {result.message}")
    return result.x.copy()
```
**Do not use when:** The requested abstraction or lifecycle differs from
`bounded-quadratic-minimize`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `scipy.verify-optimality-status`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
import pytest
from solution import solve_quadratic


def test_solution_and_domain() -> None:
    target = np.array([1.5, 7.25])
    assert np.allclose(solve_quadratic(target), target, atol=1e-7)
    with pytest.raises(ValueError):
        solve_quadratic([11.0])
```
**Do not use when:** The requested abstraction or lifecycle differs from
`bounded-quadratic-minimize`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `scipy.bracketed-root-solve`
**Use when:** solve a scalar root with a proof-bearing bracket.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import math
from scipy.optimize import root_scalar


def positive_root(value: float, xtol: float = 1e-12) -> float:
    if not math.isfinite(value) or value < 0 or xtol <= 0:
        raise ValueError("invalid value or tolerance")
    if value == 0:
        return 0.0
    result = root_scalar(
        lambda x: x * x - value, bracket=(0.0, max(1.0, value)), method="brentq", xtol=xtol
    )
    root = float(result.root)
    if not result.converged or abs(root * root - value) > max(xtol, 1e-12) * max(1.0, value):
        raise RuntimeError("root solve did not satisfy residual contract")
    return root
```
**Do not use when:** The requested abstraction or lifecycle differs from
`bracketed-root`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `scipy.verify-root-residual`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import math
import pytest
from solution import positive_root


def test_root_and_rejection() -> None:
    assert math.isclose(positive_root(2), math.sqrt(2), rel_tol=1e-11)
    assert positive_root(0) == 0
    with pytest.raises(ValueError):
        positive_root(-1)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`bracketed-root`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `scipy.sparse-solve-with-residual`
**Use when:** solve a sparse system without accidental densification.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def solve_sparse(matrix, rhs, tolerance: float = 1e-10):
    operator = sparse.csc_array(matrix)
    vector = np.asarray(rhs, dtype=float)
    if (
        operator.ndim != 2
        or operator.shape[0] != operator.shape[1]
        or vector.shape != (operator.shape[0],)
    ):
        raise ValueError("shape mismatch")
    if not np.isfinite(vector).all() or tolerance <= 0:
        raise ValueError("invalid rhs or tolerance")
    result = np.asarray(spsolve(operator, vector))
    scale = max(float(np.linalg.norm(vector)), 1.0)
    if (
        not np.isfinite(result).all()
        or np.linalg.norm(operator @ result - vector) / scale > tolerance
    ):
        raise RuntimeError("linear solve residual too large")
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`sparse-linear-system`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `scipy.verify-sparse-residual`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
import pytest
from scipy import sparse
from solution import solve_sparse


def test_sparse_solution() -> None:
    matrix = sparse.diags([2.0, 3.0, 4.0], format="csr")
    rhs = np.array([2.0, 6.0, 8.0])
    assert np.allclose(solve_sparse(matrix, rhs), [1, 2, 2])
    with pytest.raises(ValueError):
        solve_sparse(matrix, [1, 2])
```
**Do not use when:** The requested abstraction or lifecycle differs from
`sparse-linear-system`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
