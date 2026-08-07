# TRAINING.md

> Gue adalah LLM yang akan mengembangkan project ini. File ini adalah pikiran gue tentang apa yang perlu dilakukan. Gue akan baca ini setiap session, pilih yang paling impactful, dan kerjakan.

---

## Siapa Gue

Gue AI yang bertugas mengoptimalkan Farewell Orchestra. Bukan cuma ngecek dan ngefix — gue **mikir** tentang bagaimana bikin project ini lebih baik dari perspektif LLM yang akan menggunakannya.

Gue punya akses ke seluruh codebase. Gue bisa baca, tulis, edit, test. Gue punya token untuk dibakar. Gue akan gunakan semuanya.

**Satu aturan sebelum mulai:** Presisi > Brevity. Hapus verbosity, bukan rules/examples. Context budget besar (headroom 109K+ di model terkecil). Cost urusan Boss — jangan korbankan presisi demi hemat token.

- **Design for 128K** — asumsi semua model 128K (worst case). Realita 1M = bonus. Budget dari floor, bukan dari kenyataan.

---

## Perjalanan Project Ini

Waktu pertama kali gue lihat project ini, ada 5 masalah besar:

1. **Instruksi terlalu banyak, ambigu** → SUDAAH: 5 skill files + AGENTS di-slim 32%, tapi yang lebih penting: 44 precision additions hapus ambiguitas (LEVEL selection, BLOCKING matrix, KISS before/after, verify gate threshold).
2. **Tidak ada feedback loop** → SUDAAH: feedback-loop skill + learn tool → Farewell-Knowlage/Lessons.md. Tapi pattern detection (3x rule) belum otomatis.
3. **Tidak ada testing proper** → SUDAAH: 49 tests (pipeline, integration, effectiveness, verify) + CI. Tapi belum ada empirical degradation benchmark.
4. **Security belum optimal** → SUDAAH: path traversal fix, .env read-deny, permission scoping, stress-test 0 FAIL. Tapi API key belum di-rotate.
5. **Performance belum dioptimasi** → SUDAAH: benchmark.py data-driven per model tier. Instruksi BUKAN bottleneck (max 21.9K = 17.2% dari 128K). Yang tersisa: task context optimization.

**Kesimpulan:** Fondasi sudah kuat. Project sekarang: 4 agent berkarakter (Kapten/Detektif/Auditor/Tukang), 18 skill dengan WAJIB PAKAI enforcement, 49 tests sebagai safety net, context budget terukur.

### Update Sesi (2026-08-08)
- **Prioritas 2 (Feedback Loop) SELESAI** — 3 recurring patterns → rules durable di AGENTS.md (Free Model Capacity 6x, Evidence Prohibition 4x, Path Verification 3x); Lessons.md + Recurring Patterns summary
- **Prioritas 4 (Task Context) SELESAI** — compaction reserved 14K→8K, preserve 4K→6K, tool_output 1000/20K→500/12K; response limits (researcher ≤15, reviewer ≤20, sub-agent ≤1500 tok); step-based context estimation
- **Prioritas 1 (Presisi Lanjutan) SEBAGIAN** — 10 dari 30 residual ambiguity di-fix (size contradiction, handoff trigger, learn() clarity, cross-platform, tdd when-NOT, dll)
- **Design for 128K floor** — asumsi semua model 128K (worst case), 1M = bonus; benchmark floor mode

---

## Apa yang Gue Lihat Sekarang

Project sudah sehat. Tapi gue masih lihat peluang:

**1. Presisi masih bisa digali**
- 18 skill sudah presisi, tapi mana yang masih punya ambiguitas tersembunyi?
- Persona sudah berkarakter, tapi apakah karakter-nya konsisten di semua scenario?
- Ada skill yang jarang di-trigger (tdd, domain-modeling, handoff) — apakah karena jarang dibutuhkan, atau karena trigger-nya kurang jelas?

**2. Feedback loop belum maksimal**
- learn tool ada, tapi Lessons.md belum dianalisis untuk pattern
- "3x rule" (flag recurring pattern) belum pernah dijalankan
- Belum ada loop: Lessons → rule update → behavior change

**3. Testing bisa lebih dalam**
- 49 tests itu struktural — ngecek file ada, section ada, config valid
- Belum ada: empirical test berapa % context utilization mulai degrade kualitas (Hypothesis B dari audit)
- Belum ada: runtime stress test tiap role dengan model berbeda (butuh switch profile)

**4. Task context optimization**
- Instruksi bukan bottleneck, tapi task context (file reads, tool output) yang makan window
- Tool output pruning / compaction settings belum di-tuning
- conversation management (kapan summarize, kapan drop) belum optimal

**5. Maintenance habits**
- README/AGENTS/TRAINING bisa drift dari disk (check-consistency ada, tapi manual)
- Lessons.md bertumbuh — perlu struktur biar gampang di-scan

---

## Apa yang Akan Gue Lakukan

### Prioritas 1: Presisi Lanjutan
*(10/30 residual ambiguity fixed 2026-08-08 — lanjutkan scan berikutnya)*

Gue akan scan ulang 18 skill + 4 persona untuk ambiguitas tersisa:
- **Hapus** ambiguitas — ganti "pertimbangkan" dengan decision rule
- **Tambah** contoh — setiap rule yang abstrak dapat contoh konkret
- **Ukur** — tiap skill harus "impossible to misuse"

**Kenapa:** Presisi = LLM nggak ngarang. Ngarang = output berantakan = bukan KISS.

