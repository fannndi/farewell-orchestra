---
name: lessons-learned
description: Use after every Boss correction. Logs error patterns to LESSONS.md and suggests rule updates when same mistake repeats 3+ times.
---

## Purpose

Close the feedback loop. Feed-forward systems (classify → dispatch → verify → done) repeat the same mistakes forever. This skill captures every correction, detects patterns, and auto-suggests persona/skill updates. Turns Boss corrections into system improvements — not just one-time fixes.

## Trigger

Invoke AUTOMATICALLY:
- After every Boss correction (`salah`, `fix`, `gak gitu`, `bukan`)
- After orchestrator completes rework
- On orchestrator session end (pattern review)

## Process

1. **Capture** — what was the original instruction? What was the correction? What was the root cause?
2. **Log** — append entry to `LESSONS.md` with: date, trigger phrase, original intent, what went wrong, correction, root cause category
3. **Detect pattern** — scan last 10 entries. Same root cause category appearing 3+ times?
4. **Suggest** — if pattern detected, propose specific rule/persona update. Format:
   ```
   📊 Pattern: [category] — 3x dalam [N] koreksi terakhir.
      Gejala: [apa yang terjadi berulang]
      Akar: [root cause]
      Suggested fix: [file spesifik]:[section] — [perubahan]
      Apply? (ya/tidak/nanti)
   ```
5. **Boss decides** — apply, defer, or ignore. If apply → executor implements the persona/skill change.

## Root Cause Categories

| Category | Contoh |
|----------|--------|
| `SCOPE_CREEP` | Executor modify file di luar scope |
| `AMBIGUITY` | Boss prompt vague, orchestrator tidak clarify |
| `OVER_ENGINEER` | Solusi terlalu kompleks untuk task sederhana |
| `WRONG_ASSUMPTION` | Asumsi salah, tidak dikonfirmasi |
| `MISSED_EDGE` | Edge case tidak terdeteksi researcher/reviewer |
| `DRIFT` | Executor kerjakan beda dari acceptance criteria |
| `BUDGET` | Token habis di tengah task |
| `RULE_CONFLICT` | Dua persona rule bertentangan |

## Rules

- Log harus SINGKAT. 2-3 baris per entry. Bukan cerita.
- Pattern detection: EXACT root cause category. 3+ dalam 10 entry terakhir → suggest.
- Suggestion harus SPESIFIK: file mana, section mana, teks apa yang berubah.
- Boss tidak apply suggestion? → catat "DECLINED" di LESSONS.md. Jangan suggest lagi untuk pattern yang sama.
- Jangan suggest rule yang sudah ada di persona. Cek dulu.
- Log LESSONS.md every session. Jangan timpa — append.

## Failure Modes

- **Over-logging** — setiap typo kecil dicatat. Hanya correction yang mengubah behavior.
- **Vague suggestion** — "update orchestrator rules" tanpa spesifik. Harus: "orchestrator.md:Pre-Flight — jadi default = clarify".
- **Pattern hallucination** — melihat pattern yang tidak ada (2 kejadian beda kategori dianggap sama).
- **Never suggests** — log menumpuk, tidak ada pattern detection. Review otomatis setiap 10 entry.
