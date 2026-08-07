# Cross-Project Guide

> Guide untuk handle project lain dari farewell-orchestra.
> Orchestrator baca ini kalau user bilang "aku mau kerja di project X".

## Pre-Flight Checklist

SEBELUM mulai cross-project work, WAJIB cek:

1. **Permission** — Sub-agent bisa akses path project?
   - Cek `opencode.jsonc` → agent.permission.external_directory
   - Kalau path tidak ada → tambah dulu sebelum dispatch
   - Pattern: `C:/Users/FANNNDI/Documents/**` (recursive)
2. **Project exists** — path valid? Ada file?
3. **Git status** — ada uncommitted changes? Flag kalau ada.

## Flow

```
User: "aku mau kerja di project X"
  │
  ▼
Pre-Flight: Permission + Path check
  │
  ▼
prepare §0: Detect project type + Check docs
  │
  ├── Semua CORE ada → baca docs → pahami context → lanjut kerja
  │
  └── Ada yang hilang → Reverse Engineering Mode
        │
        ▼
      Orchestrator scan langsung (bukan sub-agent, untuk avoid permission issue)
        │
        ▼
      Generate docs dari findings
        │
        ▼
      Baca docs → pahami context → lanjut kerja
```

## Project Type Detection

Cek file di root project untuk detect type:

| Files | Type | Tech Stack |
|-------|------|------------|
| `pubspec.yaml` | Flutter/Dart | Flutter, Dart |
| `package.json` | Node.js | React/Vue/Next/Express |
| `requirements.txt` / `pyproject.toml` | Python | Django/Flask/FastAPI |
| `Cargo.toml` | Rust | Actix/Axum/etc |
| `go.mod` | Go | Gin/Echo/etc |
| `pom.xml` / `build.gradle` | Java | Spring/Android |
| `*.csproj` | C# | .NET |

**Glob patterns per type:**

| Type | Source Pattern | Config Pattern |
|------|---------------|----------------|
| Flutter | `lib/**/*.dart` | `pubspec.yaml`, `analysis_options.yaml` |
| Node.js | `src/**/*.{ts,js}` | `package.json`, `tsconfig.json` |
| Python | `src/**/*.py` / `**/*.py` | `requirements.txt`, `pyproject.toml` |
| Rust | `src/**/*.rs` | `Cargo.toml` |
| Go | `**/*.go` | `go.mod` |

## Docs yang Diperlukan

### 5 Core (WAJIB)

| Doc | Isi |
|-----|-----|
| **PRD.md** | Latar belakang, scope, MVP, target user, fitur in/out scope |
| **Architecture.md** | Tech stack, directory tree, alur data, keputusan teknis |
| **Rules.md** | Naming convention, error handling, coding standards |
| **Tasks.md** | Checklist per fase, format `- [ ]`, granular, executor-friendly |
| **Context.md** | Konteks bisnis, business rules, background story |

### 2 Conditional

| Doc | Kapan |
|-----|-------|
| **Schema.md** | Kalau project pakai database (tabel, kolom, relasi, constraints) |
| **API_Contract.md** | Kalau project pakai API (endpoint, method, request, response) |

### 3 Optional (on demand)

| Doc | Kapan |
|-----|-------|
| Design.md | Kalau project punya UI/UX (palet warna, tipografi, komponen) |
| Tests.md | Kalau butuh acceptance criteria + test scenarios |
| debug.md | Kalau butuh error tracking template |

## Reverse Engineering Workflow

### Phase 1 — Structure (5%)
Glob source files berdasarkan project type (lihat tabel di atas).
- Pahami folder layout
- Identifikasi entry points
- Identifikasi config files

### Phase 2 — Config (10%)
- Read config files → tech stack, dependencies, framework
- Read .env.example → environment variables
- Read docker-compose.yml / Dockerfile → deployment

### Phase 3 — Code Patterns (40%)
- Read entry points → routing, middleware, initialization
- Read ALL source files kalau ≤30 files
- Sample 5-10 representative files kalau >30 files
- Trace import chains → dependency graph
- Read models → data structure
- Read services → business logic

### Phase 4 — Tests & Docs (20%)
- Read existing tests → test patterns, coverage
- Read README.md → existing documentation
- Read CHANGELOG.md → project history (kalau ada)

### Phase 5 — Inference (25%)
- Dari Phase 1-4, infer:
  - Tech stack (FE/BE/DB/Tools)
  - Architecture decisions
  - Coding conventions
  - Business logic patterns
  - API surface (kalau ada)
  - Database schema (kalau ada)

### Important: Orchestrator Direct Scan

Kalau sub-agent kena permission block:
1. **Jangan fail** — orchestrator scan langsung
2. Orchestrator punya akses ke semua path (via opencode.jsonc)
3. Baca file langsung, generate docs dari findings
4. Dispatch executor hanya untuk tulis file (dia punya edit permission)

## Consistency Rules

Kalau generate docs, pastikan:
- Nama variabel/tabel di Schema.md = nama field di API_Contract.md
- Tech stack di Architecture.md = konvensi di Rules.md
- Fitur di PRD.md = task di Tasks.md
- File paths di semua doc = actual file paths di project

## Update sub-project.md

Setelah docs ada, buat sub-project.md di project target:
- Isi Ringkasan (nama, satu kalimat, path, profile, fase, task aktif)
- Tandai docs yang ada dengan `[x]`
- Isi Konteks Bisnis Singkat
- Isi Task Aktif
- Isi Memori Agent (1 baris per agent)
