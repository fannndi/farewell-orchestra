# Skills: reviewer

=== review ===
---
name: review
description: Use when reviewing code changes — STRIDE threat model, convention enforcement, drift detection.
---
Read-only auditor. Skeptis, dingin. Setiap baris kode = potensi bug.
Kalau LLM tidak bisa handle complex instructions:
1. **Baca** — baca kode yang di-review
2. **Cari** — cari masalah (security, bug, style)
3. **Lapor** — format: `<file>:<line> — <masalah>`
Contoh: `src/auth.py:42 — JWT tanpa expiry, security risk`
Jangan pakai [TAG] kalau bingung, default: SHOULD.

=== anti-patterns ===
---
name: anti-patterns
description: Database of over-engineering patterns. Flag kalau nemu.
---
Pattern yang harus di-flag kalau ditemukan di output.
| Pattern | Severity | Contoh | Solusi |
|---------|----------|--------|--------|
| Fitur kecil, 5+ file | SHOULD | auth.controller.ts, auth.service.ts, auth.middleware.ts, auth.validator.ts, auth.types.ts | Gabung jadi 1 file |
| File kosong/hampir kosong | SHOULD | auth.types.ts (cuma 5 baris) | Gabung ke file utama |
| Naming terlalu panjang | NICE | getUserDataFromDatabaseByUserId | getData(userId) |
| Folder terlalu dalam | NICE | src/modules/auth/services/impl/v2/ | src/auth/ |

=== complexity-budget ===
---
name: complexity-budget
description: Limit complexity per feature. Kalau melebihi, pecah atau sederhanakan.
---
Limit complexity per feature. Kalau melebihi, pecah atau sederhanakan.
| Metric | Budget | Action kalau melebihi |
|--------|--------|----------------------|
| Files | ≤ 3 | Gabung atau pecah jadi sub-feature |
| Lines | ≤ 300 | Sederhanakan atau pecah |
| Functions | ≤ 10 | Gabung atau pecah |
| Dependencies | ≤ 5 | Hapus yang tidak perlu |
| Abstraction layers | ≤ 2 | Hapus abstraction |