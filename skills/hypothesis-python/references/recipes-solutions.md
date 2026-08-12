# Evaluated solution recipes

## Recipe `hypothesis.recursive-json-strategy`
**Use when:** test a serialization round trip over recursive JSON values.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import json
import math
from hypothesis import given, strategies as st

scalar = (
    st.none()
    | st.booleans()
    | st.integers(-(2**53), 2**53)
    | st.floats(allow_nan=False, allow_infinity=False)
    | st.text()
)
json_values = st.recursive(
    scalar,
    lambda children: (
        st.lists(children, max_size=8) | st.dictionaries(st.text(), children, max_size=8)
    ),
    max_leaves=20,
)


@given(json_values)
def test_json_round_trip(value) -> None:
    assert json.loads(json.dumps(value, allow_nan=False)) == value
```
**Do not use when:** The requested abstraction or lifecycle differs from
`json-round-trip-property`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `hypothesis.verify-json-round-trip`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import subprocess, sys


def test_property_executes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed" in result.stdout
```
**Do not use when:** The requested abstraction or lifecycle differs from
`json-round-trip-property`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `hypothesis.constructive-intervals`
**Use when:** construct ordered intervals without rejection filtering.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from hypothesis import given, strategies as st


@st.composite
def intervals(draw):
    start = draw(st.integers(-1000, 1000))
    end = draw(st.integers(start, 1000))
    return start, end


@given(intervals(), st.integers(-1000, 1000))
def test_translation_preserves_width(interval, offset) -> None:
    start, end = interval
    assert end - start >= 0
    assert (end + offset) - (start + offset) == end - start
```
**Do not use when:** The requested abstraction or lifecycle differs from
`constructive-interval-strategy`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `hypothesis.verify-shrinkable-relations`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import inspect, subprocess, sys
import solution


def test_constructive_property() -> None:
    source = inspect.getsource(solution)
    assert ".filter(" not in source and "assume(" not in source
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
```
**Do not use when:** The requested abstraction or lifecycle differs from
`constructive-interval-strategy`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `hypothesis.stateful-model`
**Use when:** compare operation sequences against a simple model.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, precondition, rule


class StackMachine(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.actual: list[int] = []
        self.model: list[int] = []

    @rule(value=st.integers())
    def push(self, value: int) -> None:
        self.actual.append(value)
        self.model.append(value)

    @precondition(lambda self: bool(self.model))
    @rule()
    def pop(self) -> None:
        assert self.actual.pop() == self.model.pop()

    @invariant()
    def same_state(self) -> None:
        assert self.actual == self.model


TestStackMachine = StackMachine.TestCase
```
**Do not use when:** The requested abstraction or lifecycle differs from
`stateful-stack-model`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `hypothesis.verify-operation-sequences`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import subprocess, sys
import solution


def test_state_machine_executes() -> None:
    assert issubclass(solution.TestStackMachine, object)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
```
**Do not use when:** The requested abstraction or lifecycle differs from
`stateful-stack-model`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
