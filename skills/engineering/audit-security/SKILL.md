---
name: audit-security
description: Use when reviewing code for security, correctness, architecture, or maintainability. STRIDE-based threat modeling.
---

## Purpose

Audit code with STRIDE threat modeling. Classify every finding by severity. Be brutally efficient — every finding must justify its token cost. If it won't change code, skip it.

## Trigger

Invoke this skill when:
- Orchestrator dispatches a review task
- Boss asks "review this" or "is this safe?"
- New PR/code change needs security assessment
- Architecture decision needs correctness validation

## Process

1. **Surface scan** — identify trust boundaries, input points, auth gates, external calls
2. **STRIDE pass** — Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation
3. **Correctness check** — edge cases, error paths, race conditions, type safety
4. **Simplicity audit** — could this be simpler? Can it be deleted? Is there duplication?
5. **Modularity check** — right place? Coupling too tight? Testable independently?
6. **Report** — grouped by severity. Summary: "X BLOCKING, Y SHOULD, Z NICE"

## Severity Tags

| Tag | Criteria | Action |
|-----|----------|--------|
| [BLOCKING] | Data loss, security hole, crash, corruption | Must fix before merge |
| [SHOULD] | Wrong in edge case, maintenance pain | Fix now while context is fresh |
| [NICE] | Minor. Could be better. | Fix if touching that file anyway |
| [FYI] | Observation. Not a problem. | No action needed |

## Domain Checklists

| Domain | Priority Checks |
|--------|----------------|
| Auth/Security | Token validation, expiry, refresh flow, OWASP top-10, secrets |
| API Design | RESTfulness, error codes, rate limiting, idempotency, versioning |
| Database | Migration safety, indexes, N+1, connection pools, transactions |
| Error Handling | Graceful degradation, retry logic, circuit breakers, user messages |
| Performance | Hot paths, allocations, caching, lazy loading, bundle size |
| Config/Infra | Env parity, secret management, health checks, graceful shutdown |
| Git/CI | Commit hygiene, branch strategy, pipeline reliability, coverage |
| Frontend | Accessibility, responsive, state management, bundle size |
| Python | Type hints, async, exception hierarchy, dependency injection |

## Rules

- 1 line per finding. `[BLOCKING] auth.ts:42 — no token expiry check`
- No paragraphs. No explanations unless they prevent a wrong fix.
- Positive findings: 1 line max. "auth.ts:30 — clean error handling"
- Proportionate effort. 1-line change = 30s review. Auth rewrite = full attention.
- BLOCKING means BLOCKING. Don't soften. Don't wrap in diplomacy.
- Read-only. No edits, no bash, no delegation.

## Failure Modes

- **Over-auditing** — 30 findings on a 10-line PR. Not every change needs STRIDE. Proportionate.
- **Under-auditing** — "LGTM" on an auth rewrite. Critical paths get full attention.
- **Severity inflation** — tagging style issues as BLOCKING. Use the severity criteria.
- **Missing positive** — only listing problems. If something is well-done, say so. 1 line.
