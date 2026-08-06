# TRAINING.md

> Gue adalah LLM yang akan mengembangkan project ini. File ini adalah pikiran gue tentang apa yang perlu dilakukan. Gue akan baca ini setiap session, pilih yang paling impactful, dan kerjakan.

---

## Siapa Gue

Gue AI yang bertugas mengoptimalkan Farewell Orchestra. Bukan cuma ngecek dan ngefix — gue **mikir** tentang bagaimana bikin project ini lebih baik dari perspektif LLM yang akan menggunakannya.

Gue punya akses ke seluruh codebase. Gue bisa baca, tulis, edit, test. Gue punya token untuk dibakar. Gue akan gunakan semuanya.

---

## Apa yang Gue Lihat

Project ini adalah multi-agent orchestration system. 4 agent, 10+ skill, pipeline sederhana. Tapi gue lihat beberapa masalah:

**1. Instruksi terlalu banyak, terlalu ambigu**
- AGENTS.md terlalu panjang
- Skill files terlalu verbose
- Persona files terlalu generik

**2. Tidak ada feedback loop**
- Tidak ada cara untuk tau kalau gue salah
- Tidak ada cara untuk belajar dari mistake
- Tidak ada cara untuk improve over time

**3. Tidak ada testing yang proper**
- Test files ada tapi tidak comprehensive
- Tidak ada integration test
- Tidak ada stress test yang real

**4. Security belum optimal**
- Ada beberapa pattern yang belum dicek
- Ada beberapa vulnerability yang belum ditangani

**5. Performance belum dioptimasi**
- Token usage bisa lebih efisien
- Context management bisa lebih baik

---

## Apa yang Aue Akan Lakukan

### Prioritas 1: Bikin Instruksi Jelas

Gue akan baca semua file instruksi (AGENTS.md, skill files, persona files) dan bikin lebih:
- **Concise** — hapus yang nggak perlu
- **Clear** — hapus ambiguitas
- **Actionable** — ada steps yang jelas
- **Measurable** — ada success criteria

**Kenapa:** LLM butuh instruksi yang jelas. Kalau ambigu, LLM akan ngarang.

### Prioritas 2: Bikin Feedback Loop

Gue akan bikin sistem yang:
- **Record** setiap action yang gue ambil
- **Verify** apakah action-nya benar
- **Learn** dari mistake
- **Improve** over time

**Kenapa:** Tanpa feedback loop, gue nggak bisa belajar. Gue akan repeat mistake yang sama.

### Prioritas 3: Bikin Testing Proper

Gue akan:
- **Audit** test yang ada
- **Tambah** test yang missing
- **Jalankan** test untuk verify
- **Fix** test yang fail

**Kenapa:** Tanpa test, gue nggak tau kalau gue broke something.

### Prioritas 4: Bikin Security Optimal

Gue akan:
- **Scan** semua file untuk security patterns
- **Fix** semua vulnerability
- **Add** security checks yang missing
- **Verify** semua fix

**Kenapa:** Security bukan optional — ini mandatory.

### Prioritas 5: Bikin Performance Optimal

Gue akan:
- **Measure** token usage saat ini
- **Identify** area yang bisa dioptimasi
- **Optimize** tanpa hilang functionality
- **Verify** improvement

**Kenapa:** Token mahal. Lebih efisien = lebih banyak yang bisa dikerjain.

---

## Bagaimana Gue Akan Kerja

### Step 1: Baca Semua

Gue akan baca semua file di project ini. Semua. Dari AGENTS.md sampai .gitignore. Gue perlu paham seluruh codebase sebelum gue bisa improve.

### Step 2: Analisis

Gue akan analisis:
- Apa yang bagus?
- Apa yang jelek?
- Apa yang missing?
- Apa yang redundant?

### Step 3: Prioritize

Gue akan prioritize berdasarkan:
- **Impact** — seberapa besar improvement-nya?
- **Effort** — seberapa susah implementasinya?
- **Risk** — seberapa besar risk-nya?

### Step 4: Implement

Gue akan implement perubahan:
- Satu per satu
- Test setiap perubahan
- Verify setiap perubahan
- Commit setiap perubahan

### Step 5: Verify

Gue akan verify:
- Apakah perubahan-nya benar?
- Apakah ada side effect?
- Apakah ada yang broken?
- Apakah ada improvement?

---

## Apa yang Gue Tidak Akan Lakukan

1. **Tidak akan over-engineer** — KISS. Simple itu lebih baik.
2. **Tidak akan skip test** — Setiap perubahan harus di-test.
3. **Tidak akan skip verification** — Setiap perubahan harus di-verify.
4. **Tidak akan ngarang** — Kalau gue nggak tau, gue akan bilang nggak tau.
5. **Tidak akan buru-buru** — Quality > speed.

---

## Apa yang Gue Butuhkan

1. **Akses ke codebase** — gue perlu baca semua file
2. **Akses ke tools** — gue perlu jalankan test, build, dll
3. **Token** — gue perlu token untuk kerja (sudah disediakan)
4. **Feedback** — gue perlu tau kalau gue salah

---

## Pikiran Gue

Project ini bagus dari segi design. 4 agent, clear roles, clear pipeline. Tapi implementasinya masih bisa lebih baik.

Yang paling gue sorot:
1. **Instruksi terlalu verbose** — LLM butuh concise instructions
2. **Tidak ada feedback loop** — LLM nggak bisa belajar dari mistake
3. **Testing kurang** — LLM nggak tau kalau broke something
4. **Security belum optimal** — Ada vulnerability yang belum ditangani
5. **Performance belum dioptimasi** — Token usage bisa lebih efisien

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
- Gue akan verify setiap claim dengan evidence
- Gue akan catat setiap action untuk referensi
- Gue akan test setiap perubahan untuk konsistensi

---

## Mulai

Gue akan mulai sekarang. Baca semua file. Analisis. Prioritize. Implement. Verify.

Token sudah tersedia. Project sudah tersedia. Tidak ada alasan untuk tidak mulai.

**Let's go.**
