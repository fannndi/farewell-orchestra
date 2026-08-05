# Cross-Project Guide

> Guide untuk handle project lain dari farewell-orchestra.
> Orchestrator baca ini kalau user bilang "aku mau kerja di project X".

## Flow

```
User: "aku mau kerja di project X"
  │
  ▼
Orchestrator detect cross-project request
  │
  ▼
prepare §0: Check docs di project X
  │
  ├── Semua CORE ada → baca docs → pahami context → lanjut kerja
  │
  └── Ada yang hilang → Reverse Engineering Mode
        │
        ▼
      Researcher deep scan project
        │
        ▼
      Executor generate 5 core docs + 2 conditional
        │
        ▼
      Baca docs → pahami context → lanjut kerja
```

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
```
glob <project>/**/*.{ts,js,py,go,rs,java,tsx,jsx}
```
- Pahami folder layout
- Identifikasi entry points
- Identifikasi config files

### Phase 2 — Config (10%)
- package.json / requirements.txt / Cargo.toml → tech stack
- tsconfig / vite.config / next.config → framework config
- .env.example → environment variables
- docker-compose.yml → deployment setup

### Phase 3 — Code Patterns (40%)
- Read entry points → routing, middleware, initialization
- Trace import chains → dependency graph
- Read 2-3 representative files → naming conventions, error handling
- Read database models / migrations → schema (kalau ada)
- Read API routes / controllers → endpoints (kalau ada)

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

## Consistency Rules

Kalau generate docs, pastikan:
- Nama variabel/tabel di Schema.md = nama field di API_Contract.md
- Tech stack di Architecture.md = konvensi di Rules.md
- Fitur di PRD.md = task di Tasks.md

## Update sub-project.md

Setelah docs ada, update sub-project.md di project target:
- Isi Ringkasan (nama, satu kalimat, path, profile, fase, task aktif)
- Tandai docs yang ada dengan `[x]`
- Isi Konteks Bisnis Singkat
- Isi Task Aktif
- Isi Memori Agent (1 baris per agent)
