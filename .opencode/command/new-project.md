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
4. Setelah docs di-generate: auto-register project ke .opencode/project-registry.md (nama, path relatif dari ~/projects, tech stack, fase 'onboarding', status 'aktif', last active hari ini). Kalau sudah ada entry → update fase/status.
5. Report: "10/10 docs [dibuat/diupdate] di {project}/docs/. sub-project.md siap. Terdaftar di project-registry." — 3 baris max.
