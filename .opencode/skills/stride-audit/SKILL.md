---
name: stride-audit
description: Use when reviewing code changes — STRIDE threat model, cumulative judgment, convention enforcement
---

# STRIDE Audit

Audit keamanan + arsitektur. Read-only. Setiap finding harus justified. Kalau nggak akan mengubah kode → skip.

## Priority Tags

| Tag | Trigger | Action |
|-----|---------|--------|
| **[BLOCKING]** | Data loss, security hole, crash | Harus diperbaiki sebelum merge |
| **[SHOULD]** | Edge case bug, maintenance pain | Perbaiki sekarang selagi fresh |
| **[NICE]** | Minor, style | Perbaiki kalau sentuh file itu |
| **[FYI]** | Observasi, bukan masalah | No action needed |

**Format:** `[TAG] path:42 — apa yang salah, kenapa, dampak`

## STRIDE Threat Model

| Threat | Cek |
|--------|-----|
| **S**poofing | Auth bypass? Token bisa dipalsukan? |
| **T**ampering | Data bisa dimodifikasi tanpa deteksi? |
| **R**epudiation | Action bisa disangkal? Ada audit log? |
| **I**nformation Disclosure | Data sensitif bocor? Error message leak? |
| **D**enial of Service | Rate limit? Timeout? Resource exhaustion? |
| **E**levation of Privilege | Role bypass? Task delegation escape? |

## Cumulative Judgment

- **Jangan cuma lihat per-file.** Lihat aggregate change.
- 3 file individual "aman" bisa combined jadi **BLOCKING** kalau bikin attack surface baru.
- Series of incremental "safe" changes bisa aggregate jadi risiko. Step back, assess whole.

## Domain Checklists

| Domain | Priority Checks |
|--------|----------------|
| Auth | Token lifecycle, session hijack, password policy |
| API | RESTfulness, error codes, rate limiting, idempotency |
| Database | Migration safety, index strategy, N+1, transactions |
| Error Handling | Degradation path, user messages, retry logic |
| Config | Env parity, secret rotation, health checks |

## Convention Enforcement

Sebelum audit keamanan, cek apakah kode comply dengan konvensi proyek:

1. **Rules.md** — aturan spesifik proyek (naming, struktur file, pattern yang dilarang)
2. **Architecture.md** — struktur direktori, layer, dependency rule
3. **Existing code** — ikut gaya file yang diedit? Nggak campur snake_case/camelCase?
4. **Project config** — ESLint, Prettier, tsconfig, editorconfig — kode comply?

**Yang dicek:** naming, struktur file, import order, error handling pattern, logging convention.

**Tag:** compliance violation → `[SHOULD]`. Tapi kalau violation menyebabkan bug/security issue → `[BLOCKING]`.

## Cross-File Consistency & Drift Detection

Audit bukan cuma per-file — tapi celah ANTAR file yang seharusnya sinkron.

### Drift Types

| Jenis | Cek |
|-------|-----|
| **Numeric drift** | Angka di 2+ file beda (steps, limit, versi) |
| **Structural drift** | Field ada di file A, hilang di file B |
| **Stale reference** | File A nunjuk ke file B yang udah nggak ada |
| **Silent divergence** | 2 file harusnya identik tapi udah beda |
| **Claim vs reality** | Docs bilang X, kenyataannya Y |

### Prosedur

1. Identifikasi grup file yang mengaku saling konsisten (config utama vs turunan, docs vs kode)
2. Cross-check klaim di docs ke sumber aslinya (config/kode), jangan percaya dokumentasi
3. Catat tiap drift walau "minor" — drift kecil hari ini = bug besar nanti

### Format temuan drift

`[TAG] fileA:baris ↔ fileB:baris — apa yang harusnya sama tapi beda`

## Checklist (order = priority)

1. **Correctness** — bugs, edge cases, race conditions
2. **Simplicity** — bisa lebih sederhana? bisa dihapus?
3. **Modularity** — coupling? penempatan tepat?
4. **Security** — misuse vectors, auth bypass, data leaks
5. **Consistency** — ikut pola proyek?

## Output

Summary: `"X BLOCKING, Y SHOULD, Z NICE, W FYI"` — lalu list findings 1 baris per finding.

**Jangan:** paragraf penjelasan, rekomendasi panjang, diskusi alternatif. 1 finding = 1 baris.
