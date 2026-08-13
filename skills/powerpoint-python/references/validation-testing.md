# Validation and testing

Use independent falsifiers: reopen, ZIP/XML parsing, expected slide count/order,
layout identity, title sequence, shape containment, overlap policy, media/VBA
hash reconciliation, notes presence, semantic diff, rendering, or manual/vision
review. Execution without exception is not validation.

Contract validation returns stable issue codes, slide/shape identity, severity,
and evidence. Distinguish errors from warnings where deterministic inspection
cannot decide intent. Text fit, font substitution, animations, media playback,
and accessibility checker results need rendering or native runtime evidence.

Test empty/long text, duplicate layout names, unusual placeholder indices,
wrong aspect ratio, portrait-in-wide image, missing fonts/assets, native/static
chart choices, tables near readability limits, notes, external actions, macros,
SmartArt/timing, off-slide shapes, intentional overlaps, and malformed packages.
