---
name: research
description: Use when investigating codebase or external sources — evidence-first, file:line mandatory.
---

# Research

Read-only. Codebase forensics + web research. Setiap klaim WAJIB punya `file:line` atau `URL`.

## Simplified Mode (untuk LLM lemah)

Kalau LLM tidak bisa handle complex instructions:

1. **Cari** — glob/grep untuk temukan file relevan
2. **Baca** — baca file yang ditemukan
3. **Lapor** — format: `<file>:<line> — <temuan>`

Contoh: `src/auth.py:42 — JWT tanpa signature verification`

Jangan pakai [LEVEL] kalau bingung. Cukup file:line + temuan.

## Kapan Pakai Mana

| Scope | Tool |
|-------|------|
| Kode sendiri / codebase | Codebase Investigation (§1) |
| Fakta eksternal / library / API | Web Research (§2) |
| Keduanya | Codebase dulu, web kalau kurang |

## 1. Codebase Investigation

**Search Protocol:**
1. `glob` — pahami struktur
2. `grep` — temukan entry point
3. `read` — konfirmasi dengan bukti
4. 3x search angle beda tetap kosong → lapor "Dicari di X,Y,Z. Tidak ditemukan." STOP.

**Cross-file tracing:** Ikuti data flow (input → transform → output), bukan call stack. Tiap hop → catat `file:line` asal dan tujuan.

**Multi-match:** Grep return puluhan hit? Prioritaskan file dekat entrypoint/nama fungsi yang di-mention di brief dulu, baru fallback ke recency (`git log -1`).

**Evidence kontradiktif** (2 code path beda perilaku)? Cari 1-2 titik tambahan (caller/config/flag) buat disambiguasi — lapor both + confidence level.

**Domain Mapping:**

| Domain | Approach |
|--------|----------|
| Code analysis | glob → grep → read, cross-file call chains |
| Bug diagnosis | trace symptom → root cause, follow data flow |
| API surface | endpoints, method, input, output, auth |
| Config/infra | .env, docker, CI, deployment |

**Deep Debugging** (dipanggil saat executor gagal 2x):
1. Reproduce error — baca error message, stack trace, kondisi trigger
2. Trace backward — dari symptom ke call site, dari call site ke dependency
3. Framework internals — kalau error dari library, baca source upstream
4. Root cause — trace ke penyebab fundamental. Cek env (versi runtime, OS, env vars).

Output: root cause (1 baris) + fix strategy (1 baris).

**Tech Stack Forensics** — setiap dependency/rekomendasi:

| Cek | Pertanyaan |
|-----|-----------|
| Maintenance | Terakhir update kapan? Maintainer aktif? |
| Security | Ada CVE? GitHub Advisory? |
| Compatibility | Support versi kita? Alternatif? |
| Deprecated | Ada di npm deprecated? Ada successor? |

**Explicit Deprecation Enforcement (WAJIB untuk weak LLM):**

| Step | Check | Fail Action |
|------|-------|-------------|
| 1 | Baca package.json/requirements.txt | Tidak baca → report: "Cannot check dependencies" |
| 2 | Cek setiap dependency untuk deprecated | Tidak cek → report: "Dependencies not checked" |
| 3 | Kalau ada deprecated → flag | Tidak flag → BLOCKING |
| 4 | Report: "Deprecated: [package] → use [alternative]" | Format salah → re-dispatch |

**Log Fallback** — kalau logs tidak ditemukan:
1. Cek: console.log, stderr, stdout
2. Cek: .log files di root / logs/ / var/log/
3. Cek: Docker logs (docker logs <container>)
4. Cek: systemd journal (journalctl)
5. Tidak ada → lapor: "No logs found. Need to add logging."

**Circular Dependency Detection** — kalau trace dependency:
1. Catat setiap hop: A -> B -> C
2. Kalau C -> A (loop balik) → flag: "Circular dependency: A -> B -> C -> A"
3. Lapor ke orchestrator: "Circular dependency detected. Need refactor?"

## 2. Web Research

**Decision Gate:**
- **Skip search** kalau: fakta stabil, subjek mati/discontinued, query tidak minta "current/latest", lo 100% yakin.
- **WAJIB search** kalau: status terkini, harga/kebijakan/versi, library yang tidak dikenal, angka spesifik/statistik.

**Protocol:**
- Query pendek 2-6 kata, satu fakta per query
- Multi-query: bikin 2-3 variasi query untuk 1 pertanyaan
- Max 5 URL per batch, prioritas: docs resmi > blog > news > forum
- Max 3 iterasi re-query kalau hasil kurang

**Copyright:** Parafrase, jangan quote. Max 15 kata kalau terpaksa. Jangan mirror struktur artikel sumber.

**Refuse to search:** konten ekstremis, tools bypass safety, stalking/surveillance.

## Output Format

Satu finding = satu baris:

```
file:line — [LEVEL] deskripsi
```

Level:
- `P` — Present: bukti ada (file:line ditemukan)
- `W` — Wired: ≥2 sumber independent setuju
- `E` — Exercised: verified via command/tool output
- `O` — Outcome: acceptance criteria terpenuhi

Web finding: `URL — deskripsi`

**Jangan announce tool call.** Just do it.
