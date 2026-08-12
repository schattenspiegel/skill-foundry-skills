# Evaluated solution recipes

## Recipe `typing.structural-reader`
**Use when:** accept a minimal structural dependency without inheritance.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Reader(Protocol[T_co]):
    def read(self, key: str) -> T_co: ...


def load_name(reader: Reader[str], key: str) -> str:
    name = reader.read(key).strip()
    if not name:
        raise ValueError("name is empty")
    return name
```
**Do not use when:** The requested abstraction or lifecycle differs from
`structural-reader-protocol`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `typing.verify-protocol-implementation`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from pathlib import Path
import subprocess, sys
from solution import load_name


class MemoryReader:
    def read(self, key: str) -> str:
        return " Ada "


def test_structural_runtime_and_mypy() -> None:
    assert load_name(MemoryReader(), "name") == "Ada"
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
```
**Do not use when:** The requested abstraction or lifecycle differs from
`structural-reader-protocol`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `typing.paramspec-decorator`
**Use when:** preserve a wrapped callable signature and return type.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def traced(call: Callable[P, R]) -> Callable[P, R]:
    @wraps(call)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return call(*args, **kwargs)

    return wrapper


@traced
def add(left: int, right: int) -> int:
    return left + right
```
**Do not use when:** The requested abstraction or lifecycle differs from
`paramspec-decorator`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `typing.verify-decorator-signature`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import inspect
from pathlib import Path
import subprocess, sys
from solution import add


def test_signature_and_checker() -> None:
    assert add(2, 3) == 5
    assert list(inspect.signature(add).parameters) == ["left", "right"]
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
```
**Do not use when:** The requested abstraction or lifecycle differs from
`paramspec-decorator`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `typing.typeis-payload`
**Use when:** narrow an unknown mapping to a precise TypedDict.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from typing import TypedDict
from typing_extensions import TypeIs


class UserPayload(TypedDict):
    id: int
    name: str


def is_user_payload(value: object) -> TypeIs[UserPayload]:
    return (
        isinstance(value, dict)
        and type(value.get("id")) is int
        and isinstance(value.get("name"), str)
        and set(value) == {"id", "name"}
    )
```
**Do not use when:** The requested abstraction or lifecycle differs from
`typeis-mapping-narrower`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `typing.verify-bidirectional-narrowing`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import subprocess, sys
from solution import is_user_payload


def test_runtime_and_checker() -> None:
    assert is_user_payload({"id": 1, "name": "Ada"})
    assert not is_user_payload({"id": True, "name": "Ada"})
    assert not is_user_payload({"id": 1, "name": "Ada", "admin": True})
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "solution.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
```
**Do not use when:** The requested abstraction or lifecycle differs from
`typeis-mapping-narrower`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
