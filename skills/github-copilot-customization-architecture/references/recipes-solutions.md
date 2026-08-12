# Architecture recipes

## Recipe `copilot.customization-map`
**Use when:** A repository has several overlapping customization needs.
**Inspect first:** Existing artifacts, parent discovery, VS Code/Copilot version, policies, and trust constraints.
**Invariants:** One owner per rule; smallest activation scope; executable trust is explicit.
```python
customizations = [
    {"need": "coding rules", "activation": "automatic", "artifact": "instructions"},
    {"need": "prepare PR", "activation": "manual", "artifact": "prompt"},
    {"need": "security gate", "activation": "PreToolUse", "artifact": "hook"},
    {"need": "issue data", "activation": "tool call", "artifact": "mcp"},
]
assert all({"need", "activation", "artifact"} <= item.keys() for item in customizations)
```
**Do not use when:** One already-selected artifact is the entire task.
**Verify:** Parse every file, resolve references, audit collisions/tools, and record one positive and negative discovery smoke.
