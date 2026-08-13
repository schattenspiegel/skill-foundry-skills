# Evaluated PowerShell recipes

## Recipe `powershell.safe-literal-removal`
**Use when:** deleting known files beneath one approved root with `-WhatIf` support.
**Inspect first:** runtime floor, approved root, path ownership, and symlink policy.
**Invariants:** literal paths only; roots and escapes rejected; every deletion gated.
```powershell
[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
param(
    [Parameter(Mandatory, ValueFromPipeline)]
    [string] $Path,
    [Parameter(Mandatory)]
    [string] $ApprovedRoot
)
process {
    $root = [IO.Path]::GetFullPath($ApprovedRoot)
    $target = [IO.Path]::GetFullPath($Path)
    $prefix = $root.TrimEnd([IO.Path]::DirectorySeparatorChar) +
        [IO.Path]::DirectorySeparatorChar
    if ($target -eq $root -or -not $target.StartsWith($prefix, [StringComparison]::Ordinal)) {
        throw "Target is outside the approved root: $target"
    }
    if ($PSCmdlet.ShouldProcess($target, 'Remove file')) {
        Remove-Item -LiteralPath $target -ErrorAction Stop
    }
}
```
**Do not use when:** recursive directory deletion or symlink traversal is allowed.
**Verify:** test a name containing `[` and `]`, an escape, the root, `-WhatIf`, and deletion.

## Recipe `powershell.pipeline-object-transform`
**Use when:** converting each pipeline input into one stable result object.
**Inspect first:** input binding, output schema, ordering, and empty-input behavior.
**Invariants:** one object per item; no presentation objects or status text on success.
```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory, ValueFromPipeline)]
    [ValidateNotNullOrEmpty()]
    [string] $Name
)
process {
    [pscustomobject]@{
        Name       = $Name
        Normalized = $Name.Trim().ToUpperInvariant()
    }
}
```
**Do not use when:** all inputs must be aggregated before producing a result.
**Verify:** pipe zero, one, and several values; assert cardinality, order, and properties.

## Recipe `powershell.native-argv-exit`
**Use when:** a native executable consumes caller-controlled values as separate argv items.
**Inspect first:** executable path, argument protocol, accepted exit codes, and encoding.
**Invariants:** no evaluation or joined command string; exit status checked immediately.
```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string] $Executable,
    [Parameter(Mandatory)] [string] $Payload
)
$output = & $Executable '--payload' $Payload
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "Native command failed with exit code $exitCode"
}
$output
```
**Do not use when:** stdin is the required secret or data protocol.
**Verify:** use a fixture executable to assert spaces/metacharacters remain one argument and nonzero fails.

## Recipe `powershell.dual-runtime-guard`
**Use when:** a declared script supports PowerShell 7 and Windows PowerShell 5.1 but one branch is platform-specific.
**Inspect first:** `PSEdition`, version, platform, command availability, and CI lanes.
**Invariants:** unsupported combinations fail before side effects; each supported lane is executed.
```powershell
$isDesktop = $PSVersionTable.PSEdition -eq 'Desktop'
$isCore = $PSVersionTable.PSEdition -eq 'Core'
if (-not ($isDesktop -or $isCore)) {
    throw "Unsupported PowerShell edition: $($PSVersionTable.PSEdition)"
}
if ($isDesktop -and $PSVersionTable.PSVersion -lt [version]'5.1') {
    throw 'Windows PowerShell 5.1 or newer is required.'
}
```
**Do not use when:** repository policy supports PowerShell 7 only.
**Verify:** parse and run the relevant suite in `pwsh` and Windows `powershell.exe`; test the unsupported guard.