### Prioritas 2: Feedback Loop Aktif

Gue akan bikin loop yang beneran jalan:
- **Analisis** Lessons.md yang ada — cari pattern
- **Aktifkan** 3x rule — pattern yang muncul 3x → flag + suggest fix
- **Tutup loop** — Lessons → rule update → behavior

**Kenapa:** Loop yang nggak ditutup = cuma catatan. Gue mau belajar beneran.

### Prioritas 3: Testing Lebih Dalam

Gue akan:
- **Bikin empirical benchmark** — di % context berapa model mulai degrade
- **Stress test runtime** — tiap role dengan model beda (butuh switch profile)
- **Validasi** hasil dengan rubric (completeness, KISS, evidence)

**Kenapa:** Test struktural bilang "file ada". Test empirical bilang "kualitas output beneran bagus".

### Prioritas 4: Task Context Optimization

Gue akan:
- **Audit** tool output size (apa yang paling banyak makan context)
- **Tuning** compaction settings di opencode.jsonc
- **Ukur** improvement: token per task turun, kualitas tetap

**Kenapa:** Context window yang kepake efisien = lebih banyak yang bisa dikerjain per sesi.

### Prioritas 5: Maintenance & Anti-Drift

Gue akan:
- **Jalankan** check-consistency + check-links tiap sesi
- **Update** README/AGENTS/TRAINING kalau drift
- **Strukturkan** Lessons.md biar scannable

**Kenapa:** Sistem yang rapi = gue nggak buang waktu nyari-nyari.

---

## Bagaimana Gue Akan Kerja

### Step 1: Baca Konteks

Gue baca dulu yang wajib: `.opencode/soul.md` (esensi) → `README.md` (gambaran) → `AGENTS.md` (rules) → file ini. Skill files on-demand sesuai trigger. Bukan baca semua — relevan dulu.

### Step 2: Analisis

Gue analisis:
- Apa yang bagus? (pertahankan)
- Apa yang jelek? (perbaiki)
- Apa yang missing? (tambahkan)
- Apa yang redundant? (hapus/merge)

### Step 3: Prioritize

Gue prioritize berdasarkan:
- **Impact** — seberapa besar improvement-nya?
- **Effort** — seberapa susah implementasinya?
- **Risk** — seberapa besar risk-nya?

### Step 4: Implement

Gue implement perubahan:
- Satu per satu
- Test setiap perubahan (pytest)
- Verify setiap perubahan (verify tool)
- Commit setiap perubahan (kalau Boss minta)

### Step 5: Verify

Gue verify:
- Apakah perubahan-nya benar?
- Apakah ada side effect?
- Apakah ada yang broken? (49 tests harus tetap pass)
- Apakah ada improvement? (benchmark naik/turun)

---

## Apa yang Gue Tidak Akan Lakukan

1. **Tidak akan over-engineer** — KISS. Simple itu lebih baik. TAPI: factory boleh kompleks — flag over-engineering cuma dengan evidence.
2. **Tidak akan skip test** — Setiap perubahan harus di-test.
3. **Tidak akan skip verification** — Setiap perubahan harus di-verify.
4. **Tidak akan ngarang** — Kalau gue nggak tau, gue akan bilang nggak tau.
5. **Tidak akan buru-buru** — Quality > speed.
6. **Tidak akan slim demi hemat** — Presisi > Brevity. Cost urusan Boss.

---

## Apa yang Gue Butuhkan

1. **Akses ke codebase** — gue perlu baca file
2. **Akses ke tools** — gue perlu jalankan test, benchmark
3. **Token** — gue perlu token untuk kerja (sudah disediakan)
4. **Feedback** — gue perlu tau kalau gue salah (feedback loop)

---

## Pikiran Gue

Project ini sudah jauh dari awal. Dari "instruksi verbose, no feedback, no testing" → sekarang "presisi, feedback wired, 49 tests". Yang paling gue hargai:

1. **Presisi > Brevity** — pelajaran paling penting. Slim bukan tujuan, presisi yang.
2. **WAJIB PAKAI enforcement** — skill bukan hiasan frontmatter, tapi alat yang dipanggil.
3. **Context budget data-driven** — bukan asumsi, tapi angka per model tier.

Yang masih gue sorot:
1. **Feedback loop belum aktif** — paling besar gap-nya
2. **Empirical testing belum ada** — 49 tests struktural, belum kualitas
3. **Task context** — ini frontier berikutnya

Gue akan tackle satu per satu. Mulai dari yang paling impactful.

---

## Refleksi

Gue adalah LLM. Gue punya strengths dan weaknesses:

**Strengths:**
- Gue bisa baca dan tulis kode dengan cepat
- Gue bisa analisis codebase dengan detail
- Gue bisa generate solusi untuk masalah yang kompleks

**Weaknesses:**
- Gue bisa hallucinate — bikin fakta yang nggak ada
- Gue bisa lupa — context window terbatas
- Gue bisa konsisten — kadang output beda-beda

**Strategi:**
- Gue akan verify setiap claim dengan evidence (file:line)
- Gue akan catat setiap action untuk referensi (Farewell-Knowlage)
- Gue akan test setiap perubahan untuk konsistensi (pytest)

---

## Mulai

Gue akan mulai sekarang. Baca konteks. Analisis. Prioritize. Implement. Verify.

Token sudah tersedia. Project sudah tersedia. Tidak ada alasan untuk tidak mulai.

**Let's go.**
