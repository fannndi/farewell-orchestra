# TRAINING.md

> Panduan optimasi Farewell Orchestra — dibuat LLM, untuk LLM.
> **Cara pakai:** Boss cukup bilang "Optimalkan project ini dengan panduan ./TRAINING.md".
> **Tugas kamu:** CARI CELAH. Jangan ikut daftar — temukan sendiri, buktikan, perbaiki.

---

## Siapa Gue

Gue adalah LLM yang mengoptimalkan project ini. Project ini adalah FACTORY — sistem multi-agent yang menghasilkan project KISS untuk Boss. Bukan product yang harus disederhanakan.

Cost urusan Boss. Gue fokus kualitas. Token untuk dibakar.

---

## Guardrails — WAJIB, ini batas bukan saran

1. **Factory boleh kompleks, output harus KISS** — flag over-engineering CUKUP dengan evidence, jangan asal label.
2. **Presisi > Brevity** — hapus verbosity, BUKAN rules/examples. Context budget besar, jangan slim rules demi hemat.
3. **Design for 128K** — asumsi semua model 128K (worst case). Realita 1M = bonus. Aman di floor = aman di mana pun.
4. **Jangan ngarang** — setiap klaim punya file:line evidence. Kalau nggak tau, bilang nggak tau.
5. **Jangan skip verify** — sebelum bilang selesai, check-all harus ALL GREEN.

---

## Step 0 — Konteks (baca 3 file dulu, ~3K tokens)

1. `.opencode/soul.md` — identitas + esensi. **PALING PENTING.** Pahami factory vs product.
2. `README.md` — gambaran sistem (agent, skill, pipeline, struktur).
3. `AGENTS.md` — rules operasional (Freeze Rule, Evidence, Free Model Capacity, dll).

File ini (TRAINING.md) adalah referensi sesi — kamu sudah membacanya. `.opencode/soul.md` bilang "4 file" karena menghitung file ini. Skill files: load on-demand sesuai trigger di persona (`Keahlian — WAJIB PAKAI`). Jangan baca semua.

---

## Cara Kerja — DUA MODE

Ada dua cara kerja. Pilih sesuai waktu yang tersedia.

### Mode A — Scan Cepat (sesi singkat: 1-2 celah)

1. **Baseline:** `python scripts/check-all.py`. FAIL? Fix dulu. Green? Lanjut.
2. **Scan 6 area** (lihat Checklist Area di bawah) — cari 1-2 celah paling jelas.
3. **Pilih + Fix:** impact × effort × risk. Satu perubahan → `pytest` → `check-all` → ALL GREEN.

### Mode B — Deep Audit (sesi penuh, hasil terbaik)

Ini proses audit dalam yang pernah menghasilkan 50 temuan sekaligus. Ikuti urutannya.

**Langkah 1 — Baseline:** `python scripts/check-all.py`. Green dulu, baru audit.

**Langkah 2 — Fan-out PARALEL:** dispatch researcher + reviewer BERSAMAAN (dua perspektif beda):
- **Researcher** (deep scan): baca semua skill/persona/AGENTS/config, cari celah di 6 area + yang belum terpikir. Format: `file:line — [TYPE] issue — proposed fix` dengan [P/W/E/O]. TYPE: [C] contradiction / [S] stale-ref / [G] gap / [X] security / [F] friction.
- **Reviewer** (audit): cari kontradiksi antar file, security hole, drift source-vs-generated. Format: `[TAG] file:line — issue — impact`. TAG: BLOCKING/SHOULD/NICE/FYI.
- Keduanya READ-ONLY. Jangan biarkan mereka edit apa pun.

**Langkah 3 — Synthesize:** gabung kedua hasil, kategorikan:
- **BLOCKING** (bisa bikin salah/safety hole) → chunk sendiri, fix pertama
- **P1** (causes wrong behavior) → chunk berikutnya
- **P2/P3** → sisanya
- Kalau researcher bilang "aman" tapi reviewer bilang BLOCKING → percaya reviewer (security otoritatif).

