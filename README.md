# Farewell Orchestra

Satu orchestrator berpikir. Researcher + reviewer gratis, executor paid. Empat model AI dalam satu tim, diorkestrasi lewat OpenCode + 9router.

## Kenapa Project Ini Ada

Model AI mahal buat mikir — tapi kebanyakan tool treat semua task sama: satu model ngerjain semuanya. Boros, gak scalable.

Farewell Orchestra membalik logika itu:

- **Orchestrator** [PAID] — decompose, arahkan, verifikasi. Gak nulis kode.
- **Researcher** [FREE] — baca file, trace code, fact-check.
- **Reviewer** [FREE] — audit STRIDE, second opinion.
- **Executor** [PAID] — tulis kode, edit file, implementasi.

**Tech stack:** OpenCode (agent provider, hook lifecycle, verify gate, MCP) + 9router (model provider, routing free vs paid otomatis).

## Workflow

```
Boss kirim request
    │
    ▼
anti-gigo ── validasi input, tolak sampah
    │
    ▼
orchestrate ── task-chunking gate (mandatory sebelum fan-out)
    │
    ├── Researcher [FREE]  ── forensic + web-research → file:line evidence
    └── Reviewer  [FREE]  ── stride-audit → tag [BLOCKING]/[SHOULD]
    │       (parallel)
    ▼
synthesis-brief ── orchestrator tutup semua keputusan, executor hanya eksekusi
    │
    ▼
Executor [PAID] ── minimal-impl → verification-ground-truth
    │
    ▼
ping guard ── send "READY?" task sebelum dispatch; dead model → skip/escalate
    │
    ▼
Boss terima report ── 3 baris: what changed, verification result, residual risk
```

**Chunking (mandatory gate):** hitung jumlah pertanyaan (Q), file (F), output format (O). Kalau Q≥3 atau F≥3 atau O≥2 → CHUNK. Max 3 chunk per task. Dispatch sequential. `[CHUNK_REQUIRED]` dari free model = trigger re-chunk, bukan gagal.

## Persona-per-Role

| Role | Persona | Skill wajib | Model |
|------|---------|-------------|-------|
| Orchestrator | orchestrator.md | anti-gigo + orchestrate | PAID |
| Researcher | researcher.md | forensic + web-research | FREE |
| Reviewer | reviewer.md | stride-audit | FREE |
| Executor | executor.md | minimal-impl + verification-ground-truth | PAID |

Skill di-hardcode di prompt via `profiles/generate.py` — bukan opsional self-trigger.

## Cost Model

| Role | Biaya | Alasan |
|------|-------|--------|
| Orchestrator | PAID | Reasoning tinggi — decompose, verify, dispatch |
| Researcher | FREE | Read-only — baca file, forensic, web search |
| Reviewer | FREE | Read-only — STRIDE audit, convention check |
| Executor | PAID | Write access — kualitas implementasi kompetitif |

**Aturan emas:** Jangan pake model paid buat kerjaan yang model free bisa lakuin. Orchestrator pakai `edit`/`write` = uang kebakar → STOP, dispatch executor.

## Skills

| # | Skill | Guardrail |
|---|-------|-----------|
| 1 | `anti-gigo` | Gate input — tolak sampah sebelum diproses |
| 2 | `bootstrap-project` | Scaffold — generate 10 dokumen project dari ide |
| 3 | `forensic` | Codebase evidence — bukti file:line dari dalam repo |
| 4 | `grill` | Extraction — gali detail dari input ambigu |
| 5 | `minimal-impl` | YAGNI + error healing — anti over-engineering |
| 6 | `orchestrate` | Workflow — decompose → fan-out → synthesize |
| 7 | `stride-audit` | STRIDE threat model + convention enforcement |
| 8 | `synthesis-brief` | Orchestrator tutup keputusan, executor hanya eksekusi |
| 9 | `verification-ground-truth` | Verify-before-claim — klaim wajib cocok sama tool output |
| 10 | `web-research` | External evidence — fact-check dari luar repo |

