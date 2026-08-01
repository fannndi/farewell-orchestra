---
name: bootstrap-project
description: Use when Boss starts a new sub-project or says 'bikin dokumentasi project baru' — generate 10 interconnected project docs plus sub-project.md anchor.
---

> Cost Model: free sub-agent — read-only (kecuali executor). Writes → dispatch executor. Orchestrator never writes code.

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
4. Executor beres → generate `sub-project.md` dari `templates/sub-project.md`. Template source: `{orchestra_root}/templates/sub-project.md` (root repo farewell-orchestra). Orchestrator resolve path absolut SEBELUM dispatch executor. Isi placeholder, tandai semua row docs jadi [PASS].
5. Report ke Boss: "10/10 docs dibuat di {project}/docs/. sub-project.md siap." — 3 baris max.

## Update Mode (project existing)

Kalau `sub-project.md` udah ada — JANGAN generate ulang dari nol. Baca dulu, tanya Boss bagian mana yang mau di-update, edit incremental lewat executor, update baris "Terakhir update" di `sub-project.md` yang relevan aja.
