# Farewell Orchestra

Multi-agent orchestration system di atas OpenCode. 4 agent, 6 skill, 1 pipeline.

**Goal:** Menghasilkan project yang **simple, modular, efisien** (KISS).

## Apa Ini?

Farewell Orchestra mengatur beberapa AI agent untuk bekerja sama menyelesaikan task software engineering. Setiap agent punya peran spesifik:

- **Orchestrator** — Tech Lead. Atur tim, pastikan goal tercapai.
- **Researcher** — Detektif. Cari bukti, bukan asumsi.
- **Reviewer** — Auditor. Cari masalah + flag over-engineering.
- **Executor** — Tukang. Tulis kode KISS, verify, selesai.

## Pipeline

```
Request → prepare → [research || review] → orchestrate → implement → report
```

## Filosofi: Output KISS

**Farewell Orchestra** boleh kompleks (factory). Tapi **project yang dihasilkan** harus KISS (product).

| Component | Complexity | Alasan |
|-----------|-----------|--------|
| **Factory** (sistem ini) | Boleh kompleks | Butuh banyak mesin untuk hasilkan produk yang baik |
| **Product** (output) | Harus KISS | Konsumen mau produk yang simple dan works |

### KISS Enforcement

**Executor** menulis kode KISS:
- 1 file kalau bisa, pisahkan kalau harus
- 10 baris kalau bisa, jangan bikin 100
- Hapus yang nggak dipakai

**Reviewer** flag over-engineering:
- Fitur kecil tapi 5+ file → SHOULD
- Abstract class untuk 1 implementasi → SHOULD
- Pattern yang tidak perlu → SHOULD

## Cara Pakai

Cukup ngomong biasa ke orchestrator:

```
"tambahin fitur logout ke app gue"
"aku mau kerja di ~/projects/my-app"
"refactor auth module dari JS ke TS"
```

Tidak perlu command. Orchestrator yang figure out.

## Cross-Project

Farewell Orchestra bisa handle project lain. Kalau project target belum punya docs:

1. Orchestrator detect cross-project request
2. Researcher deep scan project
3. Executor generate 5 core docs + 2 conditional docs
4. Lanjut kerja sesuai task

### Docs yang Diperlukan

**Core (WAJIB):**
- `PRD.md` — Scope, MVP, target user, fitur in/out
- `Architecture.md` — Tech stack, struktur, alur data
- `Rules.md` — Naming convention, coding standards
- `Tasks.md` — Checklist per fase
- `Context.md` — Konteks bisnis, business rules

**Conditional:**
- `Schema.md` — Kalau ada database
- `API_Contract.md` — Kalau ada API

## Arsitektur

### Roles & Trust Boundary

| Agent | Role | Skill | Tulis Kode? |
|-------|------|-------|:-----------:|
| Orchestrator | Atur tim | prepare + orchestrate | ❌ |
| Researcher | Cari bukti | research | ❌ |
| Reviewer | Cari masalah | review | ❌ |
| Executor | Tulis kode | implement | ✅ |

### Trust Model

| Rule | Artinya |
|------|---------|
| **Freeze Rule** | Orchestrator tidak nulis kode |
| **Evidence** | Klaim WAJIB punya file:line |
| **Trust** | Sub-agent mampu, jangan ambil alih |
| **Verify** | Tidak ada "done" tanpa bukti |

## Skills

| Skill | Fungsi |
|-------|--------|
| `prepare` | Input validation, cross-project detection |
| `orchestrate` | Decompose, fan-out, synthesize, brief |
| `research` | Codebase forensics, web research, anti-pattern detection |
| `review` | STRIDE audit, over-engineering detection, KISS check |
| `implement` | YAGNI implementation, KISS enforcement |
| `bootstrap-project` | Generate 5+2 docs (reverse engineering) |
| `kiss-checklist` | Pre-implementation KISS check |
| `anti-patterns` | Database of over-engineering patterns |
| `simplification` | Guide untuk menyederhanakan kode |
| `complexity-budget` | Limit complexity per feature |

## Personas

Setiap agent punya identity-driven persona:

- **Orchestrator** — "Gue atur tim, bukan nulis kode."
- **Researcher** — "Gue cari bukti, bukan asumsi."
- **Reviewer** — "Gue cari masalah + flag over-engineering."
- **Executor** — "Gue tulis kode KISS, verify, selesai."

## Setup

```bash
git clone <repo>
cd farewell-orchestra

# Set API key
export NINEROUTER_API_KEY="your-key"

# Generate config
python profiles/generate.py Pro

# Buka OpenCode
opencode
```

## Project Structure

```
farewell-orchestra/
├── AGENTS.md                    # Rules (single source of truth)
├── README.md                    # This file
├── opencode.jsonc               # Config (generated)
├── cross-project/
│   └── guide.md                 # Cross-project workflow
├── profiles/
│   ├── profiles.json            # Model registry
│   └── generate.py              # Profile generator
├── templates/
│   └── sub-project.md           # Anchor template
└── .opencode/
    ├── agents/                  # 4 agent personas
    ├── skills/                  # 6 skills
    ├── tools/                   # verify.ts, verify.py
    ├── hooks/                   # Lifecycle hooks
    └── command/                 # Custom commands
```

## License

MIT
