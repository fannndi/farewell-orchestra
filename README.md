# Farewell Orchestra

**4-agent AI orchestration system** — Tech Lead, Developer, Detective, Auditor. Satu tim, satu suara.

Dibangun di atas [OpenCode](https://opencode.ai) via [9Router](http://127.0.0.1:20128). Foreground-only, deny-by-default. Input sampah ditolak di gerbang.

---

## Quick Start

```bash
cp .env.example .env                  # create env file
echo OPENCODE_ENABLE_EXA=1 >> .env    # enable web search
# edit .env — isi NINEROUTER_API_KEY dari 9Router
opencode
```

Cross-project: `"kerjain project ini <path>"` — orchestra auto-detect dan kerja di folder target. Lihat `project-guide.md`.

---

## Agent Architecture

| Agent | Persona | Skills | Role |
|-------|---------|--------|------|
| 🧙‍♂️ **Orchestrator** | Tech Lead galak | `anti-gigo` `grill` `orchestrate` | Validasi input, dekomposisi, fan-out, delegasi |
| 👷‍♂️ **Executor** | Developer minimalis | `minimal-impl` `verification-ground-truth` | Satu-satunya writer — YAGNI-first, verify-first |
| 🕵️‍♂️ **Researcher** | Detektif eksploratif | `forensic` `web-research` | Cross-file tracing, deep debugging, web research |
| 💂‍♂️ **Reviewer** | Auditor kejam | `stride-audit` | STRIDE threat model, convention enforcement |

Flow: Boss → Orchestrator (validate + decompose) → Researcher + Reviewer (parallel read-only) → Orchestrator (synthesize) → Executor (implement). Executor gagal 2x → Researcher deep debug. Satu-satunya agent dengan izin edit/bash adalah Executor.

---

## Profile System

| Profile | Tier | Orchestrator | Researcher | Reviewer | Executor | Steps |
|---------|------|-------------|------------|----------|----------|:-----:|
| **paid** | Berbayar | deepseek-v4-pro | deepseek-v4-flash | deepseek-v4-flash | deepseek-v4-pro | 30/25/24/30 |
| **hybrid** | Campuran | deepseek-v4-flash | deepseek-v4-flash | north-mini-code-free | north-mini-code-free | 25/25/18/24 |
| **free** | Gratis | nemotron (OpenRouter) | nemotron-3-ultra-free (OC) | nemotron-3-ultra-free (OC) | nemotron (OpenRouter) | 25/22/20/25 |

- **Paid** — Kualitas maksimum. 2 DeepSeek model via OCG. Konteks 1M token.
- **Hybrid** — 2 paid (orchestrator + executor) + 2 free (researcher + reviewer).
- **Free** — Nol biaya. Balanced: orchestrator+executor pakai Nemotron (OpenRouter), researcher+reviewer pakai Nemotron (OC). Load terdistribusi.

```bash
opencode                                    # paid (default)
cp profiles/opencode.hybrid.jsonc opencode.jsonc && opencode   # hybrid
cp profiles/opencode.free.jsonc opencode.jsonc && opencode     # free
```

---

## Skills

8 agent skills + 1 project scaffolding: `anti-gigo`, `grill`, `orchestrate`, `minimal-impl`, `verification-ground-truth`, `forensic`, `web-research`, `stride-audit`, `bootstrap-project`.

---

## Files

| File | Purpose |
|------|---------|
| `opencode.jsonc` | Default config (paid profile) |
| `profiles/opencode.*.jsonc` | 3 profile: paid, hybrid, free |
| `.env.example` | Env vars: NINEROUTER_API_KEY + OPENCODE_ENABLE_EXA |
| `.opencode/agents/` | Agent persona — siapa mereka, gimana mereka bersikap |
| `.opencode/skills/` | Agent specialization skills (auto-discovered by OpenCode) |
| `AGENTS.md` | Aturan orkestrasi — flow, rules, slash commands |
| `LESSONS.md` | Log pembelajaran — tiap kali Boss koreksi |
| `project-guide.md` | Cross-project access — cara pakai orchestra dari repo lain |
| `templates/sub-project.md` | Template anchor untuk sub-project |

---

MIT
