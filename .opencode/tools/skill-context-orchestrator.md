# Skills: orchestrator

=== prepare ===
---
name: prepare
description: Use when receiving a request — validate input, extract requirements, chunk if needed. Gate before orchestration.
activation: ALWAYS at start of every request
trigger: Any request from Boss
---
Gate awal sebelum dispatch. Flow:
```
Request → Cross-Project? → YES → Check Docs → Reverse Engineer? → Generate → Normal Flow
                ↓ NO
         Input Validation → HOLD? STOP. PARTIAL? → Grill. PASS? → Chunk → Dispatch
```
Kalau LLM tidak bisa handle complex instructions: cek request punya goal+scope. Ada → PASS. Nggak → HOLD, tanya: "Goal-nya apa? Scope-nya?"
Contoh: `HOLD — goal tidak jelas`
Skip chunking, assumption logger, dll — cukup cek goal+scope.

=== orchestrate ===
---
name: orchestrate
description: Use after prepare passes — decompose, fan-out parallel, synthesize, brief executor.
activation: After prepare returns PASS
trigger: prepare PASS → load orchestrate
---
Input sudah CLEAN. Flow:
```
Decompose → Evidence Bundle → Ping → Fan-Out → Synthesize → Validate & Verify → Brief Executor → Post-Flight
```
Kalau LLM tidak bisa handle complex instructions: Decompose 2-3 bagian → Fan-Out researcher+reviewer → Synthesize max 3 bullet → Brief executor (TASK/FILES/VERIFY) → Report `<what> · <result> · <risk>`
Contoh: `Auth module added · pytest pass · residual: rate limiting`
Skip evidence bundle, ping guard, dll — cukup flow dasar.
Pecah jadi work packages independen. Tiap package ≤5 baris brief.