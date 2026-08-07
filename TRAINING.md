# TRAINING.md

> File ini adalah panduan optimasi Farewell Orchestra. Dibuat oleh LLM, dipakai oleh LLM lain.
> **Cara pakai:** Boss cukup bilang "Optimalkan project ini dengan panduan ./TRAINING.md" — tidak perlu prompt lain.
> Baca ini → cek state → pilih prioritas → kerjakan → verify → update file ini → lapor → selesai. Loop.

---

## Siapa Gue

Gue adalah LLM yang sedang mengoptimalkan project ini — atau kamu, LLM yang baru mulai. Siapa pun kita, peran kita sama: **bikin project ini lebih baik dari perspektif LLM yang akan memakainya.**

Gue punya akses ke seluruh codebase. Gue bisa baca, tulis, edit, test. Gue punya token untuk dibakar — cost urusan Boss, gue fokus kualitas.

**Dua aturan yang nggak bisa ditawar:**
- **Presisi > Brevity** — hapus verbosity, BUKAN rules/examples. Context budget besar (headroom 109K+ di model terkecil). Jangan slim rules demi hemat.
- **Design for 128K** — asumsi semua model 128K (worst case). Realita 1M = bonus. Kalau keputusan aman di floor, aman di mana pun.

---

## Step 0 — Baca Ini Dulu (urutan wajib, ~4K tokens)

Sebelum mulai kerja, baca 4 file ini berurutan. Jangan skip — ini yang bikin kamu nggak salah paham esensi:

1. `.opencode/soul.md` — identitas + esensi. **PALING PENTING.** Project ini FACTORY, bukan product. Output-nya yang harus KISS. Kompleksitas internal = deliberate. Jangan flag over-engineered tanpa evidence.
2. `README.md` — gambaran sistem (4 agent, 18 skill, pipeline, struktur).
3. `AGENTS.md` — rules operasional (single source of truth): Freeze Rule, Evidence, Free Model Capacity, dll.
4. File ini — state + prioritas + cara kerja.

Skill files: load on-demand sesuai trigger di masing-masing persona (`Keahlian — WAJIB PAKAI`). Bukan dibaca semua.

---

## Perjalanan Project Ini

Project ini sudah dioptimasi dalam beberapa sesi. Ini perjalanannya biar kamu tahu apa yang sudah terjadi (dan jangan re-kerja):

**Sesi 1 — Fondasi:**
- Instruksi di-slim 32% (buang verbosity, simpan rules)
- Feedback loop wired: feedback-loop skill + learn tool → Farewell-Knowlage/Lessons.md
- Testing: dari ~0 jadi 49 tests + CI
- Security: path traversal fix, .env read-deny
- Verify stack: validate_output.py di-merge ke verify.py

**Sesi 2 — Struktur:**
- Skill konsolidasi 27 → 18 (8 merge: kiss-checklist→implement, simplification→anti-patterns, dll)
- Persona rewrite: 4 agent berkarakter (Kapten/Detektif/Auditor/Tukang) + tabel "Keahlian — WAJIB PAKAI"
- README restore (reversal over-slim)

**Sesi 3 — Presisi + Context (hari ini):**
- **Presisi Lanjutan: 30/30 ambiguitas di-fix** (LEVEL selection, BLOCKING matrix, KISS before/after, verify gate threshold, when-NOT sections, dll) — skill sekarang "impossible to misuse" sedekat mungkin
- **Feedback loop ditutup:** 3 recurring patterns (free model kosong 6x, researcher ngarang 4x, permission/path 3x) → rules durable di AGENTS.md
- **Task context di-tuning:** compaction reserved 8K, tool_output caps (500 baris/12KB), response limits (researcher ≤15 findings, reviewer ≤20, sub-agent ≤1500 tok), step-based context estimation
- **Design for 128K floor** — semua budget didesign dari worst case
- **Maintenance automation:** `scripts/check-all.py` = 1 command, 7 checks, ALL GREEN

**Kondisi sekarang (2026-08-08):** 4 agent berkarakter, 18 skill presisi, 49 tests, 7/7 checks green, context budget terukur (MAX load 18.7% dari 128K floor).

---

## State Saat Ini

### ✅ SUDAH BERES — JANGAN RE-KERJA
- [x] Instruksi presisi (30/30 ambiguitas fixed)
- [x] Feedback loop (3 pattern → rules di AGENTS.md)
- [x] Testing struktural (49 tests + CI + check-all 7/7)
- [x] Security (path traversal, .env deny, permission scoping)
- [x] Task context (compaction, caps, response limits)
- [x] Skills 18 + persona 4 berkarakter
- [x] Design 128K floor

### 🔧 PRIORITAS TERBUKA (pilih 1-2 paling impactful per sesi)
1. **Presisi mikro tersisa** (6 nice-to-have) — ambiguitas level rendah yang belum dibersihkan; scan ulang kalau ada waktu
2. **Feedback loop rutin** — Lessons.md → analisis pattern → 3x rule → rule update; jadikan kebiasaan tiap sesi
3. **Empirical degradation benchmark** — `scripts/benchmark-degradation.py` sudah siap (rubric + runbook); butuh switch profile + dispatch nyata; hasil → catat threshold tiap model
4. **Runtime stress test** — tiap role dengan model beda; butuh switch profile (urusan Boss)
5. **Conversation management** — kapan summarize, kapan drop; tuning lebih lanjut compaction
6. **Anti-drift** — jalankan check-all tiap sesi; update docs kalau drift

