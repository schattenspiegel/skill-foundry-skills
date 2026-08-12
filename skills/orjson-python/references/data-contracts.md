# orjson data contracts

## JSON domain

Decoding produces only JSON-compatible Python types: mappings with string keys,
lists, strings, numbers, booleans, and `None`. Encoding supports documented
native types plus values transformed by `default`. It is not a model validator
and does not restore application classes.

The output of `dumps` is UTF-8 bytes. Decide which layer owns conversion:

```text
domain object -> orjson bytes -> binary transport/file
domain object -> orjson bytes -> one UTF-8 decode -> text-only boundary
```

Never alternate encode/decode merely to satisfy mismatched local types.

## Datetime contract

Before serialization classify values as:

- aware instants with an accepted offset;
- UTC instants whose representation must use `+00:00` or `Z`;
- local wall times tied to a named timezone elsewhere; or
- naive values that are invalid/ambiguous for the contract.

Serialization formatting cannot repair ambiguity. Normalize at the domain
boundary and test daylight-saving edges when local time matters.

## Default dispatcher

The dispatcher is a closed conversion table:

```python
def default(value):
    if isinstance(value, Decimal):
        return str(value)  # only if the wire schema declares a string
    if isinstance(value, Path):
        return str(value)
    raise TypeError
```

Do not use `str(value)` as a catch-all. It hides unsupported types and often
changes numbers, enums, secrets, and identifiers into an undocumented schema.
Do not recursively call `dumps` from `default`; return a supported Python value.

## Duplicate/colliding keys

JSON object member names are strings. Enabling non-string keys can collapse
distinct Python keys to the same rendered name. If uniqueness or signatures
matter, normalize keys before encoding and reject collisions. Decoding cannot
recover original non-string key types.
