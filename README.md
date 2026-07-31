# Farewell Orchestra

**4-agent AI orchestration system** — Tech Lead, Developer, Detective, Auditor. Satu tim, satu suara.

Dibangun di atas [OpenCode](https://opencode.ai) via [9Router](http://127.0.0.1:20128). Foreground-only, deny-by-default. Input sampah ditolak di gerbang.

## Quick Start

```bash
profiles\switch.bat              # double-click → menu → pilih profile
opencode
```

Cross-project: `"kerjain project ini <path>"` — orchestra auto-detect dan kerja di folder target. Lihat `.opencode/project-guide.md`.

## Agent Architecture

| Agent | Persona | Skills | Role |
|-------|---------|--------|------|
| **Orchestrator** | Tech Lead galak | `anti-gigo` `grill` `orchestrate` | Validasi input, dekomposisi, fan-out, delegasi |
| **Researcher** | Detektif eksploratif | `forensic` `web-research` | Cross-file tracing, deep debugging, web research |
| **Reviewer** | Auditor kejam | `stride-audit` | STRIDE threat model, convention enforcement |
| **Executor** | Developer minimalis | `minimal-impl` `verification-ground-truth` | Satu-satunya writer — YAGNI-first, verify-first |

Flow: Boss → Orchestrator (validate + decompose) → Researcher + Reviewer (parallel read-only) → Orchestrator (synthesize) → Executor (implement). Executor gagal 2x → Researcher deep debug. Satu-satunya agent dengan izin edit/bash adalah Executor.

## Skills

Setiap agent punya skill spesifik yang auto-discovered oleh OpenCode dari `.opencode/skills/`.

### Orchestrator Skills
| Skill | Fungsi |
|-------|--------|
| `anti-gigo` | Validasi input — tolak request sampah sebelum diproses |
| `grill` | Interview Boss — gali detail kalau input ambigu |
| `orchestrate` | Decompose task → fan-out parallel → synthesize hasil |
| `bootstrap-project` | Generate 10 dokumen project dari ide (PRD, Architecture, dll) |

### Researcher Skills
| Skill | Fungsi |
|-------|--------|
| `forensic` | Cross-file tracing, deep debug, evidence-first file:line |
| `web-research` | Cek docs, API status, library version, pricing — external fact-check |

### Reviewer Skills
| Skill | Fungsi |
|-------|--------|
| `stride-audit` | STRIDE threat model, convention enforcement, [BLOCKING] gate |

### Executor Skills
| Skill | Fungsi |
|-------|--------|
| `minimal-impl` | YAGNI-first, verify-first, anti over-engineering |
| `verification-ground-truth` | Verify claim vs actual tool output sebelum report done |

## Structure

.
├── AGENTS.md                  — orchestrator rules & workflow
├── .env.example               — env template
├── .gitignore
├── .opencode/
│   ├── agents/                — agent persona definitions (4 agent)
│   ├── command/               — slash commands (/work-on, /new-project, /check, /status)
│   ├── hooks/                 — lifecycle hooks (pre/post generate)
│   ├── .opencode/LESSONS.md             — session lessons log
│   ├── .opencode/project-guide.md       — cross-project usage guide
│   ├── scripts/               — utility scripts (link checker)
│   ├── skills/                — 9 agent skills (auto-discovered)
│   └── tools/                 — custom tools (harness_status, learn, verify)
├── profiles/
│   ├── generate.py            — profile generator
│   ├── profiles.json          — model registry (6 profiles)
│   └── switch.bat             — interactive profile switcher
├── templates/
│   └── sub-project.md         — sub-project anchor template
└── tests/
    └── test_generate.py       — profile generator test suite

MIT