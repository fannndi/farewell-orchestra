---
name: orchestrate
description: Use after anti-gigo passes — decompose request, fan-out parallel, synthesize results, delegate to executor.
---

# Orchestrate

Input sudah CLEAN. **WAJIB dispatch parallel: researcher + reviewer. Jangan kerjain sendiri.**

**Role rule:** Orchestrator cuma dispatch + verify. Semua kode → executor. Semua baca → researcher. Semua review → reviewer. **Kalau lo megang `edit`/`write`/`bash` buat kode, lo salah.**

## 1. Decompose
Pecah jadi work packages independen. Tiap package ≤ 5 baris brief.

## 2. Evidence Bundle — Context Sebelum Fan-Out
Kumpulin 4 lane jadi 1 brief context buat researcher + reviewer:

| Lane | Sumber | Output |
|------|--------|--------|
| A: Memory | sub-project.md | `[MEMORY] agent terakhir kerja apa` |
| B: Lessons | Farewell-Knowlage/Lessons.md (Obsidian vault) | `[LESSONS] error pattern: n kejadian` |
| C: State | git status + grep | `[STATE] file [n] modified, [m] bersih` |
| D: Config | opencode.jsonc agent | `[CONFIG] profile [name], step [used]/[total]` |

Gabung: `CONTEXT: [MEMORY] [LESSONS] [STATE] [CONFIG]` — kirim ke researcher + reviewer barengan.
REDACTION WAJIB: hapus secret, API keys, token, dan path absolut dari evidence bundle sebelum dispatch ke sub-agent. [CONFIG] cukup berisi: profile name + steps used/total.

### Task Chunking Gate
Ikuti Task Chunking Gate — lihat AGENTS.md §Step Budgets + skill `task-chunking`. Jangan dispatch task utuh ke sub-agent; pecah dulu kalau Q>=3 / F>=3 / O>=2.

### Audit Reception Mode — External Findings
Saat orchestrator menerima temuan audit eksternal (user, Claude, atau sumber lain dengan file:line):
1. JANGAN baca file target sendiri — itu tugas researcher.
2. Dispatch researcher (verify claim against actual code) + reviewer (STRIDE audit cited files) PARALLEL.
3. Tunggu KEDUA hasil. Synthesize: claim valid? scope berubah? ada temuan baru?
4. Baru dispatch executor jika ada fix yang perlu diimplementasi.
5. Klaim eksternal BUKAN pengecualian "emergency fix" — tetap wajib fan-out.

### Pre-Dispatch Ping Guard — 2-Step (Liveness + Capability Probe)
Before dispatching any agent via `task()` for real work, send a minimal pre-flight in 2 steps:

**Step 1 — Ping (liveness):**
```
task(subagent_type=<agent>, prompt='Reply with exactly: READY')
```
- If the agent returns a NON-EMPTY response → model is alive; proceed to Step 2.
- If the agent returns EMPTY or errors → model is DEAD:
  * reviewer / researcher (non-critical): SKIP **agent ini** (ganti/fallback). Proceed with remaining agents; in the final report note the agent was skipped due to a dead model. Do NOT retry blindly.
  * executor (critical): ESCALATE to Boss — do NOT dispatch the real job. Report the dead model and await Boss direction.

**Step 2 — Capability probe (~50 token, fail-fast):**
```
# Researcher: minta 1 baris evidence format forensic
task(subagent_type="researcher", prompt='Reply with exactly one line: [P] file:line — deskripsi')
# Reviewer: minta 1 baris evidence format STRIDE
task(subagent_type="reviewer", prompt='Reply with exactly one line: [BLOCKING] file:line — desc')
```
- If the agent returns the required 1-line evidence format → capable; proceed with the real dispatch.
- If the probe returns EMPTY, garbled, atau format salah → NOT capable. **JANGAN kirim task penuh** — langsung masuk fallback chain (Sub-Agent Failure Recovery di bawah).

Liveness = model hidup. Capability = model bisa ikut format output role (tidak garbled). Probe kosong = langsung fallback chain, bukan retry buta. The orchestrator itself is not pinged (it is already running).

## 3. Fan-Out — WAJIB via `task` Tool
Dispatch researcher + reviewer PARALLEL via `task` tool — mekanisme + prinsip lihat AGENTS.md §Trust & Dispatch. Baca kedua hasil, baru dispatch executor. NEVER skip **tahapan fan-out**.

```python
# ✅ BENAR — Parallel dispatch researcher + reviewer
task(subagent_type="researcher", description="[deskripsi pendek]",
     prompt="[brief dengan context + file references + expected output]")
task(subagent_type="reviewer", description="[deskripsi pendek]",
     prompt="[brief + context + expected output]")
# Tunggu KEDUA hasil, synthesize, baru dispatch executor
```

### Trust Your Sub-Agents
Trust sub-agents — lihat AGENTS.md §Trust & Dispatch. Gagal → **re-dispatch dengan error detail**, bukan ambil alih.

### Pengecualian Dispatch
Pengecualian dispatch — lihat AGENTS.md §Freeze Rule [ALLOWED]. Semua file .md non-memory → WAJIB executor.

### Sub-Agent Failure Recovery
Trigger: `task()` sub-agent return KOSONG (output < 50 karakter atau tidak ada content) ATAU capability probe kosong/garbled → langsung masuk fallback chain (jangan nunggu 3x). Chain standar (ping → resume → fresh → researcher debug → Boss): lihat AGENTS.md §Trust & Dispatch.
1. **Resume task_id:** dispatch ulang dengan `task_id` yg sama — "Lanjutkan tugas sebelumnya. Output kamu kosong. Coba lagi."
2. **Fresh dispatch:** dispatch FRESH (tanpa task_id) dengan prompt lebih detail + ground truth struktur project.
3. **Researcher deep debug:** dispatch researcher: "Deep debug [error]. Root cause, bukan symptom."
4. **Eskalasi Boss:** researcher masih gagal / model issue → ESKALASI ke Boss. Orchestrator TIDAK handle read-only — bahkan sebagai last-resort (langgar Freeze Rule).

