"""Print installed structlog version and drift-prone API evidence as JSON."""

from __future__ import annotations

import argparse
import inspect
import json
import platform
from collections.abc import Sequence
from typing import Any

DEFAULT_APIS = (
    "BoundLoggerBase.bind",
    "BoundLoggerBase.new",
    "BoundLoggerBase.try_unbind",
    "configure",
    "contextvars.bind_contextvars",
    "contextvars.bound_contextvars",
    "contextvars.clear_contextvars",
    "contextvars.merge_contextvars",
    "dev.ConsoleRenderer",
    "get_logger",
    "make_filtering_bound_logger",
    "processors.CallsiteParameterAdder",
    "processors.ExceptionRenderer",
    "processors.JSONRenderer",
    "processors.TimeStamper",
    "processors.dict_tracebacks",
    "stdlib.ProcessorFormatter",
    "stdlib.ProcessorFormatter.remove_processors_meta",
    "stdlib.ProcessorFormatter.wrap_for_formatter",
    "stdlib.filter_by_level",
    "stdlib.recreate_defaults",
    "stdlib.render_to_log_args_and_kwargs",
    "stdlib.render_to_log_kwargs",
    "testing.CapturingLoggerFactory",
    "testing.LogCapture",
    "testing.capture_logs",
    "tracebacks.ExceptionDictTransformer",
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


def _api(root: Any, dotted_path: str) -> dict[str, bool | str | None]:
    value = _resolve(root, dotted_path)
    return {
        "available": value is not None,
        "signature": _signature(value) if value is not None else None,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect installed structlog APIs and signatures.",
    )
    parser.add_argument(
        "apis",
        nargs="*",
        metavar="API",
        help=(
            "Optional dotted paths such as stdlib.ProcessorFormatter or "
            "contextvars.bound_contextvars. Defaults to the compatibility set."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        import structlog
    except ImportError:
        print(json.dumps({"ok": False, "error": "structlog is not importable"}))
        return 2

    requested = tuple(dict.fromkeys(args.apis or DEFAULT_APIS))
    evidence = {
        "ok": True,
        "python": platform.python_version(),
        "structlog": getattr(structlog, "__version__", "unknown"),
        "apis": {path: _api(structlog, path) for path in requested},
    }
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
