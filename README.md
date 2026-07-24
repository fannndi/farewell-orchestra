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
│  model: ocg/deepseek-v4-pro                     │
└──────┬──────────────────────┬───────────────────┘
       │                      │
       ▼                      ▼
┌──────────────────┐  ┌──────────────────┐
│   researcher     │  │    reviewer      │
│   (subagent)     │  │   (subagent)     │
│   read-only      │  │   read-only      │
│   #3b82f6 · flash│  │   #f59e0b · flash│
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         └─────────┬───────────┘
                   │ synthesize
                   ▼
┌─────────────────────────────────────────────────┐
│            executor (subagent · #10b981)         │
│  write-only · bash:allow                        │
│  model: ocg/deepseek-v4-pro                     │
└─────────────────────────────────────────────────┘
```

## Orchestration Rules

1. **Orchestrator NEVER edits files** — `edit:deny` enforced. Delegate ALL write to executor.
2. **Orchestrator NEVER runs shell** — `bash:deny` enforced. Executor is sole bash/write agent.
3. **ALWAYS run researcher + reviewer concurrently** — single message, multiple tool calls.
4. **ALWAYS wait for both results** — synthesize before delegating to executor.
5. **Each executor task is self-contained** — include scope, paths, constraints, expected output, verification.
6. **NEVER duplicate child work** — once delegated, do not repeat analysis yourself.
7. **Foreground-only** — no `background:true`. Await all results before proceeding.
8. **Keep task IDs per workflow** — reuse for same-agent continuation, fresh otherwise.

## Roles

### orchestrator (primary · default · `#7c3aed`)
**Model:** `ocg/deepseek-v4-pro` · **temp:** `0.2` · **max steps:** `40`

Koordinator utama. Read-only — tidak bisa menulis atau menjalankan shell.
- Fan-out independent analysis ke researcher + reviewer secara paralel
- Mensintesis hasil sebelum memutuskan implementasi
- Delegasi semua file modifikasi ke executor sebagai satu task terfokus
- `task:allow` hanya untuk `researcher`, `reviewer`, `executor`
- `question:allow`, `todowrite:allow`

### researcher (subagent · `#3b82f6`)
**Model:** `ocg/deepseek-v4-flash` · **temp:** `0.1` · **max steps:** `30`

Read-only code investigator. Inspeksi kode, config, test, dokumentasi.
- `*:deny` baseline — hanya `read`, `glob`, `grep`, `list`, `webfetch`, `websearch`, `lsp`, `skill`
- Return bukti dengan file path + line number, asumsi, risiko, rekomendasi
- Tidak boleh edit, bash, delegasi, atau implementasi

### reviewer (subagent · `#f59e0b`)
**Model:** `ocg/deepseek-v4-flash` · **temp:** `0.1` · **max steps:** `30`

Read-only security/correctness auditor.
- `*:deny` baseline — sama dengan researcher
- Identifikasi risiko correctness, security, compatibility, concurrency, maintainability
- Return temuan prioritas, acceptance criteria, rencana verifikasi
- Tidak boleh edit, bash, delegasi, atau implementasi

### executor (subagent · `#10b981`)
**Model:** `ocg/deepseek-v4-pro` · **max steps:** `50`

Satu-satunya agen yang bisa menulis file dan menjalankan shell.
- `read`, `edit`, `glob`, `grep`, `list`, `bash`, `lsp`, `skill`
- `task:deny` — tidak bisa mendelegasikan ke subagent lain
- Scope implementasi dibatasi oleh task prompt dari orchestrator

### Escape Hatches (built-in OpenCode)
`build` dan `plan` tetap tersedia sebagai primary agents dengan model bebas. `general` dan `explore` sebagai subagents. Semua `task:deny`.

### Internal Agents (hidden)
`title`, `summary`, `compaction` — sistem agent OpenCode. `title`/`summary` pakai flash, `compaction` pakai pro.

## Slash Commands

| Command     | Description                                              |
|------------|----------------------------------------------------------|
| `/status`  | Orchestration health: active agent, model, token usage    |
| `/fanout`  | Decompose → researcher + reviewer → executor             |
| `/review`  | Code-only review via reviewer subagent, no edits          |
| `/execute` | Delegate implementation langsung ke executor              |

## Session Flow

```
1. User request
2. /status — verify orchestration health
3. Decompose into independent work packages
4. /fanout — researcher + reviewer run in PARALLEL
5. Synthesize both results
6. /execute — executor implements focused change
7. Report to user
```

## Model Allocation

| Model                       | Roles                                       | Context | Output  |
|-----------------------------|---------------------------------------------|---------|---------|
| `ocg/deepseek-v4-pro`      | orchestrator, executor, compaction           | 1M      | 128K    |
| `ocg/deepseek-v4-flash`    | researcher, reviewer, title, summary         | 1M      | 128K    |

Ganti model: edit field `model` di agent terkait di `opencode.jsonc`.

## Configuration

Semua konfigurasi di `opencode.jsonc` — fully commented JSONC. Highlights:

| Feature              | Setting                              |
|----------------------|--------------------------------------|
| Schema validation    | `$schema: opencode.ai/config.json`   |
| Provider             | 9Router via `@ai-sdk/openai-compatible` |
| Auth                 | `{env:NINEROUTER_API_KEY}`           |
| Default agent        | `orchestrator`                       |
| Subagent depth        | `1` (workers can't delegate)          |
| Snapshot             | `true` (undo/revert enabled)          |
| Autoupdate           | `notify` (alert, don't auto-install) |
| Shell                | `powershell` (Windows)               |
| LSP / Formatter      | `true`                                |

## Quick Start

```bash
git clone https://github.com/fannndi/farewell-orchestra
cd farewell-orchestra
set NINEROUTER_API_KEY=sk_...
opencode run "Hello"
```

## Files

| File              | Purpose                                       |
|-------------------|-----------------------------------------------|
| `opencode.jsonc`  | Full config: agents, permissions, commands     |
| `AGENTS.md`       | 8 orchestration rules + session flow           |
| `README.md`       | This file                                     |

## License

MIT
