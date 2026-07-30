<#
.SYNOPSIS
  Stress Test - verify dispatch configuration consistency.
.DESCRIPTION
  Cross-checks all agent config files for consistency.
  Tests: step budgets, models, permissions, prompts, cross-file refs.
  Output: PASS/FAIL per test.
#>

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$passed = 0; $failed = 0; $warnings = 0
$P = "[PASS]"; $F = "[FAIL]"; $W = "[WARN]"

Write-Host "`n=== STRESS TEST - Dispatch Configuration ===" -ForegroundColor Cyan
Write-Host ""

# Read files
$rawJsonc = Get-Content "$root\opencode.jsonc" -Raw
$orchMd = Get-Content "$root\.opencode\agents\orchestrator.md" -Raw
$agentsMd = Get-Content "$root\AGENTS.md" -Raw
$skillMd = Get-Content "$root\.opencode\skills\orchestrate\SKILL.md" -Raw

# Parse JSON: strip comment header, convert to object
$jsonBody = $rawJsonc
if ($jsonBody -match '^\s*//.*?\n') { $jsonBody = $jsonBody -replace '^\s*//.*?\n', '' }
try {
    $cfg = $jsonBody | ConvertFrom-Json
} catch {
    Write-Host "  $F Failed to parse opencode.jsonc: $_" -ForegroundColor Red
    exit 2
}
$agents = $cfg.agent

# Agent names to test
$agentNames = @('orchestrator', 'researcher', 'reviewer', 'executor')

# ---- TEST 1 ----
Write-Host "[TEST 1] Step Budget Consistency" -ForegroundColor Yellow
$t1=$true
$docO=0; $docR=0; $docV=0; $docE=0
if ($agentsMd -match 'O:(\d+)\s+R:(\d+)\s+V:(\d+)\s+E:(\d+)') {
    $docO=[int]$Matches[1]; $docR=[int]$Matches[2]; $docV=[int]$Matches[3]; $docE=[int]$Matches[4]
}
$checks1 = @{orchestrator=$docO; researcher=$docR; reviewer=$docV; executor=$docE}
foreach ($an in $agentNames) {
    $dv = $checks1[$an]
    $jv = if ($agents.$an.PSObject.Properties['steps']) { $agents.$an.steps } else { $null }
    if ($jv -eq $dv) { Write-Host "  $P ${an}: ${jv}" -ForegroundColor Green }
    else { Write-Host "  $F ${an}: jsonc=${jv} vs doc=${dv}" -ForegroundColor Red; $t1=$false }
}
if ($t1) { $passed++ } else { $failed++ }

# ---- TEST 2 ----
Write-Host "[TEST 2] Model Assignment (validated against profiles.json)" -ForegroundColor Yellow
$t2=$true
$profilesJson = Get-Content "$root\profiles\profiles.json" -Raw
try { $reg = $profilesJson | ConvertFrom-Json } catch { Write-Host "  $F Failed to parse profiles.json" -ForegroundColor Red; $t2=$false }
$validModels = @($reg.models.PSObject.Properties.Name)
foreach ($an in $agentNames) {
    $actual = if ($agents.$an.PSObject.Properties['model']) { $agents.$an.model } else { '' }
    if (-not $actual) { Write-Host "  $F ${an}: no model assigned" -ForegroundColor Red; $t2=$false; continue }
    $found = $false
    foreach ($vm in $validModels) { if ($actual -match [regex]::Escape($vm)) { $found=$true; break } }
    if ($found) { Write-Host "  $P ${an}: ${actual}" -ForegroundColor Green }
    else { Write-Host "  $F ${an}: '${actual}' not found in profiles.json models" -ForegroundColor Red; $t2=$false }
}
if ($t2) { $passed++ } else { $failed++ }

# ---- TEST 3 ----
Write-Host "[TEST 3] Permission Sanity" -ForegroundColor Yellow
$t3=$true

# Researcher no edit
$resPerm = $agents.researcher.permission
if ($resPerm.PSObject.Properties['edit']) {
    Write-Host "  $F Researcher has edit: allow (should not!)" -ForegroundColor Red; $t3=$false
} else { Write-Host "  $P Researcher: no edit access" -ForegroundColor Green }

# Executor has edit
$exePerm = $agents.executor.permission
if ($exePerm.edit -eq 'allow') {
    Write-Host "  $P Executor: has edit access" -ForegroundColor Green
} else { Write-Host "  $F Executor missing edit: allow" -ForegroundColor Red; $t3=$false }

