# Evaluated solution recipes

## Recipe `httpx.borrowed-client-json`
**Use when:** use a caller-owned client and validate status before payload.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import httpx


def get_user(client: httpx.Client, user_id: int) -> dict[str, object]:
    response = client.get(f"/users/{user_id}")
    response.raise_for_status()
    payload = response.json()
    if (
        not isinstance(payload, dict)
        or type(payload.get("id")) is not int
        or not isinstance(payload.get("name"), str)
    ):
        raise ValueError("invalid user payload")
    if payload["id"] != user_id:
        raise ValueError("response user id mismatch")
    return payload
```
**Do not use when:** The requested abstraction or lifecycle differs from
`borrowed-client-json`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `httpx.verify-request-domain-contract`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import httpx, pytest
from solution import get_user


def test_request_and_validation() -> None:
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.url.path)
        return httpx.Response(200, json={"id": 7, "name": "Ada"})

    with httpx.Client(
        base_url="https://example.test", transport=httpx.MockTransport(handler)
    ) as client:
        assert get_user(client, 7)["name"] == "Ada"
        assert not client.is_closed
    assert seen == ["/users/7"]
```
**Do not use when:** The requested abstraction or lifecycle differs from
`borrowed-client-json`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `httpx.atomic-stream-download`
**Use when:** stream a response to a file with cleanup and atomic replacement.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from pathlib import Path
import httpx


def download(client: httpx.Client, url: str, destination: Path) -> None:
    partial = destination.with_suffix(destination.suffix + ".part")
    try:
        with client.stream("GET", url) as response:
            response.raise_for_status()
            with partial.open("wb") as handle:
                for chunk in response.iter_bytes():
                    if chunk:
                        handle.write(chunk)
        partial.replace(destination)
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
```
**Do not use when:** The requested abstraction or lifecycle differs from
`streaming-download`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `httpx.verify-stream-cleanup`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from pathlib import Path
import httpx, pytest
from solution import download


def test_atomic_download(tmp_path: Path) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, content=b"abc" * 1000))
    destination = tmp_path / "data.bin"
    with httpx.Client(transport=transport) as client:
        download(client, "https://example.test/data", destination)
    assert destination.read_bytes() == b"abc" * 1000
    assert not (tmp_path / "data.bin.part").exists()
```
**Do not use when:** The requested abstraction or lifecycle differs from
`streaming-download`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `httpx.client-policy`
**Use when:** construct an application client with phase budgets and bounded pooling.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import httpx


def make_client(base_url: str) -> httpx.Client:
    return httpx.Client(
        base_url=base_url,
        timeout=httpx.Timeout(connect=2, read=10, write=5, pool=1),
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10, keepalive_expiry=30),
        follow_redirects=False,
        headers={"User-Agent": "foundry-client/1"},
    )
```
**Do not use when:** The requested abstraction or lifecycle differs from
`explicit-client-policy`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `httpx.verify-timeout-limit-policy`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from solution import make_client


def test_policy() -> None:
    with make_client("https://example.test") as client:
        assert client.timeout.connect == 2
        assert client.timeout.read == 10
        assert client.timeout.write == 5
        assert client.timeout.pool == 1
        assert client.follow_redirects is False
        assert client.headers["User-Agent"] == "foundry-client/1"
```
**Do not use when:** The requested abstraction or lifecycle differs from
`explicit-client-policy`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
