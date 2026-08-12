# Validation boundaries

Load this reference when deciding coercion, extras, input mode, attribute
loading, or validation bypasses.

Choose the entrypoint from the actual input:

| Input | Entry point |
|---|---|
| Python dictionary/object for a model | `Model.model_validate(...)` |
| JSON text or bytes for a model | `Model.model_validate_json(...)` |
| String-key/string-value mapping needing JSON-style coercion | inspect `model_validate_strings(...)` support and use when it matches the contract |
| Arbitrary annotated type | `TypeAdapter(type).validate_python(...)` or matching JSON method |

Decide extra data explicitly at external boundaries. `forbid` detects misspelled or unexpected fields; `ignore` is appropriate only when forward-compatible dropping is intentional; `allow` is appropriate only when extra values are part of the contract.

Do not use `model_construct()` for ordinary validation or assumed speed. It bypasses validation. Use it only for already-validated trusted data with a measured reason.

## Boundary decision matrix

| Boundary | Typical policy |
|---|---|
| Untrusted protocol identifiers, permissions, money | strict fields/model; `extra="forbid"`; explicit aliases |
| User form or environment strings | documented coercion can be intentional; test every accepted spelling |
| Database/ORM object attributes | `from_attributes=True` only when object loading is the declared source |
| Internal already-typed data | normal construction may still protect invariants; bypass only with trusted provenance |
| Forward-compatible external payload | `extra="ignore"` only when silent dropping is intentionally part of compatibility |

Strict does not mean identical behavior for Python and JSON input. Test both.
Use the official conversion table for individual types rather than extrapolating
from `int` or `str`.

## Error translation

Catch `ValidationError` where the application converts it into an HTTP, CLI,
queue, or domain error. Preserve the original exception as cause. Expose only
the stable error location/type/context required by the public contract; raw
input values in error output can contain secrets.
