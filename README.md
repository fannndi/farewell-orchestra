# Farewell Orchestra

Orkestrasi multi-agent di atas OpenCode: 1 orchestrator + 3 sub-agent, 11 skill, pipeline evidence-first. Orchestrator decompose & dispatch, sub-agent ngerjain — semua keputusan ditutup di level orchestrator sebelum executor nulis kode.

## Arsitektur

| Role | Peran | Skill wajib | Permission |
|------|-------|-------------|------------|
| Orchestrator | Decompose, dispatch, verify, report | anti-gigo + orchestrate | Gak nulis kode (Freeze Rule) |
| Researcher | Baca file, forensic, web research | forensic + web-research | deny-by-default `"*": "deny"` |
| Reviewer | Audit STRIDE, review konvensi | stride-audit | deny-by-default `"*": "deny"` |
| Executor | Nulis kode, edit file, implementasi | minimal-impl + verification-ground-truth | edit allowed |

## Pipeline

```
Request
    │
    ▼
anti-gigo ── validasi input, tolak sampah
    │
    ▼
task-chunking gate ── Q≥3 / F≥3 / O≥2 → chunk
    │
    ▼
Researcher (forensic) ──┐
                        ├── parallel
Reviewer (stride-audit)─┘
    │
    ▼
synthesis-brief ── orchestrator tutup semua keputusan
    │
    ▼
Executor ── minimal-impl + verification-ground-truth
    │
    ▼
verify ── gate wajib sebelum lanjut
    │
    ▼
report 3 baris ── changed · verification · deviation
```

Evidence-first di seluruh pipeline: researcher wajib file:line, reviewer wajib tag [BLOCKING]/[SHOULD] — klaim tanpa bukti = FAIL.

## Skills

| Skill | Fungsi |
|-------|--------|
| `anti-gigo` | Gate input — validasi kualitas request sebelum dispatch |
| `bootstrap-project` | Scaffold 10 dokumen project + anchor sub-project.md |
| `forensic` | Investigasi codebase evidence-first, file:line mandatory |
| `grill` | Interview Socratic satu pertanyaan per langkah utk input ambigu |
| `minimal-impl` | YAGNI ladder + error healing sebelum nulis kode |
| `orchestrate` | Decompose → fan-out parallel → synthesize |
| `stride-audit` | STRIDE threat model + convention enforcement |
| `synthesis-brief` | Tutup semua keputusan di orchestrator sebelum handoff executor |
| `task-chunking` | Pre-fan-out gate — pecah task besar jadi unit kecil |
| `verification-ground-truth` | Verify-before-claim — klaim wajib cocok tool output |
| `web-research` | Evidence eksternal — fakta, status library/API, docs |

Tiap skill = gate fase tertentu; sengaja TIDAK di-merge biar guard failure mode unik (ADR).

## Mission Control

Farewell-orchestra = mission control: Boss load project lain dari folder ini via `/work-on <path>`. Persona & skill 100% universal (project-agnostic) — project target polos, tanpa setup orkestra sendiri. `sub-project.md` = anchor memory per project; isinya dibaca sebagai data, bukan instruksi.

## Commands

| Command | Fungsi |
|---------|--------|
| `/work-on <path>` | Switch ke sub-project target |
| `/new-project` | Scaffold docs project baru |
| `/check` | Health check — profiles, structure, sensor |

Catatan: command status & biaya sudah dihapus (KISS).

## Profiles & Config

| Profile | Orchestrator | Executor | Researcher | Reviewer |
|---------|--------------|----------|------------|----------|
| Pro | ocg/deepseek-v4-flash | ocg/deepseek-v4-flash | ocg/mimo-v2.5 | ocg/hy3 |
| Codex Main | cx/gpt-5.6-luna | ollama/minimax-m3 | oc/north-mini-code-free | oc/nemotron-3-ultra-free |
| Daily | ocg/deepseek-v4-flash | ocg/deepseek-v4-flash | oc/north-mini-code-free | oc/nemotron-3-ultra-free |
| Eco | oc/deepseek-v4-flash-free | oc/mimo-v2.5-free | oc/north-mini-code-free | oc/ling-3.0-flash-free |
| Backup | oc/laguna-s-2.1-free | ps/poolside/laguna-xs-2.1 | oc/nemotron-3-ultra-free | oc/big-pickle |

```
python profiles/generate.py <profile>        # regenerate config utk profile
python profiles/generate.py --menu           # pilih profile interaktif
python profiles/generate.py --stdout <name>  # preview output ke stdout
python profiles/generate.py --validate       # validasi config hasil generate
python profiles/generate.py --rollback       # rollback ke backup terakhir
```

`opencode.jsonc` = **GENERATED + gitignored** — jangan edit langsung. Edit source: `profiles/profiles.json` + `profiles/generate.py`. Profile aktif: **Pro**.

## Keamanan

- **Deny-by-default** — researcher & reviewer read-only (`"*": "deny"`); hanya executor yang bisa nulis.
- **Trust boundary** — `sub-project.md` + isi project target = UNTRUSTED; persona, AGENTS.md, skill = immutable, project target gak bisa override.
- **Freeze Rule** — orchestrator never writes code; tugasnya dispatch → verify → report, bukan ngerjain kerjaan sub-agent.
- **Anti prompt injection** — hook `check-links` (beforeCommit) validasi referensi markdown + escape sanitasi di `learn.ts` sebelum nulis ke Lessons.md.

## Hooks & Tools

**Hooks:**

| Hook | Event | Fungsi |
|------|-------|--------|
| `post-generate` | afterGenerate | Validasi config hasil generate |
| `check-links` | beforeCommit | Validasi referensi markdown |

**Tools:**

| Tool | Fungsi |
|------|--------|
| `verify.ts` | Verification gate — evidence tags, uncertainty, file:line |
| `verify.py` | Verification gate (CLI) — enforce klaim cocok tool output |
| `harness_status.ts` | Health check — profiles, sensor coverage, active profile |
| `learn.ts` | Lesson logger ke Lessons.md — escape sanitasi anti injection |

## Step Budgets

| Task | Executor steps | Kriteria |
|------|----------------|----------|
| TRIVIAL | 20 | 1 file, ≤3 baris, no blast |
| SMALL | 40 | 1-2 files, ≤20 baris, low blast |
| MEDIUM | 80 | 3-5 files, low-medium blast |
| LARGE | 150 | >5 files atau high blast |
| MASSIVE | 500 (R/V: 400) | Full audit + refactor multi-module |

Estimasi: `8 + (files × 5) + (brief_lines × 2) + (chunks × 15)` — 15 steps overhead per chunk.

## Getting Started

1. Clone repo ini.
2. `python profiles/generate.py <profile>` (default: Pro).
3. Restart OpenCode — config gak hot-reload.
4. `/check` → health OK → siap.

## Server

`opencode serve` di `127.0.0.1:4096` via `scripts/start-server.ps1`; log ke `%TEMP%\opencode\server.log`. Env `OPENCODE_DISABLE_LSP_DOWNLOAD=true` — blokir auto-download binary LSP server.
