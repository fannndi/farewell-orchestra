# project-health.ps1 — Check project health indicators
# Usage: .\project-health.ps1 -ProjectPath "C:\path\to\project"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath
)

Write-Host "=== Project Health Check: $ProjectPath ===" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project not found" -ForegroundColor Red
    exit 1
}

$score = 0
$maxScore = 0

# Check 1: Git initialized
$maxScore++
if (Test-Path (Join-Path $ProjectPath ".git")) {
    Write-Host "  [x] Git initialized" -ForegroundColor Green
    $score++
} else {
    Write-Host "  [ ] Git not initialized" -ForegroundColor Red
}

# Check 2: README exists
$maxScore++
$readme = Get-ChildItem -Path $ProjectPath -Filter "README*" -ErrorAction SilentlyContinue
if ($readme) {
    Write-Host "  [x] README exists ($($readme.Name))" -ForegroundColor Green
    $score++
} else {
    Write-Host "  [ ] No README" -ForegroundColor Yellow
}

# Check 3: .gitignore exists
$maxScore++
if (Test-Path (Join-Path $ProjectPath ".gitignore")) {
    Write-Host "  [x] .gitignore exists" -ForegroundColor Green
    $score++
} else {
    Write-Host "  [ ] No .gitignore" -ForegroundColor Yellow
}

# Check 4: Docs directory
$maxScore++
if (Test-Path (Join-Path $ProjectPath "docs")) {
    Write-Host "  [x] docs/ directory exists" -ForegroundColor Green
    $score++
} else {
    Write-Host "  [ ] No docs/ directory" -ForegroundColor Yellow
}

# Check 5: Test directory
$maxScore++
$testDirs = @("test", "tests", "__tests__", "spec")
$hasTests = $false
foreach ($dir in $testDirs) {
    if (Test-Path (Join-Path $ProjectPath $dir)) {
        $hasTests = $true
        break
    }
}
if ($hasTests) {
    Write-Host "  [x] Test directory exists" -ForegroundColor Green
    $score++
} else {
    Write-Host "  [ ] No test directory" -ForegroundColor Yellow
}

# Check 6: sub-project.md
$maxScore++
if (Test-Path (Join-Path $ProjectPath "sub-project.md")) {
    Write-Host "  [x] sub-project.md exists" -ForegroundColor Green
    $score++
} else {
    Write-Host "  [ ] No sub-project.md" -ForegroundColor Gray
}

# Summary
Write-Host ""
$pct = [math]::Round(($score / $maxScore) * 100)
$color = if ($pct -ge 80) { "Green" } elseif ($pct -ge 50) { "Yellow" } else { "Red" }
Write-Host "HEALTH SCORE: $score/$maxScore ($pct%)" -ForegroundColor $color
