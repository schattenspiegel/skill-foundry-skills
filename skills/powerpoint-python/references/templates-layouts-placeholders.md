# Templates, layouts, and placeholders

Open the approved template with `Presentation(template_path)`. Do not use the
bundled default for professional output unless a generic blank deck is explicit.

Run `inspect_template.py` and bind semantic layout roles to discovered layout
name plus master and placeholder contract. Verify duplicate names rather than
choosing the first. For every required placeholder record `idx`, type, geometry,
and supported insertion method. Resolve `slide.placeholders[idx]` only after the
contract establishes that stable index.

Prefer placeholder insertion because geometry, typography, bullets, alignment,
theme, and accessibility order inherit from the template. Never blindly use
`prs.slide_layouts[n]` or `slide.placeholders[n]`. If a required semantic layout
has no unique match, stop and request a template decision.
