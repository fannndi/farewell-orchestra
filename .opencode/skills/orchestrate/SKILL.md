---
name: orchestrate
description: Use after anti-gigo passes — decompose request, fan-out parallel, synthesize results, delegate to executor
---

# Orchestrate

Satu-satunya koordinator. Input sudah CLEAN dari anti-gigo. Sekarang dekomposisi dan delegasi.

## 1. Decompose

- Pecah request jadi **work packages independen**
- Tiap package: bisa dikerjakan tanpa menunggu hasil package lain
- Tidak boleh ada overlap antar package
- Tiap package muat dalam **5 baris brief**

## 2. Fan-Out

Dispatch parallel untuk tiap work package:

| Task type | Agent | Read-only? |
|-----------|-------|------------|
| Code investigation | researcher | ✅ |
| Architecture/security audit | reviewer | ✅ |
| Implementation | executor (tunggu sintesis) | ❌ |

Researcher + reviewer **selalu parallel** kalau keduanya dibutuhkan.

## 3. Evidence Bundle — Pre-Execution Context (dari better-harness QoderAI)

Sebelum fan-out, kumpulkan evidence dari 4 lane:

### Lane A: Memory (sub-project.md)
- Baca Memori Agent: apa task terakhir tiap agent?
- Baca Keputusan & Konteks: keputusan arsitektur yg relevan
- Output: `[MEMORY] agent terakhir kerja apa, keputusan apa yg diambil`

### Lane B: Lessons (LESSONS.md)
- Baca error pattern terbaru: ada insiden terkait task ini?
- Output: `[LESSONS] error pattern: [n] kejadian. Root cause: [x]`

### Lane C: Project State
- Cek file yg relevan dengan task: apa state terakhir?
- Grep file yg akan disentuh: ada perubahan pending? (git status)
- Output: `[STATE] file [n] bersih, [m] modified`

### Lane D: Agent Config
- Profile aktif: model apa yg dipake?
- Step budget: berapa sisa?
- Output: `[CONFIG] profile [name], step [used]/[total]`

### Synthesize Context
Gabungin 4 lane jadi 1 brief context buat researcher + reviewer:
```
CONTEXT: [MEMORY] + [LESSONS] + [STATE] + [CONFIG]
```

Ini memastikan researcher + reviewer punya konteks penuh sebelum mulai kerja.

## 4. Synthesize

Setelah researcher + reviewer selesai:
- Gabungkan findings → **max 3 bullet points**
- Conflict? → reviewer (security audit) > researcher (code facts). Tapi kalau researcher punya bukti konkret (file:line) yang membantah reviewer → catat sebagai "dispute" dan present ke Boss, jangan resolve sendiri.
- Siapkan executor brief dari hasil sintesis

## 5. Delegate — Structured Handoff Brief

Tiap brief ke sub-agent WAJIB 5 field ini, max 200 token total:

```
TASK: [1 kalimat — apa yg harus dihasilkan]
FILES: [path, path — file yg disentuh]
CONTEXT: [1-2 kalimat — kenapa, constraint spesifik]
TRIED: [opsional — apa yg udah dicoba & gagal, biar nggak diulang]
VERIFY: [command — cara test bahwa task selesai]
```

**Jangan:** jelaskan kenapa panjang, kasih konteks tambahan, spekulasi, "mungkin kamu perlu...", "coba lihat juga...". Brief = instruksi presisi, bukan mentoring.

## 6. Blast Radius — Impact Analysis (dari better-harness QoderAI)

Sebelum executor bekerja, analisis impact perubahan:

### a. Build Symbol Graph
- List file yg akan disentuh (dari brief executor)
- Cari import/require/include antar file via grep
- Bangun dependency graph: setiap file → files yg di-import

### b. Trace Impact Radius (BFS)
```
Queue = changed files
Visited = set()
Affected = []
While queue not empty AND affected < max:
  Current = queue.shift()
  For each file that IMPORTS current:
    If not visited → mark visited, add to queue, record depth + via
```
- Depth 0 = file yg langsung diubah
- Depth 1 = file yg import file yg diubah
- Depth 2 = file yg import Depth 1, dst
- Max depth: 3. Max affected symbols: 50.

### c. Score Impact
| Metric | Threshold | Score |
|--------|-----------|-------|
| Files changed | ≤3 = low, ≤8 = medium, &gt;8 = high | 0/10/20 |
| Impact radius (files affected) | ≤5 = low, ≤15 = medium, &gt;15 = high | 0/10/20 |
| Core code hit? | Security/auth/delivery file touched? | +25 |
| Test gaps? | Changed file tanpa test pair? | +5 per gap |

Score ≥45 → ⚠️ review recommended, tanya Boss sebelum lanjut.

### d. Core Rules Check
Pattern yg trigger high alert:
- `auth`, `login`, `credential`, `token`, `password`, `secret` di path
- `permission`, `middleware`, `guard`, `rbac` di path
- `database`, `migration`, `schema` di path
- `deploy`, `release`, `ci`, `cd` di path

### e. Test Gap Detection
Untuk setiap file yg diubah:
- Cari file test pair: `*.test.*`, `*.spec.*`, `__tests__/*`, `test_*`
- Kalau gak ada → catat sebagai test gap
- Kalau ada → baca test file, cek apakah import symbol yg diubah

