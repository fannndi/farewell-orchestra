# project-dashboard.ps1 — Show project overview dashboard
# Usage: .\project-dashboard.ps1 -ProjectPath "C:\path\to\project"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath
)

if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project not found" -ForegroundColor Red
    exit 1
}

$projectName = Split-Path $ProjectPath -Leaf
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  PROJECT DASHBOARD: $projectName" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Project Type Detection
$projectType = "Unknown"
$configFile = ""
if (Test-Path (Join-Path $ProjectPath "pubspec.yaml")) { 
    $projectType = "Flutter/Dart"
    $configFile = "pubspec.yaml"
} elseif (Test-Path (Join-Path $ProjectPath "package.json")) { 
    $projectType = "Node.js"
    $configFile = "package.json"
} elseif (Test-Path (Join-Path $ProjectPath "requirements.txt")) { 
    $projectType = "Python"
    $configFile = "requirements.txt"
} elseif (Test-Path (Join-Path $ProjectPath "pyproject.toml")) { 
    $projectType = "Python"
    $configFile = "pyproject.toml"
} elseif (Test-Path (Join-Path $ProjectPath "Cargo.toml")) { 
    $projectType = "Rust"
    $configFile = "Cargo.toml"
} elseif (Test-Path (Join-Path $ProjectPath "go.mod")) { 
    $projectType = "Go"
    $configFile = "go.mod"
}

Write-Host "📋 Project Info" -ForegroundColor Yellow
Write-Host "  Type:      $projectType"
Write-Host "  Config:    $configFile"
Write-Host "  Path:      $ProjectPath"
Write-Host ""

# Git Status
Write-Host "📦 Git Status" -ForegroundColor Yellow
if (Test-Path (Join-Path $ProjectPath ".git")) {
    $gitStatus = & git -C $ProjectPath status --short 2>$null
    $branch = & git -C $ProjectPath branch --show-current 2>$null
    $commitCount = & git -C $ProjectPath rev-list --count HEAD 2>$null
    
    Write-Host "  Branch:    $branch"
    Write-Host "  Commits:   $commitCount"
    if ($gitStatus) {
        Write-Host "  Changes:   $($gitStatus.Count) file(s) modified" -ForegroundColor Yellow
    } else {
        Write-Host "  Changes:   Clean" -ForegroundColor Green
    }
} else {
    Write-Host "  Git not initialized" -ForegroundColor Red
}
Write-Host ""

# Docs Status
Write-Host "📚 Documentation" -ForegroundColor Yellow
$docsPath = Join-Path $ProjectPath "docs"
$coreDocs = @("PRD.md", "Architecture.md", "Rules.md", "Tasks.md", "Context.md")
$docsFound = 0
foreach ($doc in $coreDocs) {
    if (Test-Path (Join-Path $docsPath $doc)) {
        Write-Host "  [x] $doc" -ForegroundColor Green
        $docsFound++
    } else {
        Write-Host "  [ ] $doc" -ForegroundColor Red
    }
}
Write-Host "  Core Docs: $docsFound/5"
Write-Host ""

# File Statistics
Write-Host "📊 File Statistics" -ForegroundColor Yellow
$sourceFiles = @()
switch ($projectType) {
    "Flutter/Dart" { $sourceFiles = Get-ChildItem -Path $ProjectPath -Recurse -Filter "*.dart" -ErrorAction SilentlyContinue }
    "Node.js" { $sourceFiles = Get-ChildItem -Path $ProjectPath -Recurse -Include "*.ts","*.js" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "node_modules" } }
    "Python" { $sourceFiles = Get-ChildItem -Path $ProjectPath -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch "__pycache__|venv" } }
    "Rust" { $sourceFiles = Get-ChildItem -Path $ProjectPath -Recurse -Filter "*.rs" -ErrorAction SilentlyContinue }
    "Go" { $sourceFiles = Get-ChildItem -Path $ProjectPath -Recurse -Filter "*.go" -ErrorAction SilentlyContinue }
}

if ($sourceFiles) {
    $totalLines = 0
    foreach ($file in $sourceFiles) {
        $lines = (Get-Content $file.FullName -ErrorAction SilentlyContinue | Measure-Object -Line).Lines
        $totalLines += $lines
    }
    Write-Host "  Source Files: $($sourceFiles.Count)"
    Write-Host "  Total Lines:  $totalLines"
} else {
    Write-Host "  No source files detected"
}
Write-Host ""

# Test Status
Write-Host "🧪 Tests" -ForegroundColor Yellow
$testDirs = @("test", "tests", "__tests__", "spec")
$hasTests = $false
foreach ($dir in $testDirs) {
    if (Test-Path (Join-Path $ProjectPath $dir)) {
        $testFiles = Get-ChildItem -Path (Join-Path $ProjectPath $dir) -Recurse -ErrorAction SilentlyContinue
        Write-Host "  Test Dir:    $dir ($($testFiles.Count) files)"
        $hasTests = $true
        break
    }
}
if (-not $hasTests) {
    Write-Host "  No test directory found" -ForegroundColor Red
}
Write-Host ""

# sub-project.md Status
Write-Host "📝 Session State" -ForegroundColor Yellow
if (Test-Path (Join-Path $ProjectPath "sub-project.md")) {
    Write-Host "  sub-project.md: EXISTS" -ForegroundColor Green
} else {
    Write-Host "  sub-project.md: MISSING" -ForegroundColor Red
}
Write-Host ""

Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
