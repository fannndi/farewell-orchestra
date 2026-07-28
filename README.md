# Farewell Orchestra

Agent orchestration framework untuk OpenCode. Empat AI agent (orchestrator, researcher, reviewer, executor) kerja bareng ngerjain task dari Boss.

## Cara Pake

Jalanin `opencode` di folder ini, kasih task. Orchestrator bakal decomposisi, fan-out ke researcher+reviewer parallel, sintesis, delegasi ke executor.

## Profile

```
switch.bat     # atau switch.sh
```

| # | Profile | Model |
|:-:|---------|-------|
| 1 | **V1** (Default) | orchestrator=deepseek-v4-flash · researcher=deepseek-v4-flash-free · reviewer/executor=north-mini-code-free |
| 2 | **Limited** | orchestrator/researcher=ollama/minimax-m3 · reviewer/executor=north-mini-code-free |

Pilih 1 atau 2, restart opencode.

## Architecture

| Agent | Role | Model (V1) |
|-------|------|-----------|
| orchestrator | Tech Lead — validasi, dekomposisi, delegasi | deepseek-v4-flash |
| researcher | Forensic investigator — evidence file:line | deepseek-v4-flash-free |
| reviewer | QA/Security — STRIDE audit, [BLOCKING] | north-mini-code-free |
| executor | Developer — YAGNI-first, verify-first | north-mini-code-free |

Detail lengkap: `AGENTS.md`, `.opencode/agents/`, `.opencode/skills/`.