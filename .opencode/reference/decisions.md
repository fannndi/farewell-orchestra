# Decision Trees — Quick Reference

## ADR-001: Jangan merge skill/hook/tool
Status: Accepted (2026-08-01)
Konteks: Kritik "over-engineering" — 9 skill/3 hook/4 tool terasa berlebihan.
Keputusan: TIDAK merge. Reviewer membuktikan tiap komponen punya guardrail unik (phase separation, domain separation, temporal separation, wrapper/backend pair).
Konsekuensi: Maintenance tetap per-komponen, tapi kompleksitas justified. Prune hanya untuk duplikat NYATA, bukan komponen dengan fungsi unik.

## ADR-002: Chunking PROACTIVE bertahap (sequential, presisi-first)
Status: Accepted (2026-08-01)
Konteks: Free model (researcher/reviewer) sering terhenti ([CHUNK_REQUIRED] / return kosong) karena task kegedean. Mekanisme lama reaktif — nunggu protes.
Keputusan: Orchestrator WAJIB pre-chunk check sebelum fan-out (hitung pertanyaan/file/format). Unit ideal 1-2 file, 1 pertanyaan, 1 format, ≤8k token. Max 3 chunk/task. Dispatch SEQUENTIAL satu per satu dengan CONTEXT_SUMMARY antar chunk + CHUNK_DEPENDENCY_MAP + rollback max 1x. Verify per chunk kalau ada dependency chain.
Konsekuensi: Waktu eksekusi lebih lama (tradeoff diterima Boss — presisi di atas kecepatan). Overhead chunk di-log ke cost-log.json. CHUNK_REQUIRED dari free model = trigger pre-chunk ulang, bukan gagal.

## Task: Dispatch or Chunk?
- <=3 pertanyaan → dispatch langsung
- >3 pertanyaan → chunk 2-4 dispatch kecil
- >5 file diminta → chunk per 2-3 file
- Agent sebelumnya return KOSONG → chunk ulang lebih kecil

## Task: Which Agent?
- Baca/analisis kode → researcher
- Security/convention audit → reviewer
- External claim verification → researcher + reviewer PARALLEL
- Nulis/edit kode → executor
- Sinergi 4-agent: orchestrator decompose → researcher+reviewer parallel → executor

## Task: Failure Recovery
- Output kosong 1x → resume task_id: "Lanjutkan. Output kamu kosong."
- Output kosong 2x → fresh dispatch dengan lebih detail
- Output kosong 3x → eskalasi ke Boss
- Executor gagal 2x → dispatch researcher deep debug

## Task: Verify or Skip?
- Setiap researcher output → @verify stage:research
- Setiap reviewer output → @verify stage:review
- Sebelum executor dispatch → KEDUA verify harus PASS
- Verify FAIL → re-dispatch agent yg fail
- Verify PARTIAL → orchestrator putuskan

## Task: Emergency or Dispatch?
- Boss explicit "fix NOW" + production down → executor langsung, skip fan-out
- Typo 1 baris → TETAP executor (via dispatch, bukan orchestrator direct)
- External audit finding → TIDAK PERNAH emergency, wajib fan-out
- sub-project.md update 1 baris → orchestrator direct (allowed by permission)
