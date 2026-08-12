# Evaluated solution recipes

## Recipe `integration.fixture-factory-per-example`
**Use when:** create fresh mutable state for every generated example.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pytest
from hypothesis import HealthCheck, given, settings, strategies as st


@pytest.fixture
def stack_factory():
    return list


# The fixture is a stateless constructor; each example calls it for fresh state.
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(st.lists(st.integers(), max_size=20))
def test_stack_round_trip(stack_factory, values) -> None:
    stack = stack_factory()
    stack.extend(values)
    assert [stack.pop() for _ in values] == list(reversed(values))
    assert stack == []
```
**Do not use when:** The requested abstraction or lifecycle differs from
`fixture-factory-per-example`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `integration.verify-example-isolation`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import subprocess
import sys


def test_integrated_property_runs_cleanly() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout
```
**Do not use when:** The requested abstraction or lifecycle differs from
`fixture-factory-per-example`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `integration.parametrize-given-composition`
**Use when:** combine finite algorithm modes with generated input domains.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pytest
from hypothesis import given, strategies as st


def normalize(values, mode):
    if mode not in {"asc", "desc"}:
        raise ValueError("unknown mode")
    return sorted(values, reverse=mode == "desc")


@pytest.mark.parametrize("mode", ["asc", "desc"], ids=["ascending", "descending"])
@given(st.lists(st.integers(), max_size=30))
def test_normalize(mode, values) -> None:
    result = normalize(values, mode)
    assert sorted(result) == sorted(values)
    assert result == sorted(result, reverse=mode == "desc")
    assert normalize(result, mode) == result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`parametrize-generated-composition`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `integration.verify-collected-cross-product`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import subprocess
import sys


def test_two_items_each_run_properties() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "2 passed" in result.stdout
```
**Do not use when:** The requested abstraction or lifecycle differs from
`parametrize-generated-composition`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `integration.named-profile-regression-example`
**Use when:** combine deterministic regression replay with an explicit CI budget.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import os
from hypothesis import example, given, settings, strategies as st

settings.register_profile("ci", max_examples=75, deadline=None, suppress_health_check=())
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "ci"))


def encode(value: str) -> bytes:
    return value.encode("utf-8")


def decode(value: bytes) -> str:
    return value.decode("utf-8")


@example("\x00")
@given(st.text(max_size=100))
def test_text_round_trip(value: str) -> None:
    assert decode(encode(value)) == value
```
**Do not use when:** The requested abstraction or lifecycle differs from
`named-ci-profile-and-regression`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `integration.verify-profile-and-example`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import subprocess
import sys


def test_ci_profile_and_regression() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout
```
**Do not use when:** The requested abstraction or lifecycle differs from
`named-ci-profile-and-regression`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
