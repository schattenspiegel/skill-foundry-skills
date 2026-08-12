# Hook contracts

Each config has a top-level `hooks` object mapping supported event names to
command arrays. Each command declares `type: command`, `command`, and optional
`cwd`, `env`, `timeout`, or platform overrides. Common input includes
`hook_event_name`; event-specific input supplies fields such as `tool_name` and
`tool_input`. Exit 0 is success, exit 2 can block, and other exits can warn;
verify exact semantics in the current host.
