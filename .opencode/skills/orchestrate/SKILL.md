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

## 9. Post-Flight

Verifikasi acceptance criteria. Report 3 baris:

```
[what changed] · [verification result] · [residual risk]
```

## Failure Recovery

Sub-agent return kosong/garbled:
1. **Retry** dengan prompt lebih detail + ground truth struktur project
2. Masih gagal → **escalate ke Boss**

Max 2 attempt total. Jangan loop.

## Loop Guard

| Sinyal | Action |
|--------|--------|
| Agent+tool+intent sama 3x | STOP, ganti approach |
| Executor gagal error identik 2x | Escalate ke researcher |
| Conversation muter tanpa progress | Report: "Stuck di [topik]" |

## Peer Debate (trigger: high-stakes / "double check")

1. Researcher → analisis + evidence
2. Reviewer → critique findings
3. Researcher rebuttal → bukti tambahan
4. Orchestrator → final conclusion

## Proactive

- Task selesai → WAJIB usul next action ke Boss
- Risk/blocker → flag ke Boss sebelum ditanya
- Lihat risk di luar scope → usul investigasi
