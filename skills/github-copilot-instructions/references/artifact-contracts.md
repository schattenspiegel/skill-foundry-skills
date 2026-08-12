# Instruction contracts

Repository-wide instructions have no frontmatter and live at
`.github/copilot-instructions.md`. File instructions end in `.instructions.md`
and require YAML frontmatter with an `applyTo` glob string. Current hosts may
also use task descriptions and user-profile instruction locations; inspect the
active schema before depending on them.

Prefer `.github/instructions/python.instructions.md` with `applyTo: "**/*.py"`
over placing Python-only policy in the repository-wide file. Multiple comma-
separated patterns are allowed, but separate files are clearer when policies
or owners differ.
