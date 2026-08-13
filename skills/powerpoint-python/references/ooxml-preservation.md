# OOXML preservation

Inspect `[Content_Types].xml`, package relationships, `docProps/`, `customXml/`,
and relevant `ppt/` presentation, master, layout, slide, theme, notes, chart,
embedding, media, comment, people, tag, diagram, timing, transition, and VBA
parts. Record relationship type, target, target mode, and opaque hashes.

Classify each part as supported mutation, preserve-and-verify, unknown, or
runtime-required. Unknown or unsupported content plus an exact-preservation
requirement blocks a blind python-pptx round-trip.

For `.pptm`, verify macro-enabled content type, `ppt/vbaProject.bin`, extension,
relationships, and before/after hash. Never execute VBA. Compare semantic
inventories rather than raw ZIP bytes; part ordering and serialization can vary.
