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
│   #3b82f6 flash   │  │   #f59e0b flash   │
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

---

## All Roles (11 agents)

### 1. orchestrator — Workflow Coordinator

| Property    | Value |
|-------------|-------|
| **Mode**    | `primary` (selectable via Tab) |
| **Default** | Yes — `default_agent` |
| **Model**   | `ocg/deepseek-v4-pro` |
| **Color**   | `#7c3aed` (purple) |
| **Temperature** | `0.2` (focused, deterministic) |
| **Max Steps** | `40` |
| **Visible** | Yes |

**Purpose:** Koordinator utama seluruh workflow. Tidak bisa menulis file (`edit:deny`) dan tidak bisa menjalankan shell (`bash:deny`). Tugasnya murni analisis, dekomposisi, dan delegasi.

**Allowed tools:**
- `question:allow` — bisa bertanya ke user untuk klarifikasi
- `todowrite:allow` — bisa membuat dan mengelola task list
- `task:allow` hanya untuk `researcher`, `reviewer`, `executor`
- Selebihnya inherited dari global permission baseline (read, glob, grep, list, lsp, skill, webfetch, websearch)

**Workflow:**
1. Terima request user
2. Dekomposisi menjadi work package independen
3. Panggil researcher + reviewer secara paralel (foreground, satu turn)
4. Tunggu dan sintesis hasil keduanya
5. Delegasi implementasi ke executor sebagai satu task terfokus
6. Laporkan hasil ke user

---

### 2. researcher — Codebase Investigator

| Property    | Value |
|-------------|-------|
| **Mode**    | `subagent` (dipanggil via task tool) |
| **Model**   | `ocg/deepseek-v4-flash` |
| **Color**   | `#3b82f6` (blue) |
| **Temperature** | `0.1` (very focused) |
| **Max Steps** | `30` |
| **Visible** | Yes |

**Purpose:** Agen investigasi codebase read-only. Dipanggil orchestrator untuk menginspeksi kode, konfigurasi, test, dan dokumentasi secara mendalam.

**Permission baseline:** `*:deny`
- `read:allow` — membaca file
- `glob:allow` — mencari file berdasarkan pattern
- `grep:allow` — mencari konten dalam file
- `list:allow` — list direktori
- `webfetch:allow` — fetch dokumentasi eksternal
- `websearch:allow` — search web untuk konteks tambahan
- `lsp:allow` — language server (jump-to-def, diagnostics)
- `skill:allow` — load skill spesifik domain
- `task:deny` — tidak bisa delegasi ke agent lain
- `bash:deny` — tidak bisa menjalankan shell command
- `edit:deny` — tidak bisa mengubah file

**Expected output:** Bukti dengan path file + nomor baris, asumsi, risiko, dan rekomendasi konkret.

---

### 3. reviewer — Security and Architecture Auditor

| Property    | Value |
|-------------|-------|
| **Mode**    | `subagent` (dipanggil via task tool) |
| **Model**   | `ocg/deepseek-v4-flash` |
| **Color**   | `#f59e0b` (amber/yellow) |
| **Temperature** | `0.1` (very focused) |
| **Max Steps** | `30` |
| **Visible** | Yes |

**Purpose:** Agen audit read-only. Dipanggil orchestrator untuk validasi arsitektur, keamanan, dan correctness sebelum implementasi.

**Permission baseline:** `*:deny`
- `read:allow` — membaca file
- `glob:allow` — mencari file
- `grep:allow` — mencari konten
- `list:allow` — list direktori
- `webfetch:allow` — fetch referensi eksternal
- `websearch:allow` — search web
- `lsp:allow` — language server
- `skill:allow` — load skill
- `task:deny` — tidak bisa delegasi
- `bash:deny` — tidak bisa shell command
- `edit:deny` — tidak bisa mengubah file

**Expected output:** Temuan prioritas risiko (correctness, security, compatibility, concurrency, maintainability), acceptance criteria, dan rencana verifikasi. Semua dengan path file + nomor baris.

---

### 4. executor — Implementation Worker

| Property    | Value |
|-------------|-------|
| **Mode**    | `subagent` (dipanggil via task tool) |
| **Model**   | `ocg/deepseek-v4-pro` |
| **Color**   | `#10b981` (green) |
| **Max Steps** | `50` |
| **Visible** | Yes |

**Purpose:** Satu-satunya agen yang bisa menulis file dan menjalankan shell command. Dipanggil orchestrator SETELAH riset dan review selesai.

**Allowed tools:**
- `read:allow` — membaca file untuk inspeksi
- `edit:allow` — menulis/mengubah file (satu-satunya agent dengan akses ini)
- `glob:allow` — mencari file
- `grep:allow` — mencari konten
- `list:allow` — list direktori
- `bash:allow` — menjalankan shell command (termasuk test, build, git)
- `lsp:allow` — language server
- `skill:allow` — load skill
- `task:deny` — tidak bisa mendelegasikan ke subagent lain

**Pembatasan:** Scope implementasi dibatasi oleh task prompt dari orchestrator.

**Expected output:** Daftar file yang berubah + hasil verifikasi.

---

### 5. build — OpenCode Built-in Primary

