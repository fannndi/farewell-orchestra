# auto-deps.ps1 — Auto-detect and install project dependencies
# Usage: .\auto-deps.ps1 -ProjectPath "C:\path\to\project"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath
)

if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project not found" -ForegroundColor Red
    exit 1
}

Write-Host "=== Auto Dependencies: $ProjectPath ===" -ForegroundColor Cyan
Write-Host ""

# Detect project type and install
if (Test-Path (Join-Path $ProjectPath "pubspec.yaml")) {
    Write-Host "Detected: Flutter/Dart" -ForegroundColor Green
    Write-Host "Running: flutter pub get" -ForegroundColor Yellow
    & flutter pub get --directory=$ProjectPath
}
elseif (Test-Path (Join-Path $ProjectPath "package.json")) {
    Write-Host "Detected: Node.js" -ForegroundColor Green
    Write-Host "Running: npm install" -ForegroundColor Yellow
    & npm install --prefix=$ProjectPath
}
elseif (Test-Path (Join-Path $ProjectPath "requirements.txt")) {
    Write-Host "Detected: Python" -ForegroundColor Green
    Write-Host "Running: pip install -r requirements.txt" -ForegroundColor Yellow
    & pip install -r (Join-Path $ProjectPath "requirements.txt")
}
elseif (Test-Path (Join-Path $ProjectPath "pyproject.toml")) {
    Write-Host "Detected: Python (pyproject.toml)" -ForegroundColor Green
    Write-Host "Running: pip install ." -ForegroundColor Yellow
    & pip install . --directory=$ProjectPath
}
elseif (Test-Path (Join-Path $ProjectPath "Cargo.toml")) {
    Write-Host "Detected: Rust" -ForegroundColor Green
    Write-Host "Running: cargo fetch" -ForegroundColor Yellow
    & cargo fetch --manifest-path=(Join-Path $ProjectPath "Cargo.toml")
}
elseif (Test-Path (Join-Path $ProjectPath "go.mod")) {
    Write-Host "Detected: Go" -ForegroundColor Green
    Write-Host "Running: go mod download" -ForegroundColor Yellow
    & go mod download -C $ProjectPath
}
else {
    Write-Host "Unknown project type" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Dependencies installed!" -ForegroundColor Green
