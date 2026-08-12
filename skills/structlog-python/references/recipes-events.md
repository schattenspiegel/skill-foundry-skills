# Structlog event and processor recipes

Choose one renderer and one output owner. These recipes keep event construction,
context, filtering, and rendering in an observable order.

## Recipe `structlog.bound-event-context`

**Use when:** A component emits repeated events sharing stable low-cardinality context.
**Inspect first:** Classify fields by application, component, request, and one-event lifetime.
**Invariants:** Binding returns a new contextual logger and the event name remains stable.

```python
import structlog


def payment_logger(component: str):
    return structlog.get_logger("payments").bind(component=component)


def record_authorization(log, payment_id: str, amount_cents: int) -> None:
    log.info(
        "payment_authorized",
        payment_id=payment_id,
        amount_cents=amount_cents,
    )
```

**Do not use when:** Context follows an execution unit across independently created loggers; use contextvars lifecycle instead.
**Verify:** Capture the event dictionary and assert stable event name, bound component, per-call fields, and no secret values.

## Recipe `structlog.standalone-json-pipeline`

**Use when:** An application owns structured JSON output and foreign stdlib logs need not share its schema.
**Inspect first:** Confirm stream, minimum level, byte-versus-text renderer contract, and one-time startup ownership.
**Invariants:** Filtering precedes enrichment, redaction precedes rendering, and JSON is rendered exactly once.

```python
import logging

import structlog


def configure_logging() -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )
```

**Do not use when:** Foreign `logging` records must use the same final JSON schema; use ProcessorFormatter.
**Verify:** Parse one emitted line as JSON and assert level filtering, timestamp policy, event fields, and exactly one line.

## Recipe `structlog.redact-before-render`

**Use when:** Known sensitive keys may enter event dictionaries before output.
**Inspect first:** Define closed sensitive-key and nested-data policies; omission is safer than partial masking for tokens.
**Invariants:** Redaction runs before every renderer or stdlib handoff and always returns the event dictionary.

```python
from collections.abc import MutableMapping
from typing import Any


SENSITIVE_KEYS = frozenset({"authorization", "password", "token"})


def redact_secrets(
    _logger: object,
    _method_name: str,
    event_dict: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    for key in SENSITIVE_KEYS:
        if key in event_dict:
            event_dict[key] = "[redacted]"
    return event_dict
```

**Do not use when:** Secrets can be prevented at the binding/call boundary; exclusion is the preferred first control.
**Verify:** Place the processor immediately before a test renderer and assert raw values never occur in text, bytes, or exception paths.

## Recipe `structlog.custom-processor-contract`

**Use when:** A deterministic derived event field belongs in every retained event.
**Inspect first:** Confirm required input keys, failure policy, output type, and processor placement.
**Invariants:** The processor returns the mapping on every retained path and does no I/O.

```python
from collections.abc import MutableMapping
from typing import Any


def add_order_bucket(
    _logger: object,
    _method_name: str,
    event_dict: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    amount = event_dict.get("amount_cents")
    if isinstance(amount, int):
        event_dict["order_bucket"] = "large" if amount >= 10_000 else "normal"
    return event_dict
```

**Do not use when:** The field belongs to one event or needs external state; compute it at the call site or an owned enrichment boundary.
**Verify:** Unit-test missing, wrong-type, threshold, and ordinary inputs by calling the processor directly.
