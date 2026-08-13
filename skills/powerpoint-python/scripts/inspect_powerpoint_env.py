#!/usr/bin/env python3
"""Report PowerPoint Python dependencies, selected APIs, and renderers as JSON."""

from __future__ import annotations

import importlib
import importlib.metadata
import inspect
import json
import platform
import shutil
import subprocess
import sys
from typing import Any

SCHEMA_VERSION = 1
PACKAGES = {
    "python-pptx": "pptx",
    "lxml": "lxml",
    "Pillow": "PIL",
    "XlsxWriter": "xlsxwriter",
}
DEFAULT_APIS = (
    "pptx.Presentation",
    "pptx.presentation.Presentation.save",
    "pptx.text.text.TextFrame.fit_text",
    "pptx.shapes.shapetree.SlideShapes.add_picture",
    "pptx.slide.NotesSlide.notes_text_frame",
)
RENDERERS = ("soffice", "libreoffice")


def resolve(path: str) -> Any:
    parts = path.split(".")
    value: Any = importlib.import_module(parts[0])
    for part in parts[1:]:
        value = getattr(value, part)
    return value


def package_evidence(distribution: str, module_name: str) -> dict[str, object]:
    try:
        version = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return {"available": False, "version": None, "module_version": None}
    try:
        module_version = getattr(importlib.import_module(module_name), "__version__", None)
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


def renderer_evidence(executable: str) -> dict[str, object]:
    path = shutil.which(executable)
    if path is None:
        return {"available": False, "path": None, "version": None}
    try:
        completed = subprocess.run(
            [path, "--version"],
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
        version = (completed.stdout or completed.stderr).strip().splitlines()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        version = None
    return {"available": True, "path": path, "version": version}


def main(argv: list[str] | None = None) -> int:
    paths = tuple(dict.fromkeys((argv if argv is not None else sys.argv[1:]) or DEFAULT_APIS))
    payload = {
        "schema_version": SCHEMA_VERSION,
        "ok": True,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            distribution: package_evidence(distribution, module)
            for distribution, module in PACKAGES.items()
        },
        "apis": {path: api_evidence(path) for path in paths},
        "image_backends": {
            "pillow": importlib.util.find_spec("PIL") is not None,
        },
        "renderers": {name: renderer_evidence(name) for name in RENDERERS},
        "powerpoint_runtime_checked": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
