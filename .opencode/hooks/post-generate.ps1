# post-generate.ps1 — Hook: validasi opencode.jsonc setelah generate
# Dipanggil otomatis dari generate.py setelah copy ke root
param(
    [string]$ConfigPath = (Join-Path (Split-Path $PSScriptRoot -Parent) "opencode.jsonc")
)

if (-not (Test-Path $ConfigPath)) {
    Write-Host "[HOOK] Config not found, skipping validation" -ForegroundColor Yellow
    exit 0
}

try {
    $raw = Get-Content $ConfigPath -Raw -Encoding utf8
    # Strip JSONC comment
    $jsonStart = $raw.IndexOf("{")
    if ($jsonStart -lt 0) { throw "No JSON object found" }
    $config = $raw.Substring($jsonStart) | ConvertFrom-Json
} catch {
    Write-Host "[HOOK] Invalid JSON: $_" -ForegroundColor Red
    exit 1
}

$errors = @()
$warnings = @()

# Validasi tool scoping
$agentRules = @{
    "researcher" = @{ "forbidden" = @("edit"); "required" = @("webfetch", "websearch") }
    "reviewer"   = @{ "forbidden" = @("edit"); "required" = @("webfetch", "websearch") }
    "executor"   = @{ "required" = @("edit") }
}

foreach ($agentName in $agentRules.Keys) {
    $agent = $config.agent.$agentName
    if (-not $agent) { 
        $warnings += "$agentName agent not found"
        continue 
    }
    $perms = $agent.permission
    
    if ($agentRules[$agentName].ContainsKey("forbidden")) {
        foreach ($tool in $agentRules[$agentName]["forbidden"]) {
            $val = $perms.$tool
            if ($val -eq "allow") {
                $errors += "[SCOPE] $agentName should NOT have '$tool' permission"
            }
        }
    }
    
    if ($agentRules[$agentName].ContainsKey("required")) {
        foreach ($tool in $agentRules[$agentName]["required"]) {
            $val = $perms.$tool
            if ($val -ne "allow") {
                $errors += "[SCOPE] $agentName should have '$tool' permission"
            }
        }
    }
}

# Validasi step budgets (min thresholds)
$stepMin = @{ "orchestrator" = 20; "researcher" = 20; "reviewer" = 16; "executor" = 20 }
foreach ($name in $stepMin.Keys) {
    $steps = $config.agent.$name.steps
    if ($steps -lt $stepMin[$name]) {
        $warnings += "[BUDGET] $name steps ($steps) below recommended minimum ($($stepMin[$name]))"
    }
}

# Validasi instructions (tidak boleh load semua agent file)
$instructions = $config.instructions -join " "
if ($instructions -match "agents/\*") {
    $warnings += "[CONTEXT] instructions masih load semua agent file (*.md) - boros token"
}

# Report
if ($errors.Count -gt 0) {
    Write-Host "[HOOK] VALIDATION FAILED:" -ForegroundColor Red
    foreach ($e in $errors) { Write-Host "  $e" -ForegroundColor Red }
    exit 1
}

if ($warnings.Count -gt 0) {
    Write-Host "[HOOK] Warnings:" -ForegroundColor Yellow
    foreach ($w in $warnings) { Write-Host "  $w" -ForegroundColor Yellow }
}

Write-Host "[HOOK] Config valid. $(@($config.agent.psobject.Properties.Name).Count) agents, $($errors.Count) errors, $($warnings.Count) warnings" -ForegroundColor Green
exit 0
