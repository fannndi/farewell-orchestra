<#
.SYNOPSIS
    Pre-generate hook: validasi profiles.json sebelum generate
.DESCRIPTION
    Dipanggil oleh dispatch.ps1 sebelum profiles/generate.py jalan.
    Exit 0 = lanjutkan generate. Exit 1 = block generate.
#>
param()

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$ProfilesJson = Join-Path $ProjectRoot "profiles\profiles.json"
$GeneratePy = Join-Path $ProjectRoot "profiles\generate.py"

Write-Host "[PRE-GENERATE] Validating profiles.json..."

if (-not (Test-Path -LiteralPath $ProfilesJson)) {
    Write-Host "[PRE-GENERATE] FAIL: profiles.json not found at $ProfilesJson" -ForegroundColor Red
    exit 1
}

try {
    $raw = Get-Content -LiteralPath $ProfilesJson -Raw -Encoding utf8
    $parsed = $raw | ConvertFrom-Json -ErrorAction Stop

    # Quick sanity: must have profiles array and models
    if (-not $parsed.profiles -or $parsed.profiles.Count -eq 0) {
        Write-Host "[PRE-GENERATE] FAIL: No profiles defined" -ForegroundColor Red
        exit 1
    }
    if (-not $parsed.models) {
        Write-Host "[PRE-GENERATE] FAIL: No models defined" -ForegroundColor Red
        exit 1
    }

    # Validate required fields per profile
    foreach ($p in $parsed.profiles) {
        if (-not $p.name -or -not $p.label -or -not $p.model) {
            Write-Host "[PRE-GENERATE] FAIL: Profile '$($p.name)' missing required fields (name/label/model)" -ForegroundColor Red
            exit 1
        }
    }

    Write-Host "[PRE-GENERATE] profiles.json valid - $($parsed.profiles.Count) profiles, $(($parsed.models.PSObject.Properties).Count) models" -ForegroundColor Green
} catch {
    Write-Host "[PRE-GENERATE] FAIL: Invalid JSON: $_" -ForegroundColor Red
    exit 1
}

# Optional: run generate.py --validate for deeper check
if (Test-Path -LiteralPath $GeneratePy) {
    try {
        $result = & python $GeneratePy --validate 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[PRE-GENERATE] FAIL: generate.py --validate failed:" -ForegroundColor Red
            $result | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
            exit 1
        }
        Write-Host "[PRE-GENERATE] generate.py --validate OK" -ForegroundColor Green
    } catch {
        Write-Host "[PRE-GENERATE] WARN: generate.py --validate error: $_" -ForegroundColor Yellow
        # Non-blocking - python may not be available
    }
}

exit 0