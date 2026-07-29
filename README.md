# Farewell Orchestra

**4-agent AI orchestration system** — Tech Lead, Developer, Detective, Auditor. Satu tim, satu suara.

Dibangun di atas [OpenCode](https://opencode.ai) via [9Router](http://127.0.0.1:20128). Foreground-only, deny-by-default. Input sampah ditolak di gerbang.

---

## Quick Start

```bash
switch.bat              # double-click → menu → pilih profile
opencode
```

Cross-project: `"kerjain project ini <path>"` — orchestra auto-detect dan kerja di folder target. Lihat `project-guide.md`.

---

## Agent Architecture

| Agent | Persona | Skills | Role |
|-------|---------|--------|------|
| **Orchestrator** | Tech Lead galak | `anti-gigo` `grill` `orchestrate` | Validasi input, dekomposisi, fan-out, delegasi |
| **Researcher** | Detektif eksploratif | `forensic` `web-research` | Cross-file tracing, deep debugging, web research |
| **Reviewer** | Auditor kejam | `stride-audit` | STRIDE threat model, convention enforcement |
| **Executor** | Developer minimalis | `minimal-impl` `verification-ground-truth` | Satu-satunya writer — YAGNI-first, verify-first |

Flow: Boss → Orchestrator (validate + decompose) → Researcher + Reviewer (parallel read-only) → Orchestrator (synthesize) → Executor (implement). Executor gagal 2x → Researcher deep debug. Satu-satunya agent dengan izin edit/bash adalah Executor.

---

## Profile System

Model assignments dikelola via `profiles/profiles.json` — satu file, semua profile. Edit JSON itu untuk nambah/ubah profile.

Generator Python (`profiles/generate.py`) membaca `profiles.json`, nulis ke `profiles/opencode.temp.jsonc`, validasi JSON, lalu copy ke `opencode.jsonc`. Aman — kalau proses putus di tengah, file asli nggak kena.

| Profile | Orchestrator | Researcher | Reviewer | Executor |
|---------|-------------|------------|----------|----------|
| **default-oc** 🏆 | ocg/deepseek-v4-flash | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free |
| **default-or** | ocg/deepseek-v4-flash | north-mini-code:free (OR) | nemotron-3-ultra-550b:free (OR) | nemotron-3-ultra-550b:free (OR) |
| **ollama-oc** | ollama/minimax-m3 | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free |
| **ollama-or** | ollama/minimax-m3 | north-mini-code:free (OR) | nemotron-3-ultra-550b:free (OR) | nemotron-3-ultra-550b:free (OR) |
| **codex-oc** | cx/gpt-5.6-luna | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free |
| **codex-or** | cx/gpt-5.6-luna | north-mini-code:free (OR) | nemotron-3-ultra-550b:free (OR) | nemotron-3-ultra-550b:free (OR) |

```bash
switch.bat                       # double-click → menu interaktif → pilih
python profiles\generate.py --menu   # atau dari terminal
python profiles\generate.py codex-or # langsung pake nama profile
```

---

## Skills

8 agent skills + 1 project scaffolding: `anti-gigo`, `grill`, `orchestrate`, `minimal-impl`, `verification-ground-truth`, `forensic`, `web-research`, `stride-audit`, `bootstrap-project`.

---

## Files

| File | Purpose |
|------|---------|
| `opencode.jsonc` | Active config — hasil generate dari profile terpilih |
| `switch.bat` | Launcher — double-click untuk menu ganti profile |
| `profiles/profiles.json` | **Registry profile + models** — edit manual buat nambah/ubah |
| `profiles/generate.py` | Generator — baca profiles.json, tulis temp, copy ke root |
| `profiles/opencode.temp.jsonc` | Temp file — di-write dulu, baru di-copy (auto gitignored) |
| `profiles/opencode.example.jsonc` | Referensi — contoh hasil generate |
| `.opencode/agents/` | Agent persona — siapa mereka, gimana mereka bersikap |
| `.opencode/skills/` | Agent specialization skills (auto-discovered by OpenCode) |
| `AGENTS.md` | Aturan orkestrasi — flow, rules, slash commands |
| `LESSONS.md` | Log pembelajaran — tiap kali Boss koreksi |
| `project-guide.md` | Cross-project access — cara pakai orchestra dari repo lain |
| `templates/sub-project.md` | Template anchor untuk sub-project |

---

MIT