# Orchestrator task scoped (not wildcard)
$orchPerm = $agents.orchestrator.permission
if ($orchPerm.task.PSObject.Properties['*']) {
    $wildVal = $orchPerm.task.'*'
    if ($wildVal -eq 'allow') {
        Write-Host "  $F Orchestrator has wildcard task (should be scoped!)" -ForegroundColor Red; $t3=$false
    } else { Write-Host "  $P Orchestrator task: scoped correctly (wildcard=${wildVal})" -ForegroundColor Green }
} else {
    # Check individual scopes
    $hasRes = $orchPerm.task.researcher -eq 'allow'
    $hasRev = $orchPerm.task.reviewer -eq 'allow'
    $hasExe = $orchPerm.task.executor -eq 'allow'
    if ($hasRes -and $hasRev -and $hasExe) {
        Write-Host "  $P Orchestrator task: scoped correctly (researcher+reviewer+executor)" -ForegroundColor Green
    } else { Write-Host "  $F Orchestrator task scope incomplete" -ForegroundColor Red; $t3=$false }
}
if ($t3) { $passed++ } else { $failed++ }

# ---- TEST 4 ----
Write-Host "[TEST 4] Prompt Keywords" -ForegroundColor Yellow
$t4=$true
$promptTests = @{'orchestrator'=@('task','dispatch');'researcher'=@('evidence','file:line');'reviewer'=@('BLOCKING','audit');'executor'=@('implement','YAGNI')}
foreach ($an in $agentNames) {
    $kws = $promptTests[$an]
    $prompt = if ($agents.$an.PSObject.Properties['prompt']) { $agents.$an.prompt } else { '' }
    if (-not $prompt) { Write-Host "  $F ${an}: prompt not found" -ForegroundColor Red; $t4=$false; continue }
    $allFound = $true
    foreach ($kw in $kws) {
        if ($prompt -notmatch [regex]::Escape($kw)) { Write-Host "  $W ${an} missing keyword '${kw}'" -ForegroundColor Yellow; $allFound=$false; $t4=$false }
    }
    if ($allFound) { Write-Host "  $P ${an}: all keywords present" -ForegroundColor Green }
}
if ($t4) { $passed++ } else { $failed++ }

# ---- TEST 5 ----
Write-Host "[TEST 5] Cross-File Dispatch Consistency" -ForegroundColor Yellow
$t5=$true
$fileChecks = @{'orchestrator.md'=$orchMd; 'SKILL.md'=$skillMd; 'AGENTS.md'=$agentsMd}
foreach ($kv in $fileChecks.GetEnumerator()) {
    $fn = $kv.Key; $content = $kv.Value
    $hasTask = $content -match [regex]::Escape('task(')
    $hasSubagent = $content -match [regex]::Escape('subagent_type')
    if ($hasTask -and $hasSubagent) {
        Write-Host "  $P ${fn}: references task() + subagent_type" -ForegroundColor Green
    } else {
        $missing = @()
        if (-not $hasTask) { $missing += 'task(' }
        if (-not $hasSubagent) { $missing += 'subagent_type' }
        Write-Host "  $F ${fn}: missing $($missing -join ', ')" -ForegroundColor Red; $t5=$false
    }
}
if ($t5) { $passed++ } else { $failed++ }

# ---- Summary ----
Write-Host ""
Write-Host "=== RESULTS ===" -ForegroundColor Cyan
Write-Host "  PASS: ${passed}/5" -ForegroundColor $(if ($passed -eq 5) {'Green'} elseif ($passed -ge 3) {'Yellow'} else {'Red'})
if ($failed -gt 0) { Write-Host "  FAIL: ${failed}/5" -ForegroundColor Red }
if ($warnings -gt 0) { Write-Host "  WARN: ${warnings}" -ForegroundColor Yellow }
Write-Host ""
if ($passed -eq 5) { Write-Host "STRESS TEST PASSED - All consistent" -ForegroundColor Green; exit 0 }
elseif ($passed -ge 3) { Write-Host "STRESS TEST PARTIAL - ${passed}/5" -ForegroundColor Yellow; exit 1 }
else { Write-Host "STRESS TEST FAILED - ${passed}/5" -ForegroundColor Red; exit 2 }