## Recipe `powershell.parse-without-execution`
**Use when:** syntax and AST evidence is required without running an untrusted script.
**Inspect first:** declared runtime, literal file path, and required output evidence.
**Invariants:** parse only; never dot-source or invoke the target; report every parse error.
```powershell
[CmdletBinding()]
param([Parameter(Mandatory)] [string] $Path)

$resolved = (Resolve-Path -LiteralPath $Path -ErrorAction Stop).ProviderPath
$tokens = $null
$errors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile(
    $resolved,
    [ref] $tokens,
    [ref] $errors
)
if ($errors.Count) {
    $details = ($errors | ForEach-Object {
        "$($_.Extent.StartLineNumber):$($_.Extent.StartColumnNumber) $($_.Message)"
    }) -join [Environment]::NewLine
    throw "PowerShell parsing failed:$([Environment]::NewLine)$details"
}
[pscustomobject]@{
    Path           = $resolved
    StatementCount = @($ast.EndBlock.Statements).Count
    ErrorCount     = 0
}
```
**Do not use when:** behavioral, dependency, or platform compatibility must be proven.
**Verify:** parse valid, invalid, and side-effect-bearing scripts; prove no side effect ran.

## Recipe `powershell.pester-ci-gate`
**Use when:** CI must run a repository suite with an exact supported Pester version.
**Inspect first:** Pester major/version policy, test paths, result format, and CI host.
**Invariants:** exact module import; explicit configuration; any failed test fails the gate.
```powershell
[CmdletBinding()]
param(
    [string[]] $TestsPath = @('./tests'),
    [version] $RequiredVersion = '6.1.0'
)

Import-Module Pester -RequiredVersion $RequiredVersion -ErrorAction Stop
$config = New-PesterConfiguration
$config.Run.Path = $TestsPath
$config.Run.PassThru = $true
$config.Run.Throw = $false
$config.Output.Verbosity = 'Detailed'
$config.Output.RenderMode = 'Plaintext'
$result = Invoke-Pester -Configuration $config
if ($result.FailedCount -gt 0) {
    throw "Pester failed: $($result.FailedCount) failed, $($result.PassedCount) passed."
}
[pscustomobject]@{
    Passed   = $result.PassedCount
    Failed   = $result.FailedCount
    Skipped  = $result.SkippedCount
    Duration = $result.Duration
}
```
**Do not use when:** the repository targets another Pester major or owns a different runner.
**Verify:** run one passing and one failing suite; assert the process result and summary.

## Recipe `powershell.validated-json-ingestion`
**Use when:** a PowerShell 7.4+ script must ingest JSON governed by a JSON Schema.
**Inspect first:** runtime floor, schema draft, top-level shape, key semantics, and depth.
**Invariants:** validate before conversion; literal input path; preserve array enumeration shape.
```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string] $Path,
    [Parameter(Mandatory)] [string] $SchemaPath
)

$resolved = (Resolve-Path -LiteralPath $Path -ErrorAction Stop).ProviderPath
$schema = (Resolve-Path -LiteralPath $SchemaPath -ErrorAction Stop).ProviderPath
if (-not (Test-Json -LiteralPath $resolved -SchemaFile $schema -ErrorAction Stop)) {
    throw "JSON does not satisfy the required schema: $resolved"
}
$json = Get-Content -LiteralPath $resolved -Raw -ErrorAction Stop
ConvertFrom-Json -InputObject $json -AsHashtable -NoEnumerate
```
**Do not use when:** PowerShell below 7.4 or a non-JSON-Schema contract must be supported.
**Verify:** test valid JSON, invalid syntax, schema failure, bracketed paths, and top-level arrays.

## Recipe `powershell.bounded-rest-request`
**Use when:** a PowerShell 7.4+ script performs an idempotent JSON GET with bounded retry.
**Inspect first:** API contract, authentication boundary, retryable statuses, and time budget.
**Invariants:** HTTPS unless a disposable local fixture; finite timeouts/retries; expose status.
```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory)] [uri] $Uri,
    [ValidateRange(0, 10)] [int] $MaximumRetryCount = 3,
    [ValidateRange(1, 300)] [int] $ConnectionTimeoutSeconds = 10,
    [ValidateRange(1, 900)] [int] $OperationTimeoutSeconds = 30
)

if ($Uri.Scheme -ne 'https' -and -not $Uri.IsLoopback) {
    throw "HTTPS is required for non-loopback requests: $Uri"
}
$body = Invoke-RestMethod -Uri $Uri -Method Get `
    -ConnectionTimeoutSeconds $ConnectionTimeoutSeconds `
    -OperationTimeoutSeconds $OperationTimeoutSeconds `
    -MaximumRetryCount $MaximumRetryCount -RetryIntervalSec 1 `
    -StatusCodeVariable statusCode -ErrorAction Stop
[pscustomobject]@{ StatusCode = $statusCode; Body = $body }
```
**Do not use when:** the request mutates state or retry safety is not established.
**Verify:** use a local server for success, transient failure then success, terminal failure, and timeout.

