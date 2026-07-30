---
name: orchestrate
description: Use after anti-gigo passes — decompose request, fan-out parallel, synthesize results, delegate to executor
---

# Orchestrate

Input sudah CLEAN. **WAJIB fan-out. Jangan kerjain sendiri.**

## 1. Decompose

Pecah jadi work packages independen. Tiap package ≤ 5 baris brief.

## 2. Evidence Bundle — Context Sebelum Fan-Out

Kumpulin 4 lane jadi 1 brief context buat researcher + reviewer:

| Lane | Sumber | Output |
|------|--------|--------|
| A: Memory | sub-project.md | `[MEMORY] agent terakhir kerja apa` |
| B: Lessons | LESSONS.md | `[LESSONS] error pattern: n kejadian` |
| C: State | git status + grep | `[STATE] file [n] modified, [m] bersih` |
| D: Config | opencode.jsonc agent | `[CONFIG] profile [name], step [used]/[total]` |

Gabung: `CONTEXT: [MEMORY] [LESSONS] [STATE] [CONFIG]` — kirim ke researcher + reviewer.

## 3. Fan-Out — WAJIB

| Task | Agent | Read-only |
|------|-------|:---------:|
| Code investigation | researcher | ✅ |
| Security/architecture audit | reviewer | ✅ |
| Implementation | executor (tunggu sintesis) | ❌ |

**ALWAYS dispatch researcher + reviewer in parallel. NEVER skip.** 3 pengecualian:
- Task cuma implementasi → tetap dispatch researcher buat cek state
- Task cuma research → tetap dispatch reviewer buat cross-check
- Task trivial (1 baris typo fix) → langsung handle, gak perlu fan-out

## 4. Synthesize

Gabung hasil researcher + reviewer → max 3 bullet. Konflik? reviewer (security) > researcher (facts). Tapi researcher punya bukti file:line sanggah reviewer → catat "dispute" ke Boss.

## 5. Brief Executor — 5 field, max 200 token

```
TASK: [1 kalimat — apa yg harus dihasilkan]
FILES: [path, path — file yg disentuh]
CONTEXT: [1-2 kalimat — kenapa, constraint]
TRIED: [opsional — apa yg udah gagal, biar nggak diulang]
VERIFY: [command — cara test bahwa task selesai]
```

## 6. Blast Radius — Impact Analysis

**a. Build graph:** List file yg disentuh → grep import chain → BFS.

**b. Score impact:**
| Metric | Threshold | Score |
|--------|-----------|-------|
| Files changed | ≤3=low, ≤8=med, >8=high | 0/10/20 |
| Impact radius (affected) | ≤5=low, ≤15=med, >15=high | 0/10/20 |
| Core code hit? | auth/security/db/deploy file touched? | +25 |
| Test gaps? | file tanpa test pair | +5 each |

**c. Core rules trigger high alert:** `auth`, `login`, `credential`, `token`, `password`, `secret`, `permission`, `middleware`, `guard`, `rbac`, `database`, `migration`, `schema`, `deploy`, `release`

**d. Report:** `Blast Radius: [SCORE]/100 — [LOW|MEDIUM|HIGH|CRITICAL]`
Score ≥45 → tanya Boss. <45 & aman → silent lanjut.

## 7. Verify Gate

- **Research & Review:** Panggil `@verify stage:"research/review" claims:"..." files:["..."]`
- **Implement:** Panggil `@verify stage:"implement" claims:"..." files:["..."]`
- ❌ FAIL → reject, minta revisi. ✅ PASS → next.

## 8. Post-Flight

Verifikasi acceptance criteria. Report 3 baris: what, result, residual risk.

## 9. Escalation

Executor gagal 2x → STOP dispatch executor. Dispatch researcher: "Deep debug [error]. Root cause, bukan symptom." Researcher invoke `forensic`.

## 10. Peer Debate (trigger: `debat` / `double check` / high-stakes)

1. Researcher → analisis + evidence file:line
2. Reviewer → critique findings researcher (tunjuk celah/missing evidence)
3. Researcher rebuttal → tanggapi dengan bukti tambahan atau akui
4. Orchestrator → gabung final conclusion

Format output:
```
✅ AGREED: [poin sepakat]
⚠️ DEBAT: researcher klaim X vs reviewer counter Y — [resolusi]
📋 FINAL: [kesimpulan final]
```

**Token efficiency:** Rebuttal pake `task_id` resume subagent, jangan dispatch ulang.

## 11. Agent Work Loop — 15 Quality Gates (5 dimensi)

Tiap task lewati ini sebelum report. Gagal 1 → STOP, report ke Boss.

| Dimensi | Check | Passing criteria |
|---------|-------|------------------|
| 🎯 Task Understanding | Intent, Context, Scope | Goal jelas, path disebut, in/out scope eksplisit |
| 🎛 Execution | Reproducible, Permission, Constraint | Tool available, file di workspace, stack konsisten |
| ✅ Change Validation | Verify, Failure Diagnosis, Re-verify | Verification command ada, error di-identifikasi, fix re-run |
| 📦 Delivery | Acceptance, Risk, Rollback | Output sesuai criteria, risk dilapor, perubahan reversibel |
| 📚 Learning | Keputusan Log, Memory Update, Lesson | sub-project.md update, memori agent update, LESSONS.md log |

Gagal 3x di gate sama → eskalasi ke Boss.

## 12. Loop Guard

| Sinyal | Action |
|--------|--------|
| Agent+tool+intent sama 3x berturut-turut | STOP, tanya Boss |
| Executor gagal error identik 2x | Escalate ke researcher |
| Researcher balik hasil sama 2x | Udah cukup — jangan research lagi |
| Conversation muter tanpa progress | Report: "Stuck di [topik]. Perlu arahan." |

**Prinsip:** 3x sama = loop. Token lebih baik buat nanya Boss.

## Rules

- NEVER duplicate work. Once delegated, move on.
- Executor brief = MINIMAL. 5 field, max 200 token.
- Background tasks = FORBIDDEN. Semua foreground.
- Verify-first: jangan report "done" sebelum verify.
