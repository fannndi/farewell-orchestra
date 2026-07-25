---
name: compound-review
description: Use when reviewing a significant change (>50 lines, >3 files). Dispatches parallel axis reviewers — security, architecture, performance — then synthesizes.
---

## Purpose

Multi-axis parallel code review for significant changes. Instead of one reviewer trying to cover everything, dispatch specialized reviewer instances in parallel, each focused on one axis.

## Trigger

- PR or change >50 lines or >3 files
- Boss says "review this thoroughly" or "audit lengkap"
- Pre-merge gate for critical paths (auth, payment, data migration)

## Axes (dispatch in PARALLEL)

| Axis | Focus |
|------|-------|
| **Security** | Auth, injection, secrets, OWASP top-10, data exposure |
| **Architecture** | Coupling, cohesion, modularity, dependency direction |
| **Performance** | Hot paths, N+1, allocations, caching, bundle size |
| **Correctness** | Edge cases, error paths, race conditions, type safety |

## Process

1. Determine change scope — which files, how many lines, what domain
2. Select relevant axes (not all 4 for every change — proportionate)
3. Dispatch one `audit-security` per axis with axis-specific briefs. ALL IN PARALLEL.
4. Synthesize: combine findings, deduplicate, prioritize by severity
5. Report: "X BLOCKING, Y SHOULD, Z NICE across {n} axes"

## Rules

- Proportionate: 10-line CSS change → 1 axis. Auth middleware rewrite → all 4.
- Each axis reviewer gets a brief with: files to review, axis focus, what to ignore
- Never run axes sequentially. They're independent — PARALLEL.
- Synthesis must deduplicate. Same finding from 2 axes = 1 report entry.
- Report format: `[SEVERITY] axis: file:line — finding`

## Failure Modes

- **Over-review** — 4-axis review on a typo fix. Proportionate.
- **Under-review** — 1-axis on an auth rewrite. Critical paths get full attention.
- **Sequential axes** — running security then architecture then performance. Wastes time. Parallel.