| Property    | Value |
|-------------|-------|
| **Mode**    | `primary` (selectable via Tab) |
| **Model**   | Bebas — fallback ke global `model` |
| **Color**   | `primary` (theme default) |
| **Visible** | Yes |

**Purpose:** Agent bawaan OpenCode untuk development penuh akses — semua tools enabled. Escape hatch jika user butuh akses langsung tanpa orchestration.

**Permission override:** `task:deny` — tidak bisa memanggil subagent.

---

### 6. plan — OpenCode Built-in Primary

| Property    | Value |
|-------------|-------|
| **Mode**    | `primary` (selectable via Tab) |
| **Model**   | Bebas — fallback ke global `model` |
| **Color**   | `secondary` (theme accent) |
| **Visible** | Yes |

**Purpose:** Agent bawaan untuk planning/analisis. Edit dan bash di-set `ask` oleh OpenCode.

**Permission override:** `task:deny` — tidak bisa memanggil subagent.

---

### 7. general — OpenCode Built-in Subagent

| Property    | Value |
|-------------|-------|
| **Mode**    | `subagent` |
| **Model**   | Bebas — inherits parent model |
| **Visible** | Yes |

**Purpose:** General-purpose agent untuk riset dan task multi-langkah. Bisa dipanggil manual via `@general`.

**Permission override:** `task:deny` — tidak bisa memanggil subagent lain.

---

### 8. explore — OpenCode Built-in Subagent

| Property    | Value |
|-------------|-------|
| **Mode**    | `subagent` |
| **Model**   | Bebas — inherits parent model |
| **Visible** | Yes |

**Purpose:** Fast, read-only codebase explorer. Tidak bisa mengubah file. Cocok untuk pencarian cepat.

**Permission override:** `task:deny` — tidak bisa memanggil subagent lain.

---

### 9. title — Session Title Generator (Internal)

| Property    | Value |
|-------------|-------|
| **Mode**    | `primary` |
| **Model**   | `ocg/deepseek-v4-flash` |
| **Hidden**  | Yes — tidak muncul di UI |

**Purpose:** Agen internal OpenCode untuk membuat judul sesi otomatis. Berjalan di background setelah turn pertama. Semua tools di-deny.

---

### 10. summary — Session Summary Generator (Internal)

| Property    | Value |
|-------------|-------|
| **Mode**    | `primary` |
| **Model**   | `ocg/deepseek-v4-flash` |
| **Hidden**  | Yes — tidak muncul di UI |

**Purpose:** Agen internal untuk ringkasan sesi. Semua tools di-deny.

---

### 11. compaction — Context Compressor (Internal)

| Property    | Value |
|-------------|-------|
| **Mode**    | `primary` |
| **Model**   | `ocg/deepseek-v4-pro` |
| **Hidden**  | Yes — tidak muncul di UI |

**Purpose:** Agen internal untuk kompaksi konteks. Otomatis saat context window penuh. Kenapa Pro: compaction menghasilkan ringkasan yang dipakai di turn berikutnya — butuh reasoning kuat.

**Konfigurasi:** `auto: true`, `prune: false`, `tail_turns: 2`

---

## Slash Commands

| Command     | Agent       | Description                                       |
|-------------|-------------|---------------------------------------------------|
| `/status`   | orchestrator | Orchestration health check                         |
| `/fanout`   | orchestrator | Decompose -> researcher + reviewer -> executor     |
| `/review`   | reviewer (subtask) | Code review only, no edits                   |
| `/execute`  | executor (subtask) | Delegate implementation langsung             |

## Session Flow

```
1. User submits request
2. orchestrator runs /status -> verify health
3. orchestrator decomposes into independent work packages
4. orchestrator calls /fanout -> researcher + reviewer in PARALLEL
5. orchestrator waits for both, synthesizes results
6. orchestrator calls /execute -> executor implements
7. orchestrator reports results to user
```

## Model Allocation

| Model                       | Roles                                          | Context | Output |
|-----------------------------|------------------------------------------------|---------|--------|
| `ocg/deepseek-v4-pro`      | orchestrator, executor, compaction              | 1M      | 128K   |
| `ocg/deepseek-v4-flash`    | researcher, reviewer, title, summary            | 1M      | 128K   |
| *(bebas)*                   | build, plan, general, explore                   | —       | —      |

## Permission Matrix

| Agent          | edit  | bash  | task            | webfetch | question |
|----------------|-------|-------|-----------------|----------|----------|
| orchestrator   | deny  | deny  | researcher/reviewer/executor only | allow | allow |
| researcher     | deny  | deny  | deny            | allow    | —        |
| reviewer       | deny  | deny  | deny            | allow    | —        |
| executor       | allow | allow | deny            | —        | —        |
| build          | allow | allow | deny            | allow    | allow |
| plan           | deny  | ask   | deny            | allow    | allow |
| general        | allow | allow | deny            | allow    | —        |
| explore        | deny  | allow | deny            | allow    | —        |
| title          | deny  | deny  | deny            | —        | —        |
| summary        | deny  | deny  | deny            | —        | —        |
| compaction     | deny  | deny  | deny            | —        | —        |

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
| `AGENTS.md`       | 8 rules + session flow                         |
| `README.md`       | Comprehensive reference (this file)            |

## License

MIT