# Verification

Parse config JSON; resolve commands and working directories; compile handlers;
run them with fixture stdin; parse stdout; assert exits and no command injection;
simulate irrelevant events; test timeout; scan for secrets. Enabling the hook
or executing real tool calls requires separate authority.
