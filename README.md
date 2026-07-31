# Farewell Orchestra

Satu orchestrator berpikir. Tiga agent gratis mengeksekusi. Empat model AI dalam satu tim.

## Kenapa project ini ada

Model AI mahal bagus buat mikir, bukan buat ngetik kode yang model gratisan juga bisa. Tapi kebanyakan tool AI memperlakukan semua task sama — satu model ngerjain semuanya: riset, review, coding, debugging. Boros. Gak scalable.

Farewell Orchestra membalik logika itu. Orchestrator (model mahal) cuma berpikir — decompose, arahkan, verifikasi. Researcher, reviewer, dan executor (model gratis) yang baca file, audit keamanan, dan nulis kode. Hasilnya: output lebih baik, biaya lebih rendah, bug lebih sedikit.

## Cara kerja

```
Boss kirim request
    │
    ▼
Orchestrator [PAID]       ← validasi input, decompose task, arahkan tim
    │
    ├── Researcher [FREE]  ← baca file, trace code, verifikasi klaim
    └── Reviewer [FREE]    ← audit STRIDE, cek konvensi, second opinion
    │       (parallel — barengan)
    ▼
Orchestrator [PAID]       ← synthesize temuan, brief executor
    │
    ▼
Executor [PAID]            ← nulis kode, edit file, implementasi
    │
    ▼
Boss terima report        ← 3 baris: what, result, residual risk
```

## Kenapa ini bekerja

**Cost-aware by design.** Orchestrator PAID, sub-agent FREE. Setiap kali orchestrator pegang `edit` atau `write` = uang kebakar. Arsitektur ini memaksa orchestrator dispatch, bukan ngerjain sendiri.

**Evidence-first, bukan opini.** Researcher wajib return file:line. Reviewer wajib tag [BLOCKING]/[SHOULD]/[NICE] dengan bukti. verify.py enforce format ini — klaim tanpa bukti = FAIL. Gak ada "kayaknya" atau "mungkin".

**Self-critical.** `.opencode/LESSONS.md` nyimpen log tiap kali sistem gagal — termasuk reviewer halusinasi dan orchestrator bypass sub-agent. Project ini audit diri sendiri, persis seperti yang dia minta dari codebase lain.

**Technical enforcement, bukan imbauan.** Permission researcher/reviewer read-only (gak bisa edit/bash). Orchestrator read dibatasi *.md doang — baca source code kena ask gate. Hook pre-generate validasi profiles.json. Bukan cuma instruksi di prompt.

**Satu otak, banyak project.** Buka opencode di repo ini, arahkan ke project target — orchestra kerja di sana. sub-project.md jadi anchor buat context antar sesi. Gak perlu setup ulang tiap project.

**KISS dari akar.** Root cuma 5 file. YAGNI di-enforce oleh minimal-impl skill. Anti-gigo tolak input sampah di gerbang. "Hapus lebih baik dari tambah" — prinsip yang dipake buat diri sendiri.

## Quick Start

```bash
profiles\switch.bat     # pilih profile → generate config
opencode                # mulai sesi
```

Cross-project: `"kerjain project ini <path>"` — orchestra auto-detect dan kerja di folder target.

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
| Reviewer | `stride-audit` | STRIDE threat model, convention enforcement |
| Executor | `minimal-impl` | YAGNI-first, verify-first, anti over-engineering |
| Executor | `verification-ground-truth` | Verify claim vs tool output — gak asumsi |

## Structure

```
.
├── AGENTS.md                  — orchestrator rules
├── .env.example
├── .gitignore
├── .opencode/
│   ├── agents/                — persona 4 agent
│   ├── command/               — slash commands
│   ├── hooks/                 — lifecycle enforcement
│   ├── LESSONS                 — self-audit log (.md)
│   ├── project-guide           — cross-project usage (.md)
│   ├── skills/                — 9 agent skills
│   └── tools/                 — verify, harness_status, learn
├── profiles/
│   ├── generate.py            — profile generator
│   ├── profiles.json          — 6 model profiles
│   └── switch.bat             — interactive switcher
├── templates/
│   └── sub-project.md         — project anchor template
└── tests/
    └── test_generate.py       — 18 tests, 0 gagal
```

MIT
