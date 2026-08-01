<#
.SYNOPSIS
    Hook dispatcher - Zero-inspired event-driven hook system
.DESCRIPTION
    Reads hooks.jsonc, filters by event, executes matching hooks.
    Architecture: stdin JSON payload, exit 0=continue, non-zero=block.
.PARAMETER Event
    Event name to dispatch: beforeGenerate, afterGenerate, beforeCommit, sessionStart, sessionEnd
.PARAMETER Payload
    Optional JSON string passed via stdin to each hook command
.PARAMETER TimeoutSeconds
    Per-hook timeout in seconds (default 30)
.EXAMPLE
    .\dispatch.ps1 -Event "beforeGenerate"
    .\dispatch.ps1 -Event "afterGenerate" -Payload '{"status":"ok","profile":"default-oc"}'
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$Event,
    [string]$Payload = "{}",
    [int]$TimeoutSeconds = 30
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HooksFile = Join-Path $ScriptDir "hooks.jsonc"

# Graceful fallback jika hooks.jsonc tidak ada
if (-not (Test-Path -LiteralPath $HooksFile)) {
    Write-Host "[DISPATCH] hooks.jsonc not found, skipping" -ForegroundColor Yellow
    exit 0
}

# Parse hooks.jsonc
try {
    $raw = Get-Content -LiteralPath $HooksFile -Raw -Encoding utf8
    # Strip JSONC comments (single-line only)
    $clean = $raw -replace '//.*', ''
    $config = $clean | ConvertFrom-Json
} catch {
    Write-Host "[DISPATCH] Failed to parse hooks.jsonc: $_" -ForegroundColor Yellow
    exit 0  # graceful fallback - jangan block
}

if (-not $config.enabled) {
    Write-Host "[DISPATCH] Hooks disabled" -ForegroundColor Yellow
    exit 0
}

$hooks = $config.hooks | Where-Object { $_.enabled -eq $true -and $_.event -eq $Event }

if (-not $hooks) {
    Write-Host "[DISPATCH] No hooks for event '$Event'" -ForegroundColor Gray
    exit 0
}

$blocked = $false
$blockedBy = ""

foreach ($hook in $hooks) {
    $hookId = $hook.id
    $command = $hook.command
    $args = @($hook.args)

    Write-Host "[DISPATCH] Running hook '$hookId' ($Event)..." -ForegroundColor Cyan

    # Build stdin payload as JSON
    $stdinPayload = @{
        event = $Event
        hookId = $hookId
        payload = ($Payload | ConvertFrom-Json -ErrorAction SilentlyContinue)
        timestamp = (Get-Date -Format "o")
    } | ConvertTo-Json -Compress

    try {
        # Execute with timeout
        $psi = New-object System.Diagnostics.ProcessStartInfo
        $psi.FileName = $command
        $psi.Arguments = ($args -join ' ')
        $psi.UseShellExecute = $false
        $psi.RedirectStandardInput = $true
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.CreateNoWindow = $true
        $ProjectRoot = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
        $psi.WorkingDirectory = $ProjectRoot

        $proc = New-Object System.Diagnostics.Process
        $proc.StartInfo = $psi
        $proc.Start() | Out-Null

        # Write payload to stdin
        $proc.StandardInput.Write($stdinPayload)
        $proc.StandardInput.Close()

        # Wait with timeout
        $completed = $proc.WaitForExit($TimeoutSeconds * 1000)
        if (-not $completed) {
            $proc.Kill()
            Write-Host "[DISPATCH] Hook '$hookId' TIMEOUT after ${TimeoutSeconds}s" -ForegroundColor Red
            # Blocking event? Check if event is beforeGenerate/beforeCommit
            if ($Event -in @("beforeGenerate", "beforeCommit")) {
                $blocked = $true
                $blockedBy = $hookId
                Write-Host "[DISPATCH] BLOCKED by '$hookId' (timeout)" -ForegroundColor Red
            }
            continue
        }

        $stdout = $proc.StandardOutput.ReadToEnd()
        $stderr = $proc.StandardError.ReadToEnd()
        $exitCode = $proc.ExitCode

        if ($exitCode -eq 0) {
            Write-Host "[DISPATCH] Hook '$hookId' OK" -ForegroundColor Green
            if ($stdout.Trim()) { Write-Host "  $($stdout.Trim())" -ForegroundColor Gray }
        } else {
            Write-Host "[DISPATCH] Hook '$hookId' FAILED (exit $exitCode)" -ForegroundColor Red
            if ($stderr.Trim()) { Write-Host "  $($stderr.Trim())" -ForegroundColor Red }
            if ($stdout.Trim()) { Write-Host "  $($stdout.Trim())" -ForegroundColor Gray }

            # Blocking events: beforeGenerate, beforeCommit
            if ($Event -in @("beforeGenerate", "beforeCommit")) {
                $blocked = $true
                $blockedBy = $hookId
                Write-Host "[DISPATCH] BLOCKED by '$hookId'" -ForegroundColor Red
                break
            }
        }
    } catch {
        Write-Host "[DISPATCH] Hook '$hookId' error: $_" -ForegroundColor Yellow
    }
}

if ($blocked) {
    Write-Host "[DISPATCH] BLOCKED by $blockedBy - stopping" -ForegroundColor Red
    exit 1
}

Write-Host "[DISPATCH] All hooks completed for event '$Event'" -ForegroundColor Green
exit 0