# Agent patterns

## Pattern: read-only planner
**Use when:** Planning must be repeatable and must not mutate the workspace.
**Inspect first:** Exact read/search tool names and the implementation handoff target.
**Invariants:** No edit/terminal tools; plan cites repository evidence; handoff is user-confirmed.
```markdown
---
name: Read-only planner
description: Produce a repository-grounded implementation plan without edits
tools: [search/codebase, search/usages]
user-invocable: true
disable-model-invocation: true
handoffs:
  - label: Review implementation handoff
    agent: agent
    prompt: Implement the approved plan above.
    send: false
---
Inspect before planning. Do not edit or execute commands. State files, contracts,
tests, risks, and unresolved decisions.
```
**Do not use when:** The task is a one-off planning prompt.
**Verify:** Parse the agent, resolve tools/target, invoke it, and assert no file changes.
