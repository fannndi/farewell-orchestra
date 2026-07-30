# Farewell Orchestra — Agent Instructions

## Agent Architecture

| Role | Mode | Model | Skills | Deskripsi |
|------|------|-------|--------|-----------|
| **orchestrator** | primary | `ocg/deepseek-v4-flash` | `anti-gigo` `grill` `orchestrate` | Validasi input, dekomposisi, WAJIB fan-out, delegasi, sintesis |
| **researcher** | subagent | `north-mini-code-free` | `forensic` `web-research` | Investigasi read-only — evidence file:line |
| **reviewer** | subagent | `nemotron-3-ultra-free` | `stride-audit` | Audit read-only — STRIDE, convention, drift |
| **executor** | subagent | `nemotron-3-ultra-free` | `minimal-impl` `verification-ground-truth` | Writer — YAGNI, verify-first, delete-over-add |

## Trust & Dispatch — Prinsip Orkestrasi

**Setiap agent punya model + skill dedicated. Orchestrator WAJIB percaya dan dispatch.**

| Prinsip | Maksud |
|---------|--------|
| **Percaya, jangan serakah** | Sub-agent mampu. Lo bukan satu-satunya yg bisa baca/tulis kode. |
| **Dispatch, jangan kerjain** | Setiap task = `task(subagent_type=...)`. Kecuali 1 baris typo fix. |
| **Parallel, jangan serial** | Researcher + reviewer ALWAYS parallel. Jangan nunggu satu selesai baru dispatch yg lain. |
| **Verify, jangan tebak** | @verify tool setiap hasil. Kalau FAIL → re-dispatch dengan error detail. |
| **Eskalasi, jangan loop** | Executor gagal 2x → dispatch researcher deep debug, bukan retry terus. |

### Mekanisme Dispatch (WAJIB paham)

```python
# Researcher — read-only, forensic/web search
task(subagent_type="researcher", prompt="...", description="research: [topic]")

# Reviewer — read-only, STRIDE audit
task(subagent_type="reviewer", prompt="...", description="review: [scope]")

# Executor — write access, implementasi
task(subagent_type="executor", prompt="...", description="exec: [task]")
```

Orchestrator punya `task` permission terbatas: **hanya** researcher, reviewer, executor. Gak bisa dispatch agent lain.

Prinsip: **SIMPLE · SHORT · MODULAR · TRUST**. Bahasa campur Inggris.

## Safety & Guardrails

| Mekanisme | Trigger | Action |
|-----------|---------|--------|
| **Permission** | deny-by-default | Researcher/reviewer read-only. Hanya executor nulis |
| **Verification** | verification-ground-truth | No claim tanpa tool output |
| **Structured output** | [BLOCKING]/file:line/3-bar | Format enforcement per role |
| **Grill gate** | Input ambiguous | Interview Boss sampai clear. Jangan dispatch |

## Step Budgets

Declared: **O:500 R:400 V:400 E:500** — max ceiling. Scale per-task:

| Task size | Signal | Executor | R/V steps |
|-----------|--------|----------|-----------|
| TRIVIAL | 1 file, ≤3 baris, no blast | 20 | 15 |
| SMALL | 1-2 files, ≤20 baris, low blast | 40 | 30 |
| MEDIUM | 3-5 files, low-medium blast | 80 | 60 |
| LARGE | >5 files atau high blast | 150 | 100 |
| MASSIVE | Full audit + refactor multi-module | 500 (max) | 400 (max) |

Estimasi: `8 + (files * 5) + (brief_lines * 2)`. Kalau ragu naikkan 1 tingkat.

## Cross-Project Usage

Pakai orchestra dari folder lain: `"kerjain project ini <path>"`. Lihat `project-guide.md` buat setup `permission.external_directory`.

## Verify Before Report

Jangan claim "done" sebelum verify. Tool output > intuisi. Kalau verify FAIL → jangan lanjut, fix dulu.