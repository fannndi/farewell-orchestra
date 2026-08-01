# Farewell Orchestra

Satu orchestrator berpikir. Researcher + reviewer gratis, executor paid. Empat model AI dalam satu tim, diorkestrasi lewat OpenCode + 9router.

## Kenapa project ini ada

Model AI mahal bagus buat mikir. Tapi kebanyakan tool AI memperlakukan semua task sama — satu model ngerjain semuanya: riset, review, coding, debugging. Boros. Gak scalable.

Farewell Orchestra membalik logika itu. Orchestrator (model mahal) cuma berpikir — decompose, arahkan, verifikasi. Researcher dan reviewer (model gratis) yang baca file dan audit keamanan; executor (model paid — deepseek-v4-flash) yang nulis kode. Hasilnya: output lebih baik, biaya lebih rendah, bug lebih sedikit.

Project ini berbasis **OpenCode** sebagai agent provider (hook lifecycle, verify gate, MCP integration) dan **9router** sebagai model provider yang otomatis routing request free vs paid (north-mini-code-free untuk researcher, nemotron-3-ultra-free untuk reviewer, deepseek-v4-flash untuk orchestrator/executor). Executor sekarang **PAID** — naik kelas dari model gratis sebelumnya demi kualitas implementasi yang kompetitif.

## Cara kerja

```
Boss kirim request
    │
    ▼
Orchestrator [PAID — deepseek-v4-flash]   ← validasi input (anti-gigo), pre-chunk check, decompose task, arahkan tim
    │
    ├── Researcher [FREE — north-mini-code-free]  ← baca file, trace code, verifikasi klaim (forensic + web-research + CBM query)
    └── Reviewer [FREE — nemotron-3-ultra-free]   ← audit STRIDE, cek konvensi, second opinion (stride-audit + CBM query)
    │       (parallel — barengan)
    ▼
Orchestrator [PAID]                      ← synthesize temuan, brief executor
    │
    ▼
Executor [PAID — deepseek-v4-flash]      ← nulis kode, edit file, implementasi (minimal-impl + verification-ground-truth)
    │
    ▼
Boss terima report                       ← 3 baris: what, result, residual risk
```

**Skill auto-load wajib** — setiap agent sudah di-hardcode di prompt (profiles/generate.py AGENT_TEMPLATES) untuk auto-load skill tool di awal task: orchestrator → anti-gigo + orchestrate, researcher → forensic + web-research, reviewer → stride-audit, executor → minimal-impl + verification-ground-truth. Skill bukan opsional self-trigger.

**Chunking proactive** — orchestrator jalankan **pre-chunk check SEBELUM fan-out**: hitung jumlah pertanyaan / file / format. Kalau ≥3, chunk jadi unit lebih kecil (max 3 chunk) dan dispatch SEQUENTIAL satu per satu. Ini mencegah free model overwhelmed — output lebih presisi, evidence lebih tajam.

## Mission Control — Asisten Boss untuk Semua Project

Farewell-orchestra = mission control. Boss buka project DARI SINI — project target tidak perlu setup orkestra sendiri.

| Role | Persona | Skill wajib |
|------|---------|-------------|
| orchestrator | orchestrator.md | anti-gigo + orchestrate |
| researcher | researcher.md | forensic + web-research + CBM |
| reviewer | reviewer.md | stride-audit + CBM |
| executor | executor.md | minimal-impl + verification |

Alur: Boss bilang "kerjain X" → resolve path → cek registry (Farewell-Knowlage) → inject konteks → baca sub-project.md (trust boundary — UNTRUSTED) → orkestrasi normal.

