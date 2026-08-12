# API grounding

Load this reference when a Pydantic or pydantic-settings name, parameter,
conversion, source, migration rule, or serializer behavior can drift.

## Evidence order

1. Inspect project dependency declarations, lockfile, supported Python versions,
   public schemas, and behavior tests.
2. Inspect installed Pydantic and pydantic-settings versions independently.
3. Inspect exact installed objects and signatures.
4. Use matching official versioned documentation and migration guides.
5. Add a behavior test for each supported version branch.

Pydantic and pydantic-settings release separately. A compatible Pydantic version
does not prove a settings helper exists.

## Inspection helper

From the installed skill directory:

```text
python scripts/inspect_pydantic.py
```

The helper emits one JSON object with Python, Pydantic, and pydantic-settings
availability/version evidence plus inspected APIs. Pydantic absence exits `2`.
pydantic-settings absence is reported but does not prevent core Pydantic
inspection.

Focused paths:

```text
python scripts/inspect_pydantic.py \
  BaseModel.model_validate BaseModel.model_dump settings.BaseSettings
```

`settings.*` resolves from `pydantic_settings`; other paths resolve from
`pydantic`. Unknown paths remain `available: false`.

## Re-check when

- migrating v1 configuration, validators, ORM loading, or serialization;
- depending on strict conversion for a specific type/input mode;
- using alias validation/serialization switches;
- using union modes or callable discriminators;
- enabling polymorphic/serialize-as-any output;
- relying on newer computed-field/default-factory options;
- customizing settings source priority, CLI parsing, nested secrets, dotenv
  resolution, or decoding controls;
- asserting exact error messages or JSON Schema layout.

Prefer semantic error `type` and `loc` assertions over whole message snapshots.
Prefer the oldest common public API when a project intentionally supports a
range; otherwise pin and test the deployed version.
