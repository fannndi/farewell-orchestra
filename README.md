# Farewell Orchestra — Profile-Validated Configuration

**Workflow orchestration system for OpenCode** — parallel researcher+reviewer fan-out, controlled executor implementation, 4 tiered config profiles (Paid, Hybrid, Free, Free Backup). All profiles are structurally validated (JSON, model refs, permission coverage). Runtime enforcement depends on OpenCode engine. Self-assessed via LLM checklist, not CI-automated.

## Overview

Farewell Orchestra is a foreground-only, deny-by-default workflow orchestration setup built on [OpenCode](https://opencode.ai) via [9Router](http://127.0.0.1:20128). The orchestrator decomposes user requests, fans out to **researcher** + **reviewer** in parallel, synthesizes their findings, then delegates a single scoped task to **executor** — the only agent with write/bash permissions. Four profiles let you switch between all-paid, hybrid (1 paid + 1 free), all-free, and all-free-via-OpenRouter with zero config changes beyond `-c <profile>`.

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

## 4 Profiles

| Profile | Tier | Orchestrator | Researcher | Reviewer | Executor | Compaction | Models |
|---------|------|-------------|------------|----------|----------|------------|--------|
| `profiles/opencode.paid.jsonc` | Paid | deepseek-v4-pro | deepseek-v4-flash | deepseek-v4-flash | deepseek-v4-pro | deepseek-v4-flash | 2 paid |
| `profiles/opencode.hybrid.jsonc` | Mixed | deepseek-v4-flash | north-mini-code-free | deepseek-v4-flash | deepseek-v4-flash | deepseek-v4-flash | 1 paid + 1 free |
| `profiles/opencode.free.jsonc` | Free | nemotron-3-ultra-free | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free | nemotron-3-ultra-free | 2 free |
| `profiles/opencode.free-backup.jsonc` | Free (OpenRouter) | nemotron-3-ultra-550b-free | north-mini-code-free | nemotron-3-ultra-550b-free | nemotron-3-ultra-550b-free | nemotron-3-ultra-550b-free | 2 free |

- **Paid** — 2 DeepSeek models via OCG provider. Max quality, max speed. Heavy-thinking orchestrator + executor, fast researcher/reviewer.
- **Hybrid** — 1 paid (DeepSeek Flash) + 1 free (North Mini Code). DeepSeek Flash handles orchestrator, reviewer, executor; North Mini handles researcher. Best cost/quality balance.
- **Free** — 2 free models via OCG provider (Nemotron Ultra + North Mini Code). Zero API cost, decent quality for mid-complexity tasks.
- **Free Backup** — 2 free models via OpenRouter provider. Identical role assignment, different gateway redundancy. Fallback when OCG is unavailable.

## Quick Start

```bash
git clone https://github.com/fannndi/farewell-orchestra
cd farewell-orchestra
echo NINEROUTER_API_KEY=sk_... > .env
opencode                                    # default (paid)
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
- **Compaction limited to `steps: 10`** — prevents runaway context-compaction loops. Model tiered per profile (paid→flash, hybrid→flash, free→nemotron, free-backup→nemotron-550b).
- **Executor temperature 0.2** — deterministic, predictable implementation; no creative drift from the spec.
- **Researcher + reviewer temperature 0.1** — factual, evidence-based output with minimal hallucination.
- **Subagent depth capped at 1** — workers can't spawn workers. No recursive delegation.
- **Share disabled** — no session sharing to external services.
- **Foreground-only** — no `background: true` tasks. Every dispatch is awaited before proceeding.

## Health Score — 15/15

Three dimensions, five profiles, all passing:

| Dimension | Weight | `opencode.jsonc` | paid | hybrid | free | free-backup |
|-----------|--------|:---:|:---:|:---:|:---:|:---:|
| **Config Integrity** | 5 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Valid JSON, all agent refs resolve, model IDs match provider declarations, steps/temp within bounds, no orphan keys. | | | | | | |
| **Permission Security** | 5 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Deny-by-default on all agents, `task:deny` on workers, no write on orchestrator/researcher/reviewer, compaction fully locked, general/explore read-only. | | | | | | |
| **Model Failover** | 5 | ✅ | ✅ | ✅ | ✅ | ✅ |
| Each profile declares 2 models from its tier; agent assignments use declared models only; free-backup uses independent OpenRouter gateway for redundancy. | | | | | | |
| **Total** | **15** | **15** | **15** | **15** | **15** | **15** |

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
| `profiles/*.jsonc` | 4 tiered config profiles |
| `switch.bat` | Windows profile selector menu |
| `.env.example` | Environment variable template |
| `AGENTS.md` | Agent instruction context (loaded by OpenCode on start) |
| `.opencode/agents/` | Budget-aware agent personas |
| `README.md` | This file |

## License

MIT