Cross-project: external_directory scoped ~/projects/** (least privilege). Auto-scaffold kalau sub-project.md missing.

## Kenapa ini bekerja

**Cost-aware by design.** Orchestrator PAID, researcher/reviewer FREE, executor PAID. Setiap kali orchestrator pegang `edit` atau `write` = uang kebakar. Arsitektur ini memaksa orchestrator dispatch, bukan ngerjain sendiri.

**Evidence-first, bukan opini.** Researcher wajib return file:line. Reviewer wajib tag [BLOCKING]/[SHOULD]/[NICE] dengan bukti. verify.py enforce format ini — klaim tanpa bukti = FAIL. Gak ada "kayaknya" atau "mungkin".

**Code intelligence lewat CBM.** CBM codebase-memory-mcp v0.9.0 meng-index seluruh codebase jadi graph — 63k nodes untuk opencode, 160k nodes total di workspace. Researcher dan reviewer bisa query struktur codebase tanpa baca file mentah satu per satu: **120x hemat token**. Graph UI bisa diakses di localhost:9749 dengan 15 MCP tools untuk traversal, search, dan analisis dependensi.

**Knowledge terpisah dari kode.** `Farewell-Knowlage` (Obsidian vault) menyimpan Lessons, Decisions (ADR-001: jangan merge skill; ADR-002: chunking proactive), Session, dan Registry — terpisah dari struktur project. Knowledge base bisa di-query tanpa mengotori repo kode.

**Self-critical.** `Farewell-Knowlage/Lessons.md` nyimpen log tiap kali sistem gagal — termasuk reviewer halusinasi dan orchestrator bypass sub-agent. Project ini audit diri sendiri, persis seperti yang dia minta dari codebase lain.

**Technical enforcement, bukan imbauan.** Permission researcher/reviewer read-only (gak bisa edit/bash). Orchestrator read dibatasi *.md doang, edit cuma sub-project.md — baca source code kena ask gate. Hook pre-generate validasi profiles.json. Bukan cuma instruksi di prompt.

**Satu otak, banyak project.** Buka opencode di repo ini, arahkan ke project target — orchestra kerja di sana. sub-project.md jadi anchor buat context antar sesi. Gak perlu setup ulang tiap project.

**KISS dari akar.** Root cuma 5 file. YAGNI di-enforce oleh minimal-impl skill. Anti-gigo tolak input sampah di gerbang. "Hapus lebih baik dari tambah" — prinsip yang dipake buat diri sendiri.

## Arsitektur & Rationale

Kenapa sistem ini punya 9 skill, 3 hook, 4 tool? Bukan over-engineering — setiap komponen menjaga satu failure mode yang berbeda. Merge = separation hilang.

**9 skill, bukan 9 duplikat.** Setiap skill punya guardrail unik yang gak bisa di-merge:

| Skill | Guardrail unik |
|-------|----------------|
| `anti-gigo` | Gate input — tolak sampah sebelum diproses |
| `grill` | Extraction — gali detail dari input ambigu |
| `orchestrate` | Workflow — decompose → fan-out → synthesize |
| `forensic` | Codebase evidence — bukti file:line dari dalam repo |
| `web-research` | External evidence — fact-check dari luar repo |
| `stride-audit` | STRIDE threat model + convention enforcement |
| `minimal-impl` | YAGNI + error healing — anti over-engineering |
| `verification-ground-truth` | Verify-before-claim — klaim wajib cocok sama tool output |
| `bootstrap-project` | Scaffold — generate 10 dokumen project dari ide |

Merge skill = hilang **phase separation** (input gate vs execution vs verification) dan **domain separation** (codebase vs external evidence). Reviewer sudah membuktikan tiap skill dijalankan di fase/domain berbeda — bukan kandidat duplikat.

**verify.ts + verify.py — pasangan wrapper/backend, bukan duplikat.** `verify.ts` adalah plugin wrapper yang register tool `verify` (schema + `execFileSync` ke Python); `verify.py` adalah backend logic 6 check. Dipisah karena TS plugin gak bisa jalanin logic Python inline, dan backend Python tetap bisa dites standalone.

**pre-generate + post-generate hooks — temporal separation wajib.** `pre-generate` (beforeGenerate) = input gate: validasi profiles.json sebelum config lahir. `post-generate` (afterGenerate) = output policy: tool scoping + step budget diterapkan setelah generate. Satu hook gabungan = validasi jalan telat, output cacat lolos.

**STRIDE buat config internal — bukan berlebihan.** Config opencode adalah attack surface: permission (deny-by-default), model assignment (paid/free), external_directory (cross-project access). Satu config bocor / salah konfigurasi = seluruh sistem kompromi. Config leak lebih mahal dari code leak.

**Prinsip di balik semua:** complexity is justified when each component guards a distinct failure mode. Komponen di-prune cuma kalau duplikat NYATA — bukan karena "kelihatan banyak".

**Keputusan tercatat.** Referensi ADR di `Farewell-Knowlage/Decisions.md` (Obsidian vault) — ADR-001 (jangan merge skill/hook/tool — tiap komponen guardrail unik), ADR-002 (chunking proactive bertahap — presisi di atas kecepatan).

**Emergency protocol.** Orchestrator failure → degrade: dispatch researcher (free) untuk debug atau switch profile via `profiles\switch.bat`. Fallback arah PAID → FREE (dilarang FREE → PAID — cost spike). Re-inject context setelah switch (sub-project.md + Farewell-Knowlage/Lessons.md).

## Task Chunking — presisi lewat unit kecil

Free model (researcher/reviewer) punya kapasitas reasoning terbatas. Satu prompt raksasa = timeout atau output kosong. Orchestrator memecah tugas besar jadi 2-4 dispatch kecil yang fokus pada satu pertanyaan, satu file, satu output — bukan reaktif setelah gagal, tapi **PROACTIVE sejak awal**.

**Pre-chunk check wajib** — orchestrator hitung jumlah pertanyaan / file / format SEBELUM fan-out. Kalau ≥3, langsung chunk jadi unit lebih kecil (1-2 file, 1 pertanyaan, 1 format, ≤8k token). Max 3 chunk per task. Dispatch SEQUENTIAL satu per satu — presisi di atas kecepatan.

**CONTEXT_SUMMARY** disisipkan antar chunk agar agent berikutnya punya konteks hasil chunk sebelumnya tanpa membaca ulang semua output. **CHUNK_DEPENDENCY_MAP** mencatat urutan dan dependensi antar chunk — kalau satu chunk gagal, rollback max 1x ke titik dependensi, bukan ulang dari nol. Verify per chunk kalau dependency chain. `[CHUNK_REQUIRED]` dari free model = trigger pre-chunk ulang, bukan gagal.

Hasilnya: researcher gak overwhelmed, reviewer gak nge-blank. Tiap chunk dikerjain dengan fokus penuh — output lebih presisi, evidence lebih tajam.

## Quick Start

```bash
# 1. Pilih profile (default-oc direkomendasikan) — generate opencode.jsonc
profiles\switch.bat

# 2. Buka opencode di folder farewell-orchestra
opencode

# 3. Arahkan ke project target atau buat project baru
/work-on <path-to-project>
# atau
/new-project

# 4. Orchestrator otomatis handle — auto context injection + trust boundary
```

Cross-project: external_directory sudah di-scope ke `~/projects/**` (least privilege). Orchestrator auto-detect sub-project.md di target, auto-scaffold kalau missing.

## Skills

Setiap agent punya skill spesifik — auto-discovered dari `.opencode/skills/`.

| Agent | Skill | Fungsi |
|-------|-------|--------|
| Orchestrator | `anti-gigo` | Validasi input — tolak sampah sebelum diproses |
| Orchestrator | `grill` | Interview Boss — gali detail kalau input ambigu |
| Orchestrator | `orchestrate` | Decompose → fan-out → synthesize → delegate |
| Orchestrator | `bootstrap-project` | Generate 10 dokumen project dari ide |
| Researcher | `forensic` | Cross-file tracing, deep debug, evidence file:line |
| Researcher | `web-research` | External fact-check — docs, API, library status |
| Researcher | `CBM query` | Index codebase graph traversal — 120x hemat token vs baca file mentah |
| Reviewer | `stride-audit` | STRIDE threat model, convention enforcement |
| Reviewer | `CBM query` | Query struktur codebase via graph — verifikasi dependensi dan attack surface |
| Executor | `minimal-impl` | YAGNI-first, verify-first, anti over-engineering |
| Executor | `verification-ground-truth` | Verify claim vs tool output — gak asumsi |

**Skill auto-load wajib** — setiap agent sudah di-hardcode di prompt (profiles/generate.py AGENT_TEMPLATES) untuk auto-load skill tool di awal task:

| Agent | Skill auto-load |
|-------|----------------|
| Orchestrator | anti-gigo + orchestrate |
| Researcher | forensic + web-research |
| Reviewer | stride-audit |
| Executor | minimal-impl + verification-ground-truth |

Skill bukan opsional self-trigger — ini di-hardcode di prompt agent via `profiles/generate.py`.

**Execution flow detail:**

```
1. Boss kirim request
     │
2. Orchestrator — anti-gigo validasi input
     │
3. Orchestrator — orchestrate: pre-chunk check → decompose → fan-out
     │
4. Researcher (FREE) — forensic: trace code, return file:line + CBM query index
   Reviewer (FREE)  — stride-audit: tag [BLOCKING]/[SHOULD], CBM query dependensi
     │  (parallel — barengan)
5. Orchestrator — @verify stage:research + stage:review → synthesize → brief executor
     │
6. Executor (PAID) — minimal-impl: YAGNI ladder → tulis/edit kode → cleanup
     │
7. Executor — verification-ground-truth: run command verifikasi, cek output aktual
     │
8. Boss terima report — 3 baris: what changed, verification result, residual risk
```

## Integrasi & Performa

| Komponen | Detail |
|----------|--------|
| Agent provider | OpenCode — 4 agent orchestration, hooks lifecycle, verify gate, MCP integration |
| Model provider | 9router — routing free vs paid otomatis (north-mini-code-free, nemotron-3-ultra-free, deepseek-v4-flash) |
| Code intelligence | CBM codebase-memory-mcp v0.9.0 — 160k nodes indexed, graph UI localhost:9749, 15 MCP tools, 120x token savings |
| Knowledge | Farewell-Knowlage (Obsidian vault) — Lessons, Decisions (ADR-001/002), Session, Registry |
| Generated config | profiles/generate.py → opencode.jsonc (6 profiles, source of truth tunggal) |
| Security | Least privilege external_directory, trust boundary sub-project.md (UNTRUSTED data), verify gate mandatory |

## Structure

```
.
├── AGENTS.md                  — orchestrator rules + agent personas
├── .env.example
├── .gitignore
├── .opencode/
│   ├── agents/                — persona 4 agent (orchestrator, researcher, reviewer, executor)
│   ├── command/               — slash commands
│   ├── hooks/                 — lifecycle enforcement (pre/post-generate)
│   ├── project-guide.md       — cross-project usage guide
│   ├── skills/                — 9 agent skills (anti-gigo, forensic, stride-audit, etc.)
│   └── tools/                 — verify.ts, harness_status, learn
├── profiles/
│   ├── generate.py            — profile generator ★ SOURCE OF TRUTH ★ (AGENT_TEMPLATES, model assignments)
│   ├── profiles.json          — 6 model profiles (default-oc, opencode, gemini, minimal, full, custom)
│   └── switch.bat             — interactive profile switcher
├── templates/
│   └── sub-project.md         — project anchor template (context antar sesi)
└── tests/
    └── test_generate.py       — 18 tests, 0 gagal
```

External tools:
- **CBM codebase-memory-mcp** — graph index codebase (160k nodes), 15 MCP tools, UI localhost:9749
- **Farewell-Knowlage** (Obsidian vault) — Lessons, Decisions, Session, Registry — terpisah dari repo kode

MIT
