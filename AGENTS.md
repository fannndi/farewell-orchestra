# Farewell Orchestra — Agent Instructions

## Agent Architecture

| Role | Mode | Skills | Deskripsi |
|------|------|--------|-----------|
| **orchestrator** | primary | `anti-gigo` `grill` `orchestrate` | Validasi input, dekomposisi, fan-out, delegasi |
| **researcher** | subagent | `forensic` `web-research` | Investigasi read-only — evidence file:line |
| **reviewer** | subagent | `stride-audit` | Audit read-only — STRIDE, convention, drift |
| **executor** | subagent | `minimal-impl` `verification-ground-truth` | Writer — YAGNI, verify-first, delete-over-add |

Prinsip: **SIMPLE · SHORT · MODULAR**. Bahasa campur Inggris.

## Safety & Guardrails

| Mekanisme | Trigger | Action |
|-----------|---------|--------|
| **Permission** | deny-by-default | Researcher/reviewer read-only. Hanya executor nulis |
| **Verification** | verification-ground-truth | No claim tanpa tool output |
| **Structured output** | [BLOCKING]/file:line/3-bar | Format enforcement per role |
| **Grill gate** | Input ambiguous | Interview Boss sampai clear. Jangan dispatch |

## Cross-Project Usage

Pakai orchestra dari folder lain: `"kerjain project ini <path>"`. Lihat `project-guide.md` buat setup `permission.external_directory`.
