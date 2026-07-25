---
name: full-cycle
description: Use when Boss gives a complex request that needs full orchestration — research, review, implementation, verification. The complete pipeline in one invocation.
---

## Purpose

Execute the complete Farewell Orchestra pipeline in one flow: decompose → fan-out research+review → synthesize → implement → verify. For complex, multi-file, irreversible tasks.

## Trigger

Boss requests that are:
- >1 file affected
- >3 steps needed
- Potentially irreversible (data changes, refactors, auth changes)
- Boss says "jalanin full" or "full cycle" or "kerjain semuanya"

## Pipeline

1. **Decompose** — split into independent work packages. Write a brief TODO list (3-5 items max).
2. **Gate check** — present TODO list to Boss. WAIT for "ok"/"jalan"/"go" before proceeding.
3. **Fan-out** — for each work package: dispatch `research-codebase` + `audit-security` in PARALLEL.
4. **Synthesize** — combine findings into ≤3 bullet points per package.
5. **Implement** — dispatch `implement-change` for each package. Sequential if dependent, parallel if independent.
6. **Verify** — after ALL implementations: run `verify-profile` on any configs touched. Run tests.
7. **Report** — 3 lines: what was done, results, residual risks.

## Rules

- Gate check is NON-NEGOTIABLE. Never skip step 2 for full-cycle.
- If any verify step fails → stop. Report failure. Don't continue to next package.
- Independent packages → parallel. Dependent packages → sequential with dependency order.
- Each implement-change call is its own executor session. Fresh context.
- After completion → auto-return to PLAN mode. Present results.
- Boss can interrupt at any step with "stop"/"tunda"/"salah" → follow behavioral triggers.

## Failure Modes

- **Skipping gate** — implementing before Boss approves the plan. Never skip step 2.
- **Over-parallelizing** — dispatching dependent packages in parallel. Check dependency graph first.
- **Silent failure** — a verify step fails but you continue. Stop and report.
