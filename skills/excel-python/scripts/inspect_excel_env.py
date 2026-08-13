#!/usr/bin/env python3
"""Report installed Excel-library versions and selected API signatures as JSON."""

from __future__ import annotations

import importlib
import importlib.metadata
import inspect
import json
import platform
import sys
from typing import Any

DEFAULT_APIS = (
    "openpyxl.load_workbook",
    "openpyxl.Workbook",
    "xlsxwriter.Workbook",
    "polars.read_excel",
    "polars.DataFrame.write_excel",
)
PACKAGES = {
    "openpyxl": "openpyxl",
    "xlsxwriter": "XlsxWriter",
    "polars": "polars",
    "fastexcel": "fastexcel",
    "xlwings": "xlwings",
}


def resolve(path: str) -> Any:
    parts = path.split(".")
    value: Any = importlib.import_module(parts[0])
    for part in parts[1:]:
        value = getattr(value, part)
    return value


def package_evidence(module_name: str, distribution: str) -> dict[str, object]:
    try:
        version = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return {"available": False, "version": None}
    try:
        module = importlib.import_module(module_name)
        module_version = getattr(module, "__version__", None)
    except ImportError:
        module_version = None
    return {"available": True, "version": version, "module_version": module_version}


def api_evidence(path: str) -> dict[str, object]:
    try:
        value = resolve(path)
    except (AttributeError, ImportError, ModuleNotFoundError) as exc:
        return {"available": False, "signature": None, "error": type(exc).__name__}
    try:
        signature = str(inspect.signature(value))
    except (TypeError, ValueError):
        signature = None
    return {"available": True, "signature": signature, "type": type(value).__name__}


def main() -> int:
    paths = tuple(dict.fromkeys(sys.argv[1:] or DEFAULT_APIS))
    packages = {
        name: package_evidence(name, distribution)
        for name, distribution in PACKAGES.items()
    }
    payload = {
        "schema_version": 1,
        "ok": True,
        "python": platform.python_version(),
        "packages": packages,
        "apis": {path: api_evidence(path) for path in paths},
        "features": {
            "polars_calamine_available": bool(
                packages["polars"]["available"] and packages["fastexcel"]["available"]
            ),
            "excel_runtime_library_available": bool(packages["xlwings"]["available"]),
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
