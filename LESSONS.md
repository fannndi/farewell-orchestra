# Lessons Learned

> Auto-log oleh orchestrator via executor setiap insiden non-trivial (architectural fix, systemic bug, pattern detection).
> Skip typo/trivial. Satu baris per entry.

| date | trigger | error | root cause | fix |
|------|---------|-------|------------|-----|
| — | — | — | — | — |
| 2026-07-29 | Cross-project optimasi — audit 10 gaps + 3 BLOCKING | project-guide.md missing, templates/ missing, LESSONS.md missing, hardcode path, profile mismatch, permission boundary lemah, path traversal tanpa proteksi | Dokumentasi janji vs realita: file referenced tapi tidak ada. Path resolution tanpa sanitasi. Permission boundary global-only. | Bikin 3 file baru (project-guide, templates/sub-project, LESSONS). Fix orchestrator.md step 0 dengan path traversal protection + audit log. Update opencode.jsonc, bootstrap-project skill, AGENTS.md, README.md. Hapus helper-mode/ stale. |
