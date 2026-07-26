---
description: Scaffold documentation for a new/existing sub-project — 10 docs + sub-project.md — via bootstrap-project skill.
agent: orchestrator
---

Boss mau mulai/lanjutin sub-project di cwd sekarang.

1. Invoke `anti-gigo` — validasi: nama project, satu-liner, tech stack (tanya kalau Boss belum sebut).
2. Cek apakah `sub-project.md` udah ada di root cwd:
   - Belum ada → invoke `bootstrap-project` skill, mode generate baru.
   - Udah ada → invoke `bootstrap-project` skill, mode update (baca dulu, tanya bagian mana yang diubah).
3. Delegasikan penulisan ke executor: target `docs/` di root project aktif (cwd), BUKAN di folder farewell-orchestra.
4. Report: "10/10 docs [dibuat/diupdate] di {project}/docs/. sub-project.md siap." — 3 baris max.
