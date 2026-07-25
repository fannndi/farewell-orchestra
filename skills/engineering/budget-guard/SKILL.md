---
name: budget-guard
description: Use pre-execution to estimate token cost. Warns if estimated cost exceeds 80% of remaining budget. Always invoked during guardrail scan.
---

## Purpose

Prevent token exhaustion mid-task. Before dispatching to executor, rough-estimate token cost. If estimated cost >80% remaining budget → warn Boss. Boss decides: proceed (risky), simplify scope, or defer.

## Trigger

Invoke AUTOMATICALLY during orchestrator pre-flight guardrail scan:
- Before every executor dispatch
- After scope-guard completes
- When orchestrator budgets sub-agent tasks

## Process

1. **Estimate task size** — how many files? Create/update/delete? Lines changed? Grep needed?
2. **Factor in sub-agents** — researcher + reviewer + executor. ~500-2000 tokens per sub-agent for simple tasks.
3. **Apply heuristic**:
   - 1 file, <50 lines change = LOW (~1000 tokens)
   - 2-5 files, <200 lines = MEDIUM (~5000 tokens)
   - 5+ files, >200 lines, cross-cutting = HIGH (~15000+ tokens)
   - Grep across repo, mass rename = VERY HIGH (~30000+ tokens)
4. **Compare with budget** — rough remaining context window estimate
5. **Verdict** — BELOW 80% (safe) or ABOVE 80% (warn)

## Output Format

**SAFE:**
```
💰 Budget: ~X tokens est. Aman.
```

**WARN:**
```
⚠️ Budget Warning:
   Estimasi: ~15,000 tokens
   Sisa context: ~20,000 tokens (75% — mendekati batas)
   
   Opsi:
   1. Lanjut aja (bisa abort di tengah)
   2. Sederhanakan scope (rekomendasi: [spesifik])
   3. Jalankan bertahap (pecah jadi 2 task)
```

## Rules

- Estimasi kasar, bukan presisi. ±50% margin. Tujuannya cegah catastrophic exhaustion, bukan akuntansi presisi.
- ABOVE 80% → WARN selalu. Jangan pernah silent.
- BELOW 30% → tidak perlu report. Silent.
- 30-80% → report singkat 1 baris: "💰 Budget: ~Xk tokens."
- Kalau Boss bilang "lanjut" setelah WARN → proceed. Jangan debat. Budget guard hanya warn, tidak block.
- Research-only task (no executor) → otomatis lebih murah. Adjust estimate.

## Failure Modes

- **Over-estimate** — flag 200-line change as HIGH (15k tokens). Unnecessary panic.
- **Under-estimate** — flag cross-repo rename as MEDIUM. Token habis di tengah.
- **Budget policing** — block tugas kecil yang Boss sudah committed. Guard = warn, bukan gatekeep.
