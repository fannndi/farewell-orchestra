---
name: web-research
description: Use when investigating outside the codebase — current facts, library/API status, docs, pricing, news. Evidence-first, source-quality aware.
---

# Web Research

Read-only. Domain-nya internet, bukan filesystem. Prinsip: setiap klaim butuh bukti, "nggak tahu" lebih murah daripada ngarang. Complement `forensic` (codebase-only).

## 1. Kapan Wajib Search (jangan jawab dari memori)

- **Current state apapun:** versi terbaru, harga, status "masih aktif?", rilis software
- **Fast-changing:** CVE, breaking changes, berita, deprecation
- **Spesifik & verifiable:** angka, tanggal, statistik, nama library/versi
- **Kata kunci sinyal:** "current", "latest", "masih", "sekarang" → status hari ini

## 2. Kapan TIDAK Perlu Search

- Fakta stabil (definisi, konsep, sejarah settled)
- Jawaban yang nggak berubah seiring waktu

Kalau ragu → **search**. Salah nyari lebih murah daripada salah jawab.

## 3. Tools

### OpenCode Built-in (pakai ini dari dalam agent)

| Tool | Fungsi | Cara pakai |
|------|--------|------------|
| `websearch` | Search Google/Brave/etc | `websearch("query spesifik 2-6 kata")` — hasil: list URL + snippet |
| `webfetch` | Baca isi halaman penuh | `webfetch("https://url", "markdown")` — hasil: konten full page |

**JANGAN pakai HTTP fetch/call manual.** OpenCode sudah handle routing search engine via 9Router di belakang layar. Lo tinggal panggil `websearch` dan `webfetch`.

### Search→Extract Two-Step

JANGAN fetch langsung. Selalu dua langkah:

1. **Search** — `websearch("query")` → dapet list URL + snippet + relevance score
2. **Filter** — buang URL dg score <0.7, buang duplikat (strip query params, trailing slash)
3. **Extract** — `webfetch(url)` hanya ke URL yg lolos filter, max 5 URL per batch
4. **Merge** — gabung konten unik, pisahkan dg `---`, sort by score descending

**Kenapa:** fetch-semua = 5000+ token wasted. Search→filter→extract = hemat 50%.

### 9Router API (untuk script eksternal / custom tool — BUKAN dari dalam agent)

Kalau BUTUH akses programmatic dari luar OpenCode (script, CI, custom tool):

`POST http://127.0.0.1:20128/v1/search` — providers: tavily, exa, brave, serper, google-pse, search-combo
`POST http://127.0.0.1:20128/v1/web/fetch` — providers: firecrawl, jina-reader, tavily, exa, fetch-combo

Pakai `search-combo` / `fetch-combo` buat auto-fallback. Lihat 9Router docs buat detail.

## 4. Query Protocol

### 4a. Sub-Query Batching

Query kompleks → pecah jadi 3-5 sub-query paralel:

| Query asli | Sub-queries |
|------------|-------------|
| "Bandingin X vs Y untuk Z" | `websearch("X features Z")`, `websearch("Y features Z")`, `websearch("X vs Y comparison")` |
| "Apa implikasi X terhadap Y dan Z" | `websearch("X impact on Y")`, `websearch("X impact on Z")`, `websearch("X latest developments")` |

**Jangan gabung** dalam satu query panjang — hasil cenderung dangkal untuk semua topik.

### 4b. Query Rules

1. **Pendek & spesifik.** 2-6 kata. Bukan kalimat lengkap.
2. **Broad → narrow.** Query pertama umum, berikutnya makin spesifik.
3. **Jangan re-run query sama.** Setiap query harus beda arah.
4. **Snippet ambigu?** → `webfetch(url)` halaman aslinya.
5. **Scale effort:** 1 fakta = 1 search. Perbandingan = 3-8. Riset = 8-20.

## 5. Source Quality

- **Prioritaskan sumber primer:** docs resmi, blog perusahaan, paper, rilis resmi > aggregator/blog SEO
- **Skip forum/low-quality** kecuali opini komunitas yang dicari
- **Konflik antar sumber?** → cari 1-2 sumber tambahan buat tie-break
- **Topik rawan misinformasi** → lebih skeptis, verifikasi ekstra

## 6. Evidence Standard

- **Format:** `klaim — (Sumber, tanggal)`
- **Confidence <90%** → tandai: `(perlu verifikasi)`
- **Jangan quote panjang.** Parafrase. Kutip <15 kata, max 1 per sumber.
- **Nggak ketemu?** → `"Dicari X,Y,Z — nggak ketemu."` 1 baris.

## 7. Attitude

- Jangan asumsi hasil pertama final — verifikasi kalau ada nama/versi mirip.
- Jangan campur pengetahuan lama (basi) dengan hasil search tanpa label.
- Baca halaman penuh (`webfetch`) kalau snippet ambigu — jangan tebak.
- Kalau `webfetch` gagal (timeout, blocked), coba `websearch` alternatif atau cari mirror.

## Output

`Finding: [klaim]. Sumber: [nama/link]. Confidence: [tinggi/verifikasi].`

Beberapa temuan → 1 finding = 1 baris, sama kayak format `forensic`.
