# Pydantic settings and security recipes

Settings are validated source resolution. Instantiate once at the composition
root, then inject the immutable result into application code.

## Recipe `pydantic.subclass-secret-boundary`

**Use when:** A public field may hold a richer runtime subtype containing secrets.
**Inspect first:** Confirm the annotation-level wire contract and installed subclass serialization behavior.
**Invariants:** Output is limited to fields declared by the public annotation.

```python
from pydantic import BaseModel, SecretStr


class PublicUser(BaseModel):
    user_id: str


class InternalUser(PublicUser):
    token: SecretStr


class Envelope(BaseModel):
    user: PublicUser


def public_payload(user: InternalUser) -> dict[str, object]:
    return Envelope(user=user).model_dump(mode="json")
```

**Do not use when:** Runtime subtype fields are intentionally part of the wire contract; model and review that union explicitly.
**Verify:** Assert the token key and raw secret never appear in Python-mode, JSON-mode, or JSON-text output.

## Recipe `pydantic.validated-construction`

**Use when:** Data crosses a trust boundary before becoming a model.
**Inspect first:** Determine whether input is Python, JSON, attributes, or an already validated model.
**Invariants:** Untrusted input always passes through validation; no `model_construct` bypass exists.

```python
from pydantic import BaseModel, ConfigDict, ValidationError


class Job(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    job_id: str
    attempts: int


def decode_job(payload: bytes) -> Job:
    try:
        return Job.model_validate_json(payload, strict=True)
    except ValidationError as exc:
        raise ValueError("invalid job payload") from exc
```

**Do not use when:** A private deserializer has already proven the exact model invariants; document that proof before considering trusted construction.
**Verify:** Test malformed JSON, coercible values, extras, required fields, and that errors preserve a useful cause.

## Recipe `pydantic.nested-environment-settings`

**Use when:** Environment variables configure nested application and database settings.
**Inspect first:** Confirm prefix, case sensitivity, delimiter, dotenv policy, and secret source.
**Invariants:** Nested keys are deterministic, extras fail, and secrets are never dumped.

```python
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseModel):
    host: str
    port: int = 5432
    password: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_nested_delimiter="__",
        extra="forbid",
    )
    debug: bool = False
    database: Database


def load_settings() -> Settings:
    return Settings()
```

**Do not use when:** Arbitrary environment names or custom encoded complex values are required; define a tested custom source instead.
**Verify:** Test nested overrides, invalid ports, missing secrets, unknown dotenv keys, and redacted representations.

## Recipe `pydantic.explicit-source-priority`

**Use when:** A documented policy requires environment variables to override initializer values.
**Inspect first:** Confirm all enabled sources and the installed `settings_customise_sources` signature.
**Invariants:** The returned source tuple is the complete precedence contract and is tested with conflicting values.

```python
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    SecretsSettingsSource,
)


class Settings(BaseSettings):
    region: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: InitSettingsSource,
        env_settings: EnvSettingsSource,
        dotenv_settings: DotEnvSettingsSource,
        file_secret_settings: SecretsSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, init_settings, dotenv_settings, file_secret_settings
```

**Do not use when:** Default source priority already matches the contract; avoid custom policy with no behavioral need.
**Verify:** Set conflicting values in every enabled source and assert the documented winner plus fallback sequence.
