# Project Templates

Templates for common project types. Use when starting cross-project work.

## Available Templates

| Type | Directory | Files |
|------|-----------|-------|
| Flutter/Dart | `flutter/` | architecture.md, docs-template.md |
| Node.js | `nodejs/` | architecture.md |
| Python | `python/` | architecture.md |
| Rust | `rust/` | architecture.md |
| Go | `go/` | architecture.md |

## Usage

### 1. Detect Project Type
```powershell
.\scripts\detect-project-type.ps1 -ProjectPath "C:\path\to\project"
```

### 2. Load Template
Based on detected type, read the corresponding template:
- Flutter → `.opencode/templates/flutter/architecture.md`
- Node.js → `.opencode/templates/nodejs/architecture.md`
- Python → `.opencode/templates/python/architecture.md`
- Rust → `.opencode/templates/rust/architecture.md`
- Go → `.opencode/templates/go/architecture.md`

### 3. Generate Docs
Use template as reference for generating:
- Architecture.md — follow template structure
- Rules.md — adapt conventions from template
- Tasks.md — use template patterns for task format
- Context.md — use template sections

## Template Structure

Each template contains:
- **Layer Architecture** — diagram + description
- **Directory Structure** — standard folder layout
- **Common Patterns** — error handling, testing, etc.
- **Testing Structure** — test folder organization

## Adding New Templates

To add a new project type:
1. Create directory: `.opencode/templates/<type>/`
2. Create `architecture.md` with:
   - Layer architecture diagram
   - Directory structure
   - Common patterns
   - Testing structure
3. Update this README
4. Update `detect-project-type.ps1`
