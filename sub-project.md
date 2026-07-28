# Sub-Project: farewell-orchestra

> Anchor file. Orchestrator baca ini DULUAN di awal tiap sesi sebelum kerja apapun.
> Auto-generated oleh skill `bootstrap-project`, di-update executor tiap ada perubahan fase/docs.

## Ringkasan
- **Nama:** farewell-orchestra
- **Satu kalimat:** Agent orchestration framework (orchestrator, researcher, reviewer, executor) untuk software house mini.
- **Path absolut:** C:\Users\FANNNDI\Documents\farewell-orchestra
- **Repo:** https://github.com/anomalyco/farewell-orchestra
- **Profile:** hybrid
- **Fase:** stable — detail di `docs/Tasks.md`
- **Task aktif:** maintain orchestrator framework

## Dokumen (`docs/`)

| File | Status | Terakhir update |
|------|--------|-----------------|
| PRD.md | ❌ | — |
| Architecture.md | ✅ | 2026-07-28 |
| Design.md | ✅ | 2026-07-28 |
| Schema.md | ❌ | — |
| Rules.md | ✅ | 2026-07-28 |
| API_Contract.md | ❌ | — |
| Tasks.md | ✅ | 2026-07-28 |
| Tests.md | ❌ | — |
| Context.md | ✅ | 2026-07-28 |
| debug.md | ✅ | 2026-07-28 |

## Konteks Bisnis Singkat
Farewell Orchestra adalah framework agent orchestration untuk software house mini: 4 agent (orchestrator, researcher, reviewer, executor) dengan skill khusus (anti-gigo, forensic, stride-audit, minimal-impl, verification-ground-truth) + slash commands (/check, /new-project, /work-on). Digunakan cross-project via path reference.

## Task Aktif
Maintain orchestrator framework (agents, skills, commands, templates, config profiles)

## Memori Agent

| Agent | Konteks | File kunci |
|-------|---------|------------|
| orchestrator | Validasi input, dekomposisi task, delegasi parallel, sintesis hasil | AGENTS.md, .opencode/agents/orchestrator.md |
| researcher | Investigasi codebase, forensic debug, tech stack research, web research | .opencode/agents/researcher.md, .opencode/skills/forensic.md |
| reviewer | STRIDE audit, convention enforcement, cross-file drift detection | .opencode/agents/reviewer.md, .opencode/skills/stride-audit.md |
| executor | YAGNI-first implementasi, verification-ground-truth, error healing mandiri, update sub-project.md | .opencode/agents/executor.md, .opencode/skills/minimal-impl.md, sub-project.md |
