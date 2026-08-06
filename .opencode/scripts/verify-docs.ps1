# verify-docs.ps1 — Check if a project has all required docs
# Usage: .\verify-docs.ps1 -ProjectPath "C:\path\to\project"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath
)

$coreDocs = @("PRD.md", "Architecture.md", "Rules.md", "Tasks.md", "Context.md")
$conditionalDocs = @("Schema.md", "API_Contract.md")
$optionalDocs = @("Design.md", "Tests.md", "debug.md")

Write-Host "=== Doc Verification: $ProjectPath ===" -ForegroundColor Cyan
Write-Host ""

# Check if project exists
if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project path not found: $ProjectPath" -ForegroundColor Red
    exit 1
}

# Check docs directory
$docsPath = Join-Path $ProjectPath "docs"
if (-not (Test-Path $docsPath)) {
    Write-Host "WARNING: docs/ directory not found" -ForegroundColor Yellow
    Write-Host "  Creating docs/ directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $docsPath -Force | Out-Null
}

# Check core docs
Write-Host "CORE DOCS (required):" -ForegroundColor Green
$coreMissing = @()
foreach ($doc in $coreDocs) {
    $docPath = Join-Path $docsPath $doc
    if (Test-Path $docPath) {
        $size = (Get-Item $docPath).Length
        Write-Host "  [x] $doc ($size bytes)" -ForegroundColor Green
    } else {
        Write-Host "  [ ] $doc (MISSING)" -ForegroundColor Red
        $coreMissing += $doc
    }
}

# Check conditional docs
Write-Host ""
Write-Host "CONDITIONAL DOCS (if applicable):" -ForegroundColor Yellow
foreach ($doc in $conditionalDocs) {
    $docPath = Join-Path $docsPath $doc
    if (Test-Path $docPath) {
        Write-Host "  [x] $doc" -ForegroundColor Green
    } else {
        Write-Host "  [ ] $doc (not found - may not be needed)" -ForegroundColor Yellow
    }
}

# Check optional docs
Write-Host ""
Write-Host "OPTIONAL DOCS:" -ForegroundColor Gray
foreach ($doc in $optionalDocs) {
    $docPath = Join-Path $docsPath $doc
    if (Test-Path $docPath) {
        Write-Host "  [x] $doc" -ForegroundColor Green
    } else {
        Write-Host "  [ ] $doc" -ForegroundColor Gray
    }
}

# Check sub-project.md
Write-Host ""
$subProjectPath = Join-Path $ProjectPath "sub-project.md"
if (Test-Path $subProjectPath) {
    Write-Host "  [x] sub-project.md" -ForegroundColor Green
} else {
    Write-Host "  [ ] sub-project.md (recommended)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
if ($coreMissing.Count -eq 0) {
    Write-Host "RESULT: All core docs present!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "RESULT: Missing $($coreMissing.Count) core doc(s):" -ForegroundColor Red
    foreach ($doc in $coreMissing) {
        Write-Host "  - $doc" -ForegroundColor Red
    }
    exit 1
}
