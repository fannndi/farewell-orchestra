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

## Roles

### orchestrator (primary · default · `#7c3aed`)
**Model:** `ocg/deepseek-v4-pro`

Koordinator utama. Tidak bisa menulis atau menjalankan shell.
- Mendelegasikan riset ke researcher + reviewer secara paralel
- Mensintesis hasil keduanya
- Mendelegasikan implementasi ke executor
- `task:allow` hanya untuk researcher, reviewer, executor

### researcher (subagent · `#3b82f6`)
**Model:** `ocg/deepseek-v4-flash`

Read-only. Inspeksi kode, config, test, dokumentasi. Return bukti + rekomendasi.
- `*:deny` kecuali read, glob, grep, list, webfetch, websearch, lsp, skill

### reviewer (subagent · `#f59e0b`)
**Model:** `ocg/deepseek-v4-flash`

Read-only. Audit arsitektur, keamanan, correctness. Return temuan prioritas + acceptance criteria.
- `*:deny` kecuali read, glob, grep, list, webfetch, websearch, lsp, skill

### executor (subagent · `#10b981`)
**Model:** `ocg/deepseek-v4-pro`

Satu-satunya yang bisa menulis file dan menjalankan shell. Scope dibatasi orchestrator.
- `task:deny` — tidak bisa delegasi

### Escape Hatches (built-in OpenCode)
`build` dan `plan` tetap tersedia sebagai primary agents — model bebas diganti kapan saja. `general` dan `explore` tersedia sebagai subagents. Semua `task:deny`.

## Slash Commands

| Command    | Description                                       |
|-----------|---------------------------------------------------|
| `/status` | Orchestration health check                        |
| `/fanout` | Decompose → researcher + reviewer → executor      |
| `/review` | Code-only review via reviewer subagent            |

## Model Allocation

| Model                      | Roles                        |
|---------------------------|------------------------------|
| `ocg/deepseek-v4-pro`    | orchestrator, executor, compaction |
| `ocg/deepseek-v4-flash`  | researcher, reviewer, title, summary |

Ganti model: edit field `model` di agent terkait di `opencode.jsonc`.

## Quick Start

```bash
git clone https://github.com/fannndi/farewell-orchestra
cd farewell-orchestra
set NINEROUTER_API_KEY=sk_...
opencode run "Hello"
```

## Files

| File             | Purpose                                      |
|-----------------|----------------------------------------------|
| `opencode.jsonc` | Full config: agents, permissions, commands   |
| `AGENTS.md`      | Agent instructions + orchestration rules     |
| `README.md`      | This file                                    |

## License

MIT
