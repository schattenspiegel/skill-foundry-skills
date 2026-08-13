# Images

Each image contract states semantic role, source/provenance, source pixels,
target rectangle, crop mode, resolution/interpolation policy, alt text, and
decorative status.

Use one canonical helper for `contain`/`fit` (whole image, possible letterbox)
and `cover`/`fill` (crop to fill), preserving aspect ratio. Supplying only width
or height to `add_picture()` preserves aspect ratio; supplying arbitrary values
for both can distort the display. Validate missing assets, invalid crop ranges,
unexpected transparency, and excessive raster enlargement.

For critical composites, prepare a deterministic final image outside PowerPoint
and insert it as one predictable asset.
