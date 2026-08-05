---
description: Scaffold documentation for a new/existing sub-project.
agent: orchestrator
---

Boss mau mulai/lanjutin sub-project di cwd sekarang.

1. Invoke `prepare` — validasi: nama project, satu-liner, tech stack
2. Cek `sub-project.md` di root cwd:
   - Belum ada → invoke `bootstrap-project` skill, mode generate baru
   - Udah ada → invoke `bootstrap-project` skill, mode update
3. Delegasikan penulisan ke executor: target `docs/` di root project aktif
4. Report: "10/10 docs [dibuat/diupdate]. sub-project.md siap."
