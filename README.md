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
| Orchestrator | .opencode/agents/orchestrator.md | anti-gigo + orchestrate | PAID |
| Researcher | .opencode/agents/researcher.md | forensic + web-research | FREE |
| Reviewer | .opencode/agents/reviewer.md | stride-audit | FREE |
| Executor | .opencode/agents/executor.md | minimal-impl + verification-ground-truth | PAID |

Skill di-hardcode di prompt via `profiles/generate.py` — bukan opsional self-trigger.

## Cost Model

| Role | Biaya | Alasan |
|------|-------|--------|
| Orchestrator | PAID | Reasoning tinggi — decompose, verify, dispatch |
| Researcher | FREE | Read-only — baca file, forensic, web search |
| Reviewer | FREE | Read-only — STRIDE audit, convention check |
| Executor | PAID | Write access — kualitas implementasi kompetitif |

Catatan: label PAID/FREE = pembagian beban & peran (paid = reasoning tinggi untuk orchestrate/implement, free = read-only), bukan klaim harga model spesifik. Model aktual per profile: lihat `profiles/profiles.json`.

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
| `default` | ocg/deepseek-v4-flash | cx/gpt-5.6-luna |
| `mix` | cx/gpt-5.6-luna | ocg/hy3 |
| `low-cost` | ocg/hy3 | cx/gpt-5.6-luna |
| `free` | oc/deepseek-v4-flash-free | — |

Sumber kebenaran: `profiles/profiles.json`. Generator: `profiles/generate.py`. Switcher: `profiles/switch.bat`.

**Alur sync config (source → generated):**
- `opencode.jsonc` = **GENERATED + gitignored** — jangan edit langsung. Edit source di `profiles/profiles.json` / `profiles/generate.py`.
- Regenerate: `python profiles/generate.py "Daily"` (profile aktif).
- Restart opencode **WAJIB** setelah generate — config gak hot-reload.
- Sanity check: `python profiles/generate.py --validate`.

**4 profile, bukan 6.** Semua di-source-of-truth yang sama.

## Commands

| Command | Fungsi |
|---------|--------|
| `/work-on <path>` | Arahkan orchestra ke project target |
| `/new-project` | Buat project baru dari scratch |
| `/check` | Health check — validasi profiles.json, sensor coverage, active profile |

## Environment

- `OPENCODE_DISABLE_LSP_DOWNLOAD=true` — blokir auto-download binary LSP server (LSP tidak dipakai di orkestra ini, hemat bandwidth/disk).
- Set manual: `[Environment]::SetEnvironmentVariable("OPENCODE_DISABLE_LSP_DOWNLOAD","true","User")` (Windows) atau `export OPENCODE_DISABLE_LSP_DOWNLOAD=true` (Unix).

## Server Runbook

- Start: `powershell -File scripts/start-server.ps1` — jalankan `opencode serve` di `127.0.0.1:4096`, log ke `%TEMP%\opencode\server.log`.
- Attach: `opencode run --attach http://127.0.0.1:4096 --format json "Reply with exactly: OK"`.
- Stop: `powershell -File scripts/start-server.ps1 -Stop` — kill proses opencode serve.
- Security: bind `127.0.0.1` saja + password wajib (`OPENCODE_SERVER_PASSWORD`; kalau kosong script generate random 64-hex (32 bytes)).

## Debug Logging

Troubleshooting multi-agent (tool gagal, sub-agent output kosong, executor gagal 2x).

1. **Kapan aktifkan:** HANYA saat reproduce bug. Default cukup INFO — DEBUG bikin log membesar + berisiko bocor data.
2. **Cara aktifkan:** (a) `opencode --log-level DEBUG`, (b) env `OPENCODE_LOG_LEVEL=DEBUG`, (c) config `logLevel: "debug"`. Level: `debug`/`info`/`warn`/`error`/`none`.
3. **Lokasi log (Windows):** `%USERPROFILE%\.local\share\opencode\log\opencode.log` (file timestamped `.log`).
4. **Cara baca:** `Get-Content -Tail 100 "$env:USERPROFILE\.local\share\opencode\log\opencode.log" | Select-String "ERROR|WARN"` — fokus tool calls + error terakhir sebelum kegagalan.
5. **⚠️ Keamanan:** log berisi API key (`sk-...`, Bearer), path sensitif, isi konversasi — WAJIB redact sebelum share. Bersihkan setelah selesai: `Remove-Item "$env:USERPROFILE\.local\share\opencode\log\opencode.log"`.

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
│   ├── .opencode/project-guide.md  — cross-project usage guide
│   ├── skills/                — 11 agent skills
│   └── tools/                 — verify.ts, harness_status, learn
├── profiles/
│   ├── generate.py            — profile generator (SOURCE OF TRUTH)
│   ├── profiles.json          — 3 model profiles
│   └── switch.bat             — interactive profile switcher
├── templates/
│   └── sub-project.md         — project anchor template
└── tests/
    └── test_generate.py       — 20 tests, 0 gagal
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
