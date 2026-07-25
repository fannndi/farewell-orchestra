---
name: drift-guard
description: Use post-execution to verify output matches acceptance criteria. Detects mission drift — when executor did something different from what was asked. Always invoked after executor completes.
---

## Purpose

Catch mission drift. After executor finishes, verify the output against original acceptance criteria. If executor solved a different problem or went beyond scope → flag as DRIFT. Prevents "done but wrong" scenarios.

## Trigger

Invoke AUTOMATICALLY:
- After every executor completion
- Before reporting "done" to Boss
- When orchestrator synthesizes executor results

## Process

1. **Recall acceptance criteria** from brief template — the testable "done" condition
2. **Verify output** — run the verification command if specified. Check file changes match criteria.
3. **Compare intent vs result** — did executor do what was asked, or something else?
4. **Check for extras** — any files modified that weren't in scope? (cross-check with scope-guard)
5. **Verdict** — MATCH (criteria satisfied) or DRIFT (gap found)

## Output Format

**MATCH:**
```
🎯 Drift: bersih. Output sesuai acceptance criteria.
```

**DRIFT:**
```
⚠️ Drift Detected:
   Acceptance: [apa yang diminta]
   Actual: [apa yang dikerjakan]
   Gap: [apa yang beda — 1 kalimat]
   
   Opsi:
   1. Terima apa adanya (acceptance longgar)
   2. Fix gap — executor lanjut
   3. Rollback — revert semua perubahan
```

## Rules

- Verifikasi selalu pakai acceptance criteria dari brief. Bukan dari opini.
- Gap kecil (typo, formatting) → catat sebagai FYI, bukan DRIFT. Hanya flag kalau functional gap.
- Acceptance criteria tidak ada? → SKIP drift check. Tidak bisa verify tanpa kriteria. Tapi catat: "⚠️ No acceptance criteria — drift check skipped."
- Kalau MATCH → 1 baris. Jangan elaborate.
- Kalau DRIFT → 3 opsi selalu. Boss pilih.
- Drift guard TIDAK memblokir. Hanya mendeteksi dan melaporkan. Boss yang putuskan.

## Failure Modes

- **Nitpicking** — flag formatting difference sebagai DRIFT. Hanya functional gap.
- **Missing drift** — executor ganti library tanpa bilang, drift guard tidak deteksi karena tidak ada acceptance criteria tentang library. Acceptance criteria harus spesifik.
- **False drift** — executor improve sesuatu yang tidak diminta tapi relevant. Itu improvement, bukan drift. Gunakan common sense.
