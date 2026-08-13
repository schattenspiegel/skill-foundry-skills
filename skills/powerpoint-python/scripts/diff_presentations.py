#!/usr/bin/env python3
"""Compare two presentations semantically and emit a preservation report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from inspect_presentation import DEFAULT_DETAILS_LIMIT, SCHEMA_VERSION, inspect

IGNORED_TOP_LEVEL = {"path", "size"}


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    result: dict[str, Any] = {}
    if isinstance(value, dict):
        for key in sorted(value):
            if not prefix and key in IGNORED_TOP_LEVEL:
                continue
            child = f"{prefix}.{key}" if prefix else key
            result.update(flatten(value[key], child))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            result.update(flatten(item, f"{prefix}[{index}]"))
    else:
        result[prefix] = value
    return result


def category(path: str) -> str:
    if path.startswith("package.opaque_hashes") or any(
        token in path for token in ("vba", "timing", "transition", "diagrams", "embeddings")
    ):
        return "preservation_sensitive"
    if path.startswith("package.relationship") or path.startswith("package.external"):
        return "relationships"
    if path.startswith("package.media"):
        return "media"
    if path.startswith("package."):
        return "package"
    if ".slides" in path or path.startswith("presentation.slides"):
        return "slides"
    return "presentation"


def compare(before: dict[str, Any], after: dict[str, Any], limit: int) -> dict[str, Any]:
    left = flatten(before)
    right = flatten(after)
    differences = []
    for path in sorted(set(left) | set(right)):
        old = left.get(path, {"missing": True})
        new = right.get(path, {"missing": True})
        if old != new:
            differences.append(
                {"path": path, "category": category(path), "before": old, "after": new}
            )
    categories: dict[str, int] = {}
    for item in differences:
        categories[item["category"]] = categories.get(item["category"], 0) + 1
    return {
        "equivalent": not differences,
        "difference_count": len(differences),
        "categories": dict(sorted(categories.items())),
        "differences": differences[:limit],
        "truncated": len(differences) > limit,
        "note": "Semantic inventory comparison is not runtime or visual equivalence.",
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("before", type=Path)
    result.add_argument("after", type=Path)
    result.add_argument("--details-limit", type=int, default=DEFAULT_DETAILS_LIMIT)
    result.add_argument("--fail-on-diff", action="store_true")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.details_limit < 0:
        print(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "ok": False,
                    "error": "details-limit must be non-negative",
                }
            )
        )
        return 2
    try:
        before = inspect(args.before.resolve(), limit=args.details_limit)
        after = inspect(args.after.resolve(), limit=args.details_limit)
        result = compare(before, after, args.details_limit)
    except Exception as exc:  # deterministic CLI failure boundary
        print(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "ok": False,
                    "error": f"{type(exc).__name__}: {exc}",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    payload = {
        "schema_version": SCHEMA_VERSION,
        "ok": True,
        "before": str(args.before.resolve()),
        "after": str(args.after.resolve()),
        **result,
    }
    print(json.dumps(payload, indent=2, sort_keys=True, default=str))
    return 1 if args.fail_on_diff and not result["equivalent"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
