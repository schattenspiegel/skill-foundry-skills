# Parameters, pipeline objects, and streams

Define the command as a mapping from input objects to output objects plus explicit
diagnostics and side effects.

- Validate shape at binding time when a precise parameter attribute can express it;
  validate environment-dependent facts in the body with a useful error.
- Use `ValueFromPipeline` only when each input is processed independently. Use
  `ValueFromPipelineByPropertyName` only for a deliberate property contract.
- Avoid implicit array unrolling surprises: test zero, one, and many results and use
  the unary comma only when a collection must remain one output object.
- Keep status/progress off the success stream. Prefer verbose/information channels for
  optional diagnostics and warning/error channels for actionable conditions.
- Do not format (`Format-*`) inside reusable processing code. Formatting objects are
  terminal presentation artifacts.
- Avoid ambient state: pass inputs explicitly and restore any preference, location,
  or environment state the script temporarily owns.

Pester tests should consume the command exactly as callers do and assert object type,
property names, cardinality, ordering, and error behavior rather than matching source
tokens.
