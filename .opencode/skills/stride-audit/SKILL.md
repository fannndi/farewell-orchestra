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

## Depth Assurance Protocol

JANGAN lapor "Done" SEBELUM 3 pass ini selesai:

### Pass 1: Scan (5%)
- Baca README/docs → pahami klaim, arsitektur, fitur
- Catat semua klaim yg harus diverifikasi
- ⚠️ JANGAN percaya README. README bilang X, kode harus X.

### Pass 2: Detail (70%)
- Baca kode ASLI — bukan cuma struktur direktori
- Untuk setiap fungsi/fitur penting:
  1. Baca entry point (main/CLI/index)
  2. Ikuti alur ke file-file terkait (import chain)
  3. Catat implementasi aktual vs klaim docs
- Verifikasi 3 hal: (a) apakah kode sesuai docs? (b) apakah ada yg terlewat? (c) apakah ada celah?

### Pass 3: Cross-Reference (25%)
- Bandingkan temuan dari Pass 2 dengan klaim dari Pass 1
- Cari kontradiksi: docs bilang X, kode lakukan Y
- Cari missing pieces: docs janji Z, tapi kode gak ada Z
- Format temuan: `[TAG] path:42 — docs claim X, tapi kode lakukan Y`

**Self-Check Sebelum Report:**
| Pertanyaan | Ya/Tidak |
|------------|----------|
| Udah baca file kode asli (bukan cuma README)? | ❌ kalau belum → jangan report |
| Udah ikutin minimal 1 import chain dari entry point? | ❌ kalau belum → jangan claim paham |
| Ada klaim di docs yg belum diverifikasi ke kode? | ❌ kalau ada → catat sebagai "unverified" |
| Risiko ada yg terlewat? (skala 1-5) | ≥3 → tambah disclaimer |

## Skepticism Layer

Prinsip: **"Dokumentasi bohong sampai terbukti benar"**

| Situasi | Sikap |
|---------|-------|
| README bilang "mendukung fitur X" | Cari kode X. Gak ada? → catat claim vs reality |
| Docs bilang "test coverage 90%" | Run coverage tool atau cek test file count |
| "Simple API" tapi file 500 baris | Catat kontradiksi |
| "Production-ready" tapi gak ada error handling | Catat gap |
| "Lightweight" tapi dependency 40MB | Catat |

## Evidence Depth Tags
Tambahkan tag kedalaman di tiap finding:
| Tag | Artinya |
|-----|---------|
| `[D1]` | Surface — baca docs/README doang. Low confidence. |
| `[D2]` | Medium — baca struktur file + beberapa file kode |
| `[D3]` | Deep — baca implementasi penuh, ikutin import chain |
| `[D4]` | Exhaustive — verifikasi + cross-reference + test check |

Format temuan: `[TAG] [D2] path:42 — deskripsi`

## Audit Checklist (wajib tiap review)

Sebelum kirim hasil audit, pastikan checklist ini terisi:
- [ ] ✅ Pass 1 (Scan) selesai
- [ ] ✅ Pass 2 (Detail) — minimal 1 import chain dilacak
- [ ] ✅ Pass 3 (Cross-Reference) — docs claim vs reality
- [ ] ✅ Self-Check: gak ada "belum baca file" alias "cuma liat README"
- [ ] ✅ Tiap finding ada depth tag [D1-D4]
- [ ] ✅ Tiap BLOCKING ada evidence file:line
