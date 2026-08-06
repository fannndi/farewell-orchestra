# detect-project-type.ps1 — Detect project type from root files
# Usage: .\detect-project-type.ps1 -ProjectPath "C:\path\to\project"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath
)

if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project not found" -ForegroundColor Red
    exit 1
}

$type = "Unknown"
$config = ""
$sourcePattern = ""
$testCommand = ""
$buildCommand = ""
$lintCommand = ""

# Detect type
if (Test-Path (Join-Path $ProjectPath "pubspec.yaml")) {
    $type = "Flutter/Dart"
    $config = "pubspec.yaml"
    $sourcePattern = "lib/**/*.dart"
    $testCommand = "flutter test"
    $buildCommand = "flutter build apk"
    $lintCommand = "flutter analyze"
}
elseif (Test-Path (Join-Path $ProjectPath "package.json")) {
    $type = "Node.js"
    $config = "package.json"
    $sourcePattern = "src/**/*.{ts,js}"
    $testCommand = "npm test"
    $buildCommand = "npm run build"
    $lintCommand = "npm run lint"
}
elseif (Test-Path (Join-Path $ProjectPath "requirements.txt")) {
    $type = "Python"
    $config = "requirements.txt"
    $sourcePattern = "src/**/*.py"
    $testCommand = "pytest"
    $buildCommand = "python -m build"
    $lintCommand = "ruff check ."
}
elseif (Test-Path (Join-Path $ProjectPath "pyproject.toml")) {
    $type = "Python"
    $config = "pyproject.toml"
    $sourcePattern = "src/**/*.py"
    $testCommand = "pytest"
    $buildCommand = "python -m build"
    $lintCommand = "ruff check ."
}
elseif (Test-Path (Join-Path $ProjectPath "Cargo.toml")) {
    $type = "Rust"
    $config = "Cargo.toml"
    $sourcePattern = "src/**/*.rs"
    $testCommand = "cargo test"
    $buildCommand = "cargo build"
    $lintCommand = "cargo clippy"
}
elseif (Test-Path (Join-Path $ProjectPath "go.mod")) {
    $type = "Go"
    $config = "go.mod"
    $sourcePattern = "**/*.go"
    $testCommand = "go test ./..."
    $buildCommand = "go build ./..."
    $lintCommand = "golangci-lint run"
}
elseif (Test-Path (Join-Path $ProjectPath "pom.xml")) {
    $type = "Java (Maven)"
    $config = "pom.xml"
    $sourcePattern = "src/**/*.java"
    $testCommand = "mvn test"
    $buildCommand = "mvn package"
    $lintCommand = "mvn checkstyle:check"
}
elseif (Test-Path (Join-Path $ProjectPath "build.gradle")) {
    $type = "Java (Gradle)"
    $config = "build.gradle"
    $sourcePattern = "src/**/*.java"
    $testCommand = "gradle test"
    $buildCommand = "gradle build"
    $lintCommand = "gradle checkstyleMain"
}

# Output
Write-Host "=== Project Type Detection ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Type:          $type"
Write-Host "Config:        $config"
Write-Host "Source:        $sourcePattern"
Write-Host "Test:          $testCommand"
Write-Host "Build:         $buildCommand"
Write-Host "Lint:          $lintCommand"
Write-Host ""

# Return as JSON for programmatic use
$result = @{
    type = $type
    config = $config
    sourcePattern = $sourcePattern
    testCommand = $testCommand
    buildCommand = $buildCommand
    lintCommand = $lintCommand
}
$result | ConvertTo-Json
