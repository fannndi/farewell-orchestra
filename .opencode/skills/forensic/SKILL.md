---
name: forensic
description: Use when investigating codebase or debugging deep errors — evidence-first, file:line mandatory.
---

> Cost Model: free sub-agent — read-only, no edits. Writes → dispatch executor. Orchestrator never writes code.

# Forensic Investigation

Read-only. Setiap byte output bayar token. Jadi SETIAP kata harus punya nilai bukti.

## Evidence Standard

- **WAJIB:** `file:line` untuk setiap klaim
- **Format:** `path:42 — deskripsi singkat`
- **Satu finding = satu baris.** Detail hanya kalau kritis.
- **Confidence <90%:** kasih tag `(70% — butuh konfirmasi)`

## Search Protocol

1. `glob` — pahami struktur
2. `grep` — temukan titik masuk (entry point)
3. `read` — konfirmasi dengan bukti
4. **Jangan announce tool call.** Just do it.

## Cross-File Tracing

- Ikuti **data flow**, bukan call stack
- Trace dari input → transform → output
- Tiap hop antar file → catat `file:line` asal dan tujuan

## Domain Mapping

| Domain | Approach |
|--------|----------|
| Code analysis | glob → grep → read, cross-file call chains |
| Bug diagnosis | trace symptom → root cause, follow data flow |
| API surface | endpoints, method, input, output, auth |
| Config/infra | .env, docker, CI, deployment |

## Deep Debugging

Dipanggil saat executor gagal >2x. Prosedur:

1. **Reproduce error** — baca error message, stack trace, kondisi trigger
2. **Trace backward** — dari symptom ke call site, dari call site ke dependency
3. **Framework internals** — kalau error dari library/framework, baca source code upstream (node_modules, vendor, atau repo GitHub)
4. **Root cause** — trace ke penyebab fundamental. Cek env (versi runtime, OS, env vars).
**Output:** root cause (1 baris) + fix strategy (1 baris) + confidence.

## Tech Stack Forensics

Setiap dependency/rekomendasi library:

| Cek | Pertanyaan |
|-----|-----------|
| Maintenance | Terakhir update kapan? Maintainer masih aktif? |
| Security | Ada CVE? GitHub Advisory? |
| Compatibility | Support versi kita? Alternatif? |

**Output:** rekomendasi (1 baris) + alasan (1 baris) + alternatif (kalau ada).

## Evidence Levels — dari better-harness (QoderAI)
| Level | Label | Artinya |
|-------|-------|---------|
| [P] Present | `[P]` | Bukti ada (file:line ditemukan) |
| [W] Wired | `[W]` | Cross-referenced (≥2 sumber independent setuju) |
| [E] Exercised | `[E]` | Terverifikasi via command/tool output |
| [O] Outcome | `[O]` | Acceptance criteria terpenuhi |

**Format laporan:** tiap finding WAJIB dikasih level. Contoh: `path:42 — [P] deskripsi`
- Confidence <90% → tetap tag "(butuh verifikasi)" di belakang level.
- Not found → `"Dicari di X,Y,Z. Tidak ditemukan."`


