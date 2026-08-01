<#
.SYNOPSIS
    Session-end hook: auto-capture usage report (safety net footer).
.DESCRIPTION
    Non-blocking. Dipanggil dispatch.ps1 / hook runner saat event sessionEnd.
    Capture usage_report.py --delta ke %TEMP%\opencode\last-usage-report.json (JSON)
    dan last-usage-report.md (markdown, bisa dipakai orchestrator di report berikutnya).
    Exit SELALU 0 — jangan pernah block session end.
#>

$ErrorActionPreference = "Stop"
$scriptPy = Join-Path $PSScriptRoot "..\tools\usage_report.py"
$marker   = Join-Path $PSScriptRoot "..\tools\.usage-marker"
$outDir   = Join-Path $env:TEMP "opencode"
$jsonPath = Join-Path $outDir "last-usage-report.json"
$mdPath   = Join-Path $outDir "last-usage-report.md"
$noBom    = New-Object System.Text.UTF8Encoding($false)

try {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null

    # Baca marker lama — biar versi markdown konsisten dgn JSON (delta yg sama)
    $oldMarker = $null
    if (Test-Path -LiteralPath $marker) { $oldMarker = (Get-Content -LiteralPath $marker -Raw).Trim() }

    # 1) JSON: --delta --json (sekalian update marker ke now = akhir sesi)
    $jsonOut = (& python "$scriptPy" --delta --json 2>$null | Out-String)
    if ($LASTEXITCODE -eq 0 -and $jsonOut.Trim()) {
        [System.IO.File]::WriteAllText($jsonPath, $jsonOut.Trim(), $noBom)
    }

    # 2) Markdown: regenerasi dari marker lama -> delta sama dgn JSON, tanpa mutasi marker
    if ($oldMarker) {
        $mdOut = (& python "$scriptPy" --since $oldMarker 2>$null | Out-String)
    } else {
        $mdOut = (& python "$scriptPy" --delta 2>$null | Out-String)
    }
    if ($LASTEXITCODE -eq 0 -and $mdOut.Trim()) {
        [System.IO.File]::WriteAllText($mdPath, $mdOut.Trim(), $noBom)
    }

    Write-Host "[USAGE-CAPTURE] Saved $jsonPath + $mdPath"
} catch {
    # Non-blocking: hook gak boleh matikan session end
    Write-Host "[USAGE-CAPTURE] WARN: $_" -ForegroundColor Yellow
}

exit 0
