# auto-test.ps1 — Auto-detect and run project tests
# Usage: .\auto-test.ps1 -ProjectPath "C:\path\to\project"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath
)

if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project not found" -ForegroundColor Red
    exit 1
}

Write-Host "=== Auto Test: $ProjectPath ===" -ForegroundColor Cyan
Write-Host ""

# Detect project type and run tests
if (Test-Path (Join-Path $ProjectPath "pubspec.yaml")) {
    Write-Host "Detected: Flutter/Dart" -ForegroundColor Green
    Write-Host "Running: flutter test" -ForegroundColor Yellow
    & flutter test --directory=$ProjectPath
}
elseif (Test-Path (Join-Path $ProjectPath "package.json")) {
    Write-Host "Detected: Node.js" -ForegroundColor Green
    Write-Host "Running: npm test" -ForegroundColor Yellow
    & npm test --prefix=$ProjectPath
}
elseif (Test-Path (Join-Path $ProjectPath "requirements.txt")) {
    Write-Host "Detected: Python" -ForegroundColor Green
    Write-Host "Running: pytest" -ForegroundColor Yellow
    & pytest $ProjectPath
}
elseif (Test-Path (Join-Path $ProjectPath "pyproject.toml")) {
    Write-Host "Detected: Python (pyproject.toml)" -ForegroundColor Green
    Write-Host "Running: pytest" -ForegroundColor Yellow
    & pytest $ProjectPath
}
elseif (Test-Path (Join-Path $ProjectPath "Cargo.toml")) {
    Write-Host "Detected: Rust" -ForegroundColor Green
    Write-Host "Running: cargo test" -ForegroundColor Yellow
    & cargo test --manifest-path=(Join-Path $ProjectPath "Cargo.toml")
}
elseif (Test-Path (Join-Path $ProjectPath "go.mod")) {
    Write-Host "Detected: Go" -ForegroundColor Green
    Write-Host "Running: go test ./..." -ForegroundColor Yellow
    & go test ./... -C $ProjectPath
}
else {
    Write-Host "Unknown project type" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Tests completed!" -ForegroundColor Green
