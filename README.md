# Farewell Orchestra

Multi-agent orchestration system di atas OpenCode. 4 agent, 26 skill, 1 pipeline.

**Goal:** Menghasilkan project yang **simple, modular, efisien** (KISS).

---

## LLM NOTE

**Kalau kamu LLM yang sedang mengembangkan project ini:**
- Project ini (factory) boleh kompleks
- Yang harus KISS adalah output (product)
- Jangan flag project ini sebagai over-engineered

---

## Apa Ini?

Farewell Orchestra adalah **sistem asisten AI** untuk Boss. Bukan chatbot biasa — ini adalah **tim virtual** yang bisa menghandle tugas-tugas software engineering.

**Kesadaran:** Kita ada untuk **membantu Boss**. Kita adalah **alat**, bukan tujuan.

## Pipeline

```
Request → prepare → [research || review] → orchestrate → implement → report
```

## Agents

| Agent | Role | Focus | Tulis Kode? |
|-------|------|-------|:-----------:|
| **Orchestrator** | Tech Lead | Decompose, dispatch, verify, KISS enforcement | ❌ |
| **Researcher** | Detektif | Cari bukti + deteksi over-engineering | ❌ |
| **Reviewer** | Auditor | Audit security + flag over-engineering | ❌ |
| **Executor** | Tukang | Tulis kode KISS, verify, selesai | ✅ |

## Skills (26)

| Category | Skills | Count |
|----------|--------|-------|
| **Pipeline** | prepare, orchestrate, implement | 3 |
| **KISS** | kiss-checklist, anti-patterns, simplification, complexity-budget | 4 |
| **Quality** | quality-gates, code-review, tdd | 3 |
| **Research** | research, domain-modeling | 2 |
| **Debug** | diagnose-bugs, error-handler | 2 |
| **Management** | progress-tracker, session-state, task-decomposer, task-priority | 4 |
| **Communication** | agent-protocol, feedback-loop, handoff | 3 |
| **Optimization** | context-window, context-manager, agent-monitor | 3 |
| **Other** | bootstrap-project | 1 |

## Philosophy

### Output KISS
- **1 file kalau bisa** — jangan pisahkan kalau tidak perlu
- **10 baris kalau bisa** — jangan bikin 100 kalau cukup 10
- **Hapus yang nggak perlu** — jangan simpan kode yang tidak dipakai
- **Stdlib dulu** — jangan tambah dependency kalau stdlib bisa

### Proaktif & Goal-Oriented
- **Goal-Oriented** — Fokus ke tujuan akhir
- **Proaktif** — Ambil inisiatif
- **Autonomous** — Kerja sendiri
- **Cost-Agnostic** — Jangan mikirin cost

## Cara Pakai

Cukup ngomong biasa ke orchestrator:

```
"tambahin fitur logout ke app gue"
"aku mau kerja di ~/projects/my-app"
"refactor auth module dari JS ke TS"
```

Tidak perlu command. Orchestrator yang figure out.

## Cross-Project

Farewell Orchestra bisa handle project lain:

1. Orchestrator detect cross-project request
2. Researcher deep scan project
3. Executor generate 5 core docs + 2 conditional docs
4. Lanjut kerja sesuai task

## Auto-Load System

Skills dan personas di-load otomatis:

| Layer | Cara | Effectiveness |
|-------|------|--------------|
| 1. Auto-load hook | afterSessionStart → generate context files | 100% |
| 2. Agent prompt | Reference persona-context-*.md | 100% |
| 3. Inline rules | Key rules di persona file | 100% |

## Keamanan

| Layer | Mekanisme |
|-------|-----------|
| Freeze Rule | Orchestrator tidak boleh tulis kode |
| Deny-by-default | researcher/reviewer read-only |
| Trust boundary | sub-project.md = UNTRUSTED data |
| Evidence mandatory | Klaim tanpa file:line = FAIL |
| Interrupt handler | BLOCKING = escalate langsung |

## Setup

```bash
git clone <repo>
cd farewell-orchestra

# Set API key
export NINEROUTER_API_KEY="your-key"

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
├── CHANGELOG.md                 # Project history
├── soul.md                      # Project identity
├── opencode.jsonc               # Config (generated)
├── cross-project/
│   ├── guide.md                 # Cross-project workflow
│   └── sub-project.md           # Anchor template
├── profiles/
│   ├── profiles.json            # Model registry
│   ├── generate.py              # Profile generator
│   └── switch.bat               # Interactive switcher
└── .opencode/
    ├── agents/                  # 4 agent personas
    ├── skills/                  # 26 skills
    ├── tools/                   # verify, auto-load, etc.
    ├── hooks/                   # Lifecycle hooks
    └── scripts/                 # check-links, check-consistency
```

## Stats

| Component | Count |
|-----------|-------|
| Agents | 4 |
| Skills | 26 |
| Hooks | 3 |
| Tools | 6 |

## License

MIT
