---
name: bootstrap-project
description: Use when starting work on a sub-project — generate docs via reverse engineering or update existing.
activation: When project has no docs
trigger: No docs found
---

# Bootstrap Project Docs

Dipakai orchestrator saat mulai kerja di project lain. Dua mode:

## Mode 1: Project Baru (ada ide, belum ada kode)

Kalau user kasih ide project baru:
1. Info project kurang → tanya Boss (nama, satu-liner, tech stack, target user)
2. Draft 5 core docs + 2 conditional SEKALIGUS (bukan satu-satu)
3. Delegasikan ke executor dalam SATU brief
4. Generate sub-project.md dari template
5. Report: "5/5 core docs dibuat. sub-project.md siap."

## Mode 2: Project Existing (ada kode, belum ada docs)

Ini **Reverse Engineering Mode**. Dipanggil dari prepare §0.

1. Dispatch researcher untuk deep scan (lihat cross-project/guide.md Phase 1-5)
2. Dispatch executor untuk generate docs dari findings researcher
3. Consistency check: Schema↔API_Contract, PRD↔Tasks
4. Report: "Docs generated dari reverse engineering. Review?"

## 5 Core Docs (WAJIB)

| Doc | Isi |
|-----|-----|
| **PRD.md** | Latar belakang, scope, MVP, target user, fitur in/out, user flow |
| **Architecture.md** | Tech stack, directory tree, alur data, keputusan + alasan |
| **Rules.md** | Naming convention, error handling, coding standards |
| **Tasks.md** | Checklist `- [ ]` per fase, berurutan, granular |
| **Context.md** | Konteks bisnis, business rules, background story |

## 2 Conditional Docs

| Doc | Generate Kalau |
|-----|---------------|
| **Schema.md** | Project pakai database (tabel, kolom, relasi, constraints) |
| **API_Contract.md** | Project pakai API (endpoint, method, request, response) |

## Consistency Rules

- Nama variabel/tabel di Schema.md = nama field di API_Contract.md
- Tech stack di Architecture.md = konvensi di Rules.md
- Fitur di PRD.md = task di Tasks.md = acceptance di Tasks.md

## Update Mode (project existing + docs ada)

Kalau docs udah ada — JANGAN generate ulang. Baca dulu, tanya Boss bagian mana yang mau di-update, edit incremental.

## Proactive

- Orchestrator: kalau researcher lapor project tanpa docs → trigger reverse engineering
- Executor gagal di tengah generate → re-dispatch file yang gagal aja, jangan ulang semua

## Mode 3: PRD-Heavy Project (ada PRD detail, belum ada docs)

Kalau project sudah punya PRD detail (>200 baris):
1. Baca PRD → extract tech stack, features, architecture, models, services
2. Generate Architecture.md, Rules.md, Tasks.md, Context.md dari PRD
3. Skip reverse engineering → langsung generate dari PRD + code scan ringan
4. Code scan hanya untuk verify PRD accuracy, bukan discover from scratch
5. Report: "Docs generated dari PRD. Code verified."

### PRD Extraction Checklist
- [ ] Tech stack (framework, language, packages)
- [ ] Directory structure (if mentioned)
- [ ] Data models (fields, types, relationships)
- [ ] Services (business logic, API calls)
- [ ] UI/UX specs (screens, navigation, theme)
- [ ] Non-functional requirements (performance, security)
- [ ] Error handling patterns
- [ ] Localization support

## Permission Handling

### Pre-Flight
1. Check `opencode.jsonc` → agent.permission.external_directory
2. If target path not listed → add before dispatch
3. Pattern: ``"C:/Users/FANNNDI/Documents/project/**": "allow"``

### Fallback: Orchestrator Direct Scan
If sub-agents hit permission blocks:
1. Orchestrator reads files directly (universal access)
2. Generates docs from findings
3. Dispatches executor only for write operations

## Project Type Detection

Detect project type from root files:
```
pubspec.yaml     → Flutter/Dart
package.json     → Node.js
requirements.txt → Python
pyproject.toml  → Python (modern)
Cargo.toml       → Rust
go.mod           → Go
pom.xml          → Java (Maven)
build.gradle     → Java (Gradle)
*.csproj         → C# (.NET)
```

Type determines:
- Source file glob patterns
- Config files to read
- Test commands
- Build commands

### Type-Specific Commands

| Type | Test | Build | Lint |
|------|------|-------|------|
| Flutter | `flutter test` | `flutter build apk` | `flutter analyze` |
| Node.js | `npm test` | `npm run build` | `npm run lint` |
| Python | `pytest` | `python -m build` | `ruff check .` |
| Rust | `cargo test` | `cargo build` | `cargo clippy` |
| Go | `go test ./...` | `go build ./...` | `golangci-lint run` |
| Java | `mvn test` | `mvn package` | `mvn checkstyle:check` |
| C# | `dotnet test` | `dotnet build` | `dotnet format --verify-no-changes` |

### Type-Specific Source Patterns

| Type | Source Pattern |
|------|---------------|
| Flutter | `lib/**/*.dart` |
| Node.js | `src/**/*.{ts,js}` |
| Python | `src/**/*.py` |
| Rust | `src/**/*.rs` |
| Go | `**/*.go` |
| Java | `src/**/*.java` |
| C# | `**/*.cs` |

### Detection Script

Run `detect-project-type.ps1 -ProjectPath "C:\path\to\project"` untuk auto-detect dari root files.

## Verify Script

After generating docs, run:
```powershell
.\.opencode\scripts\verify-docs.ps1 -ProjectPath "C:\path\to\project"
```

This checks:
- All 5 core docs present
- Conditional docs status
- sub-project.md exists
