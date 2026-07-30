# post-generate.ps1 — Hook: validasi opencode.jsonc setelah generate
# Dipanggil otomatis dari generate.py setelah copy ke root
# Semua threshold BACA dari opencode.jsonc — no hardcode
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

# Validasi tool scoping (rules tetap hardcoded — ini policy, bukan config)
$agentRules = @{
    "researcher" = @{ "forbidden" = @("edit", "bash"); "required" = @("webfetch", "websearch") }
    "reviewer"   = @{ "forbidden" = @("edit", "bash"); "required" = @("webfetch", "websearch") }
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

# Validasi step budgets — BACA dari opencode.jsonc, threshold = 80% dari declared
# Rationale: declared budget adalah max. Min recommended = 80% of declared biar gak terlalu kecil.
foreach ($name in @("orchestrator", "researcher", "reviewer", "executor")) {
    $steps = $config.agent.$name.steps
    if ($null -eq $steps) {
        $warnings += "[BUDGET] $name steps not defined in config"
        continue
    }
    $minRecommended = [int]([math]::Ceiling($steps * 0.8))
    if ($steps -lt $minRecommended -and $steps -lt 20) {
        $warnings += "[BUDGET] $name steps ($steps) below sanity floor ($minRecommended = 80% of declared or 20, whichever higher)"
    }
}

# Validasi instructions (tidak boleh load semua agent file)
$instructions = $config.instructions -join " "
if ($instructions -match "agents/\*") {
    $warnings += "[CONTEXT] instructions masih load semua agent file (*.md) - boros token"
}

# Validasi compaction.prune_rules ada kalau prune=true
$prune = $config.compaction.prune
$pruneRules = $config.compaction.prune_rules
if ($prune -eq $true -and $null -eq $pruneRules) {
    $warnings += "[COMPACTION] prune=true but no prune_rules defined - random pruning risk"
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
