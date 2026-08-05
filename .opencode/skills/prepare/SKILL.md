---
name: prepare
description: Use when receiving a request — validate input, extract requirements, chunk if needed. Gate before orchestration.
---

# Prepare

Gate awal sebelum dispatch. Flow:

```
Request → Cross-Project? → YES → Check Docs → Reverse Engineer? → Generate → Normal Flow
                ↓ NO
         Input Validation → HOLD? STOP. PARTIAL? → Grill. PASS? → Chunk → Dispatch
```

## Fallback Mode (untuk semua LLM)

Kalau LLM tidak bisa handle complex instructions:

1. **Cek** — request punya goal dan scope?
   - Ada → PASS
   - Nggak ada → HOLD, tanya: "Goal-nya apa? Scope-nya?"
2. **Output** — format: `PASS` atau `HOLD <alasan>`

Contoh: `HOLD — goal tidak jelas`

Jangan pakai chunking, assumption logger, dll. Cukup cek goal+scope.

## 0. Cross-Project Detection

Kalau user bilang "aku mau kerja di project X" / "handle project ini" / sebut path project lain:

**Step 1 — Detect:**
- User mention path project lain (bukan farewell-orchestra)
- User bilang "project ini", "project X", "handle", "kerja di"

**Step 2 — Check Docs:**
```
glob <project>/docs/*.md
```

Cek 5 core docs + 2 conditional:

| Doc | Status | Cek |
|-----|--------|-----|
| PRD.md | **CORE** | WAJIB ada |
| Architecture.md | **CORE** | WAJIB ada |
| Rules.md | **CORE** | WAJIB ada |
| Tasks.md | **CORE** | WAJIB ada |
| Context.md | **CORE** | WAJIB ada |
| Schema.md | **CONDITIONAL** | Ada kalau project pakai database |
| API_Contract.md | **CONDITIONAL** | Ada kalau project pakai API |

**Step 3 — Decision:**
- Semua CORE ada → baca docs → pahami context → lanjut ke normal flow (§1 Input Validation)
- Ada yang hilang → **Reverse Engineering Mode** (§0.1)

### §0.1 Reverse Engineering Mode

Dispatch **researcher** untuk deep scan project:

**Phase 1 — Structure (5%)**
```
glob <project>/**/*.{ts,js,py,go,rs,java,tsx,jsx}
```
- Pahami folder layout
- Identifikasi entry points (index.ts, main.py, app.py, dll)
- Identifikasi config files (package.json, tsconfig, .env, docker-compose)

**Phase 2 — Config (10%)**
- Read package.json / requirements.txt / Cargo.toml / go.mod → tech stack
- Read tsconfig / vite.config / next.config → framework config
- Read .env.example / .env.local → environment variables
- Read docker-compose.yml / Dockerfile → deployment setup

**Phase 3 — Code Patterns (40%)**
- Read entry points → pahami routing, middleware, initialization
- Trace import chains → pahami dependency graph
- Read 2-3 representative files → infer naming conventions, error handling patterns
- Read database models / migrations → schema (kalau ada)
- Read API routes / controllers → endpoints (kalau ada)

**Phase 4 — Tests & Docs (20%)**
- Read existing tests → pahami test patterns, coverage
- Read README.md → pahami existing documentation
- Read CHANGELOG.md / HISTORY.md → project history (kalau ada)

**Phase 5 — Inference (25%)**
- Dari Phase 1-4, infer:
  - Tech stack (FE/BE/DB/Tools)
  - Architecture decisions
  - Coding conventions
  - Business logic patterns
  - API surface (kalau ada)
  - Database schema (kalau ada)

**Output: 5 Core Docs + 2 Conditional**

Dispatch **executor** untuk generate docs:

```
TASK: Generate 5 core docs + 2 conditional docs dari reverse engineering findings
FILES: <project>/docs/PRD.md, Architecture.md, Rules.md, Tasks.md, Context.md, [Schema.md], [API_Contract.md]
CONTEXT: Reverse engineering findings dari researcher
VERIFY: ls <project>/docs/ — semua core docs ada
```

**Consistency Rules:**
- Nama variabel/tabel di Schema.md = nama field di API_Contract.md
- Tech stack di Architecture.md = konvensi di Rules.md
- Fitur di PRD.md = task di Tasks.md

Setelah docs generated → baca docs → pahami context → lanjut ke normal flow (§1)

## 1. Input Validation

Cek request punya 4 elemen:

| Elemen | Wajib | Kalau kosong |
|--------|-------|-------------|
| **Goal** | YA | STOP. Tanya: "Goal-nya apa?" |
| **Scope** | YA | STOP. Tanya: "File/folder mana?" |
| **Acceptance** | YA | Usulkan 1 cara test, minta konfirmasi |
| **Risk** | Default LOW | Pakai LOW kalau tidak disebut |