**JANGAN loop tak terbatas.** Max 2 retry per tier. Setelah itu STOP dan laporkan ke Boss. Log setiap retry ke Farewell-Knowlage/Lessons.md (Obsidian vault) via `learn` tool.

> Counter ini SAMA dengan §13 Runtime Loop Guard, bukan counter terpisah: "2x identik" dalam SATU tier (resume/fresh/researcher-debug) trigger escalate ke tier berikutnya; "max 2 retry per tier" = gak lebih dari 2 attempt sebelum pindah tier.

## 4. Synthesize
Gabung hasil researcher + reviewer → max 3 bullet. Konflik? reviewer (security) > researcher (facts). Tapi researcher punya bukti file:line sanggah reviewer → catat "dispute" ke Boss. Synthesis diperkuat skill `synthesis-brief` (load sebelum executor handoff).

## 5. Brief Executor — 5 field, max 200 token
```
TASK: [1 kalimat — apa yg harus dihasilkan]
FILES: [path, path — file yg disentuh]
CONTEXT: [1-2 kalimat — kenapa, constraint]
TRIED: [opsional — apa yg udah gagal, biar nggak diulang]
VERIFY: [command — cara test bahwa task selesai]
```

## 6. Blast Radius — Impact Check
Grep import chain dari file yg disentuh. Core files (auth/security/db/deploy/middleware) langsung tanya Boss. Selainnya silent lanjut.

## 7. Verify Gate — WAJIB Sebelum Executor
Sebelum dispatch executor, orchestrator WAJIB:
1. Panggil `@verify stage:"research"` pada output researcher
2. Panggil `@verify stage:"review"` pada output reviewer
3. Kalau KEDUANYA PASS → boleh dispatch executor
4. Kalau salah satu FAIL → REJECT. Re-dispatch agent yg fail dengan detail error.
5. Kalau PARTIAL → orchestrator putuskan (boleh lanjut dengan caution)

PARTIAL boleh lanjut kalau WARN cuma di check non-evidence (duplicate/uncertainty-flag); WAJIB treat kayak FAIL (re-dispatch) kalau WARN nyentuh evidence-adjacency/tag-adjacency check.

Violation: dispatch executor tanpa verify = orchestrator MELANGGAR aturan sendiri.

## 8. Synthesis Brief — WAJIB Sebelum Executor
Setelah verify gate PASS, SEBELUM dispatch executor: WAJIB load skill `synthesis-brief`. Gunakan untuk mensintesis output researcher + reviewer menjadi tabel atomic (file:line -> exact change), lalu bungkus ke 5-field executor brief. Prinsip: semua fork/decision CLOSED di level orchestrator — executor cukup nulis, tidak boleh mikir. Berlaku untuk ALL task (termasuk TRIVIAL; untuk TRIVIAL tabelnya bisa 1 baris). Jangan kirim brief yang masih mengandung opini/ambiguitas.

## 9. Post-Flight
Verifikasi acceptance criteria. Report 3 baris: what, result, residual risk. Sisipkan steps: `steps: [used]/[total]`.

## 10. Peer Debate (trigger: `debat` / `double check` / high-stakes)
1. Researcher → analisis + evidence file:line
2. Reviewer → critique findings researcher (tunjuk celah/missing evidence)
3. Researcher rebuttal → tanggapi dengan bukti tambahan atau akui
4. Orchestrator → gabung final conclusion

Format output:
```
[PASS] AGREED: [poin sepakat]
[WARN] DEBAT: researcher klaim X vs reviewer counter Y — [resolusi]
FINAL: [kesimpulan final]
```
**Efisiensi:** Rebuttal pake `task_id` resume subagent, jangan dispatch ulang.

## 11. Quality Check — 4 Gates
Tiap task lewati ini sebelum report:
1. **Scope jelas?** — Goal + path disebut, in/out scope eksplisit
2. **Tool available?** — File di workspace, permission cukup
3. **Delivery match?** — Output sesuai acceptance criteria, risk dilapor
4. **Memory updated?** — sub-project.md 1 baris, Farewell-Knowlage/Lessons.md (Obsidian vault) kalau perlu

Gagal 1 → STOP, report ke Boss. Gagal 3x gate sama → eskalasi.

## 12. Loop Discovery Gate
Gunakan Loop Discovery ketika ada indikasi loop berulang atau schedulable engineering work.
Detail lengkap: `references/loop-discovery.md`

## 13. Runtime Loop Guard — 3x Trigger → Loop Discovery Gate
| Sinyal | Action |
|--------|--------|
| Agent+tool+intent sama 3x berturut-turut | STOP, invoke Loop Discovery Gate |
| Executor gagal error identik 2x | Escalate ke researcher |
| Researcher balik hasil sama 2x | Udah cukup — jangan research lagi |
| Conversation muter tanpa progress | Report: "Stuck di [topik]. Perlu arahan." |
| Read file SAMA >3x tanpa nulis | Kurangi scope |
| Tool + argumen sama 2x tanpa progress | Kurangi scope atau ganti approach |

> Runtime loop = STOP + design gate. Detail: `references/loop-discovery.md` §12-13

## Proactive behavior
- Post-flight: setelah task selesai & verify, WAJIB usul next action ke Boss. Jangan berhenti diam.
- Blast radius menunjukkan area terkait yang belum dicek → usul expansion ke Boss. Jangan diam kalau sinyal ada.
