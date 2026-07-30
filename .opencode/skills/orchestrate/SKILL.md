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

## 3. Fan-Out — WAJIB via `task` Tool

| Task | Agent | Read-only |
|------|-------|:---------:|
| Code investigation | researcher | ✅ |
| Security/architecture audit | reviewer | ✅ |
| Implementation | executor (tunggu sintesis) | ❌ |

**ALWAYS dispatch researcher + reviewer in parallel via `task` tool. NEVER skip.**

### Cara Dispatch yang Benar

GUNAKAN `task` tool. BUKAN lakukan sendiri.

```python
# ✅ BENAR — Parallel dispatch researcher + reviewer
task(subagent_type="researcher", description="[deskripsi pendek]",
     prompt="[brief dengan context + file references + expected output]")
task(subagent_type="reviewer", description="[deskripsi pendek]",
     prompt="[brief dengan context + file references + expected output]")

# ✅ BENAR — Dispatch executor setelah sintesis
task(subagent_type="executor", description="exec: [task]",
     prompt="[5-field brief, max 200 token]")

# ❌ SALAH — Jangan lakukan ini:
# baca file sendiri → review sendiri → implement sendiri
```

### Trust Your Sub-Agents

| Agent | Model | Kemampuan | Lo harus... |
|-------|-------|-----------|-------------|
| researcher | `north-mini-code-free` | forensic, web-research, read-only | Percaya dia baca file & lapor evidence |
| reviewer | `nemotron-3-ultra-free` | stride-audit, read-only | Percaya dia audit security & konvensi |
| executor | `nemotron-3-ultra-free` | minimal-impl, edit, verify | Percaya dia nulis kode sesuai brief |

**Prinsip:** 
- Sub-agent punya **model + skill + tool masing-masing**. Mereka specialized.
- Lo (orchestrator) tugasnya **decompose + dispatch + verify**, bukan ngerjain.
- Kalau sub-agent gagal → **re-dispatch dengan error detail**, bukan ambil alih.
- Kalau gagal 2x → **escalate ke researcher untuk deep debug**, bukan coba sendiri.

### Pengecualian (hanya ini yang diizinkan)
- Task trivial (1 baris typo fix) → langsung handle, gak perlu fan-out
- Simple file ops (read, grep, glob) sebagai preparation buat dispatch context
- Emergency fix (Boss bilang "coba aja" atau production down)

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

## 12. Loop Discovery Gate

Gunakan Loop Discovery ketika ada indikasi loop berulang atau schedulable engineering work.
Detail lengkap: `references/loop-discovery.md`

## 13. Runtime Loop Guard — 3x Trigger → Loop Discovery Gate

| Sinyal | Action |
|--------|--------|
| Agent+tool+intent sama 3x berturut-turut | STOP, invoke Loop Discovery Gate |
| Executor gagal error identik 2x | Escalate ke researcher |
| Researcher balik hasil sama 2x | Udah cukup — jangan research lagi |
| Conversation muter tanpa progress | Report: "Stuck di [topik]. Perlu arahan." |

> Runtime loop = STOP + design gate. Detail: `references/loop-discovery.md` §13-14

## 15. Dispatch Checklist (Khusus Orchestrator)

Jalankan ini secara sadar tiap kali mulai task:

```
□ 1. Task non-trivial? → Wajib dispatch researcher + reviewer
□ 2. Udah panggil task() tool? (subagent_type diisi)
□ 3. Researcher task() udah? → go
□ 4. Reviewer task() udah? → go (parallel!)
□ 5. Tunggu hasil keduanya? → jangan lanjut sebelum dua-duanya selesai
□ 6. Verify hasil researcher? → @verify stage:"research"
□ 7. Verify hasil reviewer? → @verify stage:"review"
□ 8. Sintesis hasil? → max 3 bullet
□ 9. Blast radius check? → score ≥45 tanya Boss
□ 10. Executor task() udah? → 5 field, max 200 token
□ 11. Verify hasil executor? → @verify stage:"implement"
□ 12. Report 3 baris? → what, result, residual risk
```

Kalau checklist >3 NO → STOP. Lo lagi ambil alih kerjaan sub-agent.

## 16. Stress Test — Dispatch Loop Precision

Periodik (tiap 3-5 sesi) jalankan simulasi ini untuk verifikasi dispatch berjalan:

### Skenario A: Research + Review (tanpa implementasi)
```
Brief: "Cari semua file yang pake pattern X dan audit keamanannya"
Dispatch: researcher(forensic: cari pattern X) + reviewer(stride-audit: audit security)
Expected: 2 task tool calls parallel → verify → report
```

### Skenario B: Full Pipeline (research → review → implement)
```
Brief: "Tambah validasi di form login, cek dulu state-nya"
Dispatch: researcher(cek state) + reviewer(audit existing) → sintesis → executor(tambah validasi)
Expected: 3 task tool calls total, sequential (R+V parallel → E)
```

### Skenario C: Loop Recovery
```
Brief: "Benerin bug di kalkulator" — di mana executor gagal 2x
Dispatch: executor → fail → researcher(deep debug) → executor retry
Expected: executor task → fail → researcher task → executor task lagi
```

### Skenario D: Multi-Model Trust
```
Brief: "Audit + refactor semua file di modul X"
Expected: researcher(north-mini-code-free) + reviewer(nemotron-3-ultra-free) → executor(nemotron-3-ultra-free)
FAIL jika: orchestrator melakukan research/review/implement sendiri
```

### Scoring
- PASS = semua dispatch via task tool, nggak ada yg dikerjain sendiri
- PARTIAL = dispatch tp orchestrator ikut campur
- FAIL = orchestrator kerjain sendiri

**Target: 100% PASS.** Kalau <80% → review dan tighten docs.

## Rules

- NEVER duplicate work. Once delegated, move on.
- Executor brief = MINIMAL. 5 field, max 200 token.
- Background tasks = FORBIDDEN. Semua foreground.
- Verify-first: jangan report "done" sebelum verify.
- **Trust > Control.** Lo hired sub-agent karena mereka capable. Percaya. Dispatch. Verify. Move on.
