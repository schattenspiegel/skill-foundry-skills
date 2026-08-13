# Pydantic core object model

Load this reference when choosing what Pydantic object to build or when
validation, model state, and serialization are being conflated.

## Schema compilation and execution

A model class or type adapter compiles Python annotations and metadata into a
core schema. Runtime data is executed against that schema:

```text
annotations + Field/Annotated + config + validators/serializers
                              -> core schema

input -> core validator -> typed output or ValidationError
typed output -> core serializer -> Python-mode or JSON-mode output
core schema -> JSON Schema document
```

Validation and serialization share the schema but are not inverse operations in
all cases. Defaults, aliases, exclusions, custom serializers, subclass policy,
and output modes can make the serialized shape differ from input.

## The objects

| Object | What it represents | Normal output |
|---|---|---|
| `BaseModel` subclass | Named fields, model configuration, validators, serializers, and class APIs | Model instance |
| Model instance | Typed state after validation; may still be mutable unless configured otherwise | `model_dump*` output when serialized |
| `FieldInfo` from `Field(...)` | Per-field defaults, constraints, aliases, inclusion/exclusion, and schema metadata | Part of compiled schema |
| `Annotated[T, ...]` | Type `T` plus reusable validation/serialization metadata | `T` after validation |
| `TypeAdapter[T]` | Reusable compiled validator, serializer, and JSON Schema generator for `T` | Exactly `T`, not an invented wrapper model |
| `RootModel[T]` | Named Pydantic model around one root value | Root-model instance with `.root` |
| `ValidationError` | Structured collection of data-validation failures | `.errors()` records with locations/types/context |

## Choose the runtime output first

| Required runtime result | Use | Avoid |
|---|---|---|
| Named typed domain/boundary object | `BaseModel` | A dict whose validation is forgotten after return |
| `list[Item]`, union, primitive, `TypedDict`, dataclass, or protocol payload | `TypeAdapter[T]` | A one-field model created solely to access validation |
| Public single-root type with model methods/schema identity | `RootModel[T]` | `RootModel` when a plain `TypeAdapter` output is enough |
| Trusted internal state with static typing only | dataclass/`TypedDict` | Runtime validation with no boundary |

Construct and reuse a `TypeAdapter`; creating it repeatedly rebuilds validation
and serialization machinery unnecessarily.

## Fields, requiredness, and defaults

An annotation defines the allowed type. A default defines whether omission is
allowed and what value is used. `T | None` permits the value `None`; it does not
make the field optional unless a default is supplied:

```python
class Patch(BaseModel):
    display_name: str | None  # required, but None is valid
    nickname: str | None = None  # may be omitted
```

Use `Field(default_factory=...)` for generated values. Model defaults are not
validated by default. Enable default validation intentionally when invalid
defaults must be rejected and test that behavior.

## Input modes

| Input representation | Model | Type adapter |
|---|---|---|
| Python objects/mappings | `model_validate` | `validate_python` |
| JSON text/bytes | `model_validate_json` | `validate_json` |
| Nested mapping of strings using JSON-mode conversions | `model_validate_strings` | inspect installed adapter support if required |

Strict validation is representation-sensitive. For example, some date-like
types reject a Python string in strict Python mode but accept the JSON string in
strict JSON mode. Test every representation the application exposes.

## Validation stages

| Stage | Sees | Use |
|---|---|---|
| before | arbitrary raw input | narrow normalization or legacy-shape translation |
| after | typed field/model | invariants and typed normalization |
| plain | raw input and bypasses remaining core validation | rare complete replacement with an explicit contract |
| wrap | handler plus control before/after core logic | rare delegation/error-policy cases |

Field validators should handle one field. Model validators should handle
cross-field invariants. Validators are not I/O hooks or dependency-injection
containers.

## Serialization modes

| Operation | Result |
|---|---|
| `model_dump()` | Python-mode dictionary; values can remain Python objects |
| `model_dump(mode="json")` | Dictionary/list/scalars converted to JSON-compatible Python values |
| `model_dump_json()` | JSON string |
| `TypeAdapter.dump_python(..., mode=...)` | Python or JSON-mode value for arbitrary `T` |
| `TypeAdapter.dump_json(...)` | JSON bytes for arbitrary `T` in current v2 APIs |

`dict(model)` iterates fields without recursively dumping nested models. Do not
use it as a wire serializer.

Configuration-source assembly belongs to the `pydantic-settings-python` skill.
This skill owns only the validation and serialization behavior of the resulting
Pydantic schema.
