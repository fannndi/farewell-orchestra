#!/usr/bin/env pwsh
# auto-compact.ps1 — Check context usage, trigger compaction hint if >80% with loop guard

$ErrorActionPreference = "Stop"

# Loop guard: track last compaction turn
$LastTurnFile = "$env:TEMP/opencode-compact-last-turn"
$CurrentTurn = $env:OPENCODE_TURN
if (-not $CurrentTurn -or $CurrentTurn -eq "") { $CurrentTurn = 0 }
$CurrentTurn = [int]$CurrentTurn

# Heuristic: estimate context % from turn count (~1000 tokens/turn, 128k limit)
if ($env:OPENCODE_CONTEXT_PCT) {
    $ContextPct = [int]$env:OPENCODE_CONTEXT_PCT
} else {
    # Fallback: assume ~1000 tokens per turn, 128k limit = ~128 turns = 100%
    # So: context% = (current_turn / 128) * 100
    $ContextPct = [math]::Floor($CurrentTurn * 100 / 128)
    if ($ContextPct -gt 100) { $ContextPct = 100 }
}

# Read last compaction turn
$LastTurn = 0
if (Test-Path $LastTurnFile) {
    $LastTurn = [int](Get-Content $LastTurnFile -Raw -ErrorAction SilentlyContinue)
    if (-not $LastTurn) { $LastTurn = 0 }
}

$TurnDiff = $CurrentTurn - $LastTurn

Write-Host "Context: ~${ContextPct}% (turn $CurrentTurn, last compact at turn $LastTurn)"

if ($ContextPct -gt 80 -and $TurnDiff -gt 5) {
    Write-Host "⚠️  Context >80%. Run `/compact` manually or wait for auto-compaction (enabled in config)."
    Set-Content $LastTurnFile -Value $CurrentTurn
    exit 0
} elseif ($ContextPct -gt 80 -and $TurnDiff -le 5) {
    Write-Host "⏳ Context >80% but compacted recently (turn $LastTurn). Waiting..."
    exit 0
} else {
    Write-Host "✅ Context healthy (<80%)."
    exit 0
}