## Recipe `powershell.checksum-verified-download`
**Use when:** a file must be downloaded, SHA-256 verified, then published once.
**Inspect first:** destination ownership, overwrite policy, expected digest provenance, and URI.
**Invariants:** no overwrite; stage beside destination; verify before move; clean every failure.
```powershell
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)] [uri] $Uri,
    [Parameter(Mandatory)] [string] $Destination,
    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Fa-f0-9]{64}$')] [string] $ExpectedSha256
)

$target = [IO.Path]::GetFullPath($Destination)
$parent = [IO.Path]::GetDirectoryName($target)
if (-not [IO.Directory]::Exists($parent)) { throw "Missing destination directory: $parent" }
if ([IO.File]::Exists($target)) { throw "Destination already exists: $target" }
$temp = Join-Path $parent ".$([guid]::NewGuid().ToString('N')).download"
if ($PSCmdlet.ShouldProcess($target, 'Download, verify SHA-256, and publish')) {
    try {
        Invoke-WebRequest -Uri $Uri -OutFile $temp -ErrorAction Stop
        $actual = (Get-FileHash -LiteralPath $temp -Algorithm SHA256).Hash
        if (-not $actual.Equals($ExpectedSha256, [StringComparison]::OrdinalIgnoreCase)) {
            throw "SHA-256 mismatch: expected $ExpectedSha256; received $actual"
        }
        Move-Item -LiteralPath $temp -Destination $target -ErrorAction Stop
        Get-Item -LiteralPath $target
    } finally {
        if ([IO.File]::Exists($temp)) { [IO.File]::Delete($temp) }
    }
}
```
**Do not use when:** authenticity requires a signature or the destination may be overwritten.
**Verify:** test success, mismatch, existing destination, `-WhatIf`, and temporary-file cleanup.

## Recipe `powershell.bounded-parallel-file-hash`
**Use when:** many local files need SHA-256 and each hash dominates runspace overhead.
**Inspect first:** PowerShell 7 target, input bound, ordering, timeout, and concurrency budget.
**Invariants:** bounded input and throttle; literal resolved files; output restored to input order.
```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory, ValueFromPipeline)] [string[]] $Path,
    [ValidateRange(1, 32)] [int] $ThrottleLimit = 4,
    [ValidateRange(1, 3600)] [int] $TimeoutSeconds = 120,
    [ValidateRange(1, 100000)] [int] $MaxItems = 1000
)
begin { $paths = [Collections.Generic.List[string]]::new() }
process {
    foreach ($item in $Path) {
        if ($paths.Count -ge $MaxItems) { throw "Input exceeds MaxItems=$MaxItems" }
        $paths.Add((Resolve-Path -LiteralPath $item -ErrorAction Stop).ProviderPath)
    }
}
end {
    $indexed = for ($index = 0; $index -lt $paths.Count; $index++) {
        [pscustomobject]@{ Index = $index; Path = $paths[$index] }
    }
    $results = @($indexed | ForEach-Object -Parallel {
        $hash = Get-FileHash -LiteralPath $_.Path -Algorithm SHA256 -ErrorAction Stop
        [pscustomobject]@{ Index = $_.Index; Path = $_.Path; Hash = $hash.Hash }
    } -ThrottleLimit $ThrottleLimit -TimeoutSeconds $TimeoutSeconds)
    if ($results.Count -ne $paths.Count) { throw 'Parallel hashing produced incomplete output.' }
    $results | Sort-Object Index | Select-Object Path, Hash
}
```
**Do not use when:** work is cheap, input is unbounded, or Windows PowerShell 5.1 is required.
**Verify:** test input order, bracketed paths, digest values, MaxItems, timeout, and missing files.
