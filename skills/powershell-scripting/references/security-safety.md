# Security and mutation safety

## Data boundaries

- Treat command text, paths, regexes, filters, templates, and format strings as
  different languages. Do not promote input data into code with `Invoke-Expression`.
- Do not embed credentials or accept plain-text secrets merely to simplify tests.
- Redact secrets before diagnostics and avoid passing them in native argv, which may
  be visible to process inspection or logs.

## Mutation boundary

1. Resolve and validate the intended target without mutating it.
2. Reject roots, empty values, scope escapes, ambiguous wildcard input, and unexpected
   item types.
3. Present an accurate `ShouldProcess` target and action.
4. Perform one bounded operation only when `ShouldProcess` returns true.
5. Verify postconditions and surface partial failure.

Do not implement `-Force`, confirmation suppression, recursive deletion, or error
suppression unless the contract defines why it is safe. `SupportsShouldProcess` is
not authorization for a live operation; it is a script interface that still requires
the caller's authority.
