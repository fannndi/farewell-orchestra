---
name: orchestrate
description: Use after anti-gigo passes — decompose request, fan-out parallel, synthesize results, delegate to executor
---

# Orchestrate

Input sudah CLEAN. Sekarang dekomposisi + delegasi. **WAJIB fan-out. Jangan kerjain sendiri.**

## 1. Decompose

Pecah request jadi work packages independen. Tiap package ≤ 5 baris brief.

## 2. Fan-Out — WAJIB

| Task | Agent | Read-only |
|------|-------|:---------:|
| Code investigation | researcher | ✅ |
| Security/architecture audit | reviewer | ✅ |
| Implementation | executor (tunggu sintesis) | ❌ |

**ALWAYS dispatch researcher + reviewer in parallel.** NEVER skip. Kalau task cuma implementasi doang → tetap dispatch researcher untuk cek konteks. Kalau cuma research → tetap dispatch reviewer untuk cross-check.

## 3. Synthesize

Gabung hasil researcher + reviewer → max 3 bullet. Konflik? reviewer (security) > researcher (facts). Tapi researcher punya bukti file:line sanggah reviewer → catat sebagai "dispute" ke Boss.

## 4. Brief Executor — 5 field, max 200 token

```
TASK: [1 kalimat]
FILES: [path, path]
CONTEXT: [1-2 kalimat]
TRIED: [optional — apa yg udah gagal]
VERIFY: [command buat test]
```

## 5. Verify

- **Research & Review:** Panggil `@verify stage:"research/review" claims:"..." files:["..."]`
- **Implement:** Panggil `@verify stage:"implement" claims:"..." files:["..."]`
- ❌ FAIL → reject, minta revisi
- ✅ PASS → next

## 6. Blast Radius (sebelum executor kerja)

```
Files changed → grep imports → BFS impact.
Score: ≤3 files=0, ≤8=10, >8=20 | radius ≤5=0, ≤15=10, >15=20 | core hit? +25 | test gap? +5 each
Score ≥45 → tanya Boss sebelum lanjut.
```

## 7. Post-Flight

Verifikasi acceptance. Report 3 baris: what, result, residual risk.

## Rules

- NEVER duplicate work. Once delegated, move on.
- Executor gagal 2x → dispatcher researcher deep debug.
- 3x loop (agent+tool+intent sama) → STOP, tanya Boss.
- Output: 3 lines max.
