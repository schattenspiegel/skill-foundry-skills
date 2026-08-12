# MCP configuration contracts

VS Code workspace MCP configuration is `.vscode/mcp.json`. The top level uses
`servers` and optional `inputs`; current schemas support local stdio and remote
HTTP-style servers with transport-specific fields. User configuration lives in
the VS Code profile. Inspect IntelliSense/current documentation for exact
fields. Server trust is re-evaluated after configuration changes.
