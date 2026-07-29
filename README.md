# Farewell Orchestra

**4-agent AI orchestration system** — Tech Lead, Developer, Detective, Auditor. Satu tim, satu suara.

Dibangun di atas [OpenCode](https://opencode.ai) via [9Router](http://127.0.0.1:20128). Foreground-only, deny-by-default. Input sampah ditolak di gerbang.

---

## Quick Start

```bash
switch.bat        # pilih 1-6 sesuai profile (default-oc/or, ollama-oc/or, codex-oc/or)
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
| **default-oc** 🏆 | ocg/deepseek-v4-flash | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free | 20/18/14/18 |
| **default-or** | ocg/deepseek-v4-flash | north-mini-code:free (OR) | nemotron-3-ultra-550b:free (OR) | nemotron-3-ultra-550b:free (OR) | 20/18/14/18 |
| **ollama-oc** | ollama/minimax-m3 | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free | 20/18/14/18 |
| **ollama-or** | ollama/minimax-m3 | north-mini-code:free (OR) | nemotron-3-ultra-550b:free (OR) | nemotron-3-ultra-550b:free (OR) | 20/18/14/18 |
| **codex-oc** | cx/gpt-5.6-luna | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free | 20/18/14/18 |
| **codex-or** | cx/gpt-5.6-luna | north-mini-code:free (OR) | nemotron-3-ultra-550b:free (OR) | nemotron-3-ultra-550b:free (OR) | 20/18/14/18 |

- **default-oc** — Champion. ocg/deepseek-v4-flash paid + OC free (north-mini-code + nemotron).
- **default-or** — Default dgn OpenRouter free (north-mini-code + nemotron).
- **ollama-oc** — Local-first. ollama/minimax-m3 + OC free sub-agents.
- **ollama-or** — Ollama dgn OpenRouter free.
- **codex-oc** — cx/gpt-5.6-luna + OC free sub-agents.
- **codex-or** — Codex dgn OpenRouter free.

```bash
switch.bat                       # Windows: pilih 1-6 sesuai profile
# Atau copy manual:
copy profiles\opencode.default-oc.jsonc opencode.jsonc
```

---

## Skills

8 agent skills + 1 project scaffolding: `anti-gigo`, `grill`, `orchestrate`, `minimal-impl`, `verification-ground-truth`, `forensic`, `web-research`, `stride-audit`, `bootstrap-project`.

---

## Files

| File | Purpose |
|------|---------|
| `opencode.jsonc` | Default config (salinan salah satu profile) |
| `profiles/opencode.default-oc.jsonc` | default-oc — ocg/deepseek-v4-flash (paid) + OC free |
| `profiles/opencode.default-or.jsonc` | default-or — ocg/deepseek-v4-flash + OR free |
| `profiles/opencode.ollama-oc.jsonc` | ollama-oc — ollama/minimax-m3 (local) + OC free |
| `profiles/opencode.ollama-or.jsonc` | ollama-or — ollama/minimax-m3 + OR free |
| `profiles/opencode.codex-oc.jsonc` | codex-oc — cx/gpt-5.6-luna (codex) + OC free |
| `profiles/opencode.codex-or.jsonc` | codex-or — cx/gpt-5.6-luna + OR free |
| `switch.bat` | Profile switcher |
| `.opencode/agents/` | Agent persona — siapa mereka, gimana mereka bersikap |
| `.opencode/skills/` | Agent specialization skills (auto-discovered by OpenCode) |
| `AGENTS.md` | Aturan orkestrasi — flow, rules, slash commands |
| `LESSONS.md` | Log pembelajaran — tiap kali Boss koreksi |
| `project-guide.md` | Cross-project access — cara pakai orchestra dari repo lain |
| `templates/sub-project.md` | Template anchor untuk sub-project |

---

MIT