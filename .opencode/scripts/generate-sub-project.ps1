# generate-sub-project.ps1 — Auto-generate sub-project.md for a project
# Usage: .\generate-sub-project.ps1 -ProjectPath "C:\path\to\project" -ProjectName "My Project"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath,
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectName = ""
)

if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project not found: $ProjectPath" -ForegroundColor Red
    exit 1
}

# Auto-detect project name if not provided
if ($ProjectName -eq "") {
    $ProjectName = Split-Path $ProjectPath -Leaf
}

# Detect project type
$projectType = "Unknown"
if (Test-Path (Join-Path $ProjectPath "pubspec.yaml")) { $projectType = "Flutter/Dart" }
elseif (Test-Path (Join-Path $ProjectPath "package.json")) { $projectType = "Node.js" }
elseif (Test-Path (Join-Path $ProjectPath "requirements.txt")) { $projectType = "Python" }
elseif (Test-Path (Join-Path $ProjectPath "pyproject.toml")) { $projectType = "Python" }
elseif (Test-Path (Join-Path $ProjectPath "Cargo.toml")) { $projectType = "Rust" }
elseif (Test-Path (Join-Path $ProjectPath "go.mod")) { $projectType = "Go" }

# Check docs status
$docsPath = Join-Path $ProjectPath "docs"
$coreDocs = @("PRD.md", "Architecture.md", "Rules.md", "Tasks.md", "Context.md")
$docsStatus = @()
foreach ($doc in $coreDocs) {
    if (Test-Path (Join-Path $docsPath $doc)) {
        $docsStatus += "[x] $doc"
    } else {
        $docsStatus += "[ ] $doc"
    }
}

# Generate sub-project.md
$date = Get-Date -Format "yyyy-MM-dd"
$content = @"
# sub-project: $ProjectName

## Ringkasan
- **Nama:** $ProjectName
- **Satu kalimat:** [TODO: describe project in one sentence]
- **Path:** $ProjectPath
- **Profile:** [TODO: Pro/Standard/Minimal]
- **Fase:** [TODO: Development/Maintenance/Archive]
- **Task aktif:** [TODO: current task]

## Docs
$($docsStatus -join "`n")
- [ ] Schema.md (conditional)
- [ ] API_Contract.md (conditional)

## Konteks Bisnis Singkat
[TODO: describe business context]

## Task Aktif
1. [TODO: current task]

## Memori Agent
| Agent | Konteks | File kunci |
|-------|---------|------------|
| orchestrator | [TODO] | — |
| researcher | [TODO] | [TODO] |
| reviewer | [TODO] | [TODO] |
| executor | [TODO] | [TODO] |
"@

$subProjectPath = Join-Path $ProjectPath "sub-project.md"
$content | Set-Content -Path $subProjectPath -Encoding UTF8

Write-Host "Generated: $subProjectPath" -ForegroundColor Green
Write-Host "Project Type: $projectType" -ForegroundColor Cyan
Write-Host "Docs Status:" -ForegroundColor Cyan
foreach ($status in $docsStatus) {
    Write-Host "  $status"
}
