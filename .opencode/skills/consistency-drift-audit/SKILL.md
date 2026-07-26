---
name: consistency-drift-audit
description: Use when reviewing multi-file changes, config sets, or docs — detect contradiction, drift, and stale duplication across files. Complements `stride-audit` (security) with a cross-referential lens.
---

# Consistency & Drift Audit

STRIDE nanya "apakah ini aman". Skill ini nanya "apakah semua file yang saling ngaku sinkron, beneran sinkron". Bug paling nyebelin sering bukan di satu file — tapi di celah antar file yang lupa di-update bareng.

## Kapan Dipakai

- Ada >1 file yang **secara desain harus saling merefleksikan** (config vs profile turunannya, docs vs implementasi, schema vs API contract)
- Perubahan yang nyentuh salah satu dari sepasang/sekumpulan file yang "seharusnya identik/sinkron"
- Audit rutin — bukan cuma pas ada perubahan, tapi juga cek drift yang udah lama ngendep

## 1. Peta Ketergantungan Dulu

Sebelum audit, identifikasi **pasangan/grup file yang claim saling konsisten**:

- Config utama vs turunannya (contoh: root config = salah satu profile — kalau iya, itu harus identik atau ada alasan jelas kenapa beda)
- Dokumentasi vs kode (README bilang "3 profile" — beneran ada 3 file profile? angka steps yang disebut di docs match sama yang di config?)
- Schema vs kontrak (nama field di database schema = nama field di API response?)
- Skill/persona frontmatter vs isi (persona nyebut skill X — file skill X beneran ada di path yang disebut?)

## 2. Drift Detector

| Jenis Drift | Cara Cek |
|---|---|
| **Numeric drift** | Angka yang disebut di 2+ tempat (steps, versi, limit) — diff manual, jangan percaya "kayaknya sama" |
| **Structural drift** | Field/section ada di satu file tapi hilang di file pasangannya |
| **Stale reference** | File A nunjuk ke file B yang udah dipindah/dihapus/di-rename |
| **Silent duplication** | 2 file isinya harusnya sama tapi ternyata udah diverge (edit di satu, lupa di yang lain) |
| **Claim vs reality** | Dokumen bilang "X ada" tapi pas dicek filesystem/kode, X nggak ada atau beda |

## 3. Prosedur

1. `glob`/`list` — kumpulin semua file yang termasuk grup "harus konsisten"
2. `diff` mental (atau literal, kalau formatnya sama) antar file sejenis
3. Untuk klaim di docs (angka, daftar, path) — cross-check ke sumber aslinya (config/kode), jangan trust dokumentasi begitu aja
4. Catat tiap drift yang ketemu, walau "kelihatannya minor" — drift kecil hari ini = bug besar 3 bulan lagi

## 4. Priority Tags (reuse dari stride-audit)

- **[BLOCKING]** — drift yang bikin sistem behave beda dari yang didokumentasikan/diharapkan (misal: config production nunjuk ke value yang salah)
- **[SHOULD]** — drift yang belum berdampak tapi bakal confuse orang berikutnya
- **[NICE]** — inkonsistensi kosmetik (formatting, urutan)
- **[FYI]** — drift yang disengaja & valid (beda profile memang harus beda) — dicatat biar jelas itu bukan bug

**Format:** `[TAG] fileA:baris ↔ fileB:baris — apa yang harusnya sama tapi beda`

## 5. Cumulative Judgment

Sama kayak STRIDE — jangan cuma cek 1 pasang file lalu berhenti. Drift sering nyebar berantai: docs salah → developer berikutnya ikutin docs yang salah → kode baru ikut salah. Trace dari mana kebenaran itu seharusnya berasal (single source of truth) baru cek yang lain nurut apa nggak.

## Output

Summary: `"X BLOCKING drift, Y SHOULD, Z NICE"` — lalu list per finding, 1 baris tiap temuan, format di atas.

**Jangan:** re-tulis ulang seluruh isi kedua file buat nunjukin bedanya — cukup titik perbedaan + lokasi.
