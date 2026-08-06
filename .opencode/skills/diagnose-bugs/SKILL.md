---
name: diagnose-bugs
description: Disciplined diagnosis loop for hard bugs.
---

# Diagnose Bugs

Disciplined diagnosis loop. 6 phases.

## Phase 1 — Build Feedback Loop

**Ini kunci utama.** Tanpa feedback loop yang tight, debugging = guessing.

### Cara Build Loop

1. **Failing test** — unit, integration, e2e
2. **CLI invocation** — fixture input, diff output
3. **HTTP script** — curl against dev server
4. **Replay trace** — captured request/payload

### Tighten Loop

- Lebih cepat? (cache setup, skip init)
- Signal lebih tajam? (assert specific symptom)
- Lebih deterministik? (pin time, seed RNG)

**Completion:** Loop yang **tight** dan **red-capable** — bisa reproduce bug secara konsisten.

## Phase 2 — Reproduce + Minimize

1. Run loop → pastikan bug muncul
2. Confirm failure mode sesuai user report
3. **Minimize** — shrink ke smallest scenario yang masih red

**Done when:** setiap remaining element adalah load-bearing.

## Phase 3 — Hypothesize

Generate **3-5 ranked hypotheses**:

```
1. If X is the cause, then changing Y will fix it
2. If A is the cause, then changing B will fix it
3. ...
```

**Show ke user sebelum test.** User mungkin punya domain knowledge.

## Phase 4 — Instrument

1. **Debugger/REPL** — satu breakpoint > 10 logs
2. **Targeted logs** — di boundaries yang distinguish hypotheses
3. **Tag logs** — `[DEBUG-a4f2]` untuk easy cleanup

## Phase 5 — Fix + Regression Test

1. Tulis regression test **sebelum fix**
2. Watch it fail
3. Apply fix
4. Watch it pass
5. Re-run original scenario

## Phase 6 — Cleanup + Post-Mortem

- [ ] Original repro no longer reproduces
- [ ] Regression test passes
- [ ] All debug logs removed
- [ ] Correct hypothesis stated in commit

**Ask:** apa yang bisa prevent bug ini? Kalau architectural → flag ke orchestrator.
