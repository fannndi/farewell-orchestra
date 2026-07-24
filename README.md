# Farewell Orchestra

Workflow orchestration untuk OpenCode — foreground parallel research, review, dan controlled implementation via 9Router model gateway.

## Arsitektur

```
User Request
    │
    ▼
┌─────────────────────────────────────┐
│          orchestrator (primary)      │
│  read-only · edit:deny · bash:deny   │
│  model: ocg/deepseek-v4-pro         │
└──────┬──────────────────┬───────────┘
       │                  │
       ▼                  ▼
┌──────────────┐  ┌──────────────┐
│  researcher  │  │   reviewer   │
│  (subagent)  │  │  (subagent)  │
│  read-only   │  │  read-only   │
│  flash       │  │  flash       │
└──────────────┘  └──────────────┘
       │                  │
       └──────┬───────────┘
              │ synthesize
              ▼
┌─────────────────────────────────────┐
│           executor (subagent)        │
│  write-only · bash:allow            │
│  model: ocg/deepseek-v4-pro         │
└─────────────────────────────────────┘
```

## Role

### 1. orchestrator (primary · default)
**Model:** `ocg/deepseek-v4-pro` (bisa diganti manual)

Orchestrator adalah koordinator utama. Tugasnya:
- Menerima permintaan user dan mendekomposisi menjadi work package independen
- Memanggil **researcher** dan **reviewer** secara paralel (foreground) untuk analisis read-only
- Menunggu dan mensintesis hasil keduanya sebelum memutuskan implementasi
- Mendelegasikan SEMUA modifikasi file ke **executor** sebagai satu task terfokus

**Permission:**
- `edit: deny`, `bash: deny` — tidak bisa menulis atau menjalankan command
- `question: allow`, `todowrite: allow` — bisa tanya user dan bikin TODO
- `task: allow` hanya untuk `researcher`, `reviewer`, `executor`

### 2. researcher (subagent)
**Model:** `ocg/deepseek-v4-flash` (bisa diganti manual)

Researcher adalah agen read-only untuk investigasi codebase. Tugasnya:
- Inspeksi kode, konfigurasi, test, dan dokumentasi
- Return bukti dengan path file dan nomor baris, asumsi, risiko, dan rekomendasi
- **Tidak boleh** edit file, jalankan shell command, delegasi kerja, atau implementasi

**Permission:** `*: deny` kecuali `read, glob, grep, list, webfetch, websearch, lsp, skill`

### 3. reviewer (subagent)
**Model:** `ocg/deepseek-v4-flash` (bisa diganti manual)

Reviewer adalah agen read-only untuk validasi arsitektur, keamanan, dan perencanaan verifikasi. Tugasnya:
- Identifikasi risiko correctness, security, compatibility, concurrency, dan maintainability
- Return temuan prioritas, acceptance criteria, dan rencana verifikasi
- **Tidak boleh** edit file, jalankan shell command, delegasi kerja, atau implementasi

**Permission:** `*: deny` kecuali `read, glob, grep, list, webfetch, websearch, lsp, skill`

### 4. executor (subagent)
**Model:** `ocg/deepseek-v4-pro` (bisa diganti manual)

Executor adalah satu-satunya agen yang bisa menulis file. Tugasnya:
- Implementasi hanya scope yang diberikan orchestrator
- Inspeksi file terkait, ikuti konvensi lokal, lakukan edit terfokus
- Jalankan perintah verifikasi, laporkan file yang berubah dan hasilnya
- **Tidak boleh** delegasi kerja, memperluas scope, atau modifikasi file di luar change set

**Permission:** `read, edit, glob, grep, list, bash, lsp, skill` · `task: deny`

### 5. build / plan / general / explore (built-in OpenCode)
Mode bawaan OpenCode tetap tersedia sebagai escape hatch — bisa diganti model secara bebas. `build` dan `plan` adalah primary agents; `general` dan `explore` adalah subagents.

### Internal (hidden)
`title`, `summary`, `compaction` — sistem agent OpenCode internal, tidak terlihat di UI.

## Model

Dua model via 9Router gateway (OpenAI-compatible di `http://127.0.0.1:20128/v1`):

| Model | Alokasi |
|---|---|
| `ocg/deepseek-v4-pro` | orchestrator, executor, compaction |
| `ocg/deepseek-v4-flash` | researcher, reviewer, title, summary |

Untuk ganti model: edit field `model` di tiap agent di `opencode.jsonc`.

## Foreground Parallel Flow

1. User memberikan request kompleks
2. Orchestrator dekomposisi menjadi work package independen
3. Researcher dan reviewer dipanggil **bersamaan** dalam satu turn
4. Orchestrator menunggu hasil keduanya, lalu mensintesis
5. Executor dipanggil dengan scope terbatas untuk implementasi
6. Hasil dilaporkan ke user

Tidak ada background task. Semua foreground — orchestrator menunggu sebelum lanjut.

## Konfigurasi

Semua konfigurasi ada di `opencode.jsonc`. Tidak ada MCP server, skill, persona, atau Python package — murni orchestration via OpenCode config.

## Environment

```bash
export NINEROUTER_API_KEY="sk_..."
# atau set di Windows:
set NINEROUTER_API_KEY=sk_...
```

## Lisensi

MIT
