# Sub-Project: {{PROJECT_NAME}}

> Anchor file. Orchestrator baca ini DULUAN di awal tiap sesi sebelum kerja apapun.
> Auto-generated oleh skill `bootstrap-project`, di-update executor tiap ada perubahan fase/docs.

## Ringkasan
- **Nama:** {{PROJECT_NAME}}
- **Satu kalimat:** {{ONE_LINER}}
- **Path absolut:** {{PROJECT_PATH}}
- **Repo:** {{REPO_URL}}
- **Profile:** {{PROFILE}} (paid | hybrid | free)
- **Fase:** {{CURRENT_PHASE}} — detail di `docs/Tasks.md`
- **Task aktif:** {{ACTIVE_TASK}}

## Dokumen (`docs/`)

| File | Status | Terakhir update |
|------|--------|-----------------|
| PRD.md | ⬜ | — |
| Architecture.md | ⬜ | — |
| Design.md | ⬜ | — |
| Schema.md | ⬜ | — |
| Rules.md | ⬜ | — |
| API_Contract.md | ⬜ | — |
| Tasks.md | ⬜ | — |
| Tests.md | ⬜ | — |
| Context.md | ⬜ | — |
| debug.md | ⬜ | — |

## Konteks Bisnis Singkat
{{2-3 kalimat ringkasan dari Context.md — bukan copy paste, biar anchor ini tetep ringan}}

## Task Aktif
{{task yang lagi dikerjakan sekarang, sinkron sama checklist di Tasks.md}}

## Memori Agent

| Agent | Konteks | File kunci |
|-------|---------|------------|
| orchestrator | {{ORCH_CTX}} | — |
| researcher | {{RESEARCH_CTX}} | {{RESEARCH_FILES}} |
| reviewer | {{REVIEW_CTX}} | {{REVIEW_FILES}} |
| executor | {{EXEC_CTX}} | {{EXEC_FILES}} |

*Diupdate executor tiap selesai task. Bukan log lengkap — cukup 1 kalimat konteks terakhir + file yg sering disentuh.*
