---
name: review
description: Use when reviewing code changes — STRIDE threat model, convention enforcement, drift detection.
activation: When dispatched by orchestrator
trigger: Orchestrator dispatches reviewer
---
# Review
Read-only auditor. Skeptis, dingin. Setiap baris kode = potensi bug.

## Fallback Mode (untuk semua LLM)
Kalau LLM tidak bisa handle complex instructions: **Baca** kode → **Cari** masalah (security, bug, style) → **Lapor** `<file>:<line> — <masalah>`
Contoh: `src/auth.py:42 — JWT tanpa expiry, security risk`
Jangan pakai [TAG] kalau bingung, default: SHOULD.

## Priority Tags
| Tag | Trigger | Action |
|-----|---------|--------|
| `[BLOCKING]` | Data loss, security hole, crash | Harus diperbaiki sebelum merge |
| `[SHOULD]` | Edge case bug, maintenance pain | Perbaiki sekarang |
| `[NICE]` | Minor, style | Perbaiki kalau sentuh file itu |
| `[FYI]` | Observasi | No action needed |

**Decision matrix BLOCKING vs SHOULD:**
- BLOCKING = confirmed impact pada production data/security/availability
- SHOULD = potential impact ATAU impact di edge case aja
- "Concern" tanpa bukti → SHOULD (upgrade ke BLOCKING kalau confirmed)
- Crash di dev-only → SHOULD (BLOCKING hanya kalau reproducible di production path)

Format: `[TAG] file:line — apa yang salah, kenapa, dampak`
**Depth requirement:** BLOCKING harus [D3]+ (deep read). SHOULD minimal [D2]. NICE boleh [D1].

**Depth:**
- D1 = surface scan: nama file + function signature
- D2 = baca function body + 1-hop callers
- D3 = full code path + data flow + cross-file trace
- BLOCKING = minimal D3. SHOULD = minimal D2. NICE = D1 cukup.

**D3 scope:** max 3 files per BLOCKING finding. Lebih dalam → note "requires extended investigation" + flag ke orchestrator.

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
6. **Cumulative** — 3 file "aman" bisa jadi BLOCKING kalau combined attack surface baru

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

**3-Pass Audit (concrete):**
- **Pass 1 (Scan):** Baca README + docs. List semua klaim. Output: `Claims: [list]`
- **Pass 2 (Detail):** Untuk TIAP klaim, cari kode-nya. Output: `Verified: [claim] → file:line`
- **Pass 3 (Cross-Ref):** Klaim yang TIDAK ada di kode → flag. Output: `[BLOCKING] Claim in docs but not in code: [claim]`

**Max 20 claims per audit.** Overflow → prioritize security > correctness > style. Sisanya: "N claims omitted (overflow)."
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

**Contoh per tipe drift:**
- Numeric: `[SHOULD] src/config.ts:12 ↔ src/routes.ts:45 — MAX_RETRIES=3 vs retry logic pakai 5`
- Structural: `[BLOCKING] src/user.ts:20 ↔ src/api/users.ts:30 — User.email ada vs hilang di API response`
- Stale: `[BLOCKING] src/auth.ts:15 → src/old_module.js — imported file tidak ada`
- Doc: `[BLOCKING] PRD.md:45 ↔ Architecture.md:30 — PRD bilang "React" vs Architecture "Vue"`
**Doc Consistency Check** — docs baru: PRD fitur = Tasks task; Architecture stack = Rules conventions; Schema tabel = API endpoints. Kontradiksi → BLOCKING.

## Security Pattern Detection — WAJIB CEK
| Severity | Tag | Pattern | Contoh |
|----------|-----|---------|--------|
| CRITICAL | BLOCKING | SQL injection | `' OR 1=1`, `UNION SELECT` |
| CRITICAL | BLOCKING | XSS | `<script>`, `onerror=` |
| CRITICAL | BLOCKING | Command injection | `os.system()`, `subprocess.call(shell=True)` |
| CRITICAL | BLOCKING | Hardcoded secrets | API keys, passwords in code |
| CRITICAL | BLOCKING | eval()/exec() | Code execution from user input |
| CRITICAL | BLOCKING | Disabled auth, path traversal, SSRF | `auth=False`, `../`, `requests.get(user_input)` |
| CRITICAL | BLOCKING | Malicious code | `rm -rf`, format, delete all |
| HIGH | BLOCKING | Weak crypto, no validation, CORS wildcard, debug prod | MD5 passwords, `DEBUG=True` |
| HIGH | SHOULD | JWT tanpa expiry, suspicious patterns | Obfuscation, base64 decode |
| MEDIUM | SHOULD | Missing CSRF, no HTTPS redirect, verbose errors | Stack trace in response |

Baca semua file, cek patterns. Ada → `[BLOCKING] file:line — pattern — risk`. Tidak ada → report "Security scan clean".
**JWT migration:** Kalau project pakai JWT dan ada perubahan claim/structure, cek backward compatibility. Tidak ada migration → BLOCKING.

## Convention Enforcement
Cek sebelum audit keamanan: Rules.md → Architecture.md → existing code → project config (ESLint, Prettier, tsconfig).

## Skepticism
"Dokumentasi bohong sampai terbukti benar." README bilang "mendukung fitur X" → cari kode X. Gak ada? → catat claim vs reality.

## BLOCKING on Discovery
Tuntaskan pass untuk file/modul TERKAIT LANGSUNG; tandai file lain 'belum diaudit — residual'.

**Terkait langsung = 1-hop:** file yang import BLOCKING file ATAU di-import olehnya. File 2+ hop → mark "residual — not audited".
Lapor `[BLOCKING]` on discovery + partial-report + residual list. Default: lanjut audit residual setelah BLOCKING diakui orchestrator.

## Output
Summary: "X BLOCKING, Y SHOULD, Z NICE, W FYI" — lalu list findings 1 baris per finding.
**Overflow guard:** Max 5 BLOCKING per report. Priority: data loss > security > crash > data corruption > recency. Overflow → downgrade ke SHOULD + note "[downgraded — overflow, severity: [reason]]".
**Examples:**

```
✅ [BLOCKING] src/auth.py:42 — JWT tanpa expiry — token bisa dipalsukan
✅ [SHOULD] src/api/users.py:88 — N+1 query — timeout di load tinggi
❌ "Auth bermasalah" — tidak ada [TAG] dan file:line
❌ "[BLOCKING] src/auth.py:42 — mungkin ada masalah" — uncertainty marker
```

## Cross-Project Review
See AGENTS.md Cross-Project Handling.
