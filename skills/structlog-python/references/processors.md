# Processor contracts and ordering

Load this reference when adding, reordering, or debugging processors.

## Default ordering model

Use the shortest chain that satisfies the event contract:

```text
context merge
-> early filtering (when architecture permits)
-> level/logger normalization
-> deterministic enrichment
-> redaction/drop policy
-> stack and exception transformation
-> exactly one renderer or handoff
```

This is a decision model, not a mandatory fixed list. Remove a stage when no
contract or evaluation requires it.

## Invariants

- Every retained nonterminal path returns an event dictionary.
- Every dropped path raises `DropEvent` intentionally.
- Exactly one terminal processor returns data for the wrapped logger.
- No secret reaches the terminal processor.
- Processor output keys have stable meanings and types.
- A processor does not perform network/database I/O or unbounded computation.
- Filtering happens before expensive work when compatible with integration and
  level ownership.
- Exceptions are transformed before the renderer.

## Collision policy

Choose one policy for each injected key:

- `setdefault`: caller/bound context may intentionally override the default;
- assignment: the processor owns the key and overrides earlier values;
- reject: raise or mark a contract violation if the key already exists;
- namespace: place a nested mapping under an owned key.

Do not overwrite fields accidentally. In particular, avoid processors that
silently repurpose `event`, `level`, `timestamp`, logger name, or correlation
keys.

## Renderer switch

Development and production may use different terminal renderers, but the
processors before them should preserve one event schema:

```python
shared_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    redact_secrets,
    structlog.processors.format_exc_info,
]

renderer = (
    structlog.dev.ConsoleRenderer(colors=False)
    if development
    else structlog.processors.JSONRenderer()
)
processors = [*shared_processors, renderer]
```

Do not branch event names or field semantics by renderer.

## Exception shape

Text tracebacks are easy for humans and common collectors. Structured traceback
dictionaries support programmatic processing but expand the public schema and
can expose locals depending on formatter configuration. Choose from the actual
consumer. Test:

- exception type and message are present;
- the event name and correlation fields survive;
- no secret-bearing local values are emitted;
- non-exception events do not receive fake exception fields;
- the output remains parseable by its collector.

## Redaction is defense in depth

Prefer not to bind secrets at all. A redaction processor protects against known
keys but cannot reliably detect every secret hidden in arbitrary objects or
messages. Keep payloads bounded and structured; never log whole request/config
objects to avoid enumerating their fields.

Test exact banned keys and nested structures the application permits. If nested
arbitrary mappings are allowed, define a bounded recursive policy rather than a
top-level-only redactor.

## Performance claims

Do not call a chain fast or nonblocking from processor count alone. Measure:

- events discarded by level before enrichment;
- timestamp/callsite/traceback cost;
- serializer cost and return type;
- destination write behavior and contention;
- async wrapper/executor overhead;
- allocation or large-value expansion.

Caching bound loggers avoids repeated assembly but also makes temporary global
configuration changes less observable. Optimize after semantic tests exist.
