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
| **V1** (Default) 🏆 | deepseek-v4-flash | deepseek-v4-flash-free | north-mini-code-free | north-mini-code-free | 25/25/18/24 |
| **Limited** | ollama/minimax-m3 | ollama/minimax-m3 | north-mini-code-free | north-mini-code-free | 25/25/18/24 |

- **V1** — Hasil stress test champion. Minimal paid (orchestrator only), sisanya free model. Researcher pakai deepseek-v4-flash-free (reasoning kuat). Reviewer+executor pakai north-mini-code-free (code-focused, structured output).
- **Limited** — V1 base, flash model diganti ollama/minimax-m3. Cocok pas 9router limited atau mau pake model lokal.

```bash
switch.bat                       # Windows: pilih 1 (V1) atau 2 (Limited)
switch.sh                        # Unix: pilih 1 (V1) atau 2 (Limited)
# atau copy manual:
copy profiles\hybrid-v1.jsonc opencode.jsonc
copy profiles\opencode.limited.jsonc opencode.jsonc
```

---

## Skills

8 agent skills + 1 project scaffolding: `anti-gigo`, `grill`, `orchestrate`, `minimal-impl`, `verification-ground-truth`, `forensic`, `web-research`, `stride-audit`, `bootstrap-project`.

---

## Files

| File | Purpose |
|------|---------|
| `opencode.jsonc` | Default config (V1 profile) |
| `profiles/hybrid-v1.jsonc` | V1 profile — champion, deepseek + free models |
| `profiles/opencode.limited.jsonc` | Limited profile — ollama/minimax-m3 + free models |
| `switch.bat` / `switch.sh` | Profile switcher |
| `.opencode/agents/` | Agent persona — siapa mereka, gimana mereka bersikap |
| `.opencode/skills/` | Agent specialization skills (auto-discovered by OpenCode) |
| `AGENTS.md` | Aturan orkestrasi — flow, rules, slash commands |
| `LESSONS.md` | Log pembelajaran — tiap kali Boss koreksi |
| `project-guide.md` | Cross-project access — cara pakai orchestra dari repo lain |
| `templates/sub-project.md` | Template anchor untuk sub-project |

---

MIT