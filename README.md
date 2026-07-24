# Farewell Orchestra

Workflow orchestration untuk OpenCode — foreground parallel research, review, dan controlled implementation via 9Router model gateway.

## Architecture

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────┐
│            orchestrator (primary · #7c3aed)      │
│  read-only · edit:deny · bash:deny              │
│  HEAVY model                                     │
└──────┬──────────────────────┬───────────────────┘
       │                      │
       ▼                      ▼
┌──────────────────┐  ┌──────────────────┐
│   researcher     │  │    reviewer      │
│   (subagent)     │  │   (subagent)     │
│   read-only      │  │   read-only      │
│   #3b82f6 · LIGHT│  │   #f59e0b · LIGHT│
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         └─────────┬───────────┘
                   │ synthesize
                   ▼
┌─────────────────────────────────────────────────┐
│            executor (subagent · #10b981)         │
│  write-only · bash:allow                        │
│  LIGHT model                                     │
└─────────────────────────────────────────────────┘
```

## Quick Start

```bash
git clone https://github.com/fannndi/farewell-orchestra
cd farewell-orchestra

# Set API key di .env (wajib)
echo NINEROUTER_API_KEY=sk_... > .env

# Pilih profile + start
switch.bat pro       # Pro (default)
switch.bat flash     # Flash (hemat token)
switch.bat free      # Free (max hemat)
switch.bat custom    # edit .env manual lalu run opencode
```

PowerShell: `.\switch.ps1 pro`

## Model Profiles

Switch via `switch.bat <profile>` — if/else logic, auto-tulis `.env`, auto-start opencode.

| Profile  | orchestrator (HEAVY)      | 7 workers (LIGHT)          |
|----------|--------------------------|---------------------------|
| **pro**  | `ocg/deepseek-v4-pro`   | `ocg/deepseek-v4-flash`   |
| **flash**| `ocg/deepseek-v4-flash` | `oc/deepseek-v4-flash-free` |
| **free** | `oc/deepseek-v4-flash-free` | `oc/deepseek-v4-flash-free` |
| **custom** | edit `.env` bebas      | edit `.env` bebas          |

**Role mapping:**
- **HEAVY** → orchestrator
- **LIGHT** → researcher, reviewer, executor, title, summary, compaction
- **BEBAS** → build, plan, general, explore (model pilih sendiri)

## Orchestration Rules

1. **Orchestrator NEVER edits files** — `edit:deny` enforced. Delegate ALL write to executor.
2. **Orchestrator NEVER runs shell** — `bash:deny` enforced. Executor is sole bash/write agent.
3. **ALWAYS run researcher + reviewer concurrently** — single message, multiple tool calls.
4. **ALWAYS wait for both results** — synthesize before delegating to executor.
5. **Each executor task is self-contained** — include scope, paths, constraints, expected output, verification.
6. **NEVER duplicate child work** — once delegated, do not repeat analysis yourself.
7. **Foreground-only** — no `background:true`. Await all results before proceeding.
8. **Keep task IDs per workflow** — reuse for same-agent continuation, fresh otherwise.

## All Roles (11 agents)

### 1. orchestrator — Workflow Coordinator

| Property    | Value |
|-------------|-------|
| **Mode**    | `primary` (selectable via Tab) |
| **Default** | Yes — `default_agent` |
| **Model**   | HEAVY (`{env:ORCHESTRA_HEAVY_MODEL}`) |
| **Color**   | `#7c3aed` (purple) |
| **Temperature** | `0.2` |
| **Max Steps** | `40` |

Koordinator utama. Read-only — tidak bisa edit/bash. Hanya delegasi ke researcher, reviewer, executor via `task:allow`.

### 2. researcher — Codebase Investigator

| Property    | Value |
|-------------|-------|
| **Mode**    | `subagent` |
| **Model**   | LIGHT (`{env:ORCHESTRA_LIGHT_MODEL}`) |
| **Color**   | `#3b82f6` (blue) |
| **Temperature** | `0.1` |
| **Max Steps** | `30` |

Read-only. Inspeksi kode, config, test, dokumentasi. `*:deny` kecuali read, glob, grep, list, webfetch, websearch, lsp, skill. `bash:deny`, `edit:deny`, `task:deny`.

### 3. reviewer — Security & Architecture Auditor

| Property    | Value |
|-------------|-------|
| **Mode**    | `subagent` |
| **Model**   | LIGHT (`{env:ORCHESTRA_LIGHT_MODEL}`) |
| **Color**   | `#f59e0b` (amber) |
| **Temperature** | `0.1` |
| **Max Steps** | `30` |

Read-only. Audit correctness, security, compatibility, concurrency, maintainability. Return temuan + acceptance criteria + rencana verifikasi.

### 4. executor — Implementation Worker

| Property    | Value |
|-------------|-------|
| **Mode**    | `subagent` |
| **Model**   | LIGHT (`{env:ORCHESTRA_LIGHT_MODEL}`) |
| **Color**   | `#10b981` (green) |
| **Max Steps** | `50` |

Satu-satunya agen dengan `edit:allow` + `bash:allow`. Scope dibatasi orchestrator. `task:deny` — tidak bisa delegasi.

### 5–8. Built-in OpenCode Agents

| Agent     | Mode      | Model  | Permission  |
|-----------|-----------|--------|-------------|
| `build`   | primary   | bebas  | `task:deny` |
| `plan`    | primary   | bebas  | `task:deny` |
| `general` | subagent  | bebas  | `task:deny` |
| `explore` | subagent  | bebas  | `task:deny` |

Escape hatches — model bebas dipilih user.

### 9–11. Internal Agents (hidden)

| Agent        | Model  | Purpose                              |
|--------------|--------|--------------------------------------|
| `title`      | LIGHT  | Auto-generate judul sesi             |
| `summary`    | LIGHT  | Ringkasan sesi                       |
| `compaction` | LIGHT  | Kompaksi konteks saat window penuh   |

## Slash Commands

| Command     | Agent              | Description                                  |
|-------------|--------------------|----------------------------------------------|
| `/status`   | orchestrator       | Health: agent, model, token                   |
| `/fanout`   | orchestrator       | researcher + reviewer parallel → executor     |
| `/review`   | reviewer (subtask) | Code audit — no edits                         |
| `/execute`  | executor (subtask) | Implementasi langsung                         |

## Session Flow

```
1. User request
2. /status → verify health
3. Decompose → independent work packages
4. /fanout → researcher + reviewer PARALLEL
5. Synthesize both results
6. /execute → executor implements
7. Report to user
```

## Permission Matrix

| Agent          | edit  | bash  | task                | webfetch | question |
|----------------|-------|-------|---------------------|----------|----------|
| orchestrator   | deny  | deny  | researcher,reviewer,executor only | allow | allow |
| researcher     | deny  | deny  | deny                | allow    | —        |
| reviewer       | deny  | deny  | deny                | allow    | —        |
| executor       | allow | allow | deny                | —        | —        |
| build          | allow | allow | deny                | allow    | allow |
| plan           | deny  | ask   | deny                | allow    | allow |
| general        | allow | allow | deny                | allow    | —        |
| explore        | deny  | allow | deny                | allow    | —        |
| title          | deny  | deny  | deny                | —        | —        |
| summary        | deny  | deny  | deny                | —        | —        |
| compaction     | deny  | deny  | deny                | —        | —        |

## Configuration

| Feature           | Setting                              |
|-------------------|--------------------------------------|
| Provider          | 9Router via `@ai-sdk/openai-compatible` |
| Auth              | `{env:NINEROUTER_API_KEY}`           |
| Default agent     | `orchestrator`                       |
| Subagent depth     | `1` (workers can't delegate)          |
| Snapshot          | `true` (undo/revert enabled)          |
| Autoupdate        | `notify`                              |
| Shell             | `powershell`                          |
| LSP / Formatter   | `true`                                |

## Files

| File              | Purpose                                       |
|-------------------|-----------------------------------------------|
| `opencode.jsonc`  | Agent config, permissions, commands            |
| `.env.example`    | Env var template                               |
| `switch.bat`      | If/else profile switch + auto-start opencode   |
| `switch.ps1`      | PowerShell version                             |
| `AGENTS.md`       | 8 orchestration rules                          |
| `README.md`       | This file                                      |

## License

MIT
