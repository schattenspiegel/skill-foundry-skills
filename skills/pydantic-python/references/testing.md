# Testing Pydantic behavior

For each boundary, cover:

- smallest valid payload;
- complete valid payload;
- missing required field;
- wrong type with coercion expected;
- wrong type with strict rejection expected;
- unknown key under the chosen extra policy;
- each field and cross-field validator failure;
- Python and JSON mode when both are supported;
- `model_dump`/`model_dump_json` output, aliases, and excluded fields;
- stable error locations and error types when callers depend on them.

Assert `ValidationError.errors()` fields needed by the application rather than snapshotting an entire human-formatted message that may change.

## Add falsifiers by feature

| Feature | Required falsifier |
|---|---|
| Strictness | a value accepted only through coercion |
| Extra policy | a plausible misspelled key |
| Optional/nullable field | omitted versus explicit `None` |
| Union | ambiguous input and wrong/missing discriminator |
| Before validator | an object of an unexpected raw type |
| Model invariant | each field valid alone but combination invalid |
| Alias | field name and each accepted external name |
| Serializer | Python mode, JSON mode, and any exclusion/alias switch exposed |
| Subclass field | sensitive subclass-only value does not leak |
| `TypeAdapter` collection | empty, one invalid element, and exact output type |
| Settings | collision between every enabled adjacent priority source |

For public JSON Schema, test meaningful required fields, aliases, tags, and
formats rather than snapshotting every generated definition ordering. Pair schema
assertions with runtime validation and serialization tests.
