# Farewell Orchestra

**4-agent AI orchestration system** — Tech Lead, Developer, Detective, Auditor. Satu tim, satu suara.

Dibangun di atas [OpenCode](https://opencode.ai) via [9Router](http://127.0.0.1:20128). Foreground-only, deny-by-default. Input sampah ditolak di gerbang.

---

## Quick Start

```bash
switch.bat        # pilih 1 (V1) atau 2 (Limited)
opencode
```

Cross-project: `"kerjain project ini <path>"` — orchestra auto-detect dan kerja di folder target. Lihat `project-guide.md`.

---

## Agent Architecture

| Agent | Persona | Skills | Role |
|-------|---------|--------|------|
| 🧙‍♂️ **Orchestrator** | Tech Lead galak | `anti-gigo` `grill` `orchestrate` | Validasi input, dekomposisi, fan-out, delegasi |
| 🕵️‍♂️ **Researcher** | Detektif eksploratif | `forensic` `web-research` | Cross-file tracing, deep debugging, web research |
| 💂‍♂️ **Reviewer** | Auditor kejam | `stride-audit` | STRIDE threat model, convention enforcement |
| 👷‍♂️ **Executor** | Developer minimalis | `minimal-impl` `verification-ground-truth` | Satu-satunya writer — YAGNI-first, verify-first |

Flow: Boss → Orchestrator (validate + decompose) → Researcher + Reviewer (parallel read-only) → Orchestrator (synthesize) → Executor (implement). Executor gagal 2x → Researcher deep debug. Satu-satunya agent dengan izin edit/bash adalah Executor.

---

## Profile System

| Profile | Orchestrator | Researcher | Reviewer | Executor | Steps |
|---------|-------------|------------|----------|----------|:-----:|
| **Default** 🏆 | deepseek-v4-flash | deepseek-v4-flash-free | north-mini-code-free | deepseek-v4-flash-free | 25/25/18/24 |
| **Def-OR** | deepseek-v4-flash | gpt-oss-20b:free (OR) | north-mini-code:free (OR) | gpt-oss-20b:free (OR) | 25/25/18/24 |
| **Ollama** | ollama/minimax-m3 | ollama/minimax-m3 | north-mini-code-free | north-mini-code-free | 25/25/18/24 |
| **Oll-OR** | ollama/minimax-m3 | gpt-oss-20b:free (OR) | north-mini-code:free (OR) | gpt-oss-20b:free (OR) | 25/25/18/24 |
| **Codex** | cx/gpt-5.6-luna | north-mini-code-free | north-mini-code-free | deepseek-v4-flash-free | 25/25/18/24 |
| **Codex-OR** | cx/gpt-5.6-luna | gpt-oss-20b:free (OR) | north-mini-code:free (OR) | gpt-oss-20b:free (OR) | 25/25/18/24 |

- **Default** — Champion. deepseek-v4-flash paid orchestrator + OC free sub-agents.
- **Def-OR** — Default dgn OpenRouter free model.
- **Ollama** — Local-first. ollama/minimax-m3 untuk orchestrator + researcher.
- **Oll-OR** — Ollama dgn OpenRouter free model.
- **Codex** — cx/gpt-5.6-luna orchestrator + OC free (north-mini-code + deepseek-free).
- **Codex-OR** — Codex dgn OpenRouter free model.

```bash
switch.bat                       # Windows: pilih 1-6 sesuai profile
# Atau copy manual:
copy profiles\opencode.default.jsonc opencode.jsonc
```

---

## Skills

8 agent skills + 1 project scaffolding: `anti-gigo`, `grill`, `orchestrate`, `minimal-impl`, `verification-ground-truth`, `forensic`, `web-research`, `stride-audit`, `bootstrap-project`.

---

## Files

| File | Purpose |
|------|---------|
| `opencode.jsonc` | Default config (V1 profile) |
| `profiles/opencode.default.jsonc` | Default — deepseek-v4-flash (paid) + OC free |
| `profiles/opencode.default-or.jsonc` | Def-OR — deepseek-v4-flash + OR free |
| `profiles/opencode.ollama.jsonc` | Ollama profile — ollama/minimax-m3 (local) + OC free |
| `profiles/opencode.ollama-or.jsonc` | Oll-OR — ollama/minimax-m3 + OR free |
| `profiles/opencode.codex.jsonc` | Codex — cx/gpt-5.6-luna (codex) + OC free |
| `profiles/opencode.codex-or.jsonc` | Codex-OR — cx/gpt-5.6-luna + OR free |
| `switch.bat` | Profile switcher |
| `.opencode/agents/` | Agent persona — siapa mereka, gimana mereka bersikap |
| `.opencode/skills/` | Agent specialization skills (auto-discovered by OpenCode) |
| `AGENTS.md` | Aturan orkestrasi — flow, rules, slash commands |
| `LESSONS.md` | Log pembelajaran — tiap kali Boss koreksi |
| `project-guide.md` | Cross-project access — cara pakai orchestra dari repo lain |
| `templates/sub-project.md` | Template anchor untuk sub-project |

---

MIT