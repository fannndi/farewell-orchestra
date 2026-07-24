# Farewell Orchestra — Agent Instructions

## Orchestration Rules

1. **orchestrator** is the only entry point. It decomposes requests, fans out researcher+reviewer in parallel, synthesizes, then delegates all file changes to executor.
2. **NEVER edit files from orchestrator** — `edit:deny` is enforced.
3. **NEVER run shell commands from orchestrator** — `bash:deny` is enforced.
4. **ALWAYS run researcher and reviewer concurrently** in one turn for independent analysis.
5. **ALWAYS wait for both results** before delegating to executor.
6. **Every executor task must be self-contained** with scope, paths, constraints, expected output, and verification criteria.
7. **Never duplicate child work** — once delegated, do not repeat the same analysis yourself.
8. **Foreground only** — no background tasks.

## Slash Commands

| Command      | Description                                         |
|-------------|-----------------------------------------------------|
| `/status`   | Show orchestration health: agent, model, tokens     |
| `/fanout`   | Run researcher + reviewer in parallel               |
| `/review`   | Code review via reviewer subagent, no edits         |

## Role Colors (TUI)

- orchestrator: `#7c3aed` (purple)
- researcher: `#3b82f6` (blue)  
- reviewer: `#f59e0b` (amber)
- executor: `#10b981` (green)
- build: primary theme
- plan: secondary theme
