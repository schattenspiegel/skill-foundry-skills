# Testing structlog behavior

Load this reference before deciding that one captured string proves the logging
contract.

Separate two test layers:

1. Event semantics: capture event dictionaries and assert stable names, keys, levels, context, and exception markers.
2. Integration/rendering: exercise configured handlers/formatters and parse JSON or inspect plain output.

Cover:

- minimum canonical event;
- level filtering;
- bound and context-local fields;
- two sequential requests to detect leakage;
- exception logging;
- one foreign stdlib record when integrated;
- initialization twice when configuration can be re-entered;
- absence of secret or banned fields.

## Pick the observable

| Requirement | Assert |
|---|---|
| Event name/keys/context/level before rendering | event dictionary through `LogCapture` |
| Processor enrichment or redaction | event dictionary after the tested processors |
| Renderer schema | parsed JSON or exact plain output with colors disabled |
| Wrapped logger arguments | `CapturingLoggerFactory.logger.calls` |
| Foreign stdlib interoperability | output from real handler + formatter + stream |
| No context leak | two sequential boundaries plus `get_contextvars()`/events |
| Concurrency isolation | overlapping real framework tasks with distinct IDs |
| Initialization idempotence | configure twice through the application entrypoint and count each event once |

`structlog.testing.capture_logs()` disables the configured processor chain while
its context is active. Pass processors explicitly when the test depends on them.
A logger already cached with `cache_logger_on_first_use=True` is not affected, so
disable caching for capture-based tests or construct the logger inside the
capture context. The helper changes global configuration and is not suitable for
concurrent tests; serialize those tests or use an isolated configuration.
