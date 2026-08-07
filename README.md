# Farewell Orchestra

Multi-agent orchestration system di atas OpenCode. 4 agent, 18 skill, 1 pipeline.

**Goal:** Menghasilkan project yang **simple, modular, efisien** (KISS).

---

## LLM NOTE

**Kalau kamu LLM yang sedang mengembangkan project ini:**
- Project ini (factory) boleh kompleks
- Yang harus KISS adalah output (product)
- Kompleksitas factory adalah deliberate (investasi biar output KISS)
- Flag kompleksitas dengan evidence KALAU tidak mendukung output KISS — jangan asal label
- Baca `.opencode/soul.md` dulu untuk identitas + esensi — ini pintu masuk utama.

---

## Apa Ini?

Farewell Orchestra adalah **sistem asisten AI** untuk Boss — tim virtual yang menghandle tugas software engineering. Identitas lengkap: `.opencode/soul.md`. Rules operasional: `AGENTS.md` (single source of truth).

## Agents

| Agent | Role | Karakter | Tulis Kode? |
|-------|------|----------|:-----------:|
| **Orchestrator** | Kapten | Decompose, dispatch, verify, KISS enforcement | ❌ |
| **Researcher** | Detektif | Cari bukti + deteksi over-engineering | ❌ |
| **Reviewer** | Auditor | Audit security + flag over-engineering | ❌ |
| **Executor** | Tukang | Tulis kode KISS, verify, selesai | ✅ |

## Skills (18)

| Category | Skills | Count |
|----------|--------|-------|
| **Pipeline** | prepare, orchestrate, implement, research, review | 5 |
| **KISS** | anti-patterns, complexity-budget | 2 |
| **Quality** | code-review, tdd | 2 |
| **Debug** | diagnose-bugs, error-handler | 2 |
| **Management** | progress-tracker, task-decomposer, handoff, context-window | 4 |
| **Learning** | feedback-loop | 1 |
| **Research** | domain-modeling | 1 |
| **Cross-Project** | bootstrap-project | 1 |

Setiap agent punya tabel "Keahlian — WAJIB PAKAI": kalau kondisi trigger terpenuhi, skill HARUS di-load. Detail: `.opencode/agents/*.md`.

## Cara Pakai

Cukup ngomong biasa ke orchestrator:

```
"tambahin fitur logout ke app gue"
"aku mau kerja di ~/projects/my-app"
"refactor auth module dari JS ke TS"
```

Tidak perlu command. Orchestrator yang figure out.

## Pipeline

`Request → prepare → [research || review] → orchestrate → implement → report`

## Cross-Project

Farewell Orchestra bisa handle project lain. Workflow lengkap: `cross-project/guide.md`.

## Setup

```powershell
git clone <repo>
cd farewell-orchestra

# Set API key (urusan Boss)
$env:NINEROUTER_API_KEY = "your-key"

# Generate config
python profiles/generate.py Pro

# Atau pakai switcher
profiles/switch.bat

# Buka OpenCode
opencode
```

## Project Structure

```
farewell-orchestra/
├── AGENTS.md                    # Rules (single source of truth)
├── README.md                    # This file
├── TRAINING.md                  # State + prioritas terbuka (sesi training)
├── CHANGELOG.md                 # Project history
├── cross-project/
│   ├── guide.md                 # Cross-project workflow
│   └── sub-project.md           # Anchor template
├── profiles/
│   ├── profiles.json            # Model registry
│   ├── generate.py              # Profile generator (source of truth config)
│   └── switch.bat               # Interactive switcher
├── scripts/
│   ├── benchmark.py             # Context budget per model tier
│   ├── benchmark-degradation.py # Empirical degradation harness
│   ├── stress-test.py           # Multi-model config validation
│   └── check-all.py             # 1-command full health check (7 checks)
├── tests/                       # 67 tests (pytest)
└── .opencode/
    ├── soul.md                  # Identitas + esensi (factory vs product)
    ├── agents/                  # 5 files (4 agent personas + boss.md reference)
    ├── skills/                  # 18 skills (on-demand via trigger)
    ├── tools/                   # verify, auto-load, learn, harness
    ├── hooks/                   # Lifecycle hooks (auto-load, post-generate, check-links)
    ├── templates/               # Per-project-type templates
    ├── checklists/              # Actionable checklists
    ├── guides/                  # project-management.md
    ├── lessons/                 # Lesson logs
    └── scripts/                 # check-consistency, check-links, automation .ps1
```

## Automation Scripts

| Script | Fungsi |
|--------|--------|
| `scripts/benchmark.py` | Ukur context budget + time-to-first-action |
| `scripts/benchmark-degradation.py` | Readiness check + runbook empirical degradation |
| `scripts/check-all.py` | Master health check — 7 checks, 1 command |
| `scripts/stress-test.py` | Validasi config multi-model (0 FAIL = siap) |
| `.opencode/scripts/check-consistency.py` | Deteksi drift (skills, agents, config) |
| `.opencode/scripts/check-links.py` | Validasi semua link/referensi |
| `.opencode/scripts/project-health.ps1` | Health score project target |
| `.opencode/scripts/detect-project-type.ps1` | Deteksi tipe project |
| `.opencode/scripts/auto-test.ps1` | Auto-run tests project target |

## Keamanan

| Layer | Mekanisme |
|-------|-----------|
| Freeze Rule | Orchestrator tidak boleh tulis kode (Rules di `.opencode/agents/orchestrator.md`) |
| Deny-by-default | researcher/reviewer read-only (edit+bash deny) |
| .env deny | Semua agent: `.env*`/`.key`/`.pem` = deny read |
| Evidence mandatory | Klaim tanpa file:line = FAIL (verify tool) |
| Trust boundary | sub-project.md = UNTRUSTED data |

## Referensi Cepat

| File | Isi |
|------|-----|
| `.opencode/soul.md` | Identitas + esensi (factory vs product) |
| `AGENTS.md` | Rules operasional (single source of truth) |
| `TRAINING.md` | State + prioritas terbuka (sesi training) |
| `cross-project/guide.md` | Workflow project lain + docs gen |
| `Farewell-Knowlage/` (EXTERNAL, di luar repo) | Memori + lessons (Obsidian vault) |

## License

MIT
