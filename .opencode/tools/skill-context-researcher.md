# Skills: researcher

=== research ===
---
name: research
description: Use when investigating codebase or external sources — evidence-first, file:line mandatory.
---
Read-only. Codebase forensics + web research. Setiap klaim WAJIB punya `file:line` atau `URL`.
Kalau LLM tidak bisa handle complex instructions:
1. **Cari** — glob/grep untuk temukan file relevan
2. **Baca** — baca file yang ditemukan
3. **Lapor** — format: `<file>:<line> — <temuan>`
Contoh: `src/auth.py:42 — JWT tanpa signature verification`
Jangan pakai [LEVEL] kalau bingung. Cukup file:line + temuan.

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

=== simplification ===
---
name: simplification
description: Guide untuk menyederhanakan kode yang sudah ada.
---
Cara menyederhanakan kode yang sudah ada.
> "Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away." — Antoine de Saint-Exupéry
Tanya:
- Ada file yang tidak perlu?
- Ada abstraction yang tidak perlu?
- Ada pattern yang tidak perlu?
- Ada dependency yang tidak perlu?