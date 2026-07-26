# Farewell Orchestra — Profile-Validated Configuration

**Workflow orchestration system for OpenCode** — parallel researcher+reviewer fan-out, controlled executor implementation, 5 tiered config profiles (Paid, Paid-Limit, Hybrid, Free, Free Backup). All profiles are structurally validated (JSON, model refs, permission coverage). Runtime enforcement depends on OpenCode engine. Self-assessed via LLM checklist, not CI-automated.

## Overview

Farewell Orchestra is a foreground-only, deny-by-default workflow orchestration setup built on [OpenCode](https://opencode.ai) via [9Router](http://127.0.0.1:20128). The orchestrator decomposes user requests, fans out to **researcher** + **reviewer** in parallel, synthesizes their findings, then delegates a single scoped task to **executor** — the only agent with write/bash permissions. Five profiles let you switch between all-paid, hybrid (1 paid + 1 free), all-free, and all-free-via-OpenRouter with zero config changes beyond `-c <profile>`.

## Architecture

```
User Request
    │
    ▼
┌─────────────────────────────────────────┐
│       orchestrator (primary · #7c3aed)   │
│  mode: primary · model: tier-dependent   │
│  permissions: read-only · edit:deny      │
│  steps: 40 · temperature: 0.2            │
└──────┬──────────────────┬────────────────┘
       │  fan-out         │  (parallel)
       ▼                  ▼
┌──────────────┐  ┌──────────────┐
│  researcher  │  │   reviewer   │
│  #3b82f6     │  │   #f59e0b    │
│  read-only   │  │  read-only   │
│  steps: 30   │  │  steps: 30   │
│  temp: 0.1   │  │  temp: 0.1   │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
              synthesize
                │
                ▼
┌─────────────────────────────────────────┐
│        executor (subagent · #10b981)     │
│  write+bash · temp: 0.2 · steps: 50     │
│  only agent with edit:allow, bash:allow  │
└─────────────────────────────────────────┘
```

## 5 Profiles

| Profile | Tier | Orchestrator | Researcher | Reviewer | Executor | Compaction | Models |
|---------|------|-------------|------------|----------|----------|------------|--------|
| `paid` | Paid | deepseek-v4-pro | deepseek-v4-flash | deepseek-v4-flash | deepseek-v4-pro | deepseek-v4-flash | 2 paid |
| `paid-limit` | Paid (Alt) | minimax-m3 | nemotron-3-ultra-550b | nemotron-3-ultra-550b | minimax-m3 | minimax-m3 | 1 paid + 1 paid |
| `hybrid` | Mixed | deepseek-v4-flash | north-mini-code-free | deepseek-v4-flash | deepseek-v4-flash | deepseek-v4-flash | 1 paid + 1 free |
| `free` | Free | nemotron-3-ultra-free | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free | nemotron-3-ultra-free | 2 free |
| `free-backup` | Free (OR) | nemotron-3-ultra-550b-free | north-mini-code-free | nemotron-3-ultra-550b-free | nemotron-3-ultra-550b-free | nemotron-3-ultra-550b-free | 2 free |

- **Paid** — 2 DeepSeek models via OCG provider. Max quality, max speed. Heavy-thinking orchestrator + executor, fast researcher/reviewer.
- **Paid-Limit** — Minimax M3 (primary) + Nemotron 3 Ultra 550B (sub) via NVIDIA. Large 512K context on primary, 128K on sub. Good for large-context tasks on a budget.
- **Hybrid** — 1 paid (DeepSeek Flash) + 1 free (North Mini Code). DeepSeek Flash handles orchestrator, reviewer, executor; North Mini handles researcher. Best cost/quality balance.
- **Free** — 2 free models via OCG provider (Nemotron Ultra + North Mini Code). Zero API cost, decent quality for mid-complexity tasks.
- **Free Backup** — 2 free models via OpenRouter provider. Identical role assignment, different gateway redundancy. Fallback when OCG is unavailable.

### Actual Context Limits (from 9Router source + direct API test)

| Model | Context Window | Max Output | Source |
|-------|---------------|------------|--------|
| `ocg/deepseek-v4-pro` | **1,000,000** | 65,536 | 9Router capabilities.js |
| `ocg/deepseek-v4-flash` | **1,000,000** | 65,536 | 9Router capabilities.js |
| `ollama/minimax-m3` | **512,000** | 131,072 | 9Router capabilities.js |
| `nvidia/nvidia/nemotron-3-ultra-550b-a55b` | **128,000** | — | 9Router capabilities.js |
| `oc/nemotron-3-ultra-free` | **128,000** | — | 9Router capabilities.js |
| `oc/north-mini-code-free` | **256,000** | — | Provider docs (AINorth) |
| `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` | **128,000** | — | 9Router capabilities.js |
| `openrouter/cohere/north-mini-code:free` | **256,000** | — | OpenRouter spec |

> **Note:** Context limits are enforced by 9Router gateway, not by OpenCode config. Values above are from `open-sse/providers/capabilities.js` in the 9Router source. The `limit.context` in profile files should match these numbers.

## Quick Start

```bash
git clone https://github.com/fannndi/farewell-orchestra
cd farewell-orchestra
echo NINEROUTER_API_KEY=sk_... > .env
opencode                                    # default (paid)
opencode -c profiles/opencode.paid-limit.jsonc  # paid-limit
opencode -c profiles/opencode.hybrid.jsonc  # hybrid
opencode -c profiles/opencode.free.jsonc    # free
opencode -c profiles/opencode.free-backup.jsonc  # free backup
```

> **Prerequisite:** 9Router must be running on `127.0.0.1:20128`. Configure your API key in `.env`.

## Agent Details

| Agent | Mode | Temperature | Steps | Permissions Summary |
|-------|------|-------------|-------|---------------------|
| `orchestrator` | primary | 0.2 | 40 | read-only; edit/bash deny; task→researcher,reviewer,executor; question allow |
| `researcher` | subagent | 0.1 | 30 | read-only; read/glob/grep/list/webfetch/websearch/lsp/skill allow; task deny |
| `reviewer` | subagent | 0.1 | 30 | read-only; read/glob/grep/list/webfetch/websearch/lsp/skill allow; task deny |
| `executor` | subagent | 0.2 | 50 | read/edit/glob/grep/list/bash/lsp/skill allow; task deny |

Additional built-in agents: `build` (primary, escape hatch), `plan` (primary, escape hatch), `general` (subagent, locked read-only), `explore` (subagent, locked read-only), `title`/`summary`/`compaction` (hidden internal).

## Permission Model

Deny-by-default enforced via `"*": "deny"` catch-all on every agent. Only explicitly listed tools are allowed.

| Agent | Default | edit | bash | task | webfetch | question |
|-------|---------|------|------|------|----------|----------|
| orchestrator | deny | deny | deny | researcher,reviewer,executor | — | allow |
| researcher | deny | deny | deny | deny | allow | — |
| reviewer | deny | deny | deny | deny | allow | — |
| executor | deny | allow | allow | deny | — | — |
| general | deny | — | — | deny | — | — |
| explore | deny | — | — | deny | — | — |
| compaction | deny | deny | deny | deny | — | — |

**Key principles:**
- **Orchestrator never touches files or shell** — delegation only.
- **Researcher + reviewer are pure read-only** — can inspect via code tools + web, cannot mutate.
- **Executor is the sole write/bash agent** — scoped to one task at a time; cannot delegate further (`task: deny`).
- **General + explore are locked down** — deny-by-default with read-only tool access. No bash/edit/task.
- **Compaction is fully restricted** — no tool access, `steps: 10` cap, hidden from user.

## Security Hardening

- **`"*": "deny"` catch-all** on orchestrator, researcher, reviewer, executor, general, explore — nothing slips through an unlisted permission.
- **Explicit deny-by-default on general + explore** — previously had relaxed permissions with bash/edit; now locked to read-only with `task: deny`.
- **Compaction limited to `steps: 10`** — prevents runaway context-compaction loops. Model tiered per profile.
- **Executor temperature 0.2** — deterministic, predictable implementation; no creative drift from the spec.
- **Researcher + reviewer temperature 0.1** — factual, evidence-based output with minimal hallucination.
- **Subagent depth capped at 1** — workers can't spawn workers. No recursive delegation.
- **Share disabled** — no session sharing to external services.
- **Foreground-only** — no `background: true` tasks. Every dispatch is awaited before proceeding.

## Skills

Setiap agent punya 1-2 skill spesialisasi di `skills/{role}/`:

| Agent | Skill | Fungsi |
|-------|-------|--------|
| orchestrator | `anti-gigo` | Validasi input — cegah sampah ke downstream |
| orchestrator | `orchestrate` | Dekomposisi, fan-out parallel, sintesis, delegasi |
| researcher | `forensic` | Cross-file tracing, evidence file:line, confidence calibration |
| reviewer | `stride-audit` | STRIDE threat model, priority tags, cumulative judgment |
| executor | `minimal-impl` | YAGNI ladder, verify-first, delete-over-add |

**Prinsip GIGO:** AI model termahal pun hasilkan sampah kalau inputnya sampah. `anti-gigo` adalah gerbang kualitas — Brief Framework (Goal/Scope/Acceptance/Risk) wajib terisi sebelum dispatch.

## Slash Commands

| Command | Agent | Description |
|---------|-------|-------------|
| `/status` | orchestrator | Show orchestration health: agent, model, tokens |
| `/fanout` | orchestrator | Decompose → researcher + reviewer parallel → executor |
| `/review` | reviewer (subtask) | Code review only — no edits, via reviewer subagent |
| `/execute` | executor (subtask) | Delegate implementation directly to executor |

## Orchestration Rules

1. **Decompose first.** Classify request by scope, risk, clarity, independence.
2. **Parallel by default.** Dispatch independent work packages concurrently.
3. **Sync before execute.** Wait for all parallel results before delegating to executor.
4. **Executor brief is precise.** Include paths, constraints, acceptance criteria, verification commands.
5. **No duplicate work.** Once delegated, do not repeat.
6. **Foreground only.** No background tasks.
7. **Verify against criteria.** Executor output must match acceptance criteria.
8. **Report: what, why, result.** Three sentences max.

## Files

| File | Purpose |
|------|---------|
| `opencode.jsonc` | Default config (same as paid profile) |
| `profiles/*.jsonc` | 5 tiered config profiles |
| `switch.bat` | Windows profile selector menu |
| `.env.example` | Environment variable template |
| `AGENTS.md` | Agent instruction context (loaded by OpenCode on start) |
| `.opencode/agents/` | Budget-aware agent personas |
| `README.md` | This file |

## Context Tuning (2026-07-26)

Profile di-tune berdasarkan audit 9Router v0.5.40 untuk efisiensi context:

- **RTK Token Saver**: aktif via 9Router web UI — kompresi tool_result, headroom, caveman, ponytail
- **Agent prompts**: dipangkas 40-50% (`orchestrator.md` 143→70 baris, `executor.md` 69→45, dll)
- **Compaction**: `keep.tokens` 12.000→8.000
- **Steps**: orchestrator 35→30, researcher/reviewer 25→20, executor 40→30
- **Skills restructure**: 23 file → 5 skill (anti-gigo, orchestrate, forensic, stride-audit, minimal-impl)

Estimasi hemat token: ~40% per session.

## License

MIT