11 skill, bukan 11 duplikat. Tiap skill guard phase/domain berbeda. Merge = separation hilang (ADR-001).

## Profiles

| Profile | Model | Fallback |
|---------|-------|----------|
| `default` | ocg (primary) | openrouter |
| `mix` | codex | ollama |
| `low-cost` | hy3 | mimo |

Sumber kebenaran: `profiles/profiles.json`. Generator: `profiles/generate.py`. Switcher: `profiles/switch.bat`.

**3 profile, bukan 6.** Semua di-source-of-truth yang sama.

## Commands

| Command | Fungsi |
|---------|--------|
| `/work-on <path>` | Arahkan orchestra ke project target |
| `/new-project` | Buat project baru dari scratch |
| `/check` | Health check — validasi profiles.json, sensor coverage, active profile |

## CBM (Codebase Memory)

CBM codebase-memory-mcp v0.9.0 dikonfigurasi sebagai MCP server — tersedia tapi **belum diintegrasikan** ke agent persona/skill manapun.

- **Researcher** pakai: forensic + web-research
- **Reviewer** pakai: stride-audit
- **CBM** → available via MCP tools untuk query manual kalau diperlukan

160k nodes indexed, 15 MCP tools, graph UI di localhost:9749.

## ADRs

| ADR | Keputusan |
|-----|-----------|
| ADR-001 | **Jangan merge skill/hook/tool** — tiap komponen guard failure mode unik. Merge = separation hilang. |
| ADR-002 | **Chunking proactive** — presisi di atas kecepatan. Chunk SEBELUM fan-out, bukan reaktif setelah gagal. |

Tercatat di `Farewell-Knowlage/Decisions.md`.

## Mission Control

Farewell-orchestra = mission control. Boss load project DARI SINI — project target tidak perlu setup orkestra sendiri.

- **Alur:** Boss bilang "kerjain X" → resolve path → cek registry → inject konteks → baca sub-project.md (trust boundary: UNTRUSTED) → orkestrasi normal
- **Cross-project:** `external_directory` scoped `~/projects/**` (least privilege). Auto-scaffold kalau sub-project.md missing
- **Emergency:** Orchestrator failure → degrade ke researcher (free) atau switch profile via `profiles\switch.bat`. Fallback: PAID → FREE (dilarang FREE → PAID)

## Structure

```
.
├── AGENTS.md                  — orchestrator rules + agent personas
├── .env.example
├── .gitignore
├── .opencode/
│   ├── agents/                — persona 4 agent
│   ├── command/               — slash commands
│   ├── hooks/                 — lifecycle enforcement (pre/post-generate)
│   ├── project-guide.md       — cross-project usage guide
│   ├── skills/                — 11 agent skills
│   └── tools/                 — verify.ts, harness_status, learn
├── profiles/
│   ├── generate.py            — profile generator (SOURCE OF TRUTH)
│   ├── profiles.json          — 3 model profiles
│   └── switch.bat             — interactive profile switcher
├── templates/
│   └── sub-project.md         — project anchor template
└── tests/
    └── test_generate.py       — 24 tests, 0 gagal
```

## Kenapa Ini Bekerja

- **Cost-aware by design** — orchestrator + executor paid, researcher + reviewer free. Arsitektur memaksa dispatch, bukan ngerjain sendiri.
- **Evidence-first** — researcher wajib file:line, reviewer wajib tag [BLOCKING]/[SHOULD]/[NICE]. verify.py enforce — klaim tanpa bukti = FAIL.
- **External audit rule** — findings butuh researcher verify + reviewer second opinion. Gak ada "kayaknya".
- **Technical enforcement** — permission read-only researcher/reviewer, hook validasi profiles.json, verify gate mandatory.
- **Self-critical** — `Lessons.md` nyimpen log tiap kali sistem gagal. Audit diri sendiri.
- **KISS dari akar** — root cuma 5 file. YAGNI di-enforce. "Hapus lebih baik dari tambah."
- **Satu otak, banyak project** — buka opencode di repo ini, arahkan ke target. Gak perlu setup ulang.

---

MIT
