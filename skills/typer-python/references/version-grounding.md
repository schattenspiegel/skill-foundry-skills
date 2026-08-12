# Typer version grounding

Typer evolves with Click and Python typing. Ground edits in the target project.

1. Inspect declared dependencies and lockfiles.
2. Run `python -c 'import importlib.metadata as m; print(m.version("typer"))'`
   with the project's interpreter.
3. Inspect the exact callable when a copied keyword or annotation pattern is
   uncertain: `inspect.signature(typer.Option)`, `typer.Argument`, `typer.Typer`,
   or the relevant method.
4. Run the project's help and tests with warnings enabled.

Canonical examples in this skill were executed against Typer 0.27.1 on Python
3.11 during authoring. That is evidence for those examples, not a compatibility
claim for every project version.

High-drift surfaces include `Annotated` recommendations, Click compatibility,
rich help behavior, shell completion hooks, supported parameter types, and
exception rendering. Preserve a project's pinned style if a migration is not
requested. If no installed evidence exists, use the project's documented lower
bound and avoid an unverified new keyword.
