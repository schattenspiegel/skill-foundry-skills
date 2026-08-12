# Artifact and scope contracts

| Artifact | Workspace path | User path | Primary risk |
|---|---|---|---|
| Instructions | `.github/copilot-instructions.md`, `.github/instructions/` | VS Code profile | Context pollution/conflict |
| Prompt | `.github/prompts/*.prompt.md` | VS Code profile | Excess tools or stale context |
| Skill | `.github/skills/`, `.agents/skills/` | `~/.copilot/skills/` | Trigger collisions |
| Agent | `.github/agents/*.agent.md` | `~/.copilot/agents/` | Excess capability |
| Hook | `.github/hooks/*.json` | `~/.copilot/hooks/` | Arbitrary command execution |
| MCP | `.vscode/mcp.json` | VS Code profile | External code/data/secrets |
| Plugin | `plugin.json` package | Installed plugin store | Bundled executable trust |

Paths and fields drift. Inspect the Agent Customizations editor, JSON/YAML
validation, and current documentation in the active host.
