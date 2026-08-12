# Verification

- Parse YAML frontmatter and JSON; reject unknown assumed fields.
- Resolve relative references, target agents, tools, scripts, and plugin components.
- Test automatic, manual, and negative activation separately.
- Execute hook helpers only with synthetic stdin in an isolated test directory.
- Never start MCP servers or enable plugins merely to validate configuration.
- Record VS Code, Copilot extension, settings, preview flags, model, and Agent Debug Log evidence.
