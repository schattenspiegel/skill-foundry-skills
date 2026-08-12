# structlog object and event model

Load this reference when the task depends on what structlog creates, owns, or
passes between processors.

## The objects

| Object | Contains | Created by | Important behavior |
|---|---|---|---|
| Lazy logger proxy | Initial values and optional logger-construction arguments | `structlog.get_logger(...)` | Final bound logger assembly can be deferred until first use. |
| Bound logger | Local context, a wrapped logger, and processors | Configured wrapper class | `.bind()`, `.unbind()`, `.try_unbind()`, and `.new()` return derived bound loggers. Keep the return. |
| Local context | Key/value fields attached to one bound logger | `get_logger(initial=...)`, `.bind(...)` | It is not the same store as contextvars. |
| Event dictionary | A fresh mapping for one call | Bound context plus keyword fields plus `event` | Later call fields override same-named bound fields. Processors may mutate this copy. |
| Processor | Callable accepting wrapped logger, method name, and event dictionary | Configuration or formatter | Returns an event dictionary for continued processing, returns terminal arguments at the end, or raises `DropEvent`. |
| Processor chain | Ordered processors | `structlog.configure(processors=...)` | A function composition; each output becomes the next input. Order changes semantics. |
| Terminal processor | Last processor | Renderer or adapter choice | Returns a string/bytes or `(args, kwargs)` accepted by the wrapped logger. No event-dictionary processor can follow it. |
| Wrapped logger | Actual output API | Logger factory | Receives terminal output: print/write/bytes logger or standard-library `Logger`. |
| Logger factory | Callable creating wrapped loggers | `logger_factory=` | Determines output destination and the arguments accepted by `get_logger(...)`. |
| Context-variable store | Per-execution-context values | `bind_contextvars(...)` | Enters an event only if `merge_contextvars` runs. Must be cleared at unit-of-work start. |

## One event call

Given:

```python
base = structlog.get_logger("billing").bind(component="invoice", attempt=1)
log = base.bind(invoice_id="inv_7")
log.info("invoice_sent", attempt=2, channel="email")
```

the call's event dictionary begins conceptually as:

```python
{
    "component": "invoice",
    "invoice_id": "inv_7",
    "attempt": 2,
    "channel": "email",
    "event": "invoice_sent",
}
```

`base` is still usable without `invoice_id`; `.bind()` did not mutate it. The
call field `attempt=2` overrides the bound `attempt=1` for this event. Processors
then enrich, redact, filter, adapt, or render that dictionary in order.

Do not use the same key for incompatible meanings at different scopes. Define
key ownership in the event contract.

## The configuration dimensions

`structlog.configure()` selects independent dimensions:

| Dimension | Question |
|---|---|
| `processors` | Which transformations run, and in what order? |
| `wrapper_class` | Which bound logger methods and filtering behavior exist? |
| `context_class` | Which mapping stores local bound context? Usually the default is sufficient. |
| `logger_factory` | Which wrapped logger receives final output? |
| `cache_logger_on_first_use` | Is the assembled logger reused after first use? |

Do not change one dimension to compensate for misunderstanding another. For
example, `context_class` does not provide request-local context; contextvars do.
A wrapper-level filter does not configure stdlib handler levels.

Configuration is global default state. Configure before first log use. With
caching enabled, proxies already used can retain their assembled configuration;
tests that temporarily replace processors must avoid or account for that.

## Local binding versus contextvars

| Lifetime | Mechanism | Example |
|---|---|---|
| Process/component logger | `.bind(component="worker")` | retained on the returned logger |
| One object/unit helper | `.bind(order_id=...)` | retained only by code receiving the child logger |
| Whole request/task execution context | `bind_contextvars(request_id=...)` | available to all loggers in the same execution context after merge |
| One nested execution scope | `with bound_contextvars(operation=...):` | restored on exit |
| One call | keyword fields on `.info(...)` | only that event |

Clear contextvars at the start of every independent request or job. Clearing a
bound logger's local context with `.new()` does not clear contextvars, and
`clear_contextvars()` does not alter fields bound on a logger.

## Output ownership

Trace one event all the way to the stream:

```text
structlog renders -> wrapped logger transports -> handler writes
```

or:

```text
structlog wraps event dictionary -> stdlib LogRecord -> ProcessorFormatter renders -> handler writes
```

or:

```text
structlog adapts fields to stdlib arguments -> existing formatter renders -> handler writes
```

Choose one. If two arrows both render, duplicate or double-formatted output is
likely. If no arrow renders, a raw event dictionary or unsupported argument shape
can reach the sink.

## Processor return contract

Before the terminal processor:

```python
from typing import Any


def add_service(
    logger: object,
    method_name: str,
    event_dict: dict[str, Any],
) -> dict[str, Any]:
    event_dict.setdefault("service", "billing")
    return event_dict
```

The terminal processor must instead adapt to the wrapped logger. A renderer
normally returns text or bytes. `ProcessorFormatter.wrap_for_formatter` returns
arguments that preserve the event dictionary inside a stdlib `LogRecord` for
formatter-side processing.

## Stable event contract

For each public event define:

- stable machine event name;
- required and optional keys with types/units;
- level and escalation policy;
- timestamp convention and owner;
- correlation identifiers and their lifetime;
- exception representation;
- banned secret or payload fields;
- compatibility policy for field removal/rename.

Changing `amount` from cents to major units without changing its name is a
contract break. So is changing an exception from text to nested dictionaries if
collectors or tests consume the old shape.
