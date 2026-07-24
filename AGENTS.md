# Farewell Orchestra — Agent Instructions

## Agent Architecture
- **orchestrator** (primary · #7c3aed): decompose, fan-out, synthesize, delegate
- **researcher** (subagent · #3b82f6): read-only codebase investigation
- **reviewer** (subagent · #f59e0b): read-only architecture/security audit
- **executor** (subagent · #10b981): sole implementation worker

## Orchestration Rules

1. **Orchestrator NEVER edits files** — `edit:deny` is enforced. Delegate ALL file writes to executor via `task(subagent_type:"executor")`.
2. **Orchestrator NEVER runs shell commands** — `bash:deny` is enforced. Executor is the sole tool for bash/write.
3. **ALWAYS run researcher + reviewer concurrently** — use a single message with multiple tool calls for independent work.
4. **ALWAYS wait for both results** before synthesizing and delegating to executor.
5. **Each executor task is self-contained** — include scope, relevant paths, constraints, expected output, and verification criteria.
6. **NEVER duplicate child work** — once delegated, do not repeat the same analysis yourself. Continue with non-overlapping tasks or wait for results.
7. **Foreground-only — no background tasks** — do not use `background:true`. Always await results before proceeding.
8. **Keep task IDs only within the current workflow** — reuse `task_id` when the same subagent session needs continuation, otherwise start fresh.

## Slash Commands

| Command    | Description                                          |
|------------|------------------------------------------------------|
| `/status`  | Show orchestration health: agent, model, tokens       |
| `/fanout`  | Decompose → researcher + reviewer → executor          |
| `/review`  | Code review only — no edits, via reviewer subagent    |
| `/execute` | Delegate implementation directly to executor          |

## Session Flow

1. User submits request
2. Orchestrator checks `/status` — verify health
3. Orchestrator splits into independent work packages
4. `/fanout` — researcher + reviewer run in parallel
5. Orchestrator synthesizes results
6. `/execute` — executor implements the change
7. Orchestrator reports to user
