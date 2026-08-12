# Hook patterns

## Pattern: PreToolUse Python policy
**Use when:** One tool call must be deterministically allowed, denied, or escalated from structured fields.
**Inspect first:** Current `PreToolUse` schema, exact tool name, and desired failure policy.
**Invariants:** No shell evaluation; unrelated tools pass; malformed input fails safely.
```python
from __future__ import annotations
import json
import sys


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeError):
        print("invalid hook input", file=sys.stderr)
        return 2
    if event.get("hook_event_name") != "PreToolUse":
        print(json.dumps({"continue": True}))
        return 0
    tool = event.get("tool_name")
    if tool == "execute/runInTerminal":
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "permissionDecision": "ask",
                        "permissionDecisionReason": "Terminal use requires review",
                    }
                }
            )
        )
        return 0
    print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
**Do not use when:** Prose guidance is sufficient or the exact tool cannot be identified.
**Verify:** Pipe synthetic JSON for unrelated, terminal, malformed, and missing-field cases; assert exit status and parsed stdout.
