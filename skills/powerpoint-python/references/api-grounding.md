# API grounding

Run `python scripts/inspect_powerpoint_env.py` in the task environment before
using a version-sensitive method, keyword, enum, private XML surface, notes API,
chart-data operation, text fitting behavior, or package content type.

Prefer the installed object's public signature and official documentation for
that version. If examples, current docs, and installed behavior disagree,
target the installed environment and record the compatibility branch. Private
attributes and `_element` access require a narrow tested helper plus package
regression fixtures.

The evaluated baseline is python-pptx 1.0.2, but the runtime contract is not a
promise that every 1.x package has the same API or preservation behavior.
