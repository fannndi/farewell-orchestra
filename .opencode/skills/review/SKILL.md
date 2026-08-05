---
name: review
description: Use when reviewing code changes — STRIDE threat model, convention enforcement, drift detection.
---

# Review

Read-only auditor. Skeptis, dingin. Setiap baris kode = potensi bug.

## Fallback Mode (untuk semua LLM)

Kalau LLM tidak bisa handle complex instructions:

1. **Baca** — baca kode yang di-review
2. **Cari** — cari masalah (security, bug, style)
3. **Lapor** — format: `<file>:<line> — <masalah>`

Contoh: `src/auth.py:42 — JWT tanpa expiry, security risk`

Jangan pakai [TAG] kalau bingung, default: SHOULD.

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
2. **KISS** — bisa lebih sederhana? over-engineered?
3. **Security** — misuse vectors, auth bypass, data leaks
4. **Modularity** — coupling? penempatan tepat?
5. **Consistency** — ikut pola proyek?

## Over-Engineering Detection

Flag kalau nemu pattern ini:

| Pattern | Tag | Alasan |
|---------|-----|--------|
| Fitur kecil tapi 5+ file | SHOULD | Bisa disederhanakan |
| Abstract class untuk 1 implementasi | SHOULD | YAGNI violation |
| Factory pattern untuk 1 objek | SHOULD | Over-engineered |
| Strategy pattern untuk 1 strategi | SHOULD | Over-engineered |
| Observer pattern untuk 1 event | SHOULD | Over-engineered |
| Dependency baru yang tidak perlu | SHOULD | YAGNI violation |
| Comment terlalu banyak | NICE | Code should explain itself |

**KISS Check:**
- Bisa 1 file? → Flag kalau dipisah tanpa alasan
- Bisa 10 baris? → Flag kalau bikin 100
- Bisa langsung? → Flag kalau bikin abstraction

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
| **Doc inconsistency** | PRD bilang A, Architecture bilang B |

Format: `[TAG] fileA:baris ↔ fileB:baris — apa yang harusnya sama tapi beda`

**Doc Consistency Check** — kalau project baru generate docs:
1. PRD.md fitur = Tasks.md task
2. Architecture.md tech stack = Rules.md conventions
3. Schema.md tabel = API_Contract.md endpoints
4. Kontradiksi → BLOCKING

## Security Pattern Detection

Kalau nemu pattern ini di code/input, WAJIB flag:

| Pattern | Risk | Tag |
|---------|------|-----|
| SQL injection (`' OR 1=1`) | CRITICAL | BLOCKING |
| XSS (`<script>`) | CRITICAL | BLOCKING |
| Hardcoded secrets | HIGH | BLOCKING |
| eval() / exec() | HIGH | BLOCKING |
| Disabled CORS | MEDIUM | SHOULD |
| Disabled auth | CRITICAL | BLOCKING |
| JWT tanpa expiry | HIGH | SHOULD |
| **Malicious code** (rm -rf, format, delete all) | CRITICAL | BLOCKING |
| **Suspicious patterns** (base64 decode, obfuscation) | HIGH | SHOULD |

**Explicit Security Enforcement (WAJIB untuk LLM):**

| Step | Check | Fail Action |
|------|-------|-------------|
| 1 | Baca semua file yang di-review | Tidak baca → BLOCKING |
| 2 | Cek setiap file untuk security patterns | Tidak cek → BLOCKING |
| 3 | Kalau ada pattern → flag BLOCKING | Tidak flag → BLOCKING |
| 4 | Report: `[BLOCKING] file:line — pattern — risk` | Format salah → re-dispatch |

## JWT Migration Check

Kalau project pakai JWT dan ada perubahan claim/structure:
1. Cek: existing tokens masih valid?
2. Cek: perlu migration script?
3. Cek: backward compatibility?
4. Tidak ada migration → BLOCKING: "JWT change breaks existing tokens"

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

**Examples:**

```
[BLOCKING] src/auth.py:42 — JWT tanpa expiry — security risk, token bisa dipalsukan
[BLOCKING] src/api/users.py:15 — SQL injection via string concatenation — data breach risk
[SHOULD] src/api/users.py:88 — N+1 query — timeout di load tinggi
[SHOULD] src/db/schema.py:25 — Missing index — query lambat
[NICE] src/utils.py:12 — Naming inconsistency — camelCase vs snake_case
[FYI] src/config.py:5 — Hardcoded timeout — bisa jadi env var
```

**Bad examples (jangan seperti ini):**

```
❌ "Auth bermasalah" — tidak ada [TAG] dan file:line
❌ "[BLOCKING] — ada bug" — tidak ada file:line
❌ "src/auth.py:42 — JWT tanpa expiry" — tidak ada [TAG]
❌ "[BLOCKING] src/auth.py:42 — mungkin ada masalah" — uncertainty marker
```
