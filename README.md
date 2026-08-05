# Farewell Orchestra

Multi-agent orchestration untuk OpenCode. 4 agent, 6 skill, 1 pipeline.

## Konsep

```
Request → prepare → [research || review] → orchestrate → implement → report
```

| Agent | Tugas | Tulis Kode? |
|-------|-------|:-----------:|
| Orchestrator | Decompose, dispatch, verify | ❌ |
| Researcher | Investigasi codebase + web | ❌ |
| Reviewer | STRIDE audit + conventions | ❌ |
| Executor | Implementasi kode | ✅ |

## Cara Pakai

Cukup ngomong biasa ke orchestrator:

```
"tambahin fitur logout ke app gue"
"aku mau kerja di ~/projects/my-app"
"refactor auth module dari JS ke TS"
```

Tidak perlu command. Orchestrator yang figure out.

## Cross-Project

Kalau project target belum punya docs, sistem otomatis:
1. Reverse engineer project
2. Generate 5 core docs (PRD, Architecture, Rules, Tasks, Context)
3. +2 conditional (Schema, API_Contract) kalau ada DB/API

## Rules Kunci

| Rule | Artinya |
|------|---------|
| **Freeze Rule** | Orchestrator tidak nulis kode |
| **Evidence Standard** | Klaim WAJIB punya `file:line` |
| **Trust Boundary** | Sub-agent mampu, trust them |
| **Verify Gate** | Tidak ada "done" tanpa verify |

## Skills

| Skill | Fungsi |
|-------|--------|
| `prepare` | Input validation + cross-project detection |
| `orchestrate` | Decompose → fan-out → synthesize → brief |
| `research` | Codebase forensics + web research |
| `review` | STRIDE audit + convention enforcement |
| `implement` | YAGNI implementation + verify |
| `bootstrap-project` | Generate 5+2 docs (reverse engineering) |

## Setup

```bash
git clone <repo>
cd farewell-orchestra
python profiles/generate.py Pro
# Buka OpenCode di folder ini
```

## Struktur

```
AGENTS.md              — Rules (single source of truth)
cross-project/guide.md — Cross-project workflow
.opencode/
  agents/              — 4 persona (identity-driven)
  skills/              — 6 skills
  tools/               — verify.ts, verify.py
  hooks/               — post-generate, check-links
profiles/
  profiles.json        — Model registry
  generate.py          — Profile generator
```
