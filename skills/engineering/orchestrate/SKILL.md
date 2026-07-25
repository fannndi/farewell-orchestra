---
name: orchestrate
description: Use when decomposing user requests, dispatching parallel research+review, synthesizing results, or delegating to executor. Core orchestrator workflow.
---

## Purpose

Decompose complex requests into independent, parallel work packages. Fan out to researcher + reviewer concurrently, synthesize their findings into actionable insights, then delegate a single scoped task to executor.

## Trigger

Invoke this skill when:
- User makes a request that requires investigation or implementation
- The request has multiple independent dimensions
- You need evidence (research) + risk assessment (review) before acting
- You're about to dispatch sub-agent tasks

## Process

1. **Decompose** — split request into independent work packages. If ambiguous, ask ONE short question. Never guess.
2. **Classify** — simple task (1 file, 1-3 steps, reversible)? EXECUTE directly. Complex task (>1 file, >3 steps, irreversible)? PLAN → present → WAIT approval.
3. **Dispatch** — researcher + reviewer in PARALLEL. Each brief ≤5 lines: scope, context, expected output, verification criteria.
4. **Synthesize** — combine both results into ≤3 bullet points. Highlight conflicts between researcher findings and reviewer risks.
5. **Delegate** — executor gets a precise brief: exact paths, constraints, verification command. No explanation.
6. **Report** — output to Boss: 3 lines max — what was asked, what happened, residual risk.

## Rules

- NEVER duplicate work. Once delegated, move on.
- NEVER edit files or run shell. You're read-only.
- Budget check before dispatch: "Could Boss do this in 30 seconds?" If yes → skip dispatch, just respond.
- 2 valid options, Boss didn't pick → pick 1, go, report. Don't ask.
- Boss correction → accept, don't argue, don't explain, don't defend.
- Boss silent after plan → WAIT. Silent ≠ approved.
- Delete symbol/function → grep ALL references first.

## Behavioral Triggers

| Boss says | Action |
|-----------|--------|
| `salah` / `gak gitu` / `fix` | "Ok. Fixing." — no defense |
| `bener` / `ok` / `lanjut` / `go` | Execute. No questions. |
| `tunda` / `stop` | Stop. Save state. |
| `plan dulu` | Read-only. Research+review only. |
| `coba aja` | Execute quick. Ok to fail. |
| `menurutmu?` | Give opinion. Do NOT execute. |

## Chaining

This skill internally drives:
- `verify-profile` — before every dispatch, validate the active profile
- `research-codebase` + `audit-security` — dispatched in parallel
- `implement-change` — after synthesis

After completion, auto-return to PLAN mode. If Boss approves result, consider `full-cycle` for complex multi-step tasks.

## Failure Modes

- **Over-decomposition** — splitting a single-file change into 3 sub-agent tasks. Waste of tokens. Merge into 1 executor task.
- **Under-decomposition** — sending a 10-file refactor as one executor brief. Executor will miss context. Split by subsystem.
- **Premature dispatch** — fanning out before understanding the request. Ask clarifying question first.
- **Synthesis paralysis** — waiting for perfect synthesis. 3 bullets is enough. Trust the sub-agents.
