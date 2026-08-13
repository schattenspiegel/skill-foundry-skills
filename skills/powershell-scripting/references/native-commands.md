# Native command boundaries

Before invoking a native program, define executable discovery, argv values, working
directory, environment inheritance, stdin/stdout encoding, accepted exit codes,
timeout/cancellation, and cleanup.

- Resolve a required executable deliberately; do not depend on an interactive shell
  profile.
- Keep each argument as one PowerShell value and invoke with the call operator. Do not
  join values into a command line or evaluate a source string.
- Capture output only when the contract needs it. Preserve text versus bytes and do
  not merge stderr into result data accidentally.
- Save and inspect the native exit code immediately after invocation. A lack of a
  PowerShell exception is not native success.
- Use `Start-Process` only when its process object, redirection, credentials, window,
  or lifecycle behavior is required; it is not the default solution for argv safety.
- For complex cross-platform process control, verify the installed PowerShell
  semantics and test paths, spaces, quotes, empty arguments, Unicode, stderr, nonzero
  exit, and timeout behavior in each target lane.
