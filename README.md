# Farewell Orchestra

Multi-agent orchestration system di atas OpenCode. 4 agent, 6 skill, evidence-first pipeline.

## Overview

Farewell Orchestra mengatur beberapa AI agent untuk bekerja sama menyelesaikan task software engineering. Setiap agent punya peran spesifik dan trust boundary yang ketat.

```
Request → prepare → [research || review] → orchestrate → implement → report
```

## Architecture

| Agent | Role | Skill | Boleh Tulis Kode? |
|-------|------|-------|:-----------------:|
| **Orchestrator** | Decompose, dispatch, verify, report | prepare + orchestrate | ❌ |
| **Researcher** | Investigasi codebase + web | research | ❌ |
| **Reviewer** | STRIDE audit + convention enforcement | review | ❌ |
| **Executor** | Implementasi kode | implement | ✅ |

### Trust Model

- **Freeze Rule** — Orchestrator tidak pernah menulis kode
- **Evidence Standard** — Setiap klaim WAJIB punya `file:line`
- **Trust Boundary** — Sub-agent mampu, jangan ambil alih kerjaan mereka
- **Verify Gate** — Tidak ada "done" tanpa verifikasi

## Cara Pakai

Cukup ngomong biasa ke orchestrator:

```
"tambahin fitur logout ke app gue"
"aku mau kerja di ~/projects/my-app"
"refactor auth module dari JS ke TS"
```

Tidak perlu command. Orchestrator yang figure out.

## Cross-Project Workflow

Farewell Orchestra bisa handle project lain. Kalau project target belum punya docs:

1. Orchestrator detect cross-project request
2. Researcher deep scan project (structure, config, code patterns)
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

## Skills

| Skill | Fungsi |
|-------|--------|
| `prepare` | Input validation, cross-project detection, task chunking |
| `orchestrate` | Decompose, fan-out, synthesize, brief executor |
| `research` | Codebase forensics, web research |
| `review` | STRIDE threat model, convention enforcement, drift detection |
| `implement` | YAGNI implementation, verify before claim |
| `bootstrap-project` | Generate 5+2 docs (reverse engineering mode) |

## Personas

Setiap agent punya identity-driven persona — bukan cuma rules, tapi karakter.

- **Orchestrator** — Conductor. "Gue mikir, bukan ngetik."
- **Researcher** — Detektif. "Bukti atau nggak ngomong."
- **Reviewer** — Auditor. "Kode yang aman itu membosankan."
- **Executor** — Tukang. "Kode paling sederhana adalah kode yang nggak ditulis."

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
