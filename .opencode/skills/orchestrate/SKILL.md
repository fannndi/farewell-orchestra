---
name: orchestrate
description: Use after prepare passes — decompose, fan-out parallel, synthesize, brief executor.
---

# Orchestrate

Input sudah CLEAN. Flow:

```
Decompose → Evidence Bundle → Ping → Fan-Out → Synthesize → Verify Gate → Brief Executor → Post-Flight
```

## 1. Decompose

Pecah jadi work packages independen. Tiap package ≤5 baris brief.

## 2. Evidence Bundle

Kumpulin context buat researcher + reviewer:

| Lane | Sumber | Output |
|------|--------|--------|
| Memory | sub-project.md | agent terakhir kerja apa |
| Lessons | Farewell-Knowlage/Lessons.md | error pattern: n kejadian |
| State | git status | file modified, bersih |
| Config | opencode.jsonc | profile name |

**REDACTION:** Hapus secret, API keys, token, path absolut sebelum dispatch.

## 3. Ping Guard

Sebelum dispatch real work:

```
task(subagent_type=<agent>, prompt='Reply with exactly: READY')
```

- Non-empty response → alive. Proceed.
- Empty/error → DEAD. Researcher/reviewer: SKIP. Executor: ESCALATE ke Boss.

## 4. Fan-Out

Dispatch researcher + reviewer **PARALLEL**:

```python
task(subagent_type="researcher", description="...", prompt="brief + evidence bundle")
task(subagent_type="reviewer", description="...", prompt="brief + evidence bundle")
```

Tunggu KEDUA hasil. NEVER skip fan-out (kecuali TRIVIAL → reviewer optional).

**Chunk guard:** Kalau salah satu return `[CHUNK_REQUIRED]` → tunggu re-chunk, JANGAN gunakan partial results dari agent lain. Re-dispatch keduanya dengan chunk yang lebih kecil.

**Trust sub-agents.** Gagal → re-dispatch dengan error detail, bukan ambil alih.

## 5. Synthesize

Gabung hasil researcher + reviewer → max 3 bullet.

**Conflict Resolution:**

| Conflict | Winner | Alasan |
|----------|--------|--------|
| Researcher "aman" vs Reviewer "BLOCKING" | Reviewer | STRIDE otoritatif di security |
| Researcher fakta vs Reviewer asumsi | Researcher | dia yang trace source |
| Kedua contradict soal fakta | Re-verify | suruh researcher re-check |
| Reviewer flag konvensi, researcher diam | Reviewer | silence ≠ disagreement |

Researcher clean + Reviewer clean = VALID. Lanjut tanpa reject.

## 6. Verify Gate

Sebelum dispatch executor:
1. Cek output researcher ada `file:line`
2. Cek output reviewer ada `[TAG]` + `file:line`
3. Kedua PASS → dispatch executor
4. Salah satu FAIL → re-dispatch agent yang fail

**BLOCKING gate:** Kalau reviewer menemukan `[BLOCKING]` → executor TIDAK BOLEH mulai sampai BLOCKING di-resolve. Orchestrator:
1. Report BLOCKING ke Boss
2. Tanya: "BLOCKING ditemukan: [deskripsi]. Mau fix dulu atau skip?"
3. Boss approve → baru dispatch executor

## 7. Brief Executor

```
TASK: [1 kalimat — apa yang harus dihasilkan]
FILES: [path, path — file yang disentuh]
CONTEXT: [1-2 kalimat — kenapa, constraint]
TRIED: [opsional — apa yang sudah gagal]
VERIFY: [command — cara test bahwa task selesai]
```

**Banned phrasing:** "consider", "mungkin", "sebaiknya", "bisa jadi", "improve/optimize" tanpa target, "refactor as needed", "clean up".

Semua fork/decision WAJIB CLOSED di orchestrator. Executor cukup nulis, tidak boleh mikir.

## 8. Blast Radius

Grep import chain dari file yang disentuh. Core files (auth/security/db/deploy/middleware) → tanya Boss. Selainnya silent lanjut.

**Cascade Detection** — kalau update di satu service/module:
1. Trace: siapa yang depend on ini?
2. Kalau dependency chain > 2 hop → flag: "Cascade risk: [A] -> [B] -> [C]"
3. Kalau cascade melibatkan DB/data → BLOCKING: "Cascade ke data layer. Backup dulu?"

**Dependency Order Validation** — kalau chunk multiple modules:
1. Map dependency: A depends on B depends on C
2. Urutan implement: C -> B -> A (bottom-up)
3. Kalau urutan salah → flag: "Urutan salah: [C] harus sebelum [A]"

## 9. Post-Flight

Verifikasi acceptance criteria. Report 3 baris:

```
[what changed] · [verification result] · [residual risk]
```

## 10. Session Memory — WAJIB setelah task selesai

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

**Kenapa:** LLM lupa context antar session. Memori ini bikin LLM bisa lanjut tanpa mulai dari nol.

**Update trigger:**
- Task selesai → update executor baris
- Keputusan arsitektur → update Keputusan & Konteks
- Temuan penting → update agent yang relevan

**Memory check di awal session:**
1. Baca sub-project.md Memori Agent
2. Kalau kosong → lapor: "Memory kosong. Mulai dari nol?"
3. Kalau outdated (>7 hari) → lapor: "Memory outdated. Re-verify context?"
4. Kalau ada → gunakan sebagai starting point

**Code change detection:**
Kalau resume task dari session lalu:
1. `git diff` dari last memory update
2. Ada perubahan → flag: "Code berubah sejak session lalu: [files]. Re-verify?"
3. Tidak ada perubahan → lanjut normal

## Failure Recovery

Sub-agent return kosong/garbled:
1. **Retry** dengan prompt lebih detail + ground truth struktur project
2. Masih gagal → **escalate ke Boss**

**All agents dead:** Kalau SEMUA agent (researcher + reviewer + executor) gagal setelah retry → escalate ke Boss: "Semua agent tidak merespons. Perlu restart atau manual intervention."

Max 2 attempt total. Jangan loop.

## Loop Guard

| Sinyal | Action |
|--------|--------|
| Agent+tool+intent sama 3x | STOP, ganti approach |
| Executor gagal error identik 2x | Escalate ke researcher |
| Executor gagal error **mirip** 2x (>80% similarity) | Escalate ke researcher |
| Conversation muter tanpa progress | Report: "Stuck di [topik]" |

**Error similarity:** Kalau error message berbeda tapi root cause mirip (misal: "cannot find module X" vs "module X not found") → treat sebagai error identik.

## Peer Debate (trigger: high-stakes / "double check")

1. Researcher → analisis + evidence
2. Reviewer → critique findings
3. Researcher rebuttal → bukti tambahan
4. Orchestrator → final conclusion

## Proactive

- Task selesai → WAJIB usul next action ke Boss
- Risk/blocker → flag ke Boss sebelum ditanya
- Lihat risk di luar scope → usul investigasi
