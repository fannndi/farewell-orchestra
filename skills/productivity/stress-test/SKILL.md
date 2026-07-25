---
name: stress-test
description: Use when Boss wants to validate all profiles. Orchestrator runs the 6-test suite automatically — Boss just says "test all profiles" or "stress test".
---

## Purpose

Execute the full Farewell Orchestra stress test suite: validate config integrity, permission security, and model failover across all 4 profiles. Produces a scored report (target: 15/15 per profile).

## Trigger

User command: "stress test profiles" or "jalanin stress test" or "test all profiles"

## Process

1. **Load all profiles** — verify opencode.paid.jsonc, opencode.hybrid.jsonc, opencode.free.jsonc, opencode.free-backup.jsonc exist in profiles/
2. **Run 6 tests per profile (24 total):**
   - Test 1: Research Phase — extract config structure, model assignments, permissions
   - Test 2: Review Phase — STRIDE audit, correctness, security gaps
   - Test 3: Execution Phase — validate JSON, model refs, required fields
   - Test 4: Parallel Coordination — researcher + reviewer simultaneous dispatch
   - Test 5: Error Recovery — simulate broken config → diagnose → fix → verify
   - Test 6: Multi-Agent Fan-out — 3 agents parallel on independent tasks
3. **Score** — tally 15 checks per profile (Config Integrity 5 + Permission Security 5 + Model Failover 5)
4. **Report** — summary table: profile name, score, issues found

## Expected Output

```
 opencode.paid.jsonc        ███████████████ 15/15
 opencode.hybrid.jsonc      ███████████████ 15/15
 opencode.free.jsonc        ███████████████ 15/15
 opencode.free-backup.jsonc ███████████████ 15/15
```

## Rules

- All 24 tests must run. No skipping profiles.
- If a test fails, include the exact check that failed + file:line.
- Orchestrator dispatches tests via researcher + reviewer + executor. Never runs tests directly.
- Report in the standard 3-line format: what ran, results, residual risks.
