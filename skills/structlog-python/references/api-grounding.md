# API grounding

Load this reference when a processor, renderer, async method, factory, stdlib
adapter, or testing helper may differ by structlog version.

## Evidence order

1. Read the target project's dependency declarations, lockfile, framework setup,
   and logging tests.
2. Inspect the active environment's structlog version.
3. Inspect exact installed objects and signatures.
4. Consult the matching official versioned structlog documentation.
5. Add a compatibility test for each supported branch.

Do not implement the newest stable documentation against an older project lock.
Do not preserve stale syntax merely because it appears in the prompt.

## Inspection helper

From the installed skill directory:

```text
python scripts/inspect_structlog.py
```

The helper returns one JSON object with Python and structlog versions plus
availability/signatures for the skill's drift-prone APIs. Exit `2` means
structlog is not importable. Unknown paths remain `available: false` instead of
crashing the whole probe.

Pass focused dotted paths when needed:

```text
python scripts/inspect_structlog.py \
  stdlib.ProcessorFormatter contextvars.bound_contextvars processors.JSONRenderer
```

Useful direct evidence:

```python
import inspect
import structlog

print(structlog.__version__)
print(inspect.signature(structlog.configure))
print(inspect.signature(structlog.stdlib.ProcessorFormatter))
```

## Re-check when

- using `ProcessorFormatter` metadata/wrapper options;
- choosing `render_to_log_kwargs` versus another stdlib adapter;
- using async log methods or executor behavior;
- passing a non-standard JSON serializer that returns bytes;
- selecting write/bytes logger factories;
- relying on callsite or exception renderer options;
- using temporary testing helpers with cached loggers;
- copying examples that use deprecated thread-local context.

The stable docs can describe 26.1.0 while the target project deploys another
version. Record both documentation and installed evidence.
