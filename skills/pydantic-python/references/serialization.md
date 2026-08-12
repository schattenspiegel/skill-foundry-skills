# Serialization and aliases

Load this reference when the external output shape, aliases, exclusions,
subclasses, or custom serializers matter.

## Pick the output representation

| Consumer expects | Use |
|---|---|
| Python objects such as `datetime`, `UUID`, `Decimal` | `model_dump(mode="python")` |
| JSON-compatible Python containers/scalars | `model_dump(mode="json")` |
| JSON text | `model_dump_json()` |
| Same operations for arbitrary `T` | matching `TypeAdapter.dump_python` or `dump_json` |

Do not infer JSON compatibility from a Python-mode dump. Do not call `dict(model)`
for recursive serialization: nested models remain model instances.

## Alias directions

```python
from pydantic import BaseModel, ConfigDict, Field


class UserWire(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(
        validation_alias="userId",
        serialization_alias="user_id",
    )
```

`validation_alias` selects accepted input names. `serialization_alias` selects
the output name only when serialization enables aliases (`by_alias=True`). If
the same external name is required in both directions, `alias=` can express
both. Test field-name acceptance separately from alias acceptance; configuration
controls whether both are legal.

Use `AliasChoices` for an explicit migration window with multiple accepted input
names. Remove old aliases after the compatibility window and a regression run.

## Omission policy

| Option | Omits |
|---|---|
| `exclude_unset=True` | fields not explicitly set |
| `exclude_defaults=True` | values equal to defaults |
| `exclude_none=True` | `None` values |
| field `exclude=True` | field from normal serialization |
| call `include` / `exclude` | exact requested paths |

These options answer different questions and can change PATCH semantics. For
example, explicitly setting a field to its default is distinguishable through
`model_fields_set` and `exclude_unset`, but can disappear with
`exclude_defaults`. Test omitted, explicit-default, and explicit-`None` inputs.

## Subclass safety

When a field annotation is a model-like base type, default serialization uses
the fields declared on that annotation even if the runtime value is a subclass.
This prevents a newly added subclass secret from appearing unexpectedly:

```python
class User(BaseModel):
    name: str


class UserLogin(User):
    password: str


class Envelope(BaseModel):
    user: User


assert Envelope(user=UserLogin(name="Ada", password="secret")).model_dump() == {
    "user": {"name": "Ada"}
}
```

Runtime-type/polymorphic serialization options are version-sensitive and can
expose subclass-only fields. Enable them only when the wire contract requires
polymorphism, enumerate sensitive fields, and add a regression test.

## Custom serializers

Use a serializer only when normal modes/configuration cannot express the output:

- field serializer for one field;
- model serializer for a fundamentally different whole-model shape;
- plain mode to replace normal serialization;
- wrap mode to delegate to normal serialization and adjust its result;
- `when_used` to limit the representation where it applies.

Keep serializers deterministic and side-effect free. Declare/inspect return
types where schema generation depends on them. Test both Python and JSON modes
if the API exposes both.

Serialization does not validate post-construction assignment unless model
configuration does. A serializer can therefore receive invalid runtime state;
do not silently coerce it into plausible wire data. Prefer preventing invalid
mutation or fail clearly.

## Secret types

`SecretStr`/`SecretBytes` protect ordinary display and serialization from raw
secret exposure, but calling the explicit secret-value accessor retrieves the
secret. Never include whole settings/model dumps in logs. Test that repr,
Python-mode dump, JSON-mode dump, custom serializers, and error translation do
not expose raw secrets.

## Round-trip and fallback options

Options such as round-trip serialization, fallback serializers,
serialize-as-any, or polymorphic serialization alter semantics and can drift.
Use them only for a concrete consumer contract and inspect the installed
signature. A fallback that stringifies arbitrary objects can hide unsupported
types; prefer an explicit serializer for known types.
