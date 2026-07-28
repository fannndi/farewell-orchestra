# # Architecture.md

## Ringkasan
Dibangun di atas OpenCode framework, sistem ini mengimplementasikan **4-agent AI orchestration** untuk otomatisasi pengembangan software. Arsitektur mengikuti prinsip anti-GIGO dengan validasi input yang ketat, delegasi tugas yang jelas, dan audit keamanan yang enforce-konvensi.

## Komponen
- **Orchestrator Agent** — Pengalokasi task, validator input, dan Socratic requirement extractor
- **Researcher Agent** — Investigator codebase & dokumentasi read-only, penambang tech stack
- **Reviewer Agent** — Auditor STRIDE & audit konvensi, cross-file drift detection
- **Executor Agent** — Pembuat kode YAGNI-first, implementasi verifikasi-ground-truth

## Skill System
8 native skills: anti-gigo, grill, orchestrate, minimal-impl, verification-ground-truth, forensic, web-research, stride-audit

## Fleksibilitas Profile
3 tier: paid (maksimum performa), hybrid (campuran kost-efficient), free (tanpa biaya)

## Integritas Data
Sub-project.md sebagai file anchor, update eksekutor per fase, struktur task terstruktur

## Keselamatan & Pemantauan
Loop guard (3x), step budget, escalation (executor gagal 2x), loop guard, verificator berbasis output, grill gate, permission deny-by-default

## Integrasi Proyek Silang
Dapat beralih context antar proyek pakai pattern `/work-on`. Orchestrator treat path target sebagai root workspace.

## Kekuatan
- Anti-GIGO enforcement
- YAGNI-first implementation
- Parallel processing (researcher + reviewer)
- Cost-benefit gating (TRIVIAL → COMPLEX)
- Circuit breaker: executor gagal 2x -> researcher deep debug
- Loop guard & step budget
- Peer debate mode buat high-stakes verification
- Mandatory reporting: 3 baris per output (what, result, residual risk)
---