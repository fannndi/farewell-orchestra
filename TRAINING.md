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

**Langkah 5 — Verify final + simpan:** `check-all` ALL GREEN → commit → push → update file ini + Session.md + Lessons.md.

**Kenapa Mode B lebih kuat:** dua perspektif (cari-celah vs cari-salah) nemu hal yang beda. Researcher nemu "verify.py klaim depth tapi tidak dicek" (gate palsu). Reviewer nemu "executor bisa rewrite generate.py" (self-escalation). Sendiri-sendiri keduanya lolos; digabung, ketahuan.

---

## Checklist Area — apa yang dicari per area

- **Instruksi:** skill/persona/AGENTS ambigu? "pertimbangkan" tanpa rule? kontradiksi antar file? skill sebut file yang tidak ada? trigger frontmatter vs isi body cocok?
- **Feedback:** `Farewell-Knowlage/Lessons.md` pattern berulang (3x rule)? rules di-enforce atau cuma didokumentasi? learn() flow incident → Lessons → rule benar-benar jalan?
- **Testing:** critical path tanpa test (cross-project, hooks, generated output)? gate jujur — klaim "cek X" tapi tidak di-implement? test assert hal yang sebenarnya tidak diverifikasi?
- **Context:** compaction math vs 128K floor? caps (tool_output 500/12K) vs apa yang skill suruh agent baca? agent step limits masuk akal?
- **Struktur:** stale refs (file/skill dirujuk tapi tidak ada)? orphan? generated vs source drift (opencode.jsonc vs generate.py)? README/CHANGELOG akurat?
- **Security:** permission DUA ARAH (read deny → edit juga deny)? self-escalation (agent bisa edit file yang define permission)? auto-load potong safety rules? exec tanpa timeout?

---

## Pola Temuan Historis — cek ini dulu, jangan temukan ulang

Pola yang sudah pernah ditemukan di deep audit. Kalau kamu scan, cek pola ini LEBIH DULU (kemungkinan besar masih ada atau muncul lagi):

1. **Gate palsu** — tool klaim cek sesuatu tapi tidak di-implement (verify.py klaim depth D1-D4 tapi regex tidak match). Cek: klaim vs implementasi.
2. **Permission satu arah** — read deny secrets tapi edit allow → agent bisa overwrite/create secrets. Cek: deny harus dua arah.
3. **Self-escalation** — agent punya edit access ke file yang define permission (generate.py, opencode.jsonc, agents/) → bisa naikin permission sendiri. Cek: deny file permission-defining.
4. **Auto-load truncation** — context file dipotong raw-line, safety rules (## Rules) hilang → model tidak dapat constraint. Cek: truncation per-section, bukan per-line.
5. **Stale refs** — referensi ke skill/file yang sudah di-merge/dihapus (quality-gates → code-review). Cek: grep nama lama.
6. **Test gap** — critical path tanpa test (cross-project, hooks, generated output). Cek: setiap flow punya test?
7. **Config drift** — opencode.example.jsonc bisa ketinggalan dari generate.py (misal: skill allowlist, permission). Cek: example = real config minus profile; regenerate + diff.
8. **Orphan trigger** — skill di trigger table tapi tidak ada jalur real untuk di-load. Cek: trigger → jalur eksekusi.
9. **Deny-map hole** — deny permission-defining SURFACE (hooks/tools/skills), bukan cuma config files. Kalau deny cuma di config files, executor masih bisa edit .opencode/** → auto-run code / subprocess / instruction injection. Cek: deny mencakup hooks/tools/skills/agents, bukan hanya opencode.jsonc.

---

## Looping Protocol — yang bikin sesi ini berguna untuk sesi berikutnya

**Akhir sesi:**
1. `python scripts/check-all.py` → ALL GREEN (wajib)
2. Update file ini: ganti bagian "Update Sesi" di bawah dengan catatan singkat (2-5 baris naratif: apa dikerjakan, celah apa yang ditemukan, pelajaran)
3. Catat di `Farewell-Knowlage/Session.md` (ringkasan) + `Lessons.md` (insiden/pelajaran)
4. Lapor Boss: apa dikerjakan, hasil verify, celah tersisa

**Kenapa:** Boss tidak perlu prompt detail tiap sesi. LLM berikutnya baca file ini → langsung tahu arah → lanjut cari celah. File ini otak kolektif yang tumbuh.

---

## Update Sesi

_(isi di akhir sesi, 2-5 baris naratif: apa yang dikerjakan, celah apa yang ditemukan, pelajaran. Update juga pola temuan historis kalau ada pola baru.)_

**Sesi deep audit (2026-08-08):** fan-out researcher+reviewer nemu 50 temuan. Fix: security hardening (executor edit deny map, learn.ts mkdir, auto-load full persona), verify gate depth beneran di-enforce (BLOCKING=[D3]+), allowlist tidak dekoratif, 67 tests (dari 49). Pelajaran: dua perspektif (cari-celah + cari-salah) nemu hal yang beda — gabung keduanya. Pola baru #1 (gate palsu) dan #2 (permission satu arah) ditemukan di sesi ini.

**Sesi deep audit R2 (2026-08-08):** deny-map hole — round-1 cuma blok config files, tapi executor masih bisa edit .opencode/** (hooks = auto-run code, tools = subprocess, skills = instruction injection) → ditutup (.opencode/** + AGENTS.md + cross-project/guide.md). verify.py: review stage reject [P/W/E/O] (false gate) + multi-line depth — fixed. learn.ts atomic append (lock) + insertion bound ke main table. npm* → ask (RCE via editable package.json). ci.yaml ||true dihapus (drift bikin CI FAIL). Pola baru #9: "deny-map hole" — deny permission-defining SURFACE (hooks/tools/skills), bukan cuma config files.

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

Baca konteks. Jalankan check-all. Cari celah. Buktikan. Perbaiki. Verify. Update file ini.

Token sudah tersedia. Project sudah tersedia. Tidak ada alasan untuk tidak mulai.

**Let's go.**
