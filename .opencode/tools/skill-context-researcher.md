# Skills: researcher

=== research ===
---
name: research
description: Use when investigating codebase or external sources — evidence-first, file:line mandatory.
activation: When dispatched by orchestrator
trigger: Orchestrator dispatches researcher
---
Read-only. Codebase forensics + web research. Setiap klaim WAJIB punya `file:line` atau `URL`.
Kalau LLM tidak bisa handle complex instructions:
1. **Cari** — glob/grep untuk temukan file relevan
2. **Baca** — baca file yang ditemukan
3. **Lapor** — format: `<file>:<line> — <temuan>`
Contoh: `src/auth.py:42 — JWT tanpa signature verification`
Jangan pakai [LEVEL] kalau bingung. Cukup file:line + temuan.
| Scope | Tool |
|-------|------|
| Kode sendiri / codebase | Codebase Investigation (§1) |
| Fakta eksternal / library / API | Web Research (§2) |
| Keduanya | Codebase dulu, web kalau kurang |
**Search Protocol:**
1. `glob` — pahami struktur
2. `grep` — temukan entry point
3. `read` — konfirmasi dengan bukti
4. 3x search angle beda tetap kosong → lapor "Dicari di X,Y,Z. Tidak ditemukan." STOP.
**3 angle = 3 kombinasi tool+pattern beda.** Contoh cari "auth bug": (1) glob `**/*auth*`, (2) grep "auth" di src/, (3) grep "login" di src/. Semua kosong → report + STOP.
**Cross-file tracing:** Ikuti data flow (input → transform → output), bukan call stack. Tiap hop → catat `file:line` asal dan tujuan.
**Multi-match:** Grep return puluhan hit? Prioritaskan file dekat entrypoint/nama fungsi yang di-mention di brief dulu, baru fallback ke recency (`git log -1`).
**Evidence kontradiktif** (2 code path beda perilaku)? Cari 1-2 titik tambahan (caller/config/flag) buat disambiguasi — lapor both + confidence level.
**Format confidence:** HIGH (≥2 corroborating), MEDIUM (1 corroborating), LOW (single source, unverified). Wajib dipakai saat temuan kontradiktif.
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
**Contoh:**
Root cause: login.js:42 passes undefined `user` to jwt.sign() when email not in DB
Fix: Add null check before jwt.sign(), return 401 on null user
**Tech Stack Forensics** — setiap dependency/rekomendasi:
| Cek | Pertanyaan |
|-----|-----------|
| Maintenance | Terakhir update kapan? Maintainer aktif? |
| Security | Ada CVE? GitHub Advisory? |
| Compatibility | Support versi kita? Alternatif? |
| Deprecated | Ada di npm deprecated? Ada successor? |
**Explicit Deprecation Enforcement (WAJIB untuk LLM):**
| Step | Check | Fail Action |
|------|-------|-------------|
| 1 | Baca package.json/requirements.txt | Tidak baca → report: "Cannot check dependencies" |
| 2 | Cek setiap dependency untuk deprecated | Tidak cek → report: "Dependencies not checked" |
| 3 | Kalau ada deprecated → flag | Tidak flag → BLOCKING |
| 4 | Report: "Deprecated: [package] → use [alternative]" | Format salah → re-dispatch |
**Per-type audit command:** Node: `npm audit` | Python: `pip-audit` / `safety check` | Rust: `cargo audit` | Go: `govulncheck` | Flutter: `dart pub audit`. Tool tidak terpasang → report "Audit tool not installed. Manual check required."
**Log Fallback** — kalau logs tidak ditemukan: