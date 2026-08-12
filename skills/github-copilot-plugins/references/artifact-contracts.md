# Plugin contracts

Agent Plugins 1.0 uses root `plugin.json` with
`$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`, required
`name`, and optional version/description/author/homepage/repository/license/
keywords/extensions. Skills are discovered under `skills/`; MCP definitions
under `mcp.json`. Current VS Code ignores client extension namespaces.

Legacy Copilot, Claude, and OpenPlugin formats have different manifests,
component locations, and root tokens. Inspect the active schema; never mix
fields from multiple formats by intuition.
