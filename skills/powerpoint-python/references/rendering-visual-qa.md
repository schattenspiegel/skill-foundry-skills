# Rendering and visual QA

python-pptx produces packages, not pixels. Record renderer name/version and
render every slide when appearance is part of delivery. LibreOffice, cloud
renderers, and PowerPoint are different evidence sources; only actual
PowerPoint output establishes `POWERPOINT_NATIVE_RENDERED`.

Inspect clipping, overflow, minimum font size, unintended overlap, canvas
bounds, image distortion, alignment, margins, wrapping, orphan labels, chart
collisions, legends, hierarchy, footnotes/footers, title position, substitution,
and unexpected blank space.

For regression, compare baseline and new slide images with pixel/perceptual
diagnostics, changed-pixel bounds, heatmaps, and an expected-change allowlist.
Pixel equality is neither semantic equivalence nor proof of correctness.
