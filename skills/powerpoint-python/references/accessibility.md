# Accessibility

When accessibility is contractual, require a unique meaningful slide title,
logical object order, meaningful visual alt text, decorative classification,
understandable standalone link labels, simple table structure, sufficient
contrast, and non-color-only encoding.

Prefer template placeholders and add objects in intended reading order. Visual
position is not reading order. python-pptx does not expose every accessibility
property; use a narrowly tested OOXML helper only for a known schema property,
otherwise escalate to PowerPoint runtime.

Report deterministic warnings and manual review separately. Never emit
`ACCESSIBILITY_CHECKED` or `ACCESSIBILITY_CHECKER_PASSED` unless Microsoft
PowerPoint's checker actually ran.
