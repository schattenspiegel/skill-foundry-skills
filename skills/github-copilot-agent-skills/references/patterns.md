# Skill patterns

## Pattern: bounded skill
**Use when:** A repeated multi-step task benefits from automatic discovery and a reusable reference.
**Inspect first:** Real prompts, target hosts, installed neighbors, and objective verification.
**Invariants:** One job; precise router; direct resources; no authoring leakage.
```markdown
---
name: api-contract-review
description: Use for reviewing API contract changes against repository compatibility rules. Do not use for general code review or API implementation.
argument-hint: "[changed contract or path]"
---
# API contract review
1. Inspect the current and proposed contract.
2. Classify compatible, conditionally compatible, or breaking changes.
3. Apply the bundled compatibility rules.
4. Report evidence and the narrow verification command.
```
**Do not use when:** One short prompt can state the entire stable task.
**Verify:** Validate structure, resolve the reference, test explicit/implicit/negative cases, and inspect slash discovery.
