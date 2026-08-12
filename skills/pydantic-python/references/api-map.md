# Pydantic intent-to-API map

Load this reference when selecting an abstraction or API family. Inspect the
installed version before relying on exact newer parameters.

## Model and arbitrary-type boundaries

| Intent | API | Guardrail |
|---|---|---|
| Named object from Python input | `Model.model_validate(value)` | State strictness, extras, and attribute-loading policy. |
| Named object from JSON | `Model.model_validate_json(data)` | Do not `json.loads` first unless non-Pydantic processing requires it. |
| String mapping with JSON-style conversion | `Model.model_validate_strings(mapping)` | Only for an actual string-mapping source. |
| Arbitrary annotated type | `adapter = TypeAdapter(T)` | Reuse the adapter; output is `T`. |
| True single-root model | `class Items(RootModel[list[Item]])` | `RootModel` cannot use model extra-field policy for the root payload. |
| Validate call arguments | `@validate_call` | Use at a real boundary; it adds runtime work and is not a static type checker. |
| Load object attributes | `ConfigDict(from_attributes=True)` or call option | Declare it; do not revive v1 `orm_mode`. |
| Trusted data bypass | `model_construct()` | Only already-validated data with a proven need; never untrusted input. |

## Fields and reusable constraints

| Intent | API |
|---|---|
| Numeric/string/container constraint | `Annotated[T, Field(...)]` |
| Generated default | `Field(default_factory=...)` |
| Validate a default | `Field(..., validate_default=True)` or model config |
| Private runtime attribute not a model field | `PrivateAttr` |
| Computed serialized property | `@computed_field` on a property, version-grounded |
| Pydantic dataclass semantics | `pydantic.dataclasses.dataclass` |
| Standard dataclass/TypedDict validation without conversion to model | `TypeAdapter` |

Prefer named `Annotated` aliases for a reusable semantic type:

```python
from typing import Annotated
from pydantic import Field

OrderId = Annotated[int, Field(gt=0, strict=True)]
```

Do not hide field-specific descriptions, aliases, or defaults in a global type
alias when they belong to one wire contract.

## Validators

| Rule | Use |
|---|---|
| Raw single-field normalization | `@field_validator(name, mode="before")` |
| Typed single-field invariant | `@field_validator(name)` / after |
| Reusable typed validator | `Annotated[T, AfterValidator(fn)]` |
| Reusable raw transform | `Annotated[T, BeforeValidator(fn)]` |
| Cross-field invariant | `@model_validator(mode="after")` |
| Full control around normal validation | wrap validator, only with a demonstrated need |

Before validators must accept arbitrary objects. After validators must return the
typed value or model. Avoid plain validators unless bypassing core validation is
the explicit desired contract.

## Unions

| Input shape | Use |
|---|---|
| Variants have a stable tag | Discriminated union with `Literal` tag fields and `Field(discriminator="tag")` |
| Untagged variants are unavoidable and default best-match behavior is acceptable | default smart union, with ambiguity tests |
| First-success order is the contract | `Field(union_mode="left_to_right")`, with coercion tests |
| Discriminator logic cannot be a field | callable discriminator plus `Tag`, after reading current docs |

Prefer discriminated unions: one branch is selected, errors are focused, and
behavior is more predictable. Do not use validators to guess a variant when the
payload can carry a stable tag.

Canonical tagged union:

```python
from typing import Annotated, Literal
from pydantic import BaseModel, Field, TypeAdapter


class EmailJob(BaseModel):
    kind: Literal["email"]
    address: str


class SmsJob(BaseModel):
    kind: Literal["sms"]
    number: str


Job = Annotated[EmailJob | SmsJob, Field(discriminator="kind")]
job_adapter = TypeAdapter(Job)
```

## Aliases

| Contract | Use |
|---|---|
| Same alternate name for input and output | `Field(alias="external")` |
| Input-only name | `Field(validation_alias="external")` |
| Multiple input names during migration | `validation_alias=AliasChoices(...)` |
| Input nested path | `validation_alias=AliasPath(...)` |
| Output-only name | `Field(serialization_alias="external")`, dump with `by_alias=True` |
| Systematic naming | configured `alias_generator`/`AliasGenerator`, with precedence tests |

Alias acceptance and alias output are separate switches. Test both field names
and aliases at validation, and `by_alias=False/True` at serialization.

## Serialization and schema

| Intent | API |
|---|---|
| Python dictionary | `model_dump()` |
| JSON-compatible dictionary | `model_dump(mode="json")` |
| JSON text | `model_dump_json()` |
| Custom one-field output | `@field_serializer` or serializer metadata |
| Whole-model output contract | `@model_serializer` only when normal model shape is insufficient |
| Validation schema | `model_json_schema(mode="validation")` |
| Serialization schema | `model_json_schema(mode="serialization")` |
| Arbitrary type schema | `TypeAdapter(T).json_schema(...)` |

Schema generation documents the compiled contract; it does not execute external
OpenAPI/client generation or prove backward compatibility. Diff schema plus
behavior tests when public contracts change.

## Dynamic models and advanced hooks

Use `create_model()` only when fields truly come from runtime metadata. Prefer
normal class definitions for static schemas: they are clearer to type checkers
and reviewers. Custom core-schema hooks and JSON-schema hooks are advanced
extension points; ground them in the exact version and test validation,
serialization, and schema output together.
