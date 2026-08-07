# Skills: orchestrator

=== prepare ===
---
name: prepare
description: Use when receiving a request — validate input, extract requirements, chunk if needed. Gate before orchestration.
activation: ALWAYS at start of every request
trigger: Any request from Boss
---
Gate awal sebelum dispatch. Flow:
```
Request → Cross-Project? → YES → Check Docs → Reverse Engineer? → Generate → Normal Flow
                ↓ NO
         Input Validation → HOLD? STOP. PARTIAL? → Grill. PASS? → Chunk → Dispatch
```
Kalau LLM tidak bisa handle complex instructions: cek request punya goal+scope. Ada → PASS. Nggak → HOLD, tanya: "Goal-nya apa? Scope-nya?"
Contoh: `HOLD — goal tidak jelas`
Skip chunking, assumption logger, dll — cukup cek goal+scope.
Kalau user mention path project lain atau bilang "kerja di project X":
1. **Check docs** — `glob <project>/docs/*.md`
2. **Core docs:** PRD.md, Architecture.md, Rules.md, Tasks.md, Context.md (WAJIB)
3. **Conditional:** Schema.md (kalau ada DB), API_Contract.md (kalau ada API)
4. **All CORE exist?** → baca docs → pahami context → normal flow (§1)
5. **Ada yang hilang?** → Reverse Engineering Mode
Deep scan via researcher. Lihat `cross-project/guide.md` untuk full flow (5 phases: Structure → Config → Code Patterns → Tests & Docs → Inference).
**Output:** 5 core docs + 2 conditional. Dispatch **executor** untuk generate.
**Consistency Rules:**
- Nama variabel/tabel di Schema.md = nama field di API_Contract.md
- Tech stack di Architecture.md = konvensi di Rules.md
- Fitur di PRD.md = task di Tasks.md
**PRD-Already-Exists:** PRD sudah ada → baca PRD, extract tech stack/features/architecture, generate docs dari PRD + code scan ringan (verify accuracy, bukan discover from scratch).
Permission: See AGENTS.md Permission First.
Project type: See AGENTS.md Project Type Detection.
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
Hanya kalau PARTIAL. Auto-generate asumsi implisit, max 3:

=== orchestrate ===
---
name: orchestrate
description: Use after prepare passes — decompose, fan-out parallel, synthesize, brief executor.
activation: After prepare returns PASS
trigger: prepare PASS → load orchestrate
---
Input sudah CLEAN. Flow:
```
Decompose → Evidence Bundle → Ping → Fan-Out → Synthesize → Validate & Verify → Brief Executor → Post-Flight
```
Kalau LLM tidak bisa handle complex instructions: Decompose 2-3 bagian → Fan-Out researcher+reviewer → Synthesize max 3 bullet → Brief executor (TASK/FILES/VERIFY) → Report `<what> · <result> · <risk>`
Contoh: `Auth module added · pytest pass · residual: rate limiting`
Skip evidence bundle, ping guard, dll — cukup flow dasar.
Pecah jadi work packages independen. Tiap package ≤5 baris brief.
**Contoh work package:** "Fix auth bypass di login.js" = 1 package. "Refactor auth module (login.js, token.js, middleware.js)" = 1 package (satu domain). "Fix auth bug + tambah logging di api.js" = 2 packages (domain beda).
| Event | Action |
|-------|--------|
| Researcher: BLOCKING found | Escalate ke Boss langsung |
| Researcher: CRITICAL finding | Escalate ke Boss langsung |
| Reviewer: BLOCKING found | Escalate ke Boss langsung |
| Either: ABORT error | Stop semua, escalate ke Boss |
**Priority:** ABORT stop semua > BLOCKING/CRITICAL escalate langsung > normal tunggu keduanya selesai.
| Lane | Sumber | Output |
|------|--------|--------|
| Memory | sub-project.md | agent terakhir kerja apa |
| Lessons | Farewell-Knowlage/Lessons.md (external Obsidian vault) | error pattern: n kejadian |
| State | git status | file modified, bersih |
| Config | opencode.jsonc | profile name |
**REDACTION:** Hapus secret, API keys, token, path absolut sebelum dispatch.
```
task(subagent_type=<agent>, prompt='Reply with exactly: READY')
```
- Non-empty response → alive. Proceed.
- Empty/error → DEAD. Researcher/reviewer: SKIP. Executor: ESCALATE ke Boss.
**SKIP researcher** → reviewer-only audit + flag "Researcher offline. Reviewer-only." **SKIP reviewer** → researcher-only + flag. **SKIP both** → ESCALATE. **Executor DEAD** → ESCALATE langsung.
**Valid ping response:** mengandung "READY" (case-insensitive). Selain itu → retry sekali, lalu DEAD.
Dispatch researcher + reviewer **PARALLEL**:
```python
task(subagent_type="researcher", description="...", prompt="brief + evidence bundle")
task(subagent_type="reviewer", description="...", prompt="brief + evidence bundle")
```
Tunggu KEDUA hasil. NEVER skip fan-out (kecuali TRIVIAL → reviewer optional).
See AGENTS.md Dispatch — table kanonik.
**Chunk guard:** Kalau salah satu return `[CHUNK_REQUIRED]` → tunggu re-chunk, JANGAN gunakan partial results dari agent lain. Re-dispatch keduanya dengan chunk yang lebih kecil.
**Trust sub-agents.** Gagal → re-dispatch dengan error detail, bukan ambil alih.
Sebelum synthesize, WAJIB validasi output sub-agent via `verify` custom tool (verify.ts → verify.py; reads JSON dari stdin, bukan CLI flags).
**Validation Rules:**
| Agent | Check | Fail Action |
|-------|-------|-------------|
| Researcher | file:line exists? | Re-dispatch: "file:X tidak ada. Cek ulang." |
| Researcher | [LEVEL] valid? | Re-dispatch: "Format: file:line — [P/W/E/O] desc" |
| Reviewer | [TAG] valid? | Re-dispatch: "Format: [BLOCKING/SHOULD/NICE/FYI] file:line — desc" |
| Reviewer | BLOCKING has file:line? | Re-dispatch: "BLOCKING WAJIB punya file:line" |
| Executor | Verify command ada? | Re-dispatch: "WAJIB jalankan verify command" |
| Executor | "should work" tidak ada? | Re-dispatch: "Jangan 'should work', jalankan command" |
Sebelum dispatch executor: cek researcher ada `file:line`, reviewer ada `[TAG]`+`file:line`. Kedua PASS → dispatch. Salah satu FAIL → re-dispatch agent yang fail.
**Verify gate PASS:** researcher ≥1 [LEVEL] finding dengan valid file:line. Reviewer ≥1 [TAG] finding dengan valid file:line. 0 finding dari salah satu → re-dispatch dengan "Scope too narrow, widen search."
**BLOCKING gate:** `[BLOCKING]` ditemukan → executor TIDAK mulai sampai di-resolve. Report ke Boss → tanya "Mau fix dulu atau skip?" → approve baru dispatch.
**Boss timeout (>3 exchange soal BLOCKING)** → default: dispatch executor SKIP area BLOCKING + flag "BLOCKING unresolved, skipped per timeout." Log untuk next session.
**Prioritas:** Timeout rule OVERRIDES audit completion. Setelah 3 exchange, executor dispatch jalan tanpa menunggu audit selesai.