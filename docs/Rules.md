# # Rules.md

## Ringkasan
**Orchestration Rules, Standards, Guardrails** untuk production-grade AI software development.

## Orchestration Rules

1. **Anti-GIGO first.** Validasi input sebelum dispatch. Goal/Scope/Acceptance wajib.
2. **Decompose.** Pecah request jadi work packages independen.
3. **Parallel by default.** Researcher + reviewer jalan bersamaan.
4. **Sync before execute.** Tunggu hasil parallel sebelum delegasi.
5. **Executor brief is precise.** Paths, constraints, verification command. No fluff.
6. **No duplicate work.** Sekali didelegasikan, jangan ulangi.
7. **Foreground only.** No background tasks.
8. **Cumulative judgment.** Review aggregate change, bukan per-file. Safe individually ≠ safe combined.
9. **Never narrate tool calls.** Just do, report result.
10. **Report 3 lines max.** What, result, residual risk.

## Safety & Guardrails

### Deskripsi Guardrails

- **Loop Guard** — 3x agent+tool+intent identik → STOP
- **Step Budget** — Per-agent limit (20-30 steps), auto-terminate
- **Escalation** — Executor gagal 2x → STOP, researcher deep debug
- **Termination** — TRASH input / loop / structural error → STOP
- **Structured output** — [BLOCKING]/file:line/3-bar enforcement
- **Permission** — Deny-by-default (researcher/reviewer read-only)
- **Verification** — No claim tanpa command output
- **Grill gate** — Input ambiguous → interview sampai clear

## Skema Permission Agent

```jsonc
{
  "orchestrator": { "*": "deny", "edit": "deny", "bash": "deny", "question": "allow", "skill": "allow", "todowrite": "allow", "task": { "*": "deny", "researcher": "allow", "reviewer": "allow", "executor": "allow" } },
  "researcher": { "*": "deny", "read": "allow", "glob": "allow", "grep": "allow", "list": "allow", "webfetch": "allow", "websearch": "allow", "lsp": "allow", "skill": "allow", "task": "deny" },
  "reviewer": { "*": "deny", "read": "allow", "glob": "allow", "grep": "allow", "list": "allow", "webfetch": "allow", "websearch": "allow", "lsp": "allow", "skill": "allow", "task": "deny" },
  "executor": { "*": "deny", "read": "allow", "edit": "allow", "glob": "allow", "grep": "allow", "list": "allow", "bash": "allow", "lsp": "allow", "skill": "allow", "task": "deny" }
}
```

## Skill Usage Rules

- Hanya orchestrator invoke `anti-gigo`
- Grill (interview) sebelum dispatch kalau ambigu
- Suealways resep 5 baris brief untuk setiap delegasi
- Verification command WAJIB eksak (bukan suggest)
- Hs bear-remove unused import/comment (cleanup otomatis)

## Penerapan Kesalahan Proses

1. **Void input** → Hold, grill, interview sampai clear
2. **Loop/duplicate task** → Hentikan sesuai loop guard, lapor ke Boss
3. **Executor gagal** → Escalation (gagal 2x) -> researcher forensic debugging
4. **Permission block** → Audit permission matrix, status penambahan
5. **Stale reference** → Sync audit, update references (.md, config, skill)
6. **Verification fail** → Executor retry (1x dengan asumsi berbeda)

## Standard Output Format

### Format output tiap agent

```
### Format output orchestrator
ORCHESTRATOR: PASS. [TRIVIAL|MEDIUM|COMPLEX]. Lanjut synchronize.

### Format output researcher
[ANALISIS]/file:line - penemuan | [BLOCKING]/file:line - penghalang | [SHOULD]/file:line - must-have | [NICE]/file:line - nice-to-have

### Format output reviewer
[SECURITY]/file:line - celah | [ARCH]/file:line - drift | [CONVENTION]/file:line - violation

### Format output executor
Done. X file(s) changed. Verification: [output 1 baris]
```

## Pola Naming Konsisten

- **File:** kebab-case (Architecture.md, Design.md)
- **Variable:** camelCase, hindari underscore kecuali slash command
- **Kelas/Fungsi:** PascalCase
- **Direktori:** snake_case (bootstrap-project, Stride-Audit)
- **Skill path:** .opencode/skills/<nama-skill>/SKILL.md

## Kitaran Token Sumbu

1. Boss submit request
2. Orchestrator invoke anti-gigo → validasi
3. Orchestrator grill (kalau ambigu)
4. Orchestrator orchestrate → dekomposisi + fan-out
5. Researcher + reviewer parallel read-only investigation
6. Orchestrator synthesize → 3-bulat findings
7. Executor brief (5 field)
8. Executor invoke minimal-impl + verification-ground-truth
9. Executor cleanup → hapus debug artifacts
10. Report ke Boss: 3 lines max

## Keamanan Konvensi

- Whitelist command per agent (deny-by-default)
- Semua read-only kecuali executor
- Verifikasi ketat: tidak ada claim tanpa command output
- Input validation di trust boundary
- Error handling mencegah data loss
- Tidak ada background task
- Tidak ada duplicate processing
- Tidak ada tool call narrative

## Monitoring & Observability

- Loop guard: 3x identik intent
- Step budget: 30 max/per-agent
- Token usage cap: 1500 lines, 38.4KB per output
- Autocompact: context prune, tokens reserved 15000
- Ekspor error: Per menit, format: tanggal | tipe | pemicu | error | akar | fix
- Tampilan kesehatan: /status agent, model, token, detik

## Regenerasi & Improvement

### LESSONS.md
- Append-only, satu baris per insiden non-trivial
- Taxonomy: HALLUCINATED_TOOL, MALFORMED_OUTPUT, STALE_REFERENCE, RUNAWAY_AGENT, PERMISSION_BLOCK, SILENT_REGRESSION
- Fix pattern untuk tiap error type

### perbaikan Skala
- Revisit guardrails tiap triwulan
- Mekanisme gradasi pejabat
- Linting rules per-session ulang
- Rollback plans buat region produksi
---