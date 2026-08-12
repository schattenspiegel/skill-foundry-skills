# Evaluated solution recipes

## Recipe `pytest.patch-lookup-site`
**Use when:** patch the symbol used by the target module instead of its origin.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
def test_notify(monkeypatch) -> None:
    import app

    calls: list[str] = []
    monkeypatch.setattr(app, "send_message", calls.append)
    app.notify("Ada")
    assert calls == ["hello ada"]
```
**Do not use when:** The requested abstraction or lifecycle differs from
`patch-lookup-site`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pytest.verify-patch-restoration`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import importlib
import sys
from pathlib import Path
import pytest
import solution


def test_candidate_patches_lookup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "transport.py").write_text(
        "def send_message(value): raise RuntimeError('network')\n"
    )
    (tmp_path / "app.py").write_text(
        "from transport import send_message\n"
        "def notify(name): send_message('hello '+name.lower())\n"
    )
    monkeypatch.syspath_prepend(tmp_path)
    for name in ("app", "transport"):
        sys.modules.pop(name, None)
    with pytest.MonkeyPatch.context() as candidate_patch:
        solution.test_notify(candidate_patch)
    assert importlib.import_module("app").send_message.__module__ == "transport"
```
**Do not use when:** The requested abstraction or lifecycle differs from
`patch-lookup-site`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pytest.yield-fixture-owner`
**Use when:** release an owned resource even when a test fails.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pytest


@pytest.fixture
def opened_resource():
    import service

    resource = service.open_resource()
    try:
        yield resource
    finally:
        resource.close()


def test_resource_ready(opened_resource) -> None:
    assert opened_resource.ready is True
```
**Do not use when:** The requested abstraction or lifecycle differs from
`yield-fixture-cleanup`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pytest.verify-teardown-on-failure`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import sys
import types
import pytest
import solution


class Resource:
    ready = True
    closed = False

    def close(self) -> None:
        self.closed = True


def test_generator_fixture_closes(monkeypatch: pytest.MonkeyPatch) -> None:
    resource = Resource()
    monkeypatch.setitem(
        sys.modules, "service", types.SimpleNamespace(open_resource=lambda: resource)
    )
    generator = solution.opened_resource.__wrapped__()
    assert next(generator) is resource
    generator.close()
    assert resource.closed
```
**Do not use when:** The requested abstraction or lifecycle differs from
`yield-fixture-cleanup`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pytest.parametrize-invalid-boundaries`
**Use when:** cover invalid boundaries as distinct parametrized items.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pytest


@pytest.mark.parametrize(
    "value",
    [None, "", "0", "65536", "abc"],
    ids=["missing", "empty", "zero", "too-large", "nonnumeric"],
)
def test_parse_rejects_bad_port(value) -> None:
    from config import parse_port

    with pytest.raises(ValueError):
        parse_port(value)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`parameterized-error-contract`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pytest.verify-distinct-items`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import inspect
import solution


def test_parameter_matrix_is_explicit() -> None:
    marks = list(solution.test_parse_rejects_bad_port.pytestmark)
    parametrize = next(mark for mark in marks if mark.name == "parametrize")
    assert list(parametrize.args[1]) == [None, "", "0", "65536", "abc"]
    assert parametrize.kwargs["ids"] == ["missing", "empty", "zero", "too-large", "nonnumeric"]
    source = inspect.getsource(solution.test_parse_rejects_bad_port)
    assert "pytest.raises(ValueError)" in source
```
**Do not use when:** The requested abstraction or lifecycle differs from
`parameterized-error-contract`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
