# orjson options and integration

Start with `option=0`. Combine only documented installed flags with bitwise OR.
Maintain a test that fails if each flag disappears.

Common contract-driven families include indentation, trailing newline, sorted
keys, UTC formatting, naive-datetime assumptions, non-string keys, strict
integers, NumPy serialization, and passthrough of otherwise native types. Names
and semantics can drift; inspect `dir(orjson)` and upstream docs for the pinned
version instead of copying a flag list from this reference.

## File and JSON Lines

orjson does not open files. Match modes to data:

```python
with path.open("wb") as target:
    target.write(orjson.dumps(value))
    target.write(b"\n")
```

For JSONL, serialize one record at a time and ensure each record contains no raw
line delimiter outside JSON escaping. For a standard JSON document, write one
value; do not append multiple values separated only by whitespace.

## Framework adapters

Inspect whether the framework expects a Python value, text, or bytes. A custom
response renderer usually owns `dumps`; middleware must not encode the result a
second time. Preserve status, headers, media type, and charset semantics. In a
logging pipeline, decide whether the final renderer returns bytes or text from
the processor chain rather than decoding in arbitrary processors.

## Trusted fragments

`orjson.Fragment` is appropriate for JSON bytes produced and stored by a
trusted serializer when avoiding reparse/re-encode is a measured requirement.
It can produce invalid or structurally surprising output if fed untrusted or
wrongly scoped bytes. Validate at ingestion and keep the fragment source typed
and documented.
