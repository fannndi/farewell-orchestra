# Decision Trees — Quick Reference

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
