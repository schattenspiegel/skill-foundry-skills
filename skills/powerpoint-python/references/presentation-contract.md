# Presentation contract

Resolve audience, objective, key decision/takeaway, delivery context, sources,
template/version, dimensions, theme/font expectations, slide sequence and roles,
editability, notes, accessibility, preservation, rendering, and evidence before
rendering.

Each slide needs a stable semantic ID, role, layout identity, assertion/title,
required and optional elements, sources, notes, and validation rules. Use frozen
typed models such as `DeckSpec`, `SlideSpec`, and `ElementSpec`; exact class names
are project choices.

The renderer receives resolved labels, values, ordering, units, and asset paths.
It must not calculate business metrics or decide narrative structure while
mutating shapes. Keep provenance in custom properties, a metadata slide/notes,
or sidecar JSON according to the sensitivity contract.
