# Verification matrix

| Claim | Minimum evidence |
|---|---|
| Script is syntactically valid | Parser returns no errors in the declared runtime. |
| Script follows repository analysis policy | Pinned PSScriptAnalyzer run with explicit settings and reviewed findings. |
| Parameters and pipeline are correct | Pester tests for binding, zero/one/many inputs, object shape, and failure. |
| Mutation is previewable | Pester proves `-WhatIf` leaves the fixture unchanged and normal mode changes only the bounded target. |
| Native invocation is correct | Executable fixture proves argv boundaries, output, and accepted/rejected exit codes. |
| PowerShell 7 cross-platform | Same behavioral suite passes on every claimed OS. |
| Windows PowerShell 5.1 compatible | Same relevant suite passes under `powershell.exe` 5.1 on Windows. |
| Live operation succeeded | Attended execution plus provider-specific readback; code tests alone are insufficient. |

Parser, analyzer, Pester, platform, and live-operation results are separate evidence
states. Report the exact runtime and module versions with each result.
