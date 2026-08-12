#!/usr/bin/env python3
"""Report installed DuckDB versions and selected dotted API signatures."""

from __future__ import annotations

import importlib
import importlib.metadata
import inspect
import json
import sys


def resolve(path: str) -> object:
    parts = path.split(".")
    value: object = importlib.import_module(parts[0])
    for part in parts[1:]:
        value = getattr(value, part)
    return value


def main() -> int:
    import duckdb

    paths = sys.argv[1:] or ["duckdb.connect", "duckdb.DuckDBPyConnection.execute"]
    apis: dict[str, object] = {}
    for path in paths:
        try:
            value = resolve(path)
            try:
                signature = str(inspect.signature(value))
            except (TypeError, ValueError):
                signature = None
            apis[path] = {"signature": signature, "type": type(value).__name__}
        except (AttributeError, ImportError, ModuleNotFoundError) as exc:
            apis[path] = {"error": f"{type(exc).__name__}: {exc}"}
    payload = {
        "distribution": importlib.metadata.version("duckdb"),
        "module": duckdb.__version__,
        "engine": duckdb.version(),
        "apis": apis,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
