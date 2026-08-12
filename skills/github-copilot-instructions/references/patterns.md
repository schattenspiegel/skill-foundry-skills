# Instruction patterns

## Pattern: scoped path instructions
**Use when:** A stable rule applies only to a known file family.
**Inspect first:** Actual paths, existing instruction overlap, and the current host schema.
**Invariants:** Matching paths receive the rule; near misses do not; no conflict with broad instructions.
```markdown
---
applyTo: "src/**/*.py,tests/**/*.py"
---

- Target Python 3.11 or newer.
- Run `uv run pytest` after changing Python behavior.
- Run `uv run ruff check .` before completion.
```
**Do not use when:** The rule applies to nearly every repository task.
**Verify:** Parse YAML, expand the glob against positive/negative paths, and confirm the file appears in VS Code response references.
