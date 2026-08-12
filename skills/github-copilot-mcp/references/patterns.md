# MCP patterns

## Pattern: remote read-only MCP
**Use when:** A reviewed remote server exposes required read-only tools and authentication must stay out of source control.
**Inspect first:** URL, publisher, TLS, OAuth/input support, tool inventory, data policy, and organization policy.
**Invariants:** No token in the repository; no implicit write authority; startup requires trust.
```json
{
  "servers": {
    "project-catalog": {
      "type": "http",
      "url": "https://mcp.example.invalid/read-only"
    }
  }
}
```
**Do not use when:** Static repository documentation supplies the needed context.
**Verify:** Validate JSON and domain policy offline; after explicit approval, inspect the trust dialog, advertised tools, logs, and one harmless read.
