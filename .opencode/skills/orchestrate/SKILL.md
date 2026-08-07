---
name: orchestrate
description: Use after prepare passes — decompose, fan-out parallel, synthesize, brief executor.
activation: After prepare returns PASS
trigger: prepare PASS → load orchestrate
---
# Orchestrate
Input sudah CLEAN. Flow:
```
Decompose → Evidence Bundle → Ping → Fan-Out → Synthesize → Validate & Verify → Brief Executor → Post-Flight
```

## Fallback Mode (untuk semua LLM)
Kalau LLM tidak bisa handle complex instructions: Decompose 2-3 bagian → Fan-Out researcher+reviewer → Synthesize max 3 bullet → Brief executor (TASK/FILES/VERIFY) → Report `<what> · <result> · <risk>`
Contoh: `Auth module added · pytest pass · residual: rate limiting`
Skip evidence bundle, ping guard, dll — cukup flow dasar.

## 1. Decompose
Pecah jadi work packages independen. Tiap package ≤5 baris brief.

**Contoh work package:** "Fix auth bypass di login.js" = 1 package. "Refactor auth module (login.js, token.js, middleware.js)" = 1 package (satu domain). "Fix auth bug + tambah logging di api.js" = 2 packages (domain beda).

## 2. Interrupt Handler
| Event | Action |
|-------|--------|
| Researcher: BLOCKING found | Escalate ke Boss langsung |
| Researcher: CRITICAL finding | Escalate ke Boss langsung |
| Reviewer: BLOCKING found | Escalate ke Boss langsung |
| Either: ABORT error | Stop semua, escalate ke Boss |

**Priority:** ABORT stop semua > BLOCKING/CRITICAL escalate langsung > normal tunggu keduanya selesai.

## 3. Evidence Bundle
| Lane | Sumber | Output |
|------|--------|--------|
| Memory | sub-project.md | agent terakhir kerja apa |
| Lessons | Farewell-Knowlage/Lessons.md (external Obsidian vault) | error pattern: n kejadian |
| State | git status | file modified, bersih |
| Config | opencode.jsonc | profile name |

**REDACTION:** Hapus secret, API keys, token, path absolut sebelum dispatch.

## 4. Ping Guard
```
task(subagent_type=<agent>, prompt='Reply with exactly: READY')
```
- Non-empty response → alive. Proceed.
- Empty/error → DEAD. Researcher/reviewer: SKIP. Executor: ESCALATE ke Boss.

**SKIP researcher** → reviewer-only audit + flag "Researcher offline. Reviewer-only." **SKIP reviewer** → researcher-only + flag. **SKIP both** → ESCALATE. **Executor DEAD** → ESCALATE langsung.

**Valid ping response:** mengandung "READY" (case-insensitive). Selain itu → retry sekali, lalu DEAD.

## 5. Fan-Out
Dispatch researcher + reviewer **PARALLEL**:
```python
task(subagent_type="researcher", description="...", prompt="brief + evidence bundle")
task(subagent_type="reviewer", description="...", prompt="brief + evidence bundle")
```
Tunggu KEDUA hasil. NEVER skip fan-out (kecuali TRIVIAL → reviewer optional).
**Explicit Fan-Out Enforcement (WAJIB untuk LLM):**

| Size | Researcher | Reviewer | Executor |
|------|------------|----------|----------|
| TRIVIAL | OPTIONAL | OPTIONAL | LANGSUNG |
| SMALL | WAJIB | OPTIONAL | SETELAH research |
| MEDIUM | WAJIB | WAJIB | SETELAH keduanya |
| LARGE | WAJIB | WAJIB | SETELAH keduanya |

**Chunk guard:** Kalau salah satu return `[CHUNK_REQUIRED]` → tunggu re-chunk, JANGAN gunakan partial results dari agent lain. Re-dispatch keduanya dengan chunk yang lebih kecil.
**Trust sub-agents.** Gagal → re-dispatch dengan error detail, bukan ambil alih.

## 6. Validate & Verify
### Programmatic Validation
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

### Verify Gate
Sebelum dispatch executor: cek researcher ada `file:line`, reviewer ada `[TAG]`+`file:line`. Kedua PASS → dispatch. Salah satu FAIL → re-dispatch agent yang fail.

**Verify gate PASS:** researcher ≥1 [LEVEL] finding dengan valid file:line. Reviewer ≥1 [TAG] finding dengan valid file:line. 0 finding dari salah satu → re-dispatch dengan "Scope too narrow, widen search."
**BLOCKING gate:** `[BLOCKING]` ditemukan → executor TIDAK mulai sampai di-resolve. Report ke Boss → tanya "Mau fix dulu atau skip?" → approve baru dispatch.

**Boss timeout (>3 exchange soal BLOCKING)** → default: dispatch executor SKIP area BLOCKING + flag "BLOCKING unresolved, skipped per timeout." Log untuk next session.

**Prioritas:** Timeout rule OVERRIDES audit completion. Setelah 3 exchange, executor dispatch jalan tanpa menunggu audit selesai.

## 7. Brief Executor
```
TASK: [1 kalimat — apa yang harus dihasilkan]
FILES: [path, path — file yang disentuh]
CONTEXT: [1-2 kalimat — kenapa, constraint]
TRIED: [opsional — apa yang sudah gagal]
VERIFY: [command — cara test bahwa task selesai]
CONSTRAINTS: [opsional — jangan ubah X, tetap Y]
```
**Cross-project addition:**
```
PROJECT_PATH: [absolute path ke project]
PROJECT_TYPE: [Flutter/Node/Python/Rust/Go]
```
**Banned phrasing:** "consider", "mungkin", "sebaiknya", "bisa jadi", "improve/optimize" tanpa target, "refactor as needed", "clean up".
Semua fork/decision WAJIB CLOSED di orchestrator. Executor cukup nulis, tidak boleh mikir.

