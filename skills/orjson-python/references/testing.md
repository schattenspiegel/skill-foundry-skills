# Testing orjson behavior

Test the wire contract directly.

- Assert `isinstance(encoded, bytes)` when bytes are public.
- Assert decoded structure and application shape separately.
- Assert exact bytes only for contractual ordering, whitespace, newline, or
  datetime spelling.
- Test malformed JSON, invalid UTF-8 where relevant, unsupported types, and
  out-of-range/depth policy.
- Test aware UTC, non-UTC offset, and naive datetime branches.
- Test key collisions before enabling non-string keys.
- Test the custom `default` accepted types and one rejected neighboring type.
- Test JSONL with zero, one, and several records and a final-line policy.

Do not rely only on `loads(dumps(value)) == value`: datetimes, tuples, dataclass
instances, non-string keys, and custom types may intentionally decode to a
different Python representation. Compare to the declared JSON-domain value.

For a migration from `json`, run both implementations against a corpus of real
payload shapes and compare either exact wire bytes when contractual or decoded
semantics plus declared formatting. Benchmark only after correctness, using the
actual adapter so decode copies or framework double-encoding are included.
