"""Print version and drift-prone Polars API evidence as JSON."""

from __future__ import annotations

import argparse
import inspect
import json
import platform
from collections.abc import Sequence
from typing import Any

DEFAULT_APIS = (
    "DataFrame",
    "DataFrame.explode",
    "DataFrame.filter",
    "DataFrame.gather",
    "DataFrame.get_column",
    "DataFrame.group_by",
    "DataFrame.group_by_dynamic",
    "DataFrame.join",
    "DataFrame.join_where",
    "DataFrame.pivot",
    "DataFrame.rolling",
    "DataFrame.select",
    "DataFrame.unique",
    "DataFrame.unpivot",
    "DataFrame.with_columns",
    "DataFrame.write_parquet",
    "Expr.map_batches",
    "Expr.map_elements",
    "Expr.over",
    "LazyFrame",
    "LazyFrame.collect",
    "LazyFrame.collect_batches",
    "LazyFrame.collect_schema",
    "LazyFrame.group_by_dynamic",
    "LazyFrame.join",
    "LazyFrame.join_asof",
    "LazyFrame.join_where",
    "LazyFrame.map_batches",
    "LazyFrame.pivot",
    "LazyFrame.rolling",
    "LazyFrame.show_graph",
    "LazyFrame.sink_batches",
    "LazyFrame.sink_parquet",
    "Series",
    "col",
    "concat",
    "map_batches",
    "read_csv",
    "scan_csv",
    "scan_parquet",
    "selectors.numeric",
    "testing.assert_frame_equal",
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
        description="Inspect installed Polars API availability and signatures.",
    )
    parser.add_argument(
        "apis",
        nargs="*",
        metavar="API",
        help=(
            "Optional dotted API paths such as DataFrame.select, "
            "selectors.numeric, or testing.assert_frame_equal. "
            "Without paths, inspect the skill's default compatibility set."
        ),
    )
    return parser


def _inspect_api(
    path: str,
    *,
    polars: Any,
    selectors: Any,
    testing: Any,
) -> dict[str, bool | str | None]:
    if path.startswith("selectors."):
        return _api(selectors, path.removeprefix("selectors."))
    if path.startswith("testing."):
        return _api(testing, path.removeprefix("testing."))
    return _api(polars, path)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        import polars as pl
        from polars import selectors, testing
    except ImportError:
        print(json.dumps({"ok": False, "error": "polars is not importable"}))
        return 2

    requested_apis = tuple(dict.fromkeys(args.apis or DEFAULT_APIS))
    evidence = {
        "ok": True,
        "python": platform.python_version(),
        "polars": getattr(pl, "__version__", "unknown"),
        "apis": {
            path: _inspect_api(
                path,
                polars=pl,
                selectors=selectors,
                testing=testing,
            )
            for path in requested_apis
        },
    }
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
