# Standard-library integration

Load this reference when structlog and standard-library `logging` coexist or a
framework already owns handlers.

Before writing configuration, inventory:

- handlers and formatters already installed;
- framework logging setup and initialization order;
- foreign library records that must share output;
- desired output streams and level filters.

Decision rules:

- If structlog renders, let stdlib transport the rendered value without adding a second competing format.
- If `ProcessorFormatter` renders both sources, end the structlog chain with
  `ProcessorFormatter.wrap_for_formatter`; use `foreign_pre_chain` for foreign
  records; remove `_record`/`_from_structlog` metadata on the formatter side
  before the final renderer.
- If stdlib renders, use the installed documented render-to-logging adapter and
  prove the required fields survive into `LogRecord` attributes.
- Avoid repeated `basicConfig()` or root-handler additions. Test initialization twice when startup can be re-entered.

Use current official examples for exact processor names and signatures.

## `ProcessorFormatter` anchor

```python
shared = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_log_level,
]

structlog.configure(
    processors=[
        *shared,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

formatter = structlog.stdlib.ProcessorFormatter(
    foreign_pre_chain=shared,
    processors=[
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.processors.JSONRenderer(),
    ],
)
```

Attach the formatter to exactly the intended handlers. Root/child propagation,
framework handlers, and repeated initialization remain stdlib concerns and must
be tested with real records from both sources.

## Duplicate-output diagnostic

1. List root and named logger handlers, levels, and `propagate` values.
2. Identify the one layer that renders each structlog and foreign record.
3. Initialize twice in a test and count outputs.
4. Emit one event from a child logger and one foreign stdlib event.
5. Remove only the duplicate owner; do not suppress propagation blindly.
