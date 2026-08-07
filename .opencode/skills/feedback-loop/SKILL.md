---
name: feedback-loop
description: Find issue, fix durable rule or test, verify. No written history.
activation: After task complete
trigger: Task selesai
---

# Feedback Loop

Find issue → Fix durable rule/test → Verify

## When to Update Rules

| Trigger | Update Rule/Test? |
|---------|-------------------|
| Task SUCCESS with issue discovered | YES |
| Task FAILURE | YES |
| Task PARTIAL | YES |
| Pattern repeats 3x | YES |
| Orchestrator corrects agent | YES |
| Task SUCCESS, no issues | NO |

## Process

### 1. Find Issue (After Each Task)

Tiap task, cek: ada masalah? (error, pattern berulang, koreksi orchestrator, bottleneck).
Jangan catat prosa — kalau masalah nyata, langsung encode jadi rule ATAU test.

### 2. Fix Durable Rule or Test

- **Rule:** update AGENTS.md / skill file — satu kalimat, eksplisit, actionable.
- **Test:** tambah assertion yang akan FAIL kalau masalah muncul lagi (regression guard).
- Kalau dua-duanya tidak tepat → masalah bukan rule/test material → skip.

### 3. Verify

Jalankan `python scripts/check-all.py` → ALL GREEN sebelum bilang selesai.
Test baru harus FAIL dulu (red) sebelum fix, PASS setelahnya (green).

### 4. Apply (Next Task)

Scan ulang rules + tests untuk gap. Jangan baca lesson log — tidak ada.
Rules + tests adalah satu-satunya memori durable.

## Rules

1. **Always encode failures** — error nyata → rule atau test, no exceptions
2. **Skip only clean success** — task SUCCESS zero issues = no change needed
3. **Pattern threshold = 3** — setelah 3x error sama, jadikan rule eksplisit (bukan cuma test)
4. **Satu perubahan per masalah** — jangan gabung fix + refactor + rename
5. **Tanpa written history** — masalah → rule/test, jangan catat di mana pun

## Output

Setelah update, orchestrator reports:
```
[FEEDBACK] rule/test updated — <file> — <apa yang berubah>
[PATTERN] (if applicable) "X happened 3+ times, rule added to <file>"
```
