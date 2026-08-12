# Pydantic validation and serialization recipes

Load the recipe matching the external boundary. The model contract includes
input mode, coercion, errors, and output representation—not only field names.

## Recipe `pydantic.strict-money-boundary`

**Use when:** Untrusted Python data carries money, identifiers, and a closed payment kind.
**Inspect first:** Confirm whether upstream sends Python objects or JSON bytes and whether numeric strings are legitimate.
**Invariants:** Extras are rejected, money is positive Decimal, and Python input is not coerced.

```python
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


PositiveMoney = Annotated[Decimal, Field(gt=0, strict=True)]


class Payment(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    payment_id: str
    kind: Literal["card"]
    amount: PositiveMoney
    currency: str = Field(pattern=r"^[A-Z]{3}$")


def validate_payment(value: object) -> Payment:
    return Payment.model_validate(value)
```

**Do not use when:** JSON numeric strings are an accepted wire representation; specify and test that separate mode.
**Verify:** Test booleans, floats, numeric strings, zero, negative amounts, extras, and JSON-versus-Python behavior.

## Recipe `pydantic.adapter-collection-boundary`

**Use when:** A list or mapping needs validation without inventing a wrapper model.
**Inspect first:** Fix the complete container type, strictness, and output mode.
**Invariants:** Every member is validated and serialization uses the same adapter contract.

```python
from pydantic import BaseModel, ConfigDict, TypeAdapter


class Event(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    attempts: int


events_adapter = TypeAdapter(list[Event])


def parse_events(payload: object) -> list[Event]:
    return events_adapter.validate_python(payload, strict=True)


def dump_events(events: list[Event]) -> list[dict[str, object]]:
    return events_adapter.dump_python(events, mode="json")
```

**Do not use when:** The container itself has named domain invariants or metadata; model that wrapper explicitly.
**Verify:** Test one invalid member, extras, wrong container shape, strict fields, and JSON-safe output.

## Recipe `pydantic.discriminated-command-union`

**Use when:** One payload has several variants selected by a stable tag.
**Inspect first:** Confirm the discriminator name, closed tag set, and whether unknown variants must be rejected.
**Invariants:** Each tag selects exactly one model and variant-specific fields do not leak across branches.

```python
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class CreateUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["create_user"]
    email: str


class DeleteUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["delete_user"]
    user_id: str


Command = Annotated[CreateUser | DeleteUser, Field(discriminator="kind")]
command_adapter = TypeAdapter(Command)


def parse_command(payload: object) -> Command:
    return command_adapter.validate_python(payload)
```

**Do not use when:** Selection depends on heuristics or overlapping field presence; establish an explicit protocol tag first.
**Verify:** Test every tag, missing/unknown tags, cross-variant fields, extras, and error locations.

## Recipe `pydantic.directional-aliases`

**Use when:** Inbound and outbound field names differ during an API migration.
**Inspect first:** Decide accepted old/new input names, emitted name, and collision behavior.
**Invariants:** Validation aliases and serialization aliases are intentional and independently tested.

```python
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class Customer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(
        validation_alias=AliasChoices("customer_id", "customerId"),
        serialization_alias="customerId",
    )


def normalize_customer(payload: object) -> dict[str, object]:
    value = Customer.model_validate(payload)
    return value.model_dump(mode="json", by_alias=True)
```

**Do not use when:** Both aliases appearing together have no defined precedence; reject ambiguity at ingress first.
**Verify:** Test each accepted input name, both together, internal attribute access, `by_alias` output, and extras.
