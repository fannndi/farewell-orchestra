---
name: bootstrap-project
description: Use when starting work on a sub-project — generate docs via reverse engineering or update existing.
---

# Bootstrap Project Docs

Dipakai orchestrator saat mulai kerja di project lain. Dua mode:

## Mode 1: Project Baru (ada ide, belum ada kode)

Kalau user kasih ide project baru:
1. Info project kurang → tanya Boss (nama, satu-liner, tech stack, target user)
2. Draft 5 core docs + 2 conditional SEKALIGUS (bukan satu-satu)
3. Delegasikan ke executor dalam SATU brief
4. Generate sub-project.md dari template
5. Report: "5/5 core docs dibuat. sub-project.md siap."

## Mode 2: Project Existing (ada kode, belum ada docs)

Ini **Reverse Engineering Mode**. Dipanggil dari prepare §0.

1. Dispatch researcher untuk deep scan (lihat cross-project/guide.md Phase 1-5)
2. Dispatch executor untuk generate docs dari findings researcher
3. Consistency check: Schema↔API_Contract, PRD↔Tasks
4. Report: "Docs generated dari reverse engineering. Review?"

## 5 Core Docs (WAJIB)

| Doc | Isi |
|-----|-----|
| **PRD.md** | Latar belakang, scope, MVP, target user, fitur in/out, user flow |
| **Architecture.md** | Tech stack, directory tree, alur data, keputusan + alasan |
| **Rules.md** | Naming convention, error handling, coding standards |
| **Tasks.md** | Checklist `- [ ]` per fase, berurutan, granular |
| **Context.md** | Konteks bisnis, business rules, background story |

## 2 Conditional Docs

| Doc | Generate Kalau |
|-----|---------------|
| **Schema.md** | Project pakai database (tabel, kolom, relasi, constraints) |
| **API_Contract.md** | Project pakai API (endpoint, method, request, response) |

## Consistency Rules

- Nama variabel/tabel di Schema.md = nama field di API_Contract.md
- Tech stack di Architecture.md = konvensi di Rules.md
- Fitur di PRD.md = task di Tasks.md = acceptance di Tasks.md

## Update Mode (project existing + docs ada)

Kalau docs udah ada — JANGAN generate ulang. Baca dulu, tanya Boss bagian mana yang mau di-update, edit incremental.

## Proactive

- Orchestrator: kalau researcher lapor project tanpa docs → trigger reverse engineering
- Executor gagal di tengah generate → re-dispatch file yang gagal aja, jangan ulang semua
