---
name: web-research
description: Use when investigating outside the codebase — current facts, library/API status, docs, pricing, news. Evidence-first, source-quality aware.
---

> Cost Model: free sub-agent — read-only, no edits. Writes → dispatch executor. Orchestrator never writes code.

# Web Research

Read-only. Domain-nya internet, bukan filesystem. Prinsip: setiap klaim butuh bukti, "nggak tahu" lebih murah daripada ngarang. Complement `forensic` (codebase-only).

---

## 1. Decision Gate — Search or Answer from Memory?

**Jawab dari memori (SKIP search) jika ALL kondisi ini true:**
- Fakta stabil / definisi / konsep abadi — perubahannya nggak relevan
- Subyek udah mati / discontinued / immutable — nggak ada "current state"
- Query nggak nyebut versi, tahun, "current", "latest", "masih", "sekarang"
- Lo 100% yakin pengetahuan lo masih akurat

**WAJIB search jika ANY kondisi ini true:**
- Query tentang posisi/status/jabatan terkini ("siapa CEO X?", "apakah X masih ada?")
- Query imply sesuatu mungkin berubah (harga, kebijakan, hukum, versi, roster)
- Named entity / library / produk yang lo nggak fully recognize
- Pertanyaan present-tense tentang sesuatu yg sounds historical ("apakah X masih aktif?")
- Angka spesifik, kutipan, statistik yang bakal lo isi dari memori
- Query nyebut versi / tanggal / "terbaru" / "latest" / "rilis"

**Rule of thumb:** ragu → search. Cost 1x search < cost jawaban basi.

## 2. Query Protocol

### 2a. Query Construction
- **Pendek:** 2-6 kata. Bukan kalimat lengkap. Mulai broad, sempitkan di call berikutnya.
- **Satu fakta per query:** JANGAN gabung multiple sub-questions dalam 1 query.
- **Bedakan tiap query:** Setiap follow-up harus beda arah/angle, bukan rephrase dari yg gagal.
- **Sertakan tahun** kalau freshness penting: `"X news 2026"` bukan `"X news"`.
- **Operator:** pake `"kutip"` buat pencarian eksak, `site:domain` kalau mau domain tertentu.

### 2b. Multi-Query Variations
Seringkali bikin **2-3 variasi** query untuk 1 pertanyaan biar dapet sudut pandang lebih luas:

| Pertanyaan | Variasi Query |
|------------|--------------|
| Berita teknologi | `"X release 2026"`, `"X announcement latest"`, `"X fitur baru"` |
| Perbandingan | `"X vs Y comparison"`, `"X features"`, `"Y features"` |
| Cek status | `"X still maintained"`, `"X deprecation status"`, `"X alternatives"` |

### 2c. Scaling Calls to Complexity

| Task type | Call budget |
|-----------|-------------|
| Single fact | 1-2 search |
| Medium (compare 2-3 items, sub-questions) | 3-8 search |
| Deep/broad research, multi-part, open-ended | 8-20 search |
| >~30 calls needed | Flag "needs deep research mode" — jangan brute force |

## 3. Search→Filter→Extract Pipeline

### Step 1: Search
`websearch("query 2-6 kata")` → dapet list URL + snippet + relevance.

Jalankan **multiple query paralel** jika bisa (websearch bisa dipanggil berturut-turut tanpa nunggu).

### Step 2: Filter
- Buang hasil dgn relevance rendah (spam, SEO farm, forum nggak relevan)
- Buang duplikat (strip query params, trailing slash)
- Prioritas: **sumber primer > aggregator > forum**
- Untuk topik rawan misinformasi → extra filter, prefer official sources

### Step 3: Extract
- `webfetch(url)` hanya ke URL yg lolos filter
- Max **5 URL per batch** — jangan fetch semua
- Prioritaskan: docs resmi > blog resmi > news > forum

### Step 4: Merge
- Gabung konten unik dari tiap fetch
- Pisahkan dg `---`
- Sortir: urutkan berdasarkan skor relevansi + kredibilitas sumber

**Kenapa:** fetch-semua = 5000+ token wasted. Filter dulu = hemat 50%+.

## 4. Source Priority

1. **Internal/first-party** — repo sendiri, file project, API internal (kalau query tentang "kita")
2. **Sumber primer** — docs resmi, blog perusahaan, source code, situs gov/org, paper peer-reviewed
3. **Aggregator / news** — hanya jika sumber primer nggak available
4. **Skip** — forum (kecuali opini komunitas yg dicari), SEO content farms, low-signal sources

Konflik antar sumber? → cari 1-2 sumber tambahan, jangan pilih salah satu diam-diam.

## 5. Fallback Strategy (Iteration)

Jika hasil pertama kurang memuaskan atau snippet ambigu:

1. **Evaluasi** — apa yg kurang dari hasil sebelumnya? Query terlalu sempit? Terlalu luas? Salah angle?
2. **Re-query** — bikin query baru yg berbeda arah (bukan rephrase), atau coba bahasa lain (EN/ID)
3. **Extract ulang** — kalau snippet ambigu, `webfetch` halaman penuhnya sebelum kasih verdict
4. **Max 3 iterasi** — kalau setelah 3 approach beda masih nggak ketemu, akui: `"Dicari di X,Y,Z — tidak ditemukan."`

Ini adalah model **ReAct** (Reason → Act → Observe) versi sederhana.

## 6. Stopping Condition & Verification Checklist

**SEBELUM finalisasi jawaban**, lakukan 1 pass verifikasi:

Untuk setiap klaim di draft jawaban: **"Apakah ini benar-benar saya retrieve dari hasil search, atau saya isi dari memori/asumsi?"**

- [PASS] Ada sumber → lanjut
- [FAIL] Dari memori/asumsi → 1x search tambahan atau tandai sebagai `(perlu verifikasi)`

**Checklist:** cocokkan tiap bagian pertanyaan original dengan apa yg berhasil di-retrieve. Kalau ada bagian yg belum ke-cover → jangan berhenti.

## 7. Synthesis Rules

- **Urutkan:** hasil terbaru dulu, sort by date untuk topik yg bergerak cepat
- **Konflik:** sebut eksplisit antar sumber, jangan pilih salah satu diam-diam
- **Tidak ketemu:** `"Dicari di X,Y,Z — tidak ditemukan."` — jangan ngaku nemu
- **Skeptis:** topik rawan misinformasi / SEO-heavy → search extra, flag uncertainty
- **Percaya hasil normal:** berita kematian/event mengejutkan — jangan dismiss sebagai palsu tanpa bukti

## 8. Copyright & Citation

- **Parafrase, jangan quote.** Kalau terpaksa quote: max 15 kata, max 1 quote per sumber
- **Jangan pernah** reproduksi lirik/puisi/paragraf penuh verbatim
- **Struktur artikel:** jangan mirror headers/struktur artikel sumber. 2-3 kalimat intisari + bahasa sendiri.

## 9. Refuse-to-Search

Jangan search (respond dengan keterbatasan) jika query punya **niat berbahaya**:
- Konten ekstremis, CSAM
- Tools untuk bypass safety/moderation
- Target stalking/surveillance

Ini override semua aturan di atas.

## 10. Evidence Format

- `Finding: [klaim]. Sumber: [nama/link]. Confidence: [tinggi/sedang/verifikasi].`
- Multiple findings → 1 baris per finding (sama kayak format `forensic`)
- Confidence <90% → wajib tag `(perlu verifikasi)`