### f. Report
```
Blast Radius: [SCORE]/100 — [LOW|MEDIUM|HIGH|CRITICAL]
Files: [n] changed → [n] affected
Core hits: [list] or none
Test gaps: [list] or none
```

Kalau score ≥45 atau ada core hit → informasikan ke Boss, minta konfirmasi sebelum lanjut.
Kalau score <45 dan aman → silent, lanjut eksekusi.

## 7. Post-Flight

Setelah executor selesai → verifikasi:
- Output sesuai acceptance criteria?
- Ada residual risk?
- Report ke Boss: 3 baris — what, result, residual risk.

## 8. Escalation

executor gagal 2x → STOP. Jangan dispatch executor lagi. Dispatch researcher dengan brief: "Deep debug [error]. Root cause, bukan symptom." Researcher invoke `forensic`.

## 9. Peer Debate Mode (high-stakes correctness)

Kalau Boss minta verifikasi ekstra atau task high-stakes (auth, keamanan, data integrity):

1. **Researcher** → analisis codebase, temukan fakta (evidence file:line)
2. **Reviewer** → critique findings researcher, tunjuk celah atau missing evidence
3. **Researcher (rebuttal)** → tanggapi critique dengan bukti tambahan atau akui kalau reviewer benar
4. **Synthesize** → orchestrator gabungkan final conclusion

**Token efficiency:** Saat researcher rebuttal, GUNAKAN `task_id` dari dispatch researcher pertama — resume subagent, bukan dispatch ulang dari nol. Researcher bawa full history sendiri, nggak perlu re-brief. Ini bypass 200-token cap karena context sudah ada dari sesi sebelumnya.

Trigger: Boss bilang `debat` atau `double check` atau `pastiin bener`. Atau orchestrator deteksi task nyangkut auth/security/data-loss.

Output format:
```
✅ AGREED: [poin yg researcher & reviewer sepakat]
⚠️ DEBAT: researcher klaim X (path:42), reviewer counter Y — [resolusi]
📋 FINAL: [kesimpulan setelah debate]
```

## Rules

- NEVER duplicate work. Once delegated, move on.
- Background tasks = FORBIDDEN. Semua foreground.
- Executor brief = MINIMAL. No fluff.
- Silent after dispatch? → WAIT. Jangan spam.

## 10. Loop Guard

Deteksi loop sebelum buang token:

| Sinyal loop | Action |
|-------------|--------|
| Agent + tool + intent sama terulang 3x berturut-turut | STOP. Jangan dispatch lagi. |
| Executor gagal dengan error identik 2x | Escalate ke researcher, jangan retry executor |
| Researcher balikin hasil yg sama 2x | Udah cukup — synthesize, jangan research lagi |
| Conversation muter di topik yg sama tanpa progress | Report ke Boss: "Stuck di [topik]. Perlu arahan." |

**Prinsip:** 3x sama = loop. Token lebih baik buat nanya Boss daripada muter di tempat.

## Agent Work Loop — Quality Gates (dari better-harness QoderAI)

Setiap task melewati 15 check di 5 dimensi. Gagal di satu check → STOP, report.

### 🎯 Task Understanding
| Check | Passing Criteria |
|-------|-----------------|
| Intent & Acceptance | Goal jelas, ada acceptance criteria (dari anti-gigo) |
| Relevant Context | File path, target, constraint disebut di brief |
| Scope Boundary | In/out scope eksplisit — "change only X, not Y" |

### 🎛 Controlled Execution
| Check | Passing Criteria |
|-------|-----------------|
| Reproducible Startup | Tool/skill dependencies available |
| Permission Boundary | File di dalam workspace. External? → Boss confirm |
| Constraint Guard | Tech stack, framework rules konsisten |

### ✅ Change Validation
| Check | Passing Criteria |
|-------|-----------------|
| Relevant Verification | Verification command ada di brief |
| Failure Diagnosis | Kalau error → diidentifikasi tipenya (typo/timeout/tool/structural) |
| Post-repair Revalidation | Setelah fix → re-run verification |

### 📦 Reliable Delivery
| Check | Passing Criteria |
|-------|-----------------|
| Delivery Acceptance | Output sesuai acceptance criteria |
| Residual Risk | Risk yg tersisa dilaporkan (bukan disembunyiin) |
| Rollback Path | Perubahan reversibel? (git revert? file backup?) |

### 📚 Learning Capture
| Check | Passing Criteria |
|-------|-----------------|
| Keputusan Log | Keputusan arsitektur dicatat di sub-project.md |
| Memory Update | Memori Agent diupdate (1 kalimat per agent) |
| Lesson Learned | Insiden non-trivial → logged ke LESSONS.md |

### Failure Protocol
- **1 check gagal** → STOP gate tsb. Report ke Boss: "Gate [nama] failed. Reason: ...". Jangan lanjut ke gate berikutnya.
- **Fix oleh executor** → setelah fix, re-verify gate yg gagal.
- **3x gagal di gate yg sama** → eskalasi ke Boss: butuh intervensi manual.
