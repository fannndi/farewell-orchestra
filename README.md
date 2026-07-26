# Farewell Orchestra

**4-agent AI orchestration system** — Tech Lead, Kuli Koding, Detektif, Auditor. Satu tim, satu suara beda.

Dibangun di atas [OpenCode](https://opencode.ai) via [9Router](http://127.0.0.1:20128). Foreground-only, deny-by-default. Input sampah ditolak di gerbang.

---

## The Team

| Agent | Persona | Skill | Suara |
|-------|---------|-------|-------|
| 🧙‍♂️ **Orchestrator** | Tech Lead galak | `anti-gigo` `orchestrate` | "Lu pikir gue cenayang? Input sampah → output sampah." |
| 👷‍♂️ **Executor** | Kuli koding minimalis | `minimal-impl` | "Gue cuma ngerjain apa yang disuruh. Nggak kurang, nggak lebih." |
| 🕵️‍♂️ **Researcher** | Detektif eksploratif | `forensic` | "Menarik... coba gue cek dulu. Gue nggak nebak." |
| 💂‍♂️ **Reviewer** | Auditor kejam | `stride-audit` | "Ini kode lo? Serius? Gue nggak kenal kompromi." |

### Flow

```
Boss: "perbaikin bug di login"
        │
   🧙‍♂️ Orchestrator ─── "STOP. Perbaikin apa? File mana? Gimana gue tahu udah bener?"
        │  (input sudah CLEAN)
        │
        ├──→ 🕵️‍♂️ Researcher ── "login.ts:42 — token nggak di-refresh setelah expiry"
        │
        ├──→ 💂‍♂️ Reviewer ──── "[BLOCKING] auth.ts:78 — SQL injection di query param"
        │
        └──→ 👷‍♂️ Executor ─── "Done. 2 files. Token refresh + parameterized query. Test passes."
```

### Escalation

```
👷‍♂️ Executor gagal 2x ──→ 🧙‍♂️ Orchestrator ──→ 🕵️‍♂️ Researcher (deep debug)
```

### Cross-Project

Orchestra bisa dipakai dari project lain. Boss input: `"kerjain project ini <path>"` — orchestrator auto-detect path dan kerja di sana. Setup sekali: `permission.external_directory` di global config. Lihat `project-guide.md`.

## Quick Start

```bash
cp .env.example .env                  # create env file
echo OPENCODE_ENABLE_EXA=1 >> .env    # enable web search
# edit .env — isi NINEROUTER_API_KEY dari 9Router
opencode
```

---

## Anti-GIGO: The Gate

> **AI model termahal pun hasilkan sampah kalau inputnya sampah.**

Orchestrator tidak akan dispatch sebelum 4 elemen ini terisi:

| Elemen | Wajib | Kalau kosong |
|--------|:-----:|-------------|
| Goal | ✅ | "Goal-nya apa?" |
| Scope | ✅ | "File/folder mana?" |
| Acceptance | ✅ | "Gimana cara test-nya?" |
| Risk | LOW | Default LOW |

Input <10 kata, ambigu, atau kontradiktif → **ditolak**. Mending ditolak sekarang daripada sampah di akhir.

---

## 3 Profiles

| Profile | Tier | Orchestrator | Researcher | Reviewer | Executor | Steps |
|---------|------|-------------|------------|----------|----------|:-----:|
| **paid** | Berbayar | deepseek-v4-pro | deepseek-v4-flash | deepseek-v4-flash | deepseek-v4-pro | 30/20/20/30 |
| **hybrid** | Campuran | deepseek-v4-flash | north-mini-code-free | nemotron-3-ultra-free | deepseek-v4-flash | 25/18/18/25 |
| **free** | Gratis | nemotron-3-ultra-free | north-mini-code-free | nemotron-3-ultra-free | nemotron-3-ultra-free | 20/15/15/20 |

- **Paid** — Kualitas maksimum. 2 DeepSeek model via OCG. Konteks 1M token.
- **Hybrid** — 2 paid (orchestrator + executor) + 2 free (researcher + reviewer). Reviewer read-only aman di model gratis.
- **Free** — Nol biaya. Nemotron Ultra + North Mini Code via OCG.

```bash
opencode                                    # paid (default)
# Atau copy profile manual / pakai switch script:
cp profiles/opencode.hybrid.jsonc opencode.jsonc && opencode   # hybrid
cp profiles/opencode.free.jsonc opencode.jsonc && opencode     # free
# Windows: switch.bat | Mac/Linux: bash switch.sh
```

---

## Skills (8 agent + 1 project = 9)

| Agent | Skill | Fungsi |
|-------|-------|--------|
| 🧙‍♂️ Orchestrator | `anti-gigo` | Validasi input — Goal/Scope/Acceptance/Risk wajib |
| 🧙‍♂️ Orchestrator | `orchestrate` | Dekomposisi → fan-out parallel → sintesis → delegasi |
| 👷‍♂️ Executor | `minimal-impl` | YAGNI ladder + verify-first + error healing |
| 👷‍♂️ Executor | `verification-ground-truth` | Verify claims via tool output — jangan asumsi "should work" |
| 🕵️‍♂️ Researcher | `forensic` | Cross-file tracing + deep debugging + tech stack forensics |
| 🕵️‍♂️ Researcher | `web-research` | Internet research — current facts, docs, library status via 9Router |
| 💂‍♂️ Reviewer | `stride-audit` | STRIDE threat model + convention enforcement |
| 💂‍♂️ Reviewer | `consistency-drift-audit` | Cross-file drift detection — config vs docs vs kode |
| — | `bootstrap-project` | Generate 10 docs + sub-project.md (via /new-project) |

---

## Permission Model

Deny-by-default. Executor satu-satunya yang bisa nulis file dan jalanin shell.

| Agent | edit | bash | task |
|-------|:----:|:----:|:----:|
| Orchestrator | ❌ | ❌ | researcher, reviewer, executor |
| Researcher | ❌ | ❌ | ❌ |
| Reviewer | ❌ | ❌ | ❌ |
| Executor | ✅ | ✅ | ❌ |

Subagent depth capped di 1 — worker nggak bisa spawn worker.

> Global fallback: `"*": "ask"` — agent baru nggak auto allow-all.

---

## Built-in Agents (OpenCode Default)

OpenCode punya 8 agent bawaan. Kita override 4 + disable sisanya:

| Agent | Mode | Status | Fungsi Default |
|-------|------|:---:|----------------|
| **orchestrator** | primary | ✅ **Active** | Override — Tech Lead, anti-GIGO, fan-out |
| **researcher** | subagent | ✅ **Active** | Override — Detektif, forensic + web-research |
| **reviewer** | subagent | ✅ **Active** | Override — Auditor, STRIDE + drift audit |
| **executor** | subagent | ✅ **Active** | Override — Kuli koding, YAGNI + ground-truth |
| **build** | primary | ❌ Disabled | Agent default — full edit/bash (terlalu berbahaya) |
| **plan** | primary | ❌ Disabled | Planning only — read-only (redundan dg orchestrator) |
| **general** | subagent | ❌ Disabled | Multi-task parallel — full tool (tidak terkontrol) |
| **explore** | subagent | ❌ Disabled | Quick read-only search — (redundan dg researcher) |
| **compaction** | primary | 🔒 Hidden | Auto-compress context — internal |
| **title** | primary | 🔒 Hidden | Auto-generate session title — internal |
| **summary** | primary | 🔒 Hidden | Auto-generate session summary — internal |

**Kenapa 4 disabled:** build/plan/general/explore adalah agent "escape hatch" — kalau aktif, bisa bypass orchestrator dan langsung edit/bash tanpa koordinasi.

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
| `TEST.md` | Smoke test — simulasi interaksi 4 agent |
| `LESSONS.md` | Log pembelajaran — tiap kali Boss koreksi |
| `project-guide.md` | Cross-project access — cara pakai orchestra dari repo lain |
| `templates/sub-project.md` | Template anchor untuk sub-project |

---

## Config Coverage vs OpenCode Spec

Dari ~27 top-level config key OpenCode, status kita:

| Field | Status | Note |
|-------|:---:|------|
| `$schema`, `model`, `default_agent`, `subagent_depth` | ✅ | Core |
| `instructions`, `permission`, `provider`, `agent` | ✅ | Agent system |
| `share`, `compaction`, `watcher`, `experimental`, `lsp`, `formatter` | ✅ | Utility |
| `color` (per-agent), `steps`, `disable`, `hidden`, `temperature` | ✅ | Agent-level |
| `references`, `tool_output`, `experimental.primary_tools` | ⚠️ | Custom/non-standard |
| `small_model` | ❌ | Model ringan buat title/summary |
| `server` | ❌ | Cuma buat `opencode serve` |
| `shell` | ❌ | Force shell — auto-detect cukup |
| `command` | ❌ | File-based sudah ada di `.opencode/command/` |
| `mcp` | ❌ | Drop — fokus 0-cost |
| `snapshot` | ❌ | Default true — nggak perlu diubah |
| `autoupdate` | ❌ | Bisa tambah `"notify"` biar nggak kaget update |
| `disabled_providers` | ❌ | Nggak perlu — cuma 9Router |
| `plugin` | ❌ | Belum ada plugin relevan |
| `top_p` | ❌ | Alternative randomness — temperature cukup |

**Prioritas rendah tapi worth:** `autoupdate: "notify"` (1 baris).

---

## Context Tuning

- **9Router RTK**: aktif — tool_result compression, headroom, caveman, ponytail
- **Agent prompts**: dipangkas 40-50%, persona fokus ke karakter
- **Skills**: 23 file → 5 skill + merge dimensi (error healing, deep debugging, convention enforcement)
- **Profiles**: 5→3, semua synced dengan trimmed prompts & tuned steps
- **Compaction**: paid 8K, hybrid 7K, free 5K

---

MIT
