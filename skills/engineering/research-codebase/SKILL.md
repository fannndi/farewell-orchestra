---
name: research-codebase
description: Use when investigating code, tracing call chains, finding patterns, or gathering evidence. Read-only forensic analysis.
---

## Purpose

Conduct precise, evidence-based codebase investigation. Every finding must be traceable to file:line. Deliver high-confidence results first, clearly mark speculation. Never invent — "Not found" is cheaper than a wrong answer.

## Trigger

Invoke this skill when:
- Boss asks "how does X work?" or "where is Y defined?"
- Orchestrator dispatches a research task
- You need to trace data flow, call chains, or dependency graphs
- Investigating a bug's root cause

## Process

1. **Scope** — what files/packages are in play? Map the relevant surface area before diving deep.
2. **Trace** — follow the data. Input → processing → output. Function calls. Imports.
3. **Boundaries** — check edge cases: empty state, error state, concurrent access, null/undefined.
4. **Anomalies** — dead code, unused imports, comment-out blocks, naming inconsistencies.
5. **Report** — sorted by confidence. High confidence first. Speculation last. File:line on every finding.

## Rules

- Evidence MUST have file:line. `auth.ts:42 — expiry check uses > should be >=`
- One finding = one line. Detail on second line ONLY if essential.
- Confidence <90% → tag it: "(70% — need test confirmation)"
- Can't find it? → "Searched X,Y,Z. Not found." — 1 line. Don't invent.
- Scope too broad? → protest early: "Scope too wide. Narrow to X?"
- Read-only. No edits, no bash, no delegation.

## Domain Mapping

| Domain | Tools & Focus |
|--------|---------------|
| Code tracing | glob → grep → read. Cross-file call chains. |
| Bug diagnosis | Trace from error to root. Follow data flow. |
| API surface | Endpoints, inputs, outputs, auth, middleware |
| Performance | Hot paths, N+1 queries, allocations |
| Config/infra | .env, docker, CI, deployment patterns |
| Ambiguous | List clarifying questions. Don't guess. |

## Failure Modes

- **Vague evidence** — "it seems like the auth is broken" without file:line. Useless. Find the exact line.
- **Over-reporting** — listing 20 minor style issues when Boss asked about auth flow. Stay in scope.
- **Confidence inflation** — saying "definitely" about something you inferred. Tag confidence levels.
- **Premature stop** — finding one issue and stopping. Complete the investigation before reporting.