## 8. Blast Radius
Grep import chain dari file yang disentuh. Core files (auth/security/db/deploy/middleware) → tanya Boss. Selainnya silent lanjut.
**Cascade Detection** — kalau update di satu service/module:
1. Trace siapa yang depend
2. Chain > 2 hop → flag: "Cascade risk: [A] -> [B] -> [C]"
3. Melibatkan DB/data → BLOCKING: "Cascade ke data layer. Backup dulu?"
**Dependency Order Validation** — kalau chunk multiple modules:
1. Map dependency: A → B → C
2. Urutan implement bottom-up: C -> B -> A
3. Salah urutan → flag: "Urutan salah: [C] harus sebelum [A]"

## 9. Post-Flight
Verifikasi acceptance criteria. Report 3 baris:
```
[what changed] · [verification result] · [residual risk]
```

**Template report:**
```
[CHANGE] <apa yang berubah — max 15 kata>
[VERIFY] <command + result — 1 baris>
[RISK] <residual risk ATAU "none">
```

## 10. Session Memory
Update `sub-project.md` di project target:
```markdown
## Memori Agent

| Agent | Konteks | File kunci |
|-------|---------|------------|
| orchestrator | [1 baris: apa yang terakhir diputuskan] | — |
| researcher | [1 baris: apa yang terakhir di-investigasi] | [file kunci] |
| reviewer | [1 baris: apa yang terakhir di-audit] | [file kunci] |
| executor | [1 baris: apa yang terakhir di-implement] | [file kunci] |

## Keputusan & Konteks
- [max 5 bullets: keputusan arsitektur, task yg ditunda, temuan penting]
```
**Kenapa:** LLM lupa context antar session; memori ini bikin LLM lanjut tanpa mulai dari nol.
**Update trigger:**
- Task selesai → update executor baris
- Keputusan arsitektur → update Keputusan & Konteks
- Temuan penting → update agent yang relevan
**Awal session:** baca Memori Agent. Kosong → "Memory kosong. Mulai dari nol?". Outdated (>7 hari) → "Memory outdated. Re-verify context?". Ada → gunakan sebagai starting point.
**Resume session:** `git diff` dari last memory update. Ada perubahan → "Code berubah sejak session lalu: [files]. Re-verify?". Tidak → lanjut normal.

## Failure Recovery
Sub-agent return kosong/garbled:
1. **Retry** dengan prompt lebih detail + ground truth struktur project
2. Masih gagal → **escalate ke Boss**
**All agents dead:** researcher + reviewer + executor gagal setelah retry → escalate: "Semua agent tidak merespons. Perlu restart atau manual intervention."
Max 2 attempt total. Jangan loop.
See AGENTS.md Error Recovery for detailed patterns (permission denied, timeout, format violation).

## Loop Guard
| Sinyal | Action |
|--------|--------|
| Agent+tool+intent sama 3x | STOP, ganti approach |
| Executor gagal error identik 2x | Escalate ke researcher |
| Executor gagal error **mirip** 2x (>80% similarity) | Escalate ke researcher |
| Conversation muter tanpa progress | Report: "Stuck di [topik]" |

**Error similarity:** Error beda tapi root cause mirip (misal: "cannot find module X" vs "module X not found") → treat sebagai error identik.

## Peer Debate (trigger: high-stakes / "double check")
Researcher analisis → reviewer critique → researcher rebuttal → orchestrator conclusion.

## Proactive
- Task selesai → WAJIB usul next action ke Boss
- Risk/blocker → flag ke Boss sebelum ditanya
- Lihat risk di luar scope → usul investigasi

## Cross-Project Orchestration
See `.opencode/skills/prepare/SKILL.md` §0 + AGENTS.md: permission pre-check, orchestrator direct scan, detect type → check docs → normal flow.

## Task Size Classification
See AGENTS.md Task Size Classification.

## Agent Communication Protocol

Standard komunikasi antar agents.

### Message Format: Orchestrator → Sub-agent

```json
{
  "task": "apa yang harus dilakukan",
  "files": ["file1.ts", "file2.ts"],
  "context": "kenapa, constraint",
  "format": "expected output format",
  "verify": "how to verify"
}
```

### Message Format: Sub-agent → Orchestrator

```json
{
  "status": "DONE/BLOCKED/FAILED",
  "output": "hasil kerja",
  "files_changed": ["file1.ts"],
  "issues": ["issue1", "issue2"],
  "next": "apa yang perlu dilakukan selanjutnya"
}
```

### Error Response

```json
{
  "status": "FAILED",
  "error": "apa yang salah",
  "type": "RETRY/FALLBACK/ESCALATE/SKIP/ABORT",
  "suggestion": "bagaimana cara fix"
}
```

### Interrupt Protocol (BLOCKING)

```json
{
  "interrupt": true,
  "type": "BLOCKING",
  "message": "apa yang salah",
  "file": "file:line",
  "action": "apa yang harus dilakukan"
}
```

### Context Passing

```json
{
  "context": {
    "session_state": "apa yang sedang dikerjakan",
    "decisions": ["decision1", "decision2"],
    "blockers": ["blocker1"],
    "files_modified": ["file1.ts"]
  }
}
```

### Communication Rules

1. **Structured** — gunakan format yang sudah didefinisikan
2. **Concise** — jangan basa-basi
3. **Actionable** — selalu ada next step
4. **Evidence-based** — sertakan file:line untuk claims
5. **Interrupt-aware** — BLOCKING = escalate langsung
6. **Max response (count-based, bukan token — LLM tidak punya token counter):** researcher ≤15 findings, reviewer ≤20 findings, executor ≤500 words. Total per response ≤50 findings.
