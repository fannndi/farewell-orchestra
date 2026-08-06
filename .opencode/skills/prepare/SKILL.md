---
name: prepare
description: Use when receiving a request — validate input, extract requirements, chunk if needed. Gate before orchestration.
activation: ALWAYS at start of every request
trigger: Any request from Boss
---
# Prepare
Gate awal sebelum dispatch. Flow:
```
Request → Cross-Project? → YES → Check Docs → Reverse Engineer? → Generate → Normal Flow
                ↓ NO
         Input Validation → HOLD? STOP. PARTIAL? → Grill. PASS? → Chunk → Dispatch
```

## Fallback Mode (untuk semua LLM)
Kalau LLM tidak bisa handle complex instructions: cek request punya goal+scope. Ada → PASS. Nggak → HOLD, tanya: "Goal-nya apa? Scope-nya?"
Contoh: `HOLD — goal tidak jelas`
Skip chunking, assumption logger, dll — cukup cek goal+scope.

## 0. Cross-Project Detection
Kalau user mention path project lain atau bilang "kerja di project X":
1. **Check docs** — `glob <project>/docs/*.md`
2. **Core docs:** PRD.md, Architecture.md, Rules.md, Tasks.md, Context.md (WAJIB)
3. **Conditional:** Schema.md (kalau ada DB), API_Contract.md (kalau ada API)
4. **All CORE exist?** → baca docs → pahami context → normal flow (§1)
5. **Ada yang hilang?** → Reverse Engineering Mode

### §0.1 Reverse Engineering Mode
Deep scan via researcher. Lihat `cross-project/guide.md` untuk full flow (5 phases: Structure → Config → Code Patterns → Tests & Docs → Inference).
**Output:** 5 core docs + 2 conditional. Dispatch **executor** untuk generate.
**Consistency Rules:**
- Nama variabel/tabel di Schema.md = nama field di API_Contract.md
- Tech stack di Architecture.md = konvensi di Rules.md
- Fitur di PRD.md = task di Tasks.md
**PRD-Already-Exists:** PRD sudah ada → baca PRD, extract tech stack/features/architecture, generate docs dari PRD + code scan ringan (verify accuracy, bukan discover from scratch).
Permission: See AGENTS.md Permission First.
Project type: See AGENTS.md Project Type Detection.

## 1. Input Validation
Cek request punya 4 elemen:

| Elemen | Wajib | Kalau kosong |
|--------|-------|-------------|
| **Goal** | YA | STOP. Tanya: "Goal-nya apa?" |
| **Scope** | YA | STOP. Tanya: "File/folder mana?" |
| **Acceptance** | YA | Usulkan 1 cara test, minta konfirmasi |
| **Risk** | Default LOW | Pakai LOW kalau tidak disebut |

**Max 2 rounds konfirmasi acceptance.** Boss masih disagree → default "Verify via existing test suite" → PASS.

**Trash detection** — STOP + clarify kalau:
- <10 kata tanpa konteks ("perbaikin", "tambahin")
- Ambigu multi-interpretasi ("benerin itu")
- Kontradiktif dalam satu request
- Scope liar ("refactor semuanya") tanpa batasan
- **Contradiction:** request sebelumnya bilang A, sekarang bilang B → flag: "Kontradiksi: [A] vs [B]. Mana yang benar?"
- **Wrong order:** request minta X sebelum Y padahal Y prerequisite X → flag: "Urutan salah: [Y] harus sebelum [X]?"
- **Terserah/terserah lo:** Boss bilang "terserah lo" → PARTIAL, force grill: "Gue butuh spesifik. Goal-nya apa?"
- **Impossible request:** request yang tidak feasible (prediksi masa depan, buat AGI) → HOLD: "Ini tidak feasible. Alternatif?"
- **Panic mode:** Boss panik, kasih info vague ("production down!", "cepetan!") → tanya spesifik: "Error apa? Gejalanya?"
- **Dependency:** request mention "depends on", "requires", "needs" → cek dependency ada. Tidak ada → HOLD
- **Constraint:** request mention "jangan ubah", "tetap", "keep" → catat constraint. Violation = BLOCKING
- **Scope limit:** request mention "cuma", "hanya", "only" → catat scope limit. Exceed = BLOCKING
- **Test request:** request mention "test", "verify", "pastikan" → executor WAJIB verify. Skip = BLOCKING

**Output decision:**
- `HOLD [alasan]` → STOP. Tanya Boss.
- `PARTIAL` → lanjut ke §2 Assumption Logger, lalu §3 Grill.
- `PASS [SIZE]` → lanjut ke §4 Task Chunking.
Size: TRIVIAL (1 file, ≤3 baris) / SMALL (1-2 files, ≤50 baris) / MEDIUM (3-5 files, ≤200 baris) / LARGE (>5 files ATAU >200 baris) / MASSIVE (>10 files ATAU >500 baris)

## 2. Assumption Logger
Hanya kalau PARTIAL. Auto-generate asumsi implisit, max 3:
```
Asumsi:
1. [asumsi 1] — ok?
2. [asumsi 2] — ok?
```
Boss reply `1:ya 2:tidak → pakai X` atau `semua ok`.
**Rubber-stamp guard:** "ok" semua tanpa edit → flag "Asumsi belum dikonfirmasi. Konfirmasi 1 per 1?" Jangan lanjut sebelum asumsi benar-benar dikonfirmasi.

## 3. Requirement Extraction (Grill)
Kalau PARTIAL setelah Assumption Logger:

| Level | Pertanyaan |
|-------|-----------|
| Goal | Apa yang mau dicapai? |
| Scope | Batasan? In/Out? |
| Constraints | Tech stack? Deadline? |
| Acceptance | Gimana tau selesai? |
| Risk | Apa yang bisa gagal? |
| Edge cases | Input kosong? Concurrent? |

Satu `question` tool call = satu pertanyaan. Max 8 pertanyaan, lalu sign-off paksa dengan asumsi default.

**Default asumsi kalau Boss tidak jawab:** Goal=terjemahkan literally, Scope=punya Boss aja, Constraints=none, Acceptance="build pass + verify command", Risk=LOW, Edge cases=skip.
**Pendulum Check:** Over-spec (10 library, 5 pattern) → tanya "Prioritas?". Under-spec (terlalu umum) → paksa "Contoh input/output?"

## 4. Task Chunking
Trigger chunk kalau: **Q≥3** (pertanyaan) ATAU **F≥3** (file) ATAU **O≥2** (format output).

**Q** = pertanyaan pending dari grill. **F** = file di scope. **O** = jumlah format output beda (code, markdown, JSON = 3).

| Size | Action | Chunk Strategy |
|------|--------|----------------|
| TRIVIAL/SMALL | 1 chunk, fan-out normal | — |
| MEDIUM (F=3-5) | 1 chunk, fan-out normal | — |
| LARGE (F=3-10) | 2-3 chunk | Per module/feature, ≤3 file per chunk |
| MASSIVE (F>10) | 3-4 chunk | Per layer (FE/BE/DB), ≤3 file per chunk |

Per chunk: ≤3 file, 1 fokus, 1 format. **DALAM chunk:** parallel. **ANTAR chunk:** sequential dengan CONTEXT_SUMMARY.

**fan-out normal** = dispatch researcher + reviewer parallel (MEDIUM+), researcher only (SMALL), direct executor (TRIVIAL).
**Sampling (F>50):** Prioritaskan entry points → core modules → config → tests. Max 20 file per chunk. Skip node_modules, dist, build, vendor, .git.
Sub-agent boleh return `[CHUNK_REQUIRED]` kalau task kegedean → re-chunk, bukan gagal.
