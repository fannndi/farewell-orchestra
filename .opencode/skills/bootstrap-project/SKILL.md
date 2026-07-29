---
name: bootstrap-project
description: Generate 10 interconnected project docs (PRD, Architecture, Design, Schema, Rules, API_Contract, Tasks, Tests, Context, debug) from a project idea, plus sub-project.md anchor. Use when Boss starts a new sub-project, says "bikin dokumentasi project baru", "scaffold docs", or runs /new-project.
---

# Bootstrap Project Docs

Dipakai orchestrator SEBELUM kode ditulis. Prasyarat: udah lolos `anti-gigo` (Goal/Scope/Acceptance jelas). Kalau info project belum lengkap (nama, satu-liner, tech stack), tanya dulu — jangan asumsi stack yang nggak disebut Boss.

## Konsistensi Wajib
10 file ini saling rujuk, harus zero-kontradiksi:
- Nama variabel/tabel di `Schema.md` = nama field di `API_Contract.md`
- Tech stack di `Architecture.md` = konvensi di `Rules.md`
- Fitur Core di `PRD.md` = task di `Tasks.md` = acceptance criteria di `Tests.md`

## 10 File & Isi Wajib

1. **PRD.md** — latar belakang, definisi MVP, Core Features (wajib ada), Out of Scope, target user, user flow.
2. **Architecture.md** — tech stack (FE/BE/DB), directory tree, alur data (Client→API→Service→DB), architecture decisions + alasan.
3. **Design.md** — palet warna (hex), tipografi, style komponen global (tombol/input/card), layout guide (mobile-first/grid).
4. **Schema.md** — daftar tabel, kolom+tipe data, relasi (1:1/1:N/N:N), constraints (unique/not-null).
5. **Rules.md** — naming convention (var/fungsi/file/komponen), aturan framework spesifik, error handling + standar respons API.
6. **API_Contract.md** — tiap endpoint: method+URL, request payload, response sukses (JSON), response error+status HTTP.
7. **Tasks.md** — checklist `- [ ]` per fase, berurutan, granular, executor-friendly.
8. **Tests.md** — acceptance criteria per fitur utama, skenario manual test.
9. **Context.md** — masalah dunia nyata yang diselesaikan, business logic rules.
10. **debug.md** — kosong di awal, cuma format template: Tanggal | Gejala | Penyebab | Solusi.

## Workflow

1. Info project kurang → tanya Boss (nama, satu-liner, tech stack, target user). Jangan lanjut kalau ambigu.
2. Draft ke-10 file SEKALIGUS sebagai satu synthesis pass — bukan satu-satu berurutan — biar cross-reference (Schema↔API_Contract, PRD↔Tasks) konsisten sejak awal, bukan ditambal belakangan.
3. Delegasikan ke **executor** dalam SATU brief: isi lengkap ke-10 file, target path `docs/` di root project aktif (cwd sekarang — BUKAN folder farewell-orchestra), instruksi "tulis persis, jangan ubah struktur".
4. Executor beres → generate `sub-project.md` dari `templates/sub-project.md` (cari dari root repo tempat skill ini dipanggil, relative path dari cwd), isi placeholder, tandai semua row docs jadi ✅.
5. Report ke Boss: "10/10 docs dibuat di {project}/docs/. sub-project.md siap." — 3 baris max.

## Update Mode (project existing)

Kalau `sub-project.md` udah ada — JANGAN generate ulang dari nol. Baca dulu, tanya Boss bagian mana yang mau di-update, edit incremental lewat executor, update baris "Terakhir update" di `sub-project.md` yang relevan aja.
