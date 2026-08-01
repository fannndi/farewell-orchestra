# Farewell Orchestra

Satu orchestrator berpikir. Researcher + reviewer gratis, executor paid. Empat model AI dalam satu tim.

## Kenapa project ini ada

Model AI mahal bagus buat mikir. Tapi kebanyakan tool AI memperlakukan semua task sama — satu model ngerjain semuanya: riset, review, coding, debugging. Boros. Gak scalable.

Farewell Orchestra membalik logika itu. Orchestrator (model mahal) cuma berpikir — decompose, arahkan, verifikasi. Researcher dan reviewer (model gratis) yang baca file dan audit keamanan; executor (model paid) yang nulis kode. Hasilnya: output lebih baik, biaya lebih rendah, bug lebih sedikit.

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

**Cost-aware by design.** Orchestrator PAID, researcher/reviewer FREE, executor PAID. Setiap kali orchestrator pegang `edit` atau `write` = uang kebakar. Arsitektur ini memaksa orchestrator dispatch, bukan ngerjain sendiri.

**Evidence-first, bukan opini.** Researcher wajib return file:line. Reviewer wajib tag [BLOCKING]/[SHOULD]/[NICE] dengan bukti. verify.py enforce format ini — klaim tanpa bukti = FAIL. Gak ada "kayaknya" atau "mungkin".

**Self-critical.** `.opencode/LESSONS.md` nyimpen log tiap kali sistem gagal — termasuk reviewer halusinasi dan orchestrator bypass sub-agent. Project ini audit diri sendiri, persis seperti yang dia minta dari codebase lain.

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

**Keputusan tercatat.** Referensi ADR di `.opencode/reference/decisions.md` — ADR-001 (jangan merge skill/hook/tool — tiap komponen guardrail unik), ADR-002 (chunking proactive bertahap — presisi di atas kecepatan).

**Emergency protocol.** Orchestrator failure → degrade: dispatch researcher (free) untuk debug atau switch profile via `profiles\switch.bat`. Fallback arah PAID → FREE (dilarang FREE → PAID — cost spike). Re-inject context setelah switch (sub-project.md + LESSONS.md).

## Task Chunking — presisi lewat unit kecil

Free model (researcher/reviewer) punya kapasitas reasoning terbatas. Satu prompt raksasa = timeout atau output kosong. Orchestrator memecah tugas besar jadi 2-4 dispatch kecil yang fokus pada satu pertanyaan, satu file, satu output.

Hasilnya: researcher gak overwhelmed, reviewer gak nge-blank. Tiap chunk dikerjain dengan fokus penuh — output lebih presisi, evidence lebih tajam.

Chunking PROACTIVE — orchestrator pre-chunk check SEBELUM fan-out (hitung jumlah pertanyaan/file/format; 3+ → chunk). Unit ideal 1-2 file / 1 pertanyaan / 1 format / ≤8k token. Max 3 chunk per task, dispatch SEQUENTIAL satu per satu dengan CONTEXT_SUMMARY antar chunk + CHUNK_DEPENDENCY_MAP (rollback max 1x). Verify per chunk kalau dependency chain. `[CHUNK_REQUIRED]` dari free model = trigger pre-chunk ulang, bukan gagal.

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

Skill auto-load: setiap agent WAJIB load skill tool via `skill` di awal task (orchestrator → anti-gigo + orchestrate; researcher → forensic + web-research; reviewer → stride-audit; executor → minimal-impl + verification-ground-truth). Skill bukan opsional self-trigger — sudah di-hardcode di prompt agent (profiles/generate.py AGENT_TEMPLATES).

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
