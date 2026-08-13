# API grounding

Load this reference when a Pydantic name, parameter, conversion, migration rule,
or serializer behavior can drift.

## Evidence order

1. Inspect project dependency declarations, lockfile, supported Python versions,
   public schemas, and behavior tests.
2. Inspect the installed Pydantic version.
3. Inspect exact installed objects and signatures.
4. Use matching official versioned documentation and migration guides.
5. Add a behavior test for each supported version branch.

## Inspection helper

From the installed skill directory:

```text
python scripts/inspect_pydantic.py
```

The helper emits one JSON object with Python, Pydantic version evidence, and
inspected APIs. Pydantic absence exits `2`.

Focused paths:

```text
python scripts/inspect_pydantic.py \
  BaseModel.model_validate BaseModel.model_dump TypeAdapter.validate_python
```

Paths resolve from `pydantic`. Unknown paths remain `available: false`.

## Re-check when

- migrating v1 configuration, validators, ORM loading, or serialization;
- depending on strict conversion for a specific type/input mode;
- using alias validation/serialization switches;
- using union modes or callable discriminators;
- enabling polymorphic/serialize-as-any output;
- relying on newer computed-field/default-factory options;
- asserting exact error messages or JSON Schema layout.

Prefer semantic error `type` and `loc` assertions over whole message snapshots.
Prefer the oldest common public API when a project intentionally supports a
range; otherwise pin and test the deployed version.
