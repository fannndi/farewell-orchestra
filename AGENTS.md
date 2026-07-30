# Farewell Orchestra — Agent Instructions

## Agent Architecture

| Role | Mode | Skills | Deskripsi |
|------|------|--------|-----------|
| **orchestrator** | primary | `anti-gigo` `grill` `orchestrate` | Validasi input, dekomposisi, WAJIB fan-out, delegasi, sintesis |
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

## Session Break Protocol (Step Limit / Max Steps)

**Trigger:** Kena "Maximum Steps Reached" atau sesi terpaksa berakhir dengan item pending.

**Action WAJIB sebelum output habis:**
1. Scan `todowrite` list — cari item masih `in_progress` atau `pending`
2. Pindahin ke `TODO.md` sebagai task list untuk next session
3. Tulis `TODO.md` header: `# Next Session — <tanggal>`
4. Setiap item: `- [ ] <task> — <file path, status terakhir>`
5. Report 1 baris: "Saved [n] pending items to TODO.md"

**Kriteria:** Skip kalau task tinggal verify doang (≤2 sub-items sisa). Wajib kalau ≥3 sub-items atau ada BLOCKING issue belum diresolve.

**Maturity:** [D] AGENTS.md | [W] orchestrator.md post-flight | [E] sesi ini (contoh: researcher limit di sesi ini) | [V] cek TODO.md setelah step limit