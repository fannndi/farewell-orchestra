---
name: web-research
description: Use when investigating outside the codebase — current facts, library/API status, docs, pricing, news. Evidence-first, source-quality aware. Uses 9Router /v1/search and /v1/web/fetch for execution.
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

Kalau ragu → **search**. Salah nyari (boros 1 call) lebih murah daripada salah jawab.

## 3. Query Protocol

1. **Pendek & spesifik.** 2-6 kata. Bukan kalimat lengkap.
2. **Broad → narrow.** Query pertama umum, berikutnya makin spesifik.
3. **Setiap query harus beda arah** — jangan re-run query sama dengan kata ganti.
4. **Item majemuk → pisah.** "Bandingin X dan Y" → 1 query X, 1 query Y.
5. **Snippet nggak cukup?** → `web_fetch` halaman aslinya.

## 4. Scale Effort

| Task | Jumlah search |
|------|:---:|
| 1 fakta sederhana | 1 |
| Perbandingan/multi-part | 3-8 |
| Riset mendalam | 8-20 |

Berhenti kalau semua bagian request ke-cover buktinya.

## 5. Source Quality

- **Prioritaskan sumber primer:** docs resmi, blog perusahaan, paper, rilis resmi > aggregator/blog SEO
- **Skip forum/low-quality** kecuali opini komunitas memang yang dicari
- **Konflik antar sumber?** → cari 1-2 sumber tambahan buat tie-break
- **Topik rawan misinformasi** → lebih skeptis, verifikasi ekstra

## 6. Evidence Standard

- **Format:** `klaim — (Sumber, tanggal)`
- **Confidence <90%** → tandai: `(perlu verifikasi)`
- **Jangan quote panjang.** Parafrase. Kutip <15 kata, max 1 per sumber.
- **Nggak ketemu?** → `"Dicari X,Y,Z — nggak ketemu."` 1 baris.

## 7. 9Router API

### Web Search

`POST http://127.0.0.1:20128/v1/search`

| Field | Required | Notes |
|-------|:---:|-------|
| `model` (or `provider`) | ✅ | dari `/v1/models/web` (tavily, brave, exa, search-combo) |
| `query` | ✅ | search query |
| `max_results` | — | default 5 |
| `search_type` | — | `web` / `news` |

Provider: tavily, exa, brave-search, serper, perplexity, linkup, google-pse, searchapi, youcom, searxng.

Pakai `search-combo` buat auto-fallback antar provider.

Response: `{ results: [{ title, url, snippet, score }], usage: { search_cost_usd } }`

### Web Fetch (baca halaman penuh)

`POST http://127.0.0.1:20128/v1/web/fetch`

| Field | Required | Notes |
|-------|:---:|-------|
| `url` | ✅ | URL halaman |
| `format` | — | `markdown` (default) / `text` / `html` |
| `max_characters` | — | truncate (0 = full) |
| `model` | ✅ | firecrawl, jina-reader, tavily, exa, fetch-combo |

Pakai `fetch-combo` buat auto-fallback.

Response: `{ data: { title, content: { text, length } } }`

### Kapan Fetch vs Search?
- **Search** = nemuin sumber (URL, snippet, metadata)
- **Fetch** = baca isi penuh halaman (pas snippet nggak cukup, atau butuh detail teknis)

## 8. Attitude

- Jangan asumsi hasil pertama final — verifikasi kalau ada nama/versi mirip.
- Jangan campur pengetahuan lama (basi) dengan hasil search tanpa label.
- Baca halaman penuh kalau snippet ambigu — jangan tebak dari judul.

## Output

`Finding: [klaim]. Sumber: [nama/link]. Confidence: [tinggi/verifikasi].`

Beberapa temuan → 1 finding = 1 baris, sama kayak format `forensic`.
