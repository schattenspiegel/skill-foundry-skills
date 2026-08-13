"""Print installed Pydantic API evidence as JSON."""

from __future__ import annotations

import argparse
import inspect
import json
import platform
from collections.abc import Sequence
from typing import Any

DEFAULT_APIS = (
    "BaseModel.model_dump",
    "BaseModel.model_dump_json",
    "BaseModel.model_json_schema",
    "BaseModel.model_validate",
    "BaseModel.model_validate_json",
    "BaseModel.model_validate_strings",
    "ConfigDict",
    "RootModel",
    "TypeAdapter",
    "TypeAdapter.dump_json",
    "TypeAdapter.dump_python",
    "TypeAdapter.validate_json",
    "TypeAdapter.validate_python",
    "computed_field",
    "field_serializer",
    "field_validator",
    "model_serializer",
    "model_validator",
    "validate_call",
)


def _signature(value: Any) -> str | None:
    try:
        return str(inspect.signature(value))
    except (TypeError, ValueError):
        return None


def _resolve(root: Any, dotted_path: str) -> Any | None:
    value = root
    for part in dotted_path.split("."):
        value = getattr(value, part, None)
        if value is None:
            return None
    return value


def _api(root: Any | None, dotted_path: str) -> dict[str, bool | str | None]:
    value = _resolve(root, dotted_path) if root is not None else None
    return {
        "available": value is not None,
        "signature": _signature(value) if value is not None else None,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect installed Pydantic APIs.",
    )
    parser.add_argument(
        "apis",
        nargs="*",
        metavar="API",
        help="Optional paths from pydantic. Defaults to the compatibility set.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        import pydantic
    except ImportError:
        print(json.dumps({"ok": False, "error": "pydantic is not importable"}))
        return 2

    requested = tuple(dict.fromkeys(args.apis or DEFAULT_APIS))
    apis: dict[str, dict[str, bool | str | None]] = {}
    for path in requested:
        apis[path] = _api(pydantic, path)

    evidence = {
        "ok": True,
        "python": platform.python_version(),
        "pydantic": getattr(pydantic, "__version__", "unknown"),
        "apis": apis,
    }
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
