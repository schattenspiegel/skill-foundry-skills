# DuckDB version and API grounding

The Python package bundles a DuckDB engine, and stable documentation can move
ahead of a project's installed wheel. Inspect both before using a signature,
setting, file-scan option, result conversion, extension, or concurrency claim.

From the installed skill directory run:

```text
python scripts/inspect_duckdb.py duckdb.connect duckdb.DuckDBPyConnection.execute
```

The helper emits package/engine versions and inspectable signatures. Native
extension methods may not expose a Python signature; use installed help and a
small disposable database probe. Ground SQL behavior with `SELECT version()` or
`duckdb.version()` as supported locally.

Do not silently copy options from online examples. Gate capabilities by the
installed package, and test file/extension behavior in the deployment
environment where filesystem, network, and native-extension policies apply.