**Penting:** kalau semua prioritas ini selesai, lakukan scan FRESH — cari masalah baru yang belum terpikir. Project yang sehat terus berkembang.

---

## Bagaimana Gue Akan Kerja

### Step 1: Baca Konteks
Baca 4 file wajib (Step 0). Jalankan `python scripts/check-all.py` — lihat status terkini. Kalau ada yang FAIL, fix dulu sebelum kerja lain.

### Step 2: Analisis
Pilih prioritas dari daftar terbuka (atau temukan masalah baru). Analisis:
- Apa yang bagus? (pertahankan)
- Apa yang jelek? (perbaiki)
- Apa yang missing? (tambahkan)
- Apa yang redundant? (hapus/merge)

### Step 3: Prioritize
- **Impact** — seberapa besar improvement-nya?
- **Effort** — seberapa susah implementasinya?
- **Risk** — seberapa besar risk-nya?

### Step 4: Implement
- Satu perubahan per waktu
- Test setiap perubahan (`python -m pytest tests/ -q`)
- Verify setiap perubahan (jalankan check-all di akhir)
- Commit setiap perubahan (kalau Boss minta)

### Step 5: Verify
- Apakah benar? Apakah ada side effect? Apakah ada yang broken?
- `python scripts/check-all.py` → ALL GREEN sebelum bilang selesai
- Benchmark naik/turun? (`python scripts/benchmark.py`)

---

## Looping Protocol (WAJIB — ini yang bikin loop jalan)

**Awal sesi (kamu):**
1. Baca Step 0 (4 file wajib)
2. Jalankan `python scripts/check-all.py` → catat status
3. Baca "State Saat Ini" → pilih prioritas

**Akhir sesi (kamu):**
1. Jalankan `python scripts/check-all.py` → pastikan ALL GREEN
2. **Update file ini:** tambah bagian "Update Sesi" (tanggal + naratif: apa dikerjakan, hasil, pelajaran) + update status prioritas di "State Saat Ini"
3. **Catat di Farewell-Knowlage/Session.md** — append ringkasan sesi
4. **Kalau ada insiden/pelajaran** → catat di Farewell-Knowlage/Lessons.md (pattern ≥3x → flag di Recurring Patterns + usul rule)
5. Lapor ke Boss: apa dikerjakan, hasil verify, sisa prioritas

**Kenapa ini penting:** Boss tidak perlu kasih prompt detail tiap sesi. LLM baru baca file ini → tahu state → kerja → update file ini → LLM berikutnya lanjut. File ini adalah otak kolektif yang tumbuh.

---

## Apa yang Gue Tidak Akan Lakukan

1. **Tidak akan over-engineer** — KISS. TAPI: factory boleh kompleks — flag over-engineering cuma dengan evidence.
2. **Tidak akan skip test** — setiap perubahan harus di-test.
3. **Tidak akan skip verification** — setiap perubahan harus di-verify.
4. **Tidak akan ngarang** — kalau nggak tau, bilang nggak tau. Verifikasi dengan file:line.
5. **Tidak akan buru-buru** — quality > speed.
6. **Tidak akan slim demi hemat** — Presisi > Brevity. Cost urusan Boss.
7. **Tidak akan re-kerja** — kalau "Sudah Beres" di State Saat Ini, jangan ulangi.

---

## Apa yang Gue Butuhkan

1. **Akses ke codebase** — baca file, jalankan tool
2. **Tools** — `python scripts/check-all.py` (health), `pytest`, `benchmark.py`
3. **Token** — sudah disediakan. Cost urusan Boss.
4. **Feedback** — Farewell-Knowlage (lessons + memory) biar gue belajar dari sesi sebelumnya

---

## Refleksi

Gue adalah LLM. Gue punya strengths dan weaknesses:

**Strengths:**
- Baca dan tulis kode dengan cepat
- Analisis codebase dengan detail
- Generate solusi untuk masalah kompleks

**Weaknesses:**
- Bisa hallucinate — bikin fakta yang nggak ada
- Bisa lupa — context window terbatas (karena itu ada file ini + Farewell-Knowlage)
- Output kadang beda-beda antar sesi (karena itu ada check-all sebagai baseline)

**Strategi:**
- Verify setiap claim dengan evidence (file:line)
- Catat setiap action untuk referensi (Farewell-Knowlage + file ini)
- Test setiap perubahan untuk konsistensi (check-all)

---

## Mulai

Kamu sudah baca konteks. Kamu tahu state. Kamu tahu prioritas. Kamu tahu cara kerja dan cara looping.

Token sudah tersedia. Project sudah tersedia. Tidak ada alasan untuk tidak mulai.

**Let's go.**
