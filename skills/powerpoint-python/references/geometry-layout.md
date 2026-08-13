# Geometry and layout

Use EMUs internally and derive the canvas from `prs.slide_width` and
`prs.slide_height`. Centralize immutable `Point`, `Size`, `Rect`, `Margins`,
`Grid`, and `Gap` values with `inset`, split, align, distribute, `contains`, and
`intersects` operations.

Validate positive dimensions, slide containment, repeated margins/alignment,
title/body/footer separation, and intentional versus accidental overlap. Store
overlap exemptions by stable slide/shape identity. Axis-aligned boxes are a
conservative approximation for rotated, grouped, connector, shadow, and mask
geometry; report that limitation rather than claiming a pixel proof.

Object order affects both z-order and reading order. Add backgrounds and
decorations deliberately, then content in logical reading order; verify visual
layering separately.
