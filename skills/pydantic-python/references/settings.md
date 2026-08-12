# pydantic-settings source model

Load this reference for `BaseSettings`, environment names, dotenv, nested
configuration, secrets directories, source priority, or custom settings sources.

## Separate package and object

In Pydantic v2, import settings APIs from the separate package:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
```

`BaseSettings` is a Pydantic model with an input-source assembly phase. Use
ordinary nested `BaseModel` types for subsections unless a nested type itself
must independently resolve sources.

Instantiate settings once at the composition root, then inject the validated
instance. Re-instantiating throughout the application repeatedly reads mutable
process/file state and makes tests nondeterministic.

## Default priority

Highest wins in the current documented default order:

1. CLI arguments, only when CLI parsing is enabled;
2. explicit `Settings(...)` initializer arguments;
3. environment variables;
4. dotenv values;
5. secrets-directory values;
6. field defaults.

Do not assume dotenv overrides a real environment variable. If custom source
priority is required, override `settings_customise_sources` and return sources
in explicit highest-to-lowest order. Test one collision across every enabled
source.

## Names and aliases

| Need | Configuration |
|---|---|
| Prefix ordinary environment names | `SettingsConfigDict(env_prefix="APP_")` |
| One input environment name | `Field(validation_alias="LEGACY_NAME")` |
| Several accepted names | `AliasChoices(...)` |
| Case-sensitive matching | `case_sensitive=True`, with Windows caveat |
| Ignore empty env values and use lower source/default | `env_ignore_empty=True` |

Aliases and prefixes have interaction rules that evolve; inspect current docs
and test the exact names rather than deriving them mentally.

## Complex and nested values

Simple environment values enter as strings and are validated normally. Complex
types such as lists, sets, dicts, and submodels are JSON-decoded by default:

```text
APP_ALLOWED_HOSTS='["a.example", "b.example"]'
```

For nested keys:

```python
model_config = SettingsConfigDict(
    env_prefix="APP_",
    env_nested_delimiter="__",
)
```

then `APP_DATABASE__HOST=db.internal` targets `database.host`. A nested key
overrides the matching sub-key from a top-level JSON environment value. Limit
split depth when underscores inside field names would otherwise be interpreted
as extra nesting.

If the external format is intentionally comma-separated rather than JSON, use
the installed documented decoding control such as field `NoDecode` plus a
narrow before validator. Do not catch invalid JSON and silently invent a
different grammar.

## Dotenv

Configure a known file and encoding with `env_file`/`env_file_encoding`, or pass
the supported initializer override at startup. Relative paths resolve from the
process working directory; they are not automatically searched through all
parent directories. Test startup from the actual deployment working directory.

Current settings behavior can reject extra keys from a dotenv file even when
they do not match a prefix, depending on `extra` policy. Prefer a dedicated
dotenv file or set `extra="ignore"` only when ignoring unrelated keys is the
declared compatibility contract.

Never commit production secrets in `.env`. Treat dotenv as an input source, not
a secret-management guarantee.

## Secrets directories

`secrets_dir` maps file names to field names and file contents to values. The
default source has top-level/nesting limitations; inspect `NestedSecretsSettingsSource`
when nested secret fields are required. Decide whether a missing secrets
directory is allowed, warned, or an error in the installed version.

Use Pydantic secret types for sensitive values and never log `model_dump()` of
the settings object. File permissions, secret rotation, and provider access are
deployment responsibilities outside model validation.

## Custom sources

Override `settings_customise_sources` only when built-in init/env/dotenv/secrets
sources cannot model the contract. Return a tuple in explicit priority order.
When adding TOML, YAML, cloud secret managers, or another source:

- add only the required package extra/dependency;
- define file/path/account selection outside hidden magic;
- bound network and error behavior;
- distinguish source-loading failures from `ValidationError`;
- test collisions, missing source, malformed source, nested values, and secrets;
- do not perform asynchronous network I/O inside synchronous construction
  without the documented integration.

## Settings test matrix

Test with isolated environment and filesystem state:

- defaults only;
- required key absent;
- exact environment name and type conversion;
- initializer versus environment collision;
- environment versus dotenv collision;
- nested delimiter and top-level JSON collision;
- malformed complex JSON;
- missing and present dotenv path from deployment cwd;
- secrets directory present/missing and secret non-disclosure;
- unknown dotenv keys under the chosen `extra` policy;
- custom source order if overridden.

Restore environment variables after each test; do not let process-global state
leak across cases.
