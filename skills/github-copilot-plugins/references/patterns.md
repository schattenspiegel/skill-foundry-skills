# Plugin patterns

## Pattern: portable plugin
**Use when:** Several portable skills and MCP tools share one product, version, and trust decision.
**Inspect first:** Agent Plugins version, component licenses, server provenance, and consumer support.
**Invariants:** Canonical schema; portable components only; no secrets; all files declared by discovery rules.
```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "example-dev-tools",
  "description": "Reviewed development workflows and tools",
  "version": "1.0.0",
  "license": "MIT"
}
```
**Do not use when:** One standalone skill is sufficient or client-specific hooks are essential.
**Verify:** Validate schema, component trees and licenses; install only after review; test discovery, disable, and uninstall.
