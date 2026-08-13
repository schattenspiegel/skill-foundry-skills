#!/usr/bin/env python3
"""Validate structural and semantic presentation invariants against optional JSON."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from typing import Any

from inspect_presentation import DEFAULT_DETAILS_LIMIT, SCHEMA_VERSION, inspect


def issue(
    code: str,
    severity: str,
    message: str,
    *,
    slide: int | None = None,
    shape: str | None = None,
) -> dict[str, object]:
    return {
        "code": code,
        "severity": severity,
        "message": message,
        "slide": slide,
        "shape": shape,
    }


def shape_identity(shape: dict[str, Any]) -> set[str]:
    return {str(shape.get("shape_id")), str(shape.get("name")), str(shape.get("index"))}


def intersects(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return not (
        left["left"] + left["width"] <= right["left"]
        or right["left"] + right["width"] <= left["left"]
        or left["top"] + left["height"] <= right["top"]
        or right["top"] + right["height"] <= left["top"]
    )


def exempt_overlap(
    left: dict[str, Any],
    right: dict[str, Any],
    exemptions: list[list[object]],
    slide_width: int,
    slide_height: int,
) -> bool:
    canvas = slide_width * slide_height
    if canvas and (
        left["width"] * left["height"] >= canvas * 0.9
        or right["width"] * right["height"] >= canvas * 0.9
    ):
        return True
    ignored_types = {"LINE", "FREEFORM", "CONNECTOR"}
    if str(left["shape_type"]) in ignored_types or str(right["shape_type"]) in ignored_types:
        return True
    left_ids = shape_identity(left)
    right_ids = shape_identity(right)
    return any(
        len(pair) == 2
        and (
            (str(pair[0]) in left_ids and str(pair[1]) in right_ids)
            or (str(pair[1]) in left_ids and str(pair[0]) in right_ids)
        )
        for pair in exemptions
    )


def contract_slide(contract: dict[str, Any], number: int) -> dict[str, Any]:
    for slide in contract.get("slides", []):
        if int(slide.get("number", number)) == number:
            return slide
    return {}


def find_shape(shapes: list[dict[str, Any]], selector: object) -> dict[str, Any] | None:
    text = str(selector)
    return next((shape for shape in shapes if text in shape_identity(shape)), None)


def validate(
    report: dict[str, Any],
    contract: dict[str, Any],
    *,
    available_parts: set[str] | None = None,
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    presentation = report["presentation"]
    width = int(presentation["slide_width"])
    height = int(presentation["slide_height"])
    expected = contract.get("presentation", {})
    for key, actual, code in (
        ("slide_width", width, "SLIDE_WIDTH_MISMATCH"),
        ("slide_height", height, "SLIDE_HEIGHT_MISMATCH"),
        ("slide_count", presentation["slide_count"], "SLIDE_COUNT_MISMATCH"),
    ):
        if key in expected and expected[key] != actual:
            result.append(issue(code, "error", f"expected {expected[key]!r}, found {actual!r}"))

    titles: list[str] = []
    for slide in presentation["slides"]:
        number = int(slide["number"])
        slide_contract = contract_slide(contract, number)
        title = slide.get("title")
        if title:
            titles.append(str(title))
        if (
            slide_contract.get("title_required", contract.get("title_required", False))
            and not title
        ):
            result.append(issue("MISSING_TITLE", "error", "slide requires a title", slide=number))
        if "title" in slide_contract and slide_contract["title"] != title:
            result.append(
                issue(
                    "TITLE_MISMATCH",
                    "error",
                    f"expected {slide_contract['title']!r}, found {title!r}",
                    slide=number,
                )
            )
        if "layout" in slide_contract and slide_contract["layout"] != slide["layout"]:
            result.append(
                issue(
                    "LAYOUT_MISMATCH",
                    "error",
                    f"expected {slide_contract['layout']!r}, found {slide['layout']!r}",
                    slide=number,
                )
            )
        notes_policy = slide_contract.get("notes", "optional")
        if notes_policy == "required" and not slide["notes_present"]:
            result.append(
                issue("NOTES_REQUIRED", "error", "speaker notes are required", slide=number)
            )
        if notes_policy == "forbidden" and slide["notes_present"]:
            result.append(
                issue("NOTES_FORBIDDEN", "error", "speaker notes are forbidden", slide=number)
            )

        shapes = slide["shapes"]["items"]
        minimum_font_size = slide_contract.get(
            "minimum_font_size_pt", contract.get("minimum_font_size_pt")
        )
        accessibility = contract.get("accessibility", {})
        require_visual_alt_text = bool(
            slide_contract.get(
                "meaningful_visual_alt_text",
                accessibility.get("meaningful_visual_alt_text", False),
            )
        )
        allowed_distortion = {
            str(selector)
            for selector in slide_contract.get(
                "allow_image_distortion", contract.get("allow_image_distortion", [])
            )
        }
        aspect_ratio_tolerance = float(contract.get("image_aspect_ratio_tolerance", 0.02))
        for shape in shapes:
            name = str(shape["name"])
            if shape["width"] <= 0 or shape["height"] <= 0:
                result.append(
                    issue(
                        "NON_POSITIVE_GEOMETRY",
                        "error",
                        "shape has non-positive dimensions",
                        slide=number,
                        shape=name,
                    )
                )
            image = shape.get("image")
            if image and not (shape_identity(shape) & allowed_distortion):
                source_width, source_height = image.get("size", (0, 0))
                crop_width = (
                    1.0 - float(image.get("crop_left") or 0) - float(image.get("crop_right") or 0)
                )
                crop_height = (
                    1.0 - float(image.get("crop_top") or 0) - float(image.get("crop_bottom") or 0)
                )
                if source_width and source_height and crop_width > 0 and crop_height > 0:
                    source_ratio = (source_width * crop_width) / (source_height * crop_height)
                    target_ratio = shape["width"] / shape["height"]
                    relative_error = abs(target_ratio - source_ratio) / source_ratio
                    if relative_error > aspect_ratio_tolerance:
                        result.append(
                            issue(
                                "IMAGE_ASPECT_RATIO_RISK",
                                slide_contract.get("image_distortion_severity", "warning"),
                                "image geometry and crop do not preserve source aspect ratio",
                                slide=number,
                                shape=name,
                            )
                        )
            if require_visual_alt_text and (image or shape.get("chart")):
                authored_alt_text = shape.get("accessibility", {}).get("description")
                if image and authored_alt_text in {image.get("filename"), "Picture", "Image"}:
                    authored_alt_text = None
                decorative = shape.get("accessibility", {}).get("decorative") is True
                if not authored_alt_text and not decorative:
                    result.append(
                        issue(
                            "MISSING_ALT_TEXT",
                            "error",
                            "meaningful visual requires authored alt text or "
                            "decorative classification",
                            slide=number,
                            shape=name,
                        )
                    )
            if minimum_font_size is not None:
                for paragraph in shape.get("paragraphs", []):
                    for run in paragraph.get("runs", []):
                        font_size = run.get("font_size")
                        if font_size is not None and float(font_size) / 12700 < float(
                            minimum_font_size
                        ):
                            result.append(
                                issue(
                                    "FONT_TOO_SMALL",
                                    "error",
                                    f"explicit font size is below {minimum_font_size} pt",
                                    slide=number,
                                    shape=name,
                                )
                            )
                            break
            if (
                shape["left"] < 0
                or shape["top"] < 0
                or shape["left"] + shape["width"] > width
                or shape["top"] + shape["height"] > height
            ):
                result.append(
                    issue(
                        "SHAPE_OUT_OF_BOUNDS",
                        "error",
                        "shape extends beyond slide canvas",
                        slide=number,
                        shape=name,
                    )
                )
        exemptions = slide_contract.get("allow_overlaps", [])
        overlap_severity = slide_contract.get(
            "overlap_severity", contract.get("overlap_severity", "warning")
        )
        for left_index, left in enumerate(shapes):
            for right in shapes[left_index + 1 :]:
                if intersects(left, right) and not exempt_overlap(
                    left, right, exemptions, width, height
                ):
                    result.append(
                        issue(
                            "UNINTENDED_OVERLAP",
                            overlap_severity,
                            f"axis-aligned bounds overlap {right['name']!r}",
                            slide=number,
                            shape=str(left["name"]),
                        )
                    )
        for required in slide_contract.get("required_shapes", []):
            if find_shape(shapes, required) is None:
                result.append(
                    issue(
                        "REQUIRED_SHAPE_MISSING",
                        "error",
                        f"required shape {required!r} not found",
                        slide=number,
                    )
                )
        for group in slide_contract.get("alignment_groups", []):
            edge = group.get("edge", "left")
            selected = [find_shape(shapes, selector) for selector in group.get("shapes", [])]
            selected = [shape for shape in selected if shape is not None]
            if len(selected) > 1:
                values = {
                    "left": [shape["left"] for shape in selected],
                    "right": [shape["left"] + shape["width"] for shape in selected],
                    "top": [shape["top"] for shape in selected],
                    "bottom": [shape["top"] + shape["height"] for shape in selected],
                }.get(edge)
                if values is None:
                    result.append(
                        issue(
                            "INVALID_ALIGNMENT_EDGE",
                            "error",
                            f"unsupported edge {edge!r}",
                            slide=number,
                        )
                    )
                elif max(values) - min(values) > int(group.get("tolerance", 0)):
                    result.append(
                        issue(
                            "ALIGNMENT_DRIFT",
                            "error",
                            f"{edge} edges exceed tolerance",
                            slide=number,
                        )
                    )

    if contract.get("unique_titles", False) and len(titles) != len(set(titles)):
        result.append(issue("DUPLICATE_TITLE", "error", "slide titles must be unique"))

    package = report["package"]
    active_policy = contract.get("active_content", "report")
    active_present = bool(package["active_content"]["count"])
    if active_policy == "forbid" and active_present:
        result.append(
            issue(
                "ACTIVE_CONTENT_FORBIDDEN",
                "error",
                "presentation contains active or external content",
            )
        )
    preservation = contract.get("preservation", {})
    parts = available_parts if available_parts is not None else set(package["parts"]["items"])
    for required_part in preservation.get("required_parts", []):
        if required_part not in parts:
            result.append(
                issue(
                    "REQUIRED_PART_MISSING", "error", f"required part {required_part!r} is missing"
                )
            )
    expected_vba = preservation.get("vba_sha256")
    if expected_vba is not None and package["vba_sha256"] != expected_vba:
        result.append(
            issue("VBA_HASH_MISMATCH", "error", "VBA project hash does not match contract")
        )
    for name, expected_hash in preservation.get("opaque_hashes", {}).items():
        if package["opaque_hashes"].get(name) != expected_hash:
            result.append(
                issue("OPAQUE_PART_HASH_MISMATCH", "error", f"hash mismatch for {name!r}")
            )

    if contract.get("require_visual_text_fit", False):
        result.append(
            issue(
                "TEXT_FIT_UNVERIFIED", "warning", "package geometry cannot prove rendered text fit"
            )
        )
    return result


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("presentation", type=Path)
    result.add_argument("--contract", type=Path)
    result.add_argument("--details-limit", type=int, default=DEFAULT_DETAILS_LIMIT)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8")) if args.contract else {}
        if contract and contract.get("schema_version") != 1:
            raise ValueError("contract schema_version must be 1")
        presentation_path = args.presentation.resolve()
        report = inspect(presentation_path, limit=max(args.details_limit, 1_000_000))
        with zipfile.ZipFile(presentation_path) as archive:
            available_parts = {info.filename for info in archive.infolist() if not info.is_dir()}
        issues = validate(report, contract, available_parts=available_parts)
    except (OSError, ValueError, json.JSONDecodeError, ImportError) as exc:
        print(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "ok": False,
                    "status": "error",
                    "error": f"{type(exc).__name__}: {exc}",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    errors = sum(item["severity"] == "error" for item in issues)
    warnings = sum(item["severity"] == "warning" for item in issues)
    status = "failed" if errors else "passed_with_warnings" if warnings else "passed"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "ok": errors == 0,
        "status": status,
        "issues": issues,
        "summary": {"errors": errors, "warnings": warnings},
        "evidence": {
            "PACKAGE_VALIDATED": True,
            "SEMANTICS_VALIDATED": bool(contract) and errors == 0,
            "RENDERED": False,
            "VISUAL_QA_PASSED": False,
            "POWERPOINT_NATIVE_OPENED": False,
            "POWERPOINT_NATIVE_RENDERED": False,
            "ACCESSIBILITY_CHECKED": False,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
