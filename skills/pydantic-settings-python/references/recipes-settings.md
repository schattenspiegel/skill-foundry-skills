# Settings recipes

## Recipe `pydantic-settings.nested-environment`
**Use when:** Nested application settings are supplied through prefixed environment variables.
**Inspect first:** Prefix, delimiter, case policy, dotenv policy, extras, and secret source.
**Invariants:** Nested names are deterministic, invalid values fail, and secrets are not serialized or logged.
```python
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseModel):
    url: str
    password: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_nested_delimiter="__", extra="forbid")
    database: Database
```
**Do not use when:** A tiny script needs one optional environment value and has no settings model.
**Verify:** Isolate the environment and test nested override, invalid input, missing secret, and redaction.

## Recipe `pydantic-settings.explicit-priority`
**Use when:** Application policy requires a nondefault source order.
**Inspect first:** Enabled sources and the installed customization signature.
**Invariants:** The returned tuple exactly encodes policy and collision tests prove it.
```python
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


class Settings(BaseSettings):
    endpoint: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, init_settings, dotenv_settings, file_secret_settings
```
**Do not use when:** Documented default priority already matches policy.
**Verify:** Supply conflicting values from every enabled source and assert the winner.
