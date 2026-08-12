# Evaluated solution recipes

## Recipe `fastapi.yield-dependency-owner`
**Use when:** own and close a request-scoped resource after response completion.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from collections.abc import Iterator
from fastapi import Depends, FastAPI

app = FastAPI()
created = []


class Resource:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


def get_resource() -> Iterator[Resource]:
    resource = Resource()
    created.append(resource)
    try:
        yield resource
    finally:
        resource.close()


@app.get("/status")
def status(resource: Resource = Depends(get_resource)) -> dict[str, bool]:
    return {"closed_during_handler": resource.closed}
```
**Do not use when:** The requested abstraction or lifecycle differs from
`yield-dependency-cleanup`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `fastapi.verify-response-then-cleanup`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from fastapi.testclient import TestClient
from solution import app, created


def test_dependency_closes_after_response() -> None:
    with TestClient(app) as client:
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json() == {"closed_during_handler": False}
    assert created[-1].closed is True
```
**Do not use when:** The requested abstraction or lifecycle differs from
`yield-dependency-cleanup`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `fastapi.response-model-boundary`
**Use when:** prevent internal fields from escaping the API.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserOut(BaseModel):
    id: int
    name: str


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id != 7:
        raise HTTPException(status_code=404, detail="user not found")
    return {"id": 7, "name": "Ada", "password_hash": "secret", "admin": True}
```
**Do not use when:** The requested abstraction or lifecycle differs from
`response-model-filtering`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `fastapi.verify-secret-field-exclusion`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from fastapi.testclient import TestClient
from solution import app


def test_public_schema_filters_internal_fields() -> None:
    with TestClient(app) as client:
        response = client.get("/users/7")
        assert response.json() == {"id": 7, "name": "Ada"}
        assert client.get("/users/8").status_code == 404
        schema = client.get("/openapi.json").json()
    assert "UserOut" in schema["components"]["schemas"]
```
**Do not use when:** The requested abstraction or lifecycle differs from
`response-model-filtering`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `fastapi.lifespan-resource-owner`
**Use when:** initialize and tear down application-scoped state.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

created = []


class Catalog:
    def __init__(self) -> None:
        self.items = ["a", "b"]
        self.closed = False

    async def aclose(self) -> None:
        self.closed = True


@asynccontextmanager
async def lifespan(app: FastAPI):
    catalog = Catalog()
    created.append(catalog)
    app.state.catalog = catalog
    try:
        yield
    finally:
        await catalog.aclose()


app = FastAPI(lifespan=lifespan)


@app.get("/items")
async def items(request: Request) -> list[str]:
    return request.app.state.catalog.items
```
**Do not use when:** The requested abstraction or lifecycle differs from
`lifespan-owned-state`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `fastapi.verify-testclient-lifespan`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pytest
from fastapi.testclient import TestClient
from solution import app, created


def test_lifespan_is_entered_and_closed() -> None:
    with pytest.raises(AttributeError):
        _ = app.state.catalog
    with TestClient(app) as client:
        assert client.get("/items").json() == ["a", "b"]
        assert created[-1].closed is False
    assert created[-1].closed is True
```
**Do not use when:** The requested abstraction or lifecycle differs from
`lifespan-owned-state`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