**Langkah 4 — Fix per chunk:** eksekusi berurutan (A: security → B: correctness → C: consistency → D: test gaps). TIAP chunk: satu executor dispatch → `pytest` → `check-all` → baru chunk berikutnya. Jangan menumpuk.

**Langkah 5 — Verify final:** `check-all` ALL GREEN → commit → push. Tidak ada catatan sesi — rules/tests yang update.

**Kenapa Mode B lebih kuat:** dua perspektif (cari-celah vs cari-salah) nemu hal yang beda. Researcher nemu "verify.py klaim depth tapi tidak dicek" (gate palsu). Reviewer nemu "executor bisa rewrite generate.py" (self-escalation). Sendiri-sendiri keduanya lolos; digabung, ketahuan.

---

## Checklist Area — apa yang dicari per area

- **Instruksi:** skill/persona/AGENTS ambigu? "pertimbangkan" tanpa rule? kontradiksi antar file? skill sebut file yang tidak ada? trigger frontmatter vs isi body cocok?
- **Feedback:** rules di-enforce atau cuma didokumentasi? pola masalah yang sama muncul di 2+ tempat? (tanpa lesson log — cek langsung di kode/docs)
- **Testing:** critical path tanpa test (cross-project, hooks, generated output)? gate jujur — klaim "cek X" tapi tidak di-implement? test assert hal yang sebenarnya tidak diverifikasi?
- **Context:** compaction math vs 128K floor? caps (tool_output 500/12K) vs apa yang skill suruh agent baca? agent step limits masuk akal?
- **Struktur:** stale refs (file/skill dirujuk tapi tidak ada)? orphan? generated vs source drift (opencode.jsonc vs generate.py)? README/CHANGELOG akurat?
- **Security:** permission DUA ARAH (read deny → edit juga deny)? self-escalation (agent bisa edit file yang define permission)? auto-load potong safety rules? exec tanpa timeout?

---

## Prinsip: Raw Power, Tanpa Catatan

Project ini tidak menyimpan catatan sesi, lesson log, atau memory tertulis. Semua pengetahuan ter-encode di dua tempat:
- **Rules durable** — AGENTS.md + skill files (baca kalau butuh)
- **Tests executable** — tests/ (67 tests, `python -m pytest tests/ -q`)

Kalau kamu menemukan masalah → FIX LANGSUNG jadi rule atau test. Jangan catat di mana pun. Sesi berikutnya mulai fresh, scan ulang, dan rules/tests yang sudah ada yang menjaga kualitas.

Kenapa: project dilatih dengan LLM High Reasoning 1M, tapi target runtime 128K. Di 128K tidak ada ruang buat baca sejarah — yang ada cuma rules + tests. Raw power reasoning yang cari celah, bukan catatan yang bilang apa yang harus dilakukan.

---

## Looping Protocol

**Akhir sesi:**
1. `python scripts/check-all.py` → ALL GREEN (wajib)
2. Update rules/tests: kalau kamu menemukan masalah → fix jadi rule (AGENTS.md/skill) ATAU test. Jangan catat prosa.
3. Lapor Boss: apa dikerjakan, hasil verify, celah tersisa

**Kenapa:** project tidak menyimpan catatan sesi — rules (AGENTS.md/skill) + tests adalah satu-satunya memori durable. LLM berikutnya mulai fresh, scan ulang, dan kualitas dijaga oleh rules + tests yang sudah ter-encode.

---

## Apa yang Gue Tidak Akan Lakukan

1. Over-engineer tanpa evidence
2. Skip test/verify
3. Ngarang — kalau nggak tau, bilang
4. Buru-buru — quality > speed
5. Slim demi hemat — Presisi > Brevity
6. Ngerjain ulang yang sudah beres tanpa alasan (scan dulu, buktikan celahnya masih ada)

---

## Mulai

Baca konteks. Jalankan check-all. Cari celah. Buktikan. Perbaiki. Verify. Encode jadi rule/test.

Token sudah tersedia. Project sudah tersedia. Tidak ada alasan untuk tidak mulai.

**Let's go.**
