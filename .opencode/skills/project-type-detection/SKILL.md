---
name: project-type-detection
description: Auto-detect project type from root files.
activation: When starting cross-project work
trigger: Cross-project request detected
---

# Project Type Detection

## Detection Logic

Check root files in order:

| File | Type | Config |
|------|------|--------|
| `pubspec.yaml` | Flutter/Dart | pubspec.yaml |
| `package.json` | Node.js | package.json |
| `requirements.txt` | Python | requirements.txt |
| `pyproject.toml` | Python | pyproject.toml |
| `Cargo.toml` | Rust | Cargo.toml |
| `go.mod` | Go | go.mod |
| `pom.xml` | Java (Maven) | pom.xml |
| `build.gradle` | Java (Gradle) | build.gradle |
| `*.csproj` | C# (.NET) | *.csproj |

## Type-Specific Commands

| Type | Test | Build | Lint |
|------|------|-------|------|
| Flutter | `flutter test` | `flutter build apk` | `flutter analyze` |
| Node.js | `npm test` | `npm run build` | `npm run lint` |
| Python | `pytest` | `python -m build` | `ruff check .` |
| Rust | `cargo test` | `cargo build` | `cargo clippy` |
| Go | `go test ./...` | `go build ./...` | `golangci-lint run` |
| Java | `mvn test` | `mvn package` | `mvn checkstyle:check` |
| C# | `dotnet test` | `dotnet build` | `dotnet format --verify-no-changes` |

## Type-Specific Source Patterns

| Type | Source Pattern |
|------|---------------|
| Flutter | `lib/**/*.dart` |
| Node.js | `src/**/*.{ts,js}` |
| Python | `src/**/*.py` |
| Rust | `src/**/*.rs` |
| Go | `**/*.go` |
| Java | `src/**/*.java` |
| C# | `**/*.cs` |

## Usage

1. Run `detect-project-type.ps1 -ProjectPath "C:\path\to\project"`
2. Use detected type for:
   - Source file glob patterns
   - Config file reading
   - Test/build/lint commands
   - Template selection
