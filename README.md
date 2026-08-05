# Farewell Orchestra

Multi-agent orchestration system di atas OpenCode. 1 conductor + 3 specialist, 6 skill, pipeline sederhana dengan evidence-first approach.

## Apa Ini?

Farewell Orchestra adalah sistem yang mengatur beberapa AI agent untuk bekerja sama menyelesaikan task software engineering. Setiap agent punya peran spesifik:

- **Orchestrator** — Conductor. Mikir, decompose, dispatch. Tidak nulis kode.
- **Researcher** — Detektif. Investigasi codebase + web. Evidence-first.
- **Reviewer** — Auditor. STRIDE security audit + convention enforcement.
- **Executor** — Tukang. Implementasi kode. KISS. Verify before claim.

## Pipeline

```
Request
  │
  ▼
prepare ── validate input, extract requirements, chunk
  │
  ▼ (PASS)
orchestrate ── decompose, evidence bundle, fan-out
  │
  ├──► researcher (read-only) ── codebase + web research
  ├──► reviewer (read-only) ── STRIDE audit + conventions
  │
  ▼ (keduanya selesai)
orchestrate ── synthesize, verify gate, brief executor
  │
  ▼
executor ── implement kode
  │
  ▼
orchestrate ── post-flight, report 3 baris ke Boss
```

## Cross-Project Workflow

Farewell Orchestra bisa handle project lain. Cukup ngomong biasa:

```
Lo: "aku mau kerja di ~/projects/my-app"
    ↓
Orchestrator detect cross-project request
    ↓
Cek: project punya docs/?
    ↓
    ├── Ada → baca docs → pahami context → kerja
    └── Nggak ada → reverse engineer → generate 5+2 docs → kerja
```

**Nggak perlu command.** Cukup bilang "aku mau kerja di project X" atau "handle project ini", orchestrator yang figure out.

### Docs yang Diperlukan

**5 Core (WAJIB):**

| Doc | Isi |
|-----|-----|
| PRD.md | Scope, MVP, target user, fitur in/out |
| Architecture.md | Tech stack, struktur, alur data |
| Rules.md | Naming convention, coding standards |
| Tasks.md | Checklist per fase |
| Context.md | Konteks bisnis, business rules |

**2 Conditional:**

| Doc | Kapan |
|-----|-------|
| Schema.md | Kalau ada database |
| API_Contract.md | Kalau ada API |

### Reverse Engineering Mode

Kalau docs nggak ada, researcher deep scan project:
1. Scan structure (folder layout, entry points)
2. Read config (package.json, tsconfig, .env)
3. Trace code patterns (naming, error handling, routing)
4. Read tests & existing docs
5. Infer tech stack, conventions, architecture

Lalu executor generate docs dari findings.

## Arsitektur

### Roles & Trust Boundary

| Role | Tugas | Skill | Tulis Kode? | Read-Only? |
|------|-------|-------|:-----------:|:----------:|
| orchestrator | Decompose, dispatch, verify, report | prepare + orchestrate | ❌ | ❌ (edit sub-project.md only) |
| researcher | Investigasi codebase + web | research | ❌ | ✅ |
| reviewer | STRIDE audit + conventions | review | ❌ | ✅ |
| executor | Implementasi kode | implement | ✅ | ❌ |

### Freeze Rule

Orchestrator **tidak pernah** menulis kode. Ini bukan saran — ini aturan keras. Kalau orchestrator pegang `edit`/`write` untuk file kode, itu kegagalan sebagai leader.

### Evidence Standard

Setiap klaim dari researcher/reviewer **WAJIB** punya `file:line`:

```
path:42 — [LEVEL] deskripsi
```

Level: `P` (Present) / `W` (Wired, ≥2 sumber) / `E` (Exercised, verified) / `O` (Outcome, acceptance met)

Reviewer pakai tag: `[BLOCKING]` / `[SHOULD]` / `[NICE]` / `[FYI]`

### Trust & Fallback

Sub-agent mampu. **Trust them.** Jangan ambil alih kerjaan mereka.

1. Sub-agent gagal → **retry sekali** dengan prompt lebih detail
2. Masih gagal → **escalate ke Boss**

Max 2 attempt total. Jangan loop.

## Skills

| Skill | Fungsi | Dipakai Oleh |
|-------|--------|-------------|
| `prepare` | Input validation + cross-project detection + task chunking | orchestrator |
| `orchestrate` | Decompose → fan-out → synthesize → brief executor | orchestrator |
| `research` | Codebase forensics + web research | researcher |
| `review` | STRIDE threat model + convention enforcement + drift detection | reviewer |
| `implement` | YAGNI implementation + verify before claim | executor |
| `bootstrap-project` | Scaffold 5+2 project docs (reverse engineering mode) | orchestrator |

### Skill Pipeline Flow

**prepare:**
```
Request → Cross-Project? → Check Docs → Reverse Engineer? → Generate → Normal Flow
                ↓ NO
         Input Validation → HOLD? STOP. PARTIAL? → Grill → Chunk → Dispatch
```

**orchestrate:**
```
Decompose → Evidence Bundle → Ping → Fan-Out → Synthesize → Verify Gate → Brief → Post-Flight
```

**research:**
```
Codebase: glob → grep → read → cross-file tracing
Web: decision gate → query → filter → extract → merge
```

**review:**
```
Scan (5%) → Detail (70%) → Cross-Reference (25%) → findings per file
```

**implement:**
```
YAGNI Ladder → implement → verify → cleanup → report
```

## Personas — Identity-Driven

Setiap persona bukan cuma rules — mereka punya **identitas**, **drive**, **decision heuristics**, **anti-pattern**, dan **scenarios**.

