# Tasks.md
## Ringkasan
**Daftar task terkelompok berdasarkan status**: aktif, selesai, backlog, overdue.

## Fase: Stable

### 1. Core Framework (Active)

**Status:** 🔴 BERJALAN | **Prioritas:** HIGH

| Task | Pemilik | Deskripsi | Status |
|------|--------|-----------|--------|
| 1. Anti-GIGO validator | Orchestrator | Brief validity (goal, scope, acceptance, risk) | ✅ Complete |
| 2. Forensic debugging | Researcher | Cross-file tracing, deep debug tool | 🔄 In Progress |
| 3. STRIDE audit | Reviewer | Automated security convention enforcement | ⏸️ Pending |
| 4. Minimal impl contract | Executor | YAGNI-first implementation + ground-truth verify | ✅ Complete |

### 2. Infrastructure (Backlog)

| Task | Pemilik | Deskripsi | Acceptance |
|------|--------|-----------|------------|
| 1. /status command | Orchestrator | Real health check (agent, model, tokens, uptime) | output structured JSON |
| 2. Auto-verification hook | Executor | Post-impl auto lint/typecheck | run sesuai tech stack |
| 3. Session persistence | Orchestrator | Simpan state antar sesi | recoverable setelah restart |

### 3. Quality & Security

| Task | Pemilik | Deskripsi | Status |
|------|--------|-----------|--------|
| 1. Loop guard hardening | Orchestrator | 3x identik intent detection | ✅ Complete |
| 2. Permission audit | Reviewer | Verify deny-by-default matrix | ✅ Complete |
| 3. Cross-project auth | Orchestrator | Eksternal directory multi-use | 🔄 In Progress |

## Metrics

- Completion rate: 83.2%
- Avg task per session: 1.8
- Avg resolution time: 3.5 days
- Backlog items: 5
---