# structlog intent-to-API map

Load this reference to route a concrete logging intent to the smallest structlog
abstraction. Exact signatures and newer helpers remain version-sensitive.

## Logger and context operations

| Intent | API | Guardrail |
|---|---|---|
| Obtain a configured logger proxy | `structlog.get_logger(*factory_args, **initial_values)` | Positional arguments are interpreted by the selected logger factory. |
| Add stable local context | `child = log.bind(**values)` | Keep the returned logger. |
| Remove required local keys | `child = log.unbind(*keys)` | Missing keys raise; use this to detect broken invariants. |
| Remove optional local keys | `child = log.try_unbind(*keys)` | Use only when absence is part of the contract. |
| Reset local bound context | `child = log.new(**values)` | Does not clear contextvars. |
| Add request/task context | `bind_contextvars(**values)` | Call `clear_contextvars()` first at an independent boundary. |
| Remove contextvar keys | `unbind_contextvars(*keys)` | Use tokens/reset semantics only when exact restoration is needed. |
| Temporary contextvars | `with bound_contextvars(**values): ...` | Restores prior values on exit. |
| Inspect contextvars in a test | `get_contextvars()` | Avoid using it as application business state. |

## Configuration and filtering

| Intent | API family | Guardrail |
|---|---|---|
| Custom process-wide defaults | `structlog.configure(...)` | Run once at startup before logger caching. |
| Restore current library defaults in tests | `reset_defaults()` | Global mutation; do not call per request. |
| Simple stdlib-backed defaults | `structlog.stdlib.recreate_defaults(log_level=...)` | Inspect whether its exact pipeline/output contract fits. |
| Filter before processors without stdlib | `make_filtering_bound_logger(level)` | The returned wrapper class owns level filtering. |
| Respect stdlib logger effective levels | `structlog.stdlib.filter_by_level` | Requires a compatible stdlib wrapped logger. |
| Runtime dynamic filtering | inspect `structlog.stdlib.BoundLogger` and stdlib levels | Do not claim hot reconfiguration for a statically filtering wrapper. |

## Enrichment and normalization

| Intent | Processor | Placement |
|---|---|---|
| Merge request/task fields | `contextvars.merge_contextvars` | First, before consumers of context. |
| Add log level | `stdlib.add_log_level` or installed equivalent | Before renderer; keep key naming stable. |
| Add logger name | `stdlib.add_logger_name` | Only when the wrapped logger provides it. |
| Add UTC ISO timestamp | `processors.TimeStamper(fmt="iso", utc=True)` | Before renderer; define timestamp owner once. |
| Format positional event arguments | `stdlib.PositionalArgumentsFormatter()` | Only if the call contract permits positional formatting. |
| Render requested stack info | `processors.StackInfoRenderer()` | Before renderer; can be expensive. |
| Add selected callsite fields | `processors.CallsiteParameterAdder(...)` | Select only operationally required parameters; measure cost. |
| Rename/drop keys | `processors.EventRenamer`, custom processor, or renderer option after inspection | Preserve the external schema and test collisions. |
| Decode bytes/event text | `processors.UnicodeDecoder()` when inputs require it | Do not add ceremonial processors without a failing case. |

## Exceptions

| Required output | Use | Guardrail |
|---|---|---|
| Conventional traceback text in an `exception` field | `.exception(...)` or `exc_info=True`, then `processors.format_exc_info` | Run before renderer. |
| Structured traceback frames for JSON consumers | `ExceptionRenderer(ExceptionDictTransformer(show_locals=False))` after installed-version inspection | This is a schema change; do not expose frame locals by default. |
| Custom exception representation | `ExceptionRenderer(custom_formatter)` | Formatter must have a deterministic, bounded, secret-safe contract. |
| Stack without an active exception | `stack_info=True` plus `StackInfoRenderer` | Do not substitute stack info for exception info. |

Do not stringify an exception into the event name. Do not emit both a raw
exception object and a rendered traceback unless the consumer contract requires
and safely handles both.

## Renderers and factories

| Consumer | Terminal/factory direction | Guardrail |
|---|---|---|
| Production JSON text | `JSONRenderer` + a text-compatible print/write factory | One JSON object per event; parse output in tests. |
| Human terminal | `dev.ConsoleRenderer` | Disable or control colors for snapshots/files. |
| Simple key/value text | `processors.KeyValueRenderer` | Define ordering only where consumers require it. |
| Bytes serializer | `JSONRenderer(serializer=...)` + a bytes-compatible factory | Verify serializer return type and sink compatibility. |
| Mixed structlog/stdlib one-renderer output | `ProcessorFormatter` architecture | See integration reference. |
| Existing stdlib formatter owns output | installed render-to-log adapter | Test field survival in the resulting `LogRecord`. |

Prefer `WriteLogger` over `PrintLogger` when structlog and stdlib write to the
same stream and atomic whole-line writes matter. Confirm the active version and
stream type.

## Custom processor patterns

Add a stable field without overwriting the caller:

```python
def add_service(logger, method_name, event_dict):
    event_dict.setdefault("service", "orders")
    return event_dict
```

Redact before output:

```python
SECRET_KEYS = {"authorization", "password", "token"}


def redact_secrets(logger, method_name, event_dict):
    for key in SECRET_KEYS & event_dict.keys():
        event_dict[key] = "[redacted]"
    return event_dict
```

Drop only from a declared policy:

```python
def drop_healthcheck(logger, method_name, event_dict):
    if event_dict.get("path") == "/health":
        raise structlog.DropEvent
    return event_dict
```

Keep processors deterministic and side-effect free except for the terminal
output operation. If a processor must read process state, inject or isolate it
so tests can prove behavior.

## Testing APIs

| Test target | API |
|---|---|
| Event dictionaries at a test-specific pipeline endpoint | `structlog.testing.LogCapture` |
| Temporary global capture for small serialized tests | `capture_logs(processors=...)` |
| Final call made on wrapped logger | `CapturingLoggerFactory` / `CapturingLogger` |
| Exact standalone JSON | real configured writer plus `json.loads` |
| Mixed stdlib integration | real `ProcessorFormatter`, handler, and stream |
| Context isolation | `get_contextvars()` plus sequential and framework-boundary tests |

`capture_logs()` globally replaces processors and does not affect already cached
loggers. It is not safe for concurrent tests. Prefer test-specific configuration
and `LogCapture` when processor behavior itself matters.