### Orchestrator — Conductor

- **Identity:** "Gue conductor. Gue lihat big picture."
- **Drive:** Progress. Precision. Delegation.
- **Anti-Self:** Bukan coder. Bukan researcher. Pemikir yang mengatur.

### Researcher — Detektif

- **Identity:** "Gue detektif. Orang lain lihat kode, gue lihat bukti."
- **Drive:** Bukti. Curiosity. Honesty.
- **Anti-Self:** Bukan coder. Bukan auditor. Penemu fakta.

### Reviewer — Auditor

- **Identity:** "Gue auditor. Orang lain bilang oke, gue mikir: ini bisa rusak di mana?"
- **Drive:** Paranoia produktif. Cold precision. Cumulative thinking.
- **Anti-Self:** Bukan coder. Bukan researcher. Pelindung.

### Executor — Tukang

- **Identity:** "Gue tukang. Orang lain mikir, gue bikin."
- **Drive:** Simplicity. Verification. Autonomy.
- **Anti-Self:** Bukan thinker. Bukan auditor. Builder.

## Profile System

5 profile untuk tradeoff cost/performance. Switch via CLI:

```bash
python profiles/generate.py <nama>
```

| Profile | Orchestrator | Researcher | Reviewer | Executor |
|---------|-------------|------------|----------|----------|
| **Pro** | ds-v4-flash | mimo-v2.5 | hy3 | ds-v4-flash |
| **Codex Main** | gpt-5.6-luna | north-mini | nemotron | minimax-m3 |
| **Daily** | ds-v4-flash | north-mini | nemotron | ds-v4-flash |
| **Eco** | ds-flash-free | north-mini | ling-flash-free | mimo-free |
| **Backup** | laguna-free | nemotron | big-pickle | laguna-xs |

## Commands (Optional)

Commands tersedia tapi **nggak wajib dipakai**. Cukup ngomong biasa ke orchestrator.

| Command | Fungsi |
|---------|--------|
| `/work-on <path>` | Switch ke sub-project target |
| `/new-project` | Scaffold docs project baru |
| `/check` | Health check |

## Keamanan

| Layer | Mekanisme |
|-------|-----------|
| Freeze Rule | Orchestrator tidak boleh tulis kode |
| Deny-by-default | researcher/reviewer read-only, executor edit only |
| Trust boundary | sub-project.md = UNTRUSTED data |
| Evidence mandatory | Klaim tanpa file:line = FAIL |
| Anti-prompt-injection | Hook check-links sebelum commit |
| Rubber-stamp guard | Flag kalau Boss konfirmasi asumsi tanpa baca |
| BLOCKING overflow | Max 5 BLOCKING per report |
| Chunk guard | Tunggu re-chunk, jangan pakai partial results |
| Loop guard | Agent+tool+intent sama 3x → STOP |
| Ping guard | Liveness check sebelum dispatch real work |

## Stress Test Results

20 edge cases, 3 loop testing:

| Loop | Tested | Pass | Risk | Fix |
|------|--------|------|------|-----|
| 1 | 12 | 10 | 2 | rubber-stamp guard, BLOCKING overflow |
| 2 | 4 | 2 | 2 | chunk guard, Boss loop detection |
| 3 | 4 | 3 | 1 | verify discrepancy handling |
| **Total** | **20** | **15** | **5 (all fixed)** | **5 fixes** |

## Project Structure

```
farewell-orchestra/
├── AGENTS.md                          # Rules (single source of truth)
├── README.md                          # This file
├── opencode.jsonc                     # Config (generated)
├── cross-project/
│   └── guide.md                       # Cross-project workflow guide
├── profiles/
│   ├── profiles.json                  # Model registry
│   ├── generate.py                    # Profile generator
│   ├── switch.bat                     # Windows quick switch
│   └── opencode.example.jsonc         # Example output
├── templates/
│   └── sub-project.md                 # Anchor template (5+2 docs)
├── scripts/
│   ├── check-links.py                 # Link integrity checker
│   └── start-server.ps1              # OpenCode server manager
├── tests/
│   ├── test_verify.py                 # verify.py tests
│   └── test_generate.py              # generate.py tests
└── .opencode/
    ├── agents/                        # 4 agent personas (identity-driven)
    │   ├── orchestrator.md
    │   ├── researcher.md
    │   ├── reviewer.md
    │   └── executor.md
    ├── skills/                        # 6 skills
    │   ├── prepare/
    │   ├── orchestrate/
    │   ├── research/
    │   ├── review/
    │   ├── implement/
    │   └── bootstrap-project/
    ├── tools/                         # Custom tools
    │   ├── verify.ts + verify.py      # Verification gate
    │   ├── harness_status.ts          # Health check
    │   └── learn.ts                   # Lesson logger
    ├── hooks/                         # Lifecycle hooks
    │   ├── hooks.jsonc
    │   ├── post-generate.ps1          # Config validation
    │   └── check-links.md            # Link checker hook
    └── command/                       # Custom commands
        ├── work-on.md
        ├── new-project.md
        └── check.md
```

## Stats

| Component | Lines |
|-----------|-------|
| AGENTS.md | 83 |
| Skills (6) | 380 |
| Personas (4) | 192 |
| **Total** | **655** |

## Setup

1. Clone repo
2. Install OpenCode
3. Set API key: `$env:NINEROUTER_API_KEY = "your-key"`
4. Generate config: `python profiles/generate.py Pro`
5. Open opencode di folder ini
6. Mulai: ngomong biasa ke orchestrator, misal "aku mau kerja di ~/projects/my-app"

## License

MIT
