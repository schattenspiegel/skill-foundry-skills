# Evaluated solution recipes

## Recipe `asyncio.bounded-ordered-map`
**Use when:** run bounded concurrent work while preserving input order.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import TypeVar, cast

T = TypeVar("T")
R = TypeVar("R")


async def bounded_map(
    items: Sequence[T], operation: Callable[[T], Awaitable[R]], limit: int
) -> list[R]:
    if limit < 1:
        raise ValueError("limit must be positive")
    semaphore = asyncio.Semaphore(limit)
    missing = object()
    results: list[R | object] = [missing] * len(items)

    async def run_one(index: int, item: T) -> None:
        async with semaphore:
            results[index] = await operation(item)

    async with asyncio.TaskGroup() as group:
        for index, item in enumerate(items):
            group.create_task(run_one(index, item))
    if any(item is missing for item in results):
        raise RuntimeError("task group exited without every result")
    return [cast(R, item) for item in results]
```
**Do not use when:** The requested abstraction or lifecycle differs from
`bounded-ordered-map`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `asyncio.verify-bounded-ordered-map`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import asyncio
import pytest
from solution import bounded_map


def test_order_and_limit() -> None:
    async def scenario() -> None:
        active = peak = 0
        lock = asyncio.Lock()

        async def operation(value: int) -> int:
            nonlocal active, peak
            async with lock:
                active += 1
                peak = max(peak, active)
            await asyncio.sleep(0)
            async with lock:
                active -= 1
            return value * 2

        assert await bounded_map([3, 1, 2], operation, 2) == [6, 2, 4]
        assert peak == 2

    asyncio.run(scenario())


def test_invalid_limit() -> None:
    async def operation(value: int) -> int:
        return value

    with pytest.raises(ValueError):
        asyncio.run(bounded_map([1], operation, 0))
```
**Do not use when:** The requested abstraction or lifecycle differs from
`bounded-ordered-map`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `asyncio.timeout-owned-resource`
**Use when:** bound an async operation and close its owned resource after timeout.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import asyncio
from collections.abc import Awaitable, Callable
from typing import Protocol, TypeVar

R = TypeVar("R")


class AsyncCloseable(Protocol):
    async def aclose(self) -> None: ...


async def call_with_resource(
    factory: Callable[[], Awaitable[AsyncCloseable]],
    operation: Callable[[AsyncCloseable], Awaitable[R]],
    timeout_seconds: float,
) -> R:
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    resource = await factory()
    try:
        async with asyncio.timeout(timeout_seconds):
            return await operation(resource)
    finally:
        await resource.aclose()
```
**Do not use when:** The requested abstraction or lifecycle differs from
`timeout-cleanup`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `asyncio.verify-timeout-cleanup`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import asyncio
import pytest
from solution import call_with_resource


class Resource:
    closed = False

    async def aclose(self) -> None:
        self.closed = True


def test_timeout_still_closes() -> None:
    resource = Resource()

    async def factory() -> Resource:
        return resource

    async def operation(_: Resource) -> None:
        await asyncio.Event().wait()

    with pytest.raises(TimeoutError):
        asyncio.run(call_with_resource(factory, operation, 0.01))
    assert resource.closed
```
**Do not use when:** The requested abstraction or lifecycle differs from
`timeout-cleanup`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `asyncio.to-thread-boundary`
**Use when:** isolate a blocking callable without freezing the event loop.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import asyncio
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


async def run_blocking(call: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
    return await asyncio.to_thread(call, *args, **kwargs)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`blocking-call-boundary`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `asyncio.verify-loop-progress`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import asyncio
import threading
from solution import run_blocking


def test_event_loop_progresses() -> None:
    async def scenario() -> None:
        release = threading.Event()
        started = threading.Event()

        def blocking() -> int:
            started.set()
            release.wait(1)
            return 7

        task = asyncio.create_task(run_blocking(blocking))
        while not started.is_set():
            await asyncio.sleep(0)
        marker = False

        async def tick() -> None:
            nonlocal marker
            marker = True
            release.set()

        await tick()
        assert marker and await task == 7

    asyncio.run(scenario())
```
**Do not use when:** The requested abstraction or lifecycle differs from
`blocking-call-boundary`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
