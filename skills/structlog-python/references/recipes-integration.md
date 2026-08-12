# Structlog integration, context, exception, and testing recipes

Load this module when structlog interacts with stdlib logging, execution-local
context, exceptions, or tests.

## Recipe `structlog.processor-formatter-integration`

**Use when:** Structlog and foreign stdlib records must share one final JSON renderer.
**Inspect first:** Inventory existing handlers, propagation, foreign-record fields, and startup call count.
**Invariants:** Structlog stops at `wrap_for_formatter`; ProcessorFormatter owns the only renderer.

```python
import logging

import structlog


def configure_unified_logging() -> None:
    shared = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]
    structlog.configure(
        processors=[*shared, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(logging.INFO)
```

**Do not use when:** Only structlog events need JSON or an existing handler contract must remain untouched.
**Verify:** Emit one structlog and one foreign stdlib event; parse both, then assert no duplicates and no `_record` metadata.

## Recipe `structlog.request-context-lifecycle`

**Use when:** Request identifiers must follow all loggers within one execution context.
**Inspect first:** Locate the true unit-of-work boundary and any sync/async or thread transitions.
**Invariants:** Context is cleared before binding and cleared in `finally`, including failures.

```python
from collections.abc import Callable
from typing import TypeVar

from structlog.contextvars import bind_contextvars, clear_contextvars


T = TypeVar("T")


def within_request(request_id: str, action: Callable[[], T]) -> T:
    clear_contextvars()
    bind_contextvars(request_id=request_id)
    try:
        return action()
    finally:
        clear_contextvars()
```

**Do not use when:** The value is component-scoped and should live on a returned bound logger.
**Verify:** Run two sequential requests plus a failing request and assert no identifier crosses boundaries.

## Recipe `structlog.structured-exception`

**Use when:** A caught exception must become a machine-readable event without losing traceback evidence.
**Inspect first:** Confirm exception processor, renderer, and which identifiers are safe to log.
**Invariants:** `.exception` supplies `exc_info`, structured fields remain separate, and formatting precedes rendering.

```python
import structlog


def load_order(order_id: str, repository):
    log = structlog.get_logger("orders")
    try:
        return repository.load(order_id)
    except Exception:
        log.exception("order_load_failed", order_id=order_id)
        raise
```

**Do not use when:** The exception is handled successfully and traceback output would be noise; emit an explicit outcome event instead.
**Verify:** Capture a failing call and assert event name, safe identifiers, exception representation, re-raise behavior, and no raw secret.

## Recipe `structlog.capture-testing-contract`

**Use when:** A unit test should assert event dictionaries without depending on terminal formatting.
**Inspect first:** Confirm logger caching and acquire the logger inside the capture context.
**Invariants:** The test asserts semantic keys and does not reset unrelated global production state.

```python
import structlog
from structlog.testing import capture_logs


def capture_action(action) -> list[dict[str, object]]:
    with capture_logs() as entries:
        logger = structlog.get_logger("test-subject")
        action(logger)
    return entries


def test_completed_event() -> None:
    entries = capture_action(
        lambda log: log.info("job_completed", job_id="job-1", rows=3)
    )
    assert entries == [
        {"event": "job_completed", "job_id": "job-1", "rows": 3, "log_level": "info"}
    ]
```

**Do not use when:** Formatter bytes, ANSI output, handler propagation, or real integration behavior is the subject of the test.
**Verify:** Run the test with the project configuration and add a separate renderer/handler test for output integration.