**Trash detection** — STOP + clarify kalau:
- <10 kata tanpa konteks ("perbaikin", "tambahin")
- Ambigu multi-interpretasi ("benerin itu")
- Kontradiktif dalam satu request
- Scope liar ("refactor semuanya") tanpa batasan
- **Contradiction:** request sebelumnya bilang A, sekarang bilang B → flag: "Kontradiksi: [A] vs [B]. Mana yang benar?"
- **Wrong order:** request minta X sebelum Y padahal Y prerequisite X → flag: "Urutan salah: [Y] harus sebelum [X]?"
- **Terserah/terserah lo:** Boss bilang "terserah lo" → PARTIAL, force grill: "Gue butuh spesifik. Goal-nya apa?"
- **Impossible request:** request yang tidak feasible (prediksi masa depan, buat AGI) → HOLD: "Ini tidak feasible. Alternatif?"
- **Panic mode:** Boss panik, kasih info vague ("production down!", "cepetan!") → tanya spesifik: "Error apa? Gejalanya?"

**Explicit Checks (WAJIB untuk LLM):**

| Check | Trigger | Action |
|-------|---------|--------|
| Dependency check | Request mention "depends on", "requires", "needs" | Cek apakah dependency ada. Tidak ada → HOLD |
| Constraint check | Request mention "jangan ubah", "tetap", "keep" | Catat constraint. Violation = BLOCKING |
| Scope check | Request mention "cuma", "hanya", "only" | Catat scope limit. Exceed = BLOCKING |
| Test check | Request mention "test", "verify", "pastikan" | Executor WAJIB verify. Skip = BLOCKING |

**Output decision:**
- `HOLD [alasan]` → STOP. Tanya Boss.
- `PARTIAL` → lanjut ke §2 Assumption Logger, lalu §3 Grill.
- `PASS [SIZE]` → lanjut ke §4 Task Chunking.

Size: TRIVIAL (1 file, ≤3 baris) / SMALL (1-2 files) / MEDIUM (3-5 files) / LARGE (>5 files)

## 2. Assumption Logger

Hanya kalau PARTIAL. Auto-generate asumsi implisit, max 3:

```
Asumsi:
1. [asumsi 1] — ok?
2. [asumsi 2] — ok?
```

Boss reply `1:ya 2:tidak → pakai X` atau `semua ok`.

**Rubber-stamp guard:** Kalau Boss bilang "ok" ke semua asumsi tanpa edit → flag: "Asumsi belum dikonfirmasi. Konfirmasi 1 per 1?" Jangan lanjut kalau asumsi belum benar-benar dikonfirmasi.

## 3. Requirement Extraction (Grill)

Hanya kalau PARTIAL setelah Assumption Logger. Interview Boss satu pertanyaan per waktu:

| Level | Pertanyaan |
|-------|-----------|
| Goal | Apa yang mau dicapai? |
| Scope | Batasan? In/Out? |
| Constraints | Tech stack? Deadline? |
| Acceptance | Gimana tau selesai? |
| Risk | Apa yang bisa gagal? |
| Edge cases | Input kosong? Concurrent? |

Satu `question` tool call = satu pertanyaan. Max 8 pertanyaan, lalu sign-off paksa dengan asumsi default.

**Pendulum Check:** Over-spec (10 library, 5 pattern) → tanya "Prioritas?". Under-spec (terlalu umum) → paksa "Contoh input/output?"

## 4. Task Chunking

Trigger chunk kalau: **Q≥3** (pertanyaan) ATAU **F≥3** (file) ATAU **O≥2** (format output).

| Size | Action | Chunk Strategy |
|------|--------|----------------|
| TRIVIAL/SMALL | 1 chunk, fan-out normal | — |
| LARGE (F=3-10) | 2-3 chunk | Per module/feature, ≤3 file per chunk |
| MASSIVE (F>10) | 3-4 chunk | Per layer (FE/BE/DB), ≤3 file per chunk |

Per chunk: ≤3 file, 1 fokus, 1 format. **DALAM chunk:** parallel. **ANTAR chunk:** sequential dengan CONTEXT_SUMMARY.

**Sampling strategy untuk F>50 (large codebase):**
1. Prioritaskan: entry points → core modules → config → tests
2. Max 20 file per chunk, fokus ke file yang relevan dengan task
3. Skip: node_modules, dist, build, vendor, .git

Sub-agent boleh return `[CHUNK_REQUIRED]` kalau task kegedean → re-chunk, bukan gagal.
