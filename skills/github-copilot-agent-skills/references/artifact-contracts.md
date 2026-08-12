# Agent Skill contract

`SKILL.md` begins with YAML frontmatter. `name` is lowercase kebab-case, at most
64 characters, and matches the directory; `description` is non-empty and at
most 1024 characters. Optional resources must be referenced by relative links.
Project locations include `.github/skills`, `.agents/skills`, and
`.claude/skills`; user locations include `~/.copilot/skills` and
`~/.agents/skills`. Host settings can add locations or parent discovery.
