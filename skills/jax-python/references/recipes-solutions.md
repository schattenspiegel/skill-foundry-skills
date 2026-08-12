# Evaluated solution recipes

## Recipe `jax.pure-jitted-training-step`
**Use when:** compile a pure parameter update without mutating input.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import jax
import jax.numpy as jnp


def loss_fn(params, x, y):
    prediction = x @ params["w"] + params["b"]
    return jnp.mean((prediction - y) ** 2)


@jax.jit
def step(params, x, y, rate):
    loss, gradients = jax.value_and_grad(loss_fn)(params, x, y)
    updated = jax.tree.map(lambda value, grad: value - rate * grad, params, gradients)
    return updated, loss
```
**Do not use when:** The requested abstraction or lifecycle differs from
`pure-jitted-update`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `jax.verify-immutability-and-loss`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import jax.numpy as jnp
from solution import loss_fn, step


def test_pure_update_reduces_loss() -> None:
    params = {"w": jnp.array([0.0, 0.0]), "b": jnp.array(0.0)}
    original = {key: value.copy() for key, value in params.items()}
    x = jnp.array([[1.0, 0.0], [0.0, 1.0]])
    y = jnp.array([1.0, 2.0])
    updated, before = step(params, x, y, 0.2)
    assert float(loss_fn(updated, x, y)) < float(before)
    assert all(bool(jnp.array_equal(params[key], original[key])) for key in params)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`pure-jitted-update`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `jax.split-fold-vmap-randomness`
**Use when:** derive reproducible nonreused random streams.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import jax
import jax.numpy as jnp


def sample_batch(key, step: int, batch_size: int):
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    next_key, batch_key = jax.random.split(key)
    batch_key = jax.random.fold_in(batch_key, step)
    keys = jax.random.split(batch_key, batch_size)
    samples = jax.vmap(lambda item: jax.random.normal(item, (3,)))(keys)
    return next_key, samples
```
**Do not use when:** The requested abstraction or lifecycle differs from
`unique-batch-randomness`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `jax.verify-key-uniqueness-reproducibility`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import jax
import jax.numpy as jnp
import pytest
from solution import sample_batch


def test_reproducible_distinct_samples() -> None:
    key = jax.random.key(9)
    next_a, values_a = sample_batch(key, 4, 5)
    next_b, values_b = sample_batch(key, 4, 5)
    assert bool(jnp.array_equal(next_a, next_b))
    assert bool(jnp.array_equal(values_a, values_b))
    assert values_a.shape == (5, 3)
    assert not bool(jnp.array_equal(values_a[0], values_a[1]))
    with pytest.raises(ValueError):
        sample_batch(key, 0, 0)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`unique-batch-randomness`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `jax.grad-vmap-composition`
**Use when:** vectorize a scalar gradient over a batch.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import jax
import jax.numpy as jnp


def per_example_gradient(weights, x, y):
    if x.ndim != 2 or y.shape != (x.shape[0],) or weights.shape != (x.shape[1],):
        raise ValueError("shape mismatch")

    def loss(one_weights, one_x, one_y):
        return (jnp.dot(one_x, one_weights) - one_y) ** 2

    return jax.vmap(jax.grad(loss), in_axes=(None, 0, 0))(weights, x, y)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`batched-per-example-gradients`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `jax.verify-batch-gradient-shape`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import jax.numpy as jnp
import pytest
from solution import per_example_gradient


def test_gradients_match_formula() -> None:
    weights = jnp.array([1.0, 2.0])
    x = jnp.array([[1.0, 0.0], [0.0, 2.0]])
    y = jnp.array([0.0, 1.0])
    actual = per_example_gradient(weights, x, y)
    expected = 2 * (x @ weights - y)[:, None] * x
    assert actual.shape == (2, 2)
    assert bool(jnp.allclose(actual, expected))
    with pytest.raises(ValueError):
        per_example_gradient(weights, x, jnp.array([1.0]))
```
**Do not use when:** The requested abstraction or lifecycle differs from
`batched-per-example-gradients`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
