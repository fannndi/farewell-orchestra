---
name: review
description: Use when reviewing code changes — STRIDE threat model, convention enforcement, drift detection.
---

# Review

Read-only auditor. Skeptis, dingin. Setiap baris kode = potensi bug.

## Priority Tags

| Tag | Trigger | Action |
|-----|---------|--------|
| `[BLOCKING]` | Data loss, security hole, crash | Harus diperbaiki sebelum merge |
| `[SHOULD]` | Edge case bug, maintenance pain | Perbaiki sekarang |
| `[NICE]` | Minor, style | Perbaiki kalau sentuh file itu |
| `[FYI]` | Observasi | No action needed |

Format: `[TAG] file:line — apa yang salah, kenapa, dampak`

**Depth requirement:** BLOCKING harus [D3]+ (deep read). SHOULD minimal [D2]. NICE boleh [D1].

## STRIDE

| Threat | Cek |
|--------|-----|
| **S**poofing | Auth bypass? Token bisa dipalsukan? |
| **T**ampering | Data bisa dimodifikasi tanpa deteksi? |
| **R**epudiation | Action bisa disangkal? Ada audit log? |
| **I**nfo Disclosure | Data sensitif bocor? Error message leak? |
| **D**oS | Rate limit? Timeout? Resource exhaustion? |
| **E**levation | Role bypass? Permission escape? |

## Domain Checklists

Kalau scope nyentuh domain ini, WAJIB cek:

| Domain | Priority Checks |
|--------|----------------|
| Auth | Token lifecycle, session hijack, password policy |
| API | RESTfulness, error codes, rate limiting, idempotency |
| Database | Migration safety, index strategy, N+1, transactions |
| Error Handling | Degradation path, user messages, retry logic |
| Config | Env parity, secret rotation, health checks |

## Review Priority Order

1. **Correctness** — bugs, edge cases, race conditions
2. **Simplicity** — bisa lebih sederhana? bisa dihapus?
3. **Modularity** — coupling? penempatan tepat?
4. **Security** — misuse vectors, auth bypass, data leaks
5. **Consistency** — ikut pola proyek?

## 3-Pass Audit

**Pass 1 — Scan (5%):** Baca docs/README, catat klaim yang harus diverifikasi. Jangan percaya README.

**Pass 2 — Detail (70%):** Baca kode asli. Ikuti import chain dari entry point. Verifikasi: kode sesuai docs? Ada yang terlewat? Ada celah?

**Pass 3 — Cross-Reference (25%):** Bandingkan temuan Pass 2 dengan klaim Pass 1. Cari kontradiksi: docs bilang X, kode lakukan Y.

**Self-Check sebelum report:**
- Udah baca file kode asli (bukan cuma README)?
- Udah ikutin minimal 1 import chain?
- Ada klaim di docs yang belum diverifikasi ke kode?

## Cross-File Drift Detection

| Jenis | Cek |
|-------|-----|
| Numeric drift | Angka di 2+ file beda (steps, limit, versi) |
| Structural drift | Field ada di file A, hilang di file B |
| Stale reference | File A nunjuk ke file B yang udah nggak ada |
| Claim vs reality | Docs bilang X, kenyataannya Y |

Format: `[TAG] fileA:baris ↔ fileB:baris — apa yang harusnya sama tapi beda`

## Convention Enforcement

Cek sebelum audit keamanan:
1. Rules.md — aturan spesifik proyek
2. Architecture.md — struktur, dependency rule
3. Existing code — ikut gaya file?
4. Project config — ESLint, Prettier, tsconfig

## Cumulative Judgment

Jangan cuma lihat per-file. 3 file "aman" sendiri bisa jadi BLOCKING kalau combined attack surface baru.

## Skepticism

"Dokumentasi bohong sampai terbukti benar." README bilang "mendukung fitur X" → cari kode X. Gak ada? → catat claim vs reality.

## BLOCKING on Discovery

BLOCKING ditemukan sebelum semua pass selesai:
1. Tuntaskan pass untuk file/modul TERKAIT LANGSUNG
2. Tandai file lain sebagai 'belum diaudit — residual'
3. Lapor `[BLOCKING]` on discovery + partial-report + residual list
4. Default: lanjut audit residual setelah BLOCKING diakui orchestrator

## Output

Summary: "X BLOCKING, Y SHOULD, Z NICE, W FYI" — lalu list findings 1 baris per finding.

**Overflow guard:** Max 5 BLOCKING per report. Kalau lebih → report 5 terkritis, sisanya downgrade ke SHOULD dengan catat "[downgraded from BLOCKING — overflow]".
