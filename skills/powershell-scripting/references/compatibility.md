# Compatibility decisions

Treat runtime edition, version, OS, architecture, and external command/module
availability as separate dimensions.

## Decision sequence

1. Read `#requires`, manifests, CI matrices, repository documentation, and existing
   tests.
2. Inspect `$PSVersionTable` and required commands/modules in the actual lane.
3. Preserve the repository's declared floor. Do not silently raise or lower it.
4. Isolate platform-specific behavior behind an explicit guard and test the failure
   path on unsupported platforms.
5. Run PSScriptAnalyzer compatibility rules when configured, then execute every
   claimed lane. Static compatibility output never substitutes for runtime tests.

PowerShell 7 `Core` edition does not itself imply macOS/Linux portability. Windows
PowerShell 5.1 uses a different runtime and must be tested independently on Windows.
If the matrix is unknown, avoid new version-specific syntax and report the unresolved
decision.
